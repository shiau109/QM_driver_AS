from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
import sys
import pathlib
# QM_script_root = str(pathlib.Path(__file__).parent.parent.resolve())
# sys.path.append(QM_script_root)
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import warnings
warnings.filterwarnings("ignore")
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)

import exp.config_par as gc
import xarray as xr

def xyfreq_time_rabi( freq_range:tuple, freq_resolution:float, time_range:tuple, time_resolution:float, q_name, ro_element, config, qmm, n_avg = 100, initializer = None, simulate=False):
    """
    Time Rabi Chavron. \n
    The excitation is using "x180" operation. \n
    Parameters: \n
    freq_range \n
    ( upper, lower )\n
    freq_resolution: \n
    unit in MHz. \n
    time_range: \n
    ( upper, lower )\n
    time_resolution:\n
    unit in ns. \n
    """
    time_r1_qua = (time_range[0]/4) *u.ns
    time_r2_qua = (time_range[1]/4) *u.ns

    if time_resolution < 4:
        print( "Warning!! time resolution < 4 ns.")
    time_resolution_qua = (time_resolution/4) *u.ns
    driving_time_qua = np.arange(time_r1_qua, time_r2_qua, time_resolution_qua)
    driving_time = driving_time_qua *4

    freq_r1_qua = freq_range[0] * u.MHz
    freq_r2_qua = freq_range[1] * u.MHz
    freq_resolution_qua = freq_resolution * u.MHz
    freqs = np.arange(freq_r1_qua, freq_r2_qua, freq_resolution_qua)

    freqs_mhz = freqs/1e6 # Unit in MHz

    ref_xy_IF = {}
    ref_xy_LO = {}
    for xy in q_name:
        ref_xy_IF[xy] = gc.get_IF(xy, config)
        ref_xy_LO[xy] = gc.get_LO(xy, config)

    freq_len = len(freqs)
    time_len = len(driving_time_qua)
    with program() as rabi:

        iqdata_stream = multiRO_declare(ro_element)
        t = declare(int)  
        n = declare(int)
        n_st = declare_stream()
        df = declare(int)  # QUA variable for the readout frequency
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(df, freqs)):
                # Update the frequency of the xy elements
                with for_( *from_array(t, driving_time_qua) ):  
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
                    for q in q_name:
                        update_frequency(q, ref_xy_IF[q]+df)

                    # Operation
                    for q in q_name:
                        play("x180", q, t)
                    align()
                    # Measurement
                    multiRO_measurement(iqdata_stream, ro_element, weights="rotated_")
            # Save iteration
            save(n, n_st)

        with stream_processing():
            multiRO_pre_save(iqdata_stream, ro_element, (freq_len,time_len) )
            n_st.save("iteration")

    if simulate:
        simulation_config = SimulationConfig(duration=10_000)  
        job = qmm.simulate(config, rabi, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
        # pass
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(rabi)

        fig, ax = plt.subplots(2, len(ro_element))
        if len(ro_element) == 1:
            ax = [[ax[0]],[ax[1]]]
        interrupt_on_close(fig, job)

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
                ax[0][r_idx].cla()
                ax[1][r_idx].cla()
                output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])

                # Plot I
                # ax[0][r_idx].set_ylabel("I quadrature [V]")
                plot_freq_dep_time_rabi(output_data[r_name], freqs, driving_time, [ax[0][r_idx],ax[1][r_idx]])
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

        fetch_data = results.fetch_all()
        qm.close()
        # Creating an xarray dataset
        output_data = {}
        for r_idx, r_name in enumerate(ro_element):
            output_data[r_name] = ( ["mixer","frequency","time"],
                                    np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
        dataset = xr.Dataset(
            output_data,
            coords={ "mixer":np.array(["I","Q"]), "frequency": freqs_mhz, "time": driving_time }
        )
        dataset.attrs["ref_xy_IF"] = list(ref_xy_IF.values())
        dataset.attrs["ref_xy_LO"] = list(ref_xy_LO.values())
    return dataset


def xyfreq_power_rabi( freq_range:tuple, freq_resolution:float, amp_range:tuple, amp_resolution:float, q_name, ro_element, config, qmm, n_avg = 100, initializer = None, simulate=False):
    """
    Power Rabi Chavron. \n
    The excitation is using "x180" operation. \n
    Parameters: \n
    freq_range \n
    ( upper, lower )\n
    freq_resolution: \n
    unit in MHz. \n
    amp_range \n
    ( upper, lower )\n
    amp_resolution: \n
    dimensionless ratio. \n
    """

    with program() as rabi:

        iqdata_stream = multiRO_declare(ro_element)
        n = declare(int)
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
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
            
            # Measurement
            set_dc_offset( "q0_z", "single", 0.2 )
            multiRO_measurement(iqdata_stream, ro_element, weights="rotated_")
            align()
            set_dc_offset( "q0_z", "single", 0 )
            # Save iteration
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            multiRO_pre_save(iqdata_stream, ro_element , None)

    if simulate:
        simulation_config = SimulationConfig(duration=10_000)  
        job = qmm.simulate(config, rabi, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
        # pass
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(rabi)

        fig, ax = plt.subplots(2, len(ro_element))
        if len(ro_element) == 1:
            ax = [[ax[0]],[ax[1]]]
        interrupt_on_close(fig, job)

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
                ax[0][r_idx].cla()
                ax[1][r_idx].cla()
                output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])

                # Plot I
                # ax[0][r_idx].set_ylabel("I quadrature [V]")
                # plot_freq_dep_time_rabi(output_data[r_name], freqs, r_amps, [ax[0][r_idx],ax[1][r_idx]])
                # # Plot Q
                # ax[0][r_idx].set_ylabel("Q quadrature [V]")
                # plot_flux_dep_qubit(output_data[r_name][1], offset_arr, d_freq_arr,ax[1][r_idx]) 

            iteration = fetch_data[-1]
            # Progress bar
            progress_counter(iteration, n_avg, start_time=results.get_start_time()) 

            plt.pause(1)

        fetch_data = results.fetch_all()
        qm.close()
        # Creating an xarray dataset
        output_data = {}
        for r_idx, r_name in enumerate(ro_element):
            output_data[r_name] = ( ["mixer"],
                                    np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
        dataset = xr.Dataset(
            output_data,
            coords={ "mixer":np.array(["I","Q"]) }
        )
        # dataset.attrs["ref_xy_IF"] = list(ref_xy_IF.values())
        # dataset.attrs["ref_xy_LO"] = list(ref_xy_LO.values())
        return dataset

def plot_freq_dep_time_rabi( data, dfs, time, ax=None ):
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
    ax[0].pcolormesh( time, dfs, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    ax[1].pcolormesh( time, dfs, np.angle(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)


def plot_ana_freq_time_rabi( data, dfs, time, freq_LO, freq_IF, ax=None, iq_rotate = 0 ):
    """
    data shape ( 2, N, M )
    2 is I,Q
    N is freq
    M is time
    """
    idata = data[0]
    qdata = data[1]
    zdata = (idata +1j*qdata)*np.exp(1j*iq_rotate)
    s21 = zdata

    abs_freq = freq_LO+freq_IF+dfs
    if type(ax)==None:
        fig, ax = plt.subplots()
        ax.set_title('pcolormesh')
        fig.show()
    ax[0].pcolormesh( time, abs_freq, np.real(zdata), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    # ax[0].axvline(x=freq_LO+freq_IF, color='b', linestyle='--', label='ref IF')
    # ax[0].axvline(x=freq_LO, color='r', linestyle='--', label='LO')
    ax[0].axhline(y=freq_LO+freq_IF, color='black', linestyle='--', label='ref IF')

    ax[0].legend()
    ax[1].pcolormesh( time, abs_freq, np.imag(zdata), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    ax[1].axhline(y=freq_LO+freq_IF, color='black', linestyle='--', label='ref IF')

    ax[1].legend()


