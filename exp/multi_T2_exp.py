from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.plot import interrupt_on_close
from macros import qua_declaration, multiplexed_readout
from qualang_tools.plot.fitting import Fit
from common_fitting_func import gaussian
from scipy.optimize import curve_fit
import warnings

warnings.filterwarnings("ignore")

def T2_exp(Qi,n_avg,idle_times,operation_flux_point,q_id,qmm):
    resonators = [i+1 for i in q_id]
    res_num = len(resonators)
    with program() as ramsey:
        I, I_st, Q, Q_st, n, n_st = qua_declaration(res_num)
        t = declare(int)  
        for i in q_id:
            set_dc_offset(f"q{i+1}_z", "single", operation_flux_point[i])
        update_frequency(f"q{Qi}_xy", detuning + qubit_IF[Qi-1])
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(t, idle_times)):
                # Qubit Qi
                play("x90", f"q{Qi}_xy")  
                wait(t, f"q{Qi}_xy")  
                play("x90", f"q{Qi}_xy") 
                align()
                multiplexed_readout(I, I_st, Q, Q_st, resonators=resonators, weights="rotated_")
                wait(thermalization_time * u.ns)
            save(n, n_st)

        with stream_processing():
            n_st.save("n")
            for i in range(res_num):
                I_st[i].buffer(len(idle_times)).average().save(f"I{i+1}")
                Q_st[i].buffer(len(idle_times)).average().save(f"Q{i+1}")    
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
        progress_counter(n, n_avg, start_time=results.start_time)
        for i in range(res_num):
            I[i] = u.demod2volts(I[i], readout_len)
            Q[i] = u.demod2volts(Q[i], readout_len)
        T2_plot(I[Qi-1],Q[Qi-1],Qi,False)
    plt.close()
    qm.close()
    return I[Qi-1], Q[Qi-1]

def T2_plot(I, Q, Qi,fitting):
    plt.suptitle("T2 measurement")
    plt.subplot(121)
    plt.cla()
    plt.plot(4 * idle_times, I)
    plt.ylabel("I quadrature [V]")
    plt.subplot(122)
    plt.cla()
    plt.plot(4 * idle_times, Q)
    plt.ylabel("Q quadrature [V]")
    plt.xlabel("Idle times [ns]")
    plt.title(f"Qubit {Qi}")
    plt.tight_layout()
    plt.pause(0.1)
    if fitting:
        fit = Fit()
        plt.figure()
        plt.suptitle(f"Ramsey measurement with detuning={detuning} Hz")
        plt.subplot(121)
        fit.ramsey(4 * idle_times, I, plot=True)
        plt.xlabel("Idle times [ns]")
        plt.ylabel("I quadrature [V]")
        plt.subplot(122)
        fit.ramsey(4 * idle_times, Q, plot=True)
        plt.xlabel("Idle times [ns]")
        plt.ylabel("Q quadrature [V]")
        plt.title(f"Qubit {Qi}")
        plt.tight_layout()
        plt.show()

def T2_fitting(signal):
    fit = Fit()
    decay_fit = fit.ramsey(4 * idle_times, signal, plot=False)
    qubit_T2 = np.round(np.abs(decay_fit["T2"][0]) / 4) * 4
    return qubit_T2

def multi_T2_exp(m, Qi, n_avg,idle_times,operation_flux_point,q_id,qmm):
    T2_I, T2_Q = [], []
    for i in range(m):
        I, Q = T2_exp(Qi,n_avg,idle_times,operation_flux_point,q_id,qmm)
        T2_I.append(T2_fitting(I))
        T2_Q.append(T2_fitting(Q))
    return T2_I, T2_Q

def T2_hist(data,T2_max,signal_name):
    try:
        new_data = [round(x / 1000) for x in data] # change ns to us
        bin_width = 0.5
        start_value = 0.75
        end_value = T2_max + 0.25
        custom_bins = [start_value + i * bin_width for i in range(int((end_value - start_value) / bin_width) + 1)]
        hist_values, bin_edges = np.histogram(new_data, bins=custom_bins, density=True)
        bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
        params, covariance = curve_fit(gaussian, bin_centers, hist_values)
        mu, sigma = params
        plt.cla()
        plt.hist(new_data, bins=custom_bins, density=True, alpha=0.7, color='blue', label='Histogram')
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = gaussian(x, mu, sigma)
        plt.plot(x, p, 'k', linewidth=2, label=f'Fit result: $\mu$={mu:.2f}, $\sigma$={sigma:.2f}')
        plt.legend()
        plt.title('T2_'+signal_name+' Gaussian Distribution Fit')
        plt.show()
        print(f'Mean: {mu:.2f}')
        print(f'Standard Deviation: {sigma:.2f}')
    except (Exception,):
        pass

n_avg = 500  
idle_times = np.arange(4, 2500, 5)  
detuning = 1e6  
operation_flux_point = [0, 4.000e-02, -3.100e-01, 4.000e-02]
q_id = [0,1,2,3]
Qi = 3

qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
# I,Q = T2_exp(Qi,n_avg,idle_times,operation_flux_point,q_id,qmm)
# T2_plot(I, Q, Qi, True)
m = 2
T2_I, T2_Q = multi_T2_exp(m, Qi, n_avg,idle_times,operation_flux_point,q_id,qmm)
T2_hist(T2_I,20,'I')
T2_hist(T2_Q,20,'Q')