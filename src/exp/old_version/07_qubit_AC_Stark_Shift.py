"""
        QUBIT SPECTROSCOPY
This sequence involves sending a saturation pulse to the qubit, placing it in a mixed state,
and then measuring the state of the resonator across various qubit drive intermediate dfs.
In order to facilitate the qubit search, the qubit pulse duration and amplitude can be changed manually in the QUA
program directly without having to modify the configuration.

The data is post-processed to determine the qubit resonance frequency, which can then be used to adjust
the qubit intermediate frequency in the configuration under "qubit_IF".

Note that it can happen that the qubit is excited by the image sideband or LO leakage instead of the desired sideband.
This is why calibrating the qubit mixer is highly recommended.

This step can be repeated using the "x180" operation to adjust the pulse parameters (amplitude, duration, frequency)
before performing the next calibration steps.

Prerequisites:
    - Identification of the resonator's resonance frequency when coupled to the qubit in question (referred to as "resonator_spectroscopy_multiplexed").
    - Calibration of the IQ mixer connected to the qubit drive line (whether it's an external mixer or an Octave port).
    - Set the flux bias to the maximum frequency point, labeled as "max_frequency_point", in the configuration.
    - Configuration of the cw pulse amplitude (const_amp) and duration (const_len) to transition the qubit into a mixed state.
    - Specification of the expected qubits T1 in the configuration.

Before proceeding to the next node:
    - Update the qubit frequency, labeled as "qubit_IF_q", in the configuration.
"""

from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
import sys
import pathlib
QM_script_root = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(QM_script_root)
from configuration_with_octave import *
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.loops import from_array
from macros import qua_declaration, multiplexed_readout
from scipy import signal
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

###################
#   Data Saving   #
###################
from datetime import datetime
import sys
save_data = False  # change to True when you want to save data

if save_data == True:
    save_dir = r"C:\Users\ASUS\SynologyDrive\09 Data\Fridge Data\Qubit\20231011_DR4_5QX\08 AC_Stark_shift"  # change save directory
    # save_name = f"Test"  # change data name
    save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
    save_time = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
    # save_path = f"{save_dir}\{save_time}_{save_progam_name}_{save_name}"
    save_path = f"{save_dir}\{save_time}_{save_progam_name}"
    # save_path = f"{save_dir}\Test"

###################
# The QUA program #
###################
n_avg = 100000  # The number of averages
# Adjust the pulse duration and amplitude to drive the qubit into a mixed state

saturation_len1 = 2 * u.us  # In ns
saturation_amp1 = 0.001 # 0.005  # pre-factor to the value defined in the config - restricted to [-2; 2)
ro_amp_min = 0 
ro_amp_max = 1.2
da = 0.05
amplitudes = np.arange(ro_amp_min, ro_amp_max + da / 2, da)  # The amplitude vector +da/2 to add a_max to the scan 

# Qubit detuning sweep with respect to qubit_IF
span = 100 * u.MHz
df = 100 * u.kHz
dfs = np.arange(-span, span , df)

with program() as res_amp_vs_quibt_spec:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=1)
    df = declare(int)  # QUA variable for the readout frequency
    a = declare(fixed)  # QUA variable for sweeping the readout amplitude pre-factor

    # Adjust the flux line biases to check whether you are actually measuring the qubit
    set_dc_offset("q1_z", "single", max_frequency_point1)
    set_dc_offset("q2_z", "single", max_frequency_point2)
    with for_(n, 0, n < n_avg, n + 1):
        with for_(*from_array(df, dfs)):
            # Update the frequency of the two qubit elements
            update_frequency("q2_xy", df + qubit_IF_q2)            
            with for_(*from_array(a, amplitudes)):  # QUA for_ loop for sweeping the readout amplitude
                # Play the saturation pulse to put the qubit in a mixed state - Can adjust the amplitude on the fly [-2; 2)
                # qubit 1
                play("stark" * amp(a), "q2_ro", duration=saturation_len1 * u.ns) 
                wait(1500 * u.ns, "q2_xy")               
                # play("x180", "q2_xy")
                # play("x180", "q2_xy")
                # play("x180", "q2_xy")
                # play("x180", "q2_xy")
                play("x180", "q2_xy")

                align("q2_xy", "q2_ro")
                wait(3000 * u.ns)
                measure(
                    "readout",
                    "rr2",
                    None,
                    dual_demod.full("cos", "out1", "sin", "out2", I[0]),
                    dual_demod.full("minus_sin", "out1", "cos", "out2", Q[0]),
                )
                # Save the 'I' & 'Q' quadratures for rr2 to their respective streams
                save(I[0], I_st[0])
                save(Q[0], Q_st[0])
                # Wait for the qubit to decay to the ground state
                wait(20 * u.us)

        save(n, n_st)

    with stream_processing():
        n_st.save("n")
        # resonator 1
        I_st[0].buffer(len(amplitudes)).buffer(len(dfs)).average().save("I1")
        Q_st[0].buffer(len(amplitudes)).buffer(len(dfs)).average().save("Q1")

#####################################
#  Open Communication with the QOP  #
#####################################
qmm = QuantumMachinesManager(host=qop_ip, cluster_name=cluster_name, octave=octave_config)

###########################
# Run or Simulate Program #
###########################

simulate = False

if simulate:
    # Simulates the QUA program for the specified duration
    simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
    job = qmm.simulate(config, res_amp_vs_quibt_spec, simulation_config)
    job.get_simulated_samples().con1.plot()
    plt.show()
else:
    # Open a quantum machine to execute the QUA program
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(res_amp_vs_quibt_spec)
    # Prepare the figure for live plotting
    fig = plt.figure()
    interrupt_on_close(fig, job)
    # Tool to easily fetch results from the OPX (results_handle used in it)
    results = fetching_tool(job, ["n", "I1", "Q1"], mode="live")
    # Live plotting
    while results.is_processing():
        # Fetch results
        n, I1, Q1 = results.fetch_all()
        # Progress bar
        progress_counter(n, n_avg, start_time=results.start_time)
        # Data analysis
        S1 = u.demod2volts(I1 + 1j * Q1, readout_len)
        R1 = np.abs(S1)
        phase1 = np.angle(S1)

        # Plot
        plt.suptitle(f"AC Stark Shift \n Number of average = {n_avg}")
        plt.subplot(211)
        plt.cla()
        plt.title("Q2")
        plt.ylabel("qubit IF [MHz]")
        plt.pcolor((amplitudes * readout_amp_q1)*2, (dfs + qubit_IF_q1) / u.MHz, R1)

        plt.subplot(212)
        plt.cla()
        plt.xlabel("Readout power [V^2]")
        plt.ylabel("qubit IF [MHz]")
        plt.pcolor((amplitudes * readout_amp_q1)*2, (dfs + qubit_IF_q1) / u.MHz, signal.detrend(np.unwrap(phase1)))
        plt.pause(0.1)

    ###################
    #  Figure Saving  #
    ################### 
    if save_data == True:
        figure = plt.gcf() # get current figure
        figure.set_size_inches(16, 9)
        plt.tight_layout()
        # Save Figure
        plt.savefig(f"{save_path}.png", dpi = 500)

    ###################
    #   .npz Saving   #
    ###################
    if save_data == True:
        # Change what you want to save
        np.savez(save_path,
                F1=qubit_LO_q1+qubit_IF_q1+dfs, R1=R1, P1=phase1, U1=signal.detrend(np.unwrap(phase1)), I1=I1, Q1=Q1,
                )


    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()

    
    plt.show()