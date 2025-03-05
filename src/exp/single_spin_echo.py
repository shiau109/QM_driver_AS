from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
import exp.config_par as gc
import warnings
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import xarray as xr
warnings.filterwarnings("ignore")
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
import time
from exp.QMMeasurement import QMMeasurement
import numpy as np
class SpinEcho( QMMeasurement ):
    def __init__( self, config, qmm: QuantumMachinesManager):
        super().__init__( config, qmm )
        self.time_range = (32,400)

        """evo time is the duration between x90 and x180, unit in nano seconds
          I want the program to try spin echo for different time durations"""
        
        self.time_resolution = 80
        self.xy_elements = ["q0_xy"]
        self.ro_elements = ["q0_ro"]
        self.shot_num = 100
        self.initializer = None

        self.qua_dim = ["index","time"]

        self.preprocess = "average"

    def _get_qua_program( self ):
        half_time_r1_qua = (self.time_range[0]/4 /2) *u.ns
        half_time_r2_qua = (self.time_range[1]/4 /2) *u.ns

        if self.time_resolution < 4:
            print( "Warning!! time resolution < 4 ns.")
        time_resolution_qua = (self.time_resolution/4) *u.ns
        self.qua_half_evo_time = np.arange(half_time_r1_qua, half_time_r2_qua, time_resolution_qua)
        print(self.qua_half_evo_time)
        # QUA program
        with program() as spin_echo:

            iqdata_stream = multiRO_declare( self.ro_elements )
            half_evo_time = declare(int)  # x180 -> x90 has same time duration as x90 -> x180
            n = declare(int)
            outermost_st = declare_stream()
            with for_(n, 0, n < self.shot_num, n + 1):
                with for_(*from_array(half_evo_time, self.qua_half_evo_time)):
                    # initializaion
                    if self.initializer is None:
                        wait(1*u.us,self.ro_elements)
                    else:
                        try:
                            self.initializer[0](*self.initializer[1])
                        except:
                            wait(1*u.us,self.ro_elements)

                    # Operation: x90 -> x180 -> x-90, should theoretically project to |0>    
                    for q in self.xy_elements:
                        play("x90", q)
                        wait(half_evo_time)
                        play("x180", q)  
                        wait(half_evo_time)  
                        play("-x90",q)
                    align()
                    # Readout
                    multiRO_measurement( iqdata_stream,  resonators=self.ro_elements, weights="rotated_")
                
                # Save the averaging iteration to get the progress bar
                save(n, outermost_st)

            with stream_processing():
                # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
                multiRO_pre_save( iqdata_stream, self.ro_elements, (self.qua_half_evo_time.shape[-1], ), stream_preprocess=self.preprocess)
                outermost_st.save("outermost_i")

        return spin_echo
    
    def _data_formation( self ):
        evo_time = self.qua_half_evo_time*4 *2#4 for scaling back to normal dimension
        self.qua_dim = ["index","time"]
        self.output_data = super()._data_formation()

        self.output_data["time"] = evo_time
        return self.output_data