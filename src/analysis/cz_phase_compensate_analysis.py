import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

filename = r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240905_DR3_5Q4C_0430#7\raw_data\20240930_175732_CZ_diff\q3q3_cz_phasediff_shot.nc"
dataset = xr.open_dataset(filename,engine='netcdf4', format='NETCDF4')


threhold = 4.101e-5#4.101e-5#1.163e-4#8.246e-7
ro_element = "q3_ro" # target qubit readout
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