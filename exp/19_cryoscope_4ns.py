from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *
from scipy import signal, optimize
import matplotlib.pyplot as plt
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.plot import interrupt_on_close
import numpy as np
from macros import qua_declaration, multiplexed_readout
from qualang_tools.loops import from_array
import warnings

warnings.filterwarnings("ignore")

simulate = False

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


###################
# The QUA program #
###################
# Index of the qubit to measure
qubit = 2
cryo_const_flux_len = 200
cryo_const_flux_amp = 0.12 / const_flux_amp
n_avg = 1_000  # Number of averages
# Flux pulse durations in clock cycles (4ns) - must be > 4 or the pulse won't be played.
durations = np.arange(4, cryo_const_flux_len // 4, 1)  # Starts at 3 clock-cycles to have the first point without pulse.
flux_waveform = np.array([cryo_const_flux_amp] * max(durations))
xplot = durations * 4  # x-axis for plotting and deriving the filter taps - must be in ns.
step_response_th = [1.0] * len(xplot)  # Perfect step response (square)


with program() as cryoscope:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=4)
    t = declare(int)  # QUA variable for the flux pulse duration
    flag = declare(bool)  # QUA boolean to switch between x90 and y90
    state = [declare(bool) for _ in range(4)]
    state_st = [declare_stream() for _ in range(4)]

    # Outer loop for averaging
    with for_(n, 0, n < n_avg, n + 1):
        # Loop over the truncated flux pulse
        with for_(*from_array(t, durations)):
            # Alternate between X/2 and Y/2 pulses
            with for_each_(flag, [True, False]):
                # Wait cooldown time and save the results
                if not simulate: wait(thermalization_time * u.ns)
                # Play first X/2
                play("x90", f"q{qubit}_xy")
                # Play truncated flux pulse
                align()
                # Wait some time to ensure that the flux pulse will arrive after the x90 pulse
                wait(200 * u.ns)
                # Play the flux pulse only if t is larger than the minimum of 4 clock cycles (16ns)
                play("const" * amp(cryo_const_flux_amp), f"q{qubit}_z", duration=t)
                # Wait for the idle time set slightly above the maximum flux pulse duration to ensure that the 2nd x90
                # pulse arrives after the longest flux pulse
                # wait((len(flux_waveform) + 20) * u.ns, f"q{qubit}_xy")
                align()
                wait( 200 * u.ns)
                # Play second X/2 or Y/2
                with if_(flag):
                    play("x90", f"q{qubit}_xy")
                with else_():
                    play("y90", f"q{qubit}_xy")
                # Measure resonator state after the sequence
                align()
                multiplexed_readout(I, I_st, Q, Q_st, resonators=[1, 2, 3, 4], weights="rotated_")
                # State discrimination
                assign(state[0], I[0] > ge_threshold[0])
                assign(state[1], I[1] > ge_threshold[1])
                assign(state[2], I[2] > ge_threshold[2])
                assign(state[3], I[3] > ge_threshold[3])
                save(state[0], state_st[0])
                save(state[1], state_st[1])
                save(state[2], state_st[2])
                save(state[3], state_st[3])

        save(n, n_st)

    with stream_processing():
        # for the progress counter
        n_st.save("n")
        # resonator 1
        I_st[0].buffer(2).buffer(len(durations)).average().save("I1")
        Q_st[0].buffer(2).buffer(len(durations)).average().save("Q1")
        state_st[0].boolean_to_int().buffer(2).buffer(len(durations)).average().save("state1")
        # resonator 2
        I_st[1].buffer(2).buffer(len(durations)).average().save("I2")
        Q_st[1].buffer(2).buffer(len(durations)).average().save("Q2")
        state_st[1].boolean_to_int().buffer(2).buffer(len(durations)).average().save("state2")
        # resonator 3
        I_st[2].buffer(2).buffer(len(durations)).average().save("I3")
        Q_st[2].buffer(2).buffer(len(durations)).average().save("Q3")
        state_st[2].boolean_to_int().buffer(2).buffer(len(durations)).average().save("state3")
        # resonator 4
        I_st[3].buffer(2).buffer(len(durations)).average().save("I4")
        Q_st[3].buffer(2).buffer(len(durations)).average().save("Q4")
        state_st[3].boolean_to_int().buffer(2).buffer(len(durations)).average().save("state4")

#####################################
#  Open Communication with the QOP  #
#####################################

qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

###########################
# Run or Simulate Program #
###########################

if simulate:
    # Simulates the QUA program for the specified duration
    simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
    job = qmm.simulate(config, cryoscope, simulation_config)
    job.get_simulated_samples().con1.plot()
    plt.show()
else:
    # Open the quantum machine
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(cryoscope)
    # Get results from QUA program
    results = fetching_tool(job, ["n", "I1", "Q1", "state1", "I2", "Q2", "state2", "I3", "Q3", "state3", "I4", "Q4", "state4"], mode="live")
    # Live plotting
    fig = plt.figure()
    interrupt_on_close(fig, job)  #  Interrupts the job when closing the figure
    while results.is_processing():
        # Fetch results
        n, I1, Q1, state1, I2, Q2, state2, I3, Q3, state3, I4, Q4, state4  = results.fetch_all()
        # Convert the results into Volts
        I1, Q1 = u.demod2volts(I1, readout_len), u.demod2volts(Q1, readout_len)
        I2, Q2 = u.demod2volts(I2, readout_len), u.demod2volts(Q2, readout_len)
        I3, Q3 = u.demod2volts(I3, readout_len), u.demod2volts(Q3, readout_len)
        I4, Q4 = u.demod2volts(I4, readout_len), u.demod2volts(Q4, readout_len)
        # Progress bar
        progress_counter(n, n_avg, start_time=results.start_time)
        # Bloch vector Sx + iSy
        ############   The state is the result of qubit state population with average number: n_avg. It should be in a range [0,1].
        ############   Sxx and Syy should be in a range of [-1,1].

        if qubit == 1:
            Sxx = state1[:, 0] * 2 - 1
            Syy = state1[:, 1] * 2 - 1
        elif qubit == 2:
            Sxx = state2[:, 0] * 2 - 1
            Syy = state2[:, 1] * 2 - 1
        elif qubit == 3:
            Sxx = state3[:, 0] * 2 - 1
            Syy = state3[:, 1] * 2 - 1
        elif qubit == 4:
            Sxx = state4[:, 0] * 2 - 1
            Syy = state4[:, 1] * 2 - 1
        else:
            Sxx = 0
            Syy = 0
        S = Sxx + 1j * Syy
        # Accumulated phase: angle between Sx and Sy
        phase = np.unwrap(np.angle(S))
        phase = phase - phase[-1]
        detuning = signal.savgol_filter(phase / 2 / np.pi, 21, 2, deriv=1, delta=0.001)
        step_response_freq = detuning / np.average(detuning[-int(cryo_const_flux_len / 2) :])
        step_response_volt = np.sqrt(step_response_freq)


        plt.subplot(131)
        plt.cla()
        plt.plot(xplot, state2)
        plt.xlabel("Pulse duration [ns]")
        plt.ylabel("I quadrature [V]")
        plt.subplot(132)
        plt.cla()
        plt.plot(xplot, phase)
        plt.xlabel("Pulse duration [ns]")
        plt.ylabel("phase")
        plt.subplot(133)
        plt.cla()
        plt.plot(xplot, detuning)
        plt.xlabel("Pulse duration [ns]")
        plt.ylabel("detuning (MHz)")

        plt.tight_layout()
        plt.pause(0.1)

    print(step_response_volt.shape)
    print(step_response_volt)
    plt.subplot(121)
    plt.cla()
    plt.plot(xplot, I2)
    plt.xlabel("Pulse duration [ns]")
    plt.ylabel("I quadrature [V]")
    plt.subplot(122)
    plt.plot(xplot, step_response_volt, label=r"Voltage ($\sqrt{freq}$)")
    plt.xlabel("Pulse duration [ns]")
    plt.ylabel("Step response")
    plt.tight_layout()
    plt.show()

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
    with_filter = no_filter * signal.lfilter(fir, [1, iir[0]], step_response_th)  # Output filter , DAC Output

    # Plot all data
    plt.rcParams.update({"font.size": 13})
    plt.figure()
    plt.suptitle("Cryoscope with filter implementation")
    plt.plot(xplot, step_response_volt, "o-", label="Experimental data")
    plt.plot(xplot, no_filter, label="Fitted response without filter")
    plt.plot(xplot, with_filter, label="Fitted response with filter")
    plt.plot(xplot, step_response_th, label="Ideal WF")  # pulse
    plt.text(
        max(xplot) // 2,
        max(step_response_volt) / 2,
        f"IIR = {iir}\nFIR = {fir}",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )
    plt.text(
        max(xplot) // 4,
        max(step_response_volt) / 2,
        f"A = {A:.2f}\ntau = {tau:.2f}",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )
    plt.xlabel("Flux pulse duration [ns]")
    plt.ylabel("Step response")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
