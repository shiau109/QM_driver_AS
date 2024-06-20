import numpy as np
import matplotlib.pyplot as plt
from exp.zz_ramsey import plot_phase
import xarray as xr

dataset1 = xr.open_dataset()
dataset2 = xr.open_dataset()

time = dataset1.coords["time"].values
fig, ax = plt.subplots()
plot_phase(time, dataset1, dataset2,ax)

plt.legend()
plt.show()