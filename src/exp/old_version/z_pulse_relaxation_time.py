from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
from qualang_tools.plot.fitting import Fit
# from common_fitting_func import gaussian
import exp.config_par as gc
from scipy.optimize import curve_fit
import warnings
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import xarray as xr
warnings.filterwarnings("ignore")
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
import time
def exp_z_pulse_relaxation_time(max_time, time_resolution, flux_range:tuple, flux_resolution:float, q_name:list, z_name:list, ro_element:list, config, qmm:QuantumMachinesManager, n_avg=100, initializer=None ):
    """
    parameters: \n
    max_time: unit in us, can't < 20 ns \n
    time_resolution: unit in us, can't < 4 ns \n

    Return: \n
    xarray with value 2*N array \n
    coors: ["mixer","z_voltage","time"]\n
    attrs: z_offset\n
    time unit in ns \n
    """

    fluxes = np.arange(flux_range[0], flux_range[1], flux_resolution)
    fluxes_len = fluxes.shape[-1]

    cc_max_qua = (max_time/4) * u.us
    cc_resolution_qua = (time_resolution/4) * u.us
    cc_delay_qua = np.arange( 4, cc_max_qua, cc_resolution_qua)
    evo_time = cc_delay_qua*4
    evo_time_len = cc_delay_qua.shape[-1]
    
    ref_z_offset = {}
    for z in z_name:
        ref_z_offset[z] = gc.get_offset(z, config)
    # QUA program
    with program() as t1:

        iqdata_stream = multiRO_declare( ro_element )
        t = declare(int)  
        dc = declare(fixed)  
        n = declare(int)
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(dc, fluxes)):
                with for_(*from_array(t, cc_delay_qua)):
                    # initializaion
                    if initializer is None:
                        wait(1*u.us,ro_element)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            wait(1*u.us,ro_element)

                    # Operation   
                    for q in q_name:
                        play("x180", q)
                    wait(25)    
                    for z_name, ref_z in ref_z_offset.items():
                        set_dc_offset( z_name, "single", ref_z +dc)
                        # assign(index, 0)
                    wait(t)
                    for z_name, ref_z in ref_z_offset.items():
                        set_dc_offset( z_name, "single", ref_z)
                    wait(25)                         
                    # align()
                    # Readout
                    multiRO_measurement( iqdata_stream,  resonators=ro_element, weights="rotated_")
                
            # Save the averaging iteration to get the progress bar
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            multiRO_pre_save(iqdata_stream, ro_element, (fluxes_len,evo_time_len) )

    qm = qmm.open_qm(config)
    job = qm.execute(t1)

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
        time.sleep(1)
    # Measurement finished
    fetch_data = results.fetch_all()
    qm.close()
    output_data = {}

    for r_idx, r_name in enumerate(ro_element):
        output_data[r_name] = ( ["mixer","z_voltage","time"],
                               np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
    dataset = xr.Dataset(
        output_data,
        coords={ "mixer":np.array(["I","Q"]), "time": evo_time, "z_voltage":fluxes }
    )
    
    dataset.attrs["z_offset"] = list(ref_z_offset.values())

    return dataset



