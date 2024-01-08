"""
        iSWAP CHEVRON - 4ns granularity
The goal of this protocol is to find the parameters of the iSWAP gate between two flux-tunable qubits.
The protocol consists in flux tuning one qubit (the one with the highest frequency) so that it becomes resonant with the second qubit.
If one qubit is excited, then they will start swapping their states by exchanging one photon when they are on resonance.
The process can be seen as an energy exchange between |10> and |01>.

By scanning the flux pulse amplitude and duration, the iSWAP chevron can be obtained and post-processed to extract the
iSWAP gate parameters corresponding to half an oscillation so that the states are fully swapped (flux pulse amplitude
and interation time).

This version sweeps the flux pulse duration using real-time QUA, which means that the flux pulse can be arbitrarily long
but the step must be larger than 1 clock cycle (4ns) and the minimum pulse duration is 4 clock cycles (16ns).

Prerequisites:
    - Having found the resonance frequency of the resonator coupled to the qubit under study (resonator_spectroscopy).
    - Having found the qubits maximum frequency point (qubit_spectroscopy_vs_flux).
    - Having calibrated qubit gates (x180) by running qubit spectroscopy, rabi_chevron, power_rabi, Ramsey and updated the configuration.
    - (Optional) having corrected the flux line distortions by running the Cryoscope protocol and updating the filter taps in the configuration.

Next steps before going to the next node:
    - Update the iSWAP gate parameters in the configuration.
"""

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


def exp_coarse_iSWAP(  z_amp, z_time, excited_q:str, ro_element:list, z_name:list, config, qmm:QuantumMachinesManager, n_avg:int=100, simulate:bool=False, initializer=None ):

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
                    align()
                    # Wait some time to ensure that the flux pulse will end before the readout pulse
                    
                    for z in z_name:
                        set_dc_offset( z, "single", ref_z_offset[z])
                    # Align the elements to measure after having waited a time "tau" after the qubit pulses.
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
            for r_idx, r_name in enumerate(ro_element):
                ax[0][r_idx].cla()
                ax[1][r_idx].cla()
                output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])

                # Plot I
                ax[0][r_idx].set_ylabel("I quadrature [V]")
                plot_iSWAP_chavron(output_data[r_name], z_amp, z_time, [ax[0][r_idx],ax[1][r_idx]])
                # # Plot Q
                # ax[0][r_idx].set_ylabel("Q quadrature [V]")
                # plot_flux_dep_qubit(output_data[r_name][1], offset_arr, d_freq_arr,ax[1][r_idx]) 

            iteration = fetch_data[-1]
            # Progress bar
            progress_counter(iteration, n_avg, start_time=results.get_start_time()) 

            plt.pause(1)
        fetch_data = results.fetch_all()
        output_data = {}
        for r_idx, r_name in enumerate(ro_element):
            output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])
        # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
        qm.close()
    return output_data
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

def plot_ana_iSWAP_chavron( data, amp, time, ax=None ):
    """
    data shape ( 2, N, M )
    2 is I,Q
    N is freq
    M is time
    """
    idata = data[0]
    qdata = data[1]
    zdata = idata +1j*qdata
    s21 = zdata

    # abs_freq = freq_LO+freq_IF+amp
    if type(ax)==None:
        fig, ax = plt.subplots()
        ax.set_title('pcolormesh')
        fig.show()
    ax[0].pcolormesh( amp, time, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    # ax[0].axvline(x=freq_LO+freq_IF, color='b', linestyle='--', label='ref IF')
    # ax[0].axvline(x=freq_LO, color='r', linestyle='--', label='LO')

    # ax[0].legend()
    ax[1].pcolormesh( amp, time, np.angle(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)

    # ax[1].legend()