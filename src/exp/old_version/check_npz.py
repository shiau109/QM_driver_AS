import numpy as np


file_path = r"D:\Data\DR2_5Q"
file_name = "iSWAP_Qc3500_20240105-102207"
data = np.load(file_path+"\\"+file_name+".npz", allow_pickle=True)

for k, v in data.items():
    print(k, v.shape)