from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
from qualang_tools.plot.fitting import Fit
from macros import qua_declaration, multiplexed_readout
from common_fitting_func import gaussian
from scipy.optimize import curve_fit
import warnings

warnings.filterwarnings("ignore")

n_avg = 1000
tau_min = 4  # in clock cycles
tau_max = 17_000  # in clock cycles
d_tau = 140  # in clock cycles
t_delay = np.arange(tau_min, tau_max + 0.1, d_tau)  # Linear sweep
operation_flux_point = [-0.177, -0.132, -0.009, -3.300e-01] 
nb_of_qubits = 4
Qi = 4
# Qi = 1 stands for Q1

def T1_exp(Qi,n_avg,t_delay,operation_flux_point,nb_of_qubits,qmm):
    resonators = list(range(1, nb_of_qubits+1))
    res_num = len(resonators)
    # QUA program
    with program() as T1:
        I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits)
        t = declare(int)  # QUA variable for the wait time
        # Adjust the flux line biases to check whether you are actually measuring the qubit
        for i, flux_point in enumerate(operation_flux_point):
            set_dc_offset(f"q{i+1}_z", "single", flux_point)

        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(t, t_delay)):
                play("x180", f"q{Qi}_xy")
                wait(t, f"q{Qi}_xy")
                align()
                multiplexed_readout(I, I_st, Q, Q_st, resonators=resonators, weights="rotated_")
                wait(thermalization_time * u.ns)

            # Save the averaging iteration to get the progress bar
            save(n, n_st)

        with stream_processing():
            n_st.save("n")
            for i in range(res_num):
                I_st[i].buffer(len(t_delay)).average().save(f"I{i+1}")
                Q_st[i].buffer(len(t_delay)).average().save(f"Q{i+1}")                

    qm = qmm.open_qm(config)
    job = qm.execute(T1)
    I_list, Q_list = [f"I{i+1}" for i in range(res_num)], [f"Q{i+1}" for i in range(res_num)]
    results = fetching_tool(job, I_list + Q_list + ["n"], mode="wait_for_all")
    all_results = results.fetch_all()
    n = all_results[-1]
    I, Q = all_results[0:res_num], all_results[res_num:res_num*2] 
    # Convert the results into Volts
    for i in range(res_num):
        I[i] = u.demod2volts(I[i], readout_len)
        Q[i] = u.demod2volts(Q[i], readout_len)
    qm.close()

    return I[Qi-1], Q[Qi-1]

def T1_plot(I, Q, Qi):
    # Plot
    plt.suptitle("T1 measurement")
    plt.subplot(121)
    plt.cla()
    plt.plot(4 * t_delay, I)
    plt.ylabel("I quadrature [V]")
    plt.title(f"Qubit {Qi}")
    plt.subplot(122)
    plt.cla()
    plt.plot(4 * t_delay, Q)
    plt.ylabel("Q quadrature [V]")
    plt.xlabel("Wait time (ns)")
    plt.title(f"Qubit {Qi}")
    plt.tight_layout()
    plt.pause(0.1)

    fit = Fit()
    plt.figure()
    plt.subplot(121)
    decay_fit = fit.T1(4 * t_delay, I, plot=True)
    qubit_T1_I = np.round(np.abs(decay_fit["T1"][0]) / 4) * 4
    plt.xlabel("Delay [ns]")
    plt.ylabel("I quadrature [V]")
    print(f"Qubit decay time to update in the config: qubit_T1 = {qubit_T1_I:.0f} ns")
    plt.legend((f"depletion time = {qubit_T1_I:.0f} ns",))
    plt.title(f"Qubit {Qi}")    
    plt.subplot(122)
    decay_fit = fit.T1(4 * t_delay, Q, plot=True)
    qubit_T1_Q = np.round(np.abs(decay_fit["T1"][0]) / 4) * 4
    plt.xlabel("Delay [ns]")
    plt.ylabel("Q quadrature [V]")
    print(f"Qubit decay time to update in the config: qubit_T1 = {qubit_T1_Q:.0f} ns")
    plt.legend((f"depletion time = {qubit_T1_Q:.0f} ns",))
    plt.title(f"Qubit {Qi}")       
    plt.tight_layout()
    plt.show()

def T1_fitting(signal):
    fit = Fit()
    decay_fit = fit.T1(4 * t_delay, signal, plot=True)
    qubit_T1 = np.round(np.abs(decay_fit["T1"][0]) / 4) * 4
    return qubit_T1
        
def multi_T1_exp(m, Qi, n_avg,t_delay,operation_flux_point,nb_of_qubits,qmm):
    T1_I, T1_Q = [], []
    for i in range(m):
        I, Q = T1_exp(Qi, n_avg,t_delay,operation_flux_point,nb_of_qubits,qmm)
        T1_I.append(T1_fitting(I))
        T1_Q.append(T1_fitting(Q))
    return T1_I, T1_Q

def T1_hist(data,T1_max):
    new_data = [round(x / 1000) for x in data] # change ns to us

    bin_width = 0.5
    start_value = 0.75
    end_value = T1_max + 0.25
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
    plt.title('Gaussian Distribution Fit')
    plt.show()
    print(f'Mean: {mu:.2f}')
    print(f'Standard Deviation: {sigma:.2f}')

m = 20
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
T1_I, T1_Q = multi_T1_exp(m, Qi, n_avg, t_delay, operation_flux_point, nb_of_qubits, qmm)
print(T1_Q)
T1_hist(T1_Q,40)