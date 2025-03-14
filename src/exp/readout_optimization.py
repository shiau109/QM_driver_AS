
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
# from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool, progress_counter
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save

import warnings

warnings.filterwarnings("ignore")

from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
import xarray as xr
import time

from exp.QMMeasurement import QMMeasurement
import exp.config_par as gc
import numpy as np
class ROAmp( QMMeasurement ):
    """
    Parameters:\n

    Output:\n
    Dataset:\n
    coords: "mixer","frequency","prepare_state"

    """
    def __init__( self, config, qmm: QuantumMachinesManager ):
        super().__init__( config, qmm )

        self.ro_elements = ["q4_ro"]
        # self.z_elements = ["q0_z"]
        self.xy_elements = ["q4_xy"]

        self.initializer = None

        self.amp_mod_range = (0.5, 1.5)
        self.amp_resolution = 0.1

        self.qua_dim = ["index","amplitude_ratio", "prepare_state"]

        self.preprocess = "average"

    def _get_qua_program( self ):
        
        self.qua_amp_ratio_array = self._lin_amp_ratio_array()

        self._attribute_config()
        

        with program() as multi_res_spec_vs_amp:
        
            iqdata_stream = multiRO_declare(self.ro_elements)
            n = declare(int)
            outermost_st = declare_stream()
            r_amp = declare(fixed)  # QUA variable for the readout frequency
            p_idx = declare(bool,)
            with for_(n, 0, n < self.shot_num, n + 1):
                with for_(*from_array(r_amp, self.qua_amp_ratio_array)):
                    # Update the frequency of the two resonator elements
                    with for_each_( p_idx, [False, True]):  
                        # Init
                        if self.initializer is None:
                            wait(100*u.us)
                            #wait(thermalization_time * u.ns)
                        else:
                            try:
                                self.initializer[0](*self.initializer[1])
                            except:
                                print("Initializer didn't work!")
                                wait(100*u.us)
                        align()
                        # Operation
                        with if_(p_idx):
                            for q in self.xy_elements:
                                play("x180", q)
                        align()
                        # Measurement
                        multiRO_measurement(iqdata_stream, self.ro_elements, weights="rotated_",amp_modify=r_amp)
                # Save the averaging iteration to get the progress bar
                save(n, outermost_st)

            with stream_processing():
                outermost_st.save("outermost_i")
                multiRO_pre_save( iqdata_stream, self.ro_elements, (len(self.qua_amp_ratio_array),2), stream_preprocess=self.preprocess)


        return multi_res_spec_vs_amp
    
    def _data_formation( self ):
        self.qua_dim = ["index","amplitude_ratio", "prepare_state"]
        self.output_data = super()._data_formation()

        amp_ratio = self.qua_amp_ratio_array
        self.output_data["amplitude_ratio"] = amp_ratio

        self.output_data["prepare_state"] = np.array([0,1])

        self._attribute_config()
        self.output_data.attrs["ro_LO"] = self.ref_ro_LO
        self.output_data.attrs["ro_IF"] = self.ref_ro_IF
        self.output_data.attrs["xy_LO"] = self.ref_xy_LO
        self.output_data.attrs["xy_IF"] = self.ref_xy_IF
        self.output_data.attrs["xy_elements"] = self.xy_elements


        return self.output_data

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


    def _lin_amp_ratio_array( self ):
        amp_ratio = np.arange( self.amp_mod_range[0],self.amp_mod_range[1], self.amp_resolution)
        return amp_ratio




class ROFreq( QMMeasurement ):
    """
    Parameters:\n

    Output:\n
    Dataset:\n
    coords: "mixer","frequency","prepare_state"

    """
    def __init__( self, config, qmm: QuantumMachinesManager ):
        super().__init__( config, qmm )

        self.ro_elements = ["q4_ro"]
        # self.z_elements = ["q0_z"]
        self.xy_elements = ["q4_xy"]

        self.initializer = None

        self.freq_range = ( -1, 1 )
        self.freq_resolution = 0.5

        self.amp_mod = 1

        self.qua_dim = ["index", "frequency", "prepare_state"]

        self.preprocess = "average"

    def _get_qua_program( self ):
        
        self.qua_freqs = self._lin_freq_array()

        self._attribute_config()
        

        with program() as multi_res_spec_vs_amp:
        
            iqdata_stream = multiRO_declare(self.ro_elements)
            n = declare(int)
            outermost_st = declare_stream()
            df = declare(int)  # QUA variable for the readout frequency
            p_idx = declare(bool,)
            with for_(n, 0, n < self.shot_num, n + 1):
                with for_(*from_array(df, self.qua_freqs)):
                    # Update the frequency of the two resonator elements
                    with for_each_( p_idx, [False, True]):  
                        # Init
                        if self.initializer is None:
                            wait(100*u.us)
                            #wait(thermalization_time * u.ns)
                        else:
                            try:
                                self.initializer[0](*self.initializer[1])
                            except:
                                print("Initializer didn't work!")
                                wait(100*u.us)
                        align()
                        # Operation
                        with if_(p_idx):
                            for q in self.xy_elements:
                                play("x180", q)
                        align()
                        # Measurement
                        for i, r in enumerate(self.ro_elements):
                            update_frequency(r, df +self.ref_ro_IF[i])
                        multiRO_measurement(iqdata_stream, self.ro_elements, weights="rotated_",amp_modify=self.amp_mod)
                # Save the averaging iteration to get the progress bar
                save(n, outermost_st)

            with stream_processing():
                outermost_st.save("outermost_i")
                multiRO_pre_save( iqdata_stream, self.ro_elements, (len(self.qua_freqs),2), stream_preprocess=self.preprocess)

        return multi_res_spec_vs_amp
    
    def _data_formation( self ):
        self.qua_dim = ["index", "frequency", "prepare_state"]
        self.output_data = super()._data_formation()

        freqs_mhz = self.qua_freqs/1e6
        self.output_data["frequency"] = freqs_mhz

        self.output_data["prepare_state"] = np.array([0,1])

    
        self._attribute_config()
        self.output_data.attrs["ro_LO"] = self.ref_ro_LO
        self.output_data.attrs["ro_IF"] = self.ref_ro_IF
        self.output_data.attrs["xy_LO"] = self.ref_xy_LO
        self.output_data.attrs["xy_IF"] = self.ref_xy_IF
        self.output_data.attrs["xy_elements"] = self.xy_elements


        return self.output_data

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


    def _lin_freq_array( self ):

        freq_r1_qua = self.freq_range[0] * u.MHz
        freq_r2_qua = self.freq_range[1] * u.MHz
        freq_resolution_qua = self.freq_resolution * u.MHz
        freqs_qua = np.arange(freq_r1_qua,freq_r2_qua,freq_resolution_qua )
        
        return freqs_qua




class ROFreqAmpMapping( QMMeasurement ):
    """
    Parameters:\n

    Output:\n
    Dataset:\n
    coords: "mixer","frequency","amp_ratio","prepare_state"

    """
    def __init__( self, config, qmm: QuantumMachinesManager ):
        super().__init__( config, qmm )

        self.ro_elements = ["q4_ro"]
        # self.z_elements = ["q0_z"]
        self.xy_elements = ["q4_xy"]
        self.preprocess = "ave"
        self.initializer = None
        
        self.amp_mod_range = (0.5, 1.5)
        self.amp_resolution = 0.1

        self.freq_range = ( -1, 1 )
        self.freq_resolution = 0.5

        

    def _get_qua_program( self ):
        
        self.qua_amp_ratio_array = self._lin_amp_ratio_array()
        # print(self.qua_cc_pi_timing)
        self.qua_freqs = self._lin_freq_array()

        self._attribute_config()
        

        with program() as multi_res_spec_vs_amp:
        
            iqdata_stream = multiRO_declare( self.ro_elements )
            n = declare(int)
            n_st = declare_stream()
            df = declare(int)
            r_amp = declare(fixed)
            p_idx = declare(bool, )

            with for_(n, 0, n < self.shot_num, n + 1):

                with for_(*from_array(df, self.qua_freqs)):
                    with for_(*from_array(r_amp, self.qua_amp_ratio_array)):
                        with for_each_( p_idx, [False, True]):  

                            # Init
                            if self.initializer is None:
                                wait(100*u.us)
                                #wait(thermalization_time * u.ns)
                            else:
                                try:
                                    self.initializer[0](*self.initializer[1])
                                except:
                                    print("Initializer didn't work!")
                                    wait(100*u.us)
                            align()
                            # Operation
                            with if_(p_idx):
                                for q in self.xy_elements:
                                    play("x180", q)
                            align()
                            # Measurement
                            for i, r in enumerate(self.ro_elements):
                                update_frequency(r, df +self.ref_ro_IF[i])
                            multiRO_measurement(iqdata_stream, self.ro_elements, weights="rotated_",amp_modify=r_amp)
                # Save the averaging iteration to get the progress bar
                save(n, n_st)

            with stream_processing():
                n_st.save("iteration")
                # NOTE that the buffering goes from the most inner loop (left) to the most outer one (right)
                match self.preprocess:
                    case "shot":
                        multiRO_pre_save( iqdata_stream, self.ro_elements, (self.shot_num, len(self.qua_freqs), len(self.qua_amp_ratio_array),2), stream_preprocess="shot")
                    case _:
                        multiRO_pre_save( iqdata_stream, self.ro_elements, (len(self.qua_freqs), len(self.qua_amp_ratio_array),2))

        return multi_res_spec_vs_amp
    
    def _get_fetch_data_list( self ):
        ro_ch_name = []
        for r_name in self.ro_elements:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")

        data_list = ro_ch_name + ["iteration"]   
        return data_list
    
    def _data_formation( self ):
        freqs_mhz = self.qua_freqs/1e6
        amp_ratio = self.qua_amp_ratio_array
        coords = { 
            "mixer":np.array(["I","Q"]), 
            "frequency": freqs_mhz, 
            "amp_ratio":amp_ratio,
            "prepare_state": np.array([0,1])
            }
        match self.preprocess:
            case "shot":
                dims_order = ["mixer","shot","frequency","amp_ratio","prepare_state"]
                coords["shot"] = np.arange(self.shot_num)
            case _:
                dims_order = ["mixer","frequency","amp_ratio","prepare_state"]

        output_data = {}
        for r_idx, r_name in enumerate(self.ro_elements):
            data_array = np.array([ self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]])
            output_data[r_name] = ( dims_order, np.squeeze(data_array))

        dataset = xr.Dataset( output_data, coords=coords )

        # dataset = dataset.transpose("mixer", "prepare_state", "frequency", "amp_ratio")

        self._attribute_config()
        dataset.attrs["ro_LO"] = self.ref_ro_LO
        dataset.attrs["ro_IF"] = self.ref_ro_IF
        dataset.attrs["xy_LO"] = self.ref_xy_LO
        dataset.attrs["xy_IF"] = self.ref_xy_IF


        return dataset

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


    def _lin_freq_array( self ):

        freq_r1_qua = self.freq_range[0] * u.MHz
        freq_r2_qua = self.freq_range[1] * u.MHz
        freq_resolution_qua = self.freq_resolution * u.MHz
        freqs_qua = np.arange(freq_r1_qua,freq_r2_qua,freq_resolution_qua )
        
        return freqs_qua

    def _lin_amp_ratio_array( self ):
        amp_ratio = np.arange( self.amp_mod_range[0],self.amp_mod_range[1], self.amp_resolution)
        return amp_ratio
    

