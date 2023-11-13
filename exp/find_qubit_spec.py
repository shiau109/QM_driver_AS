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

q_id = [0,1,2,3]
Qi = 4
simulate = False

def flux_twotone_qubit(q_id, Qi, simulate):
    res_num = len(q_id)
    with program() as multi_qubit_spec_vs_flux:
        I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=res_num)
        df = declare(int)  
        dc = declare(fixed)  
        resonator_freq1 = declare(int, value=test)  
        index = declare(int, value=0) 

        with for_(n, 0, n < n_avg, n + 1):
            for i in q_id:
                set_dc_offset(f"q{i+1}_z", "single", operation_flux_point[i])
            with for_(*from_array(df, dfs)):
                update_frequency(f"q{Qi}_xy", df + qubit_IF[Qi-1])
                assign(index, 0)
                with for_(*from_array(dc, dcs)):
                    set_dc_offset(f"q{Qi}_z", "single", dc + operation_flux_point[Qi-1])
                    wait(flux_settle_time * u.ns) 
                    update_frequency(f"rr{Qi}", resonator_freq1[index])
                    play("saturation" * amp(saturation_amp), f"q{Qi}_xy", duration=saturation_len * u.ns)
                    multiplexed_readout(I, I_st, Q, Q_st, resonators=[1, 2, 3, 4], amplitude=0.9)
                    assign(index, index + 1)
            save(n, n_st)
        with stream_processing():
            n_st.save("n")
            for i in range(res_num):
                I_st[i].buffer(len(dcs)).buffer(len(dfs)).average().save(f"I{i+1}")
                Q_st[i].buffer(len(dcs)).buffer(len(dfs)).average().save(f"Q{i+1}")
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

    if simulate:
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, multi_qubit_spec_vs_flux, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(multi_qubit_spec_vs_flux)
        fig = plt.figure()
        interrupt_on_close(fig, job)

        I_list, Q_list = [f"I{i+1}" for i in range(res_num)], [f"Q{i+1}" for i in range(res_num)]
        results = fetching_tool(job, I_list + Q_list + ["n"], mode="live")

        while results.is_processing():
            all_results = results.fetch_all()
            n = all_results[-1]
            I, Q = all_results[0:res_num], all_results[res_num:res_num*2] 
            R = []
            phase = []
            for i in range(res_num):
                I[i] = u.demod2volts(I[i], readout_len)
                Q[i] = u.demod2volts(Q[i], readout_len)
                S = I[i] + 1j * Q[i]
                R.append(np.abs(S))
                phase.append(np.angle(S))

            progress_counter(n, n_avg, start_time=results.start_time)
            live_plotting(R,phase,Qi)
        
        qm.close()
        plt.show()

def live_plotting(R,phase,Qi):
    plt.suptitle("Qubit spectroscopy")
    plt.subplot(121)
    plt.cla()
    plt.pcolor(dcs, (qubit_IF[Qi-1] + dfs) / u.MHz, R[Qi-1])
    plt.xlabel("Flux bias [V]")
    plt.ylabel(f"q{Qi} IF [MHz]")
    plt.title(f"q{Qi} amp. (f: {(qubit_LO[Qi-1] + qubit_IF[Qi-1]) / u.MHz} MHz)")
    plt.subplot(122)
    plt.cla()
    plt.pcolor(dcs, (qubit_IF[Qi-1] + dfs) / u.MHz, phase[Qi-1])
    plt.xlabel("Flux bias [V]")
    plt.ylabel(f"q{Qi} IF [MHz]")
    plt.title(f"q{Qi} phase (f: {(qubit_LO[Qi-1] + qubit_IF[Qi-1]) / u.MHz} MHz)")
    plt.tight_layout()
    plt.pause(0.1)


flux_twotone_qubit(q_id,Qi,simulate)
