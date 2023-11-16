"""
        TIME RABI
The sequence consists in playing the qubit pulse and measuring the state of the resonator
for different qubit pulse durations.
The results are then post-processed to find the qubit pulse duration for the chosen amplitude.

Prerequisites:
    - Having found the resonance frequency of the resonator coupled to the qubit under study (resonator_spectroscopy).
    - Having calibrated the IQ mixer connected to the qubit drive line (external mixer or Octave port)
    - Having found the rough qubit frequency and pi pulse amplitude (rabi_chevron_amplitude or power_rabi).
    - Set the qubit frequency and desired pi pulse amplitude (pi_amp_q) in the configuration.
    - Set the desired flux bias

Next steps before going to the next node:
    - Update the qubit pulse duration (pi_len_q) in the configuration.
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
from common_fitting_func import *
import warnings

warnings.filterwarnings("ignore")

###################
# The QUA program #
###################
t_min = 4
t_max = 100
dt = 1
times = np.arange(t_min, t_max, dt)  # In clock cycles = 4ns
cooldown_time = 1 * u.us
n_avg = 5000
q_id = [0,1,2,3]
Qi = 4
operation_flux_point = [0, 4.000e-02, 4.000e-02, -3.200e-01] 
res_F = resonator_flux( operation_flux_point[Qi-1], *p1[Qi-1])
res_IF = (res_F - resonator_LO)/1e6
res_IF = int(res_IF * u.MHz)

with program() as rabi:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=4)
    t = declare(int)  # QUA variable for the qubit pulse duration
    resonator_freq1 = declare(int, value=res_IF)
    # Adjust the flux line biases to check whether you are actually measuring the qubit
    for i in q_id:
        set_dc_offset("q%s_z"%(i+1), "single", operation_flux_point[i])
    update_frequency(f"rr{Qi}", resonator_freq1)
    with for_(n, 0, n < n_avg, n + 1):
        with for_(*from_array(t, times)):
            # Play the qubit pulses
            # play("x180", "q1_xy", duration=t)
            # play("x180", "q2_xy", duration=t)
            # play("x180", "q3_xy", duration=t)
            play("x180", "q4_xy", duration=t)
            # Align the elements to measure after playing the qubit pulses.
            align()
            # Start using Rotated integration weights (cf. IQ_blobs.py)
            multiplexed_readout(I, I_st, Q, Q_st, resonators=[1, 2, 3, 4], weights="rotated_")
            # Wait for the qubit to decay to the ground state
            wait(thermalization_time * u.ns)
        # Save the averaging iteration to get the progress bar
        save(n, n_st)

    with stream_processing():
        n_st.save("n")
        # resonator 1
        I_st[0].buffer(len(times)).average().save("I1")
        Q_st[0].buffer(len(times)).average().save("Q1")
        # resonator 2
        I_st[1].buffer(len(times)).average().save("I2")
        Q_st[1].buffer(len(times)).average().save("Q2")
        # resonator 3
        I_st[2].buffer(len(times)).average().save("I3")
        Q_st[2].buffer(len(times)).average().save("Q3")
        # resonator 4
        I_st[3].buffer(len(times)).average().save("I4")
        Q_st[3].buffer(len(times)).average().save("Q4")

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
    job = qmm.simulate(config, rabi, simulation_config)
    job.get_simulated_samples().con1.plot()

else:
    # Open the quantum machine
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(rabi)
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
        # Plots
        plt.suptitle("Time Rabi \n number of average = " + str(n_avg))
        plt.subplot(241)
        plt.cla()
        plt.plot(4 * times, I1)
        plt.title("Qubit 1")
        plt.ylabel("I quadrature [V]")
        plt.subplot(245)
        plt.cla()
        plt.plot(4 * times, Q1)
        plt.xlabel("Qubit pulse duration [ns]")
        plt.ylabel("Q quadrature [V]")
        plt.subplot(242)
        plt.cla()
        plt.plot(4 * times, I2)
        plt.title("Qubit 2")
        plt.subplot(246)
        plt.cla()
        plt.plot(4 * times, Q2)
        plt.xlabel("Qubit pulse duration [ns]")
        plt.subplot(243)
        plt.cla()
        plt.plot(4 * times, I3)
        plt.title("Qubit 3")
        plt.ylabel("I quadrature [V]")
        plt.subplot(247)
        plt.cla()
        plt.plot(4 * times, Q3)
        plt.xlabel("Qubit pulse duration [ns]")
        plt.ylabel("Q quadrature [V]")
        plt.subplot(244)
        plt.cla()
        plt.plot(4 * times, I4)
        plt.title("Qubit 4")
        plt.ylabel("I quadrature [V]")
        plt.subplot(248)
        plt.cla()
        plt.plot(4 * times, Q4)
        plt.xlabel("Qubit pulse duration [ns]")
        plt.ylabel("Q quadrature [V]")
        plt.tight_layout()
        plt.pause(1.0)

    # Fit the time Rabi curves
    try:
        from qualang_tools.plot.fitting import Fit

        fit = Fit()
        plt.figure()
        plt.suptitle("Multiplexed Time Rabi \n number of average = " + str(n_avg))
        # plt.subplot(141)
        # fit.rabi(4 * times, I1, plot=True)
        # plt.xlabel("Qubit pulse duration [ns]")
        # plt.ylabel("I quadrature [V]")
        # plt.title("Qubit 1")
        # plt.subplot(142)
        # fit.rabi(4 * times, I2, plot=True)
        # plt.xlabel("Qubit pulse duration [ns]")
        # plt.title("Qubit 2")
        # plt.subplot(143)

        # fit.rabi(4 * times, I3, plot=True)
        # plt.xlabel("Qubit pulse duration [ns]")
        # plt.ylabel("I quadrature [V]")
        # plt.title("Qubit 3")

        fit.rabi(4 * times, I4, plot=True)
        plt.xlabel("Qubit pulse duration [ns]")
        plt.ylabel("I quadrature [V]")
        plt.title("Qubit 4")
        plt.tight_layout()

        plt.figure()
        fit.rabi(4 * times, Q4, plot=True)
        plt.xlabel("Qubit pulse duration [ns]")
        plt.ylabel("Q quadrature [V]")
        plt.title("Qubit 4")
        plt.tight_layout()
    
    except (Exception,):
        pass

    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    plt.show()