from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from configuration import *
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.loops import from_array
from macros import qua_declaration, multiplexed_readout
import matplotlib.pyplot as plt
from scipy import signal
import warnings
from common_fitting_func import *
warnings.filterwarnings("ignore")

def flux_twotone_qubit(q_id, Qi, flux_Qi, flux, plot_index, simulate,qmm):
    ### The resonator freq will vary with flux
    if Qi == flux_Qi:
        res_F = cosine_func( flux + operation_flux_point[Qi-1], *g1[Qi-1])
        res_IF = (res_F - resonator_LO)/1e6
        res_IF_list = []
        for IF in res_IF:
            res_IF_list.append(int(IF * u.MHz)) 
    ### Assume the crosstalk too weak to influence other resonator freq
    else: 
        res_F = cosine_func( operation_flux_point[Qi-1], *g1[Qi-1])
        res_IF = (res_F - resonator_LO)/1e6
        res_IF = int(res_IF * u.MHz)
    with program() as multi_qubit_spec_vs_flux:
        I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(q_id))
        df = declare(int)  
        dc = declare(fixed)  
        if Qi == flux_Qi:
            resonator_freq = declare(int, value=res_IF_list)  
        else:
            resonator_freq = declare(int, value=res_IF) 
            update_frequency(f"rr{Qi}", resonator_freq)
        index = declare(int, value=0) 
        with for_(n, 0, n < n_avg, n + 1):
            for i in q_id:
                set_dc_offset(f"q{i+1}_z", "single", operation_flux_point[i])
            assign(index, 0)     
            with for_(*from_array(dc, flux)):
                set_dc_offset(f"q{flux_Qi}_z", "single", dc + operation_flux_point[flux_Qi-1])  
                ### Constantly varying resonator freq corresponding to the flux
                if Qi==flux_Qi: update_frequency(f"rr{Qi}", resonator_freq[index])                
                with for_(*from_array(df, dfs)):
                    update_frequency(f"q{Qi}_xy", df + qubit_IF[Qi-1]) 
                    wait(thermalization_time * u.ns) 
                    play("saturation" * amp(saturation_amp), f"q{Qi}_xy", duration=saturation_len * u.ns)
                    multiplexed_readout(I, I_st, Q, Q_st, resonators=[x+1 for x in q_id], amplitude=0.9)
                assign(index, index + 1)
            save(n, n_st)
        with stream_processing():
            n_st.save("n")
            for i in q_id:
                I_st[q_id.index(i)].buffer( len(flux),len(dfs) ).average().save(f"I{i+1}")
                Q_st[q_id.index(i)].buffer( len(flux),len(dfs) ).average().save(f"Q{i+1}")
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
        I_list, Q_list = [f"I{i+1}" for i in q_id], [f"Q{i+1}" for i in q_id]
        results = fetching_tool(job, I_list + Q_list + ["n"], mode="live")
        while results.is_processing():
            all_results = results.fetch_all()
            n = all_results[-1]
            I, Q = all_results[0:len(q_id)], all_results[len(q_id):len(q_id)*2]
            R = []
            phase = []
            for i in q_id:
                I[q_id.index(i)] = u.demod2volts(I[q_id.index(i)], readout_len)
                Q[q_id.index(i)] = u.demod2volts(Q[q_id.index(i)], readout_len)
                S = u.demod2volts(I[q_id.index(i)] + 1j * Q[q_id.index(i)], readout_len)
                R = np.abs(S)
                phase = np.angle(S)
                Flux[q_id.index(i)] = flux
                Frequency[q_id.index(i)] = dfs + resonator_IF[i] + resonator_LO
                Amplitude[q_id.index(i)] = R
                Phase[q_id.index(i)] = signal.detrend(np.unwrap(phase))
            progress_counter(n, n_avg, start_time=results.start_time)
            live_plotting(Amplitude,Phase,plot_index)
        qm.close()
        plt.show()
        return I, Q
    
def live_plotting(Amplitude,Phase,plot_index):
    plt.suptitle("Qubit spectroscopy")
    plt.subplot(221)
    plt.cla()
    plt.pcolor(flux, (qubit_IF[Qi-1] + dfs) / u.MHz, Amplitude[plot_index].transpose())
    plt.colorbar()
    plt.xlabel(f"qubit {flux_Qi} Flux bias [V]")
    plt.ylabel(f"q{Qi} IF [MHz]")
    plt.title(f"q{Qi} amp. (f: {(qubit_LO[Qi-1] + qubit_IF[Qi-1]) / u.MHz} MHz)")

    plt.subplot(222)
    plt.cla()
    plt.pcolor(flux, (qubit_IF[Qi-1] + dfs) / u.MHz, Phase[plot_index].transpose())
    plt.colorbar()
    plt.xlabel(f"qubit {flux_Qi} Flux bias [V]")
    plt.ylabel(f"q{Qi} IF [MHz]")
    plt.title(f"q{Qi} phase (f: {(qubit_LO[Qi-1] + qubit_IF[Qi-1]) / u.MHz} MHz)")
    plt.tight_layout()

    plt.subplot(223)
    plt.cla()
    plt.pcolor(flux, (qubit_IF[Qi-1] + dfs + qubit_LO[Qi-1])/ u.GHz, Amplitude[plot_index].transpose())
    plt.colorbar()
    plt.xlabel(f"qubit {flux_Qi} Flux bias [V]")
    plt.ylabel(f"q{Qi} [GHz]")

    plt.subplot(224)
    plt.cla()
    plt.pcolor(flux, (qubit_IF[Qi-1] + dfs + qubit_LO[Qi-1])/ u.GHz, Phase[plot_index].transpose())
    plt.colorbar()
    plt.xlabel(f"qubit {flux_Qi} Flux bias [V]")
    plt.ylabel(f"q{Qi} [GHz]")

    plt.pause(0.1)

def qubit_flux_fitting(I,Q,plot_index,fitting):
    R = []
    phase = []
    min_index = [[] for _ in q_id]
    max_index = [[] for _ in q_id]
    res_F = [[] for _ in q_id]
    resonator_flux_params, resonator_flux_covariance = [], []   
    for i in q_id:
        Flux[q_id.index(i)] = flux
        Frequency[q_id.index(i)] = dfs + qubit_IF[i] + qubit_LO[i]
        S = I[q_id.index(i)] + 1j * Q[q_id.index(i)]
        R.append(np.abs(S))
        phase.append(np.angle(S))
        for j in range(len(Flux[q_id.index(i)])):
            min_index[q_id.index(i)].append(np.argmax(R[q_id.index(i)][:,j])) 
            max_index[q_id.index(i)].append(np.argmax(phase[q_id.index(i)][:,j])) 
    amp_max_qubit_freq = max(Frequency[plot_index][min_index[plot_index]])
    amp_min_qubit_freq = min(Frequency[plot_index][min_index[plot_index]])
    amp_max_qubit_flux = Flux[plot_index][np.argmax(Frequency[plot_index][min_index[plot_index]])]
    amp_min_qubit_flux = Flux[plot_index][np.argmin(Frequency[plot_index][min_index[plot_index]])]

    phase_max_qubit_freq = max(Frequency[plot_index][max_index[plot_index]])
    phase_min_qubit_freq = min(Frequency[plot_index][max_index[plot_index]])
    phase_max_qubit_flux = Flux[plot_index][np.argmax(Frequency[plot_index][max_index[plot_index]])]
    phase_min_qubit_flux = Flux[plot_index][np.argmin(Frequency[plot_index][max_index[plot_index]])]
    v_period = np.abs(max_frequency_point[Qi-1] - min_frequency_point[Qi-1]) * 2
    plt.subplot(1, 2, 1)
    plt.cla()
    plt.title(f"q{Qi}:")
    plt.pcolor(Flux[plot_index], Frequency[plot_index], R[plot_index].transpose())        
    plt.plot(Flux[plot_index], Frequency[plot_index][min_index[plot_index]])
    print(f'amp_max qubit_freq: {amp_max_qubit_freq}')
    print(f'amp_max qubit_freq_flux: {amp_max_qubit_flux}')
    if fitting: plt.plot(flux,flux_qubit_spec(
        flux,
        v_period,
        max_freq = amp_max_qubit_freq,
        max_flux=amp_max_qubit_flux,
        idle_freq=amp_min_qubit_freq,
        idle_flux=amp_min_qubit_flux,
        Ec=0.196e9))
    plt.subplot(1, 2, 2)
    plt.cla()
    plt.title(f"q{Qi}:")
    plt.pcolor(Flux[plot_index], Frequency[plot_index], phase[plot_index].transpose())        
    plt.plot(Flux[plot_index], Frequency[plot_index][max_index[plot_index]])
    print(f'phase_max qubit_freq: {phase_max_qubit_freq}')
    print(f'phase_max qubit_freq_flux: {phase_max_qubit_flux}')
    if fitting: plt.plot(flux,flux_qubit_spec(
        flux,
        v_period,
        max_freq=phase_max_qubit_freq,
        max_flux=phase_max_qubit_flux,
        idle_freq=phase_min_qubit_freq,
        idle_flux=phase_min_qubit_flux,
        Ec=0.196e9))
    plt.tight_layout()
    plt.show()

n_avg = 100  
saturation_len = 12 * u.us  
saturation_amp =  0.05
q_id = [1,2,3,4]
Qi = 4
flux_Qi = 4
fitting = False
for i in q_id: 
    if i == Qi-1: plot_index = q_id.index(i)  
dfs = np.arange(-300e6, 50e6, 1e6)
flux = np.arange(-0.02, 0.25, 0.01)
Flux = np.zeros((len(q_id), len(flux)))
Frequency = np.zeros((len(q_id), len(dfs)))
Amplitude = np.zeros((len(q_id), len(flux), len(dfs)))
Phase = np.zeros((len(q_id), len(flux), len(dfs)))
operation_flux_point = [0, -3.000e-01, -0.2525, -0.3433, -3.400e-01] 
simulate = False
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
I, Q = flux_twotone_qubit(q_id,Qi,flux_Qi,flux,plot_index,simulate,qmm)
qubit_flux_fitting(I,Q,plot_index,fitting)

### Q3
# plt.plot(flux,flux_qubit_spec(flux,v_period=0.7,max_freq=(3.5235e9),max_flux=0.004,idle_freq=(3.2252e9),idle_flux=0.146,Ec=0.2e9))

### Q4
# plt.plot(flux,flux_qubit_spec(flux,v_period=0.72,max_freq=(3.8497e9),max_flux=-0.0204,idle_freq=(3.6507e9),idle_flux=0.0917,Ec=0.196e9))