"""
        RAMSEY WITH VIRTUAL Z ROTATIONS
The program consists in playing a Ramsey sequence (x90 - idle_time - x90 - measurement) for different idle times.
Instead of detuning the qubit gates, the frame of the second x90 pulse is rotated (de-phased) to mimic an accumulated
phase acquired for a given detuning after the idle time.
This method has the advantage of playing resonant gates.

From the results, one can fit the Ramsey oscillations and precisely measure the qubit resonance frequency and T2*.

Prerequisites:
    - Having found the resonance frequency of the resonator coupled to the qubit under study (resonator_spectroscopy).
    - Having calibrated qubit pi pulse (x180) by running qubit, spectroscopy, rabi_chevron, power_rabi and updated the config.
    - (optional) Having calibrated the readout (readout_frequency, amplitude, duration_optimization IQ_blobs) for better SNR.
    - Set the desired flux bias.

Next steps before going to the next node:
    - Update the qubit frequency (qubit_IF_q) in the configuration.
"""

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
import sys
import pathlib
QM_script_root = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(QM_script_root)
from configuration_with_octave import *
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.plot import interrupt_on_close
# from macros import qua_declaration, multiplexed_readout
from qualang_tools.plot.fitting import Fit
# from qualang_tools.bakery import baking
import warnings
from RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save

warnings.filterwarnings("ignore")




###################
# The QUA program #
###################


def exp_spin_echo(virtial_detune_freq, q_name:str, ro_element:list, config, qmm:QuantumMachinesManager, n_avg:int=100, simulate = False, echo_number:int=1 ):
    """
    virtial_detune_freq unit in MHz
    """

    point_per_period = 60
    time_period =  (1e3/virtial_detune_freq)*u.ns # ns
    tick_period = time_period//4 # tick per period
    tick_step = time_period//(4*point_per_period) #tick_period//point_per_period

    observe_period = 10/2
    
    max_echo = 5
    evo_time_tick = np.arange( 4, tick_period*observe_period, tick_step)
    evo_time = evo_time_tick*4 *2 

    evo_time_tick_n = evo_time_tick /(2*echo_number)
    tick_len = len(evo_time_tick)
    with program() as echo:
        tick = declare(int)  # QUA variable for the idle time
        phi = declare(fixed)  # Phase to apply the virtual Z-rotation
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)
        n_st = declare_stream()

        with for_(n, 0, n < n_avg, n + 1):

            with for_( *from_array(tick, evo_time_tick) ):
                
                # Initialize
                wait( thermalization_time * u.ns )


                # Operation
                # for e in range(echo_number):
                # echo_number = 0 (Ramsey)
                # play("x90", q_name)   
                # wait( tick )

                # echo_number = 1
                # play("x90", q_name)   
                # wait( tick/2 )
                # play("x180", q_name)   
                # wait( tick/2 )

                # echo_number = 2
                # play("x90", q_name)   
                # wait( tick/4 )
                # play("x180", q_name)   
                # wait( tick/2 )
                # play("x180", q_name)   
                # wait( tick/4 )


                # echo_number = 3
                # play("x90", q_name)   
                # wait( tick/6 )
                # play("x180", q_name)   
                # wait( tick/3 )
                # play("x180", q_name)   
                # wait( tick/3 )
                # play("x180", q_name)   
                # wait( tick/6 )


                # echo_number = 4
                play("x90", q_name)   
                wait( tick/8 )
                play("x180", q_name)   
                wait( tick/4 )
                play("x180", q_name)   
                wait( tick/4 )
                play("x180", q_name)   
                wait( tick/4 )
                play("x180", q_name)   
                wait( tick/8 )



                # echo_number = 5
                # play("x90", q_name)   
                # wait( tick/10 )
                # play("x180", q_name)   
                # wait( tick/5 )
                # play("x180", q_name)   
                # wait( tick/5 )
                # play("x180", q_name)   
                # wait( tick/5 )
                # play("x180", q_name)   
                # wait( tick/5 )
                # play("x180", q_name)   
                # wait( tick/10 )

                assign(phi, Cast.mul_fixed_by_int(virtial_detune_freq * 1e-3, 2*4*tick))
                frame_rotation_2pi(phi, q_name)  # Virtual Z-rotation                
                play("x90", q_name)             


                # Readout
                multiRO_measurement(iqdata_stream, ro_element, weights="rotated_")         

            # Save the averaging iteration to get the progress bar
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            multiRO_pre_save(iqdata_stream, ro_element, (tick_len,) )


    ###########################
    # Run or Simulate Program #
    ###########################

    simulate = False

    if simulate:
        # Simulates the QUA program for the specified duration
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, echo, simulation_config)
        job.get_simulated_samples().con1.plot()

    else:
        # Open the quantum machine
        qm = qmm.open_qm(config)
        # Send the QUA program to the OPX, which compiles and executes it
        job = qm.execute(echo)
        # Get results from QUA program
        ro_ch_name = []
        for r_name in ro_element:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")
        data_list = ro_ch_name + ["iteration"]
           
        results = fetching_tool(job, data_list=data_list, mode="live")
        # Live plotting

        fig, ax = plt.subplots(2, len(ro_element))
        interrupt_on_close(fig, job)  # Interrupts the job when closing the figure
        
        output_data = {}

        while results.is_processing():
            # Fetch results
            fetch_data = results.fetch_all()

            # Plot
            for r_idx, r_name in enumerate(ro_element):
                ax[0][r_idx].cla()
                ax[1][r_idx].cla()
                output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])

                # Plot I
                ax[0][r_idx].set_ylabel("I quadrature [V]")
                plot_echo_live(evo_time, output_data[r_name][0], ax[0][r_idx])
                # Plot Q
                ax[1][r_idx].set_ylabel("Q quadrature [V]")
                plot_echo_live(evo_time, output_data[r_name][1], ax[1][r_idx])
            # Progress bar
            iteration = fetch_data[-1]
            progress_counter(iteration, n_avg, start_time=results.start_time)
            
            plt.pause(1)

        fetch_data = results.fetch_all()
        # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
        qm.close()

        for r_idx, r_name in enumerate(ro_element):
            output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])
        
        output_data["evo_time"] = evo_time
        return output_data


def plot_echo_live( x, y, ax ):
    ax.plot( x, y )

def plot_echo_result( evo_time, y, ax = None,  ):

    if ax == None:
            fig, ax = plt.subplots()
    fit = Fit()
    fig.suptitle("Echo_number = 0 \n average = 1000 " )
    fit.ramsey(evo_time, y, plot=True)
    ax.set_ylabel("signal [V]")
    ax.set_xlabel("Idle times [ns]")
    # ax.title("Qubit 3")
    
def fit_T1( evo_time, signal ):
    fit = Fit()
    decay_fit = fit.T1( evo_time, signal )
    relaxation_time = np.round(np.abs(decay_fit["T1"][0]) / 4) * 4
    fit_func = decay_fit["fit_func"]
    return relaxation_time, fit_func

def statistic_T2_exp( repeat:int, t_delay, q_name, ro_element, config, qmm, n_avg:int=100 ):
    """
    repeat is the measurement times for statistic
    n_avg is the measurement times for getting relaxation time (T1)
    return 2D array with shape ( 2, M )
    axis 0 (2) is I, Q
    axis 1 (M) is repeat 
    """
    statistic_T2 = {}
    raw_data = {}
    for r in ro_element:
        statistic_T2[r] = []
        raw_data[r] = []
    for i in range(repeat):
        print(f"{i}th T1")
        data = exp_spin_echo(t_delay, q_name, ro_element, config, qmm, n_avg)
        for r in ro_element:
            T1_i = fit_T1(t_delay*4, data[r][0])[0]
            print(f"{r} T1 = {T1_i}")
            statistic_T2[r].append( [T1_i, 0])
            raw_data[r].append(data[r])

    for r in ro_element:
        statistic_T2[r] = np.array(statistic_T2[r]).transpose()
        raw_data[r] = np.array(raw_data[r])

    return statistic_T2, raw_data


if __name__ == '__main__':


    n_avg = 1000  # Number of averages
    
    #  Open Communication with the QOP  
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

    ro_element = ["rr3","rr4"]
    q_name = "q4_xy"

    # echo_number = 1

    detuning = 0.5  # "Virtual" detuning in MHz

    output_data = exp_spin_echo( detuning, q_name, ro_element, config, qmm, n_avg=n_avg, simulate=False )  #echo_number=echo_number
    plot_echo_result( output_data["evo_time"], output_data["rr4"][0])  

    #   Data Saving   # 
    save_data = True
    if save_data:
        from save_data import save_npz
        import sys
        # save_dir = r"C:\Users\quant\SynologyDrive\00 Users\Wei\Quantum Machine\DR4 measurement\Data\spin_echo\Q4"  # change save directory
        save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
        save_npz(save_dir, save_progam_name, output_data)  
    
    plt.show()