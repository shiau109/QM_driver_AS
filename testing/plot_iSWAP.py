import numpy as np
import matplotlib.pyplot as plt
raw_data = np.load(r'D:\Data\DR2_5Q\iSWAP_20240108_193231.npz', allow_pickle=True)# ["arr_0"].item()
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

for r, data in raw_data.items():
    if r not in ["paras","setting"]:
        fig, ax = plt.subplots(2)
        plot_ana_iSWAP_chavron( data, amps, time, ax )
        ax[0].set_title(r)
        # ax[1].set_title(r)

plt.show()

