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

def CZ(time_max,time_resolution,z_amps_range,z_amps_resolution,ro_element,flux_Qi,excited_Qi,flux_Ci,coupler_z,preprocess,qmm,config,n_avg=1,initializer=None,simulate=True):
    cc_resolution = (time_resolution/4.)*u.us
    cc_max_qua = (time_max/4.)*u.us
    cc_qua = np.arange( 4, cc_max_qua, cc_resolution)
    print(cc_qua)
    evo_time = cc_qua*4
    
    z_amps_array = np.arange(z_amps_range[0],z_amps_range[1],z_amps_resolution)
    amp_len = len(z_amps_array)
    time_len = len(evo_time)

    with program() as cz:
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)
        n_st = declare_stream()
        cc = declare(int)  
        z_amps = declare(fixed)
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(z_amps, z_amps_array)):
                with for_(*from_array(cc,cc_qua )):
                    # initializaion
                    if initializer is None:
                        wait(1*u.us,ro_element)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            wait(1*u.us,ro_element)
                    
                    # operation
                    if excited_Qi != []: 
                        for excited_Qi in excited_Qi:
                            play("x180", f"q{excited_Qi}_xy")
                    align()
                    wait(40 *u.ns)
                    play("const" * amp(z_amps*2), f"q{flux_Qi}_z", duration=cc)
                    play("const" * amp(coupler_z*2),f"q{flux_Ci}_z",duration=cc) 
                    wait(40 *u.ns)
                    wait(cc)
                    multiRO_measurement(iqdata_stream, ro_element, weights="rotated_") 
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            match preprocess:
                case "shot":
                    multiRO_pre_save(iqdata_stream, ro_element, (n_avg,amp_len,time_len) ,stream_preprocess="shot")
                case _:
                    multiRO_pre_save(iqdata_stream, ro_element, (amp_len,time_len))
    if simulate:
        simulation_config = SimulationConfig(duration=20000)  # In clock cycles = 4ns
        job = qmm.simulate(config, cz, simulation_config)
        job.get_simulated_samples().con1.plot()
        job.get_simulated_samples().con2.plot()
        plt.show()
    else:
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
        match preprocess:
            case "shot":
                for r_idx, r_name in enumerate(ro_element):
                    output_data[r_name] = ( ["mixer","shot","amps","time"],
                                np.squeeze(np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) ))
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]), "shot":np.arange(n_avg),"amps":z_amps_array, "time": evo_time }
                )
            case _:
                for r_idx, r_name in enumerate(ro_element):
                    output_data[r_name] = ( ["mixer","amps","time"],
                                np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]), "amps":z_amps_array, "time": evo_time }
                )
        return dataset 

def CZ_couplerz(z_amps_range,z_amps_resolution,couplerz_amps_range,couplerz_amps_resolution,ro_element,flux_Qi,excited_Qi,flux_Ci,preprocess,qmm,config,n_avg=100,initializer=None,simulate=True):
    """
    find the point of turn off qubit-qubit coupling with coupler\n
    z pulse time is fixed at 80 ns
    """
    z_amps_array = np.arange(z_amps_range[0],z_amps_range[1],z_amps_resolution)
    couplerz_amps_array = np.arange(couplerz_amps_range[0],couplerz_amps_range[1],couplerz_amps_resolution)
    amps_len = len(z_amps_array)
    camps_len = len(couplerz_amps_array)

    with program() as cz:
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)
        n_st = declare_stream()
        couplerz_amps = declare(fixed)  
        z_amps = declare(fixed)
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(couplerz_amps, couplerz_amps_array)):
                with for_(*from_array(z_amps,z_amps_array )):
                    # initializaion
                    if initializer is None:
                        wait(1*u.us,ro_element)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            wait(1*u.us,ro_element)
                    
                    # operation
                    if excited_Qi != []: 
                        for excited_Qi in excited_Qi:
                            play("x180", f"q{excited_Qi}_xy")
                    align()
                    wait(40 *u.ns)
                    play("const" * amp(z_amps*2), f"q{flux_Qi}_z", duration=40)
                    play("const" * amp(couplerz_amps*2), f"q{flux_Ci}_z", duration=40)
                    align()               
                    wait(40 * u.ns)
                    multiRO_measurement(iqdata_stream, ro_element, weights="rotated_") 
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            match preprocess:
                case "shot":
                    multiRO_pre_save(iqdata_stream, ro_element, (n_avg,camps_len,amps_len) ,stream_preprocess="shot")
                case _:
                    multiRO_pre_save(iqdata_stream, ro_element, (camps_len,amps_len))
    if simulate:
        simulation_config = SimulationConfig(duration=20000)  # In clock cycles = 4ns
        job = qmm.simulate(config, cz, simulation_config)
        job.get_simulated_samples().con1.plot()
        job.get_simulated_samples().con2.plot()
        plt.show()
    else:
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

        match preprocess:
            case "shot":
                for r_idx, r_name in enumerate(ro_element):
                    output_data[r_name] = ( ["mixer","shot","c_amps","amps"],
                                np.squeeze(np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) ))
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]), "shot":np.arange(n_avg),"c_amps":couplerz_amps_array, "amps": z_amps_array }
                )
            case _:
                for r_idx, r_name in enumerate(ro_element):
                    output_data[r_name] = ( ["mixer","c_amps","amps"],
                                np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]), "c_amps": couplerz_amps_array, "amps": z_amps_array }
                )

        return dataset
def plot_cz_chavron(x,y,z,ax=None):
    """
    x in shape (N,) \n
    y in shape (M,) \n
    z in shape (M,N) \n
    N is pulse time \n
    M is flux
    """
    if ax == None:
        fig, ax = plt.subplots()
    ax.set_title('pcolormesh')
    ax.set_xlabel("interaction time (ns)")
    ax.set_ylabel("qubit flux (V)")
    a1 = ax.pcolormesh(x,y,z,cmap='RdBu')
    plt.colorbar(a1,ax=ax, label="|11> population")

def plot_cz_couplerz(x,y,z,ax=None):
    """
    x in shape (N,) \n
    y in shape (M,) \n
    z in shape (M,N) \n
    N is qubit flux \n
    M is coupler flux
    """
    if ax == None:
        fig, ax = plt.subplots()
    ax.set_title('pcolormesh')
    ax.set_xlabel("qubit flux (V)")
    ax.set_ylabel("coupler flux (V)")
    a1 = ax.pcolormesh(x,y,z,cmap='RdBu')
    plt.colorbar(a1,ax=ax, label="|10> population")

