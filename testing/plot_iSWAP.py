import numpy as np
import matplotlib.pyplot as plt
raw_data = np.load(r'D:\Data\5Q4C_0411_3_DR4\iSWAP_q3_xy_q3_z_q8_z_0.06_20240502_1538.nc', allow_pickle=True)# ["arr_0"].item()
# tomo_data =




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
