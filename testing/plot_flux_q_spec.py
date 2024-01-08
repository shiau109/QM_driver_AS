import numpy as np
import matplotlib.pyplot as plt
raw_data = np.load(r'D:\Data\DR2_5Q\Qc3450\Q1Z3_flux_dep_Qspectrum_20240108_182143.npz', allow_pickle=True)# ["arr_0"].item()
# raw_data = np.load(r'D:\Data\DR2_5Q\Q1Z3_flux_dep_Qspectrum_20240105_195810.npz', allow_pickle=True)# ["arr_0"].item()
other_info = {}
for k, v in raw_data.items():
    print(k, v.shape)
    if k in ["paras","setting"]:
        other_info[k]=v.item()
from exp.flux_dep_qubit_spec_J import *
setting = other_info["setting"]
xy_LO = setting["xy_freq_LO"]
xy_IF_idle = setting["xy_freq_Idle"]
z_abs = setting["z_offset"]

paras = other_info["paras"]
flux = paras["d_z_amp"]
dfs = paras["d_xy_freq"]

for r, data in raw_data.items():
    if r not in ["paras","setting"]:
        fig, ax = plt.subplots(2)
        plot_ana_flux_dep_qubit(data, flux, dfs, xy_LO, xy_IF_idle, z_abs, ax)
        ax[0].set_title(r)
        # ax[1].set_title(r)

plt.show()

