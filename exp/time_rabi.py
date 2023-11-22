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

def time_rabi(q_id,Qi,simulate,qmm):
    res_F = cosine_func( operation_flux_point[Qi-1], *g1[Qi-1])
    res_IF = (res_F - resonator_LO)/1e6
    res_IF = int(res_IF * u.MHz)
    with program() as rabi:
        I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(q_id))
        t = declare(int)  
        resonator_freq = declare(int, value=res_IF)
        for i in q_id:
            set_dc_offset(f"q{i+1}_z", "single", operation_flux_point[i])
        update_frequency(f"rr{Qi}", resonator_freq)
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(t, times)):
                play("x180", f"q{Qi}_xy", duration=t)
                align()
                multiplexed_readout(I, I_st, Q, Q_st, resonators=[x+1 for x in q_id], weights="rotated_")
                wait(thermalization_time * u.ns)
            save(n, n_st)

        with stream_processing():
            n_st.save("n")
            for i in q_id:
                I_st[q_id.index(i)].buffer(len(times)).average().save(f"I{i+1}")
                Q_st[q_id.index(i)].buffer(len(times)).average().save(f"Q{i+1}")
    if simulate:
        simulation_config = SimulationConfig(duration=10_000)  
        job = qmm.simulate(config, rabi, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(rabi)
        fig = plt.figure()
        interrupt_on_close(fig, job)
        I_list, Q_list = [f"I{i+1}" for i in q_id], [f"Q{i+1}" for i in q_id]
        results = fetching_tool(job, I_list + Q_list + ["n"], mode="live")
        while results.is_processing():
            all_results = results.fetch_all()
            n = all_results[-1]
            I, Q = all_results[0:len(q_id)], all_results[len(q_id):len(q_id)*2]
            for i in q_id:
                I[q_id.index(i)] = u.demod2volts(I[q_id.index(i)], readout_len)
                Q[q_id.index(i)] = u.demod2volts(Q[q_id.index(i)], readout_len)
            progress_counter(n, n_avg, start_time=results.start_time)
            live_plotting(I,Q,plot_index)    
        qm.close()
        plt.show()
        return I, Q

def live_plotting(I,Q,plot_index):
    plt.suptitle("Time Rabi \n number of average = " + str(n_avg))
    plt.subplot(121)
    plt.cla()
    plt.plot(4 * times, I[plot_index])
    plt.title(f"Qubit {Qi}")
    plt.xlabel("Qubit pulse duration [ns]")
    plt.ylabel("I quadrature [V]")
    plt.tight_layout()
    plt.subplot(122)
    plt.cla()
    plt.plot(4 * times, Q[plot_index])
    plt.title(f"Qubit {Qi}")
    plt.xlabel("Qubit pulse duration [ns]")
    plt.ylabel("Q quadrature [V]")
    plt.tight_layout()
    plt.pause(1.0)

def pi_length_fitting(I,Q,plot_index):
    try:
        from qualang_tools.plot.fitting import Fit
        fit = Fit()
        fit.rabi(4 * times, I[plot_index], plot=True)
        plt.xlabel("Qubit pulse duration [ns]")
        plt.ylabel("I quadrature [V]")
        plt.title(f"Qubit {Qi}")
        plt.show()
        plt.cla()
        fit.rabi(4 * times, Q[plot_index], plot=True)
        plt.xlabel("Qubit pulse duration [ns]")
        plt.ylabel("Q quadrature [V]")
        plt.title(f"Qubit {Qi}")
        plt.tight_layout()
        plt.show()
    except (Exception,):
        pass

times = np.arange(4, 200, 1)  
n_avg = 1000
q_id = [1,2,3,4]
Qi = 3
simulate = False
operation_flux_point = [0, -3.000e-01, -0.2525, -0.3433, -3.400e-01] 
for i in q_id: 
    if i == Qi-1: plot_index = q_id.index(i)  

qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
I,Q = time_rabi(q_id,Qi,simulate,qmm)
pi_length_fitting(I,Q,plot_index)