

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
# from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
import numpy as np
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save

import exp.config_par as gc
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)

import xarray as xr

def exp_coarse_iSWAP(  coupler_z, coupler_amp, z_amp, z_time, excited_q:str, ro_element:list, z_name:list, config, qmm:QuantumMachinesManager, n_avg:int=100, simulate:bool=False, initializer=None ):


    c_offset = gc.get_offset(coupler_z, config)
    ref_z_offset = {}
    for z in z_name:
        ref_z_offset[z] = gc.get_offset(z, config)
    amp_len = len(z_amp)
    time_len = len(z_time)

    ###################
    # The QUA program #
    ###################
    with program() as iswap:
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)  
        n_st = declare_stream()
        t = declare(int)  
        a = declare(fixed)  

        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(t, z_time)):
                with for_(*from_array(a, z_amp)):
                    # Init
                    if initializer is None:
                        wait(100*u.us)
                        #wait(thermalization_time * u.ns)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            print("Initializer didn't work!")
                            wait(100*u.us)

                    # Operation 
                    # Put one qubit in the excited state
                    play("x180", excited_q)
                    wait(25,excited_q)
                    align()
                    # Wait some time to ensure that the flux pulse will arrive after the x90 pulse
                    # "const 0.2"
                    for z in z_name:
                        set_dc_offset( z, "single", ref_z_offset[z] +a)
                        wait(t, z)
                    set_dc_offset( coupler_z, "single", c_offset +coupler_amp)
                    align()
                    # Wait some time to ensure that the flux pulse will end before the readout pulse
                    
                    for z in z_name:
                        set_dc_offset( z, "single", ref_z_offset[z])
                    # Align the elements to measure after having waited a time "tau" after the qubit pulses.
                    set_dc_offset( coupler_z, "single", c_offset)

                    align()
                    wait(25)
                    # Readout
                    multiRO_measurement( iqdata_stream, ro_element, weights="rotated_")

        # Save the averaging iteration to get the progress bar
        save(n, n_st)

        with stream_processing():
            # for the progress counter
            multiRO_pre_save( iqdata_stream, ro_element, (time_len,amp_len) )
            n_st.save("n")

    ###########################
    # Run or Simulate Program #
    ###########################
    if simulate:
        # Simulates the QUA program for the specified duration
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, iswap, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        # Open the quantum machine
        qm = qmm.open_qm(config)
        job = qm.execute(iswap)

        fig, ax = plt.subplots(2, len(ro_element))
        if len(ro_element) == 1:
            ax = [[ax[0]],[ax[1]]]
        interrupt_on_close(fig, job)

        ro_ch_name = []
        for r_name in ro_element:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")

        data_list = ro_ch_name + ["n"]   
        results = fetching_tool(job, data_list=data_list, mode="live")
        output_data = {}
        # Live plotting
        while results.is_processing():
            # Fetch results
            fetch_data = results.fetch_all()
 

            iteration = fetch_data[-1]
            # Progress bar
            progress_counter(iteration, n_avg, start_time=results.get_start_time()) 

        fetch_data = results.fetch_all()
        qm.close()
        # Creating an xarray dataset
        output_data = {}
        for r_idx, r_name in enumerate(ro_element):
            output_data[r_name] = ( ["mixer","time","amplitude"],
                                    np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
        dataset = xr.Dataset(
            output_data,
            coords={ "mixer":np.array(["I","Q"]), "time": z_time, "amplitude": z_amp }
        )

        dataset.attrs["z_offset"] = list(ref_z_offset.values())
    return dataset
    # np.savez(save_dir / 'iswap', I1=I1, Q1=Q1, I2=I2, ts=ts, amps=amps)

def plot_iSWAP_chavron( data, amp, time, ax=None ):
    """
    data shape ( 2, N, M )
    2 is I,Q
    N is freq
    M is flux
    """
    idata = data[0]
    qdata = data[1]
    zdata = idata +1j*qdata
    s21 = zdata

    if type(ax)==None:
        fig, ax = plt.subplots()
        ax.set_title('pcolormesh')
        fig.show()
    ax[0].pcolormesh( amp, time, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    ax[1].pcolormesh( amp, time, np.angle(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)

def plot_ana_iSWAP_chavron( data, amp, time, ax=None, iq_rotate = 0 ):
    """
    data shape ( 2, N, M )

    """
    idata = data[0]
    qdata = data[1]
    zdata = (idata +1j*qdata)*np.exp(1j*iq_rotate)
    s21 = zdata

    # abs_freq = freq_LO+freq_IF+amp
    if type(ax)==None:
        fig, ax = plt.subplots()
        ax.set_title('pcolormesh')
        fig.show()
    ax[0].pcolormesh( amp, time, np.real(zdata), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    # ax[0].axvline(x=freq_LO+freq_IF, color='b', linestyle='--', label='ref IF')
    # ax[0].axvline(x=freq_LO, color='r', linestyle='--', label='LO')

    # ax[0].legend()
    ax[1].pcolormesh( amp, time, np.imag(zdata), cmap='RdBu')# , vmin=z_min, vmax=z_max)

    # ax[1].legend()