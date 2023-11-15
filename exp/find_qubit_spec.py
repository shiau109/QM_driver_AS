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

n_avg = 500  # The number of averages
# Adjust the pulse duration and amplitude to drive the qubit into a mixed state
saturation_len = 12 * u.us  # In ns
saturation_amp =  0.03  # pre-factor to the value defined in the config - restricted to [-2; 2)
# Qubit detuning sweep with respect to qubit_IF
dfs = np.arange(-350e6, +100e6, 0.1e6)
# Flux sweep
flux = np.arange(-0.1, 0.2, 0.01)
Qi = 3
operation_flux_point = [0, 4.000e-02, -3.100e-01, 4.000e-02] 
res_F = resonator_flux( flux + operation_flux_point[Qi-1], *p1[Qi-1])
res_IF = (res_F - resonator_LO)/1e6
res_IF_list = []

for IF in res_IF:
    res_IF_list.append(int(IF * u.MHz))  

q_id = [0,1,2,3]
simulate = False

def flux_twotone_qubit(q_id, Qi, simulate,qmm):
    res_num = len(q_id)
    with program() as multi_qubit_spec_vs_flux:
        I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=res_num)
        df = declare(int)  
        dc = declare(fixed)  
        resonator_freq1 = declare(int, value=res_IF_list)  
        index = declare(int, value=0) 

        with for_(n, 0, n < n_avg, n + 1):
            for i in q_id:
                set_dc_offset(f"q{i+1}_z", "single", operation_flux_point[i])
            with for_(*from_array(df, dfs)):
                update_frequency(f"q{Qi}_xy", df + qubit_IF[Qi-1])
                assign(index, 0)
                with for_(*from_array(dc, flux)):
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
                I_st[i].buffer(len(flux)).buffer(len(dfs)).average().save(f"I{i+1}")
                Q_st[i].buffer(len(flux)).buffer(len(dfs)).average().save(f"Q{i+1}")
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
                S = u.demod2volts(I[i] + 1j * Q[i], readout_len)
                R.append(np.abs(S))
                phase.append(np.angle(S))
            progress_counter(n, n_avg, start_time=results.start_time)
            live_plotting(R,phase,Qi)
        qm.close()
        plt.show()
        return I, Q
    
def live_plotting(R,phase,Qi):
    plt.suptitle("Qubit spectroscopy")
    plt.subplot(121)
    plt.cla()
    plt.pcolor(flux, (qubit_IF[Qi-1] + dfs) / u.MHz, R[Qi-1])
    plt.colorbar()
    plt.xlabel("Flux bias [V]")
    plt.ylabel(f"q{Qi} IF [MHz]")
    plt.title(f"q{Qi} amp. (f: {(qubit_LO[Qi-1] + qubit_IF[Qi-1]) / u.MHz} MHz)")
    plt.subplot(122)
    plt.cla()
    plt.pcolor(flux, (qubit_IF[Qi-1] + dfs) / u.MHz, phase[Qi-1])
    plt.colorbar()
    plt.xlabel("Flux bias [V]")
    plt.ylabel(f"q{Qi} IF [MHz]")
    plt.title(f"q{Qi} phase (f: {(qubit_LO[Qi-1] + qubit_IF[Qi-1]) / u.MHz} MHz)")
    plt.tight_layout()
    plt.pause(0.1)

def qubit_flux_fitting(I,Q,Qi):
    R = []
    phase = []
    Flux = np.zeros((len(q_id), len(flux)))
    Frequency = np.zeros((len(q_id), len(dfs)))
    min_index = [[] for _ in q_id]
    max_index = [[] for _ in q_id]
    res_F = [[] for _ in q_id]
    resonator_flux_params, resonator_flux_covariance = [], []   
    for i in q_id:
        Flux[i] = flux
        Frequency[i] = dfs + qubit_IF[i] + qubit_LO[i]
        S = I[i] + 1j * Q[i]
        R.append(np.abs(S))
        phase.append(np.angle(S))
        for j in range(len(Flux[i])):
            min_index[i].append(np.argmax(R[i][:,j])) 
            max_index[i].append(np.argmax(phase[i][:,j])) 

    plt.subplot(1, 2, 1)
    plt.cla()
    plt.title(f"q{Qi}:")
    plt.pcolor(Flux[Qi-1], Frequency[Qi-1], R[Qi-1])        
    plt.plot(Flux[Qi-1], Frequency[Qi-1][min_index[Qi-1]])
    plt.subplot(1, 2, 2)
    plt.cla()
    plt.title(f"q{Qi}:")
    plt.pcolor(Flux[Qi-1], Frequency[Qi-1], phase[Qi-1])        
    plt.plot(Flux[Qi-1], Frequency[Qi-1][max_index[Qi-1]])

    plt.plot(flux,flux_qubit_spec(flux,v_period=0.7,max_freq=(3.5235e9),max_flux=0.004,idle_freq=(3.2252e9),idle_flux=0.146,Ec=0.2e9))

    plt.tight_layout()
    plt.show()


qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
I, Q = flux_twotone_qubit(q_id,Qi,simulate,qmm)
qubit_flux_fitting(I,Q,Qi)

### Q3
# plt.plot(flux,flux_qubit_spec(flux,v_period=0.7,max_freq=(3.5235e9),max_flux=0.004,idle_freq=(3.2252e9),idle_flux=0.146,Ec=0.2e9))