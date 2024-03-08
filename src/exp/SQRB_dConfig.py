"""
        SINGLE QUBIT RANDOMIZED BENCHMARKING (for gates >= 40ns)
The program consists in playing random sequences of Clifford gates and measuring the state of the resonator afterwards.
Each random sequence is derived on the FPGA for the maximum depth (specified as an input) and played for each depth
asked by the user (the sequence is truncated to the desired depth). Each truncated sequence ends with the recovery gate,
found at each step thanks to a preloaded lookup table (Cayley table), that will bring the qubit back to its ground state.

If the readout has been calibrated and is good enough, then state discrimination can be applied to only return the state
of the qubit. Otherwise, the 'I' and 'Q' quadratures are returned.
Each sequence is played n_avg times for averaging. A second averaging is performed by playing different random sequences.

The data is then post-processed to extract the single-qubit gate fidelity and error per gate
.
Prerequisites:
    - Having found the resonance frequency of the resonator coupled to the qubit under study (resonator_spectroscopy).
    - Having calibrated qubit pi pulse (x180) by running qubit, spectroscopy, rabi_chevron, power_rabi and updated the config.
    - Having the qubit frequency perfectly calibrated (ramsey).
    - (optional) Having calibrated the readout (readout_frequency, amplitude, duration_optimization IQ_blobs) for better SNR.
    - Set the desired flux bias.
"""

from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from scipy.optimize import curve_fit

import matplotlib.pyplot as plt
import numpy as np
from qualang_tools.bakery.randomized_benchmark_c1 import c1_table
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.plot import interrupt_on_close
import warnings
from qualang_tools.units import unit

from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save

from matplotlib.figure import Figure

#######################
# AUXILIARY FUNCTIONS #
#######################
u = unit(coerce_to_integer=True)




###################################
# Helper functions and QUA macros #
###################################
def power_law(power, a, b, p):
    return a * (p**power) + b

# List of recovery gates from the lookup table
inv_gates = [int(np.where(c1_table[i, :] == 0)[0][0]) for i in range(24)]
def generate_sequence():
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


def play_sequence(sequence_list, depth, q_name):
    i = declare(int)
    with for_(i, 0, i <= depth, i + 1):
        with switch_(sequence_list[i], unsafe=True):
            with case_(0):
                wait(pi_len // 4, q_name)
            with case_(1):
                play("x180", q_name)
            with case_(2):
                play("y180", q_name)
            with case_(3):
                play("y180", q_name)
                play("x180", q_name)
            with case_(4):
                play("x90", q_name)
                play("y90", q_name)
            with case_(5):
                play("x90", q_name)
                play("-y90", q_name)
            with case_(6):
                play("-x90", q_name)
                play("y90", q_name)
            with case_(7):
                play("-x90", q_name)
                play("-y90", q_name)
            with case_(8):
                play("y90", q_name)
                play("x90", q_name)
            with case_(9):
                play("y90", q_name)
                play("-x90", q_name)
            with case_(10):
                play("-y90", q_name)
                play("x90", q_name)
            with case_(11):
                play("-y90", q_name)
                play("-x90", q_name)
            with case_(12):
                play("x90", q_name)
            with case_(13):
                play("-x90", q_name)
            with case_(14):
                play("y90", q_name)
            with case_(15):
                play("-y90", q_name)
            with case_(16):
                play("-x90", q_name)
                play("y90", q_name)
                play("x90", q_name)
            with case_(17):
                play("-x90", q_name)
                play("-y90", q_name)
                play("x90", q_name)
            with case_(18):
                play("x180", q_name)
                play("y90", q_name)
            with case_(19):
                play("x180", q_name)
                play("-y90", q_name)
            with case_(20):
                play("y180", q_name)
                play("x90", q_name)
            with case_(21):
                play("y180", q_name)
                play("-x90", q_name)
            with case_(22):
                play("x90", q_name)
                play("y90", q_name)
                play("x90", q_name)
            with case_(23):
                play("-x90", q_name)
                play("y90", q_name)
                play("-x90", q_name)

def single_qubit_RB( max_circuit_depth, delta_clifford, q_name:str, ro_element:list, config, qmm:QuantumMachinesManager, sequence_repeat:int=1, n_avg=100, state_discrimination:list=None, initialization_macro=None, simulate:bool=True ):
    
    
    is_discriminated = False
    if state_discrimination is not None:
        is_discriminated = True

    is_const_init = False
    if initialization_macro is not None:
        is_const_init = True  

    gate_step = max_circuit_depth / delta_clifford + 1
    ###################
    # The QUA program #
    ###################
    with program() as rb:
        depth = declare(int)  # QUA variable for the varying depth
        depth_target = declare(int)  # QUA variable for the current depth (changes in steps of delta_clifford)
        # QUA variable to store the last Clifford gate of the current sequence which is replaced by the recovery gate
        saved_gate = declare(int)
        m = declare(int)  # QUA variable for the loop over random sequences
        n = declare(int)  # QUA variable for the averaging loop
        a = declare(fixed)  # QUA variable for the DRAG coefficient pre-factor
        iqdata_stream = multiRO_declare( ro_element )
        n_st = declare_stream()  # Stream for the averaging iteration 'n'
        state = declare(bool)  # QUA variable for state discrimination
        # The relevant streams
        m_st = declare_stream()

  
        if is_discriminated:
            state_st = declare_stream()

        with for_(m, 0, m < num_of_sequences, m + 1):  # QUA for_ loop over the random sequences
            sequence_list, inv_gate_list = generate_sequence()  # Generate the random sequence of length max_circuit_depth

            assign(depth_target, 0)  # Initialize the current depth to 0

            with for_(depth, 1, depth <= max_circuit_depth, depth + 1):  # Loop over the depths
                # Replacing the last gate in the sequence with the sequence's inverse gate
                # The original gate is saved in 'saved_gate' and is being restored at the end
                assign(saved_gate, sequence_list[depth])
                assign(sequence_list[depth], inv_gate_list[depth - 1])
                # Only played the depth corresponding to target_depth
                with if_((depth == 1) | (depth == depth_target)):
                    with for_(n, 0, n < n_avg, n + 1):
                        # Initialize
                        if is_const_init:
                            wait(100 * u.us)
                        else:
                            initialization_macro()
                        align()

                        # Operation
                        # The strict_timing ensures that the sequence will be played without gaps
                        with strict_timing_():
                            # Play the random sequence of desired depth
                            play_sequence(sequence_list, depth, q_name)
                        # Align the two elements to measure after playing the circuit.
                        align()

                        # Make sure you updated the ge_threshold and angle if you want to use state discrimination
                        multiRO_measurement(iqdata_stream, ro_element, weights="rotated_")
                        # Make sure you updated the ge_threshold
                        if is_discriminated:
                            assign(state, iqdata_stream[0][0] > threshold)
                            save(state, state_st)

                    # Go to the next depth
                    assign(depth_target, depth_target + delta_clifford)
                # Reset the last gate of the sequence back to the original Clifford gate
                # (that was replaced by the recovery gate at the beginning)
                assign(sequence_list[depth], saved_gate)
            # Save the counter for the progress bar
            save(m, m_st)

        with stream_processing():
            m_st.save("iteration")
            if is_discriminated:
                # saves a 2D array of depth and random pulse sequences in order to get error bars along the random sequences
                state_st.boolean_to_int().buffer(n_avg).map(FUNCTIONS.average()).buffer(
                    gate_step
                ).buffer(num_of_sequences).save("state")
                # returns a 1D array of averaged random pulse sequences vs depth of circuit for live plotting
                state_st.boolean_to_int().buffer(n_avg).map(FUNCTIONS.average()).buffer(
                    gate_step
                ).average().save("state_avg")
            else:
                # multiRO_pre_save(iqdata_stream, ro_element, (gate_step,2) )
                iqdata_stream[0][0].buffer(n_avg).map(FUNCTIONS.average()).buffer(gate_step).buffer(
                    num_of_sequences
                ).save("I")
                iqdata_stream[0][2].buffer(n_avg).map(FUNCTIONS.average()).buffer(gate_step).buffer(
                    num_of_sequences
                ).save("Q")
                iqdata_stream[0][1].buffer(n_avg).map(FUNCTIONS.average()).buffer(gate_step).average().save(
                    "I_avg"
                )
                iqdata_stream[0][3].buffer(n_avg).map(FUNCTIONS.average()).buffer(gate_step).average().save(
                    "Q_avg"
                )

    ###########################
    # Run or Simulate Program #
    ###########################
    if simulate:
        # Simulates the QUA program for the specified duration
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, rb, simulation_config)
        job.get_simulated_samples().con1.plot()

    else:
        # Open the quantum machine
        qm = qmm.open_qm(config)
        # Send the QUA program to the OPX, which compiles and executes it
        job = qm.execute(rb)
        # Get results from QUA program
        if is_discriminated:
            results = fetching_tool(job, data_list=["state_avg", "iteration"], mode="live")
        else:
            results = fetching_tool(job, data_list=["I_avg", "Q_avg", "iteration"], mode="live")
        # Live plotting
        fig, ax = plt.subplots()
        interrupt_on_close(fig, job)  # Interrupts the job when closing the figure
        # data analysis
        x = np.arange(0, max_circuit_depth + 0.1, delta_clifford)
        x[0] = 1  # to set the first value of 'x' to be depth = 1 as in the experiment
        while results.is_processing():
            # data analysis
            if is_discriminated:
                state_avg, iteration = results.fetch_all()
                value_avg = state_avg
            else:
                I, Q, iteration = results.fetch_all()
                value_avg = I

            # Progress bar
            progress_counter(iteration, num_of_sequences, start_time=results.get_start_time())
            # Plot averaged values
            plot_SQRB_live( x, value_avg, ax )
            plt.cla()
            plt.pause(0.1)


        # At the end of the program, fetch the non-averaged results to get the error-bars
        if is_discriminated:
            results = fetching_tool(job, data_list=["state"])
            state = results.fetch_all()[0]
            value_avg = np.mean(state, axis=0)
            error_avg = np.std(state, axis=0)
        else:
            results = fetching_tool(job, data_list=["I", "Q"])
            I, Q = results.fetch_all()
            value_avg = np.mean(I, axis=0)
            error_avg = np.std(I, axis=0)

        # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
        qm.close()

        return x, value_avg, error_avg


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
    
    return pars

def plot_SQRB_live( x, y, ax ):
    ax.plot(x, y, marker=".")
    ax.xlabel("Number of Clifford gates")
    ax.ylabel("Sequence Fidelity")
    ax.title("Single qubit RB")

def plot_SQRB_result( x, y, yerr, fig:Figure=None ):

    fig, ax = plt.subplots()
    par = ana_SQRB( x, y )
    ax.errorbar(x, y, yerr=yerr, marker=".")
    ax.plot(x, power_law(x, *par), linestyle="--", linewidth=2)
    ax.set_xlabel("Number of Clifford gates")
    ax.set_ylabel("Sequence Fidelity")
    ax.set_title("Single qubit RB")



if __name__ == '__main__':
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
    
    warnings.filterwarnings("ignore")
    from QM_config_dynamic import QM_config, Circuit_info
    dyna_config = QM_config()
    dyna_config.import_config(path=r'.\TEST\BETAsite\QM\OPXPlus\3_5q Tune up\Standard Configuration\Config_1205_Calied')
    the_specs = Circuit_info(q_num=5)
    the_specs.import_spec(path=r'.\TEST\BETAsite\QM\OPXPlus\3_5q Tune up\Standard Configuration\Spec_1205_Calied')
    
    config = dyna_config.get_config()
    pi_len = the_specs.get_spec_forConfig('xy')['q1']['pi_len']
    ##############################
    # Program-specific variables #
    ##############################
    q_name = "q1_xy"
    ro_element = ["rr1","rr2","rr3","rr4"]
    threshold = the_specs.get_spec_forConfig('ro')[q_name]['ge_threshold']


    num_of_sequences = 350  # Number of random sequences
    n_avg = 20  # Number of averaging loops for each random sequence
    max_circuit_depth = 500  # Maximum circuit depth
    delta_clifford = 10  #  Play each sequence with a depth step equals to 'delta_clifford - Must be > 1
    assert (max_circuit_depth / delta_clifford).is_integer(), "max_circuit_depth / delta_clifford must be an integer."
    seed = 345324  # Pseudo-random number generator seed
    # Flag to enable state discrimination if the readout has been calibrated (rotated blobs and threshold)
    state_discrimination = [1e-3]
    x, value_avg, error_avg = single_qubit_RB( max_circuit_depth, delta_clifford, q_name, ro_element, config, qmm )
    
    plot_SQRB_result( x, value_avg, error_avg )
