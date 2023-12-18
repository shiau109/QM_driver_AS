from resonator_tools.circuit import notch_port
# from .electronic_delay import *
import scipy.io
import pandas as pd
from scipy.optimize import curve_fit 
import numpy as np


def get_dispersive_shift( freq:np.ndarray, s21:np.ndarray, power:np.ndarray=None ):
    """
    shape of s21 (2,N)
    2 is prepare 0 and 1
    """

    # Fit part
    fitParas = []
    fitCurves = []
    with_power = False
    dep_num = s21.shape[0]
    print(f"Dim {freq.shape} {s21.shape}")
    if type(power) != type(None):
        with_power = True
        print("get power input")
        if type(power) != float:
            np.full(dep_num, power)
    
    if s21.ndim == 1:
        s21 = np.array([s21])

    for xi in range(dep_num):
        freq_fit = freq
        iq_fit = s21[xi]
        myResonator = notch_port()        

        # try:
            # print("auto fitting")
            #delay, params =myResonator.get_delay(freq_fit,iq_fit)
            # myResonator.autofit(electric_delay=mydelay)

        delay, amp_norm, alpha, fr, Ql, A2, frcal =\
                myResonator.do_calibration(freq_fit,iq_fit, fixed_delay=None)
        myResonator.z_data = myResonator.do_normalization(freq_fit,iq_fit,delay,amp_norm,alpha,A2,frcal)

        myResonator.fitresults = myResonator.circlefit(freq_fit,myResonator.z_data,fr,Ql)
        myResonator.z_data_sim = myResonator._S21_notch(
            freq_fit,fr=myResonator.fitresults["fr"],
            Ql=myResonator.fitresults["Ql"],
            Qc=myResonator.fitresults["absQc"],
            phi=myResonator.fitresults["phi0"],
            a=amp_norm,alpha=alpha,delay=delay)
        fit_results = myResonator.fitresults
        fit_results["A"] = amp_norm
        fit_results["alpha"] = alpha
        fit_results["delay"] = delay
        if with_power:
            fit_results["photons"] = myResonator.get_photons_in_resonator(power[xi])
        fitCurves.append(myResonator.z_data_sim)
            
        # except:
        #     print(f"{xi}th Fit failed")
        
        fitParas.append(fit_results)
    df_fitParas = pd.DataFrame(fitParas)

    
    chi = df_fitParas["chi_square"].to_numpy()
    # Refined fitting

    # min_chi_idx = chi.argmin()
    # print(df_fitParas["alpha"].to_numpy())
    # print(np.unwrap( df_fitParas["alpha"].to_numpy(), period=np.pi))
    # weights = 1/chi**2
    # fixed_delay = np.average(df_fitParas["delay"].to_numpy(), weights=weights)
    # fixed_amp = np.average(df_fitParas["A"].to_numpy(), weights=weights)
    # fixed_alpha = np.average(np.unwrap( df_fitParas["alpha"].to_numpy(), period=np.pi), weights=weights)
    
    # fixed_delay = df_fitParas["delay"].to_numpy()[min_chi_idx]  
    # fixed_amp = df_fitParas["A"].to_numpy()[min_chi_idx]  
    # fixed_alpha = df_fitParas["alpha"].to_numpy()[min_chi_idx] 
      
    
    return df_fitParas, fitCurves

def plot_freq_signal( x, data, label:str, ax ):
    print(data.shape)
    sig = get_signal_distance(data)
    ax[0].plot( x, sig, ".-")
    ax[0].set_title(f"{label} RO frequency")
    ax[0].set_xlabel("Readout frequency detuning [MHz]")
    ax[0].set_ylabel("Distance")
    ax[0].grid("on")

    sig = get_signal_amp(data)
    ax[1].plot( x, sig[0], ".-", label="0")

    ax[1].plot( x, sig[1], ".-", label="1")

    # ax[1].set_title(f"{label} RO frequency")
    ax[1].set_xlabel("Readout frequency detuning [MHz]")
    ax[1].set_ylabel("Amplitude")
    ax[1].legend()
    ax[1].grid("on")

    sig = get_signal_phase(data)
    ax[2].plot( x, sig[0], ".-", label="0")
    ax[2].plot( x, sig[1], ".-", label="1")

    # ax[2].set_title(f"{label} RO frequency")
    ax[2].set_xlabel("Readout frequency detuning [MHz]")
    ax[2].set_ylabel("Phase")
    ax[2].legend()
    ax[2].grid("on")
    # print(f"The optimal readout frequency is {dfs[np.argmax(SNR1)] + resonator_IF_q1} Hz (SNR={max(SNR1)})")
    return ax

def plot_amp_signal( x, data, label:str, ax ):
    sig = get_signal_distance(data)
    ax.plot( x, sig, ".-")
    ax.set_xlabel("Readout amplitude ")
    ax.set_ylabel("Distance")
    ax.grid("on")
    # print(f"The optimal readout frequency is {dfs[np.argmax(SNR1)] + resonator_IF_q1} Hz (SNR={max(SNR1)})")
    return ax

def plot_amp_signal_phase( x, data, label:str, ax ):
    phase_g, phase_e = get_signal_phase(data)
    ax.plot( x, phase_g, ".-", label="phase_g")
    ax.plot( x, phase_e, ".-", label="phase_e")
    ax.set_xlabel("Readout amplitude ")
    ax.set_ylabel("Phase")
    ax.grid("on")
    ax.legend()
    # print(f"The optimal readout frequency is {dfs[np.argmax(SNR1)] + resonator_IF_q1} Hz (SNR={max(SNR1)})")
    return ax

def get_signal_distance( data ):
    """
    data shape (2,2,N)
    axis 0 I,Q
    axis 1 g,e
    axis 2 N frequency
    """
    s21_g = data[0][0] +1j*data[1][0] 
    s21_e = data[0][1] +1j*data[1][1]
    signal = np.abs(s21_g -s21_e)
    return signal

def get_signal_phase( data ):
    """
    data shape (2,2,N)
    axis 0 I,Q
    axis 1 g,e
    axis 2 N frequency
    """
    s21_g = data[0][0] +1j*data[1][0] 
    s21_e = data[0][1] +1j*data[1][1]
    phase_g = np.unwrap(np.angle(s21_g))
    phase_e = np.unwrap(np.angle(s21_e))
    return (phase_g, phase_e)

def get_signal_amp( data ):
    """
    data shape (2,2,N)
    axis 0 I,Q
    axis 1 g,e
    axis 2 N frequency
    """
    s21_g = data[0][0] +1j*data[1][0] 
    s21_e = data[0][1] +1j*data[1][1]
    phase_g = np.abs(s21_g)
    phase_e = np.abs(s21_e)
    return (phase_g, phase_e)

if __name__=='__main__':
    import matplotlib.pyplot as plt

    file_path = r'D:\Data\5Q_DR3'
    file_name = "fro_r23_x23-20231213_214747.npz"

    # data = np.load(f"{file_path}\\{file_name}")# , allow_pickle=True)["arr_0"].item()
    dfs = np.arange(-2e6, 2e6, 0.05e6)
    output_data = np.load(f"{file_path}\\{file_name}")
    for r in output_data.keys():
        fig = plt.figure()
        ax = fig.subplots(3,1)
        plot_freq_signal( dfs, output_data[r], r, ax )
    plt.show() 