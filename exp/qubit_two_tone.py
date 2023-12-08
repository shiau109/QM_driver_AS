from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from configuration import *
from qualang_tools.results import fetching_tool
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.loops import from_array
from qualang_tools.plot import interrupt_on_close
from scipy import signal
from macros import qua_declaration, multiplexed_readout, live_plotting
from common_fitting_func import *
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

from datetime import datetime
import sys

def qubit_two_tone(q_id,Qi,saturation_amp,simulate,qmm):
    with program() as multi_qubit_spec:
        I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(q_id))
        df = declare(int)  # QUA variable for the readout frequency
        resonator_freq = declare(int, value=res_IF)  
        for i in q_id:
            set_dc_offset(f"q{i+1}_z", "single", idle_flux_point[i])
        update_frequency(f"rr{Qi}", resonator_freq)
        # update_frequency(f"rr2", int((74.626) * u.MHz))
        wait(flux_settle_time * u.ns)   
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(df, dfs)):
                update_frequency(f"q{Qi}_xy", df + qubit_IF[Qi-1])
                play("saturation" * amp(saturation_amp), f"q{Qi}_xy", duration=saturation_len * u.ns)  
                align(f"q{Qi}_xy", f"rr{Qi}")
                multiplexed_readout(I, I_st, Q, Q_st, resonators=[x+1 for x in q_id], amplitude=0.99)
            save(n, n_st)
        with stream_processing():
            n_st.save("n")
            for i in q_id:
                I_st[q_id.index(i)].buffer(len(dfs)).average().save(f"I{i+1}")
                Q_st[q_id.index(i)].buffer(len(dfs)).average().save(f"Q{i+1}")

    if simulate:
        simulation_config = SimulationConfig(duration=10_000)  
        job = qmm.simulate(config, multi_qubit_spec, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(multi_qubit_spec)
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
                S = u.demod2volts(I[q_id.index(i)] + 1j * Q[q_id.index(i)], readout_len)
                R = np.abs(S)
                phase = np.angle(S)
                Frequency[q_id.index(i)] = dfs + qubit_IF[i] + qubit_LO[i]
                Amplitude[q_id.index(i)] = R
                Phase[q_id.index(i)] = signal.detrend(np.unwrap(phase))     
            progress_counter(n, n_avg, start_time=results.start_time)
            live_plotting(Amplitude,Phase,plot_index)    
        plt.show()      
        qm.close()


def live_plotting(Amplitude,Phase,plot_index):
    plt.suptitle("Qubit spectroscopy")
    plt.subplot(121)
    plt.cla()
    plt.plot(Frequency[plot_index], Amplitude[plot_index])
    plt.axvline(qubit_IF[Qi-1] + qubit_LO[Qi-1], color="k", linewidth=0.37)
    plt.xlabel("Qubit frequency [GHz]")
    plt.ylabel(r"$R=\sqrt{I^2 + Q^2}$ [V]")
    plt.title(f"q{Qi} amp. (f: {(qubit_LO[Qi-1] + qubit_IF[Qi-1]) / u.MHz} MHz)")
    plt.subplot(122)
    plt.cla()
    plt.plot(Frequency[plot_index], Phase[plot_index])
    plt.axvline(qubit_IF[Qi-1] + qubit_LO[Qi-1], color="k", linewidth=0.37)
    plt.xlabel("Qubit frequency [GHz]")
    plt.ylabel("Phase [rad]")
    plt.title(f"q{Qi} phase (f: {(qubit_LO[Qi-1] + qubit_IF[Qi-1]) / u.MHz} MHz)")
    plt.tight_layout()
    plt.pause(0.1)

q_id = [1,2,3,4]
Qi = 2
n_avg = 800
saturation_amp = 0.009
saturation_len = 20 * u.us  
dfs = np.arange(-100e6, 100e6, 0.05e6)
res_F = cosine_func( idle_flux_point[Qi-1], *g1[Qi-1])
res_IF = (res_F - resonator_LO)/1e6
res_IF = int(res_IF * u.MHz)
for i in q_id: 
    if i == Qi-1: plot_index = q_id.index(i)  
simulate = False
Frequency = np.zeros((len(q_id), len(dfs)))
Amplitude = np.zeros((len(q_id), len(dfs)))
Phase = np.zeros((len(q_id), len(dfs)))
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
qubit_two_tone(q_id,Qi,saturation_amp,simulate,qmm)
