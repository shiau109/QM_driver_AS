import xarray as xr
import dataclasses
from scipy.optimize import curve_fit
import numpy as np
import xarray as xr
from matplotlib import pyplot as plt

ds = xr.load_dataset('data.nc')
data = ds.data

def power_law(m, a, b, p):
    return a * (p**m) + b

circuit_depths = data.sizes['circuit_depth']
num_averages = data.sizes['average']
num_repeats = data.sizes['repeat']

# print((data.data == 0).data.shape)
print(data.mean("average"))
counts_0 = (data == 0).sum('average') / num_averages
fidelity = (data == 0).sum(("repeat", "average")) / (num_repeats * num_averages)
std_repeat = counts_0.std('repeat')
x = np.linspace(0, circuit_depths-1, circuit_depths)
data = fidelity.values
pars, cov = curve_fit(
    f=power_law,
    xdata=x,
    ydata=data,
    p0=[0.5, 0.5, 0.9],
    bounds=(-np.inf, np.inf),
    maxfev=2000,
)
d = 2**2
ref_r = (1 - pars[2])*(d-1)/d
ref_f = 1 - ref_r
print("#########################")
print("### Fitted Parameters ###")
print("#########################")
print(f"A = {pars[0]:.3}, B = {pars[1]:.3}, p = {pars[2]:.3}")
print(f'Reference Error Rate: {ref_r:.4f}')
print(f'Reference Fidelity: {ref_f:.4f}')
plt.figure()
plt.plot(x, power_law(x, *pars), linestyle="--", linewidth=2, label='fitting')
plt.errorbar(x, fidelity, yerr=std_repeat, fmt='o', label='exp with error bar')
fidelity.rename("fidelity").plot.line(label='exp')
plt.title(f'Two-Qubit Gate Reference Fidelity: {ref_f:.4f}')
plt.legend()
plt.show()