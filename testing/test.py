import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import curve_fit
from common_fitting_func import *

def T2_hist(data, T2_max, signal_name):
    try:
        new_data = [x / 1000 for x in data]  # 將數據轉換成微秒
        bin_width = 0.5  # 修改區間寬度
        start_value = -0.25  # 修改起始值
        end_value = T2_max + 0.25  # 修改結束值
        custom_bins = [start_value + i * bin_width for i in range(int((end_value - start_value) / bin_width) + 1)]
        print(f'custom_bins:{custom_bins}')
        hist_values, bin_edges = np.histogram(new_data, bins=custom_bins, density=True)
        bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
        print(f'hist_values:{hist_values}')
        print(f'bin_edges:{bin_edges}')
        print(f'bin_centers:{bin_centers}')
        params, covariance = curve_fit(gaussian, bin_centers, hist_values)
        mu, sigma = params
        
        plt.cla()
        plt.hist(new_data, bins=custom_bins, density=True, alpha=0.7, color='blue', label='Histogram')
        
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = gaussian(x, mu, sigma)
        plt.plot(x, p, 'k', linewidth=2, label=f'Fit result: $\mu$={mu:.2f}, $\sigma$={sigma:.2f}')
        
        plt.legend()
        plt.title('T2_'+signal_name+' Gaussian Distribution Fit')
        plt.show()
        
        print(f'Mean: {mu:.2f}')
        print(f'Standard Deviation: {sigma:.2f}')
    except Exception as e:
        print(f"An error occurred: {e}")
your_data = [749,1000,1251,1480,320,2100,249]
# 假设 T2_max = 3000
T2_hist(your_data, 3, "your_signal_name")