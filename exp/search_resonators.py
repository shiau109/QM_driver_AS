"""
        RESONATOR SPECTROSCOPY INDIVIDUAL RESONATORS
This sequence involves measuring the resonator by sending a readout pulse and demodulating the signals to extract the
'I' and 'Q' quadratures across varying readout intermediate frequencies.
The data is then post-processed to determine the resonator resonance frequency.
This frequency can be used to update the readout intermediate frequency in the configuration under "resonator_IF".

Prerequisites:
    - Ensure calibration of the time of flight, offsets, and gains (referenced as "time_of_flight").
    - Calibrate the IQ mixer connected to the readout line (whether it's an external mixer or an Octave port).
    - Define the readout pulse amplitude and duration in the configuration.
    - Specify the expected resonator depletion time in the configuration.

Before proceeding to the next node:
    - Update the readout frequency, labeled as "resonator_IF_q1" and "resonator_IF_q2", in the configuration.
"""

from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from configuration import *
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.loops import from_array
import warnings

from QM_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save

warnings.filterwarnings("ignore")

###################
#   Data Saving   #
###################
from datetime import datetime
import sys

###################
# The QUA program #
###################
# ro_element = "rr1"  # The resonator element
# n_avg = 10000  # The number of averages
# # The frequency sweep parameters
# frequencies = np.arange(-247e6, -227e6, 0.01e6)

def search_resonators( frequencies, config, ro_element, n_avg, qmm:QuantumMachinesManager):
    
    freq_len = frequencies.shape[-1]

    with program() as resonator_spec:

        f = declare(int)  # QUA variable for the readout frequency --> Hz int 32 up to 2^32

        iqdata_stream = multiRO_declare( ro_element )

        n = declare(int)
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):  # QUA for_ loop for averaging
            with for_(*from_array(f, frequencies)):  # QUA for_ loop for sweeping the frequency
                # Update the frequency of the digital oscillator linked to the resonator element
                update_frequency( ro_element, f)
                # Measure the resonator (send a readout pulse and demodulate the signals to get the 'I' & 'Q' quadratures)
                multiRO_measurement( iqdata_stream, ro_element) 
                # Wait for the resonator to deplete
                wait(depletion_time * u.ns, ro_element)
            # Save the averaging iteration to get the progress bar
            save(n, n_st)

        with stream_processing():
            # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
            multiRO_pre_save( iqdata_stream, ro_element, (freq_len,))
            n_st.save("iteration")
    ###########
    # execute #
    ###########
    # Open a quantum machine to execute the QUA program
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(resonator_spec)
    # Get results from QUA program
    results = fetching_tool(job, data_list=[f"{ro_element}_I", f"{ro_element}_Q", "iteration"], mode="wait_for_all")
    output_data = results.fetch_all()
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    return output_data

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    search_range = np.arange(-400e6, 400e6, 0.5e6)
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

    idata, qdata, repetition = search_resonators(search_range,config,"rr1",100,qmm)  
    zdata = idata +1j*qdata
    plt.plot(search_range, np.abs(zdata),label="Origin")
    plt.show()
