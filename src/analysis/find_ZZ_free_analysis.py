from qualang_tools.plot.fitting import Fit

import numpy as np

import matplotlib.pyplot as plt

from scipy.optimize import fsolve, minimize

def compute_fft(data):
    """
    計算給定時間點和數據點的快速傅里葉變換（FFT）。

    參數：
    time_points : array_like
        時間點。
    data_points : array_like
        對應的數據點。

    返回值：
    fft_values : ndarray
        信號的頻域表示。
    frequencies : ndarray
        對應的頻率。
    """

    evo_time = data.coords["time"].values
    data = data - np.mean(data)
    # 計算時間間隔和取樣頻率
    time_step = evo_time[1] - evo_time[0]
    
    # 對信號進行FFT
    fft_values = np.fft.fft(data)
    n = len(data)
    
    # 計算頻率
    frequencies = np.fft.fftfreq(n, d=time_step)
    
    return fft_values, frequencies

def try_fit_ramsey(data):
    """
    data in shape (N)
    N is evo_time_point
    """
    evo_time = data.coords["time"].values
    try:
        fit = Fit()
        ana_dict = fit.ramsey(evo_time, data, plot=False)
        detune = ana_dict['f'][0]*1e3
        print(f"T2 = {ana_dict['T2'][0]*1e-3} [micro second]")
    except:
        print("an error occured when fit ramsey")
        detune = 0.
    return detune

def calculate_real_detune(data):
    """
    data in shape (2,N)
    2 is postive and negative
    N is evo_time_point
    """
    freq_pos = try_fit_ramsey(data[0])
    freq_neg = try_fit_ramsey(data[1])
    real_detune = (freq_pos-freq_neg)/2.
    return real_detune

def real_detune_X_flux(data):
    """
    data in shape (2,2,M,N)
    first 2 is postive and negative
    second 2 is postive and negative
    M is flux point
    N is evo_time_point
    """
    flux_range = data.coords["flux"].values
    q = list(data.data_vars.keys())[0]
    frequency_X=np.zeros(len(flux_range))
    frequency_I=np.zeros(len(flux_range))
    for flux_idx, flux in enumerate(flux_range):
        frequency_I[flux_idx] = calculate_real_detune(data[q][0, 1, :, flux_idx, :])
        frequency_X[flux_idx] = calculate_real_detune(data[q][0, 0, :, flux_idx, :])
    return flux_range, frequency_X, frequency_I

def compute_fc(z, fc_max, fq, z_fq, Ec):    
    return (fc_max+Ec)*np.sqrt(np.abs(np.cos(z/z_fq*np.arccos(((fq+Ec) / (fc_max+Ec))**2)))) - Ec