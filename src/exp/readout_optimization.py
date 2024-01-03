"""
        READOUT OPTIMISATION: FREQUENCY
This sequence involves measuring the state of the resonator in two scenarios: first, after thermalization
(with the qubit in the |g> state) and then after applying a pi pulse to the qubit (transitioning the qubit to the
|e> state). This is done while varying the readout frequency.
The average I & Q quadratures for the qubit states |g> and |e>, along with their variances, are extracted to
determine the Signal-to-Noise Ratio (SNR). The readout frequency that yields the highest SNR is selected as the
optimal choice.

Prerequisites:
    - Having found the resonance frequency of the resonator coupled to the qubit under study (resonator_spectroscopy).
    - Having calibrated qubit pi pulse (x180) by running qubit, spectroscopy, rabi_chevron, power_rabi and updated the config.
    - Set the desired flux bias

Next steps before going to the next node:
    - Update the readout frequency (resonator_IF_q) in the configuration.
"""

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
#######################
# AUXILIARY FUNCTIONS #
#######################
u = unit(coerce_to_integer=True)

def freq_dep_signal( dfs, q_name:list, ro_element:list, n_avg, config, qmm:QuantumMachinesManager, simulate=False, initializer:tuple=None ):

    center_IF = {}
    for r in ro_element:
        center_IF[r] = config["elements"][r]["intermediate_frequency"]
    freq_len = dfs.shape[-1]
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
            with for_(*from_array(df, dfs)):
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
                        update_frequency(r, df + center_IF[r])
                    multiRO_measurement(iqdata_stream, ro_element, weights="rotated_",amp_modify=0.5)
                    # Save the averaging iteration to get the progress bar
            save(n, n_st)

        with stream_processing():
            n_st.save("n")
            multiRO_pre_save( iqdata_stream, ro_element, (freq_len,2) )


    # Open the quantum machine
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(ro_freq_opt)
    # Get results from QUA program
    
    data_list = []
    for r in ro_element:
        data_list.append(f"{r}_I")
        data_list.append(f"{r}_Q")

    results = fetching_tool(job, data_list=data_list, mode="wait_for_all")
    fetch_data = results.fetch_all()
    output_data = {}
    for r_idx, r_name in enumerate(ro_element):
        print(np.array(fetch_data[r_idx*2]).shape)
        i_data = np.moveaxis(np.array(fetch_data[r_idx*2]), 0,-1)
        q_data = np.moveaxis(np.array(fetch_data[r_idx*2+1]), 0,-1)

        output_data[r_name] = np.array([i_data,q_data])
    
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    return output_data

def power_dep_signal( amp_ratio, q_name:list, ro_element:list, n_avg, config, qmm:QuantumMachinesManager, initializer=None, simulate=False ):

    center_IF = {}
    for r in ro_element:
        center_IF[r] = config["elements"][r]["intermediate_frequency"]
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
            n_st.save("n")
            multiRO_pre_save( iqdata_stream, ro_element, (amp_len,2))


    # Open the quantum machine
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(ro_freq_opt)
    # Get results from QUA program
    
    data_list = []
    for r in ro_element:
        data_list.append(f"{r}_I")
        data_list.append(f"{r}_Q")

    results = fetching_tool(job, data_list=data_list, mode="wait_for_all")
    fetch_data = results.fetch_all()
    output_data = {}
    for r_idx, r_name in enumerate(ro_element):
        i_data = np.moveaxis(np.array(fetch_data[r_idx*2]), 0,-1)
        q_data = np.moveaxis(np.array(fetch_data[r_idx*2+1]), 0,-1)

        output_data[r_name] = np.array([i_data,q_data])
    
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    return output_data

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