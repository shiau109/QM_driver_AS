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
from configuration import *
from qualang_tools.loops import from_array, qua_logspace
from QM_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import warnings

warnings.filterwarnings("ignore")

###################
#   Data Saving   #
###################
from datetime import datetime
import sys


###################
# The QUA program #
###################


def mRO_power_dep_resonator( freq_IF_center:list, df_array, amp_ratio, cd_time, n_avg, config, ro_element:list, qmm:QuantumMachinesManager)->dict:
    """

    """
    trans_freq_IF_center = []
    for cif in freq_IF_center:
        trans_freq_IF_center.append(cif * u.MHz)
    ro_channel_num = len(ro_element)
    freq_len = df_array.shape[-1]
    
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
                
                with for_(*from_array(df, df_array)):
                        
                    for i in range(ro_channel_num):
                        update_frequency(ro_element[i], trans_freq_IF_center[i]+df)

                    multiRO_measurement( iqdata_stream, ro_element, amp_modify=a )

                    wait(cd_time, ro_element)

            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            # Cast the data into a 2D matrix, average the 2D matrices together and store the results on the OPX processor
            # NOTE that the buffering goes from the most inner loop (left) to the most outer one (right)
            multiRO_pre_save( iqdata_stream, ro_element, (amp_ratio_len, freq_len))
    #######################
    # Simulate or execute #
    #######################

    qm = qmm.open_qm(config)
    job = qm.execute(multi_res_spec_vs_amp)
    ro_ch_name = []
    for r_name in ro_element:
        ro_ch_name.append(f"{r_name}_I")
        ro_ch_name.append(f"{r_name}_Q")

    data_list = ro_ch_name + ["iteration"]   
    results = fetching_tool(job, data_list=data_list, mode="wait_for_all")
    fetch_data = results.fetch_all()
    output_data = {}
    for r_idx, r_name in enumerate(ro_element):
        output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    return output_data

def myplot( data ):
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

    fig, ax = plt.subplots()
    c = ax.pcolormesh(dfs, amp_log_ratio, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    ax.set_title('pcolormesh')
    fig.show()

    return fig
    
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
    n_avg = 100  # The number of averages
    # The frequency sweep around the resonators' frequency "resonator_IF_q"

    span = 10 * u.MHz
    df = 0.1 * u.MHz
    dfs = np.arange(-span, +span + 0.1, df)
    freq_IF = [ -215.5, 74 ]

    # The readout amplitude sweep (as a pre-factor of the readout amplitude) - must be within [-2; 2)
    a_min = 0.05
    a_max = 1.99
    da = 0.05
    amp_ratio = np.logspace(-2, 0, 10)  # The amplitude vector +da/2 to add a_max to the scan
    amp_log_ratio = np.log10(amp_ratio)
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
    

    output_data = mRO_power_dep_resonator(freq_IF, dfs, amp_ratio,1000,n_avg,config,["rr1","rr2"],qmm)  



    
    mfg = myplot(output_data)
    mfg.show()
    plt.show()