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

def flux_twotone_qubit( offset_arr, d_freq_arr, q_name:list, ro_element:list, z_name:list, config, qmm:QuantumMachinesManager, n_avg:int=100, saturation_len=1, saturation_ampRatio=0.1, flux_settle_time=10, simulate:bool=False):
    """
    q_name is XY on
    z_name is Shift
    """
    res_num = len(ro_element)
    ref_ro_IF = {}
    for r in ro_element:
        ref_ro_IF[r] = gc.get_IF(r, config)
    
    ref_xy_IF = {}
    for xy in q_name:
        ref_xy_IF[xy] = gc.get_IF(xy, config)

    ref_z_offset = {}
    for z in z_name:
        ref_z_offset[z] = gc.get_offset(z, config)

    freq_len = len(d_freq_arr) 
    flux_len = len(offset_arr)
    with program() as multi_qubit_spec_vs_flux:
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)  
        n_st = declare_stream()
        df = declare(int)  
        dc = declare(fixed)  
        # dynamic_ro_IF = declare(int, value=res_IF_list) 
        # index = declare(int, value=0) 

        with for_(n, 0, n < n_avg, n + 1):

            with for_(*from_array(dc, offset_arr)):

                for z in z_name:
                    set_dc_offset( z, "single", dc)
                    # assign(index, 0)

                with for_(*from_array(df, d_freq_arr)):

                    # initializaion
                    wait((flux_settle_time/4)*u.us,ro_element)
            
                    # for r in ro_element:
                    #     update_frequency( r, dynamic_ro_IF[index])

                    # operation
                    for xy in q_name:
                        update_frequency( xy, ref_xy_IF[xy] +df )
                        play("saturation"*amp(saturation_ampRatio), xy, duration=(saturation_len/4) *u.us)

                    # measurement
                    multiRO_measurement( iqdata_stream, ro_element, weights='rotated_'  )

                # assign(index, index + 1)
            save(n, n_st)
        with stream_processing():
            n_st.save("n")
            multiRO_pre_save( iqdata_stream, ro_element, (flux_len, freq_len))


    if simulate:
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, multi_qubit_spec_vs_flux, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(multi_qubit_spec_vs_flux)

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
                plot_flux_dep_qubit(output_data[r_name], offset_arr, d_freq_arr, [ax[0][r_idx],ax[1][r_idx]])
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

        qm.close()

        return output_data, offset_arr, d_freq_arr
    

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
    ax[0].pcolormesh( dfs, flux, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    ax[1].pcolormesh( dfs, flux, np.angle(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)

def plot_ana_flux_dep_qubit( data, flux, dfs, freq_LO, freq_IF, ax=None ):
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

    abs_freq = freq_LO+freq_IF+dfs
    if type(ax)==None:
        fig, ax = plt.subplots()
        ax.set_title('pcolormesh')
        fig.show()
    ax[0].pcolormesh( abs_freq, flux, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    ax[0].axvline(x=freq_LO+freq_IF, color='b', linestyle='--', label='ref IF')
    ax[0].axvline(x=freq_LO, color='r', linestyle='--', label='LO')
    ax[0].legend()
    ax[1].pcolormesh( abs_freq, flux, np.angle(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    ax[1].axvline(x=freq_LO+freq_IF, color='b', linestyle='--', label='ref IF')
    ax[1].axvline(x=freq_LO, color='r', linestyle='--', label='LO')
    ax[1].legend()


