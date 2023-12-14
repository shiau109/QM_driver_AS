"""
Performs a 1 qubit randomized benchmarking to measure the 1 qubit gate fidelity. This version is using directly the 'I'
& 'Q' data and should be used when there is no single-shot readout
"""
import os, sys
# sys.path.append(os.getcwd()+'/exp')
from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from scipy.optimize import curve_fit
# from configuration import *
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy as np
from qualang_tools.bakery.randomized_benchmark_c1 import c1_table
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import fetching_tool, progress_counter
from qm.simulate import SimulationConfig
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
from matplotlib.figure import Figure

###################
#   Data Saving   #
###################
from datetime import datetime
# save_data = True  # Default = False in configuration file
# save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
# save_time = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
# save_path = f"{save_dir}\{save_time}_{save_progam_name}"

inv_gates = [int(np.where(c1_table[i, :] == 0)[0][0]) for i in range(24)]


def power_law(m, a, b, p):
    return a * (p**m) + b

def generate_sequence(max_circuit_depth,inv_gates,seed=345323):
    cayley = declare(int, value=c1_table.flatten().tolist())
    inv_list = declare(int, value=inv_gates)
    current_state = declare(int)
    step = declare(int)
    sequence = declare(int, size=max_circuit_depth + 1)
    inv_gate = declare(int, size=max_circuit_depth + 1)
    i = declare(int)
    rand = Random(seed=seed)

    assign(current_state, 0)
    with for_(i, 0, i < max_circuit_depth, i + 1):
        assign(step, rand.rand_int(24))
        assign(current_state, cayley[current_state * 24 + step])
        assign(sequence[i], step)
        assign(inv_gate[i], inv_list[current_state])

    return sequence, inv_gate

def play_sequence(qb, sequence_list, depth, pi_len):
    i = declare(int)
    with for_(i, 0, i <= depth, i + 1):
        with switch_(sequence_list[i], unsafe=True):
            with case_(0):
                wait(pi_len // 4, qb)
            with case_(1):
                play("x180", qb)
            with case_(2):
                play("y180", qb)
            with case_(3):
                play("y180", qb)
                play("x180", qb)
            with case_(4):
                play("x90", qb)
                play("y90", qb)
            with case_(5):
                play("x90", qb)
                play("-y90", qb)
            with case_(6):
                play("-x90", qb)
                play("y90", qb)
            with case_(7):
                play("-x90", qb)
                play("-y90", qb)
            with case_(8):
                play("y90", qb)
                play("x90", qb)
            with case_(9):
                play("y90", qb)
                play("-x90", qb)
            with case_(10):
                play("-y90", qb)
                play("x90", qb)
            with case_(11):
                play("-y90", qb)
                play("-x90", qb)
            with case_(12):
                play("x90", qb)
            with case_(13):
                play("-x90", qb)
            with case_(14):
                play("y90", qb)
            with case_(15):
                play("-y90", qb)
            with case_(16):
                play("-x90", qb)
                play("y90", qb)
                play("x90", qb)
            with case_(17):
                play("-x90", qb)
                play("-y90", qb)
                play("x90", qb)
            with case_(18):
                play("x180", qb)
                play("y90", qb)
            with case_(19):
                play("x180", qb)
                play("-y90", qb)
            with case_(20):
                play("y180", qb)
                play("x90", qb)
            with case_(21):
                play("y180", qb)
                play("-x90", qb)
            with case_(22):
                play("x90", qb)
                play("y90", qb)
                play("x90", qb)
            with case_(23):
                play("-x90", qb)
                play("y90", qb)
                play("-x90", qb)

def SQRB_executor(q_name:str,ro_element:list,config:dict,qmm:QuantumMachinesManager,initializer:tuple=None,plot:bool=False,max_circuit_depth:int=700,delta_clifford:int=20,num_of_sequences:int=30,n_avg:int=300,simulate:bool=False):
    gate_step = max_circuit_depth / delta_clifford + 1
    pi_len = config['pulses'][config['elements'][q_name]['operations']["x180"]]["length"]
    with program() as rb:
        depth = declare(int)
        depth_target = declare(int)
        saved_gate = declare(int)
        iqdata_stream = multiRO_declare( ro_element )
        m = declare(int)
        n = declare(int)
        m_st = declare_stream()
        # update_frequency("q2_xy", 0)
        with for_(m, 0, m < num_of_sequences, m + 1):
            sequence_list, inv_gate_list = generate_sequence(max_circuit_depth,inv_gates)
            assign(depth_target, 0)
            with for_(depth, 1, depth <= max_circuit_depth, depth + 1):
                    # Replacing the last gate in the sequence with the sequence's inverse gate
                    # The original gate is saved in 'saved_gate' and is being restored at the end
                assign(saved_gate, sequence_list[depth])
                assign(sequence_list[depth], inv_gate_list[depth - 1])
                with if_((depth == 1) | (depth == depth_target)):
                    with for_(n, 0, n < n_avg, n + 1):
                        if initializer is None:
                            pass # wait(100 * u.us)
                        else:
                            try :
                                initializer[0](*initializer[1])
                            except:
                                print("initializer didn't work!")
                                wait(100 * u.us)

                        align()
                        play_sequence(q_name, sequence_list, depth, pi_len)
                        align()
                        multiRO_measurement(iqdata_stream, ro_element, weights="rotated_")
                    assign(depth_target, depth_target + delta_clifford)   
                assign(sequence_list[depth], saved_gate) 
            save(m, m_st)

        with stream_processing():
            m_st.save("iteration")
            iqdata_stream[1][0].buffer(n_avg).map(FUNCTIONS.average()).buffer(gate_step).buffer(
                num_of_sequences
            ).save("I")
            iqdata_stream[3][0].buffer(n_avg).map(FUNCTIONS.average()).buffer(gate_step).buffer(
                num_of_sequences
            ).save("Q")
            iqdata_stream[1][0].buffer(n_avg).map(FUNCTIONS.average()).buffer(gate_step).average().save(
                "I_avg"
            )
            iqdata_stream[3][0].buffer(n_avg).map(FUNCTIONS.average()).buffer(gate_step).average().save(
                "Q_avg"
            )

    if simulate:
        # Simulates the QUA program for the specified duration
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, rb, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(rb)

        # Get results from QUA program
        results = fetching_tool(job, data_list=["I_avg", "Q_avg", "iteration"], mode="live")
        # Live plotting
        fig = plt.figure()
        interrupt_on_close(fig, job)  # Interrupts the job when closing the figure

        x = np.arange(1, max_circuit_depth + delta_clifford, delta_clifford)

        while results.is_processing():
            # Fetch results
            I, _, iteration = results.fetch_all()
            value_avg = I
            # Progress bar
            progress_counter(iteration, num_of_sequences, start_time=results.get_start_time())
            # Plot results
        results = fetching_tool(job, data_list=["I", "Q"])
        I, _ = results.fetch_all()
        value_avg = np.mean(I, axis=0)
        error_avg = np.std(I, axis=0)
        
        epg = plot_SQRB_result( x, value_avg, error_avg, plot )

        qm.close()

def ana_SQRB( x, y ):
    
    pars, cov = curve_fit(
        f=power_law,
        xdata=x,
        ydata=y,
        p0=[0.5, 0.5, 0.9],
        bounds=(-np.inf, np.inf),
        maxfev=2000,
    )
    stdevs = np.sqrt(np.diag(cov))

    print("#########################")
    print("### Fitted Parameters ###")
    print("#########################")
    print(f"A = {pars[0]:.3} ({stdevs[0]:.1}), B = {pars[1]:.3} ({stdevs[1]:.1}), p = {pars[2]:.3} ({stdevs[2]:.1})")
    print("Covariance Matrix")
    print(cov)

    one_minus_p = 1 - pars[2]
    r_c = one_minus_p * (1 - 1 / 2**1)
    r_g = r_c / 1.875  # 1.875 is the average number of gates in clifford operation
    r_c_std = stdevs[2] * (1 - 1 / 2**1)
    r_g_std = r_c_std / 1.875

    print("#########################")
    print("### Useful Parameters ###")
    print("#########################")
    print(
        f"Error rate: 1-p = {np.format_float_scientific(one_minus_p, precision=2)} ({stdevs[2]:.1})\n"
        f"Clifford set infidelity: r_c = {np.format_float_scientific(r_c, precision=2)} ({r_c_std:.1})\n"
        f"Gate infidelity: r_g = {np.format_float_scientific(r_g, precision=2)}  ({r_g_std:.1})"
    )
    
    return pars, np.format_float_scientific(r_g, precision=2)

def plot_SQRB_live( x, y, ax ):
    ax.plot(x, y, marker=".")
    ax.set_xlabel("Number of Clifford gates")
    ax.set_ylabel("Sequence Fidelity")
    ax.set_title("Single qubit RB")
    

def plot_SQRB_result( x, y, yerr, plot:bool=False ):
    par,epg = ana_SQRB( x, y )
    if plot:
        fig, ax = plt.subplots()
        ax.errorbar(x, y, yerr=yerr, marker=".")
        ax.plot(x, power_law(x, *par), linestyle="--", linewidth=2)
        ax.set_xlabel("Number of Clifford gates")
        ax.set_ylabel("Sequence Fidelity")
        ax.set_title(f"Single qubit RB, gate_error={epg}")
        plt.show()
    return epg







