from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
from qualang_tools.plot.fitting import Fit
# from common_fitting_func import gaussian
from scipy.optimize import curve_fit
import warnings
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import xarray as xr
warnings.filterwarnings("ignore")
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)

def exp_relaxation_time(max_time, time_resolution, q_name:list, ro_element:list, config, qmm:QuantumMachinesManager, n_avg=100, initializer=None ):
    """
    parameters: \n
    max_time: unit in us, can't < 20 ns \n
    time_resolution: unit in us, can't < 4 ns \n

    Return: \n
    xarray with value 2*N array
    coords: ["mixer","time"]
    max_time unit in us \n
    """

    cc_max_qua = (max_time/4) * u.us
    cc_resolution_qua = (time_resolution/4) * u.us
    cc_delay_qua = np.arange( 4, cc_max_qua, cc_resolution_qua)
    evo_time = cc_delay_qua*4
    evo_time_len = cc_delay_qua.shape[-1]
    # QUA program
    with program() as t1:

        iqdata_stream = multiRO_declare( ro_element )
        t = declare(int)  
        n = declare(int)
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(t, cc_delay_qua)):
                # initializaion
                if initializer is None:
                    wait(1*u.us,ro_element)
                else:
                    try:
                        initializer[0](*initializer[1])
                    except:
                        wait(1*u.us,ro_element)

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

    # Measurement finished
    fetch_data = results.fetch_all()
    qm.close()
    output_data = {}

    for r_idx, r_name in enumerate(ro_element):
        output_data[r_name] = ( ["mixer","time"],
                               np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
    dataset = xr.Dataset(
        output_data,
        coords={ "mixer":np.array(["I","Q"]), "time": evo_time }
    )
    return dataset



def plot_T1( x, y ):
    """
    x shape (M,) 1D array
    y shape (N,M)
    N is 1(I only) or 2(both IQ)
    """
    fig, ax = plt.subplots(2)
    fig.suptitle("T1 measurement")

    # c = ax.pcolormesh(dfs, amp_log_ratio, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    # ax.set_title('pcolormesh')
    # fig.show()
    # Plot
    for i, port in enumerate(["I", "Q"]):
        ax[i].plot( x, y[i], label="data")
        ax[i].set_ylabel(f"{port} quadrature [V]")
        ax[i].set_xlabel("Wait time (ns)")

        fit_T1_par, fit_func = fit_T1(x, y[i])
        ax[i].plot( x, fit_func(x), label="fit")
        print("T1",fit_T1_par)
    return fig

def plot_multiT1( data, rep, time ):
    """
    data shape ( 2, N, M )
    2 is I,Q
    N is rep
    M is time
    """
    idata = data[0]
    qdata = data[1]
    zdata = idata +1j*qdata

    fig, ax = plt.subplots(2)
    ax[0].set_title('I signal')
    ax[0].pcolormesh( time, rep, idata, cmap='RdBu')# , vmin=z_min, vmax=z_max)
    ax[1].set_title('Q signal')
    ax[1].pcolormesh( time, rep, qdata, cmap='RdBu')# , vmin=z_min, vmax=z_max)
    return fig

def fit_T1( evo_time, signal ):
    fit = Fit()
    decay_fit = fit.T1( evo_time, signal )
    relaxation_time = np.round(np.abs(decay_fit["T1"][0]) / 4) * 4
    fit_func = decay_fit["fit_func"]
    return relaxation_time, fit_func
        
def statistic_T1_exp( repeat:int, max_time, time_resolution, q_name:list, ro_element:list, config, qmm:QuantumMachinesManager, n_avg=100, initializer=None ):
    """
    repeat is the measurement times for statistic
    n_avg is the measurement times for getting relaxation time (T1)
    return 2D array with shape ( 2, M )
    axis 0 (2) is I, Q
    axis 1 (M) is repeat 
    """
    statistic_T1 = {}
    raw_data = {}
    repetition = np.arange(repeat)
    for r in ro_element:
        statistic_T1[r] = []
        raw_data[r] = []
    for i in range(repeat):
        print(f"{i}th T1")
        dataset = exp_relaxation_time(max_time, time_resolution, q_name, ro_element, config, qmm, n_avg, initializer)
        time = dataset.coords["time"].values
        for ro_name, data in dataset.data_vars.items():
            T1_i = fit_T1( time, data[0])[0]
            print(f"{ro_name} T1 = {T1_i}")
            statistic_T1[ro_name].append( [T1_i])
            raw_data[ro_name].append(data)

    output_data = {}
    for r in ro_element:
        statistic_T1[r] = np.array(statistic_T1[r]).transpose()[0]
        output_data[r] = (["repetition","mixer","time"], np.array(raw_data[r]))

    dataset = xr.Dataset(
        output_data,
        coords={ "mixer":np.array(["I","Q"]), "time": time, "repetition": repetition }
    )    
    dataset = dataset.transpose("mixer","repetition","time")
    return statistic_T1, dataset

def T1_hist( data, fig=None):

    if fig == None:
        fig, ax = plt.subplots()
    new_data = data/1000 # change ns to us
    mean_t1 = np.mean(new_data)
    bin_width = mean_t1 *0.05
    start_value = np.mean(new_data)*0.5
    end_value = np.mean(new_data)*1.5
    custom_bins = [start_value + i * bin_width for i in range(int((end_value - start_value) / bin_width) + 1)]
    ax.hist(new_data, custom_bins, density=False, alpha=0.7, label='Histogram')# color='blue', 
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

    from configuration import *

    n_avg = 500
    tau_min = 4 // 4 # in clock cycles
    tau_max = 40_000 // 4  # in clock cycles
    d_tau = 400 // 4  # in clock cycles
    t_delay = np.arange(tau_min, tau_max + 0.1, d_tau)  # Linear sweep

    q_name = ["q2_xy"]
    ro_element = ["rr2"]

    repeat_T1 = 1000
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
    statistic_T1, raw_data = statistic_T1_exp(repeat_T1, t_delay, q_name, ro_element, config, qmm, n_avg)
    print(statistic_T1[ro_element[0]].shape)
    fig = T1_hist(statistic_T1[ro_element[0]][0],40)
    fig.show()
    plt.show()

    #   Data Saving   # 
    save_data = True
    if save_data == True:
        from save_data import save_npz
        import sys
        save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
        save_npz(save_dir, save_progam_name+"_raw", raw_data)
        save_npz(save_dir, save_progam_name+"_ana", statistic_T1)
