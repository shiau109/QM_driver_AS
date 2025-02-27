from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qualang_tools.loops import from_array
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)

import xarray as xr
import exp.config_par as gc
from xarray import DataArray

from exp.QMMeasurement import QMMeasurement

import numpy as np

class ROFreqSweepPowerDep( QMMeasurement ):
    """
    Parameters:\n
    freq_span:\n
        a tuple (upper, lower) Unit in MHz, \n
    amp_max_ratio: \n

    amp_scale: \n
        lin or log \n
    Return: xarray dataset
        coords : frequency, amp_ratio
    """
    def __init__( self, config, qmm: QuantumMachinesManager ):
        super().__init__( config, qmm )

        self.ro_elements = ["q0_ro"]
        # self.z_elements = []
        self.xy_elements = []

        self.initializer = None
        
        self.amp_scale = "lin"

        self.amp_mod_range = ( 0.5, 1.5 )
        self.amp_resolution = 0.05

        self.freq_range = ( -10, 10 )
        self.freq_resolution = 1

        self.qua_dim = ["index","amp_ratio","frequency"]

        self.preprocess = "average"

        

    def _get_qua_program( self ):
        
        self.amp_ratio = self._get_amp_ratio_array()
        print(self.amp_ratio)
        self.frequencies_qua = self._lin_freq_array()
        self._attribute_config()
        

        with program() as multi_res_spec_vs_amp:
        
            iqdata_stream = multiRO_declare( self.ro_elements )
            n = declare(int)
            outermost_st = declare_stream()
            df = declare(int)
            a = declare(fixed)

            with for_(n, 0, n < self.shot_num, n + 1):
                # with for_(*qua_logspace(a, -1, 0, 2)):
                with for_(*from_array(a, self.amp_ratio)):
                    
                    with for_(*from_array(df, self.frequencies_qua)):
                        # Initialization
                        if self.initializer is None:
                            wait(1*u.us, self.ro_elements)
                        else:
                            try:
                                self.initializer[0](*self.initializer[1])
                            except:
                                print("initializer didn't work!")
                                wait(1*u.us, self.ro_elements)

                        # Operation    
                        for i, r in enumerate(self.ro_elements):
                            update_frequency( r, self.ref_ro_IF[i]+df)
                        
                        # Readout
                        multiRO_measurement( iqdata_stream, self.ro_elements, amp_modify=a, weights='rotated_' )

                save(n, outermost_st)

            with stream_processing():
                # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
                multiRO_pre_save( iqdata_stream, self.ro_elements, (len(self.amp_ratio), len(self.frequencies_qua),), stream_preprocess=self.preprocess)
                outermost_st.save("outermost_i")


        return multi_res_spec_vs_amp
    
    def _data_formation( self )->DataArray:

        self.qua_dim = ["index","amp_ratio","frequency"]
        self.output_data = super()._data_formation()

        self.output_data["amp_ratio"] = self.amp_ratio

        frequencies_mhz = self.frequencies_qua/1e6 #  Unit in MHz
        self.output_data["frequency"] = frequencies_mhz

        self.output_data.attrs["ro_LO"] = self.ref_ro_LO
        self.output_data.attrs["ro_IF"] = self.ref_ro_IF

        return self.output_data

    def _lin_freq_array( self ):

        freq_r1_qua = self.freq_range[0] * u.MHz
        freq_r2_qua = self.freq_range[1] * u.MHz
        freq_resolution_qua = self.freq_resolution * u.MHz
        freqs_qua = np.arange(freq_r1_qua,freq_r2_qua,freq_resolution_qua )
        
        return freqs_qua

    def _lin_amp_ratio_array( self ):
        amp_ratio = np.arange( self.amp_mod_range[0],self.amp_mod_range[1]+self.amp_resolution/2, self.amp_resolution)
        return amp_ratio
    
    def _log_amp_ratio_array( self ):
        amp_num = int( (self.amp_mod_range[1]-self.amp_mod_range[0])/self.amp_resolution )
        amp_ratio = np.logspace(self.amp_mod_range[0], self.amp_mod_range[1], amp_num)
        return amp_ratio
    
    def _get_amp_ratio_array( self ):
        match self.amp_scale:
            case "lin": return self._lin_amp_ratio_array()
            case "log": return  self._log_amp_ratio_array()
            case _: return self._lin_amp_ratio_array()    

    def _attribute_config( self ):
        self.ref_ro_IF = []
        self.ref_ro_LO = []
        for r in self.ro_elements:
            self.ref_ro_IF.append(gc.get_IF(r, self.config))
            self.ref_ro_LO.append(gc.get_LO(r, self.config))