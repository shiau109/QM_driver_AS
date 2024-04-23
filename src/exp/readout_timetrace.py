"""
        RAW ADC TRACES
This script aims to measure data captured within a specific window defined by the measure() function.
We term the digitized, unprocessed data as "raw ADC traces" because they represent the acquired waveforms without any
real-time processing by the pulse processor, such as demodulation, integration, or time-tagging.

The script is useful for inspecting signals prior to demodulation, ensuring the ADCs are not saturated,
correcting any non-zero DC offsets, and estimating the SNR.
"""

from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
import matplotlib.pyplot as plt
from qualang_tools.results import progress_counter, fetching_tool

# Dynamic config
from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from ab.QM_config_dynamic import initializer

import xarray as xr
import exp.config_par as gc
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)


def frequency_sweep_timetrace( freq_range:tuple, resolution:float, depletion_time:float, config:dict, qm_machine:QuantumMachinesManager, ro_element:list, n_avg:int=100)->xr.Dataset:
    """
    Parameters: \n

    depletion_time: \n
        unit in us \n 
    freq_range: \n
        a tuple ( upper, lower ), unit in MHz. \n
    freq_resolution:
        unit in MHz. \n
    flux_range:\n
        unit in voltage.\n
    flux_resolution: \n
        unit in voltage.\n
    Return:
    xarray dataset with \n
    coords: ["mixer","flux","frequency"]\n

    """
    depletion_time = 10 # us

    deplition_cc = (depletion_time/4) * u.us

    freq_r1_qua = freq_range[0] * u.MHz
    freq_r2_qua = freq_range[1] * u.MHz
    resolution_qua = resolution * u.MHz

    frequencies_qua = np.arange( freq_r1_qua, freq_r2_qua, resolution_qua )
    frequencies_mhz = frequencies_qua/1e6 #  Unit in MHz
    freq_len = frequencies_qua.shape[-1]

    ref_ro_IF = {}
    ref_ro_LO = {}
    for r in ro_element:
        ref_ro_IF[r] = gc.get_IF(r,config)
        ref_ro_LO[r] = gc.get_LO(r,config)
    ###################
    # The QUA program #
    ###################
    with program() as raw_trace_prog:
        n = declare(int)  # QUA variable for the averaging loop
        adc_st = declare_stream(adc_trace=True)  # The stream to store the raw ADC trace

        with for_(n, 0, n < n_avg, n + 1):  # QUA for_ loop for averaging
            
            with for_(n, 0, n < n_avg, n + 1):  # QUA for_ loop for averaging

                # Initialization
                wait( deplition_cc )

                for idx, res in enumerate(ro_element):
                    # Make sure that the readout pulse is sent with the same phase so that the acquired signal does not average out
                    # Measure the resonator (send a readout pulse and record the raw ADC trace)
                    reset_phase(res)
                    play("readout",res,duration=deplition_cc)
                    measure("readout" * amp(0), res, adc_st)
                    # measure("readout", res, adc_st)



        with stream_processing():
            # Will save average:
            adc_st.input1().average().save("adc1")
            adc_st.input2().average().save("adc2")
            # Will save only last run:
            adc_st.input1().save("adc1_single_run")
            adc_st.input2().save("adc2_single_run")

    ###########################
    # Run or Simulate Program #
    ###########################

    # if simulate:
    #     # Simulates the QUA program for the specified duration
    #     simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
    #     # Simulate blocks python until the simulation is done
    #     job = qmm.simulate(config, raw_trace_prog, simulation_config)
    #     # Plot the simulated samples
    #     job.get_simulated_samples().con1.plot()

    # else:
    # Open a quantum machine to execute the QUA program
    qm = qm_machine.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(raw_trace_prog)
    # Creates a result handle to fetch data from the OPX
    res_handles = job.result_handles
    # Waits (blocks the Python console) until all results have been acquired
    res_handles.wait_for_all_values()
    results = fetching_tool(job, data_list=[f"{ro_element[0]}_I", f"{ro_element[0]}_Q", "iteration"], mode="live")

    # Fetch the raw ADC traces and convert them into Volts
    adc1 = u.raw2volts(results.get("adc1").fetch_all())
    adc2 = u.raw2volts(results.get("adc2").fetch_all())
    adc1_single_run = u.raw2volts(results.get("adc1_single_run").fetch_all())
    adc2_single_run = u.raw2volts(results.get("adc2_single_run").fetch_all())
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


def frequency_sweep_timetrace_outloop( freq_range:tuple, resolution:float, depletion_time:float, config:dict, qm_machine:QuantumMachinesManager, ro_element:list, n_avg:int=100)->xr.Dataset:
    """
    Parameters: \n

    depletion_time: \n
        unit in us \n 
    freq_range: \n
        a tuple ( upper, lower ), unit in MHz. \n
    freq_resolution:
        unit in MHz. \n
    flux_range:\n
        unit in voltage.\n
    flux_resolution: \n
        unit in voltage.\n
    Return:
    xarray dataset with \n
    coords: ["mixer","frequency","time"]\n

    """



    frequencies_mhz = np.arange( freq_range[0], freq_range[1], resolution )
    freq_len = frequencies_mhz.shape[-1]

    ref_ro_IF = {}
    ref_ro_LO = {}
    for r in ro_element:
        ref_ro_IF[r] = gc.get_IF(r,config)
        ref_ro_LO[r] = gc.get_LO(r,config)

    all_data = []
    for freq in frequencies_mhz:
        single_data = single_timetrace( ro_element[0], ref_ro_IF[ro_element[0]], freq, depletion_time, config, qm_machine)
        all_data.append(single_data)

    dataset = xr.concat(all_data, dim='freq')
    dataset.coords['freq'] = ('freq', frequencies_mhz)

    return dataset

def single_timetrace(  ro_element, ref_ro_IF, freq:float, depletion_time:float, config:dict, qm_machine:QuantumMachinesManager, n_avg:int=100 ):
    deplition_cc = (depletion_time/4) * u.us
    freq_qua = freq* u.MHz
    print( f"Center {(ref_ro_IF)/1e6} MHz")
    print( f"Relative {(freq_qua)/1e6} MHz")

    ###################
    # The QUA program #
    ###################
    with program() as raw_trace_prog:
        n = declare(int)  # QUA variable for the averaging loop
        adc_st = declare_stream(adc_trace=True)  # The stream to store the raw ADC trace
        
        update_frequency( ro_element, ref_ro_IF+freq_qua)
        
        with for_(n, 0, n < n_avg, n + 1):  # QUA for_ loop for averaging

            # Initialization
            wait( deplition_cc )

            # Make sure that the readout pulse is sent with the same phase so that the acquired signal does not average out
            # Measure the resonator (send a readout pulse and record the raw ADC trace)
            reset_phase(ro_element)
            play("readout",ro_element,duration=deplition_cc)
            measure("readout" *amp(0), ro_element, adc_st)
            # measure("readout", ro_element, adc_st)



        with stream_processing():
            # Will save average:
            adc_st.input1().average().save("adc1")
            adc_st.input2().average().save("adc2")
            # Will save only last run:
            # adc_st.input1().save("adc1_single_run")
            # adc_st.input2().save("adc2_single_run")

    # else:
    # Open a quantum machine to execute the QUA program
    qm = qm_machine.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(raw_trace_prog)

    res_handles = job.result_handles
    # Waits (blocks the Python console) until all results have been acquired
    res_handles.wait_for_all_values()
    # Fetch the raw ADC traces and convert them into Volts
    adc1 = u.raw2volts(res_handles.get("adc1").fetch_all())
    adc2 = u.raw2volts(res_handles.get("adc2").fetch_all())


    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    
    output_data = np.array([adc1,adc2])
    dataset = xr.Dataset(
        {
            ro_element[0]: (["mixer","time"], output_data),
        },
        coords={"time": np.arange(adc1.shape[-1]), "mixer":np.array(["I","Q"]) }
    )
    return dataset


if __name__ == '__main__':
    import warnings
    warnings.filterwarnings("ignore")
    import matplotlib.pyplot as plt


    # 20231215 Test complete :Ratis
    # 20240202 Test complete :Jacky

    # Dynamic config
    from OnMachine.SetConfig.config_path import spec_loca, config_loca
    from config_component.configuration import import_config
    from config_component.channel_info import import_spec
    from ab.QM_config_dynamic import initializer

    spec = import_spec( spec_loca )
    config = import_config( config_loca ).get_config()
    qmm, _ = spec.buildup_qmm()

    freq_range = ( -5, 5 )
    resolution = 0.1
    depletion_time = 5
    n_avg = 10000
    ro_element = ['q4_ro']
    dataset = frequency_sweep_timetrace_outloop(freq_range,resolution,depletion_time, config, qmm, ro_element, n_avg)
    
    
    dataset = dataset.transpose('mixer', 'freq', 'time')
    print(dataset)

    # Plot
    freq = dataset.coords["freq"].values
    time = dataset.coords["time"].values
    print(freq.shape, time.shape)
    for ro_name, data in dataset.data_vars.items():
        fig_0, ax_0 = plt.subplots()
        ax_0.plot(time, data.values[0][int(freq.shape[-1]/2)])

        print( data.values[0].shape )
        fig, ax = plt.subplots()
        ax.set_title('pcolormesh')
        ax.set_xlabel("Time")
        ax.set_ylabel("Frequency")
        pcm = ax.pcolormesh( time/1000, freq, abs(data.values[0]+data.values[1]), cmap='RdBu')# , vmin=z_min, vmax=z_max)
        plt.colorbar(pcm, label='Value')

    plt.show()
    save_data = True
    if save_data:
        from exp.save_data import save_nc
        import sys
        save_nc(r"D:\Data\03205Q4C_6", f"{ro_element[0]}_res_decay_dt{depletion_time}", dataset)     
# Plot data
# plt.figure()
# plt.subplot(121)
# plt.title("Single run")
# plt.plot(adc1_single_run,adc2_single_run,"o",label="single")
# plt.plot(adc1, adc2, "o", label="ave")
# plt.xlabel("Time [ns]")
# plt.ylabel("Signal amplitude [V]")
# plt.legend()

# plt.subplot(122)
# plt.title("Averaged run")
# plt.plot(adc1, label="Input 1")
# plt.plot(adc2, label="Input 2")
# plt.xlabel("Time [ns]")
# plt.legend()
# plt.tight_layout()

# print(f"\nInput1 mean: {np.mean(adc1)} V\n" f"Input2 mean: {np.mean(adc2)} V")