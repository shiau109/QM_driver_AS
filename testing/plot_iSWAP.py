import numpy as np
import matplotlib.pyplot as plt
raw_data = np.load(r'D:\Data\DR2_5Q\Qc3450\iSWAP_20240109_161720.npz', allow_pickle=True)# ["arr_0"].item()
# tomo_data =
other_info = {}
for k, v in raw_data.items():
    print(k, v.shape)
    if k in ["paras","setting"]:
        other_info[k]=v.item()
from exp.iSWAP_J import *
setting = other_info["setting"]

z_abs = setting["z_offset"]

paras = other_info["paras"]
amps = paras["d_z_amp"]
time = paras["z_time"]
iq_rotate = np.array([ 0.1,0.17,0.4,0.25 ])*np.pi
target_amps = -0.0437
target_idx = np.searchsorted(amps, target_amps)
# if target_idx>len(amps):
#     target_idx = len(amps)-1
print(target_idx)
# print(amps[target_idx])

osc_data = {}
for i, (r, data) in enumerate(raw_data.items()):
    if r not in ["paras","setting"]:
        fig, ax = plt.subplots(2)
        plot_ana_iSWAP_chavron( data, amps, time, ax, iq_rotate[i] )
        ax[0].set_title(r)
        ax[0].axvline(x=amps[target_idx], color='r', linestyle='--')

        zdata = (data[0]+1j*data[1])*np.exp(1j*iq_rotate[i])
        fig_2D, ax_2D = plt.subplots(2)
        ax_2D[0].scatter( time, np.real(zdata).transpose()[target_idx])
        ax_2D[1].scatter( time, np.imag(zdata).transpose()[target_idx])

        osc_data[r] = np.real(zdata).transpose()[target_idx]

        fig_iq, ax_iq = plt.subplots()
        ax_iq.scatter( 0, 0 )
        ax_iq.scatter( np.real(zdata).transpose()[target_idx], np.imag(zdata).transpose()[target_idx])


plt.show()
# from exp.save_data import *
# save_data = True
# if save_data:
#     from exp.save_data import save_npz
#     import sys
#     save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
#     save_npz(r"D:\Data\DR2_5Q", "Qc3450_iSWAP", osc_data) 
# def find_nearest_index(sorted_array, target):
#     index = np.searchsorted(sorted_array, target, side="left")
    
#     # Check if the target is closer to the left or right element
#     if index == 0:
#         return index
#     elif index == len(sorted_array):
#         return index - 1
#     else:
#         left_difference = abs(sorted_array[index - 1] - target)
#         right_difference = abs(sorted_array[index] - target)
#         return index - 1 if left_difference < right_difference else index
