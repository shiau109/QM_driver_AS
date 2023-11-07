import numpy as np
import matplotlib.pyplot as plt
from common_fitting_func import *
from scipy.optimize import curve_fit, minimize
from configuration import *
from qm.qua import *
from qualang_tools.addons.variables import assign_variables_to_element
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.plot import interrupt_on_close
from scipy import signal
from matplotlib.ticker import FuncFormatter


def format_y_axis(value, tick_number):
    return f'{value * 1e-9:.3f}'

def res_flux(q_id, job, flux, dfs, resonator_IF, p):
    
    # extracting data
    I_list, Q_list = ["I%s"%(i+1) for i in q_id], ["Q%s"%(i+1) for i in q_id]
    results = fetching_tool(job, I_list + Q_list + ["n"], mode="live")
    # Fetch results
    all_results = results.fetch_all()
    I, Q = all_results[0:len(q_id)], all_results[len(q_id):len(q_id)*2]   

    Flux = np.zeros((len(q_id), len(flux)))
    Frequency = np.zeros((len(q_id), len(dfs)))
    Amplitude = np.zeros((len(q_id), len(dfs), len(flux)))
    Phase = np.zeros((len(q_id), len(dfs), len(flux)))
    min_index = [[] for _ in q_id]
    max_index = [[] for _ in q_id]
    resonator_flux_params, resonator_flux_covariance = [], []
    threshold = 0
    res_LO = 5.95e9

    for i in q_id:
        # Data analysis
        S = u.demod2volts(I[q_id.index(i)] + 1j * Q[q_id.index(i)], readout_len)
        R = np.abs(S)
        phase = np.angle(S)

        x_var = flux
        y_var = (dfs + resonator_IF[i]) / u.MHz
        x_label = "Flux bias [V]"
        y_label = "Readout Freq [GHz]"
        map_top = R
        map_bottom = signal.detrend(np.unwrap(phase))

        Flux[i] = x_var
        Frequency[i] = dfs + resonator_IF[i] + resonator_LO
        Amplitude[i] = R
        Phase[i] = signal.detrend(np.unwrap(phase))
        for j in range(len(Flux[i])):
            min_index[i].append(np.argmin(Amplitude[i][:,j]))    

        temp_params, temp_covariance = curve_fit(
            f = resonator_flux, 
            xdata = Flux[i],
            ydata = Frequency[i][min_index[i]],
            p0=p[i],
            bounds = ([0,0,0,-0.5,-np.inf], [3e6,7,10,0.5,np.inf])
            )
        resonator_flux_params.append(temp_params)
        resonator_flux_covariance.append(temp_covariance)
        filtered_indices = np.where(Flux[i] > threshold)[0]
        sup_num = len(Flux[i]) - len(filtered_indices)
        res_IF = resonator_flux(Flux[i][filtered_indices], *resonator_flux_params[i])
        max_index[i] = np.argmax(res_IF) + sup_num
        max_IF =  resonator_flux(Flux[i][max_index[i]], *resonator_flux_params[i])
        print(f'Q{i+1}: maximum ROF: {max_IF:.2e}, maximum res_IF: {(res_LO-max_IF):.2e}, corresponding flux: {Flux[i][max_index[i]]:.3e}')
        
        # Plot Top
        plt.subplot(2, len(q_id), q_id.index(i)+1)
        plt.cla()
        plt.title("q%s:"%(i+1))
        if q_id.index(i)==0: 
            plt.ylabel(y_label)
        plt.pcolor(Flux[i], Frequency[i], Amplitude[i])        
        plt.plot(Flux[i], Frequency[i][min_index[i]])
        plt.gca().yaxis.set_major_formatter(FuncFormatter(format_y_axis))

        # Plot Bottom
        plt.subplot(2, len(q_id), len(q_id)+q_id.index(i)+1)
        plt.cla()
        plt.xlabel(x_label)
        if q_id.index(i)==0:
            plt.ylabel(y_label)
        plt.plot(Flux[i], Frequency[i][min_index[i]])
        plt.plot(Flux[i], resonator_flux(Flux[i], *resonator_flux_params[i]))
        plt.gca().yaxis.set_major_formatter(FuncFormatter(format_y_axis))

    plt.show()
