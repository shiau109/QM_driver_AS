"""
        RAMSEY CHEVRON (IDLE TIME VS FREQUENCY)
The program consists in playing a Ramsey sequence (x90 - idle_time - x90 - measurement) for different qubit intermediate
frequencies and idle times.
From the results, one can estimate the qubit frequency more precisely than by doing Rabi and also gets a rough estimate
of the qubit coherence time.

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
from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
from macros import qua_declaration, multiplexed_readout
import warnings

warnings.filterwarnings("ignore")


###################
# The QUA program #
###################
n_avg = 1000  # Number of averages
q_id = [0,1,2,3]
dfs = np.arange(-1.5e6, 1.5e6, 0.1e6)  # Frequency detuning sweep in Hz
t_delay = np.arange(1, 200, 4)  # Idle time sweep in clock cycles (Needs to be a list of integers)

operation_flux_point = [0, 4.000e-02, -3.100e-01, 4.000e-02]

with program() as ramsey:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=4)
    t = declare(int)  # QUA variable for the idle time
    df = declare(int)  # QUA variable for the qubit frequency
    # Adjust the flux line biases to check whether you are actually measuring the qubit
    for i in q_id:
        set_dc_offset("q%s_z"%(i+1), "single", operation_flux_point[i])

    with for_(n, 0, n < n_avg, n + 1):
        with for_(*from_array(df, dfs)):
            # Update the frequency of the two qubit elements
            # update_frequency("q1_xy", df + qubit_IF[0])
            # update_frequency("q2_xy", df + qubit_IF[1])
            update_frequency("q3_xy", df + qubit_IF[2])
            # update_frequency("q4_xy", df + qubit_IF[3])
            
            with for_(*from_array(t, t_delay)):
                # qubit 1
                # play("x90", "q1_xy")
                # wait(t, "q1_xy")
                # play("x90", "q1_xy")
                # qubit 2
                # play("x90", "q2_xy")
                # wait(t, "q2_xy")
                # play("x90", "q2_xy")
                # qubit 3
                play("x90", "q3_xy")
                wait(t, "q3_xy")
                play("x90", "q3_xy")
                # qubit 4
                # play("x90", "q4_xy")
                # wait(t, "q4_xy")
                # play("x90", "q4_xy")
                # Align the elements to measure after having waited a time "tau" after the qubit pulses.
                align()
                # Measure the state of the resonators
                multiplexed_readout(I, I_st, Q, Q_st, resonators=[1, 2, 3, 4], weights="rotated_")
                # Wait for the qubit to decay to the ground state
                wait(thermalization_time * u.ns)
        # Save the averaging iteration to get the progress bar
        save(n, n_st)

    with stream_processing():
        n_st.save("n")
        # resonator 1
        I_st[0].buffer(len(t_delay)).buffer(len(dfs)).average().save("I1")
        Q_st[0].buffer(len(t_delay)).buffer(len(dfs)).average().save("Q1")
        # resonator 2
        I_st[1].buffer(len(t_delay)).buffer(len(dfs)).average().save("I2")
        Q_st[1].buffer(len(t_delay)).buffer(len(dfs)).average().save("Q2")
        # resonator 3
        I_st[2].buffer(len(t_delay)).buffer(len(dfs)).average().save("I3")
        Q_st[2].buffer(len(t_delay)).buffer(len(dfs)).average().save("Q3")
        # resonator 4
        I_st[3].buffer(len(t_delay)).buffer(len(dfs)).average().save("I4")
        Q_st[3].buffer(len(t_delay)).buffer(len(dfs)).average().save("Q4")

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
    job = qmm.simulate(config, ramsey, simulation_config)
    job.get_simulated_samples().con1.plot()
else:
    # Open the quantum machine
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(ramsey)
    # Prepare the figure for live plotting
    fig = plt.figure()
    interrupt_on_close(fig, job)
    # Tool to easily fetch results from the OPX (results_handle used in it)
    results = fetching_tool(job, ["n", "I1", "Q1", "I2", "Q2", "I3", "Q3", "I4", "Q4"], mode="live")
    # Live plotting
    while results.is_processing():
        # Fetch results
        n, I1, Q1, I2, Q2, I3, Q3, I4, Q4 = results.fetch_all()
        # Convert the results into Volts
        I1, Q1 = u.demod2volts(I1, readout_len), u.demod2volts(Q1, readout_len)
        I2, Q2 = u.demod2volts(I2, readout_len), u.demod2volts(Q2, readout_len)
        I3, Q3 = u.demod2volts(I3, readout_len), u.demod2volts(Q3, readout_len)
        I4, Q4 = u.demod2volts(I4, readout_len), u.demod2volts(Q4, readout_len)
        # Progress bar
        progress_counter(n, n_avg, start_time=results.start_time)
        # Plot
        plt.suptitle("Ramsey chevron \n Number of average = " + str(n_avg))
        plt.subplot(241)
        plt.cla()
        plt.pcolor(4 * t_delay, dfs / u.MHz, I1)
        plt.title(f"Center frequency = {(qubit_LO[0] + qubit_IF[0]) / u.MHz} MHz \n Qubit 1 I")
        plt.ylabel("Frequency detuning [MHz]")
        plt.axhline(y=0, color="k", ls="--", alpha=0.8, linewidth=3)
        plt.subplot(245)
        plt.cla()
        plt.pcolor(4 * t_delay, dfs / u.MHz, Q1)
        plt.title("Qubit 1 Q")
        plt.xlabel("Idle time [ns]")
        plt.ylabel("Frequency detuning [MHz]")
        plt.subplot(242)
        plt.cla()
        plt.pcolor(4 * t_delay, dfs / u.MHz, I2)
        plt.title(f"Center frequency = {(qubit_LO[1]+ qubit_IF[1]) / u.MHz} MHz \n Qubit 2 I")
        plt.axhline(y=0, color="k", ls="--", alpha=0.8, linewidth=3)
        plt.subplot(246)
        plt.cla()
        plt.pcolor(4 * t_delay, dfs / u.MHz, Q2)
        plt.title("Qubit 2 Q")
        plt.xlabel("Idle time [ns]")
        plt.subplot(243)
        plt.cla()
        plt.pcolor(4 * t_delay, dfs / u.MHz, I3)
        plt.title(f"Center frequency = {(qubit_LO[2]+ qubit_IF[2]) / u.MHz} MHz \n Qubit 3 I")
        plt.ylabel("Frequency detuning [MHz]")
        plt.axhline(y=0, color="k", ls="--", alpha=0.8, linewidth=3)
        plt.subplot(247)
        plt.cla()
        plt.pcolor(4 * t_delay, dfs / u.MHz, Q3)
        plt.title("Qubit 3 Q")
        plt.xlabel("Idle time [ns]")
        plt.ylabel("Frequency detuning [MHz]")
        plt.subplot(244)
        plt.cla()
        plt.pcolor(4 * t_delay, dfs / u.MHz, I4)
        plt.title(f"Center frequency = {(qubit_LO[3] + qubit_IF[3]) / u.MHz} MHz \n Qubit 4 I")
        plt.axhline(y=0, color="k", ls="--", alpha=0.8, linewidth=3)
        plt.subplot(248)
        plt.cla()
        plt.pcolor(4 * t_delay, dfs / u.MHz, Q4)
        plt.title("Qubit 4 Q")
        plt.xlabel("Idle time [ns]")
        plt.tight_layout()
        plt.pause(0.1)

    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    plt.show()
plt.show()