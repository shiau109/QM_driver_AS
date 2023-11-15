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
from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool, progress_counter
from macros import multiplexed_readout, qua_declaration
from QM_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save

import warnings

warnings.filterwarnings("ignore")


def freq_dep_signal( dfs, q_name:list, ro_element:list, n_avg, config, qmm:QuantumMachinesManager ):

    center_IF = {}
    for r in ro_element:
        center_IF[r] = config["elements"][r]["intermediate_frequency"]
    freq_len = dfs.shape[-1]
    ###################
    # The QUA program #
    ###################
    with program() as ro_freq_opt:
        iqdata_stream_g = multiRO_declare(ro_element)
        iqdata_stream_e = multiRO_declare(ro_element)
        n = declare(int)
        n_st = declare_stream()
        df = declare(int)  # QUA variable for the readout frequency

        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(df, dfs)):
                # Update the frequency of the two resonator elements
                for r in ro_element:
                    update_frequency(r, df + center_IF[r])
                # Reset both qubits to ground
                wait(thermalization_time * u.ns)
                # Measure the ground IQ blobs
                multiRO_measurement(iqdata_stream_g, ro_element, weights="rotated_")
                align()
                # Reset both qubits to ground
                wait(thermalization_time * u.ns)
                # Measure the excited IQ blobs
                for name in q_name:
                    play("x180", name)
                align()
                multiRO_measurement(iqdata_stream_e, ro_element, weights="rotated_")
            # Save the averaging iteration to get the progress bar
            save(n, n_st)

        with stream_processing():
            n_st.save("n")
            multiRO_pre_save( iqdata_stream_g, ro_element, (freq_len,), "_g" )
            multiRO_pre_save( iqdata_stream_e, ro_element, (freq_len,), "_e" )


    # Open the quantum machine
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(ro_freq_opt)
    # Get results from QUA program
    
    data_list = []
    for r in ro_element:
        data_list.append(f"{r}_I_g")
        data_list.append(f"{r}_Q_g")
        data_list.append(f"{r}_I_e")
        data_list.append(f"{r}_Q_e")

    results = fetching_tool(job, data_list=data_list, mode="wait_for_all")
    fetch_data = results.fetch_all()
    output_data = {}
    for r_idx, r_name in enumerate(ro_element):
        output_data[r_name] = np.array(
            [[fetch_data[r_idx*4], fetch_data[r_idx*4+1]],
             [fetch_data[r_idx*4+2], fetch_data[r_idx*4+3]]])
    
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    return output_data

def power_dep_signal( amp_ratio, q_name:list, ro_element:list, n_avg, config, qmm:QuantumMachinesManager ):

    center_IF = {}
    for r in ro_element:
        center_IF[r] = config["elements"][r]["intermediate_frequency"]
    amp_len = amp_ratio.shape[-1]
    ###################
    # The QUA program #
    ###################
    with program() as ro_freq_opt:
        iqdata_stream_g = multiRO_declare(ro_element)
        iqdata_stream_e = multiRO_declare(ro_element)
        n = declare(int)
        n_st = declare_stream()
        a = declare(fixed)  # QUA variable for the readout frequency

        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(a, amp_ratio)):

                # Reset both qubits to ground
                wait(thermalization_time * u.ns)
                # Measure the ground IQ blobs
                multiRO_measurement(iqdata_stream_g, ro_element, weights="rotated_", amp_modify = a)
                align()
                # Reset both qubits to ground
                wait(thermalization_time * u.ns)
                # Measure the excited IQ blobs
                for name in q_name:
                    play("x180", name)
                align()
                multiRO_measurement(iqdata_stream_e, ro_element, weights="rotated_", amp_modify = a)
            # Save the averaging iteration to get the progress bar
            save(n, n_st)

        with stream_processing():
            n_st.save("n")
            multiRO_pre_save( iqdata_stream_g, ro_element, (amp_len,), "_g" )
            multiRO_pre_save( iqdata_stream_e, ro_element, (amp_len,), "_e" )


    # Open the quantum machine
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(ro_freq_opt)
    # Get results from QUA program
    
    data_list = []
    for r in ro_element:
        data_list.append(f"{r}_I_g")
        data_list.append(f"{r}_Q_g")
        data_list.append(f"{r}_I_e")
        data_list.append(f"{r}_Q_e")

    results = fetching_tool(job, data_list=data_list, mode="wait_for_all")
    fetch_data = results.fetch_all()
    output_data = {}
    for r_idx, r_name in enumerate(ro_element):
        output_data[r_name] = np.array(
            [[fetch_data[r_idx*4], fetch_data[r_idx*4+1]],
             [fetch_data[r_idx*4+2], fetch_data[r_idx*4+3]]])
    
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    return output_data

def plot_freq_signal( x, data, label ):
    sig = get_signal_amplitude(data)
    plt.suptitle("Readout frequency optimization")
    plt.cla()
    plt.plot( x, sig, ".-")
    plt.title(f"{label} RO frequency")
    plt.xlabel("Readout frequency detuning [MHz]")
    plt.ylabel("SNR")
    plt.grid("on")
    # print(f"The optimal readout frequency is {dfs[np.argmax(SNR1)] + resonator_IF_q1} Hz (SNR={max(SNR1)})")

def plot_amp_signal( x, data, label ):
    sig = get_signal_amplitude(data)
    plt.suptitle("Readout amplitude optimization")
    plt.cla()
    plt.plot( x, sig, ".-")
    plt.title(f"{label} RO amplitude")
    plt.xlabel("Readout amplitude ")
    plt.ylabel("SNR")
    plt.grid("on")
    # print(f"The optimal readout frequency is {dfs[np.argmax(SNR1)] + resonator_IF_q1} Hz (SNR={max(SNR1)})")


def get_signal_amplitude( data ):
    """
    data shape (2,2,N)
    axis 0 g,e
    axis 1 I,Q
    axis 2 N frequency
    """
    s21_g = data[0][0] +1j*data[0][1] 
    s21_e = data[1][0] +1j*data[1][1]
    signal = np.abs(s21_g -s21_e)
    return signal

if __name__ == '__main__':

    n_avg = 4000
    # The frequency sweep around the resonators' frequency "resonator_IF_q"
    dfs = np.arange(-10e6, 10e6, 0.1e6)
    operate_qubit = ["q1_xy", "q2_xy"]
    ro_element = ["rr1","rr2"]
    data = freq_dep_signal( dfs, operate_qubit, ro_element, n_avg, config, qmm)
    for r in ro_element:
        plot_freq_signal( dfs, data[r], r )

    amps = np.linspace(0, 1.8, 180)
    data = power_dep_signal( amps, operate_qubit, ro_element, n_avg, config, qmm)
    for r in ro_element:
        plot_amp_signal( amps, data[r], r )