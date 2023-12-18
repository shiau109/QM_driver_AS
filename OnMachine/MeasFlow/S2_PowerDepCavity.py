"""
        RESONATOR SPECTROSCOPY VERSUS READOUT AMPLITUDE
This sequence involves measuring the resonator by sending a readout pulse and demodulating the signals to
extract the 'I' and 'Q' quadratures.
This is done across various readout intermediate frequencies and amplitudes.
Based on the results, one can determine if a qubit is coupled to the resonator by noting the resonator frequency
splitting. This information can then be used to adjust the readout amplitude, choosing a readout amplitude value
just before the observed frequency splitting.

Prerequisites:
    - Calibration of the time of flight, offsets, and gains (referenced as "time_of_flight").
    - Calibration of the IQ mixer connected to the readout line (be it an external mixer or an Octave port).
    - Identification of the resonator's resonance frequency (referred to as "resonator_spectroscopy_multiplexed").
    - Configuration of the readout pulse amplitude (the pulse processor will sweep up to twice this value) and duration.
    - Specification of the expected resonator depletion time in the configuration.

Before proceeding to the next node:
    - Update the readout frequency, labeled as "resonator_IF_q", in the configuration.
    - Adjust the readout amplitude, labeled as "readout_amp_q", in the configuration.
"""

from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.loops import from_array, qua_logspace
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import warnings
import matplotlib.pyplot as plt
from numpy import arange
warnings.filterwarnings("ignore")
from OnMachine.Octave_Config.QM_config_dynamic import u

###################
#   Data Saving   #
###################
from datetime import datetime
import sys


###################
# The QUA program #
###################


def mRO_power_dep_resonator( ro_element:list, config:dict, qm_machine:QuantumMachinesManager, n_avg:int=100, freq_span_MHz:int=5, freq_resolu_MHz:float=0.05, amp_max_ratio:float=1.5,amp_resolu:float=0.01, initializer:tuple=None)->list:
    """
    df_array ref is IF on config
    """

    dfs = arange(-freq_span_MHz*u.MHz,(freq_span_MHz+0.1)*u.MHz,freq_resolu_MHz*u.MHz)
    amp_ratio = arange(0.01,amp_max_ratio+0.01,amp_resolu)
    plot_freq_x = arange(-freq_span_MHz,(freq_span_MHz+0.1),freq_resolu_MHz)
    
    center_IF = {}
    for r in ro_element:
        center_IF[r] = config["elements"][r]["intermediate_frequency"]
    
    freq_len = dfs.shape[-1]
    amp_ratio_len = amp_ratio.shape[-1]

    with program() as multi_res_spec_vs_amp:
        
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)
        n_st = declare_stream()
        df = declare(int)
        a = declare(fixed)

        with for_(n, 0, n < n_avg, n + 1):
            # with for_(*qua_logspace(a, -1, 0, 2)):
            with for_(*from_array(a, amp_ratio)):
                
                with for_(*from_array(df, dfs)):
                    # Initialization
                    if initializer is None:
                        wait(1*u.us, ro_element)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            print("initializer didn't work!")
                            wait(1*u.us, ro_element)

                    # Operation    
                    for r in ro_element:
                        update_frequency( r, center_IF[r]+df)
                    
                    # Readout
                    multiRO_measurement( iqdata_stream, ro_element, amp_modify=a, weights='rotated_' )

            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            # Cast the data into a 2D matrix, average the 2D matrices together and store the results on the OPX processor
            # NOTE that the buffering goes from the most inner loop (left) to the most outer one (right)
            multiRO_pre_save( iqdata_stream, ro_element, (amp_ratio_len, freq_len))


    qm = qm_machine.open_qm(config)
    job = qm.execute(multi_res_spec_vs_amp)
    ro_ch_name = []
    for r_name in ro_element:
        ro_ch_name.append(f"{r_name}_I")
        ro_ch_name.append(f"{r_name}_Q")

    data_list = ro_ch_name + ["iteration"]   
    results = fetching_tool(job, data_list=data_list, mode="live")
    output_data = {}
    while results.is_processing():
        fetch_data = results.fetch_all()
        for r_idx, r_name in enumerate(ro_element):
            output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])
        iteration = fetch_data[-1]
        # Progress bar
        progress_counter(iteration, n_avg, start_time=results.get_start_time())        
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    return [output_data,plot_freq_x,amp_ratio]

def plot_power_dep_resonator( dfs, amp_ratio, data, ax=None ):
    """
    data shape ( 2, N, M )
    2 is I,Q
    N is freq
    M is RO amp
    """
    idata = data[0]
    qdata = data[1]
    zdata = idata +1j*qdata
    s21 = zdata/amp_ratio[:,None]

    if ax==None:
        fig, ax = plt.subplots()
        ax.set_title('pcolormesh')
        fig.show()
    ax.pcolormesh(dfs, amp_ratio, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)


if __name__ == '__main__':
    # 20231216 Test complete :Ratis
    from OnMachine.Octave_Config.QM_config_dynamic import Circuit_info, QM_config, initializer
    from OnMachine.MeasFlow.ConfigBuildUp import spec_loca, config_loca, qubit_num
    spec = Circuit_info(qubit_num)
    config = QM_config()
    spec.import_spec(spec_loca)
    config.import_config(config_loca)
    
    qmm,_ = spec.buildup_qmm()
    init_macro = initializer(spec.give_depletion_time_for("all"),mode='depletion')
    
    n_avg = 200  # The number of averages
    # The frequency sweep around the resonators' frequency "resonator_IF_q"

    ro_elements = ["q1_ro","q2_ro","q3_ro","q4_ro"]
    data = mRO_power_dep_resonator( ro_elements, config.get_config(), qmm, n_avg=200, amp_max_ratio=1.25, initializer=init_macro)  
    results = data[0]
    dfs = data[1]
    amps = data[-1]
    for r in ro_elements:
        fig, ax = plt.subplots()
        plot_power_dep_resonator(dfs, amps, results[r], ax)
        ax.set_title(r)
        ax.set_xlabel("additional IF freq (MHz)")
        ax.set_ylabel("amp scale")
    plt.show()
 
