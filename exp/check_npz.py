import numpy as np


file_path = r"D:\Data\5Q_DR3"
file_name = "r23_x2_20231212-214244"
data = np.load(file_path+"\\"+file_name+".npz", allow_pickle=True)

for k, v in data.items():
    print(k, v.shape)