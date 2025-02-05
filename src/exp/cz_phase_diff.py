from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
from qualang_tools.units import unit
import numpy as np
import time
import xarray as xr
import warnings
from exp.QMMeasurement import QMMeasurement
u = unit(coerce_to_integer=True)
warnings.filterwarnings("ignore")

class CZConditionalPhase(QMMeasurement):
    def __init__( self, config, qmm: QuantumMachinesManager ):
        super().__init__( config, qmm )
        self.ro_element=["q0_ro","q1_ro","q2_ro","q3_ro", "q4_ro"]
        self.flux_Qi = 3
        self.control_Qi = 2
        self.target_Qi = 3
        self.flux_Ci = 7 # coupler
        self.preprocess = "shot"
        self.initializer = None

        self.cz_amps_range = (-0.4, 0.0)#(-0.325,-0.275)
        self.cz_amps_resolution = 0.02
        self.couplerz_amps_range = (0.2, 0.4)#(-0.22, -0.12)
        self.couplerz_amps_resolution = 0.01
        self.cz_time = 60#160 # ns
    
    def _get_qua_program( self ):
        self.cz_amps_array = np.arange(self.cz_amps_range[0],self.cz_amps_range[1],self.cz_amps_resolution)
        self.couplerz_amps_array = np.arange(self.couplerz_amps_range[0],self.couplerz_amps_range[1],self.couplerz_amps_resolution)
        amps_len = len(self.cz_amps_array)
        camps_len = len(self.couplerz_amps_array)
        self.qua_targetz_time = self.cz_time//4 #+ 10
        self.qua_cz_time = self.cz_time//4

        with program() as cz_conphase:
            iqdata_stream = multiRO_declare( self.ro_element )
            n = declare(int)
            n_st = declare_stream()
            cz_amps = declare(fixed)
            couplerz_amps = declare(fixed)
            control = declare(int) # control qubit at 0 or 1
            rotate = declare(int)  # second gate is x90 or y90 
            with for_(n, 0, n < self.shot_num, n + 1):
                with for_(*from_array(couplerz_amps, self.couplerz_amps_array)):
                    with for_(*from_array(cz_amps, self.cz_amps_array)):
                        with for_each_( control, [0,1]):

                            with for_each_(rotate, [0,1, 2]):

                                # initializaion
                                if self.initializer is None:
                                    wait(1*u.us,self.ro_element)
                                else:
                                    try:
                                        self.initializer[0](*self.initializer[1])
                                    except:
                                        wait(1*u.us,self.ro_element)

                                # operation
                                with if_(control==1):
                                    play("x180",f"q{self.control_Qi}_xy")

                                play("x90", f"q{self.target_Qi}_xy")

                                align(f"q{self.target_Qi}_xy",f"q{self.flux_Qi}_z",f'q{self.flux_Ci}_z')
                                wait(20 *u.ns)

                                self.cz_gate(cz_amps,couplerz_amps)

                                align(f"q{self.flux_Qi}_z",f"q{self.target_Qi}_xy")
                                wait(20*u.ns)

                                with if_(rotate==1):
                                    play("-y90", f"q{self.target_Qi}_xy")
                                with elif_(rotate == 0):
                                    play("x90", f"q{self.target_Qi}_xy")
                                align()
                                # wait(cz_time*u.ns)
                                


                                # Readout
                                #play( "const"*amp( -0.2 ), "q7_z", duration=100)
                                multiRO_measurement(iqdata_stream, self.ro_element, weights="rotated_")
                save(n, n_st)

            with stream_processing():
                n_st.save("iteration")
                match self.preprocess:
                    case "shot":

                        multiRO_pre_save(iqdata_stream, self.ro_element, (self.shot_num,camps_len,amps_len,2,3) ,stream_preprocess="shot")
                    case _:
                        multiRO_pre_save(iqdata_stream, self.ro_element, (camps_len,amps_len,2,3))
        return cz_conphase
    
    def _get_fetch_data_list( self ):
        ro_ch_name = []
        for r_name in self.ro_element:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")

        data_list = ro_ch_name + ["iteration"]   
        return data_list
    
    def _data_formation( self ):
        output_data = {}

        match self.preprocess:
            case "shot":
                for r_idx, r_name in enumerate(self.ro_element):
                    output_data[r_name] = ( ["mixer","shot","c_amp","cz_amp","control","rotate"],
                                np.squeeze(np.array([self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]]) ))
                dataset = xr.Dataset(
                    output_data,

                    coords={ "mixer":np.array(["I","Q"]), "shot":np.arange(self.shot_num),"c_amp":self.couplerz_amps_array,
                             "cz_amp": self.cz_amps_array, "control":[0,1], "rotate":[0,1, 2] }

                )
            case _:
                for r_idx, r_name in enumerate(self.ro_element):
                    output_data[r_name] = ( ["mixer","c_amp","cz_amp","control","rotate"],
                                np.array([self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]]) )
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]), "c_amp":self.couplerz_amps_array, "cz_amp": self.cz_amps_array,
                             "control":[0,1], "rotate":[0,1, 2] }

                )

        return dataset
    
    def cz_gate(self,cz_amp,c_amp):
        play("const" * amp(cz_amp),f"q{self.flux_Qi}_z", duration=self.qua_targetz_time)
        #wait(20 *u.ns,f"q{self.flux_Ci}_z")
        play("const" * amp(c_amp),f"q{self.flux_Ci}_z",duration=self.qua_cz_time)

class CZCompensate(QMMeasurement):
    def __init__( self, config, qmm: QuantumMachinesManager ):
        super().__init__( config, qmm )
        self.ro_element=["q0_ro","q1_ro","q2_ro","q3_ro", "q4_ro"]
        self.flux_Qi = 3
        self.control_Qi = 2
        self.target_Qi = 3
        self.flux_Ci = 7 # coupler
        self.preprocess = "ave"
        self.initializer = None

        self.cz_amps = -0.13
        self.c_amps = 0.35
        self.cz_time = 60#160 # ns
        self.phase_resolution = 0.1
    
    def _get_qua_program( self ):
        self.qua_targetz_time = self.cz_time//4 #+ 10
        self.qua_cz_time = self.cz_time//4
        self.phase_array = np.arange(0,1,self.phase_resolution)
        match self.preprocess:
            case "ave":
                with program() as cz_phase:
                    iqdata_stream = multiRO_declare( self.ro_element )
                    n = declare(int)
                    n_st = declare_stream()
                    rotate = declare(int)
                    phase = declare(fixed)
                    with for_(n, 0, n < self.shot_num, n + 1):
                        with for_each_(rotate, [0,1]):
                            with for_(*from_array(phase, self.phase_array)):
                                # initializaion
                                if self.initializer is None:
                                    wait(1*u.us,self.ro_element)
                                else:
                                    try:
                                        self.initializer[0](*self.initializer[1])
                                    except:
                                        wait(1*u.us,self.ro_element)
                                
                                # operation
                                play("y90", f"q{self.target_Qi}_xy")
                                align(f"q{self.target_Qi}_xy",f"q{self.flux_Qi}_z",f"q{self.flux_Ci}_z")
                                wait(20 *u.ns)

                                self.cz_gate(self.cz_amps,self.c_amps)

                                align(f"q{self.flux_Qi}_z",f"q{self.target_Qi}_xy")
                                wait(20*u.ns)
                                frame_rotation_2pi(phase,f"q{self.target_Qi}_xy")

                                with if_(rotate==1):
                                    play("-y90", f"q{self.target_Qi}_xy")
                                with else_():
                                    play("x90", f"q{self.target_Qi}_xy")
                                align()

                                # Readout
                                #play( "const"*amp( -0.2 ), "q7_z", duration=100)
                                multiRO_measurement(iqdata_stream, self.ro_element, weights="rotated_")
                        save(n, n_st)

                    with stream_processing():
                        n_st.save("iteration")
                        multiRO_pre_save(iqdata_stream, self.ro_element, (2,len(self.phase_array)))
                return cz_phase

            case "shot":
                with program() as cz_phase:
                    iqdata_stream = multiRO_declare( self.ro_element )
                    n = declare(int)
                    n_st = declare_stream()
                    rotate = declare(int)  # second gate is x90 or y90 
                    with for_(n, 0, n < self.shot_num, n + 1):
                        with for_each_(rotate, [0,1]):
                            # initializaion
                            if self.initializer is None:
                                wait(1*u.us,self.ro_element)
                            else:
                                try:
                                    self.initializer[0](*self.initializer[1])
                                except:
                                    wait(1*u.us,self.ro_element)

                            # operation
                            play("y90", f"q{self.target_Qi}_xy")
                            align(f"q{self.target_Qi}_xy",f"q{self.flux_Qi}_z",f"q{self.flux_Ci}_z")
                            wait(20 *u.ns)

                            self.cz_gate(self.cz_amps,self.c_amps)

                            align(f"q{self.flux_Qi}_z",f"q{self.target_Qi}_xy")
                            wait(20*u.ns)
                            with if_(rotate==1):
                                play("-y90", f"q{self.target_Qi}_xy")
                            with else_():
                                play("x90", f"q{self.target_Qi}_xy")
                            #wait(cz_time*u.ns)
                            #wait(100*u.ns)
                            align()

                            # Readout
                            play( "const"*amp( -0.2 ), "q7_z", duration=100)
                            multiRO_measurement(iqdata_stream, self.ro_element, weights="rotated_")
                        save(n, n_st)

                    with stream_processing():
                        n_st.save("iteration")
                        multiRO_pre_save(iqdata_stream, self.ro_element, (self.shot_num,2) ,stream_preprocess="shot")
                return cz_phase
    
    def _get_fetch_data_list( self ):
        ro_ch_name = []
        for r_name in self.ro_element:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")

        data_list = ro_ch_name + ["iteration"]   
        return data_list
    
    def _data_formation( self ):
        output_data = {}

        match self.preprocess:
            case "shot":
                for r_idx, r_name in enumerate(self.ro_element):
                    output_data[r_name] = ( ["mixer","shot","rotate"],
                                np.squeeze(np.array([self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]]) ))
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]), "shot":np.arange(self.shot_num), "rotate":[0,1] }
                )
            case _:
                for r_idx, r_name in enumerate(self.ro_element):
                    output_data[r_name] = ( ["mixer","rotate","phase"],
                                np.array([self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]]) )
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]),"rotate":[0,1], "phase":self.phase_array}
                )

        return dataset
    
    def cz_gate(self,cz_amp,c_amp):
        play("const" * amp(cz_amp),f"q{self.flux_Qi}_z", duration=self.qua_targetz_time)
        #wait(20 *u.ns,f"q{self.flux_Ci}_z")
        play("const" * amp(c_amp),f"q{self.flux_Ci}_z",duration=self.qua_cz_time)

class CZFidelity(QMMeasurement):
    def __init__( self, config, qmm: QuantumMachinesManager ):
        super().__init__( config, qmm )
        self.ro_element=["q0_ro","q1_ro","q2_ro","q3_ro", "q4_ro"]
        self.flux_Qi = 3
        self.control_Qi = 2
        self.target_Qi = 3
        self.flux_Ci = 7 # coupler
        self.preprocess = "shot"
        self.initializer = None

        self.cz_amps = -0.13
        self.c_amps = 0.35
        self.cz_time = 60#160 # ns

    def _get_qua_program( self ):
        self.qua_targetz_time = self.cz_time//4 #+ 10
        self.qua_cz_time = self.cz_time//4
        with program() as cz_fidelity:
            iqdata_stream = multiRO_declare( self.ro_element )
            n = declare(int)
            n_st = declare_stream()
            flag = declare(int)  # second gate is x90 or y90 
            with for_(n, 0, n < self.shot_num, n + 1):
                with for_each_(flag, [0,1]):
                    # initializaion
                    if self.initializer is None:
                        wait(1*u.us,self.ro_element)
                    else:
                        try:
                            self.initializer[0](*self.initializer[1])
                        except:
                            wait(1*u.us,self.ro_element)

                    # operation
                    play("x180", f"q{self.control_Qi}_xy")
                    play("x180", f"q{self.target_Qi}_xy")
                    align()
                    wait(5)

                    with if_(flag == 1):
                        self.cz_gate(self.cz_amps,self.c_amps)
                        align()

                    # Readout
                    #play( "const"*amp( -0.2 ), "q7_z", duration=100)
                    multiRO_measurement(iqdata_stream, self.ro_element, weights="rotated_")
                save(n, n_st)

            with stream_processing():
                n_st.save("iteration")
                match self.preprocess:
                    case "shot":
                        multiRO_pre_save(iqdata_stream, self.ro_element, (self.shot_num,2) ,stream_preprocess="shot")
                    case _:
                        multiRO_pre_save(iqdata_stream, self.ro_element, (2,))
        return cz_fidelity
    
    def _get_fetch_data_list( self ):
        ro_ch_name = []
        for r_name in self.ro_element:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")

        data_list = ro_ch_name + ["iteration"]   
        return data_list
    
    def _data_formation( self ):
        output_data = {}

        match self.preprocess:
            case "shot":
                for r_idx, r_name in enumerate(self.ro_element):
                    output_data[r_name] = ( ["mixer","shot","flag"],
                                np.squeeze(np.array([self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]]) ))
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]), "shot":np.arange(self.shot_num), "flag":[0,1] }
                )
            case _:
                for r_idx, r_name in enumerate(self.ro_element):
                    output_data[r_name] = ( ["mixer","flag"],
                                np.array([self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]]) )
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]),"flag":[0,1] }
                )

        return dataset
    
    def cz_gate(self,cz_amp,c_amp):
        play("const" * amp(cz_amp),f"q{self.flux_Qi}_z", duration=self.qua_targetz_time)
        #wait(20 *u.ns,f"q{self.flux_Ci}_z")
        play("const" * amp(c_amp),f"q{self.flux_Ci}_z",duration=self.qua_cz_time)

class CZConditionalPhasediff(QMMeasurement):
    def __init__( self, config, qmm: QuantumMachinesManager ):
        super().__init__( config, qmm )  
        self.ro_element=["q0_ro","q1_ro","q2_ro","q3_ro", "q4_ro"]
        self.flux_Qi = 3
        self.control_Qi = 2
        self.target_Qi = 3
        self.flux_Ci = 7 # coupler
        self.preprocess = "ave"
        self.initializer = None

        self.cz_amps = -0.13
        self.c_amps = 0.35
        self.cz_time = 60#160 # ns 
        self.phase_resolution = 0.1
    
    def _get_qua_program( self ):
        self.qua_targetz_time = self.cz_time//4 #+ 10
        self.qua_cz_time = self.cz_time//4
        self.phase_array = np.arange(0,2,self.phase_resolution)
        with program() as cz_fidelity:
            iqdata_stream = multiRO_declare( self.ro_element )
            n = declare(int)
            n_st = declare_stream()
            control = declare(int)  # second gate is x90 or y90 
            phase = declare(fixed)
            with for_(n, 0, n < self.shot_num, n + 1):
                with for_each_(control, [0,1]):
                    with for_(*from_array(phase, self.phase_array)):
                        # initializaion
                        if self.initializer is None:
                            wait(1*u.us,self.ro_element)
                        else:
                            try:
                                self.initializer[0](*self.initializer[1])
                            except:
                                wait(1*u.us,self.ro_element)

                        # operation
                        with if_(control==1):
                            play("x180",f"q{self.control_Qi}_xy")
                        play("x90", f"q{self.target_Qi}_xy")
                        align()
                        wait(5)

                        self.cz_gate(self.cz_amps,self.c_amps)
                        align()
                        wait(5)
                            
                        frame_rotation_2pi(phase,f"q{self.target_Qi}_xy")
                        play("x90", f"q{self.target_Qi}_xy")
                        align()
                        #wait(5)

                        # Readout
                        #play( "const"*amp( -0.2 ), "q7_z", duration=100)
                        multiRO_measurement(iqdata_stream, self.ro_element, weights="rotated_")
                save(n, n_st)

            with stream_processing():
                n_st.save("iteration")
                match self.preprocess:
                    case "shot":
                        multiRO_pre_save(iqdata_stream, self.ro_element, (self.shot_num,2,len(self.phase_array)) ,stream_preprocess="shot")
                    case _:
                        multiRO_pre_save(iqdata_stream, self.ro_element, (2,len(self.phase_array)))
        return cz_fidelity
    
    def _get_fetch_data_list( self ):
        ro_ch_name = []
        for r_name in self.ro_element:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")

        data_list = ro_ch_name + ["iteration"]   
        return data_list
    
    def _data_formation( self ):
        output_data = {}

        match self.preprocess:
            case "shot":
                for r_idx, r_name in enumerate(self.ro_element):
                    output_data[r_name] = ( ["mixer","shot","control","phase"],
                                np.squeeze(np.array([self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]]) ))
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]), "shot":np.arange(self.shot_num), "control":[0,1], "phase":self.phase_array}
                )
            case _:
                for r_idx, r_name in enumerate(self.ro_element):
                    output_data[r_name] = ( ["mixer","control","phase"],
                                np.array([self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]]) )
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]),"control":[0,1], "phase":self.phase_array }
                )

        return dataset
    
    def cz_gate(self,cz_amp,c_amp):
        play("const" * amp(cz_amp),f"q{self.flux_Qi}_z", duration=self.qua_targetz_time)
        #wait(20 *u.ns,f"q{self.flux_Ci}_z")
        play("const" * amp(c_amp),f"q{self.flux_Ci}_z",duration=self.qua_cz_time)
 
def cz_gate(flux_Qi, flux_Ci,cz_amp,cz_time,c_amp):
    play("const" * amp(cz_amp),f"q{flux_Qi}_z", duration=cz_time/4+10)
    play("const" * amp(c_amp),f"q{flux_Ci}_z",duration=cz_time/4)

def cz_gate_compensate(flux_Qi, flux_Ci,cz_amp,cz_time,c_amp,control_Qi,target_Qi):
    play("const" * amp(cz_amp),f"q{flux_Qi}_z", duration=cz_time/4)
    play("const" * amp(c_amp),f"q{flux_Ci}_z",duration=cz_time/4)
    #frame_rotation_2pi(1.958/(2*np.pi), f"q{control_Qi}_xy")
    frame_rotation_2pi(-0.051673306854385946/(2*np.pi), f"q{target_Qi}_xy")

def CZ_phase_ramsey(cz_amps_range,cz_amps_resolution,cz_time,couplerz_amps_range,couplerz_amps_resolution,ro_element,flux_Qi,control_Qi,target_Qi,flux_Ci,preprocess,qmm,config,n_avg=1,initializer=None,simulate=True):
    cz_amps_array = np.arange(cz_amps_range[0],cz_amps_range[1],cz_amps_resolution)
    couplerz_amps_array = np.arange(couplerz_amps_range[0],couplerz_amps_range[1],couplerz_amps_resolution)
    phase_array = np.linspace(0, 1, 50)
    amps_len = len(cz_amps_array)
    camps_len = len(couplerz_amps_array)
    phase_array_len = len(phase_array)

    with program() as cz_phase:
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)
        n_st = declare_stream()
        cz_amps = declare(fixed)
        couplerz_amps = declare(fixed)
        control = declare(int) # control qubit at 0 or 1
        phase = declare(fixed)  # second gate is x90 or y90 
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(couplerz_amps, couplerz_amps_array)):
                with for_(*from_array(cz_amps, cz_amps_array)):
                    with for_each_( control, [0,1]):
                        with for_(*from_array(phase, phase_array)):
                            # initializaion
                            if initializer is None:
                                wait(1*u.us,ro_element)
                            else:
                                try:
                                    initializer[0](*initializer[1])
                                except:
                                    wait(1*u.us,ro_element)

                            # operation
                            with if_(control==1):
                                play("x180",f"q{control_Qi}_xy")
                            play("y90", f"q{target_Qi}_xy")
                            align(f"q{target_Qi}_xy",f"q{flux_Qi}_z",f'q{flux_Ci}_z')
                            wait(5)
                            cz_gate(flux_Qi,flux_Ci,cz_amps,cz_time,couplerz_amps)
                            align(f"q{flux_Qi}_z",f"q{target_Qi}_xy")
                            wait(5)
                            
                            frame_rotation_2pi(phase,f"q{target_Qi}_xy")
                            play("-y90", f"q{target_Qi}_xy")
                            align()
                            wait(5)
                                
                            # wait(cz_time*u.ns)
                            

                            # Readout
                            multiRO_measurement(iqdata_stream, ro_element, weights="rotated_")
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            match preprocess:
                case "shot":
                    multiRO_pre_save(iqdata_stream, ro_element, (n_avg,camps_len,amps_len,2,phase_array_len) ,stream_preprocess="shot")
                case _:
                    multiRO_pre_save(iqdata_stream, ro_element, (camps_len,amps_len,2,phase_array_len))
    if simulate:
        simulation_config = SimulationConfig(duration=20000)  # In clock cycles = 4ns
        job = qmm.simulate(config, cz_phase, simulation_config)
        job.get_simulated_samples().con1.plot()
        job.get_simulated_samples().con2.plot()
        plt.show()
    else:
        # Open the quantum machine
        qm = qmm.open_qm(config)
        # Send the QUA program to the OPX, which compiles and executes it
        job = qm.execute(cz_phase)
        # Get results from QUA program
        ro_ch_name = []
        for r_name in ro_element:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")
        data_list = ro_ch_name + ["iteration"]   
        results = fetching_tool(job, data_list=data_list, mode="live")

        # Live plotting
        while results.is_processing():
            # Fetch results
            fetch_data = results.fetch_all()
            # Progress bar
            iteration = fetch_data[-1]
            progress_counter(iteration, n_avg, start_time=results.start_time)
            # Plot
            plt.tight_layout()
            time.sleep(1)

        # Measurement finished 
        fetch_data = results.fetch_all()
        qm.close()
        output_data = {}

        match preprocess:
            case "shot":
                for r_idx, r_name in enumerate(ro_element):
                    output_data[r_name] = ( ["mixer","shot","c_amp","cz_amp","control","phase"],
                                np.squeeze(np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) ))
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]), "shot":np.arange(n_avg),"c_amp":couplerz_amps_array, "cz_amp": cz_amps_array, "control":[0,1], "phase":phase_array }
                )
            case _:
                for r_idx, r_name in enumerate(ro_element):
                    output_data[r_name] = ( ["mixer","c_amp","cz_amp","control","phase"],
                                np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]), "c_amp":couplerz_amps_array, "cz_amp": cz_amps_array, "control":[0,1], "phase":phase_array }
                )

        return dataset



def CZ_phase_diff(cz_amps_range,cz_amps_resolution,cz_time,couplerz_amps_range,couplerz_amps_resolution,ro_element,flux_Qi,control_Qi,target_Qi,flux_Ci,preprocess,qmm,config,n_avg=1,initializer=None,simulate=True):
    cz_amps_array = np.arange(cz_amps_range[0],cz_amps_range[1],cz_amps_resolution)
    couplerz_amps_array = np.arange(couplerz_amps_range[0],couplerz_amps_range[1],couplerz_amps_resolution)
    amps_len = len(cz_amps_array)
    camps_len = len(couplerz_amps_array)

    with program() as cz_phase:
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)
        n_st = declare_stream()
        cz_amps = declare(fixed)
        couplerz_amps = declare(fixed)
        control = declare(int) # control qubit at 0 or 1
        rotate = declare(int)  # second gate is x90 or y90 
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(couplerz_amps, couplerz_amps_array)):
                with for_(*from_array(cz_amps, cz_amps_array)):
                    with for_each_( control, [0,1]):

                        with for_each_(rotate, [0,1, 2]):

                            # initializaion
                            if initializer is None:
                                wait(1*u.us,ro_element)
                            else:
                                try:
                                    initializer[0](*initializer[1])
                                except:
                                    wait(1*u.us,ro_element)

                            # operation
                            with if_(control==1):
                                play("x180",f"q{control_Qi}_xy")

                            play("x90", f"q{target_Qi}_xy")

                            align(f"q{target_Qi}_xy",f"q{flux_Qi}_z",f'q{flux_Ci}_z')
                            wait(20 *u.ns,f"q{flux_Qi}_z")
                            wait(40 *u.ns,f"q{flux_Ci}_z")
                            cz_gate(flux_Qi,flux_Ci,cz_amps,cz_time,couplerz_amps)
                            align(f"q{flux_Qi}_z",f"q{target_Qi}_xy")
                            wait(20*u.ns)
                            with if_(rotate==1):
                                play("-y90", f"q{target_Qi}_xy")
                                #align()
                                #wait(20*u.ns)
                            with elif_(rotate == 0):
                                play("x90", f"q{target_Qi}_xy")
                                #align()
                                #wait(20*u.ns)
                            align()
                            # wait(cz_time*u.ns)
                            


                            # Readout
                            play( "const"*amp( -0.2 ), "q7_z", duration=100)
                            multiRO_measurement(iqdata_stream, ro_element, weights="rotated_")
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            match preprocess:
                case "shot":

                    multiRO_pre_save(iqdata_stream, ro_element, (n_avg,camps_len,amps_len,2,3) ,stream_preprocess="shot")
                case _:
                    multiRO_pre_save(iqdata_stream, ro_element, (camps_len,amps_len,2,3))

    if simulate:
        simulation_config = SimulationConfig(duration=20000)  # In clock cycles = 4ns
        job = qmm.simulate(config, cz_phase, simulation_config)
        job.get_simulated_samples().con1.plot()
        #job.get_simulated_samples().con2.plot()
        plt.show()
    else:
        # Open the quantum machine
        qm = qmm.open_qm(config)
        # Send the QUA program to the OPX, which compiles and executes it
        job = qm.execute(cz_phase)
        # Get results from QUA program
        ro_ch_name = []
        for r_name in ro_element:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")
        data_list = ro_ch_name + ["iteration"]   
        results = fetching_tool(job, data_list=data_list, mode="live")

        # Live plotting
        while results.is_processing():
            # Fetch results
            fetch_data = results.fetch_all()
            # Progress bar
            iteration = fetch_data[-1]
            progress_counter(iteration, n_avg, start_time=results.start_time)
            # Plot
            plt.tight_layout()
            time.sleep(1)

        # Measurement finished 
        fetch_data = results.fetch_all()
        qm.close()
        output_data = {}

        match preprocess:
            case "shot":
                for r_idx, r_name in enumerate(ro_element):
                    output_data[r_name] = ( ["mixer","shot","c_amp","cz_amp","control","rotate"],
                                np.squeeze(np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) ))
                dataset = xr.Dataset(
                    output_data,

                    coords={ "mixer":np.array(["I","Q"]), "shot":np.arange(n_avg),"c_amp":couplerz_amps_array, "cz_amp": cz_amps_array, "control":[0,1], "rotate":[0,1, 2] }

                )
            case _:
                for r_idx, r_name in enumerate(ro_element):
                    output_data[r_name] = ( ["mixer","c_amp","cz_amp","control","rotate"],
                                np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]), "c_amp":couplerz_amps_array, "cz_amp": cz_amps_array, "control":[0,1], "rotate":[0,1, 2] }

                )

        return dataset
    
def CZ_phase_diff_1D(cz_amps,cz_time,ro_element,flux_Qi,control_Qi,target_Qi,flux_Ci,preprocess,qmm,config,n_avg=1,initializer=None,simulate=True):

    with program() as cz_phase:
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)
        n_st = declare_stream()
        control = declare(int) # control qubit at 0 or 1
        rotate = declare(int)  # second gate is x90 or y90 
        with for_(n, 0, n < n_avg, n + 1):
            with for_each_( control, [0,1]):
                with for_each_(rotate, [0,1]):
                    # initializaion
                    if initializer is None:
                        wait(1*u.us,ro_element)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            wait(1*u.us,ro_element)

                    # operation
                    with if_(control==1):
                        play("x180",f"q{control_Qi}_xy")
                    play("x90", f"q{target_Qi}_xy")
                    align(f"q{target_Qi}_xy",f"q{flux_Qi}_z",f'q{flux_Ci}_z')
                    wait(20*u.ns)
                    cz_gate(flux_Qi,flux_Ci,cz_amps,cz_time,0.0)
                    align(f"q{flux_Qi}_z",f"q{target_Qi}_xy")
                    wait(20*u.ns)
                    with if_(rotate==1):
                        play("-y90", f"q{target_Qi}_xy")
                    with else_():
                        play("x90", f"q{target_Qi}_xy")
                    wait(cz_time*u.ns)
                    wait(100*u.ns)

                    # Readout
                    play( "const"*amp( -0.2 ), "q6_z", duration=200)
                    multiRO_measurement(iqdata_stream, ro_element, weights="rotated_")
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            match preprocess:
                case "shot":
                    multiRO_pre_save(iqdata_stream, ro_element, (n_avg,2,2) ,stream_preprocess="shot")
                case _:
                    multiRO_pre_save(iqdata_stream, ro_element, (2,2))
    if simulate:
        simulation_config = SimulationConfig(duration=20000)  # In clock cycles = 4ns
        job = qmm.simulate(config, cz_phase, simulation_config)
        job.get_simulated_samples().con1.plot()
        job.get_simulated_samples().con2.plot()
        plt.show()
    else:
        # Open the quantum machine
        qm = qmm.open_qm(config)
        # Send the QUA program to the OPX, which compiles and executes it
        job = qm.execute(cz_phase)
        # Get results from QUA program
        ro_ch_name = []
        for r_name in ro_element:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")
        data_list = ro_ch_name + ["iteration"]   
        results = fetching_tool(job, data_list=data_list, mode="live")

        # Live plotting
        while results.is_processing():
            # Fetch results
            fetch_data = results.fetch_all()
            # Progress bar
            iteration = fetch_data[-1]
            progress_counter(iteration, n_avg, start_time=results.start_time)
            # Plot
            plt.tight_layout()
            time.sleep(1)

        # Measurement finished 
        fetch_data = results.fetch_all()
        qm.close()
        output_data = {}

        match preprocess:
            case "shot":
                for r_idx, r_name in enumerate(ro_element):
                    output_data[r_name] = ( ["mixer","shot","control","rotate"],
                                np.squeeze(np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) ))
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]), "shot":np.arange(n_avg), "control":[0,1], "rotate":[0,1] }
                )
            case _:
                for r_idx, r_name in enumerate(ro_element):
                    output_data[r_name] = ( ["mixer","control","rotate"],
                                np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]), "control":[0,1], "rotate":[0,1] }
                )
        return dataset

def CZ_phase_diff_time(cz_amps_range,cz_amps_resolution,cz_time_max,cz_time_resolution,c_amps,ro_element,flux_Qi,control_Qi,target_Qi,flux_Ci,qmm,config,n_avg=1,initializer=None,simulate=True):
    cz_amps_array = np.arange(cz_amps_range[0],cz_amps_range[1],cz_amps_resolution)
    cc_resolution = (cz_time_resolution/4.)*u.ns
    cc_max_qua = (cz_time_max/4.)*u.ns
    cc_qua = np.arange( 4, cc_max_qua, cc_resolution)
    print(cc_qua)
    cz_time_array = cc_qua*4

    amps_len = len(cz_amps_array)
    time_len = len(cz_time_array)

    with program() as cz_phase:
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)
        n_st = declare_stream()
        cz_amps = declare(fixed)
        cc = declare(int)
        control = declare(int) # control qubit at 0 or 1
        rotate = declare(int)  # second gate is x90 or y90 
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(cz_amps, cz_amps_array)):
                with for_(*from_array(cc, cc_qua)):
                    with for_each_( control, [0,1]):
                        with for_each_(rotate, [0,1]):
                            # initializaion
                            if initializer is None:
                                wait(1*u.us,ro_element)
                            else:
                                try:
                                    initializer[0](*initializer[1])
                                except:
                                    wait(1*u.us,ro_element)

                            # operation
                            with if_(control==1):
                                play("x180",f"q{control_Qi}_xy")
                            play("x90", f"q{target_Qi}_xy")
                            align(f"q{target_Qi}_xy",f"q{flux_Qi}_z",f'q{flux_Ci}_z')
                            wait(40*u.ns)
                            cz_gate(flux_Qi,flux_Ci,cz_amps,cc*4,c_amps)
                            #cz_gate_compensate(flux_Qi, flux_Ci,cz_amps,cc*4,c_amps,control_Qi,target_Qi)
                            with if_(rotate==1):
                                frame_rotation_2pi(0.25, f"q{target_Qi}_xy")
                            align(f"q{flux_Qi}_z",f"q{target_Qi}_xy")
                            wait(20 *u.ns)
                            play("x90", f"q{target_Qi}_xy")
                            wait(cc)
                            wait(140*u.ns)

                            # Readout
                            multiRO_measurement(iqdata_stream, ro_element, weights="rotated_")
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            multiRO_pre_save(iqdata_stream, ro_element, (amps_len,time_len,2,2) )
    if simulate:
        simulation_config = SimulationConfig(duration=20000)  # In clock cycles = 4ns
        job = qmm.simulate(config, cz_phase, simulation_config)
        job.get_simulated_samples().con1.plot()
        job.get_simulated_samples().con2.plot()
        plt.show()
    else:
        # Open the quantum machine
        qm = qmm.open_qm(config)
        # Send the QUA program to the OPX, which compiles and executes it
        job = qm.execute(cz_phase)
        # Get results from QUA program
        ro_ch_name = []
        for r_name in ro_element:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")
        data_list = ro_ch_name + ["iteration"]   
        results = fetching_tool(job, data_list=data_list, mode="live")

        # Live plotting
        while results.is_processing():
            # Fetch results
            fetch_data = results.fetch_all()
            # Progress bar
            iteration = fetch_data[-1]
            progress_counter(iteration, n_avg, start_time=results.start_time)
            # Plot
            plt.tight_layout()
            time.sleep(1)

        # Measurement finished 
        fetch_data = results.fetch_all()
        qm.close()
        output_data = {}

        for r_idx, r_name in enumerate(ro_element):
            output_data[r_name] = ( ["mixer","cz_amp","cz_time","control","rotate"],
                                np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
        dataset = xr.Dataset(
            output_data,
            coords={ "mixer":np.array(["I","Q"]),"cz_amp":cz_amps_array,"cz_time":cz_time_array,"control":np.array([0,1]), "rotate": np.array([0,1])}
        )

        return dataset

def CZ_phase_compensate(c_amp,cz_amp,cz_time,ro_element,flux_Qi,target_Qi,flux_Ci,preprocess,qmm,config,n_avg=1,initializer=None,simulate=True):
    with program() as cz_phase:
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)
        n_st = declare_stream()
        rotate = declare(int)  # second gate is x90 or y90 
        with for_(n, 0, n < n_avg, n + 1):
            with for_each_(rotate, [0,1]):
                # initializaion
                if initializer is None:
                    wait(1*u.us,ro_element)
                else:
                    try:
                        initializer[0](*initializer[1])
                    except:
                        wait(1*u.us,ro_element)

                # operation
                play("x90", f"q{target_Qi}_xy")
                align(f"q{target_Qi}_xy",f"q{flux_Qi}_z",f"q{flux_Ci}_z")
                wait(20 *u.ns,f"q{flux_Qi}_z")
                wait(40 *u.ns,f"q{flux_Ci}_z")
                cz_gate(flux_Qi,flux_Ci,cz_amp,cz_time,c_amp)

                align(f"q{flux_Qi}_z",f"q{target_Qi}_xy")
                wait(20*u.ns)
                with if_(rotate==1):
                    play("-y90", f"q{target_Qi}_xy")
                with else_():
                    play("x90", f"q{target_Qi}_xy")
                #wait(cz_time*u.ns)
                #wait(100*u.ns)
                align()

                # Readout
                play( "const"*amp( -0.2 ), "q7_z", duration=100)
                multiRO_measurement(iqdata_stream, ro_element, weights="rotated_")
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            match preprocess:
                case "shot":
                    multiRO_pre_save(iqdata_stream, ro_element, (n_avg,2) ,stream_preprocess="shot")
                case _:
                    multiRO_pre_save(iqdata_stream, ro_element, (2,))
    if simulate:
        simulation_config = SimulationConfig(duration=20_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, cz_phase, simulation_config)
        job.get_simulated_samples().con1.plot()
        # job.get_simulated_samples().con2.plot()
        plt.show()
    else:
        # Open the quantum machine
        qm = qmm.open_qm(config)
        # Send the QUA program to the OPX, which compiles and executes it
        job = qm.execute(cz_phase)
        # Get results from QUA program
        ro_ch_name = []
        for r_name in ro_element:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")
        data_list = ro_ch_name + ["iteration"]   
        results = fetching_tool(job, data_list=data_list, mode="live")

        # Live plotting
        while results.is_processing():
            # Fetch results
            fetch_data = results.fetch_all()
            # Progress bar
            iteration = fetch_data[-1]
            progress_counter(iteration, n_avg, start_time=results.start_time)
            # Plot
            plt.tight_layout()
            time.sleep(1)

        # Measurement finished 
        fetch_data = results.fetch_all()
        qm.close()
        output_data = {}

        match preprocess:
            case "shot":
                for r_idx, r_name in enumerate(ro_element):
                    output_data[r_name] = ( ["mixer","shot","rotate"],
                                np.squeeze(np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) ))
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]), "shot":np.arange(n_avg), "rotate":[0,1] }
                )
            case _:
                for r_idx, r_name in enumerate(ro_element):
                    output_data[r_name] = ( ["mixer","rotate"],
                                np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]),"rotate":[0,1] }
                )

        return dataset

def CZ_fidelity(control_q_phase, target_q_phase, c_amp,cz_amp,cz_time,ro_element,flux_Qi, control_Qi,target_Qi,flux_Ci,preprocess,qmm,config,n_avg=1,initializer=None,simulate=True):
    with program() as cz_phase:
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)
        n_st = declare_stream()
        rotate = declare(int)  # second gate is x90 or y90 
        with for_(n, 0, n < n_avg, n + 1):
            # initializaion
            if initializer is None:
                wait(1*u.us,ro_element)
            else:
                try:
                    initializer[0](*initializer[1])
                except:
                    wait(1*u.us,ro_element)

            # operation
            play("x180", f"q{target_Qi}_xy")
            play("x180", f"q{control_Qi}_xy")

            play("y90", f"q{target_Qi}_xy")
            play("y90", f"q{control_Qi}_xy")
            align()
            wait(5)     

            # wait(25)
            play("const" * amp(cz_amp),f"q{flux_Qi}_z")
            play("const" * amp(c_amp),f"q{flux_Ci}_z")
            align()
            frame_rotation_2pi(control_q_phase/(2*np.pi), f"q{control_Qi}_xy")
            frame_rotation_2pi(target_q_phase/(2*np.pi), f"q{target_Qi}_xy")

            align()
            wait(5)
            play("x180", f"q{target_Qi}_xy")
            play("y90", f"q{target_Qi}_xy")
            # play("x90", f"q{control_Qi}_xy")
            align()
            # Readout
            multiRO_measurement(iqdata_stream, ro_element, weights="rotated_")
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            match preprocess:
                case "shot":
                    multiRO_pre_save(iqdata_stream, ro_element, (n_avg,) ,stream_preprocess="shot")
                case _:
                    multiRO_pre_save(iqdata_stream, ro_element, ())
    if simulate:
        simulation_config = SimulationConfig(duration=20_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, cz_phase, simulation_config)
        job.get_simulated_samples().con1.plot()
        # job.get_simulated_samples().con2.plot()

        plt.show()
    else:
        # Open the quantum machine
        qm = qmm.open_qm(config)
        # Send the QUA program to the OPX, which compiles and executes it
        job = qm.execute(cz_phase)
        # Get results from QUA program
        ro_ch_name = []
        for r_name in ro_element:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")
        data_list = ro_ch_name + ["iteration"]   
        results = fetching_tool(job, data_list=data_list, mode="live")

        # Live plotting
        while results.is_processing():
            # Fetch results
            fetch_data = results.fetch_all()
            # Progress bar
            iteration = fetch_data[-1]
            progress_counter(iteration, n_avg, start_time=results.start_time)
            # Plot
            plt.tight_layout()
            time.sleep(1)

        # Measurement finished 
        fetch_data = results.fetch_all()
        qm.close()
        output_data = {}

        match preprocess:
            case "shot":
                for r_idx, r_name in enumerate(ro_element):
                    output_data[r_name] = ( ["mixer","shot"],
                                np.squeeze(np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) ))
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]), "shot":np.arange(n_avg) }
                )
            case _:
                for r_idx, r_name in enumerate(ro_element):
                    output_data[r_name] = ( ["mixer"],
                                np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]) }
                )

        return dataset

def shot_analysis(shot_num, data, threshold):
    population_0 = 0
    for i in range(shot_num):
        if data[i] <= threshold:
            population_0 += 1
    population_0 = population_0/shot_num
    return population_0

def shot_analysis_2q(shot_num,data1,data2,threshold1,threshold2):
    pop_00 = 0
    pop_01 = 0
    pop_10 = 0
    pop_11 = 0

    for i in range(shot_num):
        if data1[i] < threshold1 and data2[i] < threshold2:
            pop_00 +=1
        elif data1[i] < threshold1 and data2[i] >= threshold2:
            pop_01 +=1
        elif data1[i] >= threshold1 and data2[i] < threshold2:
            pop_10 +=1
        elif data1[i] >= threshold1 and data2[i] >= threshold2:
            pop_11 +=1
    pop_00 = pop_00/shot_num
    pop_01 = pop_01/shot_num
    pop_10 = pop_10/shot_num
    pop_11 = pop_11/shot_num
    return [pop_00, pop_01,pop_10,pop_11]
        

def plot_cz_phase_diff(dataset,target_Qi,threshold_control, threshold_target):
    """
    x in (N,)
    y in (2,N)
    2 is control qubit at 0 or 1
    N is second x90 gate rotated angle
    """
    cz_amp = dataset.coords["cz_amp"].values
    c_amp = dataset.coords["c_amp"].values
    ro_element = f"q{target_Qi}_ro" # target qubit readout
    shot_num = len(dataset.coords["shot"].values)
    transposed_dataset = dataset.transpose("mixer", "c_amp", "cz_amp","control","rotate","shot")
    data = transposed_dataset[ro_element].values[0]
    print(data.shape)

    population_gy = np.zeros((len(c_amp),len(cz_amp))) # ground state y-basis
    population_gx = np.zeros((len(c_amp),len(cz_amp))) # ground state x-basis
    population_gz = np.zeros((len(c_amp),len(cz_amp))) # ground state z-basis

    population_ey = np.zeros((len(c_amp),len(cz_amp))) # excited state y-basis
    population_ex = np.zeros((len(c_amp),len(cz_amp))) # excited state x-basis
    population_ez = np.zeros((len(c_amp),len(cz_amp))) # excited state z-basis


    phase_map = np.zeros((len(c_amp),len(cz_amp)))
    phase_map_small = np.zeros((len(c_amp),len(cz_amp)))

    e_sqrt_map = np.zeros((len(c_amp),len(cz_amp)))
    e_Sz_map = np.zeros((len(c_amp),len(cz_amp)))
    g_sqrt_map = np.zeros((len(c_amp),len(cz_amp)))
    g_Sz_map = np.zeros((len(c_amp),len(cz_amp)))
    
    a = 0.9
    for i in range(len(c_amp)):
        for j in range(len(cz_amp)):
            population_gy[i,j] = shot_analysis(shot_num, data[i,j,0,0], threshold_target)/a
            population_gx[i,j] = shot_analysis(shot_num, data[i,j,0,1], threshold_target)/a
            population_gz[i,j] = shot_analysis(shot_num, data[i,j,0,2], threshold_target)/a
            population_ey[i,j] = shot_analysis(shot_num, data[i,j,1,0], threshold_target)/a
            population_ex[i,j] = shot_analysis(shot_num, data[i,j,1,1], threshold_target)/a
            population_ez[i,j] = shot_analysis(shot_num, data[i,j,1,2], threshold_target)/a

    for i in range(len(c_amp)):
        for j in range(len(cz_amp)):
            gy = population_gy[i,j] - (1-population_gy[i,j])
            gx = population_gx[i,j] - (1-population_gx[i,j])
            gz = population_gz[i,j] - (1-population_gz[i,j])
            g_phi = np.arctan2(gy,gx)

            ey = population_ey[i,j] - (1-population_ey[i,j])
            ex = population_ex[i,j] - (1-population_ex[i,j])
            ez = population_ez[i,j] - (1-population_ez[i,j])
            e_phi = np.arctan2(ey,ex)

            if abs((abs(e_phi-g_phi)-np.pi))<=0.1*2*np.pi:
                phase_map[i,j] = (abs(e_phi-g_phi)-np.pi)
                phase_map_small[i,j] = (abs(e_phi-g_phi)-np.pi)

            else: 
                phase_map[i,j] = (abs(e_phi-g_phi)-np.pi)
                phase_map_small[i,j] = 0.1*2*np.pi
            g_sqrt_map[i, j] = np.sqrt(gx**2 + gy**2)
            g_Sz_map[i, j] = gz
            e_sqrt_map[i, j] = np.sqrt(ex**2 + ey**2)
            e_Sz_map[i, j] = ez
    
    # 計算所有數據的全域最小和最大值
    z_vmin = min(np.min(e_Sz_map), np.min(g_Sz_map))
    z_vmax = max(np.max(e_Sz_map), np.max(g_Sz_map))

    r_vmin = min(np.min(e_sqrt_map), np.min(g_sqrt_map))
    r_vmax = max(np.max(e_sqrt_map), np.max(g_sqrt_map))


    output_figs = []
    # 第一張圖
    fig1, ax1 = plt.subplots()
    a1 = ax1.pcolormesh(cz_amp, c_amp, phase_map, cmap='RdBu')
    ax1.set_xlabel("q2 z")
    ax1.set_ylabel("coupler z")
    plt.colorbar(a1, ax=ax1, label="phase difference - pi")
    output_figs.append(("phase difference whole map",fig1))

    # 第二張圖
    fig2, ax2 = plt.subplots()
    a2 = ax2.pcolormesh(cz_amp, c_amp, e_sqrt_map, cmap='RdBu', vmin = r_vmin, vmax = r_vmax)  # 替換phase_map或其他資料
    ax2.set_xlabel("q2 z")
    ax2.set_ylabel("coupler z")
    plt.colorbar(a2, ax=ax2, label="e_sqrt(Sx\^2+Sy\^2)")
    output_figs.append(("e_Sxy",fig2))

    # 第三張圖
    fig3, ax3 = plt.subplots()
    a3 = ax3.pcolormesh(cz_amp, c_amp, e_Sz_map, cmap='RdBu', vmin = z_vmin, vmax = z_vmax)  # 替換phase_map或其他資料
    ax3.set_xlabel("q2 z")
    ax3.set_ylabel("coupler z")
    plt.colorbar(a3, ax=ax3, label="e_Sz")
    output_figs.append(("e_Sz",fig3))

    # 第四張圖
    fig4, ax4 = plt.subplots()
    a4 = ax4.pcolormesh(cz_amp, c_amp, g_sqrt_map, cmap='RdBu', vmin = r_vmin, vmax = r_vmax)  # 替換phase_map或其他資料
    ax4.set_xlabel("q2 z")
    ax4.set_ylabel("coupler z")
    plt.colorbar(a4, ax=ax4, label="g_sqrt(Sx\^2+Sy\^2)")
    output_figs.append(("g_Sxy",fig4))

    # 第五張圖
    fig5, ax5 = plt.subplots()
    a5 = ax5.pcolormesh(cz_amp, c_amp, g_Sz_map, cmap='RdBu', vmin = z_vmin, vmax = z_vmax)  # 替換phase_map或其他資料
    ax5.set_xlabel("q2 z")
    ax5.set_ylabel("coupler z")
    plt.colorbar(a5, ax=ax5, label="g_Sz")
    output_figs.append(("g_Sz",fig5))

    # 第一張圖
    fig6, ax6 = plt.subplots()
    a6 = ax6.pcolormesh(cz_amp, c_amp, phase_map_small, cmap='RdBu')
    ax6.set_xlabel("q2 z")
    ax6.set_ylabel("coupler z")
    plt.colorbar(a6, ax=ax6, label="phase difference - pi")
    output_figs.append(("phase difference part",fig6))

    return output_figs

def cz_phase_compensate_analysis(dataset,preprocess,target_Qi,threshold_target):
    ro_element = f"q{target_Qi}_ro" # target qubit readout
    if preprocess == "shot":
        shot_num = len(dataset.coords["shot"].values)
        transposed_dataset = dataset.transpose("mixer","rotate","shot")
        data = transposed_dataset[ro_element].values[0]
        print(data.shape)

        population_y = shot_analysis(shot_num,data[0],threshold_target)
        population_x = shot_analysis(shot_num,data[1],threshold_target)

        Sy = 2*population_y - 1
        Sx = 2*population_x - 1
        phi = np.arctan2(Sy,Sx)

        print(f"q{target_Qi} need to compensate {phi}")
    else:
        data = dataset[ro_element].values[0]
        phase = dataset.coords["phase"].values
        print(data.shape)
        from scipy import optimize
        
        def cosine_func(x, amplitude, frequency, phase, offset):
            return amplitude * np.cos(2 * np.pi * frequency * x + phase) + offset
        
        popt, pcov = optimize.curve_fit(
            cosine_func,
            phase,
            data[0],
            p0=[6e-5, 1, 0, 1.6e-4],
        )
        fig,ax = plt.subplots()
        ax.plot(phase,data[0],".",label="y raw data")
        ax.plot(phase,cosine_func(phase,*popt),label="y fit result")

        y_project = popt[2]

        popt, pcov = optimize.curve_fit(
            cosine_func,
            phase,
            data[1],
            p0=[6e-5, 1, 0, 1.6e-4],
        )
        ax.plot(phase,data[1],".",label="x raw data")
        ax.plot(phase,cosine_func(phase,*popt),label="x fit result")

        x_project = popt[2]
        phi = np.pi - x_project
        print(f"y projection = {y_project}")
        print(f"x projection = {x_project}")
        print(f"q{target_Qi} need to compensate {phi}")
        ax.legend()


        return fig


def plot_cz_fidelity(dataset, control_Qi, target_Qi, threshold_control, threshold_target):
    ro_control = f"q{control_Qi}_ro" # control qubit readout
    ro_target = f"q{target_Qi}_ro" # control qubit readout
    shot_num = len(dataset.coords["shot"].values)
    transposed_dataset = dataset.transpose("mixer", "flag","shot")
    data_control = transposed_dataset[ro_control].values[0]
    data_target = transposed_dataset[ro_target].values[0]

    statepop_beforecz = shot_analysis_2q(shot_num, data_control[0],data_target[0],threshold_control,threshold_target)
    statepop_aftercz = shot_analysis_2q(shot_num, data_control[1],data_target[1],threshold_control,threshold_target)
    statename = ["00","01","10","11"]

    output_figs = []
    fig1, ax1 = plt.subplots()
    ax1.set_title("state before CZ")
    ax1.bar(statename, statepop_beforecz)
    ax1.set_xlabel("states")
    ax1.set_ylabel("population")
    output_figs.append(("state before cz",fig1))

    fig2, ax2 = plt.subplots()
    ax2.set_title("state after CZ")
    ax2.bar(statename, statepop_aftercz)
    ax2.set_xlabel("states")
    ax2.set_ylabel("population")
    output_figs.append(("state after cz",fig2))

    return output_figs

def plot_conditional_phasediff(dataset,target_Qi):
    ro_element = f"q{target_Qi}_ro"
    data = dataset[ro_element].values[0]
    phase = dataset.coords["phase"].values
    fig,ax = plt.subplots()
    from scipy import optimize
        
    def cosine_func(x, amplitude, frequency, phase, offset):
        return amplitude * np.cos(2 * np.pi * frequency * x + phase) + offset
    
    popt0, pcov0 = optimize.curve_fit(
        cosine_func,
        phase,
        data[0],
        p0=[6e-5, 1, 0, 1.6e-4],
        bounds=([0,0.9,-2*np.pi,0],[1,1.1,2*np.pi,1])
    )
    fig,ax = plt.subplots()
    ax.plot(phase,data[0],".",label="control=0 raw data")
    ax.plot(phase,cosine_func(phase,*popt0),label="control=0 fit result")
    phase_0 = popt0[2]
    #freq_0 = popt[1]
    #x_0 = -phase_0/(2*np.pi*freq_0)
    #ax.axvline(x_0,ls="--")

    popt1, pcov1 = optimize.curve_fit(
        cosine_func,
        phase,
        data[1],
        p0=[6e-5, 1, 0, 1.6e-4],
        bounds=([0,0.9,-np.pi,0],[1,1.1,np.pi,1])
    )
    ax.plot(phase,data[1],".",label="control=1 raw data")
    ax.plot(phase,cosine_func(phase,*popt1), label="control=1 fit result")
    phase_1 = popt1[2]
    print(phase_1,phase_0)
    print(f"phase difference = {phase_1-phase_0}")
    ax.legend()
    return fig