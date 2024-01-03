import numpy as np


file_path = r"C:\Users\admin\SynologyDrive\09 Data\Fridge Data\Qubit\20231027_DR2_5XQ\Jacky"
file_name = "relaxation_time_raw_20231128-115442"
data = np.load(file_path+"\\"+file_name+".npz", allow_pickle=True)

for k, v in data.items():
    print(k, v.shape)