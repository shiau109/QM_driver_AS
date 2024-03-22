import xarray as xr
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal, optimize

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


ds = xr.load_dataset('long_cryo_with_filter.nc')
state_phase = ds.state_phase
state_x90 = ds.state_x90
state_y90 = ds.state_y90
state_detuning = ds.state_detuning
step_response_volt = ds.step_response_volt
step_response_freq = ds.step_response_freq
xplot = ds.coords['flux duration']
step_response_th = [1.0] * len(xplot)

ds2 = xr.load_dataset('long_cryo_without_filter.nc')
state2_phase = ds2.state_phase
state2_x90 = ds2.state_x90
state2_y90 = ds2.state_y90
state2_detuning = ds2.state_detuning
step2_response_volt = ds2.step_response_volt
step2_response_freq = ds2.step_response_freq
xplot2 = ds2.coords['flux duration']

ds3 = xr.load_dataset('short_cryo_with_filter.nc')
state3_phase = ds3.state_phase
state3_x90 = ds3.state_x90
state3_y90 = ds3.state_y90
state3_detuning = ds3.state_detuning
step3_response_volt = ds3.step_response_volt
step3_response_freq = ds3.step_response_freq
xplot3 = ds3.coords['flux duration']

ds4 = xr.load_dataset('short_cryo_without_filter.nc')
state4_phase = ds4.state_phase
state4_x90 = ds4.state_x90
state4_y90 = ds4.state_y90
state4_detuning = ds4.state_detuning
step4_response_volt = ds4.step_response_volt
step4_response_freq = ds4.step_response_freq
xplot4 = ds4.coords['flux duration']
cryo_const_flux_len = 200

plt.title('With filter')
plt.plot(xplot3, state3_detuning, label = 'short pulse with filter')
plt.plot(xplot, state_detuning, label = 'long pulse with filter')
plt.legend()
plt.show()

plt.title('Without filter')
plt.plot(xplot4, state4_detuning, label = 'short pulse without filter')
plt.plot(xplot2, state2_detuning, label = 'long pulse without filter')
plt.legend()
plt.show()

plt.title('long pulse')
plt.plot(xplot, state_detuning, label = 'long pulse with filter')
plt.plot(xplot2, state2_detuning, label = 'long pulse without filter')
plt.legend()
plt.show()

plt.title('short pulse')
plt.plot(xplot3, state3_detuning, label = 'short pulse with filter')
plt.plot(xplot4, state4_detuning, label = 'short pulse without filter')
plt.legend()
plt.show()

plt.subplot(211)
state_phase.plot(label='phase')
plt.xlabel('')
plt.legend()
plt.subplot(212)
state_detuning.plot(label='detuning')
plt.legend()
plt.show()

plt.subplot(211)
step_response_volt.plot(label = 'response_volt')
plt.xlabel('')
plt.legend()
plt.subplot(212)
step_response_freq.plot(label = 'response_freq')
plt.legend()
plt.show()

A, tau, fir, iir, no_filter, with_filter = fitting(xplot,step_response_volt,step_response_th)
step_response_plot(A, tau, fir, iir, no_filter, with_filter)