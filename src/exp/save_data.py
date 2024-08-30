from datetime import datetime
import os
import numpy as np
import xarray as xr
from matplotlib.figure import Figure
import json

class DataPackager():
    def __init__( self, output_path, name, time_label_type:str|None="prefix", ):
        self.package_name = name
        self.output_path = output_path
        self.package_root = f"{output_path}/{_add_time_label(name, time_label_type)}"
        self.time_label_type = time_label_type

        self._create_folder()

    def _create_folder( self ):
        # Combine fixed part with user input
        folder_name = self.package_name
        save_dir = self.output_path
        full_path = self.package_root

        if os.path.exists( full_path ):
            print(f"Warning: The directory '{full_path}' already exists, creating separate folder")
            count = 0
            while os.path.exists(full_path):
                new_folder_name = f"{folder_name}_{count}"
                full_path = os.path.join(save_dir, new_folder_name)
                count+=1
            self.package_root = full_path
        
        # Create the directory
        os.makedirs(full_path, exist_ok=True)
        print(f"Directory '{full_path}' created successfully.")
        return full_path

    def save_npz( self, file_name, data:dict, time_label:str|None=None, time_format:str="%Y%m%d_%H%M%S" ):
        save_dir = self.package_root
        save_path = f"{save_dir}/{_add_time_label(file_name, time_label, time_format)}.npz"
        np.savez(save_path, **data)

    def save_nc( self, data:xr.Dataset, file_name, time_label:str|None=None, time_format:str="%Y%m%d_%H%M%S" ):
        save_dir = self.package_root

        save_path = f"{save_dir}/{_add_time_label(file_name, time_label, time_format)}.nc"
        data.to_netcdf(save_path, engine='netcdf4')


    def save_fig( self, fig:Figure, file_name, time_label:str|None=None, time_format:str="%Y%m%d_%H%M%S" ):
        save_dir = self.package_root
        save_path = f"{save_dir}/{_add_time_label(file_name, time_label, time_format)}.png"
        fig.savefig(f"{save_path}", dpi = 500)

    def save_figs( self, figs:list, time_label:str|None=None, time_format:str="%Y%m%d_%H%M%S" ):
        save_dir = self.package_root
        for (name, fig) in figs:
            save_path = f"{save_dir}/{_add_time_label(name, time_label, time_format)}.png"
            fig.savefig(f"{save_path}", dpi = 500)

    def save_config( self, config:dict, file_name:str="config", time_label:str|None=None, time_format:str="%Y%m%d_%H%M%S" ):
        save_dir = self.package_root
        save_path = f"{save_dir}/{_add_time_label(file_name, time_label, time_format)}.json"
        with open(save_path, 'w') as json_file:
            json.dump(config, json_file, indent=2)

def _add_time_label( file_name, time_label:str|None="prefix", time_format:str="%Y%m%d_%H%M%S" ):
    save_time = str(datetime.now().strftime(time_format))

    match time_label:
        case "suffix":
            new_file_name = f"{file_name}_{save_time}"
        case "prefix":
            new_file_name = f"{save_time}_{file_name}"
        case _:
            new_file_name = f"{file_name}"  
    return new_file_name

