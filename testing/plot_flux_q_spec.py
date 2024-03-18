

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np


def plot_sub( x, y, data ):

    idata = data[0]
    qdata = data[1]
    zdata = idata +1j*qdata
    s21 = zdata
    print(x.shape, y.shape, zdata.shape)

    fig, ax = plt.subplots()
    # Add color bar to the axes

    pcm = ax.pcolormesh( x, y, np.transpose(np.abs(s21)), cmap='RdBu', vmin=0, vmax=0.0002)# , vmin=z_min, vmax=z_max)
    fig.colorbar(pcm)



dataset = xr.open_dataset(r"D:\Data\5Q4C\20240314\Spectrum_q1_xy_q5_z_20240314_1716.nc")

# Plot
dfs = dataset.coords["frequency"].values
flux = dataset.coords["flux"].values
for ro_name, data in dataset.data_vars.items():
    plot_sub( flux, dfs, data.values)
plt.show()


