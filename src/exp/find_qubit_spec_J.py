from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from configuration import *
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.loops import from_array
from QM_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import matplotlib.pyplot as plt
import warnings
from common_fitting_func import *
warnings.filterwarnings("ignore")
import get_config_para as gc
def flux_twotone_qubit( d_offset_arr, d_freq_arr, q_name:list, ro_element:list, z_name:list, config, qmm:QuantumMachinesManager, n_avg:int=100, saturation_len=1, flux_settle_time=10, Qi:int=1, isSimulate:bool=False):
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
    flux_len = len(d_offset_arr)
    with program() as multi_qubit_spec_vs_flux:
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)  
        n_st = declare_stream()
        df = declare(int)  
        dc = declare(fixed)  
        dynamic_ro_IF = declare(int, value=res_IF_list)  
        index = declare(int, value=0) 

        with for_(n, 0, n < n_avg, n + 1):

            with for_(*from_array(dc, d_offset_arr)):
                for z in z_name:
                    set_dc_offset( z, "single", dc + ref_z_offset[z])

                for r in ro_element:
                    update_frequency( r, dynamic_ro_IF[index])

                wait(flux_settle_time * u.ns) 
                assign(index, 0)

                with for_(*from_array(df, d_freq_arr)):
                    for xy in q_name:
                        update_frequency( xy, ref_xy_IF[xy] +df )
                        play("saturation" * amp(saturation_amp), xy, duration=saturation_len * u.ns)

                    multiRO_measurement( iqdata_stream, ro_element )
                assign(index, index + 1)
            save(n, n_st)
        with stream_processing():
            n_st.save("n")
            multiRO_pre_save( iqdata_stream, ro_element, (flux_len, freq_len))


    if isSimulate:
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, multi_qubit_spec_vs_flux, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(multi_qubit_spec_vs_flux)
        fig = plt.figure()
        interrupt_on_close(fig, job)

        ro_ch_name = []
        for r_name in ro_element:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")   

        data_list = ro_ch_name + ["n"]         
        results = fetching_tool(job, data_list, mode="live")
        while results.is_processing():
            all_results = results.fetch_all()
            n = all_results[-1]
            I, Q = all_results[0:res_num], all_results[res_num:res_num*2] 
            R = []
            phase = []
            for i in range(res_num):
                I[i] = u.demod2volts(I[i], readout_len)
                Q[i] = u.demod2volts(Q[i], readout_len)
                S = u.demod2volts(I[i] + 1j * Q[i], readout_len)
                R.append(np.abs(S))
                phase.append(np.angle(S))
            progress_counter(n, n_avg, start_time=results.start_time)
            x = ref_z_offset[z[Qi]] +d_offset_arr
            y = ref_xy_IF[xy[Qi]] +d_freq_arr
            live_plotting(x, y, R, phase, xy[Qi])
        fetch_data = results.fetch_all()
        output_data = {}
        for r_idx, r_name in enumerate(ro_element):
            output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])

        qm.close()

        return output_data
    
def live_plotting(x, y, R, phase, title="" ):
    plt.suptitle("Qubit spectroscopy")
    plt.subplot(121)
    plt.cla()
    plt.pcolor(x, y, R)
    plt.colorbar()
    plt.xlabel("Flux bias [V]")
    plt.ylabel(f"{title} IF [MHz]")
    plt.title(f"{title} amp.")
    plt.subplot(122)
    plt.cla()
    plt.pcolor(x, y, phase)
    plt.colorbar()
    plt.xlabel("Flux bias [V]")
    plt.ylabel(f"{title} IF [MHz]")
    plt.title(f"{title} phase. ")
    plt.tight_layout()
    plt.pause(1)





def qubit_flux_fitting( flux, freq, data, label ):
    R = []
    phase = []
    Flux = np.zeros((len(q_id), len(flux)))
    min_index = [[] for _ in q_id]
    max_index = [[] for _ in q_id]
    res_F = [[] for _ in q_id]
    resonator_flux_params, resonator_flux_covariance = [], []   
    S = data[0] +1j*data[1]
    R.append(np.abs(S))
    phase.append(np.angle(S))
    for j in range(len(Flux[i])):
        min_index[i].append(np.argmax(R[i][:,j])) 
        max_index[i].append(np.argmax(phase[i][:,j])) 

    plt.subplot(1, 2, 1)
    plt.cla()
    plt.title(label)
    plt.pcolor(flux, freq, R)        
    plt.plot(flux, freq[min_index])
    plt.subplot(1, 2, 2)
    plt.cla()
    plt.pcolor(flux, freq, phase)        
    plt.plot(flux, freq[min_index])

    plt.plot(flux,flux_qubit_spec(flux,v_period=0.72,max_freq=(3.8497e9),max_flux=-0.0289,idle_freq=(3.7497e9),idle_flux=0.05,Ec=0.196e9))

    plt.tight_layout()

if __name__ == '__main__':
    n_avg = 500  
    saturation_len = 12 * u.us  
    saturation_amp =  0.01 
    dfs = np.arange(-350e6, +100e6, 0.1e6)
    flux = np.arange(-0.1, 0.1, 0.01)
    Qi = 3
    operation_flux_point = [0, 4.000e-02, -3.100e-01, -3.200e-01] 
    res_F = resonator_flux( flux + operation_flux_point[Qi-1], *p1[Qi-1])
    res_IF = (res_F - resonator_LO)/1e6
    res_IF_list = []

    for IF in res_IF:
        res_IF_list.append(int(IF * u.MHz))  

    q_id = [0,1,2,3]
    q_name = ["q1_xy"] 
    ro_element: ["rr1","rr2","rr3","rr4","rr5"] 
    z_name = ["q1_z"] 
    isSimulate = False

    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
    output_data = flux_twotone_qubit(flux,dfs,q_name,ro_element,z_name, config, qmm, n_avg=n_avg, isSimulate=isSimulate)
    plt.show()

    qubit_flux_fitting(flux, dfs, output_data["q1_xy"])
    plt.show()

### Q3
# plt.plot(flux,flux_qubit_spec(flux,v_period=0.7,max_freq=(3.5235e9),max_flux=0.004,idle_freq=(3.2252e9),idle_flux=0.146,Ec=0.2e9))

### Q4
# plt.plot(flux,flux_qubit_spec(flux,v_period=0.72,max_freq=(3.8497e9),max_flux=-0.0204,idle_freq=(3.6507e9),idle_flux=0.0917,Ec=0.196e9))