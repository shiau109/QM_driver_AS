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
    res_num = len(q_id)
    res_F = resonator_flux( operation_flux_point[Qi-1], *p1[Qi-1])
    res_IF = (res_F - resonator_LO)/1e6
    res_IF = int(res_IF * u.MHz)
    with program() as ramsey:
        I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=res_num)
        t = declare(int)  
        df = declare(int)  
        resonator_freq = declare(int, value=res_IF)
        for i in q_id:
            set_dc_offset(f"q{i+1}_z", "single", operation_flux_point[i])
        update_frequency(f"rr{Qi}", resonator_freq)
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(df, dfs)):
                update_frequency(f"q{Qi}_xy", df + qubit_IF[Qi-1])    
                with for_(*from_array(t, t_delay)):
                    play("x90", f"q{Qi}_xy")
                    wait(t, "q4_xy")
                    play("x90", f"q{Qi}_xy")
                    align()
                    multiplexed_readout(I, I_st, Q, Q_st, resonators=[1, 2, 3, 4], weights="rotated_")
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
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(ramsey)
        fig = plt.figure()
        interrupt_on_close(fig, job)
        I_list, Q_list = [f"I{i+1}" for i in range(res_num)], [f"Q{i+1}" for i in range(res_num)]
        results = fetching_tool(job, I_list + Q_list + ["n"], mode="live")
        while results.is_processing():

            all_results = results.fetch_all()
            n = all_results[-1]
            I, Q = all_results[0:res_num], all_results[res_num:res_num*2] 
            for i in range(res_num):
                I[i] = u.demod2volts(I[i], readout_len)
                Q[i] = u.demod2volts(Q[i], readout_len)
            progress_counter(n, n_avg, start_time=results.start_time)
            live_plotting(I,Q,Qi)
        qm.close()
        plt.show()
        return I, Q
    
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

qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
simulate = False
n_avg = 1000  
q_id = [0,1,2,3]
dfs = np.arange(-1e6, 1e6, 0.05e6)  
t_delay = np.arange(1, 200, 4) 
Qi = 4
operation_flux_point = [0, 4.000e-02, 4.000e-02, -3.200e-01] 
I,Q = ramsey_chevron(n_avg,q_id,Qi,dfs,operation_flux_point,t_delay,simulate)