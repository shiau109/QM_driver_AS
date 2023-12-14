"""
        RESONATOR SPECTROSCOPY VERSUS FLUX
This sequence involves measuring the resonator by sending a readout pulse and demodulating the signals to
extract the 'I' and 'Q' quadratures. This is done across various readout intermediate frequencies and flux biases.
The resonator frequency as a function of flux bias is then extracted and fitted so that the parameters can be stored in the configuration.

This information can then be used to adjust the readout frequency for the maximum frequency point.

Prerequisites:
    - Calibration of the time of flight, offsets, and gains (referenced as "time_of_flight").
    - Calibration of the IQ mixer connected to the readout line (be it an external mixer or an Octave port).
    - Identification of the resonator's resonance frequency (referred to as "resonator_spectroscopy_multiplexed").
    - Configuration of the readout pulse amplitude and duration.
    - Specification of the expected resonator depletion time in the configuration.

Before proceeding to the next node:
    - Update the readout frequency, labeled as "resonator_IF", in the configuration.
    - Adjust the flux bias to the maximum frequency point, labeled as "max_frequency_point", in the configuration.
    - Update the resonator frequency versus flux fit parameters (amplitude_fit, frequency_fit, phase_fit, offset_fit) in the configuration
"""

from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from configuration import *
from qualang_tools.loops import from_array
from macros import qua_declaration, multiplexed_readout, live_plotting
import matplotlib.pyplot as plt
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
q_id = [0,1,2,3,4]


n_avg = 100
# The frequency sweep around the resonators' frequency "resonator_IF_q"
span = 5.0 * u.MHz
df = 100 * u.kHz
dfs = np.arange(-5 * u.MHz, 5 * u.MHz, df)
# Flux bias sweep in V
flux_min = -0.45
flux_max = 0.45
step = 0.02
flux = np.arange(flux_min, flux_max + step / 2, step)

flux_id = 0
flux_offset = np.zeros(5)
flux_offset[flux_id] = max_frequency_point[flux_id]

detune_neighbor = True
if detune_neighbor == False:
    if flux_id != 0: flux_offset[flux_id-1] = detune_point[flux_id-1]
    if flux_id != 4: flux_offset[flux_id+1] = detune_point[flux_id+1]

with program() as multi_res_spec_vs_flux:
    # QUA macro to declare the measurement variables and their corresponding streams for a given number of resonators
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(q_id))
    df = declare(int)  # QUA variable for sweeping the readout frequency detuning around the resonance
    dc = declare(fixed)  # QUA variable for sweeping the flux bias

    with for_(n, 0, n < n_avg, n + 1):
        with for_(*from_array(df, dfs)):
            for i in q_id:
                update_frequency("rr%s"%(i+1), df + resonator_IF[i])
            for i in [0,1,2,3]:            
                set_dc_offset(f"q{i+1}_z", "single", flux_offset[i])

            with for_(*from_array(dc, flux)):
                set_dc_offset(f"q{flux_id+1}_z", "single", dc+flux_offset[flux_id])
                for j in [0,1,2,3]:
                    set_dc_offset(f"q{j+1}_z", "single", dc+max_frequency_point[j])
                
                wait(flux_settle_time * u.ns)  
                multiplexed_readout(I, I_st, Q, Q_st, resonators=[x+1 for x in q_id], sequential=False)
                wait(depletion_time * u.ns, ["rr%s"%(i+1) for i in q_id]) # wait for the resonators to relax
        save(n, n_st)

    with stream_processing():
        n_st.save("n")
        for i in q_id:
            I_st[q_id.index(i)].buffer(len(flux)).buffer(len(dfs)).average().save("I%s"%(i+1))
            Q_st[q_id.index(i)].buffer(len(flux)).buffer(len(dfs)).average().save("Q%s"%(i+1))
        
#####################################
#  Open Communication with the QOP  #
#####################################
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

#######################
# Simulate or execute #
#######################
simulate = False

if simulate:
    simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
    job = qmm.simulate(config, multi_res_spec_vs_flux, simulation_config)
    job.get_simulated_samples().con1.plot()
    plt.show()
else:
    qm = qmm.open_qm(config)
    job = qm.execute(multi_res_spec_vs_flux)

    live_plotting(n_avg, q_id, job, flux, dfs, 
                     f"Flux dep. Resonator spectroscopy \n sweep q{flux_id+1}, detune neighbor = {detune_neighbor} \n", 
                     save_data, save_path, stage="6b", normalize=False)

    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()

    
