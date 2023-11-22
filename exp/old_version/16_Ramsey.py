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
from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.plot import interrupt_on_close
from macros import qua_declaration, multiplexed_readout
from qualang_tools.plot.fitting import Fit
import warnings

warnings.filterwarnings("ignore")


###################
# The QUA program #
###################
n_avg = 200  # Number of averages
idle_times = np.arange(4, 2500, 5)  # Idle time sweep in clock cycles (Needs to be a list of integers)
detuning = 1e6  # "Virtual" detuning in Hz
operation_flux_point = [0, 4.000e-02, -3.100e-01, 4.000e-02]
q_id = [0,1,2,3]

with program() as ramsey:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=4)
    t = declare(int)  # QUA variable for the idle time
    phi = declare(fixed)  # Phase to apply the virtual Z-rotation
    # Adjust the flux line biases to check whether you are actually measuring the qubit
    for i in q_id:
        set_dc_offset("q%s_z"%(i+1), "single", operation_flux_point[i])
    update_frequency("q3_xy", detuning + qubit_IF[2])
    with for_(n, 0, n < n_avg, n + 1):
        with for_(*from_array(t, idle_times)):
            # Rotate the frame of the second x90 gate to implement a virtual Z-rotation
            # 4*tau because tau was in clock cycles and 1e-9 because tau is ns
            # assign(phi, Cast.mul_fixed_by_int(detuning * 1e-9, 4 * t))
            # align()

            # Qubit 1
            # play("x90", "q1_xy")  # 1st x90 gate
            # wait(t, "q1_xy")  # Wait a varying idle time
            # frame_rotation_2pi(phi, "q1_xy")  # Virtual Z-rotation
            # play("x90", "q1_xy")  # 2nd x90 gate

            # Qubit 2
            # play("x90", "q2_xy")  # 1st x90 gate
            # wait(t, "q2_xy")  # Wait a varying idle time
            # frame_rotation_2pi(phi, "q2_xy")  # Virtual Z-rotation
            # play("x90", "q2_xy")  # 2nd x90 gate

            # Qubit 3
            play("x90", "q3_xy")  # 1st x90 gate
            wait(t, "q3_xy")  # Wait a varying idle time
            # # frame_rotation_2pi(phi, "q3_xy")  # Virtual Z-rotation
            play("x90", "q3_xy")  # 2nd x90 gate

            # Qubit 4
            # play("x90", "q4_xy")  # 1st x90 gate
            # wait(t, "q4_xy")  # Wait a varying idle time
            # frame_rotation_2pi(phi, "q4_xy")  # Virtual Z-rotation
            # play("x90", "q4_xy")  # 2nd x90 gate

            # Align the elements to measure after having waited a time "tau" after the qubit pulses.
            align()
            # Measure the state of the resonators
            multiplexed_readout(I, I_st, Q, Q_st, resonators=[1, 2, 3, 4], weights="rotated_")
            # Reset the frame of the qubit in order not to accumulate rotations
            # reset_frame("q1_xy")
            # reset_frame("q2_xy")
            # reset_frame("q3_xy")
            # reset_frame("q4_xy")

            wait(thermalization_time * u.ns)

        # Save the averaging iteration to get the progress bar
        save(n, n_st)

    with stream_processing():
        n_st.save("n")
        # resonator 1
        I_st[0].buffer(len(idle_times)).average().save("I1")
        Q_st[0].buffer(len(idle_times)).average().save("Q1")
        # resonator 2
        I_st[1].buffer(len(idle_times)).average().save("I2")
        Q_st[1].buffer(len(idle_times)).average().save("Q2")
        # resonator 3
        I_st[2].buffer(len(idle_times)).average().save("I3")
        Q_st[2].buffer(len(idle_times)).average().save("Q3")
        # resonator 4
        I_st[3].buffer(len(idle_times)).average().save("I4")
        Q_st[3].buffer(len(idle_times)).average().save("Q4")

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
        # plt.subplot(231)
        # plt.cla()
        # plt.plot(4 * idle_times, I1)
        # plt.ylabel("I quadrature [V]")
        # plt.title("Qubit 1")
        # plt.subplot(234)
        # plt.cla()
        # plt.plot(4 * idle_times, Q1)
        # plt.ylabel("Q quadrature [V]")
        # plt.xlabel("Idle times [ns]")
        # plt.subplot(232)
        # plt.cla()
        # plt.plot(4 * idle_times, I2)

        # plt.title("Qubit 2")
        # plt.subplot(235)
        # plt.cla()
        # plt.plot(4 * idle_times, Q2)
        # plt.title("Q2")
        # plt.xlabel("Idle times [ns]")

        plt.subplot(121)
        plt.cla()
        plt.plot(4 * idle_times, I3)
        plt.title("Qubit 3")
        plt.subplot(122)
        plt.cla()
        plt.plot(4 * idle_times, Q3)
        plt.title("Q3")
        plt.xlabel("Idle times [ns]")

        # plt.title("Qubit 4")
        # # plt.subplot(236)
        # plt.cla()
        # plt.plot(4 * idle_times, Q4)
        # plt.title("Q4")
        # plt.xlabel("Idle times [ns]")
        plt.tight_layout()
        plt.pause(0.1)
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    try:
        fit = Fit()
        plt.figure()
        plt.suptitle(f"Ramsey measurement with detuning={detuning} Hz")
        # plt.subplot(231)
        # fit.ramsey(4 * idle_times, I1, plot=True)
        # plt.xlabel("Idle times [ns]")
        # plt.ylabel("I quadrature [V]")
        # plt.title("Qubit 1")
        # plt.subplot(234)
        # fit.ramsey(4 * idle_times, Q1, plot=True)
        # plt.xlabel("Idle times [ns]")
        # plt.ylabel("I quadrature [V]")
        # plt.title("Qubit 2")
        # plt.subplot(232)
        # fit.ramsey(4 * idle_times, I2, plot=True)
        # plt.xlabel("Idle times [ns]")
        # plt.ylabel("I quadrature [V]")
        # plt.subplot(235)
        # fit.ramsey(4 * idle_times, Q2, plot=True)
        # plt.xlabel("Idle times [ns]")
        # plt.ylabel("I quadrature [V]")

        plt.subplot(121)
        fit.ramsey(4 * idle_times, I3, plot=True)
        plt.xlabel("Idle times [ns]")
        plt.ylabel("I quadrature [V]")
        plt.title("Qubit 3")
        plt.subplot(122)
        fit.ramsey(4 * idle_times, Q3, plot=True)
        plt.xlabel("Idle times [ns]")
        plt.ylabel("I quadrature [V]")

        # plt.subplot(121)
        # fit.ramsey(4 * idle_times, I4, plot=True)
        # plt.xlabel("Idle times [ns]")
        # plt.ylabel("I quadrature [V]")
        # plt.title("Qubit 4")
        # plt.subplot(122)
        # fit.ramsey(4 * idle_times, Q4, plot=True)
        # plt.xlabel("Idle times [ns]")
        # plt.ylabel("I quadrature [V]")

        plt.tight_layout()
        plt.show()
    except (Exception,):
        pass
