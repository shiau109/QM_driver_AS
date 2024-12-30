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
import exp.config_par as gc
from scipy.optimize import curve_fit
import warnings
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import xarray as xr
warnings.filterwarnings("ignore")
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
import time
from exp.QMMeasurement import QMMeasurement

class z_pulse_relaxation_time( QMMeasurement ):
    def __init__( self, config, qmm: QuantumMachinesManager):
        super().__init__( config, qmm )
        self.max_time = 20
        self.time_resolution = 0.2
        self.flux_range = [-0.3,0.3]
        self.flux_resolution = 0.006
        self.q_name = ["q3_xy"]
        self.z_name = ["q8_z"]
        self.ro_elements = ["q3_ro", "q4_ro"]
        self.n_avg = 100
        self.initializer = None
        self.simulate = False
        self.ref_z_offset = {"q8_z": gc.get_offset("q8_z", config)}
        
    def _get_qua_program( self ):
        """
        parameters: \n
        max_time: unit in us, can't < 20 ns \n
        time_resolution: unit in us, can't < 4 ns \n

        Return: \n
        xarray with value 2*N array \n
        coors: ["mixer","z_voltage","time"]\n
        attrs: z_offset\n
        time unit in ns \n
        """
        self.fluxes = np.arange(self.flux_range[0], self.flux_range[1], self.flux_resolution)
        fluxes_len = self.fluxes.shape[-1]

        cc_max_qua = (self.max_time/4) * u.us
        cc_resolution_qua = (self.time_resolution/4) * u.us
        cc_delay_qua = np.arange( 4, cc_max_qua, cc_resolution_qua)
        self.evo_time = cc_delay_qua*4
        evo_time_len = cc_delay_qua.shape[-1]
        
        # QUA program
        with program() as t1:

            iqdata_stream = multiRO_declare( self.ro_elements )
            t = declare(int)  
            dc = declare(fixed)  
            n = declare(int)
            n_st = declare_stream()
            with for_(n, 0, n < self.n_avg, n + 1):
                with for_(*from_array(dc, self.fluxes)):
                    with for_(*from_array(t, cc_delay_qua)):
                        # initializaion
                        if self.initializer is None:
                            wait(1*u.us,self.ro_elements)
                        else:
                            try:
                                self.initializer[0](*self.initializer[1])
                            except:
                                wait(1*u.us,self.ro_elements)

                        # Operation
                        for q in self.q_name:
                            play("x180", q)
                        wait(25)    
                        for z_name, ref_z in self.ref_z_offset.items():
                            set_dc_offset( z_name, "single", ref_z +dc)
                            # assign(index, 0)
                        wait(t)
                        for z_name, ref_z in self.ref_z_offset.items():
                            set_dc_offset( z_name, "single", ref_z)
                        wait(25)                         
                        # align()
                        # Readout
                        multiRO_measurement( iqdata_stream,  resonators=self.ro_elements, weights="rotated_")
                    
                # Save the averaging iteration to get the progress bar
                save(n, n_st)

            with stream_processing():
                n_st.save("iteration")
                multiRO_pre_save(iqdata_stream, self.ro_elements, (fluxes_len, evo_time_len) )

        return t1

    def _get_fetch_data_list( self ):
        ro_ch_name = []
        for r_name in self.ro_elements:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")

        data_list = ro_ch_name + ["iteration"]   
        return data_list
    
    def _data_formation( self ):
        output_data = {}
        for r_idx, r_name in enumerate(self.ro_elements):
            output_data[r_name] = ( ["mixer","z_voltage","time"],
                                np.array([self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]]) )
        dataset = xr.Dataset(
            output_data,
            coords={ "mixer":np.array(["I","Q"]), "time": self.evo_time, "z_voltage":self.fluxes }
        )
    
        dataset.attrs["z_offset"] = list(self.ref_z_offset.values())
        return dataset