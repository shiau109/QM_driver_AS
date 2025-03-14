from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
import sys
import pathlib
# QM_script_root = str(pathlib.Path(__file__).parent.parent.resolve())
# sys.path.append(QM_script_root)
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import warnings
warnings.filterwarnings("ignore")
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)

import exp.config_par as gc
import xarray as xr

from exp.QMMeasurement import QMMeasurement

import numpy as np

class RabiTime( QMMeasurement ):
    def __init__( self, config, qmm: QuantumMachinesManager):
        super().__init__( config, qmm )


        self.freq_range = ( -10, 10) # unit in MHz
        self.freq_resolution = 1. # unit in MHz
        self.time_range =  ( 4,100 ) #unit in ns
        self.time_resolution = 10 #unit in ns
        self.amp_range = (0,2)
        self.amp_resolution = 0.1
        self.xy_elements = ["q0_xy"]
        self.ro_elements = ["q0_ro"]

        self.shot_num = 1

        self.initializer = None
        self.process = "time"
        match self.process:
            case "time":
                self.qua_dim = ["index","frequency", "time"]
            case _:
                self.qua_dim = ["index","frequency", "amplitude"]

        self.preprocess = "average"

    def _get_qua_program( self ):
        time_r1_qua = (self.time_range[0]/4) *u.ns
        time_r2_qua = (self.time_range[1]/4) *u.ns

        if self.time_resolution < 4:
            print( "Warning!! time resolution < 4 ns.")
        time_resolution_qua = (self.time_resolution/4) *u.ns
        self.qua_driving_time = np.arange(time_r1_qua, time_r2_qua, time_resolution_qua)

        freq_r1_qua = self.freq_range[0] * u.MHz
        freq_r2_qua = self.freq_range[1] * u.MHz
        freq_resolution_qua = self.freq_resolution * u.MHz
        self.qua_freqs = np.arange(freq_r1_qua, freq_r2_qua, freq_resolution_qua)
        r_amps = np.arange(self.amp_range[0], self.amp_range[1], self.amp_resolution)


        self.ref_xy_IF = {}
        self.ref_xy_LO = {}
        for xy in self.xy_elements:
            self.ref_xy_IF[xy] = gc.get_IF(xy, self.config)
            self.ref_xy_LO[xy] = gc.get_LO(xy, self.config)

        freq_len = len(self.qua_freqs)
        amp_len = len(r_amps)
        match self.process:
            case "time":
                time_len = len(self.qua_driving_time)
                with program() as rabi: 

                    iqdata_stream = multiRO_declare(self.ro_elements)
                    t = declare(int)  
                    n = declare(int)
                    outermost_st = declare_stream()
                    df = declare(int)  # QUA variable for the readout frequency
                    with for_(n, 0, n < self.shot_num, n + 1):
                        with for_(*from_array(df, self.qua_freqs)):
                            # Update the frequency of the xy elements
                            with for_( *from_array(t, self.qua_driving_time) ):  
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
                                for q in self.xy_elements:
                                    update_frequency(q, self.ref_xy_IF[q]+df)

                                # Operation
                                for q in self.xy_elements:
                                    play("x180", q, t)
                                align()
                                # Measurement
                                multiRO_measurement(iqdata_stream, self.ro_elements, weights="rotated_")
                        # Save iteration
                        save(n, outermost_st)

                    with stream_processing():
                        # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
                        multiRO_pre_save( iqdata_stream, self.ro_elements, (len(self.qua_freqs),len(self.qua_driving_time)), stream_preprocess=self.preprocess)
                        outermost_st.save("outermost_i")
            case _:
                with program() as rabi:
                    iqdata_stream = multiRO_declare(self.ro_elements)
                    ra = declare(fixed)  
                    n = declare(int)
                    outermost_st = declare_stream()
                    df = declare(int)  # QUA variable for the readout frequency
                    with for_(n, 0, n < self.shot_num, n + 1):
                        with for_(*from_array(df, self.qua_freqs)):
                            # Update the frequency of the xy elements
                            with for_( *from_array(ra, r_amps) ):  
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
                                for q in self.xy_elements:
                                    update_frequency(q, self.ref_xy_IF[q]+df)

                                # Operation
                                for q in self.xy_elements:
                                    play("x180"*amp(ra), q)
                                align()
                                # Measurement
                                multiRO_measurement(iqdata_stream, self.ro_elements, weights="rotated_")
                        # Save iteration
                        save(n, outermost_st)

                    with stream_processing():
                        # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
                        multiRO_pre_save( iqdata_stream, self.ro_elements, (len(self.qua_freqs),len(r_amps)), stream_preprocess=self.preprocess)
                        outermost_st.save("outermost_i")
        return rabi
    
    
    # def plot_freq_dep_time_rabi( data, dfs, time, ax=None ):
    #     """
    #     data shape ( 2, N, M )
    #     2 is I,Q
    #     N is freq
    #     M is flux
    #     """
    #     idata = data[0]
    #     qdata = data[1]
    #     zdata = idata +1j*qdata
    #     s21 = zdata

    #     if type(ax)==None:
    #         fig, ax = plt.subplots()
    #         ax.set_title('pcolormesh')
    #         fig.show()
    #     ax[0].pcolormesh( time, dfs, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    #     ax[1].pcolormesh( time, dfs, np.angle(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)


    # def plot_ana_freq_time_rabi( data, dfs, time, freq_LO, freq_IF, ax=None, iq_rotate = 0 ):
    #     """
    #     data shape ( 2, N, M )
    #     2 is I,Q
    #     N is freq
    #     M is time
    #     """
    #     idata = data[0]
    #     qdata = data[1]
    #     zdata = (idata +1j*qdata)*np.exp(1j*iq_rotate)
    #     s21 = zdata

    #     abs_freq = freq_LO+freq_IF+dfs
    #     if type(ax)==None:
    #         fig, ax = plt.subplots()
    #         ax.set_title('pcolormesh')
    #         fig.show()
    #     ax[0].pcolormesh( time, abs_freq, np.real(zdata), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    #     # ax[0].axvline(x=freq_LO+freq_IF, color='b', linestyle='--', label='ref IF')
    #     # ax[0].axvline(x=freq_LO, color='r', linestyle='--', label='LO')
    #     ax[0].axhline(y=freq_LO+freq_IF, color='black', linestyle='--', label='ref IF')

    #     ax[0].legend()
    #     ax[1].pcolormesh( time, abs_freq, np.imag(zdata), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    #     ax[1].axhline(y=freq_LO+freq_IF, color='black', linestyle='--', label='ref IF')

    #     ax[1].legend()

    # def _get_fetch_data_list( self ):
    #     ro_ch_name = []
    #     for r_name in self.ro_elements:
    #         ro_ch_name.append(f"{r_name}_I")
    #         ro_ch_name.append(f"{r_name}_Q")

    #     data_list = ro_ch_name + ["iteration"]   
    #     return data_list

    def _data_formation( self ):
        freqs_mhz = self.qua_freqs/1e6
        match self.process:
            case "time":
                self.qua_dim = ["index","frequency", "time"]
                self.output_data = super()._data_formation()

                self.output_data["frequency"] = freqs_mhz

                driving_time = self.qua_driving_time *4
                self.output_data["time"] = driving_time

                self.output_data.attrs["ref_xy_IF"] = list(self.ref_xy_IF.values())
                self.output_data.attrs["ref_xy_LO"] = list(self.ref_xy_LO.values())
            case _:
                self.qua_dim = ["index","frequency", "amplitude"]
                self.output_data = super()._data_formation()

                self.output_data["frequency"] = freqs_mhz

                r_amps = np.arange(self.amp_range[0], self.amp_range[1], self.amp_resolution)
                self.output_data["amplitude"] = r_amps

                self.output_data.attrs["ref_xy_IF"] = list(self.ref_xy_IF.values())
                self.output_data.attrs["ref_xy_LO"] = list(self.ref_xy_LO.values())

        return self.output_data