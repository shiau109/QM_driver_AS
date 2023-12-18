"""
        TIME RABI
The sequence consists in playing the qubit pulse and measuring the state of the resonator
for different qubit pulse durations.
The results are then post-processed to find the qubit pulse duration for the chosen timelitude.

Prerequisites:
    - Having found the resonance frequency of the resonator coupled to the qubit under study (resonator_spectroscopy).
    - Having calibrated the IQ mixer connected to the qubit drive line (external mixer or Octave port)
    - Having found the rough qubit frequency and pi pulse timelitude (rabi_chevron_timelitude or power_rabi).
    - Set the qubit frequency and desired pi pulse timelitude (pi_time_q) in the configuration.
    - Set the desired flux bias

Next steps before going to the next node:
    - Update the qubit pulse duration (pi_len_q) in the configuration.
"""

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
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
#   Data Saving   #
###################
from datetime import datetime
import sys

# save_data = True  # Default = False in configuration file
save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
save_time = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
save_path = f"{save_dir}\{save_time}_{save_progam_name}"


###################
# The QUA program #
###################
t_min = 4
t_max = 100
dt = 1
times = np.arange(t_min, t_max, dt)  # In clock cycles = 4ns
thermalization_time = 100 * u.us
n_avg = 3000

q_id = [0,1,2,3,4]

# Tune flux and neighboring qubits
flux_id = 0
flux_offset = np.zeros(5)
flux_offset[flux_id] = max_frequency_point[flux_id]
detune_neighbor = True
if detune_neighbor == True:
    if flux_id != 0: flux_offset[flux_id-1] = detune_point[flux_id-1]
    if flux_id != 4: flux_offset[flux_id+1] = detune_point[flux_id+1]

with program() as rabi:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=5)
    t = declare(int)  # QUA variable for the qubit pulse duration

    for i in [0,1,2,3]:
        set_dc_offset(f"q{i+1}_z", "single", flux_offset[i])

    with for_(n, 0, n < n_avg, n + 1):
        with for_(*from_array(t, times)):
            # Play the qubit pulses
            play("x180", f"q{flux_id+1}_xy", duration=t)
            # Align the elements to measure after playing the qubit pulses.
            align()
            # Start using Rotated integration weights (cf. IQ_blobs.py)
            multiplexed_readout(I, I_st, Q, Q_st, resonators=[1,2,3,4,5], weights="rotated_")
            # Wait for the qubit to decay to the ground state
            wait(thermalization_time * u.ns)
        # Save the averaging iteration to get the progress bar
        save(n, n_st)

    with stream_processing():
        n_st.save("n")
        for i in q_id:
            I_st[i].buffer(len(times)).average().save(f"I{i+1}")
            Q_st[i].buffer(len(times)).average().save(f"Q{i+1}")


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
    job = qmm.simulate(config, rabi, simulation_config)
    job.get_simulated_stimeles().con1.plot()

else:
    # Open the quantum machine
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(rabi)


    
    # Prepare the figure for live plotting
    fig = plt.figure()
    interrupt_on_close(fig, job)
    # Tool to easily fetch results from the OPX (results_handle used in it)
    results = fetching_tool(job, ["n", "I1", "Q1", "I2", "Q2"], mode="live")
    # Live plotting
    while results.is_processing():
        # Fetch results
        n, I1, Q1, I2, Q2 = results.fetch_all()
        # Progress bar
        progress_counter(n, n_avg, start_time=results.start_time)
        # Convert the results into Volts
        I1, Q1 = u.demod2volts(I1, readout_len), u.demod2volts(Q1, readout_len)
        I2, Q2 = u.demod2volts(I2, readout_len), u.demod2volts(Q2, readout_len)
        # Plots
        plt.suptitle(f"Time Rabi \n number of average = {n_avg}")
        plt.subplot(221)
        plt.cla()
        plt.plot(4 * times, I1)
        # plt.title(f"Qubit 3 \n Readout timelitude = {readout_time[0]}V, Readout length = {readout_len}us \n Pi pulse timelitude = {pi_time[0]}V")
        plt.ylabel("I quadrature [V]")
        plt.subplot(223)
        plt.cla()
        plt.plot(4 * times, Q1)
        plt.xlabel("Qubit pulse duration [ns]")
        plt.ylabel("Q quadrature [V]")
        plt.subplot(222)
        plt.cla()
        plt.plot(4 * times, I2)
        # plt.title(f"Qubit 4 \n Readout timelitude = {readout_time[1]}V, Readout length = {readout_len}us \n Pi pulse timelitude = {pi_time[1]}V")
        plt.subplot(224)
        plt.cla()
        plt.plot(4 * times, Q2)
        plt.xlabel("Qubit pulse duration [ns]")
        plt.tight_layout()
        plt.pause(1.0)

    ###################
    #  Figure Saving  #
    ################### 
    if save_data == True:
        figure = plt.gcf() # get current figure
        figure.set_size_inches(16, 8.5)
        plt.tight_layout()
        # Save Figure
        plt.savefig(f"{save_path}.png", dpi = 500)


    # Fit the time Rabi curves
    try:
        from qualang_tools.plot.fitting import Fit

        fit = Fit()
        plt.figure()
        plt.suptitle(f"Time Rabi \n number of average = {n_avg}")
        plt.subplot(121)
        fit.rabi(4 * times, I1, plot=True)
        plt.xlabel("Qubit pulse duration [ns]")
        plt.ylabel("I quadrature [V]")
        # plt.title(f"Qubit 3 \n Readout timelitude = {readout_time[0]}V, Readout length = {readout_len}us \n Pi pulse timelitude = {pi_time_q1}V")
        plt.subplot(122)
        fit.rabi(4 * times, I2, plot=True)
        plt.xlabel("Qubit pulse duration [ns]")
        # plt.title(f"Qubit 4 \n Readout timelitude = {readout_time[1]}V, Readout length = {readout_len}us \n Pi pulse timelitude = {pi_time_q2}V")
        plt.tight_layout()
    except (Exception,):
        pass

    ###################
    #  Figure Saving  #
    ################### 
    if save_data == True:
        figure = plt.gcf() # get current figure
        figure.set_size_inches(16, 8.5)
        plt.tight_layout()
        # Save Figure
        plt.savefig(f"{save_path}-fitting.png", dpi = 500)
    

    ###################
    #   .npz Saving   #
    ###################
    if save_data == True:
        # Change what you want to save
        np.savez(save_path,
                times=4*times,
                I3=I1, Q3=Q1,
                I4=I2, Q4=Q2
                )

    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    plt.show()