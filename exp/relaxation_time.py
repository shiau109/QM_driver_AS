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
from common_fitting_func import gaussian
from scipy.optimize import curve_fit
import warnings
from RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save

warnings.filterwarnings("ignore")

# Qi = 1 stands for Q1

def exp_relaxation_time(t_delay, q_name:list, ro_element:list, config, qmm:QuantumMachinesManager, n_avg=100 ):

    evo_time_len = t_delay.shape[-1]
    # QUA program
    with program() as t1:

        iqdata_stream = multiRO_declare( ro_element )
        t = declare(int)  
        n = declare(int)
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(t, t_delay)):
                # Initialize   
                wait(thermalization_time * u.ns)
                # Operation   
                for q in q_name:
                    play("x180", q)
                    wait(t, q)
                align()
                # Readout
                multiRO_measurement( iqdata_stream,  resonators=ro_element, weights="rotated_")
                
            # Save the averaging iteration to get the progress bar
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            multiRO_pre_save(iqdata_stream, ro_element, (evo_time_len,) )

    qm = qmm.open_qm(config)
    job = qm.execute(t1)

    ro_ch_name = []
    for r_name in ro_element:
        ro_ch_name.append(f"{r_name}_I")
        ro_ch_name.append(f"{r_name}_Q")

    data_list = ro_ch_name + ["iteration"]   

    results = fetching_tool(job, data_list=data_list, mode="wait_for_all")
    fetch_data = results.fetch_all()

    # Convert the results into Volts
    output_data = {}
    for r_idx, r_name in enumerate(ro_element):
        output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])
    qm.close()

    return output_data



def plot_T1( x, y, y_label:list=["I","Q"], fig=None ):
    """
    x shape (M,) 1D array
    y shape (N,M)
    N is 1(I only) or 2(both IQ)
    """
    signal_num = y.shape[-1]
    if fig == None:
        fig, ax = plt.subplots(nrows=signal_num)
    # c = ax.pcolormesh(dfs, amp_log_ratio, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    # ax.set_title('pcolormesh')
    # fig.show()
    # Plot
    fig.suptitle("T1 measurement")
    for i in range(signal_num):
        ax[i].plot( x, y[i], label="data")
        ax[i].set_ylabel(f"{y_label} quadrature [V]")
        ax[i].set_xlabel("Wait time (ns)")

        fit_T1_par, fit_func = fit_T1(x, y[i])
        ax[i].plot( x, fit_func(x), label="fit")

    return fig

def fit_T1( evo_time, signal ):
    fit = Fit()
    decay_fit = fit.T1( evo_time, signal )
    relaxation_time = np.round(np.abs(decay_fit["T1"][0]) / 4) * 4
    fit_func = decay_fit["fit_func"]
    return relaxation_time, fit_func
        
def statistic_T1_exp( repeat:int, t_delay, q_name, ro_element, config, qmm, n_avg:int=100 ):
    """
    repeat is the measurement times for statistic
    n_avg is the measurement times for getting relaxation time (T1)
    return 2D array with shape ( 2, M )
    axis 0 (2) is I, Q
    axis 1 (M) is repeat 
    """
    statistic_T1 = {}
    for r in ro_element:
        statistic_T1[r] = []
    for i in range(repeat):
        print(f"{i}th T1")
        data = exp_relaxation_time(t_delay, q_name, ro_element, config, qmm, n_avg)
        for r in ro_element:
            T1_i = fit_T1(t_delay*4, data[r][0])[0]
            print(f"{r} T1 = {T1_i}")
            statistic_T1[r].append( [T1_i, 0])

    for r in ro_element:
        statistic_T1[r] = np.array(statistic_T1[r]).transpose()
    return statistic_T1

def T1_hist( data, T1_max, fig=None):

    if fig == None:
        fig, ax = plt.subplots()
    new_data = data/1000 # change ns to us

    bin_width = 0.5
    start_value = np.mean(new_data)*0.5
    end_value = np.mean(new_data)*1.5
    custom_bins = [start_value + i * bin_width for i in range(int((end_value - start_value) / bin_width) + 1)]
    hist_values, bin_edges = np.histogram(new_data, bins=custom_bins, density=True)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    # params, covariance = curve_fit(gaussian, bin_centers, hist_values)
    # mu, sigma = params
    ax.hist(new_data, 20, density=False, alpha=0.7, color='blue', label='Histogram')
    xmin, xmax = ax.get_xlim()
    x = np.linspace(xmin, xmax, 100)
    # p = gaussian(x, mu, sigma)
    # ax.plot(x, p, 'k', linewidth=2, label=f'Fit result: $\mu$={mu:.2f}, $\sigma$={sigma:.2f}')
    # ax.legend()
    fig.suptitle('T1 Distribution')
    # print(f'Mean: {mu:.2f}')
    # print(f'Standard Deviation: {sigma:.2f}')
    return fig
if __name__ == '__main__':


    n_avg = 500
    tau_min = 4 // 4 # in clock cycles
    tau_max = 40_000 // 4  # in clock cycles
    d_tau = 400 // 4  # in clock cycles
    t_delay = np.arange(tau_min, tau_max + 0.1, d_tau)  # Linear sweep

    q_name = ["q3_xy"]
    ro_element = ["rr3"]

    repeat_T1 = 100
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
    statistic_T1 = statistic_T1_exp(repeat_T1, t_delay, q_name, ro_element, config, qmm, n_avg)
    print(statistic_T1[ro_element[0]].shape)
    fig = T1_hist(statistic_T1[ro_element[0]][0],40)
    fig.show()
    plt.show()