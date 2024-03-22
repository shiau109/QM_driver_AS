import xarray as xr
import numpy as np
import xarray as xr
from matplotlib import pyplot as plt

ds = xr.load_dataset('find_CZ_Chevron.nc')
I = ds.I
Q = ds.Q
flux_Qi = 2
qubit_num = ds.coords['qubit index'].values
t_delay = ds.coords['flux duration'].values
amps = ds.coords['flux amp']
y_ticks_labels = [f'{value:.5f}' for value in amps]

plt.suptitle(f"CZ chevron sweeping the flux on qubit {flux_Qi}")
for i in range(len(qubit_num)):
    plt.subplot(2,2,i+1)
    plt.cla()
    plt.pcolor(amps, t_delay, I[i].transpose())
    plt.title(f"q{i} - I [V]")
    plt.ylabel("z pulse duration (ns)")
    plt.subplot(2,2,i+3)
    plt.cla()
    plt.pcolor(amps, t_delay, Q[i].transpose())
    plt.title(f"q{i} - Q [V]")
    plt.ylabel("z pulse duration (ns)")
    plt.xlabel("2 * z pulse amp. (V)")       
    plt.tight_layout()
plt.show()