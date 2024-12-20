
import xarray as xr
import numpy as np
import os
from exp.QMMeasurement import QMMeasurement

class RepetitionMeasurement():
    def __init__( self ):
        """ Once self.folder_path was given, save every reprtition dataset there. If repetition successfully done, they will also be removed. Otherwise, only save repetition-condensed datasets instead."""
        self.exp_list = []
        self.exp_name = []
        self.folder_path:str = ""

    def run( self, repetition:int ,folder_path:str=None):
        self.repetition = repetition
        if folder_path is not None:
            self.folder_path = folder_path
        
        if self.folder_path != "":
            dyna_save = True 
        else:
            dyna_save = False

        repetition_dataset = {}
        condensed_dataset = {}
        for name in self.exp_name:
            repetition_dataset[name] = []

        for i in range(self.repetition):
            print(f"{i}/{self.repetition}")
            for name, exp in zip(self.exp_name, self.exp_list):
                exp:QMMeasurement
                dataset = exp.run(exp.shot_num)
                if dyna_save:
                    save_path = os.path.join(self.folder_path,f"{name}_({i}).nc")
                    dataset.to_netcdf(save_path)
                repetition_dataset[name].append(dataset)
        
        for name in self.exp_name:
            condensed_dataset[name] = xr.concat(repetition_dataset[name], dim='repetition')
            condensed_dataset[name].coords["repetition"] = np.arange(repetition)

            # we have condensed-dataset, remove every single file
            if dyna_save:
                # save condensed-dataset in case
                condensed_dataset[name].to_netcdf(os.path.join(self.folder_path,f"{name}Rep.nc"))
                files = [os.path.join(self.folder_path,file_name) for file_name in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path,file_name)) and os.path.split(file_name)[-1].split(".")[-1]=='nc' and os.path.split(file_name)[-1].split("_")[0]==name]
                for file in files:
                    os.remove(file)

        return condensed_dataset