# import sys, os
# sys.path.append(os.getcwd()+"/exp")
from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
# from exp.configuration import *
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.loops import from_array
import matplotlib.pyplot as plt
import warnings
from ab.QM_config_dynamic import QM_config, Circuit_info

from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save

warnings.filterwarnings("ignore")
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
###################
# The QUA program #
###################


def DRAG_calibration_Yale( drag_coef, q_name:str, ro_element:list, config, qmm:QuantumMachinesManager, n_avg=3000, mode:str='live', initializer:tuple=None):
    """
     "The DRAG coefficient 'drag_coef' must be different from 0 in the config."
    """
    a_min = 0
    a_max = 1.5
    fit_point = 40
    da = (a_max-a_min)/fit_point
    amps = np.arange(a_min, a_max + da, da)  # + da/2 to add a_max to amplitudes
    amp_len = len(amps)
    print("excute DRAG_calibration_Yale")
    with program() as drag:
        n = declare(int)  # QUA variable for the averaging loop
        a = declare(fixed)  # QUA variable for the DRAG coefficient pre-factor
        iqdata_stream = multiRO_declare( ro_element )
        op_idx = declare(int)
        n_st = declare_stream()  # Stream for the averaging iteration 'n'

        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(a, amps)):
                # Play the 1st sequence with varying DRAG coefficient
                with for_each_( op_idx, [0, 1]):                      
                    # Init
                    if initializer is None:
                        wait(100*u.us)
                        #wait(thermalization_time * u.ns)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            print("Initializer didn't work!")
                            wait(100*u.us)


                    # Operation
                    with switch_(op_idx, unsafe=True):
                        with case_(0):
                            # positive
                            play("x180" * amp(1, 0, 0, a), q_name)
                            play("y90" * amp(a, 0, 0, 1), q_name)
                        with case_(1):
                            # nagtive
                            play("y180" * amp(a, 0, 0, 1), q_name)
                            play("x90" * amp(1, 0, 0, a), q_name)

                    # Align the two elements to measure after playing the qubit pulses.
                    align()  # Global align between the two sequences
                    # Measurement
                    multiRO_measurement(iqdata_stream, ro_element, weights="rotated_")

            save(n, n_st)

        with stream_processing():
            # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
            multiRO_pre_save(iqdata_stream, ro_element, (amp_len,2) )
            n_st.save("iteration")

    ###########################
    # Run or Simulate Program #
    ###########################
    simulate = False

    if simulate:
        # Simulates the QUA program for the specified duration
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, drag, simulation_config)
        job.get_simulated_samples().con1.plot()

    else:
        # Open the quantum machine
        qm = qmm.open_qm(config)
        # Send the QUA program to the OPX, which compiles and executes it
        job = qm.execute(drag)
        # Get results from QUA program
        ro_ch_name = []
        for r_name in ro_element:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")
        data_list = ro_ch_name + ["iteration"]   
        results = fetching_tool(job, data_list=data_list, mode="live")
        if mode.lower() == 'live':
            # Live plotting
            fig, ax = plt.subplots(2, len(ro_element))
            interrupt_on_close(fig, job)  # Interrupts the job when closing the figure
            fig.suptitle("DRAG coefficient calibration (Yale)")

            while results.is_processing():
                # Fetch results
                fetch_data = results.fetch_all()
                output_data = {}
                for r_idx, r_name in enumerate(ro_element):
                    ax[r_idx*2].cla()
                    ax[r_idx*2+1].cla()
                    output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])

                    for op_idx, op in enumerate(["x180y90","y180x90"]):
                        ax[r_idx*2].plot(amps * drag_coef, output_data[r_name][0].transpose()[op_idx], label=op)
                        ax[r_idx*2+1].plot(amps * drag_coef, output_data[r_name][1].transpose()[op_idx], label=op)
                    
                output_data['x'] = amps * drag_coef  

                iteration = fetch_data[-1]
                # Progress bar
                progress_counter(iteration, n_avg, start_time=results.get_start_time())      

                plt.legend()
                plt.tight_layout()
                plt.pause(1)
            # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
            qm.close()
            return output_data

        else:
            output_data = {}
            output_data['x'] = amps * drag_coef
            while results.is_processing():
                fetch_data = results.fetch_all()
                for r_idx, r_name in enumerate(ro_element):
                    output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])
                iteration = fetch_data[-1]
                # Progress bar
                progress_counter(iteration, n_avg, start_time=results.get_start_time())
            qm.close()
            return output_data

def amp_calibration( amp_modify_range, q_name:str, ro_element:list, config, qmm:QuantumMachinesManager, sequence_repeat:int=1, n_avg=100,  simulate:bool=True, mode:str='live', initializer:tuple=None):
    '''
        initializer from `QM_config_dynamic.initializer()`
    '''
    a_min = 1-amp_modify_range
    a_max = 1+amp_modify_range
    da = amp_modify_range/20
    n_pi = sequence_repeat *2
    n_90 = sequence_repeat *4
    amps = np.arange(a_min, a_max + da / 2, da)  # + da/2 to add a_max to amplitudes
    amp_len = len(amps)

    with program() as drag:
        n = declare(int)  # QUA variable for the averaging loop
        a = declare(fixed)  # QUA variable for the DRAG coefficient pre-factor
        r_idx = declare(int)  # QUA variable for the measured 'I' quadrature
        iqdata_stream = multiRO_declare( ro_element )
        n_st = declare_stream()  # Stream for the averaging iteration 'n'
        
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(a, amps)):
                with for_each_( r_idx, [0, 1]):                      
                    # Init
                    if initializer is None:
                        # wait(thermalization_time * u.ns)
                        wait(100 * u.us)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            print("Initializer didn't work!")
                            wait(100*u.us)
                   
                    # Operation
                    with switch_(r_idx, unsafe=True):
                        with case_(0):
                            for _ in range(n_90):
                                play("x90" * amp(a), q_name)
                        with case_(1):
                            for _ in range(n_pi):
                                play("x180" * amp(a), q_name)

                    # Align after playing the qubit pulses.
                    align()
                    # Readout
                    multiRO_measurement(iqdata_stream, ro_element, weights="rotated_")         
                
            save(n, n_st)

        with stream_processing():
            # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
            multiRO_pre_save(iqdata_stream, ro_element, (amp_len,2) )
            n_st.save("iteration")

    ###########################
    # Run or Simulate Program #
    ###########################

    if simulate:
        # Simulates the QUA program for the specified duration
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, drag, simulation_config)
        job.get_simulated_samples().con1.plot()

    else:
        # Open the quantum machine
        qm = qmm.open_qm(config)
        # Send the QUA program to the OPX, which compiles and executes it
        job = qm.execute(drag)
        # Get results from QUA program
        ro_ch_name = []
        for r_name in ro_element:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")
        data_list = ro_ch_name + ["iteration"]   
        results = fetching_tool(job, data_list=data_list, mode='live')
        # Live plotting
        if mode == 'live':
            fig, ax = plt.subplots(2, len(ro_element))
            interrupt_on_close(fig, job)  # Interrupts the job when closing the figure

            fig.suptitle("Amp pre factor calibration (AS)")
            while results.is_processing():
                # Fetch results
                fetch_data = results.fetch_all()
                output_data = {}
                for r_idx, r_name in enumerate(ro_element):
                    ax[r_idx*2].cla()
                    ax[r_idx*2+1].cla()
                    output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])

                    for op_idx, op in enumerate(["x90","x180"]):
                        ax[r_idx*2].plot(amps, output_data[r_name][0].transpose()[op_idx], label=op)
                        ax[r_idx*2+1].plot(amps, output_data[r_name][1].transpose()[op_idx], label=op)
                

                iteration = fetch_data[-1]
                # Progress bar
                progress_counter(iteration, n_avg, start_time=results.get_start_time())      

                plt.legend()
                plt.tight_layout()
                plt.pause(1)
        else:
            while results.is_processing():
            # Fetch results
                fetch_data = results.fetch_all()  
                iteration = fetch_data[-1]
                # Progress bar
                progress_counter(iteration, n_avg, start_time=results.get_start_time())      

            output_data = {}
            for r_idx, r_name in enumerate(ro_element):
                    output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])
            output_data['x'] = amps

        # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
        qm.close()
        return output_data
    

def StarkShift_program(q_name:str, ro_element:list, sequence_repeat:int=1, n_avg=100, initializer:tuple=None):
    '''
        initializer from `QM_config_dynamic.initializer()`
    '''
    # a_min = 1-amp_modify_range
    # a_max = 1+amp_modify_range
    # da = amp_modify_range/20
    # amps = np.arange(a_min, a_max + da / 2, da)  # + da/2 to add a_max to amplitudes
    # amp_len = len(amps)

    with program() as drag:
        n = declare(int)  # QUA variable for the averaging loop
        iqdata_stream = multiRO_declare( ro_element )
        n_st = declare_stream()  # Stream for the averaging iteration 'n'
        
        with for_(n, 0, n < n_avg, n + 1):
                        
            # Init
            if initializer is None:
                # wait(thermalization_time * u.ns)
                wait(100 * u.us)
            else:
                try:
                    initializer[0](*initializer[1])
                except:
                    print("Initializer didn't work!")
                    wait(100*u.us)
            
            # Operation
            for _ in range(sequence_repeat):
                play("x180", q_name)
                play("-x180", q_name)

            # Align after playing the qubit pulses.
            align()
            # Readout
            multiRO_measurement(iqdata_stream, ro_element, weights="rotated_")         
        
            save(n, n_st)

        with stream_processing():
            # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
            multiRO_pre_save(iqdata_stream, ro_element, (1,) )
            n_st.save("iteration")

    return drag
    ###########################
    # Run or Simulate Program #
    ###########################

def StarkShift_scout(program, ro_element:list, config:dict, qmm:QuantumMachinesManager, simulate:bool=False):  
    if simulate:
        # Simulates the QUA program for the specified duration
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, program, simulation_config)
        job.get_simulated_samples().con1.plot()

    else:
        # Open the quantum machine
        qm = qmm.open_qm(config)
        # Send the QUA program to the OPX, which compiles and executes it
        job = qm.execute(program)
        # Get results from QUA program
        ro_ch_name = []
        for r_name in ro_element:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")
        data_list = ro_ch_name + ["iteration"]   
        results = fetching_tool(job, data_list=data_list, mode='live')
        
        while results.is_processing():
        # Fetch results
            fetch_data = results.fetch_all()  
            iteration = fetch_data[-1]
            # Progress bar
            # progress_counter(iteration, n_avg, start_time=results.get_start_time())      

        output_data = {}
        for r_idx, r_name in enumerate(ro_element):
                output_data[r_name] = np.array([fetch_data[r_idx]])

        # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
        qm.close()
    return output_data


if __name__ == '__main__':
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
    n_avg = 4000

    # Scan the DRAG coefficient pre-factor

    drag_coef = drag_coef_q2
    # Check that the DRAG coefficient is not 0
    assert drag_coef != 0, "The DRAG coefficient 'drag_coef' must be different from 0 in the config."
    ro_element = ["rr2"]
    q_name =  "q2_xy"
    sequence_repeat = 3
    amp_modify_range = 0.25/float(sequence_repeat)
    output_data = DRAG_calibration_Yale( drag_coef, q_name, ro_element, config, qmm, n_avg=n_avg)
    # output_data =  amp_calibration( amp_modify_range, q_name, ro_element, config, qmm, n_avg=n_avg, sequence_repeat=sequence_repeat, simulate=False)

    #   Data Saving   # 
    save_data = False
    if save_data:
        from save_data import save_npz
        import sys
        save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
        save_npz(save_dir, save_progam_name, output_data)
    
    # # Plot
    plt.show()
