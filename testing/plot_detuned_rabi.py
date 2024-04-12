import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from exp.rabi import plot_ana_freq_time_rabi



def plot_sub( x, y, data, ro_name ):

    idata = data[0]
    qdata = data[1]
    zdata = idata +1j*qdata
    s21 = zdata
    print(x.shape, y.shape, zdata.shape)

    fig, ax = plt.subplots()
    # Add color bar to the axes
    ax.set_title(ro_name)
    pcm = ax.pcolormesh( x, y, np.transpose(idata), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    fig.colorbar(pcm)



dataset = xr.open_dataset(r"D:\Data\03205Q4C_6\q0_xy_idle_Rabi_20240404_1911.nc")

# y = dataset.coords["amplitude"].values
y = dataset.coords["time"].values

freqs = dataset.coords["frequency"].values
# Plot 
for ro_name, data in dataset.data_vars.items():
    xy_LO = dataset.attrs["ref_xy_LO"]/1e6
    xy_IF_idle = dataset.attrs["ref_xy_IF"]/1e6
    fig, ax = plt.subplots(2)
    plot_ana_freq_time_rabi( data, freqs, y, xy_LO, xy_IF_idle, ax )
    ax[0].set_title(ro_name)
    ax[1].set_title(ro_name)
plt.show()

