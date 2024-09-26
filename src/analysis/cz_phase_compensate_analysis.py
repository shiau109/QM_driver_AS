import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

filename = 'C:\\QM\\Data\\20240620_DR4_5Q4C_0430#7_new\\20240911_1400_q3q4_cz_phasediff_shot.nc'
dataset = xr.open_dataset(filename,engine='netcdf4', format='NETCDF4')


threhold = -1.483e-6#8.246e-7
ro_element = "q4_ro" # target qubit readout
shot_num = 500
data = dataset[ro_element].values[0]
print(data.shape)

population_y = 0
population_x = 0
for i in range(shot_num):
    if data[i,0] >= threhold:
        population_y += 1
    if data[i,1] >= threhold:
        population_x += 1
population_y = population_y/shot_num
population_x = population_x/shot_num

y = -np.cos(2*np.arcsin(population_y**0.5))
x = -np.cos(2*np.arcsin(population_x**0.5))
phi = np.arctan2(x,y)

print(phi)