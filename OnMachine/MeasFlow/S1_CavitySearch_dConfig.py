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
from numpy import arange, ndarray, absolute, arctan2, diff, array, mean, unwrap
import matplotlib.pyplot as plt


###################
# The QUA program #
###################
# ro_element = "rr1"  # The resonator element
# n_avg = 10000  # The number of averages
# # The frequency sweep parameters
# frequencies = np.arange(-247e6, -227e6, 0.01e6)

def search_resonators( config:dict, ro_element:list, qm_machine:QuantumMachinesManager, freq_span_MHz:int=400, resolu_MHz:int=2, n_avg:int=100, initializer:tuple=None):
    """
        Search cavities with the given IF span range along the given ro_element's LO.\n
        ro_element: ["q1_ro"], temporarily support only 1 element in the list.\n
        initializer: from `initializer(paras,mode='depletion')`, and use paras return from `Circuit_info.give_depletion_time_for()`  
    """
    plot_x = arange(-1*freq_span_MHz,(freq_span_MHz+0.1),resolu_MHz)
    frequencies = arange(-1*freq_span_MHz*1e6,(freq_span_MHz+0.1)*1e6,resolu_MHz*1e6)
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
    results = fetching_tool(job, data_list=[f"{ro_element[0]}_I", f"{ro_element[0]}_Q", "iteration"], mode="live")

    while results.is_processing():
        output_data = results.fetch_all()
        progress_counter(output_data[-1], n_avg, start_time=results.get_start_time())
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    return output_data[0], output_data[1], plot_x

def plot_CS(x:ndarray,idata:ndarray,qdata:ndarray,plot:bool=False,save:bool=False):
    amp = absolute(idata +1j*qdata)
    pha = unwrap(diff(arctan2(qdata,idata),append=mean(diff(arctan2(qdata,idata)))))
    fig, ax = plt.subplots(2,1)
    ax[0].plot(x,amp)
    ax[0].set_title('Amplitude')
    ax[0].set_xlabel("IF frequency (MHz)")
    ax[1].plot(x,pha)
    ax[1].set_title('Phase')
    ax[1].set_xlabel("IF frequency (MHz)")
    plt.tight_layout()
    if save:
        plt.savefig()
    if plot:
        plt.show()

if __name__ == '__main__':
    # 20231215 Test complete :Ratis

    from OnMachine.MeasFlow.ConfigBuildUp import spec_loca, config_loca, qubit_num
    spec = Circuit_info(qubit_num)
    config = QM_config()
    spec.import_spec(spec_loca)
    config.import_config(config_loca)
    qmm, _ = spec.buildup_qmm()
    init_macro = initializer(spec.give_depletion_time_for("q1"),mode='depletion')
    idata, qdata, sweep_range = search_resonators(config.get_config(),["q1_ro"],qmm,n_avg=50,initializer=init_macro)  
    
    plot_CS(sweep_range,idata,qdata,plot=True)

    
 

    
