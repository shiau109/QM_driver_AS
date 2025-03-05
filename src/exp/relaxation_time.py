from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
from qualang_tools.plot.fitting import Fit
# from common_fitting_func import gaussian
from scipy.optimize import curve_fit
import warnings
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save

import xarray as xr
warnings.filterwarnings("ignore")
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)

import numpy as np
import time

from exp.QMMeasurement import QMMeasurement
class exp_relaxation_time( QMMeasurement):
    def __init__( self, config, qmm: QuantumMachinesManager):
        super().__init__( config, qmm )
        """
        parameters: \n
        max_time: unit in us, can't < 20 ns \n
        time_resolution: unit in us, can't < 4 ns \n

        Return: \n
        xarray with value 2*N array
        coords: ["mixer","time"]
        max_time unit in us \n
        """
        self.max_time = 5
        self.time_resolution = 0.1
        self.xy_elements = ['q3_xy']
        self.ro_elements = ['q3_ro']
        self.initializer = None

        self.qua_dim = ["index","time"]

        self.preprocess = "average"

    def _get_qua_program( self ):
        cc_max_qua = (self.max_time/4) * u.us
        cc_resolution_qua = (self.time_resolution/4) * u.us
        cc_delay_qua = np.arange( 4, cc_max_qua, cc_resolution_qua)
        self.evo_time = cc_delay_qua*4
        evo_time_len = cc_delay_qua.shape[-1]
        # QUA program
        with program() as t1:

            iqdata_stream = multiRO_declare( self.ro_elements )
            t = declare(int)  
            n = declare(int)
            outermost_st = declare_stream()
            with for_(n, 0, n < self.shot_num, n + 1):
                with for_(*from_array(t, cc_delay_qua)):
                    # initializaion
                    if self.initializer is None:
                        wait(1*u.us, self.ro_elements)
                    else:
                        try:
                            self.initializer[0](*self.initializer[1])
                        except:
                            wait(1*u.us, self.ro_elements)

                    # Operation   
                    for q in self.xy_elements:
                        play("x180", q)
                        wait(t, q)
                    align()
                    # Readout
                    multiRO_measurement( iqdata_stream,  resonators= self.ro_elements, weights="rotated_")
                    
                # Save the averaging iteration to get the progress bar
                save(n, outermost_st)

            with stream_processing():
                # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
                multiRO_pre_save( iqdata_stream, self.ro_elements, (evo_time_len, ), stream_preprocess=self.preprocess)
                outermost_st.save("outermost_i")

        return t1
    
    def _data_formation( self ):
        self.qua_dim = ["index","time"]
        self.output_data = super()._data_formation()

        self.output_data["time"] = self.evo_time
        return self.output_data

