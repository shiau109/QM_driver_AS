
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

class ExpTemp( QMMeasurement ):
    """
    Parameters:\n

    Output:\n
    Dataset:\n
    coords: "mixer",

    """
    def __init__( self, config, qmm: QuantumMachinesManager ):
        super().__init__( config, qmm )

        self.ro_elements = ["q0_ro"]
        self.z_elements = ["q0_z"]
        self.xy_elements = ["q0_xy"]

        self.initializer = None
        self.preprocess = "ave"


    def _get_qua_program( self ):
        
        self._attribute_config()

        with program() as qua_program:
        
            iqdata_stream = multiRO_declare(self.ro_elements)
            n = declare(int)
            n_st = declare_stream()

            with for_(n, 0, n < self.shot_num, n + 1):
                
                for q in self.xy_elements:
                    play("x180", q)
                # Measurement
                align()
                multiRO_measurement(iqdata_stream, self.ro_elements, weights="rotated_")
                # Save the averaging iteration to get the progress bar
                save(n, n_st)

            with stream_processing():
                n_st.save("iteration")
                match self.preprocess:
                    case "shot":
                        multiRO_pre_save( iqdata_stream, self.ro_elements, (self.shot_num, 2), stream_preprocess="shot")
                    case _:
                        multiRO_pre_save( iqdata_stream, self.ro_elements, (2,))
                

        return qua_program
    
    def _get_fetch_data_list( self ):
        ro_ch_name = []
        for r_name in self.ro_elements:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")

        data_list = ro_ch_name + ["iteration"]   
        return data_list
    
    def _data_formation( self ):

        coords = { 
            "mixer":np.array(["I","Q"]), 
            "prepare_state": np.array([0,1]),
            }
        match self.preprocess:
            case "shot":
                dims_order = ["mixer","shot"]
                coords["shot"] = np.arange(self.shot_num)
            case _:
                dims_order = ["mixer",]

        output_data = {}
        for r_idx, r_name in enumerate(self.ro_elements):
            data_array = np.array([ self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]])
            output_data[r_name] = ( dims_order, np.squeeze(data_array))

        dataset = xr.Dataset(output_data, coords=coords)

        self._attribute_config()
        dataset.attrs["ro_LO"] = self.ref_ro_LO
        dataset.attrs["ro_IF"] = self.ref_ro_IF
        dataset.attrs["xy_LO"] = self.ref_xy_LO
        dataset.attrs["xy_IF"] = self.ref_xy_IF
        dataset.attrs["xy_elements"] = self.xy_elements


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




