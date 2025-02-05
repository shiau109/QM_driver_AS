from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.loops import from_array
from qm.qua import *
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import time
from datetime import datetime
from xarray import Dataset
import numpy as np


class QMMeasurement( ABC ):

    def __init__( self, config:dict, qmm:QuantumMachinesManager):
        self.__describe()
        self.config = config
        self.qmm = qmm
        self.fetch_mode = "live"
        self.common_axis = None

        self.__preprocess = "ave"
        self.__output_coords = ["q_idx","mixer"]

        self.__ro_elements = []


    @property
    def preprocess( self ):
        """
        only 'average', 'shot' can be set.\n
        if discriminator is not None, self.__preprocess will be set to 'state' mode
        """
        return self.__preprocess
    @preprocess.setter
    def preprocess( self, val:str ):
        if val in ["average","shot"]:
            self.__preprocess = val
        else:
            self.__preprocess = "ave"

    @property
    def output_coords( self ):
        """
        For all mode, there must be a coord call "q_idx"\n
        In 'average' mode, there must be a coord call "mixer"\n
        In 'shot' mode, there must be coords call "mixer", "index".\n
        """
        return self.__output_coords
    @output_coords.setter
    def output_coords( self, val:list[str] ):
        coords_name = ["q_idx"]
         
        match self.preprocess:
            case "average":
                coords_name.extend["mixer"]
            case "shot":
                coords_name.extend["mixer","index"]
            case "state":
                coords_name.extend["index"]
            case _:
                raise ValueError("self.preprocess has a wrong value.") 
        for coord_name in coords_name: 
            if coord_name not in val:
                raise ValueError(f"Must be a coord called {coord_name}.") 

    @property
    def ro_elements( self ):
        """
        Should be list of str
        Please make sure the names are register in config.
        """
        return self.__ro_elements
    @ro_elements.setter
    def ro_elements( self, val:list[str] ):
        if not isinstance(val, list): new_val = [val]
        else: new_val = val

        if all(isinstance(item, str) for item in val):
            self.__ro_elements = new_val
        else:
            raise TypeError("ro_elements should be a list of str")
        

    @abstractmethod
    def _get_qua_program( self ):
        pass

    def _get_fetch_data_list( self ):
        ro_ch_name = []
        for r_name in self.ro_elements:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")


    def _data_formation( self )->Dataset:
        coords = { 
            "mixer":np.array(["I","Q"]), 
            }
        match self.preprocess:
            case "shot":
                dims_order = ["mixer","shot","prepare_state"]
                coords["shot"] = np.arange(self.shot_num)
            case _:
                dims_order = ["mixer","prepare_state"]

        output_data = {}
        for r_idx, r_name in enumerate(self.ro_elements):
            data_array = np.array([ self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]])
            output_data[r_name] = ( dims_order, np.squeeze(data_array))

        dataset = xr.Dataset(output_data, coords=coords)

    def run( self, shot_num:int=None, save_path:str=None ):

        if shot_num is not None:
            print(f"New setting {shot_num} shots")
            self.shot_num = shot_num
        self._qm = self.qmm.open_qm( self.config )
        qua_program = self._get_qua_program()

        measurement_start_time = datetime.now()

        job = self._qm.execute(qua_program)

        match self.fetch_mode:
            case 'live':
                self._results = fetching_tool(job, data_list=self._get_fetch_data_list(), mode="live")
                while self._results.is_processing():
                    # Fetch results
                    fetch_data = self._results.fetch_all()
                    # Progress bar
                    iteration = fetch_data[-1]
                    progress_counter(iteration, self.shot_num, start_time=self._results.start_time)
                    time.sleep(1)

            case _:
                self._results = fetching_tool(job, data_list=self._get_fetch_data_list())
                
        
        measurement_end_time = datetime.now()
        self.fetch_data = self._results.fetch_all()
        self._qm.close()

        self.output_data = self._data_formation()
        self.output_data.attrs["start_time"] = str(measurement_start_time.strftime("%Y%m%d_%H%M%S"))
        self.output_data.attrs["end_time"] = str(measurement_end_time.strftime("%Y%m%d_%H%M%S"))

        if save_path is not None:
            self.output_data.to_netcdf(save_path)
            
        return self.output_data
    

    def pulse_schedule_simulation( self, controllers:list, max_time:int ):
        
        self.shot_num = 1
        simulation_config = SimulationConfig(duration=max_time)  # In clock cycles = 4ns
        qua_program = self._get_qua_program()
        job = self.qmm.simulate(self.config, qua_program, simulation_config)
        for con_name in controllers:      
            getattr(job.get_simulated_samples(), con_name).plot()
        plt.show()

    def __describe(self):
        return f"Initializing {self.__class__.__name__}"
    
    def close(self):
        
        self._qm.close()
        print("QM connection is closed.")

    def __del__(self):
        print("QM object has been deleted")
        """
        try:
            self.close()

        except AttributeError:
            # In case __inst was not initialized correctly
            print("self.close() failed.")
            pass
        except KeyError:
            print("self.close() failed.")
            pass
        """