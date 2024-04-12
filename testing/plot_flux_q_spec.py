

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np


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



dataset = xr.open_dataset(r"D:\Data\03205Q4C_6\Spectrum_q1_xy_q5_z_20240402_1649.nc")

# Plot
dfs = dataset.coords["frequency"].values
flux = dataset.coords["flux"].values
z_offset = dataset.attrs["z_offset"]
xy_LO = dataset.attrs["xy_LO"]/1e6
xy_IF_idle = dataset.attrs["xy_IF"]/1e6
for ro_name, data in dataset.data_vars.items():
    plot_sub( flux+z_offset, dfs+xy_LO+xy_IF_idle, data.values, ro_name)
plt.show()


