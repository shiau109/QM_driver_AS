import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

filename = r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240905_DR3_5Q4C_0430#7\raw_data\20240930_175732_CZ_diff\q3q3_cz_phasediff_shot.nc"
dataset = xr.open_dataset(filename,engine='netcdf4', format='NETCDF4')


threhold_q3 = 4.101e-05#2.615e-5#6.097e-5
threhold_q4 = 1.163e-04#8.246e-7
ro_element_q3 = "q3_ro" # target qubit readout
ro_element_q4 = "q4_ro" # control qubit readout

shot_num = 500
data_q3 = dataset[ro_element_q3].values[0]
data_q4 = dataset[ro_element_q3].values[0]

print(data_q3.shape)
print(data_q4.shape)


state_00 = 0
state_01 = 0
state_10 = 0
state_11 = 0

for i in range(shot_num):
    if ((data_q3[i] >= threhold_q3) & (data_q4[i] >= threhold_q4)):
        state_11+=1
    elif((data_q3[i] >= threhold_q3) & (data_q4[i] < threhold_q4)):
        state_10+=1
    elif((data_q3[i] < threhold_q3) & (data_q4[i] >= threhold_q4)):
        state_01+=1
    else:
        state_00+=1

print(f"00:{state_00}\n")
print(f"01:{state_01}\n")
print(f"10:{state_10}\n")
print(f"11:{state_11}\n")

# 把四個 state 和對應的數量放進去
states = ['00', '01', '10', '11']
counts = [state_00, state_01, state_10, state_11]

# 繪製長條圖
plt.bar(states, counts)

# 添加標題和標籤
plt.title('State Counts')
plt.xlabel('States')
plt.ylabel('Counts')

# 顯示圖表
plt.show()
