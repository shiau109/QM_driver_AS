from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *

from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.plot import interrupt_on_close
from qualang_tools.units import unit
from common_fitting_func import *
import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import os, fnmatch

from macros import multiplexed_readout
from cosine import Cosine

def cz_gate(type, idle_flux_point, flux_Qi):
    if type == "square":
        wait(5)  # for flux pulse to relax back completely
        set_dc_offset(f"q{flux_Qi}_z", "single", idle_flux_point[flux_Qi-1] + 0.1753) 
        wait(28 // 4, f"q{flux_Qi}_z")
        align()
        set_dc_offset(f"q{flux_Qi}_z", "single", idle_flux_point[flux_Qi-1])
        wait(5)  # for flux pulse to relax back completely
    elif type == "ft_gaussian":
        play("cz_1_2"*amp((0.150-max_frequency_point[1])/(cz_point_1_2_q2-idle_q2)), "q2_z", duration=80//4)
    elif type == "gaussian":
        play("cz_1_2"*amp(1.4), "q2_z", duration=32//4)

def CZ_phase_diff(q_id,flux_Qi,control_Qi,ramsey_Qi,idle_flux_point,simulate,qmm):
    res_IF = []
    resonator_freq = [[] for _ in q_id]
    with program() as cz_ops:
        I_g = [declare(fixed) for i in range(len(q_id))]
        Q_g = [declare(fixed) for i in range(len(q_id))] 
        I_e = [declare(fixed) for i in range(len(q_id))]
        Q_e = [declare(fixed) for i in range(len(q_id))] 
        I_st_g = [declare_stream() for i in range(len(q_id))]
        Q_st_g = [declare_stream() for i in range(len(q_id))]
        I_st_e = [declare_stream() for i in range(len(q_id))]
        Q_st_e = [declare_stream() for i in range(len(q_id))]
        n = declare(int)
        n_st = declare_stream()
        phi = declare(fixed)
        for i in q_id:
            res_F = cosine_func( idle_flux_point[i], *g1[i])
            res_F = (res_F - resonator_LO)/1e6
            res_IF.append(int(res_F * u.MHz))
            resonator_freq[q_id.index(i)] = declare(int, value=res_IF[q_id.index(i)])
            set_dc_offset(f"q{i+1}_z", "single", idle_flux_point[i])
            update_frequency(f"rr{i+1}", resonator_freq[q_id.index(i)])
        wait(flux_settle_time * u.ns)
        with for_(n, 0, n < n_avg, n+1):
            with for_(*from_array(phi, Phi)):
                wait(thermalization_time * u.ns, f"q{control_Qi}_z")
                align()
                play("x90", f"q{ramsey_Qi}_xy")
                align()
                cz_gate(cz_type,idle_flux_point,flux_Qi)
                align()
                frame_rotation_2pi(phi, f"q{ramsey_Qi}_xy")
                play("x90", f"q{ramsey_Qi}_xy")
                align()
                multiplexed_readout(I_g, I_st_g, Q_g, Q_st_g, resonators=[x+1 for x in q_id], weights="rotated_")
                
                align()

                wait(thermalization_time * u.ns, f"q{control_Qi}_z")
                align()
                play("x180", f"q{control_Qi}_xy")
                play("x90", f"q{ramsey_Qi}_xy")
                align()
                cz_gate(cz_type,idle_flux_point,flux_Qi)
                align()
                frame_rotation_2pi(phi, f"q{ramsey_Qi}_xy")
                play("x90", f"q{ramsey_Qi}_xy")
                align()
                multiplexed_readout(I_e, I_st_e, Q_e, Q_st_e, resonators=[x+1 for x in q_id], weights="rotated_")
            save(n, n_st)  
                  
        with stream_processing():
            n_st.save('n')
            for i in q_id:
                I_st_g[q_id.index(i)].buffer(len(Phi)).average().save(f"I{i+1}g")
                Q_st_g[q_id.index(i)].buffer(len(Phi)).average().save(f"Q{i+1}g")  
                I_st_e[q_id.index(i)].buffer(len(Phi)).average().save(f"I{i+1}e")
                Q_st_e[q_id.index(i)].buffer(len(Phi)).average().save(f"Q{i+1}e")
    if simulate:
        job = qmm.simulate(config, cz_ops, SimulationConfig(15000))
        job.get_simulated_samples().con1.plot()
        plt.show()    
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(cz_ops)
        fig = plt.figure()
        interrupt_on_close(fig, job)
        Ig_list, Qg_list, Ie_list, Qe_list = [f"I{i+1}g" for i in q_id], [f"Q{i+1}g" for i in q_id], [f"I{i+1}e" for i in q_id], [f"Q{i+1}e" for i in q_id]
        results = fetching_tool(job, Ig_list + Qg_list + Ie_list + Qe_list + ["n"], mode='live')   
        while results.is_processing(): 
            all_results = results.fetch_all()
            n = all_results[-1]
            Ig, Qg, Ie, Qe = all_results[0:len(q_id)], all_results[len(q_id):len(q_id)*2], all_results[len(q_id)*2:len(q_id)*3], all_results[len(q_id)*3:len(q_id)*4]  
            for i in q_id:
                Ig[q_id.index(i)] = u.demod2volts(Ig[q_id.index(i)], readout_len)
                Qg[q_id.index(i)] = u.demod2volts(Qg[q_id.index(i)], readout_len)
                Ie[q_id.index(i)] = u.demod2volts(Ie[q_id.index(i)], readout_len)
                Qe[q_id.index(i)] = u.demod2volts(Qe[q_id.index(i)], readout_len)
            progress_counter(n, n_avg, start_time=results.start_time)
            live_plotting(Ig, Qg, Ie, Qe, control_Qi, ramsey_Qi)
        qm.close()
        plt.show()

def live_plotting(Ig, Qg, Ie, Qe, control_Qi, ramsey_Qi):
    for i in q_id: 
        if i == control_Qi-1: control_plot_index = q_id.index(i)
        elif i == ramsey_Qi-1: ramsey_Qi_plot_index = q_id.index(i)
    plt.suptitle("CZ phase diff. \n Number of average = " + str(n_avg))    
    plt.subplot(121)
    plt.cla()
    try:
        fit = Cosine(Phi, Ig[ramsey_Qi_plot_index], plot=False)
        phase_g = fit.out.get('phase')[0]
        plt.plot(fit.x_data, fit.fit_type(fit.x, fit.popt) * fit.y_normal, '-b', alpha=0.5)
        fit = Cosine(Phi, Ie[ramsey_Qi_plot_index], plot=False)
        phase_e = fit.out.get('phase')[0]
        plt.plot(fit.x_data, fit.fit_type(fit.x, fit.popt) * fit.y_normal, '-r', alpha=0.5)
        dphase = (phase_g-phase_e)/np.pi*180     
    except Exception as e: print(e)
    plt.plot(Phi, Ig[ramsey_Qi_plot_index], '.b', Phi, Ie[ramsey_Qi_plot_index], '.r')
    plt.title(f"q{ramsey_Qi} - I, pha_diff={dphase:.1f}")
    plt.xlabel("Phase rotation period")
    plt.ylabel("Voltage [V]")
    plt.subplot(122)
    plt.cla()
    try:
        fit = Cosine(Phi, Qg[ramsey_Qi_plot_index], plot=False)
        phase_g = fit.out.get('phase')[0]
        plt.plot(fit.x_data, fit.fit_type(fit.x, fit.popt) * fit.y_normal, '-b', alpha=0.5)
        fit = Cosine(Phi, Qe[ramsey_Qi_plot_index], plot=False)
        phase_e = fit.out.get('phase')[0]
        plt.plot(fit.x_data, fit.fit_type(fit.x, fit.popt) * fit.y_normal, '-r', alpha=0.5)
        dphase = (phase_g-phase_e)/np.pi*180     
    except Exception as e: print(e)    
    plt.plot(Phi, Qg[ramsey_Qi_plot_index], '.b', Phi, Qe[ramsey_Qi_plot_index], '.r')
    plt.title(f"q{ramsey_Qi} - Q, pha_diff={dphase:.1f}")
    plt.xlabel("Phase rotation period")
    plt.ylabel("Voltage [V]")
    plt.tight_layout()
    plt.pause(0.1)

cz_type = "square"
simulate = False
Phi = np.arange(0, 5, 0.05) # 5 rotations
n_avg = 2000
q_id = [1,2,3,4]
control_Qi = 3
ramsey_Qi = 2
flux_Qi = 2

qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
CZ_phase_diff(q_id,flux_Qi,control_Qi,ramsey_Qi,idle_flux_point,simulate,qmm)

        