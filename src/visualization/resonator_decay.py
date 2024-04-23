
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

from qualang_tools.plot.fitting import Fit
from lmfit import Model
import pandas as pd
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14


def _plot_freq_dep_lifetime( freq, time, ax ):
    ax.plot(freq, time)
    ax.set_xlabel("Relative Frequency (MHz)")
    ax.set_ylabel("Decay time (ns)")

def _plot_freq_dep_amp( freq, amplitude, ax ):
    ax.plot(freq, amplitude)
    ax.set_xlabel("Relative Frequency (MHz)")
    ax.set_ylabel("Amplitude (mV)")

def _plot_freq_dep_decayrate( freq, rate, ax ):
    ax.plot(freq, rate)
    ax.set_xlabel("Relative Frequency (MHz)")
    ax.set_ylabel("Decay Rate ($\kappa/2\pi$) (MHz)")

file_path =r"D:\Data\03205Q4C_6\resonator_decay"
file_name = r"q4_ro_res_decay_dt5_20240418_1434"
dataset = xr.open_dataset(f"{file_path}\\{file_name}.nc")
dataset = dataset.transpose('mixer', 'freq', 'time')
print(dataset)

mean_start_idx = 0
mean_end_idx = 200

start_idx = 250
end_idx = 750
# Plot
freq = dataset.coords["freq"].values
time = dataset.coords["time"].values
fittime = dataset.coords["time"].values[start_idx:end_idx]
fittime = fittime-fittime[0]
time_resolution = time[1]-time[0]
Fs = time_resolution
print("time_resolution", time_resolution,"freq",freq.shape, "time",time.shape)
from exp.relaxation_time import plot_T1

mid_idx = int(freq.shape[-1]/2)


fig_0, ax_0 = plt.subplots()
ax_0.set_xlabel("Time (ns)")
ax_0.set_ylabel("I (mV)")
fig_0.subplots_adjust(left=0.15, right=0.9, bottom=0.15, top=0.9)


fig_4, ax_4 = plt.subplots()
ax_4.set_xlabel("Frequency (MHz)")
ax_4.set_ylabel("Amplitude (mV)")
fig_4.subplots_adjust(left=0.15, right=0.9, bottom=0.15, top=0.9)

fig_5, ax_5 = plt.subplots()

from analysis.damping_oscillation import resonator_decay_fitting, resonator_freqResponse_decay, damped_oscillation, freq_guess


plot_color = ["black","blue","red"]
for ro_name, data in dataset.data_vars.items():
    i_data = data.values[0]
    q_data = data.values[1]
    iq_data = i_data+1j*q_data

    for i,freq_i in enumerate([mid_idx,mid_idx+20,mid_idx-20]):
        # print(result.fit_report())    
        fitdata = i_data[freq_i][start_idx:end_idx]

        L = fitdata.shape[-1]
        fft_values = np.fft.fft(fitdata)
        P2 = np.abs(fft_values/L)
        P1 = P2[:L//2+1]
        P1[1:-1] = 2*P1[1:-1]
        frequencies = Fs * np.arange(0, (L/2)+1) / L
        # ax_5.plot(frequencies, P1)
        result = resonator_decay_fitting(time_resolution, fitdata, freq_guess(time_resolution, fitdata))
        # fit_func = decay_fit["fit_func"]
        print(f"plot freq = {freq[freq_i]:.1f}")
        print(result.fit_report())
        fit_time_curve = np.linspace(fittime[0], fittime[-1], 5000)
        ax_0.plot( time[start_idx-100:end_idx], i_data[freq_i][start_idx-100:end_idx]*1000, "-", markersize=3, color=plot_color[i],label=f"{freq[freq_i]:.1f} MHz")
        # ax_0.plot( fittime, fit_func(fittime), '-', label="fit")
        ax_0.plot( fittime+time[start_idx], result.best_fit*1000, '--', color=plot_color[i] , alpha=0.5)

        # test_result = result.params.valuesdict()
        # print(test_result["amp"])
        # ax_0.plot( fit_time_curve, 1000*damped_oscillation(fit_time_curve,test_result["amp"],test_result["tau"],test_result["freq"],test_result["phi"],test_result["offset"]), '-', color=plot_color[i] )

    
    staturate_iq_data = np.mean(np.abs(iq_data[:,mean_start_idx:mean_end_idx]), axis=1)

    ax_4.plot(freq, np.abs(staturate_iq_data))
    
    fig, ax = plt.subplots(figsize=(8, 6))
    # ax.set_title('pcolormesh')
    ax.set_xlabel("Time (ns)")
    ax.set_ylabel("Relative Frequency (GHz)")
    pcm = ax.pcolormesh( time/1000, freq, np.abs(iq_data)*1000, cmap='RdBu')# , vmin=z_min, vmax=z_max)
    plt.colorbar(pcm, label='$\sqrt{I^2+Q^2}$ (mV)')
    
    fig.subplots_adjust(left=0.15, right=0.9, bottom=0.15, top=0.9)



    df_result = resonator_freqResponse_decay( i_data[:,start_idx:end_idx], time_resolution)
        

    print(df_result)
    fig_1, ax_1 = plt.subplots(nrows=3, figsize=(6, 14))
    fig_1.subplots_adjust(left=0.15, right=0.9, bottom=0.1, top=0.9)
    _plot_freq_dep_lifetime(freq, df_result["tau"].values, ax_1[0])
    _plot_freq_dep_amp(freq, df_result["amp"].values*1000,ax_1[1])
    _plot_freq_dep_decayrate(freq, 1/df_result["tau"].values*1000/(2*np.pi),ax_1[2])


fig.savefig(f"{file_path}\\{file_name}_raw.png")
fig_0.savefig(f"{file_path}\\{file_name}_fit.png")
fig_4.savefig(f"{file_path}\\{file_name}_ave.png")
fig_1.savefig(f"{file_path}\\{file_name}_result.png")

plt.show()


