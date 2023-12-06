"""
        ALL-XY MEASUREMENT
The program consists in playing a random sequence of predefined gates after which the theoretical qubit state is known.
See [Reed's Thesis](https://rsl.yale.edu/sites/default/files/files/RSL_Theses/reed.pdf) for more details.

The sequence of gates defined below is based on https://rsl.yale.edu/sites/default/files/physreva.82.pdf-optimized_driving_0.pdf
This protocol checks that the single qubit gates (x180, x90, y180 and y90) are properly defined and calibrated and can
thus be used as a preliminary step before randomized benchmarking.

Prerequisites:
    - Having found the resonance frequency of the resonator coupled to the qubit under study (resonator_spectroscopy).
    - Having calibrated qubit pi pulse (x180) by running qubit, spectroscopy, rabi_chevron, power_rabi and updated the config.
    - Having the qubit frequency perfectly calibrated (ramsey).
    - (optional) Having calibrated the readout (readout_frequency, amplitude, duration_optimization IQ_blobs) for better SNR.
    - Set the desired flux bias.
"""

from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from configuration import *
import matplotlib.pyplot as plt
import numpy as np
from qm import SimulationConfig
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
import warnings

warnings.filterwarnings("ignore")

###################
#   Data Saving   #
###################
from datetime import datetime
import sys
# save_data = True  # Default = False in configuration file
save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
save_time = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
save_path = f"{save_dir}\{save_time}_{save_progam_name}"

##############################
# Program-specific variables #
##############################
  # The resonator to measure the qubit defined above
n_avg = 500000  # The number of 

# # Tune flux and neighboring qubits
# flux_id = 0
# flux_offset = np.zeros(5)
# flux_offset[flux_id] = max_frequency_point[flux_id]
# detune_neighbor = True
# if detune_neighbor == True:
#     if flux_id != 0: flux_offset[flux_id-1] = detune_point[flux_id-1]
#     if flux_id != 4: flux_offset[flux_id+1] = detune_point[flux_id+1]

# All XY sequences. The sequence names must match corresponding operation in the config
sequence = [
    ("I", "I"),
    ("x180", "x180"),
    ("y180", "y180"),
    ("x180", "y180"),
    ("y180", "x180"),
    ("x90", "I"),
    ("y90", "I"),
    ("x90", "y90"),
    ("y90", "x90"),
    ("x90", "y180"),
    ("y90", "x180"),
    ("x180", "y90"),
    ("y180", "x90"),
    ("x90", "x180"),
    ("x180", "x90"),
    ("y90", "y180"),
    ("y180", "y90"),
    ("x180", "I"),
    ("y180", "I"),
    ("x90", "x90"),
    ("y90", "y90"),
]


# All XY macro generating the pulse sequences from a python list.
def allXY(pulses, qb, res, xyw):
    """
    Generate a QUA sequence based on the two operations written in pulses. Used to generate the all XY program.
    **Example:** I, Q = allXY(['I', 'y90'])
    :param pulses: tuple containing a particular set of operations to play. The pulse names must match corresponding
        operations in the config except for the identity operation that must be called 'I'.
    :param qubit: The qubit element as defined in the config.
    :param resonator: The resonator element as defined in the config.
    :return: two QUA variables for the 'I' and 'Q' quadratures measured after the sequence.
    """
    I_xy = declare(fixed)
    Q_xy = declare(fixed)
    if pulses[0] != "I":
        play(pulses[0], qb)  # Either play the sequence
    else:
        wait(xyw // 4, qb)  # or wait if sequence is identity
    if pulses[1] != "I":
        play(pulses[1], qb)  # Either play the sequence
    else:
        wait(xyw // 4, qb)  # or wait if sequence is identity

    align(qb, res)
    # Play through the 2nd resonator to be in the same condition as when the readout was optimized
    # if resonator == "rr1":
    #     align(qubit, "rr2")
    #     measure("readout", "rr2", None)
    # elif resonator == "rr2":
    #     align(qubit, "rr1")
    #     measure("readout", "rr1", None)
    measure(
        "readout",
        res,
        None,
        dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", I_xy),
        dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", Q_xy),
    )
    return I_xy, Q_xy


###################
# The QUA program #
###################
def AllXY_executor(qb,res,xyw,n_avg,configuration,qm_mache,mode):
    with program() as ALL_XY:
        n = declare(int)
        n_st = declare_stream()
        r = Random()  # Pseudo random number generator
        r_ = declare(int)  # Index of the sequence to play
        # The result of each set of gates is saved in its own stream
        I_st = [declare_stream() for _ in range(21)]
        Q_st = [declare_stream() for _ in range(21)]

        # for i in [0,1,2,3]:
        #     # set_dc_offset(f"q{i+1}_z", "single", flux_offset[i])
        #     set_dc_offset(f"q{i+1}_z", "single", max_frequency_point[i])

        with for_(n, 0, n < n_avg, n + 1):
            # Get a value from the pseudo-random number generator on the OPX FPGA
            assign(r_, r.rand_int(21))
            # # Wait for the qubit to decay to the ground state - Can be replaced by active reset
            # wait(thermalization_time * u.ns, qb)
            wait(100 * u.us, qb)
            # Plays a random XY sequence
            # The switch/case method allows to map a python index (here "i") to a QUA number (here "r_") in order to switch
            # between elements in a python list (here "sequence") that cannot be converted into a QUA array (here because it
            # contains strings).
            with switch_(r_):
                for i in range(21):
                    with case_(i):
                        # Play the all-XY sequence corresponding to the drawn random number
                        I, Q = allXY(sequence[i], qb, res, xyw)
                        # Save the 'I' & 'Q' quadratures to their respective streams
                        save(I, I_st[i])
                        save(Q, Q_st[i])
            save(n, n_st)

        with stream_processing():
            n_st.save("n")
            for i in range(21):
                I_st[i].average().save(f"I{i}")
                Q_st[i].average().save(f"Q{i}")

    #####################################
    #  Open Communication with the QOP  #
    #####################################
    

    ###########################
    # Run or Simulate Program #
    ###########################

    simulate = False

    if simulate:
        # Simulates the QUA program for the specified duration
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qm_mache.simulate(configuration, ALL_XY, simulation_config)
        job.get_simulated_samples().con1.plot()

    else:
        # Open the quantum machine
        qm = qm_mache.open_qm(configuration)
        # Send the QUA program to the OPX, which compiles and executes it
        job = qm.execute(ALL_XY)
        # Get results from QUA program
        data_list = ["n"] + list(np.concatenate([[f"I{i}", f"Q{i}"] for i in range(len(sequence))]))
        results = fetching_tool(job, data_list, mode="live")
        # Live plotting
        if mode == 'live':
            fig = plt.figure()
            interrupt_on_close(fig, job)  # Interrupts the job when closing the figure
            while results.is_processing():
                # Fetch results
                res = results.fetch_all()
                I = -np.array(res[1::2])
                Q = -np.array(res[2::2])
                n = res[0]
                # Progress bar
                progress_counter(n, n_avg, start_time=results.start_time)
                # Plot results
                plt.suptitle(f"All XY for qubit {qb}")
                plt.subplot(211)
                plt.cla()
                plt.plot(I, "bx", label="Experimental data")
                plt.plot([np.max(I)] * 5 + [(np.mean(I))] * 12 + [np.min(I)] * 4, "r-", label="Expected value")
                plt.ylabel("I quadrature [a.u.]")
                plt.xticks(ticks=range(len(sequence)), labels=["" for _ in sequence], rotation=45)
                plt.legend()
                plt.subplot(212)
                plt.cla()
                plt.plot(Q, "bx", label="Experimental data")
                plt.plot([np.max(Q)] * 5 + [(np.mean(Q))] * 12 + [np.min(Q)] * 4, "r-", label="Expected value")
                plt.ylabel("Q quadrature [a.u.]")
                plt.xticks(ticks=range(len(sequence)), labels=[str(el) for el in sequence], rotation=45)
                plt.legend()
                plt.tight_layout()
                plt.pause(0.1)
                if save_data == True:
                    ###################
                    #  Figure Saving  #
                    ################### 
                    figure = plt.gcf() # get current figure
                    figure.set_size_inches(9, 5)
                    plt.tight_layout()
                    plt.pause(0.1)
                    plt.savefig(f"{save_path}.png", dpi = 500)   
                plt.show()
            qm.close()
            return {}
        else:
            while results.is_processing():
                # Fetch results
                res = results.fetch_all()
                n = res[0]
                signal_avg = np.mean(-np.array(res[1::2]))
                # Progress bar
                progress_counter(n, n_avg, start_time=results.start_time)
            qm.close()
            return {"I":-np.array(res[1::2]),"Q":-np.array(res[2::2]),"amp_error":(-np.array(res[1::2])[-7]-np.array(res[1::2])[-8])/2-signal_avg}

        # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
        


if __name__ == '__main__':
    sample = input("(A) Dynamic or (B) Static ?")

    if sample.lower() == 'b':

        qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
        xyw = pi_len
        i = 0
        qb = f"q{i+1}_xy"  # The qubit under study
        res = f"rr{i+1}"

        ret = AllXY_executor(qb,res,xyw,config,qmm,mode='live')
    
    else:
        qop_ip = '192.168.1.105'
        qop_port = None
        cluster_name = 'QPX_2'
        target_q = 'q1'
        res = f'{target_q}_ro'
        qb =  f"{target_q}_xy"

        port_mapping = {
            ("con1", 1): ("octave1", "I1"),
            ("con1", 2): ("octave1", "Q1"),
            ("con1", 3): ("octave1", "I2"),
            ("con1", 4): ("octave1", "Q2"),
            ("con1", 5): ("octave1", "I3"),
            ("con1", 6): ("octave1", "Q3"),
            ("con1", 7): ("octave1", "I4"),
            ("con1", 8): ("octave1", "Q4"),
            ("con1", 9): ("octave1", "I5"),
            ("con1", 10): ("octave1", "Q5"),
        }

        octave_1 = OctaveUnit("octave1", qop_ip, port=11250, con="con1", clock="Internal", port_mapping=port_mapping)
        # Add the octaves
        octaves = [octave_1]
        # Configure the Octaves
        octave_config = octave_declaration(octaves)

        qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

        # load config file
        from QM_config_dynamic import QM_config, Circuit_info
        dyna_config = QM_config()
        dyna_config.import_config(path=r'.\TEST\BETAsite\QM\OPXPlus\3_5q Tune up\Standard Configuration\Config_1201_afterAmpCali')
        the_specs = Circuit_info(q_num=5)
        the_specs.import_spec(path=r'.\TEST\BETAsite\QM\OPXPlus\3_5q Tune up\Standard Configuration\Spec_1201_afterAmpCali')
        print(dyna_config.get_config()['mixers']['octave_octave1_2'][-1])
        # 0.422 MHz
        old_if = the_specs.get_spec_forConfig('xy')[target_q]['qubit_IF']*1e-6
        
        # dyna_config.update_controlFreq(the_specs.update_aXyInfo_for(target_q='q1',IF=old_if+0.422))
        xyw = the_specs.get_spec_forConfig('xy')[target_q]['pi_len']
        
        print(dyna_config.get_config()['mixers']['octave_octave1_2'][-1])
        print(dyna_config.get_config()['elements']['q1_xy'])
        ret = AllXY_executor(qb,res,xyw,dyna_config.get_config(),qmm,mode='live')
    
