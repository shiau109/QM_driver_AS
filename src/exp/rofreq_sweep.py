
from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.loops import from_array
import warnings

from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save

warnings.filterwarnings("ignore")
import exp.config_par as gc
import xarray as xr
import time
# 20240202 Test complete :Jacky

def frequency_sweep( config:dict, qm_machine:QuantumMachinesManager, ro_element:list=["q0_ro"], freq_range:tuple=(-400,400), resolution:int=2, n_avg:int=100, initializer:tuple=None)->xr.Dataset:
    """
    Parameters:
    Search cavities with the given IF range along the given ro_element's LO, (LO+freq_range[0],LO+freq_range[1]) .\n

    freq_range:\n
    is a tuple ( upper, lower ), Unit in MHz.\n
    resolution:\n
    unit in MHz.\n
    ro_element: ["q1_ro"], temporarily support only 1 element in the list.\n
    initializer: from `initializer(paras,mode='depletion')`, and use paras return from `Circuit_info.give_depletion_time_for()`  
    Return: \n

    """
    freq_r1_qua = freq_range[0] * u.MHz
    freq_r2_qua = freq_range[1] * u.MHz
    resolution_qua = resolution * u.MHz

    frequencies_qua = np.arange( freq_r1_qua, freq_r2_qua, resolution_qua )
    frequencies_mhz = frequencies_qua/1e6 #  Unit in MHz
    freq_len = frequencies_qua.shape[-1]

    ref_xy_LO = {}
    for xy in ro_element:
        ref_xy_LO[xy] = gc.get_LO(ro_element[0],config)

    # The QUA program #
    with program() as resonator_spec:

        f = declare(int)  # QUA variable for the readout frequency --> Hz int 32 up to 2^32
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)
        n_st = declare_stream()

        with for_(n, 0, n < n_avg, n + 1):  # QUA for_ loop for averaging
            with for_(*from_array(f, frequencies_qua)):  # QUA for_ loop for sweeping the frequency
                # Initialization
                # Wait for the resonator to deplete
                if initializer is None:
                    wait(10 * u.us, ro_element[0])
                else:
                    try:
                        initializer[0](*initializer[1])
                    except:
                        print("initializer didn't work!")
                        wait(1 * u.us, ro_element[0]) 
                # Operation
                update_frequency( ro_element[0], f)
                # Readout
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
        # Fetch results
        fetch_data = results.fetch_all()
        # Progress bar
        iteration = fetch_data[-1]
        progress_counter(iteration, n_avg, start_time=results.start_time)
        time.sleep(1)
        

    # Creating an xarray dataset
    fetch_data = results.fetch_all()
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    
    output_data = np.array([fetch_data[0],fetch_data[1]])
    dataset = xr.Dataset(
        {
            ro_element[0]: (["mixer","frequency"], output_data),
        },
        coords={"frequency": frequencies_mhz, "mixer":np.array(["I","Q"]) }
    )
    return dataset

def plot_CS(x:np.ndarray,idata:np.ndarray,qdata:np.ndarray,plot:bool=False,save:bool=False):
    amp = np.absolute(idata +1j*qdata)
    pha = np.unwrap(np.diff(np.arctan2(qdata,idata),append=np.mean(np.diff(np.arctan2(qdata,idata)))))
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
    import matplotlib.pyplot as plt
    # from configuration import *

    search_range = np.arange(-400e6, 400e6, 0.5e6)
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

    idata, qdata, repetition = search_resonators(search_range,config,"rr1",100,qmm)  
    zdata = idata +1j*qdata
    plt.plot(search_range, np.abs(zdata),label="Origin")
    plt.show()
