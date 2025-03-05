from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qualang_tools.loops import from_array
import exp.config_par as gc

from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save

import warnings
warnings.filterwarnings("ignore")

from qualang_tools.units import unit
u = unit(coerce_to_integer=True)

from exp.QMMeasurement import QMMeasurement

import xarray as xr
import numpy as np

class XYAmpCalibraion( QMMeasurement ):

    def __init__( self, config, qmm: QuantumMachinesManager ):
        super().__init__( config, qmm )
        self.ro_elements = ['q4_ro']
        self.xy_elements = ['q4_xy']
        
        self.sequence_repeat = 1
        self.amp_modify_range = None
        self.range_modifier = 0.25
        self.amp_modify_resolution = None
        self.initializer = None

        self.qua_dim = ["index","sequence", "amplitude_ratio"]

        self.preprocess = "average"

    def _get_qua_program(self):

        if self.amp_modify_range is None:
            range_dis = self.range_modifier/float(self.sequence_repeat)
            self.amp_modify_range = (1-range_dis,1+range_dis)
            self.amp_modify_resolution = range_dis/50.

        self.amp_ratios = self._lin_amp_ratio_array()
        amp_len = len(self.amp_ratios)
        with program() as qua_prog:
            n = declare(int)  # QUA variable for the averaging loop
            a = declare(fixed)  # QUA variable for the DRAG coefficient pre-factor
            r_idx = declare(int)  # QUA variable for the measured 'I' quadrature
            iqdata_stream = multiRO_declare( self.ro_elements )
            outermost_st = declare_stream()  # Stream for the averaging iteration 'n'
            
            with for_(n, 0, n < self.shot_num, n + 1):
                with for_each_(r_idx, [0, 1]):
                    with for_(*from_array(a, self.amp_ratios)):  
                    # Init
                        if self.initializer is None:
                            # wait(thermalization_time * u.ns)
                            wait(100 * u.us)
                        else:
                            try:
                                self.initializer[0](*self.initializer[1])
                            except:
                                print("Initializer didn't work!")
                                wait(100*u.us)
                        with switch_(r_idx, unsafe=True):
                            with case_(0):
                                for xy in self.xy_elements:
                                    for _ in range(self.sequence_repeat):
                                        play('x180' * amp(a), xy)
                                        play('x180' * amp(a), xy)
                            with case_(1):
                                for xy in self.xy_elements:
                                    for _ in range(self.sequence_repeat):
                                        play('x90' * amp(a), xy)
                                        play('x90' * amp(a), xy)
                                        play('x90' * amp(a), xy)
                                        play('x90' * amp(a), xy)
                            # Align after playing the qubit pulses.
                        align()
                            # Readout
                        multiRO_measurement(iqdata_stream, self.ro_elements, weights="rotated_")         
                    
                save(n, outermost_st)
            with stream_processing():
                # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
                multiRO_pre_save(iqdata_stream, self.ro_elements, (2, amp_len), stream_preprocess=self.preprocess)
                outermost_st.save("outermost_i")

        return qua_prog
    
    def _data_formation( self ):
        self.qua_dim = ["index","sequence", "amplitude_ratio"]
        self.output_data = super()._data_formation()

        self.output_data["sequence"] = ["x180","x90"]

        param_val = self.amp_ratios
        self.output_data["amplitude_ratio"] = param_val

        return self.output_data
            
    def _lin_amp_ratio_array( self ):
        amp_r1_qua = self.amp_modify_range[0]
        amp_r2_qua = self.amp_modify_range[1]
        d_amp_qua = self.amp_modify_resolution
        amp_qua = np.arange(amp_r1_qua,amp_r2_qua,d_amp_qua )
        
        return amp_qua
            
        
    def _attribute_config( self ):
        self.ref_ro_IF = []
        self.ref_ro_LO = []
        for r in self.ro_elements:
            self.ref_ro_IF.append(gc.get_IF(r, self.config))
            self.ref_ro_LO.append(gc.get_LO(r, self.config))

        self.ref_xy_IF = []
        self.ref_xy_LO = []
        for xy in self.xy_elements:
            self.ref_xy_IF.append(gc.get_IF(xy, self.config))
            self.ref_xy_LO.append(gc.get_LO(xy, self.config))
