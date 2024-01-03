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

def ramsey_chevron(n_avg,q_id,Qi,dfs,operation_flux_point,t_delay,simulate):
    res_IF = []
    resonator_freq = [[] for _ in q_id]
    with program() as ramsey:
        I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(q_id))
        t = declare(int)  
        df = declare(int)        
        for i in q_id:
            res_F = cosine_func( operation_flux_point[i], *g1[i])
            res_F = (res_F - resonator_LO)/1e6
            res_IF.append(int(res_F * u.MHz))
            resonator_freq[q_id.index(i)] = declare(int, value=res_IF[q_id.index(i)])
            set_dc_offset(f"q{i+1}_z", "single", operation_flux_point[i])
            update_frequency(f"rr{i+1}", resonator_freq[q_id.index(i)])
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(df, dfs)):
                update_frequency(f"q{Qi}_xy", df + qubit_IF[Qi-1])    
                with for_(*from_array(t, t_delay)):
                    play("x90", f"q{Qi}_xy")
                    wait(t, f"q{Qi}_xy")
                    play("x90", f"q{Qi}_xy")
                    align()
                    multiplexed_readout(I, I_st, Q, Q_st, resonators=[x+1 for x in q_id], weights="rotated_")
                    wait(thermalization_time * u.ns)
            save(n, n_st)

        with stream_processing():
            n_st.save("n")
            for i in q_id:
                I_st[q_id.index(i)].buffer(len(t_delay)).buffer(len(dfs)).average().save(f"I{i+1}")
                Q_st[q_id.index(i)].buffer(len(t_delay)).buffer(len(dfs)).average().save(f"Q{i+1}")                
    if simulate:
        simulation_config = SimulationConfig(duration=10_000)  
        job = qmm.simulate(config, ramsey, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(ramsey)
        fig = plt.figure()
        interrupt_on_close(fig, job)
        I_list, Q_list = [f"I{i+1}" for i in q_id], [f"Q{i+1}" for i in q_id]
        results = fetching_tool(job, I_list + Q_list + ["n"], mode='live')
        while results.is_processing():
            all_results = results.fetch_all()
            n = all_results[-1]
            I, Q = all_results[0:len(q_id)], all_results[len(q_id):len(q_id)*2] 
            for i in q_id:
                I[q_id.index(i)] = u.demod2volts(I[q_id.index(i)], readout_len)
                Q[q_id.index(i)] = u.demod2volts(Q[q_id.index(i)], readout_len)
            progress_counter(n, n_avg, start_time=results.start_time)
            live_plotting(I[plot_index],Q[plot_index],Qi)
        qm.close()
        plt.show()
        return I[plot_index], Q[plot_index]
    
def live_plotting(I,Q,Qi):
    plt.suptitle("Ramsey chevron \n Number of average = " + str(n_avg))
    plt.subplot(121)
    plt.cla()
    plt.pcolor(4 * t_delay, dfs / u.MHz, I)
    plt.title(f"Qubit {Qi} I")
    plt.ylabel("Frequency detuning [MHz]")
    plt.axhline(y=0, color="k", ls="--", alpha=0.8, linewidth=3)
    plt.subplot(122)
    plt.cla()
    plt.pcolor(4 * t_delay, dfs / u.MHz, Q)
    plt.title(f"Qubit {Qi} Q")
    plt.xlabel("Idle time [ns]")
    plt.ylabel("Frequency detuning [MHz]")
    plt.tight_layout()
    plt.pause(0.1)

if __name__ == '__main__':
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
    simulate = False
    n_avg = 100  
    q_id = [1,2,3,4]
    dfs = np.arange(-1e6, 1e6, 0.01e6)  
    t_delay = np.arange(1, 500, 10) 
    Qi = 4
    for i in q_id: 
        if i == Qi-1: plot_index = q_id.index(i) 
    operation_flux_point = [0, -3.000e-01, -0.2525, -0.3433, -3.400e-01] 
    I,Q = ramsey_chevron(n_avg,q_id,Qi,dfs,operation_flux_point,t_delay,simulate)