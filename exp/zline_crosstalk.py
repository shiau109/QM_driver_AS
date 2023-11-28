from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from configuration import *
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.loops import from_array
from qualang_tools.plot import interrupt_on_close
from RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import matplotlib.pyplot as plt
import warnings
from scipy import signal
from scipy.optimize import curve_fit
from matplotlib.ticker import FuncFormatter
warnings.filterwarnings("ignore")

from config_par import get_offset

def zline_crosstalk( flux_modify_range, prob_q_name:str, ro_element:str, z_line:list, flux_settle_time, config, qmm:QuantumMachinesManager, expect_crosstalk:float=1.0, n_avg:int=100, simulate=True):
    """
    Mapping z offset crosstalk by qubit frequency 
    """
    a_min = -flux_modify_range
    a_max = flux_modify_range
    da = flux_modify_range/20

    flux_2_range = np.arange(a_min, a_max + da / 2, da)  # + da/2 to add a_max to amplitudes
    flux_1_range = flux_2_range*expect_crosstalk 

    # flux_1_range = np.arange(a_min*expect_crosstalk , (a_max + da / 2)*expect_crosstalk , da*expect_crosstalk/2 )#flux_2_range*expect_crosstalk 
    flux_1_len = len(flux_1_range) 
    flux_2_len = len(flux_2_range) 
    print(flux_1_len,flux_2_len)
    with program() as zc:

    
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int) 
        n_st = declare_stream()
        dc_1 = declare(fixed) 
        dc_2 = declare(fixed) 

        with for_(n, 0, n < n_avg, n + 1):
            
            with for_(*from_array(dc_1, flux_1_range)):
                set_dc_offset( z_line[0], "single", get_offset(z_line[0],config)+dc_1 )
                align()
                wait(flux_settle_time) 
                with for_(*from_array(dc_2, flux_2_range)):

                    set_dc_offset( z_line[1], "single", get_offset(z_line[1],config)+dc_2 )
                    
                    # Init
                    align()
                    wait(flux_settle_time) 

                    # Opration
                    play( "x90", prob_q_name )
                    wait(250) 
                    play( "x90", prob_q_name )
                    wait(10) 

                    # Readout
                    align()
                    multiRO_measurement(iqdata_stream, ro_element, weights="rotated_")
            save(n, n_st)
        with stream_processing():
            n_st.save("iteration")
            multiRO_pre_save( iqdata_stream, ro_element, (flux_1_len,flux_2_len) )

    if simulate:
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, zc, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(zc)

        ro_ch_name = []
        ro_ch_name.append(f"{ro_element}_I")
        ro_ch_name.append(f"{ro_element}_Q")
        data_list = ro_ch_name + ["iteration"]   
        results = fetching_tool(job, data_list=data_list, mode="live")

        fig, ax = plt.subplots(2)
        interrupt_on_close(fig, job)
        # fig.colorbar( p_i, ax=ax[0] )
        # fig.colorbar( p_q, ax=ax[1] )


        output_data = {}
        while results.is_processing():
            fetch_data = results.fetch_all()
            plt.cla()
            ax[0].cla()
            ax[1].cla()
            output_data[ro_element] = np.array([fetch_data[0], fetch_data[1]])
            plot_crosstalk_3Dscalar( flux_2_range, flux_1_range, output_data[ro_element][0], z_line, ax[0])
            plot_crosstalk_3Dscalar( flux_2_range, flux_1_range, output_data[ro_element][1], z_line, ax[1])
            iteration = fetch_data[-1]
            # Progress bar
            progress_counter(iteration, n_avg, start_time=results.get_start_time())      

            plt.tight_layout()
            plt.pause(1) 

        qm.close()
        return output_data

def plot_crosstalk_3Dscalar( x, y, z, z_line_name, ax=None ):
        if ax == None:
            fig, ax = plt.subplots(2)
        p_i = ax.pcolor(x, y, z)

        # plt.colorbar( p_q, ax=ax[1] )
        ax.set_xlabel(f"{z_line_name[1]} Delta Voltage (V)")
        ax.set_ylabel(f"{z_line_name[0]} Delta Voltage (V)")


if __name__=='__main__':
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

    from qualang_tools.units import unit
    u = unit(coerce_to_integer=True)
    n_avg = 100
    q_id = 0
    crosstalk_q_id = 2
    expect_crosstalk = 0.1
    flux_modify_range = 0.15
    prob_q_name = f"q{q_id+1}_xy"
    ro_element = f"rr{q_id+1}"
    z_line = [f"q{q_id+1}_z", f"q{crosstalk_q_id+1}_z"]
    flux_settle_time = 400 * u.us
    print(f"Z {q_id+1} offset {get_offset(z_line[0],config)} +/- {flux_modify_range*expect_crosstalk}")
    print(f"Z {crosstalk_q_id+1} offset {get_offset(z_line[1],config)} +/- {flux_modify_range}")

    zline_crosstalk( flux_modify_range, prob_q_name, ro_element, z_line, flux_settle_time, config, qmm, expect_crosstalk=expect_crosstalk, n_avg=n_avg, simulate=False)
    plt.show()