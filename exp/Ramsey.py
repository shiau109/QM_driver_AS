"""
        RAMSEY CHEVRON (IDLE TIME VS FREQUENCY)
The program consists in playing a Ramsey sequence (x90 - idle_time - x90 - measurement) for different qubit intermediate
frequencies and idle times.
From the results, one can estimate the qubit frequency more precisely than by doing Rabi and also gets a rough estimate
of the qubit coherence time.

Prerequisites:
    - Having found the resonance frequency of the resonator coupled to the qubit under study (resonator_spectroscopy).
    - Having calibrated qubit pi pulse (x180) by running qubit, spectroscopy, rabi_chevron, power_rabi and updated the config.
    - (optional) Having calibrated the readout (readout_frequency, amplitude, duration_optimization IQ_blobs) for better SNR.
    - Set the desired flux bias.

Next steps before going to the next node:
    - Update the qubit frequency (qubit_IF_q) in the configuration.
"""

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
from macros import qua_declaration, multiplexed_readout
from QM_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save

import warnings

warnings.filterwarnings("ignore")


def detune_ramsey( dfs, times, q_name:list, ro_element:list, n_avg, config, qmm:QuantumMachinesManager):
    """
    Output shape (N,M) 2D data
    N is evolution time ( unit in tick )
    M is detuned frequency
    """
    center_IF = {}
    for r in ro_element:
        center_IF[r] = config["elements"][r]["intermediate_frequency"]
    freq_len = dfs.shape[-1]
    time_len = times.shape[-1]

    ###################
    # The QUA program #
    ###################

    with program() as ramsey:
        iqdata_stream = multiRO_declare(ro_element)
        t = declare(int)  # QUA variable for the idle time
        df = declare(int)  # QUA variable for the qubit frequency
        n = declare(int)

        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(df, dfs)):
                # Update the frequency of the two qubit elements
                for r in ro_element:
                    update_frequency(r, df + center_IF[r])

                with for_(*from_array(t, times)):
                # Measure the excited IQ blobs
                    for name in q_name:
                        play("x90", name)
                        wait(t, name)
                        play("x90", name)
                    # Align the elements to measure after having waited a time "tau" after the qubit pulses.
                    align()
                    # Measure the state of the resonators
                    multiRO_measurement(iqdata_stream, ro_element, weights="rotated_")
                    # Wait for the qubit to decay to the ground state
                    wait(thermalization_time * u.ns)

        with stream_processing():
            multiRO_pre_save( iqdata_stream, ro_element, (freq_len,time_len)  )
   
    # Open the quantum machine
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(ramsey)
    # Tool to easily fetch results from the OPX (results_handle used in it)
    data_list = []
    for r in ro_element:
        data_list.append(f"{r}_I")
        data_list.append(f"{r}_Q")


    results = fetching_tool(job, data_list=data_list, mode="wait_for_all")
    fetch_data = results.fetch_all()
    output_data = {}
    for r_idx, r_name in enumerate(ro_element):
        output_data[r_name] = np.array(
            [fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) 

    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    return output_data

def plot_ramsey_chavron( x, y, data, title:str, center_freq:float=0):
        plt.suptitle("Ramsey chevron")
        plt.subplot(201)
        plt.pcolor(x, y, data[0])
        plt.title(f"{title} I, fcent={center_freq} MHz")
        plt.ylabel("Frequency detuning [MHz]")
        plt.subplot(202)
        plt.pcolor( x, y, data[1])
        plt.title(f"{title} 1 Q")
        plt.xlabel("Idle time [ns]")
        plt.ylabel("Frequency detuning [MHz]")

if __name__ =='__main__':
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
    n_avg = 1000  # Number of averages
    q_name = ["q1_xy"]
    ro_elements = ["rr1", "rr2"]
    dfs = np.arange(-10e6, 10e6, 0.1e6)  # Frequency detuning sweep in Hz
    tick = np.arange(4, 300, 4)  # Idle time sweep in clock cycles (Needs to be a list of integers)
    time = tick*4.0
    data = detune_ramsey( dfs, tick, q_name, ro_elements, n_avg, config, qmm)
    for r in ro_elements:
        plot_ramsey_chavron( time, dfs, data[r], r)