import numpy as np
import matplotlib.pyplot as plt
raw_data = np.load(r'D:\Data\DR2_5Q\Qc3500\Q1_idle_Rabi_20240108_214206.npz', allow_pickle=True)# ["arr_0"].item()
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

iq_rotate = np.array([ 0.1,0.17,0.4,0.25 ])*np.pi
target_dfs = 3.54
print( (dfs+xy_IF_idle+xy_LO)/1e9 )
target_idx = np.searchsorted( (dfs+xy_IF_idle+xy_LO)/1e9, target_dfs, side="left")
print(target_idx)

for i, (r, data) in enumerate(raw_data.items()):
    if r not in ["paras","setting"]:
        fig, ax = plt.subplots(2)
        plot_ana_freq_time_rabi(data, dfs, time, xy_LO, xy_IF_idle, ax, iq_rotate[i])
        ax[0].set_title(r)
        # ax[1].set_title(r)

        zdata = (data[0]+1j*data[1])*np.exp(1j*iq_rotate[i])
        # fig_2D, ax_2D = plt.subplots(2)
        # ax_2D[0].scatter( time, np.real(zdata)[target_idx])
        # ax_2D[1].scatter( time, np.imag(zdata)[target_idx])

        # fig_iq, ax_iq = plt.subplots()
        # ax_iq.scatter( 0, 0 )
        # ax_iq.scatter( np.real(zdata)[target_idx], np.imag(zdata)[target_idx])

plt.show()

