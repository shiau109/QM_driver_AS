"""
        RABI CHEVRON (AMPLITUDE VS FREQUENCY)
This sequence involves executing the qubit pulse and measuring the state
of the resonator across various qubit intermediate frequencies and pulse amplitudes.
By analyzing the results, one can determine the qubit and estimate the x180 pulse amplitude for a specified duration.

Prerequisites:
    - Determination of the resonator's resonance frequency when coupled to the qubit of interest (referred to as "resonator_spectroscopy").
    - Calibration of the IQ mixer connected to the qubit drive line (be it an external mixer or an Octave port).
    - Identification of the approximate qubit frequency (referred to as "qubit_spectroscopy").
    - Configuration of the qubit frequency and the desired pi pulse duration (labeled as "pi_len_q").
    - Set the desired flux bias

Before proceeding to the next node:
    - Adjust the qubit frequency setting, labeled as "qubit_IF_q", in the configuration.
    - Modify the qubit pulse amplitude setting, labeled as "pi_amp_q", in the configuration.
"""

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
import sys
import pathlib
QM_script_root = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(QM_script_root)
from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
import warnings
from datetime import datetime
from scipy import signal
from macros import qua_declaration, multiplexed_readout, live_plotting
warnings.filterwarnings("ignore")

###################
# The QUA program #
###################
n_avg = 100  # The number of averages
# Qubit detuning sweep with respect to qubit_IF
dfs = np.arange(-10e6, +10e6, 0.05e6)  # optifined
#dfs = np.arange(-50e6, 50e6, 1e6)
# Qubit pulse amplitude sweep (as a pre-factor of the qubit pulse amplitude) - must be within [-2; 2)
durations = np.arange(4, 100, 2)
q_id = [1,2,3,4]
save_data = False  # change to True when you want to save data

if save_data == True:
    save_dir = r"C:\Users\ASUS\SynologyDrive\09 Data\Fridge Data\Qubit\20231011_DR4_5QX\07 rabi_chevron_duration"  # change save directory
    # save_name = f"Test"  # change data name
    save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
    save_time = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
    # save_path = f"{save_dir}\{save_time}_{save_progam_name}_{save_name}"
    save_path = f"{save_dir}\{save_time}_{save_progam_name}"
    # save_path = f"{save_dir}\Test"


with program() as rabi_chevron:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=4)
    df = declare(int)  # QUA variable for the qubit detuning
    t = declare(int)  # QUA variable for the qubit pulse duration
    # Adjust the flux line biases to check whether you are actually measuring the qubit
    for i in q_id:
        set_dc_offset("q%s_z"%(i+1), "single", max_frequency_point[i])
    # Adjust the flux line biases to check whether you are actually measuring the qubit
    # for i in q_id:
    #     set_dc_offset("q%s_z"%(i+1), "single", max_frequency_point[i])
    with for_(n, 0, n < n_avg, n + 1):
        with for_(*from_array(df, dfs)):
            # Update the frequency of the two qubit elements
            # update_frequency("q1_xy", df + qubit_IF[0])
            update_frequency("q2_xy", df + qubit_IF[1])
            # update_frequency("q1_xy", df + qubit_IF_q3)
            # update_frequency("q2_xy", df + qubit_IF_q4)

            with for_(*from_array(t, durations)):
                # Play qubit pulses simultaneously
                # play("x180", "q1_xy", duration=t)
                play("x180", "q2_xy", duration=t)
                # Measure after the qubit pulses
                align()
                # Multiplexed readout, also saves the measurement outcomes
                multiplexed_readout(I, I_st, Q, Q_st, resonators=[1, 2, 3, 4], weights="rotated_")
                # Wait for the qubit to decay to the ground state
                wait(thermalization_time * u.ns)
        # Save the averaging iteration to get the progress bar
        save(n, n_st)

    with stream_processing():
        n_st.save("n")
        # resonator 1
        I_st[0].buffer(len(durations)).buffer(len(dfs)).average().save("I1")
        Q_st[0].buffer(len(durations)).buffer(len(dfs)).average().save("Q1")
        # resonator 2
        I_st[1].buffer(len(durations)).buffer(len(dfs)).average().save("I2")
        Q_st[1].buffer(len(durations)).buffer(len(dfs)).average().save("Q2")
        # resonator 3
        I_st[2].buffer(len(durations)).buffer(len(dfs)).average().save("I3")
        Q_st[2].buffer(len(durations)).buffer(len(dfs)).average().save("Q3")
        # resonator 4
        I_st[3].buffer(len(durations)).buffer(len(dfs)).average().save("I4")
        Q_st[3].buffer(len(durations)).buffer(len(dfs)).average().save("Q4")


#####################################
#  Open Communication with the QOP  #
#####################################
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

###########################
# Run or Simulate Program #
###########################

simulate = False

if simulate:
    # Simulates the QUA program for the specified duration
    simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
    job = qmm.simulate(config, rabi_chevron, simulation_config)
    job.get_simulated_samples().con1.plot()
    plt.show()
else:
    # Open the quantum machine
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(rabi_chevron)
    # Prepare the figure for live plotting
    fig = plt.figure()
    interrupt_on_close(fig, job)
    # Tool to easily fetch results from the OPX (results_handle used in it)
    results = fetching_tool(job, ["n", "I1", "Q1", "I2", "Q2", "I3", "Q3", "I4", "Q4"], mode="live")

    # Live plotting
    while results.is_processing():
        # Fetch results
        n, I1, Q1, I2, Q2, I3, Q3, I4, Q4 = results.fetch_all()
        # Progress bar
        progress_counter(n, n_avg, start_time=results.start_time)
        # Convert the results into Volts
        I1, Q1 = u.demod2volts(I1, readout_len), u.demod2volts(Q1, readout_len)
        I2, Q2 = u.demod2volts(I2, readout_len), u.demod2volts(Q2, readout_len)
        I3, Q3 = u.demod2volts(I3, readout_len), u.demod2volts(Q3, readout_len)
        I4, Q4 = u.demod2volts(I4, readout_len), u.demod2volts(Q4, readout_len)
        # Data analysis
        S1 = u.demod2volts(I1 + 1j * Q1, readout_len)
        S2 = u.demod2volts(I2 + 1j * Q2, readout_len)
        S3 = u.demod2volts(I3 + 1j * Q3, readout_len)
        S4 = u.demod2volts(I4 + 1j * Q4, readout_len)
        R1 = np.abs(S1)
        phase1 = np.angle(S1)
        R2 = np.abs(S2)
        phase2 = np.angle(S2)
        R3 = np.abs(S3)
        phase3 = np.angle(S3)
        R4 = np.abs(S4)
        phase4 = np.angle(S4)
        # Plots
        plt.suptitle("Rabi chevron")

        # plt.subplot(241)
        # plt.cla()
        # plt.pcolor(durations * 4, dfs, I1)
        # plt.xlabel("Qubit pulse duration [ns]")
        # plt.ylabel("Qubit 1 detuning [MHz]")
        # plt.title(f"Q2 (f_res: {(qubit_LO[0] + qubit_IF[0]) / u.MHz} MHz)")
        # plt.subplot(245)
        # plt.cla()
        # plt.pcolor(durations * 4, dfs, Q1)
        # plt.xlabel("Qubit pulse duration [ns]")
        # plt.ylabel("Qubit 1 detuning [MHz]")

        plt.subplot(121)
        plt.cla()
        plt.pcolor(durations * 4, dfs, I2)
        plt.title(f"Q3 (f_res: {(qubit_LO[1] + qubit_IF[1]) / u.MHz} MHz)")
        plt.xlabel("Qubit pulse duration [ns]")
        plt.ylabel("Qubit 2 detuning [MHz]")
        plt.subplot(122)
        plt.cla()
        plt.pcolor(durations * 4, dfs, Q2)
        plt.xlabel("Qubit pulse duration [ns]")
        plt.ylabel("Qubit 2 detuning [MHz]")

        # plt.subplot(243)
        # plt.cla()
        # plt.pcolor(durations * 4, dfs, I3)
        # plt.xlabel("Qubit pulse duration [ns]")
        # plt.ylabel("Qubit 3 detuning [MHz]")
        # plt.title(f"Q4 (f_res: {(qubit_LO[2] + qubit_IF[2]) / u.MHz} MHz)")
        # plt.subplot(247)
        # plt.cla()
        # plt.pcolor(durations * 4, dfs, Q3)
        # plt.xlabel("Qubit pulse duration [ns]")
        # plt.ylabel("Qubit 3 detuning [MHz]")

        # plt.subplot(244)
        # plt.cla()
        # plt.pcolor(durations * 4, dfs, I4)
        # plt.xlabel("Qubit pulse duration [ns]")
        # plt.ylabel("Qubit 4 detuning [MHz]")
        # plt.title(f"Q4 (f_res: {(qubit_LO[2]+ qubit_IF[3]) / u.MHz} MHz)")
        # plt.subplot(248)
        # plt.cla()
        # plt.pcolor(durations * 4, dfs, Q4)
        # plt.xlabel("Qubit pulse duration [ns]")
        # plt.ylabel("Qubit 4 detuning [MHz]")

        plt.tight_layout()
        plt.pause(0.1)


    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
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
                R1=R1, P1=phase1, U1=signal.detrend(np.unwrap(phase1)), I1=I1, Q1=Q1, 
                R2=R2, P2=phase2, U2=signal.detrend(np.unwrap(phase2)), I2=I2, Q2=Q2, 
                R3=R3, P3=phase3, U3=signal.detrend(np.unwrap(phase3)), I3=I3, Q3=Q3,
                R4=R4, P4=phase4, U4=signal.detrend(np.unwrap(phase4)), I4=I4, Q4=Q4,
                # R5=R5, P5=phase5, U5=signal.detrend(np.unwrap(phase5)), I5=I5, Q5=Q5,
                )
        
plt.show()
