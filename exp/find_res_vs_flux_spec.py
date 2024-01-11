from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from configuration import *
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.loops import from_array
from qualang_tools.plot import interrupt_on_close
from macros import qua_declaration, multiplexed_readout, live_plotting
import matplotlib.pyplot as plt
import warnings
from scipy import signal
from scipy.optimize import curve_fit
from matplotlib.ticker import FuncFormatter
from common_fitting_func import *
warnings.filterwarnings("ignore")

from datetime import datetime
import sys

def mRO_flux_dep_resonator( q_id,Qi_list,n_avg,dfs,flux,depletion_time,simulate,qmm):
    with program() as multi_res_spec_vs_flux:
        I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(q_id))
        df = declare(int) 
        dc = declare(fixed) 
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(dc, flux)):
                for i in q_id: # set all resonators in idle points
                    set_dc_offset(f"q{i+1}_z", "single", idle_flux_point[i]) 
                for Qi in Qi_list:    
                    set_dc_offset(f"q{Qi}_z", "single", dc)                   
                wait(flux_settle_time * u.ns)             
                with for_(*from_array(df, dfs)):
                    for i in q_id:
                        update_frequency(f"rr{i+1}", df + resonator_IF[i])
                    multiplexed_readout(I, I_st, Q, Q_st, resonators=[x+1 for x in q_id], sequential=False)
                    wait(depletion_time * u.ns, [f"rr{i+1}" for i in q_id]) 
            save(n, n_st)
        with stream_processing():
            n_st.save("n")
            for i in q_id:
                I_st[q_id.index(i)].buffer( len(flux),len(dfs) ).average().save(f"I{i+1}")
                Q_st[q_id.index(i)].buffer( len(flux),len(dfs) ).average().save(f"Q{i+1}")
    if simulate:
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, multi_res_spec_vs_flux, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(multi_res_spec_vs_flux)
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
                Flux[q_id.index(i)] = flux
                Frequency[q_id.index(i)] = dfs + resonator_IF[i] + resonator_LO
                Amplitude[q_id.index(i)] = R
                Phase[q_id.index(i)] = signal.detrend(np.unwrap(phase))     
            progress_counter(n, n_avg, start_time=results.start_time)
            res_flux_live_plot(Amplitude)    
        plt.show()      
        qm.close()
        return Flux, Frequency, Amplitude, Phase, I, Q

def res_flux_live_plot(Amplitude):
    for i in q_id:
        x_label = "Flux bias [V]"
        y_label = "Readout Freq [GHz]"  
        title = "Flux dep. Resonator spectroscopy"
        plt.suptitle(title + " signal: amplitude")             
        plt.subplot(1, len(q_id), q_id.index(i)+1)
        plt.cla()
        plt.title(f"q{i+1}:")
        if q_id.index(i)==0: 
            plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.pcolor(Flux[q_id.index(i)], (Frequency[q_id.index(i)])/u.GHz, Amplitude[q_id.index(i)].transpose())        
    plt.tight_layout()
    plt.pause(0.1)

def res_flux_fitting(signal):
    resonance_index = [[] for _ in q_id] # Find the index of the resonance frequency
    res_F = [[] for _ in q_id]
    resonator_flux_params, resonator_flux_covariance = [], []
    res_LO = resonator_LO
    for i in q_id:
        for j in range(len(Flux[q_id.index(i)])):
            resonance_index[q_id.index(i)].append(np.argmin(signal[q_id.index(i)][j,:]))
        temp_params, temp_covariance = curve_fit(
            f = cosine_func, 
            xdata = Flux[q_id.index(i)],
            ydata = Frequency[q_id.index(i)][resonance_index[q_id.index(i)]],
            p0=g0[i],
            bounds = ([0,0,-np.pi,5e9], [4e6,7,+np.pi,7e9]))
        resonator_flux_params.append(temp_params)
        resonator_flux_covariance.append(temp_covariance)
        res_F[q_id.index(i)].append(cosine_func(Flux[q_id.index(i)], *resonator_flux_params[q_id.index(i)]))
        res_F[q_id.index(i)] = res_F[q_id.index(i)][0]
        sorted_indices = np.argsort(res_F[q_id.index(i)])
        max_index = np.argmax(res_F[q_id.index(i)])
        second_largest_index = sorted_indices[-2]
        max_flux = Flux[q_id.index(i)][max_index]
        second_largest_flux = Flux[q_id.index(i)][second_largest_index]
        second_min_index = sorted_indices[1]
        min_index = np.argmin(res_F[q_id.index(i)])
        min_flux = Flux[q_id.index(i)][min_index]
        second_min_flux = Flux[q_id.index(i)][second_min_index]

        if abs(max_flux-second_largest_flux) > 0.1: # It means we have two maximum sweet points in our flux span.
            if abs(max_flux) >= abs(second_largest_flux):
                max_ROF =  cosine_func(second_largest_flux, *resonator_flux_params[q_id.index(i)])
                print(f'Q{i+1}: maximum ROF: {max_ROF:.4e}, maximum res_IF: {(max_ROF-res_LO):.4e}, corresponding flux: {second_largest_flux:.3e}')
            else:
                max_ROF =  cosine_func(max_flux, *resonator_flux_params[q_id.index(i)])
                print(f'Q{i+1}: maximum ROF: {max_ROF:.4e}, maximum res_IF: {(max_ROF-res_LO):.4e}, corresponding flux: {max_flux:.3e}')
        else: # It means we only have one maximum sweet point in our flux span.
            max_ROF =  cosine_func(max_flux, *resonator_flux_params[q_id.index(i)])
            print(f'Q{i+1}: maximum ROF: {max_ROF:.4e}, maximum res_IF: {(max_ROF-res_LO):.4e}, corresponding flux: {max_flux:.3e}')            
        if abs(min_flux-second_min_flux) > 0.1: # It means we have two minimum points in our flux span.
            if abs(min_flux) >= abs(second_min_flux):
                min_ROF =  cosine_func(second_min_flux, *resonator_flux_params[q_id.index(i)])
                print(f'Q{i+1}: minimum ROF: {min_ROF:.4e}, minimum res_IF: {(min_ROF-res_LO):.4e}, corresponding flux: {second_min_flux:.3e}')
            else:
                min_ROF =  cosine_func(min_flux, *resonator_flux_params[q_id.index(i)])
                print(f'Q{i+1}: minimum ROF: {min_ROF:.4e}, minimum res_IF: {(min_ROF-res_LO):.4e}, corresponding flux: {min_flux:.3e}')
        else: # It means we only have one minimum point in our flux span.
            min_ROF =  cosine_func(min_flux, *resonator_flux_params[q_id.index(i)])
            print(f'Q{i+1}: minimum ROF: {min_ROF:.4e}, minimum res_IF: {(min_ROF-res_LO):.4e}, corresponding flux: {min_flux:.3e}') 
        print(f"Q{i+1} fitting params: {resonator_flux_params[q_id.index(i)]}")           
    return res_F, resonance_index

def res_flux_plot(Flux,Frequency,signal,fitting):
    x_label = "Flux bias [V]"
    y_label = "Readout Freq [GHz]"
    if fitting:  
        res_F, resonance_index = res_flux_fitting(signal)
        for i in q_id: 
            # TOP figure
            plt.subplot(2, len(q_id), q_id.index(i)+1)
            plt.cla()
            plt.title("q%s:"%(i+1))
            if q_id.index(i)==0: 
                plt.ylabel(y_label)
            plt.pcolor(Flux[q_id.index(i)], Frequency[q_id.index(i)], signal[q_id.index(i)].transpose())        
            plt.plot(Flux[q_id.index(i)], Frequency[q_id.index(i)][resonance_index[q_id.index(i)]])
            # BOTTOM figure
            plt.subplot(2, len(q_id), len(q_id)+q_id.index(i)+1)
            plt.cla()
            plt.xlabel(x_label)
            if q_id.index(i)==0:
                plt.ylabel(y_label)
            plt.plot(Flux[q_id.index(i)], Frequency[q_id.index(i)][resonance_index[q_id.index(i)]])
            plt.plot(Flux[q_id.index(i)], res_F[q_id.index(i)])
        plt.tight_layout()
    else:
        for i in q_id:
            plt.subplot(1, len(q_id), q_id.index(i)+1)
            plt.cla()
            plt.title("q%s:"%(i+1))
            if q_id.index(i)==0: 
                plt.ylabel(y_label)
            plt.xlabel(x_label)
            plt.pcolor(Flux[i], Frequency[i], signal[i])        
            # plt.gca().yaxis.set_major_formatter(FuncFormatter(format_y_axis))
        plt.tight_layout()
    plt.show()

qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
# Flux, Frequency, Amplitude, Phase, I, Q = mRO_flux_dep_resonator(q_id,n_avg,dfs,flux,depletion_time,simulate,'live',qmm) 
# fig = res_flux_plot(Flux,Frequency,Amplitude,True)
q_id = [1,2,3,4] # q_id = [1] means rr2
Qi_list = [3] # Qi = 1 means Q1
n_avg = 500
dfs = np.arange(-3e6, 3e6, 0.05e6)
flux = np.arange(idle_flux_point[1]-0.15, idle_flux_point[1]+0.3, 0.005)
Flux = np.zeros((len(q_id), len(flux)))
Frequency = np.zeros((len(q_id), len(dfs)))
Amplitude = np.zeros((len(q_id), len(flux),len(dfs)))
Phase = np.zeros((len(q_id), len(flux), len(dfs)))
depletion_time = 10 * u.us
simulate = False
Flux, Frequency, Amplitude, Phase, I, Q = mRO_flux_dep_resonator(q_id,Qi_list,n_avg,dfs,flux,depletion_time,simulate,qmm) 
fig = res_flux_plot(Flux,Frequency,Amplitude,True)