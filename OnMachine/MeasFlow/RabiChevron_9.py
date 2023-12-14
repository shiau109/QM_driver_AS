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
from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from macros import qua_declaration, multiplexed_readout, live_plotting
import warnings

warnings.filterwarnings("ignore")

###################
#   Data Saving   #
###################
from datetime import datetime
import sys

save_data = False  # Default = False in configur/ation file
save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
save_time = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
save_path = f"{save_dir}\{save_time}_{save_progam_name}"

###################
# The QUA program #
###################
n_avg = 100  # The number of averages
# Qubit detuning sweep with respect to qubit_IF
dfs = np.arange(-20e6, +20e6, 0.5e6)
# Qubit pulse amplitude sweep (as a pre-factor of the qubit pulse amplitude) - must be within [-2; 2)
amps = np.arange(0.0, 1.5, 0.01)

q_id = [0]

# # Tune flux and neighboring qubits
# flux_id = 0
# flux_offset = np.zeros(5)
# flux_offset[flux_id] = max_frequency_point[flux_id]
# detune_neighbor = True
# if detune_neighbor == True:
#     if flux_id != 0: flux_offset[flux_id-1] = detune_point[flux_id-1]
#     if flux_id != 4: flux_offset[flux_id+1] = detune_point[flux_id+1]



with program() as rabi_chevron:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(q_id))
    df = declare(int)  # QUA variable for the qubit detuning
    a = declare(fixed)  # QUA variable for the qubit pulse amplitude pre-factor

    for i in [0,1,2,3]:
        # set_dc_offset(f"q{i+1}_z", "single", flux_offset[i])
        set_dc_offset(f"q{i+1}_z", "single", max_frequency_point[i])

    with for_(n, 0, n < n_avg, n + 1):
        with for_(*from_array(df, dfs)):
            # Update the frequency of the two qubit elements
            # update_frequency(f"q{flux_id+1}_xy", df + qubit_IF[flux_id])
            for i in q_id:
                update_frequency(f"q{i+1}_xy", df + qubit_IF[i])

            with for_(*from_array(a, amps)):
                # Play qubit pulse
                # play("x180" * amp(a), f"q{flux_id+1}_xy")
                for i in q_id:
                    play("x180" * amp(a), f"q{i+1}_xy")
                # play("x180" * amp(a), "q2_xy")
                # Measure after the qubit pulse
                align()
                # Multiplexed readout, also saves the measurement outcomes
                multiplexed_readout(I, I_st, Q, Q_st, resonators=[1], weights="rotated_", amplitude=0.9)
                # Wait for the qubit to decay to the ground state
                wait(thermalization_time * u.ns)
        # Save the averaging iteration to get the progress bar
        save(n, n_st)

    with stream_processing():
        n_st.save("n")
        for i, qid in enumerate(q_id):
            I_st[i].buffer(len(amps)).buffer(len(dfs)).average().save(f"I{qid+1}")
            Q_st[i].buffer(len(amps)).buffer(len(dfs)).average().save(f"Q{qid+1}")



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
    qm = qmm.open_qm(config)
    job = qm.execute(rabi_chevron)

    live_plotting(n_avg, q_id, job, amps, dfs, 
                     f"Rabi chevron", 
                     save_data, save_path, stage="9", normalize=False, dimension=2)
    
    qm.close()
