from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from configuration import *
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.loops import from_array
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

q_id = [0,1,2,3]
n_avg = 500
span = 3 * u.MHz
df = 100 * u.kHz
dfs = np.arange(-span, +span + 0.1, df)

flux = np.arange(-0.5, 0.5, 0.01)
depletion_time = 10 * u.us
operation_flux_point = [0,0,0,0] 
simulate = False

def mRO_flux_dep_resonator( q_id,n_avg,dfs,flux,depletion_time,simulate,mode,qmm):
    with program() as multi_res_spec_vs_flux:
        I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(q_id))
        df = declare(int) 
        dc = declare(fixed) 
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(df, dfs)):
                for i in q_id:
                    update_frequency("rr%s"%(i+1), df + resonator_IF[i])
                with for_(*from_array(dc, flux)):
                    for i in [0,1,2,3]: # set all resonators in operation points
                        set_dc_offset("q%s_z"%(i+1), "single", operation_flux_point[i])  
                    for i in q_id:
                        set_dc_offset("q%s_z"%(i+1), "single", dc)                   
                    wait(flux_settle_time * u.ns)  
                    multiplexed_readout(I, I_st, Q, Q_st, resonators=[x+1 for x in q_id], sequential=False)
                    wait(depletion_time * u.ns, ["rr%s"%(i+1) for i in q_id]) 
            save(n, n_st)
        with stream_processing():
            n_st.save("n")
            for i in q_id:
                I_st[q_id.index(i)].buffer(len(flux)).buffer(len(dfs)).average().save("I%s"%(i+1))
                Q_st[q_id.index(i)].buffer(len(flux)).buffer(len(dfs)).average().save("Q%s"%(i+1))
    if simulate:
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, multi_res_spec_vs_flux, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(multi_res_spec_vs_flux)
        I_list, Q_list = ["I%s"%(i+1) for i in q_id], ["Q%s"%(i+1) for i in q_id]
        if mode == 'live':
            results = fetching_tool(job, I_list + Q_list + ["n"], mode='live')
            while results.is_processing():
                all_results = results.fetch_all()
                n = all_results[-1]
                I, Q = all_results[0:len(q_id)], all_results[len(q_id):len(q_id)*2]
                for i in q_id:
                    I[q_id.index(i)] = u.demod2volts(I[q_id.index(i)], readout_len)
                    Q[q_id.index(i)] = u.demod2volts(Q[q_id.index(i)], readout_len)
                    res_flux_live_plot(I,Q)
                    progress_counter(n, n_avg, start_time=results.start_time)
            plt.show()      
        elif mode == 'wait_for_all':
            results = fetching_tool(job, I_list + Q_list + ["n"], mode="wait_for_all")
            fetch_data = results.fetch_all()
            I, Q = fetch_data[0:len(q_id)], fetch_data[len(q_id):len(q_id)*2]
        Flux = np.zeros((len(q_id), len(flux)))
        Frequency = np.zeros((len(q_id), len(dfs)))
        Amplitude = np.zeros((len(q_id), len(dfs), len(flux)))
        Phase = np.zeros((len(q_id), len(dfs), len(flux)))
        for i in q_id:
            S = u.demod2volts(I[q_id.index(i)] + 1j * Q[q_id.index(i)], readout_len)
            R = np.abs(S)
            phase = np.angle(S)
            Flux[q_id.index(i)] = flux
            Frequency[q_id.index(i)] = dfs + resonator_IF[i] + resonator_LO
            Amplitude[q_id.index(i)] = R
            Phase[q_id.index(i)] = signal.detrend(np.unwrap(phase)) 
        qm.close()
        return Flux, Frequency, Amplitude, Phase, I, Q

def res_flux_live_plot(I,Q):
    Flux = np.zeros((len(q_id), len(flux)))
    Frequency = np.zeros((len(q_id), len(dfs)))
    Amplitude = np.zeros((len(q_id), len(dfs), len(flux)))
    Phase = np.zeros((len(q_id), len(dfs), len(flux)))
    for i in q_id:
        S = I[q_id.index(i)] + 1j * Q[q_id.index(i)]
        R = np.abs(S)
        phase = np.angle(S)
        Flux[q_id.index(i)] = flux
        Frequency[q_id.index(i)] = dfs + resonator_IF[i] + resonator_LO
        Amplitude[q_id.index(i)] = R
        Phase[q_id.index(i)] = signal.detrend(np.unwrap(phase)) 
        x_label = "Flux bias [V]"
        y_label = "Readout Freq [GHz]"  
        title = "Flux dep. Resonator spectroscopy"
        plt.suptitle(title + " signal: amplitude")             
        plt.subplot(1, len(q_id), q_id.index(i)+1)
        plt.cla()
        plt.title("q%s:"%(i+1))
        if q_id.index(i)==0: 
            plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.pcolor(Flux[q_id.index(i)], Frequency[q_id.index(i)], Amplitude[q_id.index(i)])        
        plt.gca().yaxis.set_major_formatter(FuncFormatter(format_y_axis))
    plt.tight_layout()
    plt.pause(0.1)

def format_y_axis(value, tick_number):
    return f'{value * 1e-9:.3f}'

def res_flux_fitting(signal):
    resonance_index = [[] for _ in q_id] # Find the index of the resonance frequency
    res_F = [[] for _ in q_id]
    resonator_flux_params, resonator_flux_covariance = [], []
    res_LO = resonator_LO
    for i in q_id:
        for j in range(len(Flux[q_id.index(i)])):
            resonance_index[q_id.index(i)].append(np.argmin(signal[q_id.index(i)][:,j]))

        temp_params, temp_covariance = curve_fit(
            f = resonator_flux, 
            xdata = Flux[q_id.index(i)],
            ydata = Frequency[q_id.index(i)][resonance_index[q_id.index(i)]],
            p0=p[i],
            bounds = ([0,0,0,-0.5,-np.inf], [3e6,7,10,0.5,np.inf]))
        resonator_flux_params.append(temp_params)
        resonator_flux_covariance.append(temp_covariance)
        res_F[q_id.index(i)].append(resonator_flux(Flux[q_id.index(i)], *resonator_flux_params[q_id.index(i)]))
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
                max_ROF =  resonator_flux(second_largest_flux, *resonator_flux_params[q_id.index(i)])
                print(f'Q{i+1}: maximum ROF: {max_ROF:.4e}, maximum res_IF: {(max_ROF-res_LO):.4e}, corresponding flux: {second_largest_flux:.3e}')
            else:
                max_ROF =  resonator_flux(max_flux, *resonator_flux_params[q_id.index(i)])
                print(f'Q{i+1}: maximum ROF: {max_ROF:.4e}, maximum res_IF: {(max_ROF-res_LO):.4e}, corresponding flux: {max_flux:.3e}')
        else: # It means we only have one maximum sweet point in our flux span.
            max_ROF =  resonator_flux(max_flux, *resonator_flux_params[q_id.index(i)])
            print(f'Q{i+1}: maximum ROF: {max_ROF:.4e}, maximum res_IF: {(max_ROF-res_LO):.4e}, corresponding flux: {max_flux:.3e}')            
        if abs(min_flux-second_min_flux) > 0.1: # It means we have two minimum points in our flux span.
            if abs(min_flux) >= abs(second_min_flux):
                min_ROF =  resonator_flux(second_min_flux, *resonator_flux_params[q_id.index(i)])
                print(f'Q{i+1}: minimum ROF: {min_ROF:.4e}, minimum res_IF: {(min_ROF-res_LO):.4e}, corresponding flux: {second_min_flux:.3e}')
            else:
                min_ROF =  resonator_flux(min_flux, *resonator_flux_params[q_id.index(i)])
                print(f'Q{i+1}: minimum ROF: {min_ROF:.4e}, minimum res_IF: {(min_ROF-res_LO):.4e}, corresponding flux: {min_flux:.3e}')
        else: # It means we only have one minimum point in our flux span.
            min_ROF =  resonator_flux(min_flux, *resonator_flux_params[q_id.index(i)])
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
            plt.pcolor(Flux[q_id.index(i)], Frequency[q_id.index(i)], signal[q_id.index(i)])        
            plt.plot(Flux[q_id.index(i)], Frequency[q_id.index(i)][resonance_index[q_id.index(i)]])
            plt.gca().yaxis.set_major_formatter(FuncFormatter(format_y_axis))
            # BOTTOM figure
            plt.subplot(2, len(q_id), len(q_id)+q_id.index(i)+1)
            plt.cla()
            plt.xlabel(x_label)
            if q_id.index(i)==0:
                plt.ylabel(y_label)
            plt.plot(Flux[q_id.index(i)], Frequency[q_id.index(i)][resonance_index[q_id.index(i)]])
            plt.plot(Flux[q_id.index(i)], res_F[q_id.index(i)])
            plt.gca().yaxis.set_major_formatter(FuncFormatter(format_y_axis))  
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
            plt.gca().yaxis.set_major_formatter(FuncFormatter(format_y_axis))
        plt.tight_layout()
    plt.show()

qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
# Flux, Frequency, Amplitude, Phase, I, Q = mRO_flux_dep_resonator(q_id,n_avg,dfs,flux,depletion_time,simulate,'live',qmm) 
# fig = res_flux_plot(Flux,Frequency,Amplitude,True)

# Q1: maximum ROF: 5.7358e+09, maximum res_IF: -2.1422e+08, corresponding flux: -3.500e-01
# Q1: minimum ROF: 5.7344e+09, minimum res_IF: -2.1557e+08, corresponding flux: 4.441e-16
# Q1 fitting params: [2.99999984e+06 4.45914973e+00 2.92751456e-01 3.52360851e-01
#  5.73278447e+09]
# Q2: maximum ROF: 6.0251e+09, maximum res_IF: 7.5132e+07, corresponding flux: -3.100e-01
# Q2: minimum ROF: 6.0244e+09, minimum res_IF: 7.4368e+07, corresponding flux: 3.000e-02
# Q2 fitting params: [2.99966759e+06 4.63869457e+00 1.45922984e-01 3.06517001e-01
#  6.02213244e+09]
# Q3: maximum ROF: 5.8469e+09, maximum res_IF: -1.0315e+08, corresponding flux: -3.000e-01
# Q3: minimum ROF: 5.8460e+09, minimum res_IF: -1.0396e+08, corresponding flux: 4.000e-02
# Q3 fitting params: [1.21997328e+06 4.56292000e+00 5.00492826e-01 2.99382282e-01
#  5.84563065e+09]
# Q4: maximum ROF: 6.1129e+09, maximum res_IF: 1.6291e+08, corresponding flux: -2.800e-01
# Q4: minimum ROF: 6.1124e+09, minimum res_IF: 1.6238e+08, corresponding flux: 5.000e-02
# Q4 fitting params: [1.19360646e+06 4.79382094e+00 2.84429045e-01 2.82308549e-01
#  6.11171247e+09]

q_id = [3]
operation_flux_point = [0, 4.000e-02, 4.000e-02, 0] 
Flux, Frequency, Amplitude, Phase, I, Q = mRO_flux_dep_resonator(q_id,n_avg,dfs,flux,depletion_time,simulate,'live',qmm) 
fig = res_flux_plot(Flux,Frequency,Amplitude,True)