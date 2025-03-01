
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm.simulate import SimulationConfig
# from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.analysis import two_state_discriminator
# from exp.macros import qua_declaration, multiplexed_readout, reset_qubit
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import numpy as np
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
import xarray as xr
import time
import numpy as np
from exp.QMMeasurement import QMMeasurement
import exp.config_par as gc

class ROFidelity( QMMeasurement ):
    """
    Parameters:\n

    Output:\n
    Dataset:\n
    coords: "mixer","frequency","prepare_state"

    """
    def __init__( self, config, qmm: QuantumMachinesManager ):
        super().__init__( config, qmm )

        self.ro_elements = ["q0_ro"]
        # self.z_elements = ["q0_z"]
        self.xy_elements = ["q0_xy"]

        self.initializer = None

        self.amp_mod_range = (0.5, 1.5)
        self.amp_resolution = 0.1

        self.qua_dim = ["index","prepare_state"]

        self.preprocess = "shot"

    def _get_qua_program( self ):
        
        self.qua_amp_ratio_array = self._lin_amp_ratio_array()

        self._attribute_config()
        

        with program() as iq_blobs:

            iqdata_stream = multiRO_declare( self.ro_elements )

            n = declare(int)
            outermost_st = declare_stream()
            p_idx = declare(int)
            with for_(n, 0, n < self.shot_num, n + 1):

                with for_each_( p_idx, [0, 1]):  
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
                        
                    # Operation
                    with switch_(p_idx, unsafe=True):
                        with case_(0):
                            pass
                        with case_(1):
                            for q in self.xy_elements:
                                play("x180", q)
                    align()
                    # Readout
                    multiRO_measurement(iqdata_stream, self.ro_elements, weights="rotated_")  
                save(n, outermost_st)

            with stream_processing():
                # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
                multiRO_pre_save( iqdata_stream, self.ro_elements, (2,), stream_preprocess=self.preprocess)
                outermost_st.save("outermost_i")

        return iq_blobs
    
    def _data_formation( self ):
        self.qua_dim = ["index","prepare_state"]
        self.output_data = super()._data_formation()

        self.output_data["prepare_state"] = [0, 1]

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



