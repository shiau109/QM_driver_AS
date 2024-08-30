
import xarray as xr
import numpy as np
class RepetitionMeasurement():
    def __init__( self ):

        self.exp_list = []
        self.exp_name = []

    def run( self, repetition:int ):
        self.repetition = repetition

        repetition_dataset = {}
        condensed_dataset = {}
        for name in self.exp_name:
            repetition_dataset[name] = []

        for i in range(self.repetition):
            print(f"{i}/{self.repetition}")
            for name, exp in zip(self.exp_name, self.exp_list):
                dataset = exp.run(exp.shot_num)
                repetition_dataset[name].append(dataset)
        
        for name in self.exp_name:
            condensed_dataset[name] = xr.concat(repetition_dataset[name], dim='repetition')
            condensed_dataset[name].coords["repetition"] = np.arange(repetition)

        return condensed_dataset[name]