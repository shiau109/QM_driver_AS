from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qualang_tools.loops import from_array
import exp.config_par as gc
import numpy as np

from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save

import warnings
warnings.filterwarnings("ignore")

from qualang_tools.units import unit
u = unit(coerce_to_integer=True)

from exp.QMMeasurement import QMMeasurement
from ab.QM_config_dynamic import initializer

import xarray as xr

class SQ_deterministic_benchmarking_all( QMMeasurement ):

    def __init__( self, config, qmm: QuantumMachinesManager ):
        super().__init__( config, qmm )
        self.ro_elements = ['q4_ro']
        self.xy_elements = ['q4_xy']
        self.gate_time = 40
        self.sequence_repeat = 300
        self.initializer = initializer(120000,mode='wait')
        self.threshold = -1.787e-03

    def _get_qua_program(self):
        
        # 0 = T1
        # 1 = X X (T2 echo)
        # 2 = Y Y (rotational error)
        # 3 = Y -Y (phase error)
        
        with program() as qua_prog:
            n = declare(int)  # QUA variable for the averaging loop
            rep = declare(int)  # QUA variable for the measured 'repeat' quadrature
            t = declare(int)
            r_idx = declare(int)
            iqdata_stream = multiRO_declare( self.ro_elements )
            n_st = declare_stream()  # Stream for the averaging iteration 'n'
            state = [declare(bool) for _ in range(len(self.ro_elements))]  # QUA variable for state discrimination
            state_st = [declare_stream() for _ in range(len(self.ro_elements))]
            with for_(n, 0, n < self.shot_num, n + 1):
                with for_each_(r_idx, [0, 1, 2, 3]):
                    with switch_(r_idx, unsafe=True):
                        
                        with case_(0):
                            with for_(t, self.gate_time*2, t <= self.gate_time*self.sequence_repeat*2, t + self.gate_time*2):
                                # initializaion
                                try:
                                    self.initializer[0](*self.initializer[1])
                                except:
                                    print("Initializer didn't work!")
                                    wait(100*u.us)

                                # Operation   
                                for q in self.xy_elements:
                                    play("x180", q)
                                    wait(t, q)
                                align()
                                # Readout
                                multiRO_measurement( iqdata_stream,  resonators= self.ro_elements, weights="rotated_")
                                for idx_res, res in enumerate(self.ro_elements):
                                    assign(state[idx_res], iqdata_stream[0][idx_res] > self.threshold)
                                    save(state[idx_res], state_st[idx_res])
                                
                        with case_(1):
                            with for_(rep, 1, rep <= self.sequence_repeat, rep + 1):
                                # Init
                                try:
                                    self.initializer[0](*self.initializer[1])
                                except:
                                    print("Initializer didn't work!")
                                    wait(100*u.us)
                                i = declare(int)
                                for xy in self.xy_elements:
                                    play('y90', xy)
                                    wait(4, q)
                                    with for_(i, 0, i < rep, i + 1):
                                        play('x180', xy)
                                        wait(4, q)
                                        play('x180', xy)
                                        wait(4, q)
                                    play('-y90', xy)
                                align()
                                # Readout
                                multiRO_measurement(iqdata_stream, self.ro_elements, weights="rotated_")        
                                for idx_res, res in enumerate(self.ro_elements):
                                    assign(state[idx_res], iqdata_stream[0][idx_res] > self.threshold)
                                    save(state[idx_res], state_st[idx_res])
                        
                        with case_(2):
                            with for_(rep, 1, rep <= self.sequence_repeat, rep + 1):
                                # Init
                                try:
                                    self.initializer[0](*self.initializer[1])
                                except:
                                    print("Initializer didn't work!")
                                    wait(100*u.us)
                                i = declare(int)
                                for xy in self.xy_elements:
                                    play('y90', xy)
                                    wait(4, q)
                                    with for_(i, 0, i < rep, i + 1):
                                        play('y180', xy)
                                        wait(4, q)
                                        play('y180', xy)
                                        wait(4, q)
                                    play('-y90', xy)
                                align()
                                # Readout
                                multiRO_measurement(iqdata_stream, self.ro_elements, weights="rotated_")     
                                for idx_res, res in enumerate(self.ro_elements):
                                    assign(state[idx_res], iqdata_stream[0][idx_res] > self.threshold)
                                    save(state[idx_res], state_st[idx_res])
                                        
                        with case_(3):
                            with for_(rep, 1, rep <= self.sequence_repeat, rep + 1):
                                # Init
                                try:
                                    self.initializer[0](*self.initializer[1])
                                except:
                                    print("Initializer didn't work!")
                                    wait(100*u.us)
                                i = declare(int)
                                for xy in self.xy_elements:
                                    play('y90', xy)
                                    wait(4, q)
                                    with for_(i, 0, i < rep, i + 1):
                                        play('y180', xy)
                                        wait(4, q)
                                        play('-y180', xy)
                                        wait(4, q)
                                    play('-y90', xy)
                                align()
                                # Readout
                                multiRO_measurement(iqdata_stream, self.ro_elements, weights="rotated_")     
                                for idx_res, res in enumerate(self.ro_elements):
                                    assign(state[idx_res], iqdata_stream[0][idx_res] > self.threshold)
                                    save(state[idx_res], state_st[idx_res])
                                        
                save(n, n_st)
            with stream_processing():
                # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
                multiRO_pre_save(iqdata_stream, self.ro_elements, (4,self.sequence_repeat) )
                for idx_res, res in enumerate(self.ro_elements):
                    state_st[idx_res].boolean_to_int().buffer(4,self.sequence_repeat).average().save(f"{res}_state")
                n_st.save("iteration")

        return qua_prog
    
    def _get_fetch_data_list( self ):

        ro_ch_name = []
        for r_name in self.ro_elements:
            ro_ch_name.append(f"{r_name}_state")
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")
        data_list = ro_ch_name + ["iteration"]
        return data_list
    
    def _data_formation( self ):

        param_name = 'repeat_time'
        param_val = np.arange(0, self.sequence_repeat, 1)

        output_data = {}
        for r_idx, r_name in enumerate(self.ro_elements):
            output_data[r_name] = ( ["mixer", "sequence", param_name],
                                np.array([self.fetch_data[3*r_idx], self.fetch_data[3*r_idx+1], self.fetch_data[3*r_idx+2]]))
        dataset = xr.Dataset(
            output_data,
            coords={ "mixer":np.array(["state_val", "I_val", "Q_val"]) , "sequence":['T1', 'X X(T2 echo)', 'Y Y (rotational error)', 'Y -Y (phase error)'], param_name: param_val}
        )

        return dataset