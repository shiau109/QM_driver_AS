"""
        CRYOSCOPE
The goal of this protocol is to measure the step response of the flux line and design proper FIR and IIR filters
(implemented on the OPX) to pre-distort the flux pulses and improve the two-qubit gates fidelity.
Since the flux line ends on the qubit chip, it is not possible to measure the flux pulse after propagation through the
fridge. The idea is to exploit the flux dependency of the qubit frequency, measured with a modified Ramsey sequence, to
estimate the flux amplitude received by the qubit as a function of time.

The sequence consists of a Ramsey sequence ("x90" - idle time - "x90" or "y90") with a fixed dephasing time.
A flux pulse with varying duration is played during the idle time. The Sx and Sy components of the Bloch vector are
measured by alternatively closing the Ramsey sequence with a "x90" or "y90" gate in order to extract the qubit dephasing
 as a function of the flux pulse duration.

The results are then post-processed to retrieve the step function of the flux line which is fitted with an exponential
function. The corresponding exponential parameters are then used to derive the FIR and IIR filter taps that will
compensate for the distortions introduced by the flux line (wiring, bias-tee...).
Such digital filters are then implemented on the OPX. Note that these filters will introduce a global delay on all the
output channels that may rotate the IQ blobs so that you may need to recalibrate them for state discrimination or
active reset protocols for instance. You can read more about these filters here:
https://docs.quantum-machines.co/0.1/qm-qua-sdk/docs/Guides/output_filter/?h=filter#hardware-implementation

The protocol is inspired from https://doi.org/10.1063/1.5133894, which contains more details about the sequence and
the post-processing of the data.

This version sweeps the flux pulse duration using the baking tool, which means that the flux pulse can be scanned with
a 1ns resolution, but must be shorter than ~260ns. If you want to measure longer flux pulse, you can either reduce the
resolution (do 2ns steps instead of 1ns) or use the 4ns version (cryoscope_4ns.py).

Prerequisites:
    - Having found the resonance frequency of the resonator coupled to the qubit under study (resonator_spectroscopy).
    - Having calibrated qubit gates (x90 and y90) by running qubit spectroscopy, rabi_chevron, power_rabi, Ramsey and updated the configuration.

Next steps before going to the next node:
    - Update the FIR and IIR filter taps in the configuration (config/controllers/con1/analog_outputs/"filter": {"feedforward": fir, "feedback": iir}).
"""

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
from qualang_tools.bakery import baking
import warnings

warnings.filterwarnings("ignore")

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


def baked_waveform(waveform, pulse_duration, qubit_index):
    pulse_segments = []  
    for i in range(0, pulse_duration + 1):
        with baking(config, padding_method="right") as b:
            if i == 0:  
                wf = [0.0] * 16
            else:
                wf = waveform[:i].tolist()
            b.add_op("flux_pulse", f"q{qubit_index}_z", wf)
            b.play("flux_pulse", f"q{qubit_index}_z")
        pulse_segments.append(b)
    return pulse_segments

def short_cryoscope(flux_Qi,resonator,cryo_const_flux_len,simulate,qmm):
    with program() as cryoscope:
        I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(resonator))
        segment = declare(int)  
        flag = declare(bool)  
        state = [declare(bool) for _ in range(len(resonator))]
        state_st = [declare_stream() for _ in range(len(resonator))]

        with for_(n, 0, n < n_avg, n + 1):
            with for_(segment, 0, segment <= cryo_const_flux_len, segment + 1):
                with for_each_(flag, [True, False]):

                    if not simulate: wait(thermalization_time * u.ns)
                    play("x90", f"q{flux_Qi}_xy")
                    align()
                    wait(200 * u.ns)
                    with switch_(segment):
                        for j in range(0, len(flux_waveform) + 1):
                            with case_(j):
                                square_pulse_segments[j].run()
                    # Wait for the idle time set slightly above the maximum flux pulse duration to ensure that the 2nd x90
                    # pulse arrives after the longest flux pulse
                    align()
                    wait(200 * u.ns)
                    # wait((len(flux_waveform) + 20) * u.ns, f"q{flux_Qi}_xy")
                    with if_(flag):
                        play("x90", f"q{flux_Qi}_xy")
                    with else_():
                        play("y90", f"q{flux_Qi}_xy")
                    align()
                    multiplexed_readout(I, I_st, Q, Q_st, resonators=resonator, weights="rotated_")
                    for i in resonator_index:
                        assign(state[i], I[i] > ge_threshold[resonator[i]-1]) # ge_threshold[1] related to rr2
                        save(state[i], state_st[i])
            save(n, n_st)

        with stream_processing():
            n_st.save("n")
            for i in resonator_index:
                I_st[i].buffer(2).buffer(cryo_const_flux_len + 1).average().save(f"I{i}")
                state_st[i].boolean_to_int().buffer(2).buffer(cryo_const_flux_len + 1).average().save(f"state{i}")                

    if simulate:
        simulation_config = SimulationConfig(duration=40_000) 
        job = qmm.simulate(config, cryoscope, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(cryoscope)
        I_list, state_list = [f"I{i}" for i in resonator_index], [f"state{i}" for i in resonator_index]
        results = fetching_tool(job, I_list + state_list + ["n"], mode="live")
        fig = plt.figure()
        interrupt_on_close(fig, job)  #  Interrupts the job when closing the figure
        while results.is_processing():
            # Fetch results
            all_results = results.fetch_all()
            n = all_results[-1]
            I, state = all_results[0:len(resonator)], all_results[len(resonator):len(resonator)*2]
            I = u.demod2volts(I[resonator.index(flux_Qi)], readout_len)
            state = np.array(state[resonator.index(flux_Qi)])
            progress_counter(n, n_avg, start_time=results.start_time)
            # Bloch vector Sx + iSy
            ############   The state is the result of qubit state population with average number: n_avg. It should be in a range [0,1].
            ############   Sxx and Syy should be in a range of [-1,1].
            Sxx = state[:, 0] * 2 - 1
            Syy = state[:, 1] * 2 - 1
            S = Sxx + 1j * Syy
            phase = np.unwrap(np.angle(S))
            phase = phase - phase[-1]
            detuning = signal.savgol_filter(phase / 2 / np.pi, 21, 2, deriv=1, delta=0.001)
            step_response_freq = detuning / np.average(detuning[-int(cryo_const_flux_len / 2) :])
            step_response_volt = np.sqrt(step_response_freq)
            live_plotting(state,phase,detuning)
        qm.close()
        return I, state, phase, detuning, step_response_freq, step_response_volt

def live_plotting(state,phase,detuning):
    plt.subplot(131)
    plt.cla()
    plt.plot(xplot, state)
    plt.xlabel("Pulse duration [ns]")
    plt.ylabel("state population")
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

def fitting(xplot,step_response_volt,step_response_th):
    [A, tau], _ = optimize.curve_fit(
        exponential_decay,
        xplot,
        step_response_volt,
    )
    print(f"A: {A}\ntau: {tau}")
    fir, iir = filter_calc(exponential=[(A, tau)])
    print(f"FIR: {fir}\nIIR: {iir}")
    no_filter = exponential_decay(xplot, A, tau)
    with_filter = no_filter * signal.lfilter(fir, [1, iir[0]], step_response_th) 
    return A, tau, fir, iir, no_filter, with_filter

def step_response_plot(A, tau, fir, iir, no_filter, with_filter):
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

flux_Qi = 2
resonator = [2,3]   ###  [2,3] means measuring rr2 and rr3
resonator_index = [resonator.index(i) for i in resonator]
cryo_const_flux_len = 200
cryo_const_flux_amp = 0.06
n_avg = 1_000 
simulate = False
flux_waveform = np.array( [cryo_const_flux_amp] * cryo_const_flux_len )
square_pulse_segments = baked_waveform(flux_waveform, len(flux_waveform), flux_Qi)
step_response_th = ( [1.0] * (cryo_const_flux_len + 1) ) 
xplot = np.arange(0, len(flux_waveform) + 1, 1)  
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
I, state, phase, detuning, step_response_freq, step_response_volt = short_cryoscope(flux_Qi,resonator,cryo_const_flux_len,simulate,qmm)
A, tau, fir, iir, no_filter, with_filter = fitting(xplot,step_response_volt,step_response_th)
step_response_plot(A, tau, fir, iir, no_filter, with_filter)

import xarray as xr

coords = {'flux duration': xplot}  # 定义坐标
dims = ['flux duration']  # 定义维度
state_x90 = xr.DataArray(state[:,0], coords=coords, dims=dims)
state_y90 = xr.DataArray(state[:,1], coords=coords, dims=dims)
state_phase = xr.DataArray(phase, coords=coords, dims=dims)
state_detuning = xr.DataArray(detuning, coords=coords, dims=dims)
step_response_freq = xr.DataArray(step_response_freq, coords=coords, dims=dims)
step_response_volt = xr.DataArray(step_response_volt, coords=coords, dims=dims)

ds = xr.Dataset({
    'state_x90':state_x90,
    'state_y90':state_y90,
    'state_phase':state_phase,
    'state_detuning':state_detuning,
    'step_response_freq':step_response_freq,
    'step_response_volt':step_response_volt
    },
    coords=coords
) 
ds.to_netcdf("short_cryo.nc", engine='netcdf4', format='NETCDF4')