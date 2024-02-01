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
from qualang_tools.bakery import baking
from macros import multiplexed_readout
from common_fitting_func import *
from cosine import Cosine

def get_CZ_wf(segment,a):
    edge = 10
    sFactor = 4
    duration = np.linspace(0,49,50)
    paras = [a, edge, sFactor]
    p = ( paras[0], paras[1]/2, paras[1]/paras[2], 2*paras[1], 5 ) # This 5 can make the pulse edge smooth in the begining.
    eerp_up_wf = np.array(EERP(duration,*p)[:(paras[1]+5)]) 
    eerp_dn_wf = eerp_up_wf[::-1]
    waveform = np.array([a]*(segment+1))
    eerp_wf = np.concatenate((eerp_up_wf, waveform, eerp_dn_wf))
    eerp_wf = eerp_wf.tolist()
    wf = eerp_wf
    return wf

def cz_gate(flux_Qi,ramsey_Qi,segment,a):
    wf = get_CZ_wf(segment,a)
    with baking(config,padding_method="symmetric_l") as b:
        q1_xy_element = f"q{flux_Qi}_xy"  
        q2_xy_element = f"q{ramsey_Qi}_xy"
        q1_z_element = f"q{flux_Qi}_z"
        b.add_op("cz",q1_z_element,wf)
        b.wait(20,q1_xy_element,q2_xy_element,q1_z_element) # The unit is 1 ns.
        b.align(q1_xy_element,q2_xy_element,q1_z_element)
        b.play("cz", q1_z_element)
        b.align(q1_xy_element,q2_xy_element,q1_z_element)
        b.wait(23,q1_xy_element,q2_xy_element,q1_z_element)
        b.align(q1_xy_element,q2_xy_element,q1_z_element)
        b.run()

def CZ_phase_diff(q_id,flux_Qi,control_Qi,ramsey_Qi,idle_flux_point,signal_mode,simulate,qmm):
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
        a = declare(fixed)  
        segment = declare(int)
        for i in q_id:
            res_F = cosine_func( idle_flux_point[i], *g1[i])
            res_F = (res_F - resonator_LO)/1e6
            res_IF.append(int(res_F * u.MHz))
            resonator_freq[q_id.index(i)] = declare(int, value=res_IF[q_id.index(i)])
            set_dc_offset(f"q{i+1}_z", "single", idle_flux_point[i])
            update_frequency(f"rr{i+1}", resonator_freq[q_id.index(i)])
        wait(flux_settle_time * u.ns)
        with for_(n, 0, n < n_avg, n+1):
            with for_(*from_array(a, amps)):
                ## This +1 is inserted because of making segment equal to actual pulse duration
                with for_(segment, t_min+1, segment <= t_max+1, segment + 1): 
                    with for_(*from_array(phi, Phi)):
                        if not simulate: wait(thermalization_time * u.ns)
                        align()
                        play("x90", f"q{ramsey_Qi}_xy")
                        align()
                        cz_gate(flux_Qi,ramsey_Qi,segment,a)
                        align()
                        frame_rotation_2pi(phi, f"q{ramsey_Qi}_xy")
                        play("x90", f"q{ramsey_Qi}_xy")
                        wait(flux_settle_time * u.ns)
                        multiplexed_readout(I_g, I_st_g, Q_g, Q_st_g, resonators=[x+1 for x in q_id], weights="rotated_")

                        if not simulate: wait(thermalization_time * u.ns)
                        align()                       
                        play("x180", f"q{control_Qi}_xy")
                        play("x90", f"q{ramsey_Qi}_xy")
                        align()
                        cz_gate(flux_Qi,ramsey_Qi,segment,a)
                        align()
                        frame_rotation_2pi(phi, f"q{ramsey_Qi}_xy")
                        play("x90", f"q{ramsey_Qi}_xy")
                        wait(flux_settle_time * u.ns)
                        align()
                        multiplexed_readout(I_e, I_st_e, Q_e, Q_st_e, resonators=[x+1 for x in q_id], weights="rotated_")
            save(n, n_st)        
        with stream_processing():
            n_st.save('n')
            for i in q_id:
                I_st_g[q_id.index(i)].buffer( len(amps),len(t_delay),len(Phi) ).average().save(f"I{i+1}g")
                Q_st_g[q_id.index(i)].buffer( len(amps),len(t_delay),len(Phi) ).average().save(f"Q{i+1}g")  
                I_st_e[q_id.index(i)].buffer( len(amps),len(t_delay),len(Phi) ).average().save(f"I{i+1}e")
                Q_st_e[q_id.index(i)].buffer( len(amps),len(t_delay),len(Phi) ).average().save(f"Q{i+1}e")
    if simulate:
        job = qmm.simulate(config, cz_ops, SimulationConfig(15000))
        job.get_simulated_samples().con1.plot()
        plt.show()    
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(cz_ops)
        row,col = len(amps),len(t_delay)
        fig, ax = plt.subplots(row,col)
        fig.suptitle(f"q{ramsey_Qi} "+signal_mode+" CZ phase diff. \n Number of average = " + str(n_avg)) 
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
            match signal_mode:
                case 'I':
                    signal_g = Ig
                    signal_e = Ie
                case 'Q':
                    signal_g = Qg
                    signal_e = Qe
            live_plotting(signal_g, signal_e, control_Qi, ramsey_Qi,row,col,ax)
        qm.close()
        plt.show()

def live_plotting(signal_g, signal_e, control_Qi, ramsey_Qi,row,col,ax):
    for i in q_id: 
        if i == control_Qi-1: control_plot_index = q_id.index(i)
        elif i == ramsey_Qi-1: ramsey_Qi_plot_index = q_id.index(i)

    for i in range(row):
        for j in range(col):
            ax[i,j].cla()
            ax[i,j].plot(Phi, signal_g[ramsey_Qi_plot_index][i][j], '.b', Phi, signal_e[ramsey_Qi_plot_index][i][j], '.r')
            try:
                fit = Cosine(Phi, signal_g[ramsey_Qi_plot_index][i][j], plot=False)
                phase_g = fit.out.get('phase')[0]
                ax[i,j].plot(fit.x_data, fit.fit_type(fit.x, fit.popt) * fit.y_normal, '-b', alpha=0.5)
                fit = Cosine(Phi, signal_e[ramsey_Qi_plot_index][i][j], plot=False)
                phase_e = fit.out.get('phase')[0]
                ax[i,j].plot(fit.x_data, fit.fit_type(fit.x, fit.popt) * fit.y_normal, '-r', alpha=0.5)
                dphase = (phase_g-phase_e)/np.pi*180     
            except Exception as e: print(e)
            ax[i,j].set_title(f"pha_diff {dphase:.1f}, ZW {t_delay[j]:.0f}, ZL {amps[i]*const_flux_amp:.5f}",fontsize = 7)
            # ax[i,j].set_xlabel('Phase cycle',fontsize = 7)
            # ax[i,j].set_ylabel('Voltage [V]',fontsize = 7)
            # ax[i, j].tick_params(axis='both', labelsize=7)
    plt.tight_layout()
    plt.pause(1.0)

# type = "eerp"
# simulate = True
# Phi = np.arange(0, 5, 0.05) # 5 rotations
# n_avg = 1500
# q_id = [1,2,3,4]
# control_Qi = 2
# ramsey_Qi = 3
# flux_Qi = 2
# t_min, t_max = 20, 25
# t_delay = np.arange(t_min, t_max + 0.1, 1) 
# edge = 10
# sFactor = 4
# amps = np.arange(0.3336, 0.3356, 0.0004) 
# signal_mode = 'I'
# qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
# CZ_phase_diff(q_id,flux_Qi,control_Qi,ramsey_Qi,idle_flux_point,signal_mode,simulate,qmm)
    
segment = 20
a = 0.33
wf = get_CZ_wf(segment,a)
print(len(wf))
x = np.linspace(0,50,51)
plt.plot(x,wf)
plt.show()

