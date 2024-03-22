import xarray as xr
import dataclasses
from scipy.optimize import curve_fit
import numpy as np
import xarray as xr
from matplotlib import pyplot as plt

ds = xr.load_dataset('two_qubit_RB.nc')
data = ds.state


def power_law(m, a, b, p):
    return a * (p**m) + b

circuit_depths = data.sizes['circuit_depth']
num_averages = data.sizes['average']
num_repeats = data.sizes['repeat']

I1 = ds.I1.sum(("repeat", "average")) / (num_repeats * num_averages)
I2 = ds.I2.sum(("repeat", "average")) / (num_repeats * num_averages)
Q1 = ds.Q1.sum(("repeat", "average")) / (num_repeats * num_averages)
Q2 = ds.Q2.sum(("repeat", "average")) / (num_repeats * num_averages)

counts_0 = (data == 0).sum('average') / num_averages
fidelity = (data == 0).sum(("repeat", "average")) / (num_repeats * num_averages)
state_10 = (data == 1).sum(("repeat", "average")) / (num_repeats * num_averages)
state_01 = (data == 2).sum(("repeat", "average")) / (num_repeats * num_averages)
state_11 = (data == 3).sum(("repeat", "average")) / (num_repeats * num_averages)
std_repeat = counts_0.std('repeat')
x = np.linspace(0, circuit_depths-1, circuit_depths)
data = fidelity.values
data10 = state_10.values
data01 = state_01.values
data11 = state_11.values
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
# print('-------------------------')
# print('state 00: ',data[-1])
# print('state 10: ',data10[-1])
# print('state 01: ',data01[-1])
# print('state 11: ',data11[-1])
plt.figure()
plt.plot(x, power_law(x, *pars), linestyle="--", linewidth=2, label='fitting')
plt.errorbar(x, fidelity, yerr=std_repeat, fmt='o', label='exp with error bar')    
# state_10.rename("state_10").plot.line(label='state 10')
# state_01.rename("state_01").plot.line(label='state 01')
# state_11.rename("state_11").plot.line(label='state 11')
fidelity.rename("fidelity").plot.line(label='exp')
plt.title(f'Two-Qubit Gate Reference Fidelity: {ref_f:.4f}')
plt.legend()
plt.show()

# plt.title('RB circuit depth of qubit 2 & 3')
# plt.scatter(I1, Q1, color='blue', label='qubit2')
# plt.scatter(I2, Q2, color='red', label='qubit3')

# depth_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
# for i in range(len(I1)):
#     plt.text(I1[i], Q1[i], f'{depth_list[i]}', color='black', fontsize=12)
#     plt.text(I2[i], Q2[i], f'{depth_list[i]}', color='black', fontsize=12)
# plt.xlabel('I')
# plt.ylabel('Q')
# plt.axvline(x=2.203e-05, color='blue', label='qubit2', linestyle="--")
# plt.axvline(x=4.691e-06, color='red', label='qubit3', linestyle="--")
# plt.legend()
# plt.show()