import xarray as xr
import dataclasses
from scipy.optimize import curve_fit
import numpy as np
import xarray as xr
from matplotlib import pyplot as plt

# ds = xr.load_dataset('test_circuit.nc')
# data = ds.state

# num_averages = data.sizes['average']

# I1 = ds.I1.sum(("average")) / (num_averages)
# I2 = ds.I2.sum(("average")) / (num_averages)
# Q1 = ds.Q1.sum(("average")) / (num_averages)
# Q2 = ds.Q2.sum(("average")) / (num_averages)

I1 = [-7.849675416946412e-05,0.0001990748792886734,-4.522713087499142e-05,0.00022473409399390221,
      0.00012756073474884033,0.00017133062705397605,0.0001204071193933487,0.00017528328485786915,
      0.00016830211877822876]
Q1 = [-0.0002508001998066902,-0.0002621316835284233,-0.00026289434544742106,-0.00027436087280511857,
      -0.00031478453241288665,-0.0003274716716259718,-0.00032043017446994784,-0.0003344358317553997,
      -0.0003408602401614189]
I2 = [-7.629405334591865e-05,0.00011577209085226059,-6.288479268550873e-05,0.0001373820323497057,
      6.837179511785507e-05,6.425543315708637e-05,4.6676179394125936e-05,9.111156314611435e-05,
      6.5810052677989e-05]
Q2 = [-8.542624115943909e-05,-0.00010943507216870784,-9.078918024897575e-05,-0.00012675393931567668,
      -0.00011525060608983039,-9.420996345579624e-05,-9.139526076614857e-05,-0.00012268871068954468,
      -9.919631108641625e-05]


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