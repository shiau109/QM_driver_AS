from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from qualang_tools.results import progress_counter, fetching_tool

from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import time
from datetime import datetime
from xarray import Dataset

class QMMeasurement( ABC ):

    def __init__( self, config:dict, qmm:QuantumMachinesManager):
        self.__describe()
        self.config = config
        self.qmm = qmm

    @abstractmethod
    def _get_qua_program( self ):
        pass

    @abstractmethod    
    def _get_fetch_data_list( self ):
        pass

    @abstractmethod    
    def _data_formation( self )->Dataset:
        pass

    def run( self, shot_num:int ):
        self.shot_num = shot_num
        self._qm = self.qmm.open_qm( self.config )
        qua_program = self._get_qua_program()

        measurement_start_time = datetime.now()

        job = self._qm.execute(qua_program)

        self._results = fetching_tool(job, data_list=self._get_fetch_data_list(), mode="live")
        while self._results.is_processing():
            # Fetch results
            fetch_data = self._results.fetch_all()
            # Progress bar
            iteration = fetch_data[-1]
            progress_counter(iteration, shot_num, start_time=self._results.start_time)
            time.sleep(1)
        
        measurement_end_time = datetime.now()
        self.fetch_data = self._results.fetch_all()

        self.output_data = self._data_formation()
        self.output_data.attrs["start_time"] = str(measurement_start_time.strftime("%Y%m%d_%H%M%S"))
        self.output_data.attrs["end_time"] = str(measurement_end_time.strftime("%Y%m%d_%H%M%S"))
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
        try:
            self.close()

        except AttributeError:
            # In case __inst was not initialized correctly
            print("self.close() failed.")
            pass