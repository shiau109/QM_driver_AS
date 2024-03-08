from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.loops import from_array
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import matplotlib.pyplot as plt
import warnings
# from common_fitting_func import *
warnings.filterwarnings("ignore")
import exp.config_par as gc
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)

import xarray as xr
def xyfreq_sweep_flux_dep( flux_range:tuple, flux_resolution:float, freq_range:tuple, freq_resolution:float, q_name:list, ro_element:list, z_name:list, config, qmm:QuantumMachinesManager, n_avg:int=100, saturation_len=5, saturation_ampRatio=0.1, sweep_type:str="z_pulse", initializer=None, simulate:bool=False):
    """
    q_name is XY \n
    z_name is Z \n

    flux_range: \n
        is a tuple ( upper bound, lower bound), unit in voltage, ref to idle offset \n
    freq_range: \n
        is a tuple ( upper bound, lower bound), unit in MHz, ref to idle IF \n
    sweep_type: \n
        enumerate z_pulse, const_z, two_tone

    return: \n
    dataset \n
    coors: ["mixer","flux","frequency"]\n
    attrs: ref_xy_IF, ref_xy_LO, z_offset\n
    """

    fluxes = np.arange(flux_range[0], flux_range[1], flux_resolution)

    freq_r1_qua = freq_range[0] * u.MHz
    freq_r2_qua = freq_range[1] * u.MHz
    freq_resolution_qua = freq_resolution * u.MHz
    freqs = np.arange(freq_r1_qua, freq_r2_qua, freq_resolution_qua)

    freqs_mhz = freqs/1e6 # Unit in MHz

    saturation_time_qua = saturation_len/4 *u.us

    ref_ro_IF = {}
    for r in ro_element:
        ref_ro_IF[r] = gc.get_IF(r, config)
    ref_xy_IF = {}
    ref_xy_LO = {}
    for xy in q_name:
        ref_xy_IF[xy] = gc.get_IF(xy, config)
        ref_xy_LO[xy] = gc.get_LO(q_name[0],config)

    ref_z_offset = {}
    for z in z_name:
        ref_z_offset[z] = gc.get_offset(z, config)

    match sweep_type:
        case "z_pulse":
            qua_prog = qua_constant_drive_z_pulse( ro_element, n_avg, fluxes, freqs, saturation_ampRatio, saturation_time_qua, ref_z_offset, ref_xy_IF, initializer)
        case "const_z":
            qua_prog = qua_constant_drive_const_z( ro_element, n_avg, fluxes, freqs, saturation_ampRatio, saturation_time_qua, ref_z_offset, ref_xy_IF, initializer)
        case "two_tone":
            qua_prog = qua_constant_drive_twotone( ro_element, n_avg, fluxes, freqs, saturation_ampRatio, saturation_time_qua, ref_z_offset, ref_xy_IF, initializer)
        case _:
            qua_prog = qua_constant_drive_z_pulse( ro_element, n_avg, fluxes, freqs, saturation_ampRatio, saturation_time_qua, ref_z_offset, ref_xy_IF, initializer)

    if simulate:
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, qua_prog, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(qua_prog)

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
        while results.is_processing():
            fetch_data = results.fetch_all()
            for r_idx, r_name in enumerate(ro_element):
                ax[0][r_idx].cla()
                ax[1][r_idx].cla()
                output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])

                # Plot I
                ax[0][r_idx].set_ylabel("I quadrature [V]")
                plot_flux_dep_qubit(output_data[r_name], fluxes, freqs, [ax[0][r_idx],ax[1][r_idx]])
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
            output_data[r_name] = ( ["mixer","flux","frequency"],
                                    np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
        dataset = xr.Dataset(
            output_data,
            coords={ "mixer":np.array(["I","Q"]), "frequency": freqs_mhz, "flux": fluxes }
        )

        dataset.attrs["ro_IF"] = list(ref_ro_IF.values())
        dataset.attrs["xy_IF"] = list(ref_xy_IF.values())
        dataset.attrs["xy_LO"] =  list(ref_xy_LO.values())
        dataset.attrs["z_offset"] = list(ref_z_offset.values())

        return dataset


def qua_constant_drive_z_pulse( ro_element, n_avg, fluxes, freqs, saturation_ampRatio, saturation_len, ref_z_offset:dict, ref_xy_IF:dict, initializer=None):
    with program() as qua_prog:
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)  
        n_st = declare_stream()
        df = declare(int)  
        dc = declare(fixed)  

        with for_(n, 0, n < n_avg, n + 1):

            with for_(*from_array(dc, fluxes)):

                with for_(*from_array(df, freqs)):

                    # Initialization
                    if initializer is None:
                        wait(1*u.us, ro_element)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            print("initializer didn't work!")
                            wait(1*u.us, ro_element)

                    # operation
                    for z_name, ref_z in ref_z_offset.items():
                        set_dc_offset( z_name, "single", ref_z +dc)
                        # assign(index, 0)
                    wait(25)
                    for xy_name, ref_IF in ref_xy_IF.items():
                        update_frequency( xy_name, ref_IF +df )
                        play("const"*amp(saturation_ampRatio), xy_name, duration=saturation_len)
                    align()
                    for z_name, ref_z in ref_z_offset.items():
                        set_dc_offset( z_name, "single", ref_z)
                    wait(250)
                    align()
                    # measurement
                    multiRO_measurement( iqdata_stream, ro_element, weights='rotated_'  )

                # assign(index, index + 1)
            save(n, n_st)
        with stream_processing():
            n_st.save("n")
            multiRO_pre_save( iqdata_stream, ro_element, (len(fluxes), len(freqs)))

    return qua_prog

def qua_constant_drive_twotone( ro_element, n_avg, fluxes, freqs, saturation_ampRatio, saturation_len, ref_z_offset:dict, ref_xy_IF:dict, initializer=None ):
    with program() as qua_prog:
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)  
        n_st = declare_stream()
        df = declare(int)  
        dc = declare(fixed)  
        # dynamic_ro_IF = declare(int, value=res_IF_list) 
        # index = declare(int, value=0) 

        with for_(n, 0, n < n_avg, n + 1):

            with for_(*from_array(dc, fluxes)):

                with for_(*from_array(df, freqs)):

                    # Initialization
                    if initializer is None:
                        wait(1*u.us, ro_element)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            print("initializer didn't work!")
                            wait(1*u.us, ro_element)
            
                    # operation
                    for z_name, ref_z in ref_z_offset.items():
                        set_dc_offset( z_name, "single", ref_z +dc)
                    wait(250)
                    for xy_name, ref_IF in ref_xy_IF.items():
                        update_frequency( xy_name, ref_IF +df )
                        play("const"*amp(saturation_ampRatio), xy_name, duration=saturation_len)
                    # measurement
                    multiRO_measurement( iqdata_stream, ro_element, weights='rotated_'  )              
                    align()
                    

                # assign(index, index + 1)
            save(n, n_st)
        with stream_processing():
            n_st.save("n")
            multiRO_pre_save( iqdata_stream, ro_element, (len(fluxes), len(freqs)))
    return qua_prog

def qua_constant_drive_const_z( ro_element, n_avg, fluxes, freqs, saturation_ampRatio, saturation_len, ref_z_offset:dict, ref_xy_IF:dict, initializer=None ):
    with program() as qua_prog:
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)  
        n_st = declare_stream()
        df = declare(int)  
        dc = declare(fixed)  

        with for_(n, 0, n < n_avg, n + 1):

            with for_(*from_array(dc, fluxes)):

                for z_name, ref_z in ref_z_offset.items():
                    set_dc_offset( z_name, "single", ref_z +dc)

                with for_(*from_array(df, freqs)):
                    # Initialization
                    if initializer is None:
                        wait(1*u.us, ro_element)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            print("initializer didn't work!")
                            wait(1*u.us, ro_element)

                    # operation
                    for xy_name, ref_IF in ref_xy_IF.items():
                        update_frequency( xy_name, ref_IF +df )
                        play("saturation"*amp(saturation_ampRatio), xy_name, duration=saturation_len)
                    
                    align()
                    # measurement
                    multiRO_measurement( iqdata_stream, ro_element, weights='rotated_'  )

                # assign(index, index + 1)
            save(n, n_st)
        with stream_processing():
            n_st.save("n")
            multiRO_pre_save( iqdata_stream, ro_element, (len(fluxes), len(freqs)))
    return qua_prog


def plot_flux_dep_qubit( data, flux, dfs, ax=None ):
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
    ax[0].pcolormesh( dfs, flux, idata, cmap='RdBu')# , vmin=z_min, vmax=z_max)
    ax[1].pcolormesh( dfs, flux, qdata, cmap='RdBu')# , vmin=z_min, vmax=z_max)

def plot_ana_flux_dep_qubit( data, flux, dfs, freq_LO, freq_IF, abs_z, ax=None, iq_rotate=0 ):
    """
    data shape ( 2, N, M )
    2 is I,Q
    N is freq
    M is flux
    """
    idata = data[0]
    qdata = data[1]
    zdata = (idata +1j*qdata)*np.exp(iq_rotate)
    s21 = zdata

    abs_freq = freq_LO+freq_IF+dfs
    if type(ax)==None:
        fig, ax = plt.subplots()
        ax.set_title('pcolormesh')
        fig.show()
    pcm = ax[0].pcolormesh( abs_freq, abs_z+flux, np.real(zdata), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    ax[0].axvline(x=freq_LO+freq_IF, color='b', linestyle='--', label='ref IF')
    ax[0].axvline(x=freq_LO, color='r', linestyle='--', label='LO')
    ax[0].axhline(y=abs_z, color='black', linestyle='--', label='idle z')
    plt.colorbar(pcm, label='Value')
    # Add a color bar
    ax[0].legend()
    pcm = ax[1].pcolormesh( abs_freq, abs_z+flux, np.imag(zdata), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    ax[1].axvline(x=freq_LO+freq_IF, color='b', linestyle='--', label='ref IF')
    ax[1].axvline(x=freq_LO, color='r', linestyle='--', label='LO')
    ax[1].axhline(y=abs_z, color='black', linestyle='--', label='idle z')
    plt.colorbar(pcm, label='Value')

    ax[1].legend()


