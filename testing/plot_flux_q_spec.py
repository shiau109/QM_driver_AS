import numpy as np
import matplotlib.pyplot as plt
raw_data = np.load(r'D:\Data\DR2_5Q\Qc3450\Q2Z3_flux_dep_Qspectrum_20240108_182432.npz', allow_pickle=True)# ["arr_0"].item()
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

iq_rotate = np.array([ 0.1,0.17,0.4,0.25 ])*np.pi

for i, (r, data) in enumerate(raw_data.items()):
    if r not in ["paras","setting"]:
        fig, ax = plt.subplots(2)
        plot_ana_flux_dep_qubit(data, flux, dfs, xy_LO, xy_IF_idle, z_abs, ax, iq_rotate=iq_rotate[i])
        ax[0].set_title(r)
        # ax[1].set_title(r)

        # zdata = (data[0]+1j*data[1])*np.exp(1j*iq_rotate[i])
        # fig_2D, ax_2D = plt.subplots(2)
        # ax_2D[0].scatter( time, np.real(zdata).transpose()[target_idx])
        # ax_2D[1].scatter( time, np.imag(zdata).transpose()[target_idx])


plt.show()

