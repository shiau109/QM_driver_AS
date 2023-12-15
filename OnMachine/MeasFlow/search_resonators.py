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
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.loops import from_array
import warnings
from OnMachine.Octave_Config.QM_config_dynamic import Circuit_info, QM_config, initializer,u
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
warnings.filterwarnings("ignore")
from numpy import arange


###################
# The QUA program #
###################
# ro_element = "rr1"  # The resonator element
# n_avg = 10000  # The number of averages
# # The frequency sweep parameters
# frequencies = np.arange(-247e6, -227e6, 0.01e6)

def search_resonators( freq_span_Hz:float, config:dict, ro_element:list, qm_machine:QuantumMachinesManager, n_avg:int=10000, initializer:tuple=None):
    reso_Hz = 2e6 # 2 MHz/point
    frequencies = arange(-1*freq_span_Hz,freq_span_Hz,reso_Hz)
    freq_len = frequencies.shape[-1]

    with program() as resonator_spec:

        f = declare(int)  # QUA variable for the readout frequency --> Hz int 32 up to 2^32
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)
        n_st = declare_stream()

        with for_(n, 0, n < n_avg, n + 1):  # QUA for_ loop for averaging
            with for_(*from_array(f, frequencies)):  # QUA for_ loop for sweeping the frequency
                # Initialization
                # Wait for the resonator to deplete
                if initializer is None:
                    wait(1 * u.us, ro_element[0])
                else:
                    try:
                        initializer[0](*initializer[1])
                    except:
                        print("initializer didn't work!")
                        wait(1 * u.us, ro_element[0]) 
                # Operation
                # Update the frequency of the digital oscillator linked to the resonator element
                update_frequency( ro_element[0], f)
                # Readout
                # Measure the resonator (send a readout pulse and demodulate the signals to get the 'I' & 'Q' quadratures)
                multiRO_measurement( iqdata_stream, ro_element,weights="rotated_") 
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
    qm = qm_machine.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(resonator_spec)
    # Get results from QUA program
    results = fetching_tool(job, data_list=[f"{ro_element[0]}_I", f"{ro_element[0]}_Q", "iteration"], mode="wait_for_all")
    output_data = results.fetch_all()
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    return output_data

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    spec = Circuit_info(q_num=5)
    config = QM_config()
    spec.import_spec("/Users/ratiswu/Documents/GitHub/QM_opt/OnMachine/Octave_Config/test_spec")
    config.import_config("/Users/ratiswu/Documents/GitHub/QM_opt/OnMachine/Octave_Config/test_config")
    qmm, _ = spec.buildup_qmm()
    freq_span = 400e6 # MHz
    init_macro = initializer(spec.give_depletion_time_for("q1"),mode='depletion')
    idata, qdata, repetition = search_resonators(freq_span,config.get_config(),["q1_ro"],qmm,50,initializer=init_macro)  
    zdata = idata +1j*qdata
    search_range = arange(-1*freq_span,freq_span,2e6)
    plt.plot(search_range, np.abs(zdata),label="Origin")
    plt.show()
