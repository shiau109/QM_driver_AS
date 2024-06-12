
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
# from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool, progress_counter
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save

import warnings

warnings.filterwarnings("ignore")

from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
import xarray as xr
import time

def freq_dep_signal( freq_range, freq_resolution, q_name:list, ro_element:list, n_avg, config, qmm:QuantumMachinesManager, amp_mod=0.5, simulate=False, initializer:tuple=None )->xr.Dataset:
    """
    Parameters:\n
    freq_range: readout frequency, unit in MHz.\n
    freq_resolution: unit in MHz.\n
    amp_mod: The modification ratio of RO pulse amplitude default is 0.5 

    Return:
    ["mixer", "frequency", "state"]
    """
    freq_r1_qua = freq_range[0] * u.MHz
    freq_r2_qua = freq_range[1] * u.MHz

    freq_resolution_qua = freq_resolution * u.MHz

    freqs_qua = np.arange( freq_r1_qua, freq_r2_qua, freq_resolution_qua )
    freqs_mhz = freqs_qua/1e6 #  Unit in MHz

    center_IF = {}
    for r in ro_element:
        center_IF[r] = config["elements"][r]["intermediate_frequency"]
    freq_len = freqs_qua.shape[-1]
    ###################
    # The QUA program #
    ###################
    with program() as ro_freq_opt:
        iqdata_stream = multiRO_declare(ro_element)
        n = declare(int)
        n_st = declare_stream()
        df = declare(int)  # QUA variable for the readout frequency
        p_idx = declare(int)
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(df, freqs_qua)):
                # Update the frequency of the two resonator elements
                with for_each_( p_idx, [0, 1]):  
                    # Init
                    if initializer is None:
                        wait(100*u.us)
                        #wait(thermalization_time * u.ns)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            print("Initializer didn't work!")
                            wait(100*u.us)
                        
                    # Operation
                    with switch_(p_idx, unsafe=True):
                        with case_(0):
                            pass
                        with case_(1):
                            for q in q_name:
                                play("x180", q)
                    align()
                    # Measurement
                    for r in ro_element:
                        update_frequency(r, df +center_IF[r])
                    multiRO_measurement(iqdata_stream, ro_element, weights="rotated_",amp_modify=amp_mod)
                    # Save the averaging iteration to get the progress bar
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            multiRO_pre_save( iqdata_stream, ro_element, (freq_len,2) )


    # Open the quantum machine
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(ro_freq_opt)
    # Get results from QUA program
    
    ro_ch_name = []
    for r in ro_element:
        ro_ch_name.append(f"{r}_I")
        ro_ch_name.append(f"{r}_Q")
    data_list = ro_ch_name + ["iteration"]   

    results = fetching_tool(job, data_list=data_list, mode="live")
    # Live plotting
    while results.is_processing():
        # Fetch results
        fetch_data = results.fetch_all()
        # Progress bar
        iteration = fetch_data[-1]
        progress_counter(iteration, n_avg, start_time=results.start_time)
        # Plot
        plt.tight_layout()
        time.sleep(1)

    fetch_data = results.fetch_all()
    qm.close()
    # Creating an xarray dataset
    output_data = {}
    for r_idx, r_name in enumerate(ro_element):
        output_data[r_name] = ( ["mixer","frequency","state"],
                                np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
    dataset = xr.Dataset(
        output_data,
        coords={ "mixer":np.array(["I","Q"]), "frequency": freqs_mhz, "state":[0,1] }
    )
    # dataset.attrs["ref_xy_IF"] = ref_xy_IF
    # dataset.attrs["ref_xy_LO"] = ref_xy_LO

    return dataset

def power_dep_signal( amp_range, amp_resolution, q_name:list, ro_element:list, n_avg, config, qmm:QuantumMachinesManager, initializer=None, simulate=False )->xr.Dataset:
    """
    
    Return:
    dataset ["mixer", "state", "amplitude_ratio"]
    """

    amp_ratio = np.arange( amp_range[0] , amp_range[1], amp_resolution )
    amp_len = amp_ratio.shape[-1]
    ###################
    # The QUA program #
    ###################
    with program() as ro_freq_opt:
        iqdata_stream = multiRO_declare(ro_element)
        n = declare(int)
        n_st = declare_stream()
        a = declare(fixed)  # QUA variable for the readout frequency
        p_idx = declare(int)
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(a, amp_ratio)):

                with for_each_( p_idx, [0, 1]):  
                    # Init
                    if initializer is None:
                        wait(100*u.us)
                        #wait(thermalization_time * u.ns)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            print("Initializer didn't work!")
                            wait(100*u.us)
                        
                    # Operation
                    with switch_(p_idx, unsafe=True):
                        with case_(0):
                            pass
                        with case_(1):
                            for q in q_name:
                                play("x180", q)
                    align()
                    # Measurement
                    multiRO_measurement(iqdata_stream, ro_element, weights="rotated_", amp_modify = a)
            # Save the averaging iteration to get the progress bar
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            multiRO_pre_save( iqdata_stream, ro_element, (amp_len,2))


    # Open the quantum machine
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(ro_freq_opt)
    # Get results from QUA program
    
    ro_ch_name = []
    for r in ro_element:
        ro_ch_name.append(f"{r}_I")
        ro_ch_name.append(f"{r}_Q")
    data_list = ro_ch_name + ["iteration"]   

    results = fetching_tool(job, data_list=data_list, mode="live")
    # Live plotting
    while results.is_processing():
        # Fetch results
        fetch_data = results.fetch_all()
        # Progress bar
        iteration = fetch_data[-1]
        progress_counter(iteration, n_avg, start_time=results.start_time)
        time.sleep(1)

    fetch_data = results.fetch_all()
    qm.close()
    # Creating an xarray dataset
    output_data = {}
    for r_idx, r_name in enumerate(ro_element):
        output_data[r_name] = ( ["mixer","amplitude_ratio","state"],
                                np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
    dataset = xr.Dataset(
        output_data,
        coords={ "mixer":np.array(["I","Q"]), "amplitude_ratio": amp_ratio, "state":[0,1] }
    )
    return dataset

def plot_freq_signal( x, data, label:str, ax ):
    print(data.shape)
    sig = get_signal_distance(data)
    ax[0].plot( x, sig, ".-")
    ax[0].set_title(f"{label} RO frequency")
    ax[0].set_xlabel("Readout frequency detuning [MHz]")
    ax[0].set_ylabel("Distance")
    ax[0].grid("on")

    sig = get_signal_amp(data)
    ax[1].plot( x, sig[0], ".-", label="0")

    ax[1].plot( x, sig[1], ".-", label="1")

    # ax[1].set_title(f"{label} RO frequency")
    ax[1].set_xlabel("Readout frequency detuning [MHz]")
    ax[1].set_ylabel("Amplitude")
    ax[1].legend()
    ax[1].grid("on")

    sig = get_signal_phase(data)
    ax[2].plot( x, sig[0], ".-", label="0")
    ax[2].plot( x, sig[1], ".-", label="1")

    # ax[2].set_title(f"{label} RO frequency")
    ax[2].set_xlabel("Readout frequency detuning [MHz]")
    ax[2].set_ylabel("Phase")
    ax[2].legend()
    ax[2].grid("on")
    # print(f"The optimal readout frequency is {dfs[np.argmax(SNR1)] + resonator_IF_q1} Hz (SNR={max(SNR1)})")
    return ax

def plot_amp_signal( x, data, label:str, ax ):
    sig = get_signal_distance(data)
    ax.plot( x, sig, ".-")
    ax.set_xlabel("Readout amplitude ")
    ax.set_ylabel("Distance")
    ax.grid("on")
    # print(f"The optimal readout frequency is {dfs[np.argmax(SNR1)] + resonator_IF_q1} Hz (SNR={max(SNR1)})")
    return ax

def plot_amp_signal_phase( x, data, label:str, ax ):
    phase_g, phase_e = get_signal_phase(data)
    ax.plot( x, phase_g, ".-", label="phase_g")
    ax.plot( x, phase_e, ".-", label="phase_e")
    ax.set_xlabel("Readout amplitude ")
    ax.set_ylabel("Phase")
    ax.grid("on")
    ax.legend()
    # print(f"The optimal readout frequency is {dfs[np.argmax(SNR1)] + resonator_IF_q1} Hz (SNR={max(SNR1)})")
    return ax

def get_signal_distance( data ):
    """
    data shape (2,2,N)
    axis 0 I,Q
    axis 1 g,e
    axis 2 N frequency
    """
    s21_g = data[0][0] +1j*data[1][0] 
    s21_e = data[0][1] +1j*data[1][1]
    signal = np.abs(s21_g -s21_e)
    return signal

def get_signal_phase( data ):
    """
    data shape (2,2,N)
    axis 0 I,Q
    axis 1 g,e
    axis 2 N frequency
    """
    s21_g = data[0][0] +1j*data[1][0] 
    s21_e = data[0][1] +1j*data[1][1]
    phase_g = np.unwrap(np.angle(s21_g))
    phase_e = np.unwrap(np.angle(s21_e))
    return (phase_g, phase_e)

def get_signal_amp( data ):
    """
    data shape (2,2,N)
    axis 0 I,Q
    axis 1 g,e
    axis 2 N frequency
    """
    s21_g = data[0][0] +1j*data[1][0] 
    s21_e = data[0][1] +1j*data[1][1]
    phase_g = np.abs(s21_g)
    phase_e = np.abs(s21_e)
    return (phase_g, phase_e)

if __name__ == '__main__':

    n_avg = 1000

    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

    operate_qubit = ["q3_xy"]
    ro_element = ["rr3"]

    # The frequency sweep around the resonators' frequency "resonator_IF_q"
    dfs = np.arange(-1e6, 1e6, 0.02e6)
    output_data = freq_dep_signal( dfs, operate_qubit, ro_element, n_avg, config, qmm)
    for r in ro_element:
        fig = plt.figure()
        ax = fig.subplots(3,1)
        plot_freq_signal( dfs, output_data[r], r, ax )
    plt.show()
    
    # amps = np.linspace(0, 1.8, 180)
    # data = power_dep_signal( amps, operate_qubit, ro_element, n_avg, config, qmm)
    # for r in ro_element:
    #     fig = plt.figure()
    #     ax = fig.subplots(1,2,sharex=True)
    #     plot_amp_signal( amps, data[r], r, ax[0] )
    #     plot_amp_signal_phase( amps, data[r], r, ax[1] )

    #     fig.suptitle(f"{r} RO amplitude")
    plt.show()
    #   Data Saving   # 
    save_data = True
    if save_data:
        from save_data import save_npz
        import sys
        save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
        save_npz(save_dir, "r23_x2", output_data)    