import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

filename = r"C:\Users\admin\SynologyDrive\09 Data\Fridge Data\Qubit\20240920_DRKe_5Q4C\raw_data\20241004_050956_CZ_diff\q1q1_cz_phasediff_shot.nc"
dataset = xr.open_dataset(filename,engine='netcdf4', format='NETCDF4')


threhold = -1.611e-04#9.512e-05
ro_element = "q1_ro" # target qubit readout
shot_num = 500
data = dataset[ro_element].values[0]
print(data.shape)

population_y = 0
population_x = 0
for i in range(shot_num):
    if data[i,0] >= threhold:
        population_x += 1
    if data[i,1] >= threhold:
        population_y += 1
# a=87.3/(87.3+11.5)
# b=78.6/(78.6+23.7)
population_y = population_y/shot_num#*b
population_x = population_x/shot_num#*b

# y = -np.cos(2*np.arcsin(population_y**0.5))
# x = -np.cos(2*np.arcsin(population_x**0.5))
x = ((1-population_x) - population_x)
y = ((1-population_y) - population_y)
phi = np.arctan2(y,x)

print(phi)