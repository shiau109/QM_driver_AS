from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qualang_tools.results import progress_counter, fetching_tool
# from configuration import *
from qualang_tools.loops import from_array, qua_logspace
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
from datetime import datetime
import sys
import xarray as xr


def frequency_sweep_power_dep( ro_element:list, config:dict, qm_machine:QuantumMachinesManager, n_avg:int=100, freq_span:int=5, freq_resolution:float=0.05, amp_max_ratio:float=1.5,amp_resolu:float=0.01, initializer:tuple=None)->xr.Dataset:
    """
    freq_span:\n
        Unit in MHz, \n

    output: xarray dataset
        coords : frequency, amp_ratio
    """
    freq_span_qua = freq_span * u.MHz
    freq_resolution_qua = freq_resolution * u.MHz

    freqs_qua = np.arange(-freq_span_qua/2,freq_span_qua/2,freq_resolution_qua )
    amp_ratio = np.arange(0.01,amp_max_ratio+0.01,amp_resolu)
    
    freqs_mhz = freqs_qua/1e6 #  Unit in MHz

    center_IF = {}
    for r in ro_element:
        center_IF[r] = config["elements"][r]["intermediate_frequency"]
    
    freq_len = freqs_qua.shape[-1]
    amp_ratio_len = amp_ratio.shape[-1]

    ###################
    # The QUA program #
    ###################
    with program() as multi_res_spec_vs_amp:
        
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)
        n_st = declare_stream()
        df = declare(int)
        a = declare(fixed)

        with for_(n, 0, n < n_avg, n + 1):
            # with for_(*qua_logspace(a, -1, 0, 2)):
            with for_(*from_array(a, amp_ratio)):
                
                with for_(*from_array(df, freqs_qua)):
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

    # Creating an xarray dataset
    fetch_data = results.fetch_all()
    for r_idx, r_name in enumerate(ro_element):
        output_data[r_name] = ( ["mixer","amp_ratio","frequency"],
                               np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
    dataset = xr.Dataset(
        output_data,
        coords={ "mixer":np.array(["I","Q"]), "frequency": freqs_mhz, "amp_ratio": amp_ratio }
    )
    return dataset

def plot_power_dep_resonator( freqs_qua, amp_ratio, data, ax=None ):
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
    ax.pcolormesh(freqs_qua, amp_ratio, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    n_avg = 200  # The number of averages
    # The frequency sweep around the resonators' frequency "resonator_IF_q"

    freq_span = 5 * u.MHz
    df = 0.1 * u.MHz
    freqs_qua = np.arange(-freq_span, +freq_span + 0.1, df)


    # The readout amplitude sweep (as a pre-factor of the readout amplitude) - must be within [-2; 2)
    amp_ratio = np.linspace( 0.05, 1.5, 30)    # Linear
    # amp_ratio = np.logspace(-1, 0, 10)  # Log
    # amp_log_ratio = np.log10(amp_ratio)*10
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
    
    resonators = ["rr1","rr2","rr3","rr4"]
    output_data = mRO_power_dep_resonator( resonators ,freqs_qua, amp_ratio,1000,n_avg,config,qmm)  
    for r in resonators:
        fig, ax = plt.subplots()
        plot_power_dep_resonator(freqs_qua, amp_ratio, output_data[r], ax)
        ax.set_title(r)
    plt.show()
 
