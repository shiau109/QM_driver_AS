from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
from qualang_tools.units import unit
import numpy as np
import time
import xarray as xr
import warnings
u = unit(coerce_to_integer=True)
warnings.filterwarnings("ignore")

def CZ(time_max,time_resolution,amps_max,amps_resolution,ro_element,flux_Qi,excited_Qi,qmm,config,n_avg=100,initializer=None):
    cc_resolution = (time_resolution/4.)*u.us
    cc_max_qua = (time_max/4.)*u.us
    cc_qua = np.arange( 4, cc_max_qua, cc_resolution)
    print(cc_qua)
    evo_time = cc_qua*4
    
    amps = np.arange(0,amps_max,amps_resolution)
    amp_len = len(amps)
    time_len = len(evo_time)
    with program() as cz:
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)
        n_st = declare_stream()
        cc = declare(int)  
        a = declare(fixed)
        wait(100 * u.ns)
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(a, amps)):
                with for_(*from_array(cc, cc_qua)):
                    # initializaion
                    if initializer is None:
                        wait(1*u.us,ro_element)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            wait(1*u.us,ro_element)
                    
                    # operation
                    if excited_Qi_list != []: 
                        for excited_Qi in excited_Qi_list:
                            play("x180", f"q{excited_Qi}_xy")
                    align()
                    wait(100 * u.ns)
                    play("const" * amp(a), f"q{flux_Qi}_z", duration=cc)
                    align()               
                    wait(100 * u.ns)
                    align()
                    multiRO_measurement(iqdata_stream, ro_element, weights="rotated_") 
                    wait(100 * u.us)
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            multiRO_pre_save(iqdata_stream, ro_element, (amp_len,time_len) )

    # Open the quantum machine
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(cz)
    # Get results from QUA program
    ro_ch_name = []
    for r_name in ro_element:
        ro_ch_name.append(f"{r_name}_I")
        ro_ch_name.append(f"{r_name}_Q")
    data_list = ro_ch_name + ["iteration"]   
    results = fetching_tool(job, data_list=data_list, mode="live")

    # Live plotting
    while results.is_processing():
        # Fetch results
        fetch_data = results.fetch_all()
        # Progress bar
        iteration = fetch_data[-1]
        progress_counter(iteration, n_avg, start_time=results.start_time)
        # Plot
        plt.tight_layout()
        time.sleep(1)

    # Measurement finished 
    fetch_data = results.fetch_all()
    qm.close()
    output_data = {}

    for r_idx, r_name in enumerate(ro_element):
        output_data[r_name] = ( ["mixer","amplitude","time"],
                            np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
    dataset = xr.Dataset(
        output_data,
        coords={ "mixer":np.array(["I","Q"]), "amplitude":amps, "time": evo_time }
    )

    return dataset 

def plot_cz_chavron(x,y,z,ax=None):
    """
    x in shape (N,)
    y in shape (M,)
    z in shape (M,N)
    N is evo_time
    M is flux
    """
    if ax == None:
        fig, ax = plt.subplots()
    ax.set_title('pcolormesh')
    ax.set_xlabel("flux (V)")
    ax.set_ylabel("interaction time (ns)")
    ax.pcolormesh(x,y,z,cmap='RdBu')
    return fig

