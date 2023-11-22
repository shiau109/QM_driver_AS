"""
        QUBIT SPECTROSCOPY VERSUS FLUX
This sequence involves doing a qubit spectroscopy for several flux biases in order to exhibit the qubit frequency
versus flux response.

Prerequisites:
    - Identification of the resonator's resonance frequency when coupled to the qubit in question (referred to as "resonator_spectroscopy").
    - Calibration of the IQ mixer connected to the qubit drive line (whether it's an external mixer or an Octave port).
    - Having calibrated the resonator frequency versus flux fit parameters (amplitude_fit, frequency_fit, phase_fit, offset_fit) in the configuration
    - Identification of the approximate qubit frequency ("qubit_spectroscopy").

Before proceeding to the next node:
    - Update the qubit frequency, labeled as "qubit_IF_q", in the configuration.
    - Update the relevant flux points in the configuration.
"""

from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from configuration import *
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.loops import from_array
from macros import qua_declaration, multiplexed_readout
import matplotlib.pyplot as plt
import warnings
from common_fitting_func import *
warnings.filterwarnings("ignore")


# Get the resonator frequency vs flux trend from the node 05_resonator_spec_vs_flux.py in order to always measure on
# resonance while sweeping the flux
def cosine_func(x, amplitude, frequency, phase, offset):
    return amplitude * np.cos(2 * np.pi * frequency * x + phase) + offset


###################
# The QUA program #
###################
n_avg = 2000  # The number of averages
# Adjust the pulse duration and amplitude to drive the qubit into a mixed state
saturation_len = 12 * u.us  # In ns
saturation_amp = 0.1  # pre-factor to the value defined in the config - restricted to [-2; 2)
# Qubit detuning sweep with respect to qubit_IF
dfs = np.arange(-350e6, +200e6, 0.5e6)
# Flux sweep
dcs = np.arange(-0.1, 0.2, 0.01)

operation_flux_point = [-0.177, -0.132, -0.009, -3.300e-01] 
p = [[3.00000000e+06, 4.72437065e+00, 2.54347759e-01, 5.00000000e-01, 5.73269020e+09], 
     [2.99936983e+06, 4.76129330e+00, 1.36328981e-01, 4.69321121e-01, 6.02208429e+09],
     [2.14969791e+06, 4.64007989e+00, 2.57582926e-01, 3.46920235e-01, 5.84470816e+09], 
     [2.99946477e+06, 4.78859854e+00, 1.04511374e-01, 3.37195181e-01, 6.10992248e+09]]
res_F = resonator_flux( dcs + operation_flux_point[3], *p[3])
res_IF = (res_F - 5.95e9)/1e6
test = []
for IF in res_IF:
    test.append(int(IF * u.MHz))  

# plt.plot(dcs + operation_flux_point[3],res_F)
# plt.show()

# The fit parameters are take from the config
# fitted_curve1 = (cosine_func(dcs, amplitude_fit1, frequency_fit1, phase_fit1, offset_fit1)).astype(int)
# fitted_curve2 = (cosine_func(dcs, amplitude_fit2, frequency_fit2, phase_fit2, offset_fit2)).astype(int)

q_id = [0,1,2,3]
with program() as multi_qubit_spec_vs_flux:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=4)
    df = declare(int)  # QUA variable for the qubit detuning
    dc = declare(fixed)  # QUA variable for the flux bias
    resonator_freq1 = declare(int, value=test)  # res freq vs flux table
    index = declare(int, value=0)  # index to get the right resonator freq for a given flux

    with for_(n, 0, n < n_avg, n + 1):
        for i in q_id:
            set_dc_offset("q%s_z"%(i+1), "single", operation_flux_point[i])
        with for_(*from_array(df, dfs)):
            update_frequency("q4_xy", df + qubit_IF[3])
            assign(index, 0)
            with for_(*from_array(dc, dcs)):

                set_dc_offset("q4_z", "single", dc + operation_flux_point[3])
                wait(flux_settle_time * u.ns)  # Wait for the flux to settle
                # Update the resonator frequency to always measure on resonance
                update_frequency("rr4", resonator_freq1[index])

                # Saturate qubit
                play("saturation" * amp(saturation_amp), "q4_xy", duration=saturation_len * u.ns)

                # Multiplexed readout, also saves the measurement outcomes
                multiplexed_readout(I, I_st, Q, Q_st, resonators=[1, 2, 3, 4], amplitude=0.9)
                # Wait for the qubit to decay to the ground state
                # wait(thermalization_time * u.ns)
                # Update the resonator frequency vs flux index
                assign(index, index + 1)
        # Save the averaging iteration to get the progress bar
        save(n, n_st)

    with stream_processing():
        n_st.save("n")
        # resonator 1
        I_st[0].buffer(len(dcs)).buffer(len(dfs)).average().save("I1")
        Q_st[0].buffer(len(dcs)).buffer(len(dfs)).average().save("Q1")
        # resonator 2
        I_st[1].buffer(len(dcs)).buffer(len(dfs)).average().save("I2")
        Q_st[1].buffer(len(dcs)).buffer(len(dfs)).average().save("Q2")
        # resonator 3
        I_st[2].buffer(len(dcs)).buffer(len(dfs)).average().save("I3")
        Q_st[2].buffer(len(dcs)).buffer(len(dfs)).average().save("Q3")
        # resonator 4
        I_st[3].buffer(len(dcs)).buffer(len(dfs)).average().save("I4")
        Q_st[3].buffer(len(dcs)).buffer(len(dfs)).average().save("Q4")

#####################################
#  Open Communication with the QOP  #
#####################################
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

###########################
# Run or Simulate Program #
###########################

simulate = True

if simulate:
    # Simulates the QUA program for the specified duration
    simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
    job = qmm.simulate(config, multi_qubit_spec_vs_flux, simulation_config)
    job.get_simulated_samples().con1.plot()
    plt.show()
else:
    # Open a quantum machine to execute the QUA program
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(multi_qubit_spec_vs_flux)
    # Prepare the figure for live plotting
    fig = plt.figure()
    interrupt_on_close(fig, job)
    # Tool to easily fetch results from the OPX (results_handle used in it)
    results = fetching_tool(job, ["n", "I1", "Q1", "I2", "Q2", "I3", "Q3", "I4", "Q4"], mode="live")
    # Live plotting
    while results.is_processing():
        # Fetch results
        n, I1, Q1, I2, Q2, I3, Q3, I4, Q4  = results.fetch_all()
        # Progress bar
        progress_counter(n, n_avg, start_time=results.start_time)
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
        plt.suptitle("Qubit spectroscopy")
        # plt.subplot(241)
        # plt.cla()
        # plt.pcolor(dcs, (qubit_IF[0] + dfs) / u.MHz, R1)
        # plt.xlabel("Flux bias [V]")
        # plt.ylabel("q1 IF [MHz]")
        # plt.title(f"q1 (f_res: {(qubit_LO_q1 + qubit_IF[0]) / u.MHz} MHz)")
        # plt.subplot(225)
        # plt.cla()
        # plt.pcolor(dcs, (qubit_IF[1] + dfs) / u.MHz, phase1)
        # plt.xlabel("Flux bias [V]")
        # plt.ylabel("q1 IF [MHz]")
        # plt.subplot(242)
        # plt.cla()
        # plt.pcolor(dcs, (qubit_IF[1] + dfs) / u.MHz, R2)
        # plt.title(f"q2 (f_res: {(qubit_LO_q2 + qubit_IF[1]) / u.MHz} MHz)")
        # plt.xlabel("Flux bias [V]")
        # plt.ylabel("q2 IF [MHz]")
        # plt.subplot(246)
        # plt.cla()
        # plt.pcolor(dcs, (qubit_IF[1] + dfs) / u.MHz, phase2)
        # plt.xlabel("Flux bias [V]")
        # plt.ylabel("q2 IF [MHz]")

        plt.subplot(243)
        plt.cla()
        plt.pcolor(dcs, (qubit_IF[2] + dfs) / u.MHz, R3)
        plt.xlabel("Flux bias [V]")
        plt.ylabel("q3 IF [MHz]")
        plt.title(f"q3 (f_res: {(qubit_LO[2] + qubit_IF[2]) / u.MHz} MHz)")
        plt.subplot(247)
        plt.cla()
        plt.pcolor(dcs, (qubit_IF[2] + dfs) / u.MHz, phase3)
        plt.xlabel("Flux bias [V]")
        plt.ylabel("q3 IF [MHz]")

        plt.subplot(244)
        plt.cla()
        plt.pcolor(dcs, (qubit_IF[3] + dfs) / u.MHz, R4)
        plt.xlabel("Flux bias [V]")
        plt.ylabel("q4 IF [MHz]")
        plt.title(f"q4 (f_res: {(qubit_LO[3] + qubit_IF[3]) / u.MHz} MHz)")
        plt.subplot(248)
        plt.cla()
        plt.pcolor(dcs, (qubit_IF[3] + dfs) / u.MHz, phase4)
        plt.xlabel("Flux bias [V]")
        plt.ylabel("q4 IF [MHz]")

        plt.tight_layout()
        plt.pause(0.1)
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    plt.show()
