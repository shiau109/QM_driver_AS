from qm.qua import *
from qm import QuantumMachinesManager


from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.bakery import baking

from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save


from scipy import signal, optimize
import matplotlib.pyplot as plt

from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
import xarray as xr
import time


####################
# Helper functions #
####################
def exponential_decay(x, a, t):
    """Exponential decay defined as 1 + a * np.exp(-x / t).

    :param x: numpy array for the time vector in ns
    :param a: float for the exponential amplitude
    :param t: float for the exponential decay time in ns
    :return: numpy array for the exponential decay
    """
    return 1 + a * np.exp(-x / t)


def exponential_correction(A, tau, Ts=1e-9):
    """Derive FIR and IIR filter taps based on the exponential coefficients A and tau from 1 + a * np.exp(-x / t).

    :param A: amplitude of the exponential decay.
    :param tau: decay time of the exponential decay
    :param Ts: sampling period. Default is 1e-9
    :return: FIR and IIR taps
    """
    tau = tau * Ts
    k1 = Ts + 2 * tau * (A + 1)
    k2 = Ts - 2 * tau * (A + 1)
    c1 = Ts + 2 * tau
    c2 = Ts - 2 * tau
    feedback_tap = k2 / k1
    feedforward_taps = np.array([c1, c2]) / k1
    return feedforward_taps, feedback_tap


def filter_calc(exponential):
    """Derive FIR and IIR filter taps based on a list of exponential coefficients.

    :param exponential: exponential coefficients defined as [(A1, tau1), (A2, tau2)]
    :return: FIR and IIR taps as [fir], [iir]
    """
    # Initialization based on the number of exponential coefficients
    b = np.zeros((2, len(exponential)))
    feedback_taps = np.zeros(len(exponential))
    # Derive feedback tap for each set of exponential coefficients
    for i, (A, tau) in enumerate(exponential):
        b[:, i], feedback_taps[i] = exponential_correction(A, tau)
    # Derive feedback tap for each set of exponential coefficients
    feedforward_taps = b[:, 0]
    for i in range(len(exponential) - 1):
        feedforward_taps = np.convolve(feedforward_taps, b[:, i + 1])
    # feedforward taps are bounded to +/- 2
    if np.abs(max(feedforward_taps)) >= 2:
        feedforward_taps = 2 * feedforward_taps / max(feedforward_taps)

    return feedforward_taps, feedback_taps


def baked_waveform(waveform, pulse_duration, z_element, config):
    pulse_segments = []  # Stores the baking objects
    # Create the different baked sequences, each one corresponding to a different truncated duration
    for i in range(0, pulse_duration + 1):
        with baking(config, padding_method="right") as b:
            if i == 0:  # Otherwise, the baking will be empty and will not be created
                wf = [0.0] * 16
            else:
                wf = waveform[:i].tolist()
            b.add_op("flux_pulse", z_element, wf)
            b.play("flux_pulse", z_element)
        # Append the baking object in the list to call it from the QUA program
        pulse_segments.append(b)
    return pulse_segments




def cryoscope_bk( ro_element, xy_element, z_element, const_flux_amp, const_flux_len, n_avg, config, qmm:QuantumMachinesManager, initializer=None, pad_zeros=(0,0)):

    # Flag to set to True if state discrimination is calibrated (where the qubit state is inferred from the 'I' quadrature).
    # Otherwise, a preliminary sequence will be played to measure the averaged I and Q values when the qubit is in |g> and |e>.
    state_discrimination = False
    # FLux pulse waveform generation
    # The zeros are just here to visualize the rising and falling times of the flux pulse. they need to be set to 0 before
    # fitting the step response with an exponential.
    zeros_before_pulse = pad_zeros[0]  # Beginning of the flux pulse (before we put zeros to see the rising time)
    zeros_after_pulse = pad_zeros[1]  # End of the flux pulse (after we put zeros to see the falling time)
    total_zeros = zeros_after_pulse + zeros_before_pulse
    flux_waveform = np.array([0.0] * zeros_before_pulse + [const_flux_amp] * const_flux_len + [0.0] * zeros_after_pulse)

    # Baked flux pulse segments with 1ns resolution
    square_pulse_segments = baked_waveform(flux_waveform, len(flux_waveform), z_element, config)
    step_response_th = (
        [0.0] * zeros_before_pulse + [1.0] * (const_flux_len + 1) + [0.0] * zeros_after_pulse
    )  # Perfect step response (square)
    xplot = np.arange(0, len(flux_waveform) + 1, 1)  # x-axis for plotting - Must be in ns.
    qua_prog = qua_cryoscope_bk( ro_element, xy_element, flux_waveform, square_pulse_segments, const_flux_len, total_zeros, n_avg, initializer=initializer )


    # Open the quantum machine
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(qua_prog)
    # Get results from QUA program
    ro_ch_name = []
    for r_name in ro_element:
        ro_ch_name.append(f"{r_name}_I")
        ro_ch_name.append(f"{r_name}_Q")
    data_list = ro_ch_name + ["iteration"]   
    results = fetching_tool(job, data_list=data_list, mode="live")
    # Live plotting
    while results.is_processing():
        # Fetch results
        fetch_data = results.fetch_all()
        # Progress bar
        iteration = fetch_data[-1]
        progress_counter(iteration, n_avg, start_time=results.get_start_time())
        time.sleep(1)
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    fetch_data = results.fetch_all()
    qm.close()
    output_data = {}

    for r_idx, r_name in enumerate(ro_element):
        output_data[r_name] = ( ["mixer","time", "r90"],
                            np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
    dataset = xr.Dataset(
        output_data,
        coords={ "mixer":np.array(["I","Q"]), "time": xplot, "r90":np.array(["x","y"]) }
    )
    transposed_data = dataset.transpose("mixer", "r90", "time")

    return transposed_data

def qua_cryoscope_bk(  ro_element, xy_element, flux_waveform, square_pulse_segments, const_flux_len, total_zeros, n_avg, ge_threshold=None, initializer=None ):
    """
    QUA FPGA
    """
    with program() as cryoscope:
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)  # QUA variable for the averaging loop
        segment = declare(int)  # QUA variable for the flux pulse segment index
        flag = declare(bool)  # QUA boolean to switch between x90 and y90
        
        # if ge_threshold is not None:
        #     state = declare(bool)
        #     state_st = declare_stream()

        n_st = declare_stream()  # Stream for the averaging iteration 'n'

        # Outer loop for averaging
        with for_(n, 0, n < n_avg, n + 1):
            # Loop over the truncated flux pulse
            with for_(segment, 0, segment <= const_flux_len + total_zeros, segment + 1):
                # Alternate between X/2 and Y/2 pulses
                with for_each_(flag, [True, False]):

                    # Init
                    if initializer is None:
                        wait(100*u.us)
                        #wait(thermalization_time * u.ns)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            print("Initializer didn't work!")
                            wait(100*u.us)

                    # Play first X/2
                    play("x90", xy_element)
                    # Play truncated flux pulse
                    align()
                    # Wait some time to ensure that the flux pulse will arrive after the x90 pulse
                    wait(20 * u.ns)
                    with switch_(segment):
                        for j in range(0, len(flux_waveform) + 1):
                            with case_(j):
                                square_pulse_segments[j].run()
                    # Wait for the idle time set slightly above the maximum flux pulse duration to ensure that the 2nd x90
                    # pulse arrives after the longest flux pulse
                    wait((len(flux_waveform) + 20) * u.ns, xy_element)
                    # Play second X/2 or Y/2
                    with if_(flag):
                        play("x90", xy_element)
                    with else_():
                        play("y90", xy_element)
                    # Measure resonator state after the sequence
                    align()
                    
                    multiRO_measurement(iqdata_stream, ro_element, weights="rotated_") 
                    
            save(n, n_st)

        with stream_processing():
            # Cast the data into a 2D matrix (x90/y90, flux pulse length), average the 2D matrices together and store the
            # results on the OPX processor
            n_st.save("iteration")
            multiRO_pre_save(iqdata_stream, ro_element, (const_flux_len + total_zeros + 1, 2) )

    return cryoscope

def plot( xplot, step_response_volt ):
    ## Fit step response with exponential
    [A, tau], _ = optimize.curve_fit(
        exponential_decay,
        xplot,
        step_response_volt,
    )
    print(f"A: {A}\ntau: {tau}")

    ## Derive IIR and FIR corrections
    fir, iir = filter_calc(exponential=[(A, tau)])
    print(f"FIR: {fir}\nIIR: {iir}")

    ## Derive responses and plots
    # Response without filter
    no_filter = exponential_decay(xplot, A, tau)
    # Response with filters
    # with_filter = no_filter * signal.lfilter(fir, [1, iir[0]], step_response_th)  # Output filter , DAC Output

    # Plot all data
    plt.rcParams.update({"font.size": 13})
    plt.figure()
    plt.suptitle("Cryoscope with filter implementation")
    plt.plot(xplot, step_response_volt, "o-", label="Experimental data")
    plt.plot(xplot, no_filter, label="Fitted response without filter")
    # plt.plot(xplot, with_filter, label="Fitted response with filter")
    # plt.plot(xplot, step_response_th, label="Ideal WF")  # pulse
    # plt.text(
    #     max(xplot) // 2,
    #     max(step_response_volt) / 2,
    #     f"IIR = {iir}\nFIR = {fir}",
    #     bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    # )
    # plt.text(
    #     max(xplot) // 4,
    #     max(step_response_volt) / 2,
    #     f"A = {A:.2f}\ntau = {tau:.2f}",
    #     bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    # )
    plt.xlabel("Flux pulse duration [ns]")
    plt.ylabel("Step response")
    plt.legend(loc="upper right")
    plt.tight_layout()

