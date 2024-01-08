import numpy as np
import matplotlib.pyplot as plt
raw_data = np.load(r'D:\Data\DR2_5Q\Q1_idle_Rabi_20240105_195037.npz', allow_pickle=True)# ["arr_0"].item()
# tomo_data =
other_info = {}
for k, v in raw_data.items():
    print(k, v.shape)
    if k in ["paras","setting"]:
        other_info[k]=v.item()
from exp.rabi_J import freq_time_rabi, plot_ana_freq_time_rabi, freq_power_rabi

setting = other_info["setting"]
xy_LO = setting["xy_freq_LO"]
xy_IF_idle = setting["xy_freq_Idle"]

paras = other_info["paras"]
dfs = paras["d_xy_freq"]
time = paras["xy_time"]

for r, data in raw_data.items():
    if r not in ["paras","setting"]:
        fig, ax = plt.subplots(2)
        plot_ana_freq_time_rabi(data, dfs, time, xy_LO, xy_IF_idle, ax)
        ax[0].set_title(r)
        # ax[1].set_title(r)

plt.show()

