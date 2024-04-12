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
import exp.config_par as gc


def frequency_sweep_power_dep( ro_element:list, config:dict, qm_machine:QuantumMachinesManager, n_avg:int=100, freq_range:tuple=(-5,5), freq_resolution:float=0.05, amp_max_ratio:float=1.5,amp_resolution:float=0.01, amp_scale:str='lin', initializer:tuple=None)->xr.Dataset:
    """
    Parameters:\n
    freq_span:\n
        a tuple (upper, lower) Unit in MHz, \n
    amp_max_ratio: \n

    amp_scale: \n
        lin or log \n
    Return: xarray dataset
        coords : frequency, amp_ratio
    """
    freq_r1_qua = freq_range[0] * u.MHz
    freq_r2_qua = freq_range[1] * u.MHz
    freq_resolution_qua = freq_resolution * u.MHz

    freqs_qua = np.arange(freq_r1_qua,freq_r2_qua,freq_resolution_qua )
    if amp_scale == "log":
        amp_num = int((amp_max_ratio+2)/amp_resolution)
        amp_ratio = np.logspace(-2, amp_max_ratio, amp_num)
    else:
        amp_ratio = np.arange(amp_max_ratio/100,amp_max_ratio,amp_resolution)
    freqs_mhz = freqs_qua/1e6 #  Unit in MHz

    ref_ro_IF = {}
    ref_ro_LO = {}
    for r in ro_element:
        ref_ro_IF[r] = gc.get_IF(r,config)
        ref_ro_LO[r] = gc.get_LO(r,config)


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
                        update_frequency( r, ref_ro_IF[r]+df)
                    
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

    dataset.attrs["ro_LO"] = list(ref_ro_LO.values())
    dataset.attrs["ro_IF"] = list(ref_ro_IF.values())


    return dataset

def plot_power_dep_resonator( freqs, amp_ratio, data, ax=None, yscale="lin" ):
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
    if yscale == "log":
        pcm = ax.pcolormesh(freqs, np.log10(amp_ratio), np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    else:
        pcm = ax.pcolormesh(freqs, amp_ratio, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    plt.colorbar(pcm, label='Value')


if __name__ == '__main__':
    pass