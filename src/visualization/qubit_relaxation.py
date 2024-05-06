
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



def plot_multiT1( data, rep, time, t1_array ):
    """
    data shape ( 2, N, M )
    2 is I,Q
    N is rep
    M is time
    """
    idata = data[0]
    qdata = data[1]
    zdata = idata +1j*qdata

    fig, ax = plt.subplots(2)
    ax[0].set_title('I signal')
    ax[0].pcolormesh( time, rep, idata, cmap='RdBu')# , vmin=z_min, vmax=z_max)
    ax[0].plot(t1_array,rep)
    ax[1].set_title('Q signal')
    ax[1].pcolormesh( time, rep, qdata, cmap='RdBu')# , vmin=z_min, vmax=z_max)
    return fig

def T1_hist( data, fig=None):

    if fig == None:
        fig, ax = plt.subplots()
    new_data = data/1000 # change ns to us
    mean_t1 = np.mean(new_data)
    bin_width = mean_t1 *0.05
    start_value = np.mean(new_data)*0.5
    end_value = np.mean(new_data)*1.5
    custom_bins = [start_value + i * bin_width for i in range(int((end_value - start_value) / bin_width) + 1)]
    ax.hist(new_data, custom_bins, density=False, alpha=0.7, label='Histogram')# color='blue', 
    xmin, xmax = ax.get_xlim()
    x = np.linspace(xmin, xmax, 100)
    # p = gaussian(x, mu, sigma)
    # ax.plot(x, p, 'k', linewidth=2, label=f'Fit result: $\mu$={mu:.2f}, $\sigma$={sigma:.2f}')
    # ax.legend()
    fig.suptitle('T1 Distribution')


file_path = r"/Users/ratiswu/Downloads"
file_name = r"['q3_xy']_T1_20240419_2044"
dataset = xr.open_dataset(f"{file_path}/{file_name}.nc")
print(dataset)



from analysis.exp_decay import qubit_relaxation_statistic
time = dataset.coords["time"].values

rep = dataset.coords["repetition"].values

for ro_name, data in dataset.data_vars.items():
    print(ro_name, data.shape)
    result = qubit_relaxation_statistic( time, data.values[0] )
    print(result)
    plot_multiT1( data, rep, time, result["tau"].values)
    T1_hist( result["tau"].values )

plt.show()