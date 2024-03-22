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
from cosine import Cosine

warnings.filterwarnings("ignore")

def baked_waveform(pulse_duration, flux_qubit, type, paras = None):
    pulse_segments = []
    if type == 'square':
        waveform = np.array([const_flux_amp] * const_flux_len)
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
            wf = EERP(*paras,i).tolist()
            with baking(config, padding_method="symmetric_l") as b:
                b.add_op("flux_pulse", f"q{flux_qubit}_z", wf)
                b.play("flux_pulse", f"q{flux_qubit}_z")
            pulse_segments.append(b)
    return pulse_segments

def CZ_phase_compensate(flux_Qi,ramsey_Qi,Phi,simulate,qmm):

    with program() as cz_phase_compensate:
        ## _c means comparation
        I = [declare(fixed) for i in range(len(resonator))]
        Q = [declare(fixed) for i in range(len(resonator))] 
        I_c = [declare(fixed) for i in range(len(resonator))]
        Q_c = [declare(fixed) for i in range(len(resonator))] 
        I_st = [declare_stream() for i in range(len(resonator))]
        Q_st = [declare_stream() for i in range(len(resonator))]
        I_st_c = [declare_stream() for i in range(len(resonator))]
        Q_st_c = [declare_stream() for i in range(len(resonator))]  
        n = declare(int)
        n_st = declare_stream()      
        phi = declare(fixed)
        wait(flux_settle_time * u.ns)
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(phi, Phi)):
                ###  With CZ flux
                if not simulate: wait(thermalization_time * u.ns)
                play("x90", f"q{ramsey_Qi}_xy")
                align()
                ## This +1 is inserted because of making const_flux_len equal to actual pulse duration 
                wait(5)  
                pulse_segments[cz_sqr_len+1].run(amp_array=[(f"q{flux_Qi}_z", a)])   
                align()
                wait(5)  
                frame_rotation_2pi(phi, f"q{ramsey_Qi}_xy")
                play("x90", f"q{ramsey_Qi}_xy")
                wait(flux_settle_time * u.ns)
                align()
                multiplexed_readout(I, I_st, Q, Q_st, resonators=resonator, weights="rotated_")

                ###  Without CZ flux
                if not simulate: wait(thermalization_time * u.ns)
                play("x90", f"q{ramsey_Qi}_xy")
                align()
                wait(5) 
                ## This +1 is inserted because of making const_flux_len equal to actual pulse duration  
                pulse_segments[cz_sqr_len+1].run(amp_array=[(f"q{flux_Qi}_z", 0)])   
                align()
                wait(5)  
                frame_rotation_2pi(phi, f"q{ramsey_Qi}_xy")
                play("x90", f"q{ramsey_Qi}_xy")
                wait(flux_settle_time * u.ns)
                align()
                multiplexed_readout(I_c, I_st_c, Q_c, Q_st_c, resonators=resonator, weights="rotated_")
            save(n, n_st)
        with stream_processing():
            n_st.save("n")
            for i in resonator_index:
                I_st[i].buffer(len(Phi)).average().save(f"I{i}")
                I_st_c[i].buffer(len(Phi)).average().save(f"I_c{i}")
    if simulate:
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, cz_phase_compensate, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(cz_phase_compensate)
        fig = plt.figure()
        interrupt_on_close(fig, job)
        I_list, I_c_list = [f"I{i}" for i in resonator_index], [f"I_c{i}" for i in resonator_index]
        results = fetching_tool(job, I_list + I_c_list + ["n"], mode="live")
        while results.is_processing():
            all_results = results.fetch_all()
            n = all_results[-1]
            I, I_c = all_results[0:len(resonator)], all_results[len(resonator):len(resonator)*2]
            for i in resonator_index:
                I[i] = u.demod2volts(I[i], readout_len)
                I_c[i] = u.demod2volts(I_c[i], readout_len)
            progress_counter(n, n_avg, start_time=results.start_time)
            live_plotting(I,I_c)
        qm.close()
        plt.show()
        return I, I_c
    

def live_plotting(signal,signal_c):

    plt.cla()
    plt.plot(Phi, signal[plot_index], '.b', Phi, signal_c[plot_index], '.r')
    try:
        fit = Cosine(Phi, signal[plot_index], plot=False)
        phase = fit.out.get('phase')[0]
        plt.plot(fit.x_data, fit.fit_type(fit.x, fit.popt) * fit.y_normal, '-b', alpha=0.5, label='with CZ pulse')
        fit = Cosine(Phi, signal_c[plot_index], plot=False)
        phase_c = fit.out.get('phase')[0]
        plt.plot(fit.x_data, fit.fit_type(fit.x, fit.popt) * fit.y_normal, '-r', alpha=0.5, label='without CZ pulse')
        dphase = (phase-phase_c)/np.pi*180     
    except Exception as e: print(e) 
    plt.title(f"CZ phase difference at q{ramsey_Qi}, phase diff: {dphase:.3f}")  
    plt.legend()
    plt.tight_layout()
    plt.pause(0.1)

resonator = [2,3]   ###  [2,3] means measuring rr2 and rr3
resonator_index = [resonator.index(i) for i in resonator]
flux_Qi = resonator[0]  
ramsey_Qi = resonator[1]  
plot_index = resonator.index(ramsey_Qi)  ### related to resonator_index
type = 'square'
n_avg = 2000  
Phi = np.arange(0, 5, 0.05) # 5 rotations
a = cz_sqr_amp/const_flux_amp
edge_width = 10
edge_sigma = 6
paras = [cz_eerp_amp,edge_sigma,edge_width]
pulse_segments = baked_waveform(const_flux_len, flux_Qi, type, paras=paras)

simulate = False
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)      
I, I_c = CZ_phase_compensate(flux_Qi,ramsey_Qi,Phi,simulate,qmm)



# Q2 -42.070  Q3 -327.584