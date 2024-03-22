import xarray as xr
import dataclasses
from scipy.optimize import curve_fit
import numpy as np
import xarray as xr
from matplotlib import pyplot as plt

ds = xr.load_dataset('test_circuit.nc')
data = ds.state

num_averages = data.sizes['average']

I1 = ds.I1.sum(("average")) / (num_averages)
I2 = ds.I2.sum(("average")) / (num_averages)
Q1 = ds.Q1.sum(("average")) / (num_averages)
Q2 = ds.Q2.sum(("average")) / (num_averages)

plt.scatter(I1, Q1, color='blue', label='qubit2')
plt.scatter(I2, Q2, color='red', label='qubit3')
depth_list = [0,1,2,3,500,501,502,1000,1500]
# depth_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
for i in range(len(I1)):
    plt.text(I1[i], Q1[i], f'{depth_list[i]}', color='black', fontsize=12)
    plt.text(I2[i], Q2[i], f'{depth_list[i]}', color='black', fontsize=12)
plt.title('X gate Number of qubit 2 & 3')
plt.xlabel('I')
plt.ylabel('Q')
plt.axvline(x=2.203e-05, color='blue', label='qubit2', linestyle="--")
plt.axvline(x=4.691e-06, color='red', label='qubit3', linestyle="--")
plt.legend()
plt.show()