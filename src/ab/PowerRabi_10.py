"""
        POWER RABI WITH ERROR AMPLIFICATION
This sequence involves repeatedly executing the qubit pulse (such as x180, square_pi, or similar) 'N' times and
measuring the state of the resonator across different qubit pulse amplitudes and number of pulses.
By doing so, the effect of amplitude inaccuracies is amplified, enabling a more precise measurement of the pi pulse
amplitude. The results are then analyzed to determine the qubit pulse amplitude suitable for the selected duration.

Prerequisites:
    - Having found the resonance frequency of the resonator coupled to the qubit under study (resonator_spectroscopy).
    - Having calibrated the IQ mixer connected to the qubit drive line (external mixer or Octave port)
    - Having found the rough qubit frequency and pi pulse duration (rabi_chevron_duration or time_rabi).
    - Having found the pi pulse amplitude (power_rabi).
    - Set the qubit frequency, desired pi pulse duration and rough pi pulse amplitude in the configuration.
    - Set the desired flux bias

Next steps before going to the next node:
    - Update the qubit pulse amplitude (pi_amp_q) in the configuration.
"""

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
# from configuration import *
from qualang_tools.loops import from_array
# from macros import qua_declaration, multiplexed_readout, live_plotting
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
n_avg = 20  # The number of averages

q_id = [0,1]

# Pulse amplitude sweep (as a pre-factor of the qubit pulse amplitude) - must be within [-2; 2)
amps = np.arange(0, 2, 0.01)

# # Tune flux and neighboring qubits
# flux_id = 0
# flux_offset = np.zeros(5)
# flux_offset[flux_id] = max_frequency_point[flux_id]
# detune_neighbor = True
# if detune_neighbor == True:
#     if flux_id != 0: flux_offset[flux_id-1] = detune_point[flux_id-1]
#     if flux_id != 4: flux_offset[flux_id+1] = detune_point[flux_id+1]

# Number of applied Rabi pulses sweep
max_nb_of_pulses = 24  # Maximum number of qubit pulses
if max_nb_of_pulses == 2: dimension = 1
else: dimension = 2
nb_of_pulses = np.arange(1, max_nb_of_pulses, 1)  # Always play an odd/even number of pulses to end up in the same state

with program() as rabi:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(q_id))
    a = declare(fixed)  # QUA variable for the qubit drive amplitude pre-factor
    npi = declare(int)  # QUA variable for the number of qubit pulses
    count = declare(int)  # QUA variable for counting the qubit pulses

    for i in [0,1,2,3]:
        # set_dc_offset(f"q{i+1}_z", "single", flux_offset[i])
        set_dc_offset(f"q{i+1}_z", "single", max_frequency_point[i])

    with for_(n, 0, n < n_avg, n + 1):
        with for_(*from_array(npi, nb_of_pulses)):
            with for_(*from_array(a, amps)):
                # Loop for error amplification (perform many qubit pulses)
                with for_(count, 0, count < npi, count + 1):
                    # play("x180" * amp(a), f"q{flux_id+1}_xy")

                    # for i in q_id:
                    #     play("x180" * amp(a), f"q{i+1}_xy")

                    j = 1
                    play("x180" * amp(a), f"q{j+1}_xy")

                # Align the elements to measure after playing the qubit pulses.
                align()
                # Start using Rotated integration weights (cf. IQ_blobs.py)
                multiplexed_readout(I, I_st, Q, Q_st, resonators=[1,2], weights="rotated_", amplitude=0.9)
                # Wait for the qubit to decay to the ground state
                wait(thermalization_time * u.ns)
        # Save the averaging iteration to get the progress bar
        save(n, n_st)

    with stream_processing():
        n_st.save("n")
        for i in q_id:
            I_st[i].buffer(len(amps)).buffer(len(nb_of_pulses)).average().save(f"I{i+1}")
            Q_st[i].buffer(len(amps)).buffer(len(nb_of_pulses)).average().save(f"Q{i+1}")

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
    
    live_plotting(n_avg, q_id, job, amps, nb_of_pulses, 
                     f"Power Rabi", 
                     save_data, save_path, stage="10a", normalize=False, dimension=dimension)

    qm.close()
