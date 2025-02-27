from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.loops import from_array
from qm.qua import *
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import time
from datetime import datetime
from xarray import DataArray
import numpy as np
import copy


class QMMeasurement( ABC ):

    def __init__( self, config:dict, qmm:QuantumMachinesManager):
        self.__describe()
        self.config = config
        self.qmm = qmm
        self.fetch_mode = "live"
        self.common_axis = None

        self.__preprocess = "average"
        self.__qua_dim = None
        self.__output_dim = None
        self.__output_coords = None
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
    def qua_dim( self )->list[str]:
        """
        Please write in the name of each for loop ( from outer loop to inner loop ) 
        """
        return self.__qua_dim
    
    @qua_dim.setter
    def qua_dim( self, val:list[str] ):
        
        self.__qua_dim = copy.deepcopy(val) 
        output_dim = ["q_idx"]
        self.__output_coords = {
            "q_idx" : self.ro_elements
        }
        
        new_qua_dim = val
        new_qua_dim.remove("index")

        match self.preprocess:
            case "average":
                output_dim += ["mixer"]
                self.__output_coords["mixer"] = np.array(["I","Q"])
            
            case "shot":
                output_dim += ["mixer","index"]
                self.__output_coords["mixer"] = np.array(["I","Q"])
                self.__output_coords["index"] = np.arange(self.shot_num)
                
            case "state":
                output_dim += ["index"]
                self.__output_coords["index"] = np.arange(self.shot_num)
                
            case _:
                raise ValueError("self.preprocess has a wrong value.") 
            
        self.__output_dim = output_dim + new_qua_dim


    @property
    def output_dim( self ):
        """
        For all mode, there must be a coord call "q_idx"\n
        In 'average' mode, there must be a coord call "mixer"\n
        In 'shot' mode, there must be coords call "mixer", "index".\n
        """
        
        return self.__output_dim
    
    @property
    def output_coords( self ):
        """
        For all mode, there must be a coord call "q_idx"\n
        In 'average' mode, there must be a coord call "mixer"\n
        In 'shot' mode, there must be coords call "mixer", "index".\n
        """
        
        return self.__output_coords        

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

        match self.preprocess:
            case "average":
                for r_name in self.ro_elements:
                    ro_ch_name.append(f"{r_name}_I")
                    ro_ch_name.append(f"{r_name}_Q")
            case "shot":
                for r_name in self.ro_elements:
                    ro_ch_name.append(f"{r_name}_I")
                    ro_ch_name.append(f"{r_name}_Q")
            case "state":
                for r_name in self.ro_elements:
                    ro_ch_name.append(f"{r_name}_state")
        return ro_ch_name+["outermost_i"]

    def _data_formation( self )->DataArray:

        output_data = []
        dims = ["q_idx"]
        match self.preprocess:
            case "average":
                for r_idx, r_name in enumerate(self.ro_elements):
                    data_array = np.array([ self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]])
                    output_data.append( np.squeeze(data_array))
                raw_dataArray = DataArray(output_data, dims=dims+["mixer"]+[x for x in self.qua_dim if x != "index"], coords=self.output_coords)
            case "shot":
                for r_idx, r_name in enumerate(self.ro_elements):
                    data_array = np.array([ self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]])
                    output_data.append( np.squeeze(data_array))
                raw_dataArray = DataArray(output_data, dims=dims+["mixer"]+self.qua_dim, coords=self.output_coords)

            case "state":
                for r_idx, r_name in enumerate(self.ro_elements):
                    data_array = np.array([ self.fetch_data[r_idx]])
                    output_data.append( np.squeeze(data_array))
                raw_dataArray = DataArray(output_data, dims=dims+self.qua_dim, coords=self.output_coords)


        return raw_dataArray
    
    def run( self, shot_num:int=None, save_path:str=None ):
        if self.qua_dim is None:
            raise ValueError("self.qua_dim is not set in this experiment, please set name of loop dimensions")    
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
        # print(self.output_data)
        # print(self.output_dim)
        self.output_data.attrs["start_time"] = str(measurement_start_time.strftime("%Y%m%d_%H%M%S"))
        self.output_data.attrs["end_time"] = str(measurement_end_time.strftime("%Y%m%d_%H%M%S"))
        # self.output_data = self.output_data.transpose(*self.output_dim)

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