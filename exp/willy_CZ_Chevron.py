from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
from common_fitting_func import *
import numpy as np
from common_fitting_func import *
from macros import qua_declaration, multiplexed_readout
from qualang_tools.bakery import baking
import warnings
from qm import generate_qua_script
from common_fitting_func import *
warnings.filterwarnings("ignore")

# x = np.linspace(0,49,50)
# p = (1,5,1.5,20,0) 
# print(np.round(EERP(x,*p),3))
# eerp_up_wf = const_flux_amp*np.array(EERP(x,*p)[:10])
# eerp_dn_wf = eerp_up_wf[::-1]
# waveform = np.array([const_flux_amp] * const_flux_len)
# # print(np.round(eerp_up_wf,3))
# # print(np.round(eerp_dn_wf,3))
# # flat_wf = np.array([1.0] * 10)
# eerp_wf = np.concatenate((eerp_up_wf, waveform[:30], eerp_dn_wf))
# print(eerp_wf)
# plt.plot(x,eerp_wf,'-o')
# plt.show()



def baked_waveform(waveform, pulse_duration, flux_qubit, type, paras = None):
    pulse_segments = []
    if type == 'square':  
        for i in range(0, pulse_duration + 1):
            with baking(config, padding_method="symmetric_l") as b:
                if i == 0:  # Otherwise, the baking will be empty and will not be created
                    wf = [0.0] * 16
                else:
                    wf = waveform[:i].tolist()
                b.add_op("flux_pulse", f"q{flux_qubit}_z", wf)
                b.play("flux_pulse", f"q{flux_qubit}_z")
            pulse_segments.append(b)

    elif type == 'eerp':
        for i in range(0, pulse_duration + 1):
            p = [paras[0],paras[1],paras[2]]
            wf = EERP(*p,i).tolist()
            with baking(config, padding_method="symmetric_l") as b:
                b.add_op("flux_pulse", f"q{flux_qubit}_z", wf)
                b.play("flux_pulse", f"q{flux_qubit}_z")
            pulse_segments.append(b)
    return pulse_segments

def CZ_1ns(resonator,flux_Qi,amps,const_flux_len,simulate,qmm):
    with program() as cz:
        I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(resonator))
        a = declare(fixed)  
        segment = declare(int)  
        wait(flux_settle_time * u.ns)
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(a, amps)):
                with for_(segment, 0, segment <= const_flux_len, segment + 1):
                    if not simulate: wait(thermalization_time * u.ns)
                    if excited_Qi_list != []: 
                        for excited_Qi in excited_Qi_list:
                            play("x180", f"q{excited_Qi}_xy")
                    align()
                    wait(5)
                    with switch_(segment):
                        for j in range(0, const_flux_len + 1):
                            with case_(j):
                                pulse_segments[j].run(amp_array=[(f"q{flux_Qi}_z", a)])
                    align()
                    wait(5)
                    multiplexed_readout(I, I_st, Q, Q_st, resonators=resonator, weights="rotated_")
            save(n, n_st)
        with stream_processing():
            n_st.save("n")
            for i in resonator_index:
                I_st[i].buffer( len(amps),const_flux_len+1 ).average().save(f"I{i}")
                Q_st[i].buffer( len(amps),const_flux_len+1 ).average().save(f"Q{i}")
    if simulate:
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, cz, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(cz)
        fig = plt.figure()
        interrupt_on_close(fig, job)
        I_list, Q_list = [f"I{i}" for i in resonator_index], [f"Q{i}" for i in resonator_index]
        results = fetching_tool(job, I_list + Q_list + ["n"], mode="live")
        while results.is_processing():
            all_results = results.fetch_all()
            n = all_results[-1]
            I, Q = all_results[0:len(resonator)], all_results[len(resonator):len(resonator)*2]
            for i in resonator_index:
                I[i] = u.demod2volts(I[i], readout_len)
                Q[i] = u.demod2volts(Q[i], readout_len)            
            progress_counter(n, n_avg, start_time=results.start_time)
            live_plotting(I,Q)
        qm.close()
        plt.show()
        return I, Q
    

def live_plotting(I,Q):
    plt.suptitle(f"CZ chevron sweeping the flux on qubit {flux_Qi}")
    for i in range(len(resonator)):
        plt.subplot(2,2,i+1)
        plt.cla()
        plt.pcolor(amps * scale_reference, ts, I[i].transpose())
        plt.title(f"q{i} - I [V]")
        plt.ylabel("Interaction time (ns)")
        plt.subplot(2,2,i+3)
        plt.cla()
        plt.pcolor(amps * scale_reference, ts, Q[i].transpose())
        plt.title(f"q{i} - Q [V]")
        plt.ylabel("Interaction time (ns)")
        plt.xlabel("Flux amplitude (V)")       
        plt.tight_layout()
        plt.pause(0.1)

resonator = [2,3]   ###  [2,3] means measuring rr2 and rr3
resonator_index = [resonator.index(i) for i in resonator]
flux_Qi = 2  
excited_Qi_list = [2,3]
scale_reference = const_flux_amp 
type = 'eerp'
n_avg = 100  
amps = np.arange(0.31, 0.38, 0.001) 
const_flux_len = 200
flux_waveform = np.array([const_flux_amp] * const_flux_len)
edge_width = 10
sFactor = 6
pulse_segments = baked_waveform(flux_waveform, const_flux_len, flux_Qi, type, paras=[const_flux_amp,sFactor,edge_width])

simulate = False
ts = np.arange(0,const_flux_len+0.1,1)
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)      
I,Q = CZ_1ns(resonator,flux_Qi,amps,const_flux_len,simulate,qmm)