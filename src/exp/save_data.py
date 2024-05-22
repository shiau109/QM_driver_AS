from datetime import datetime
import sys
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

def save_npz( save_dir, file_name, output_data:dict, suffix_time:bool=False, prefix_time:bool=True ):
    save_time = ""
    save_time = str(datetime.now().strftime("%Y%m%d_%H%M"))

    if suffix_time:
        save_path = f"{save_dir}/{file_name}_{save_time}.npz"
    if prefix_time:
        save_path = f"{save_dir}/{save_time}_{file_name}.npz"
    
    np.savez(save_path, **output_data)

def save_nc( save_dir, file_name, output_data:xr.Dataset, suffix_time:bool=False, prefix_time:bool=True ):
    save_time = ""
    save_time = str(datetime.now().strftime("%Y%m%d_%H%M"))

    if suffix_time:
        save_path = f"{save_dir}/{file_name}_{save_time}.nc"
    if prefix_time:
        save_path = f"{save_dir}/{save_time}_{file_name}.nc"

    output_data.to_netcdf(save_path)


def save_fig( save_dir, file_name, suffix_time:bool=False, prefix_time:bool=True ):
    save_time = ""
    save_time = str(datetime.now().strftime("%Y%m%d_%H%M"))

    if suffix_time:
        save_path = f"{save_dir}/{file_name}_{save_time}.png"
    if prefix_time:
        save_path = f"{save_dir}/{save_time}_{file_name}.png"

    figure = plt.gcf()
    figure.set_size_inches(16, 8)
    plt.tight_layout()
    plt.savefig(f"{save_path}", dpi = 500)
