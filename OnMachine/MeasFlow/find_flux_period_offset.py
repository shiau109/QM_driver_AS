"""
        RESONATOR SPECTROSCOPY VERSUS FLUX
This sequence involves measuring the resonator by sending a readout pulse and demodulating the signals to
extract the 'I' and 'Q' quadratures. This is done across various readout intermediate frequencies and flux biases.
The resonator frequency as a function of flux bias is then extracted and fitted so that the parameters can be stored in the configuration.

This information can then be used to adjust the readout frequency for the maximum frequency point.

Prerequisites:
    - Calibration of the time of flight, offsets, and gains (referenced as "time_of_flight").
    - Calibration of the IQ mixer connected to the readout line (be it an external mixer or an Octave port).
    - Identification of the resonator's resonance frequency (referred to as "resonator_spectroscopy_multiplexed").
    - Configuration of the readout pulse amplitude and duration.
    - Specification of the expected resonator depletion time in the configuration.

Before proceeding to the next node:
    - Update the readout frequency, labeled as "resonator_IF", in the configuration.
    - Adjust the flux bias to the maximum frequency point, labeled as "max_frequency_point", in the configuration.
    - Update the resonator frequency versus flux fit parameters (amplitude_fit, frequency_fit, phase_fit, offset_fit) in the configuration
"""

from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.loops import from_array
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import matplotlib.pyplot as plt
import warnings
from OnMachine.Octave_Config.QM_config_dynamic import u
from numpy import arange, absolute
warnings.filterwarnings("ignore")

###################
# The QUA program #
###################

def flux_dep_cavity( ro_element:list, config:dict, qm_machine:QuantumMachinesManager, n_avg:int=100, flux_settle_time_ns:int=200, freq_span_MHz:float=3, flux_span:float=0.3, flux_resolu:float=0.01, freq_resolu_MHz:float=0.01, initializer:tuple=None ):
    dfs = arange(-freq_span_MHz*u.MHz,(freq_span_MHz+freq_resolu_MHz)*u.MHz,freq_resolu_MHz*u.MHz)
    flux = arange(-flux_span,flux_span+flux_resolu,flux_resolu)
    plot_freq = arange(-freq_span_MHz,(freq_span_MHz+freq_resolu_MHz),freq_resolu_MHz)
    
    with program() as multi_res_spec_vs_flux:
        # QUA macro to declare the measurement variables and their corresponding streams for a given number of resonators
        iqdata_stream = multiRO_declare( ro_element )

        n = declare(int)
        n_st = declare_stream()
        df = declare(int)  # QUA variable for sweeping the readout frequency detuning around the resonance
        dc = declare(fixed)  # QUA variable for sweeping the flux bias

        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(df, dfs)):
                for ro in ro_element:
                    resonator_IF = config['elements'][ro]["intermediate_frequency"]
                    update_frequency(ro, df + resonator_IF)

                with for_(*from_array(dc, flux)):
                    # initializaion
                    if initializer is None:
                        wait(1*u.us,ro_element)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            wait(1*u.us,ro_element)
                    for ro in ro_element:
                        idx = ro.split("_")[-1]
                        set_dc_offset(f"q{idx}_z", "single", dc)
                    
                    wait(flux_settle_time_ns * u.ns)  
                    multiRO_measurement( iqdata_stream, ro_element, weights='rotated_')
                    
            save(n, n_st)

        with stream_processing():
            n_st.save("n")
            multiRO_pre_save( iqdata_stream, ro_element, (dfs.shape[0], flux.shape[0]))
            
    #######################

    qm = qm_machine.open_qm(config)
    job = qm.execute(multi_res_spec_vs_flux)
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
            output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])
        iteration = fetch_data[-1]
        # Progress bar
        progress_counter(iteration, n_avg, start_time=results.get_start_time()) 
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()

    return output_data, plot_freq, flux


def plot_flux_dep_resonator( data, dfs, flux, ax=None ):
    """
    data shape ( 2, N, M )
    2 is I,Q
    N is freq
    M is RO amp
    """
    idata = data[0]
    qdata = data[1]
    zdata = idata +1j*qdata
    s21 = zdata/flux[:,None]

    if ax==None:
        fig, ax = plt.subplots()
        ax.set_title('pcolormesh')
        fig.show()
    ax.pcolormesh(dfs, flux, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    

if __name__ == '__main__':
    from OnMachine.Octave_Config.QM_config_dynamic import Circuit_info, QM_config, initializer
    from OnMachine.MeasFlow.ConfigBuildUp import spec_loca, config_loca
    spec = Circuit_info(q_num = 4)
    config = QM_config()
    spec.import_spec(spec_loca)
    config.import_config(config_loca)
    
    qmm,_ = spec.buildup_qmm()
    init_macro = initializer(spec.give_depletion_time_for("all"),mode='depletion')
    
    ro_elements = ['q1_ro','q2_ro','q3_ro','q4_ro']
    results, freq_axis, flux_axis = flux_dep_cavity(ro_elements, config.get_config(), qmm, initializer=init_macro)
    for r in ro_elements:
        fig, ax = plt.subplots()
        plot_flux_dep_resonator(results[r], freq_axis, flux_axis, ax)
        ax.set_title(r)
        ax.set_xlabel("additional IF freq (MHz)")
        ax.set_ylabel("Flux bias")
    plt.show()