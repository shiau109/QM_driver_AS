import numpy as np
import matplotlib.pyplot as plt

common_path = f"D:\Data\DR2_5Q"
file_names = ["Qc3450_iSWAP_20240110_0024","Qc3500_iSWAP_20240109_2358","Qc3600_iSWAP_20240109_2322"]
label = ["3450","3500","3600"]
time = np.arange(40, 10000, 40)

fig_iq, ax_iq = plt.subplots()
for fn, l in zip(file_names,label):
    raw_data = np.load(f"{common_path}\{fn}.npz", allow_pickle=True)# ["arr_0"].item()

    # for i, (r, data) in enumerate(raw_data.items()):

    idata = raw_data["q3_ro"]
    
    ax_iq.plot( time, idata, label=l)
plt.legend()
plt.show()
