

from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.loops import from_array
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import matplotlib.pyplot as plt
import warnings
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
warnings.filterwarnings("ignore")
import xarray as xr
import time
import exp.config_par as gc
import numpy as np

from exp.QMMeasurement import QMMeasurement

class FluxDepCavity( QMMeasurement ):
    """
    Parameters: \n

    flux_settle_time: \n
        unit in us \n 
    freq_range: \n
        a tuple ( upper, lower ), unit in MHz. \n
    freq_resolution:
        unit in MHz. \n
    flux_range:\n
        unit in voltage.\n
    flux_resolution: \n
        unit in voltage.\n
    return:
    xarray dataset with \n
    coords: ["mixer","flux","frequency"]\n

    """
    def __init__( self, config, qmm: QuantumMachinesManager ):
        super().__init__( config, qmm )

        self.ro_elements = ["q0_ro"]
        self.z_elements = ["q0_z"]

        self.initializer = None
        

        self.z_amp_ratio_range = (-2, 2)
        self.z_amp_ratio_resolution = 0.1

        self.freq_range = ( -1, 1 )
        self.freq_resolution = 0.1

        self.qua_dim = ["index","flux","frequency"]

        self.preprocess = "average"
        
    def _get_qua_program( self ):
        self.qua_z_amp_ratio_array = self._lin_z_amp_array()
        self.qua_freqs = self._lin_freq_array()

        self._attribute_config()

        with program() as qua_prog:
            # QUA macro to declare the measurement variables and their corresponding streams for a given number of resonators
            iqdata_stream = multiRO_declare( self.ro_elements )

            n = declare(int)
            outermost_st = declare_stream()
            df = declare(int)  # QUA variable for sweeping the readout frequency detuning around the resonance
            r_z_amp = declare(fixed)  # QUA variable for sweeping the fluxes bias

            with for_(n, 0, n < self.shot_num, n + 1):
                with for_(*from_array(r_z_amp, self.qua_z_amp_ratio_array )):
                    for z in self.z_elements:
                        set_dc_offset(z, "single", self.qua_z_amp_ratio_array[0])
                    wait(4)  
                    with for_(*from_array(df, self.qua_freqs)):
                        for ro in self.ro_elements:
                            resonator_IF = self.config['elements'][ro]["intermediate_frequency"]
                            update_frequency(ro, df + resonator_IF)
                    
                        # Initialization
                        if self.initializer is None:
                            wait(1*u.us, self.ro_elements)
                        else:
                            try:
                                self.initializer[0](*self.initializer[1])
                            except:
                                print("initializer didn't work!")
                                wait(1*u.us, self.ro_elements)
                        # Operations
                        for z in self.z_elements:
                            set_dc_offset(z, "single", r_z_amp)

                        wait(4)  

                        # Readout
                        multiRO_measurement( iqdata_stream, self.ro_elements, weights='rotated_'  )
                        
                save(n, outermost_st)

            with stream_processing():
                outermost_st.save("outermost_i")
                multiRO_pre_save( iqdata_stream, self.ro_elements, (len(self.qua_z_amp_ratio_array), len(self.qua_freqs)), stream_preprocess=self.preprocess)
        return qua_prog

    def _data_formation( self ):
        self.qua_dim = ["index","flux","frequency"]
        self.output_data = super()._data_formation()

        amp_ratio = self.qua_z_amp_ratio_array
        self.output_data["flux"] = amp_ratio*self.z_amp[0]

        freqs_mhz = self.qua_freqs/1e6
        self.output_data["frequency"] = freqs_mhz
        
        self._attribute_config()
        self.output_data.attrs["ro_LO"] = self.ref_ro_LO
        self.output_data.attrs["ro_IF"] = self.ref_ro_IF
        self.output_data.attrs["z_offset"] = self.z_offset

        self.output_data.attrs["z_amp_const"] = self.z_amp
        return self.output_data


    def _attribute_config( self ):
        self.ref_ro_IF = []
        self.ref_ro_LO = []
        for r in self.ro_elements:
            self.ref_ro_IF.append(gc.get_IF(r, self.config))
            self.ref_ro_LO.append(gc.get_LO(r, self.config))

        self.z_offset = []
        self.z_amp = []
        for z in self.z_elements:
            self.z_offset.append( gc.get_offset(z, self.config ))
            self.z_amp.append(gc.get_const_wf(z, self.config ))

    def _lin_freq_array( self ):

        freq_r1_qua = self.freq_range[0] * u.MHz
        freq_r2_qua = self.freq_range[1] * u.MHz
        freq_resolution_qua = self.freq_resolution * u.MHz
        freqs_qua = np.arange(freq_r1_qua,freq_r2_qua,freq_resolution_qua )
        
        return freqs_qua

    def _lin_z_amp_array( self ):
        amp_ratio = np.arange( self.z_amp_ratio_range[0],self.z_amp_ratio_range[1], self.z_amp_ratio_resolution)
        return amp_ratio
    


def freq_sweep_Zpulse_dep( ro_element:list, z_element:list, config:dict, qm_machine:QuantumMachinesManager, n_avg:int=100, flux_settle_time:int=1000, RO_time:float=0.4, freq_range:tuple=(-3,3), flux_range:float=(-0.3,0.3), flux_resolution:float=0.015, freq_resolution:float=0.05, initializer:tuple=None )->xr.Dataset:
    """
    Parameters: \n

    flux_settle_time: \n
        unit in us \n 
    freq_range: \n
        a tuple ( upper, lower ), unit in MHz. \n
    freq_resolution:
        unit in MHz. \n
    flux_range:\n
        unit in voltage.\n
    flux_resolution: \n
        unit in voltage.\n
    return:
    xarray dataset with \n
    coords: ["mixer","flux","frequency"]\n

    """
    freq_r1_qua = freq_range[0] * u.MHz
    freq_r2_qua = freq_range[1] * u.MHz

    freq_resolution_qua = freq_resolution * u.MHz

    freqs_qua = np.arange( freq_r1_qua, freq_r2_qua, freq_resolution_qua )
    freqs_mhz = freqs_qua/1e6 #  Unit in MHz

    fluxes = np.arange( flux_range[0], flux_range[1], flux_resolution )


    freqs_len = freqs_qua.shape[0]
    flux_len = fluxes.shape[0]

    flux_settle_time_qua = (flux_settle_time/4) *u.us
    RO_time_qua = (RO_time/4) *u.us
    with program() as multi_res_spec_vs_flux:
        # QUA macro to declare the measurement variables and their corresponding streams for a given number of resonators
        iqdata_stream = multiRO_declare( ro_element )

        n = declare(int)
        n_st = declare_stream()
        df = declare(int)  # QUA variable for sweeping the readout frequency detuning around the resonance
        dc = declare(fixed)  # QUA variable for sweeping the fluxes bias

        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(df, freqs_qua)):
                for ro in ro_element:
                    resonator_IF = config['elements'][ro]["intermediate_frequency"]
                    update_frequency(ro, df + resonator_IF)
                # for z in z_element:
                #     set_dc_offset(z, "single", fluxes[0])
                # wait(flux_settle_time_qua)  
                with for_(*from_array(dc, fluxes)):
                    # initializaion
                    if initializer is None:
                        wait(1*u.us,ro_element)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            wait(1*u.us,ro_element)

                    # Operations
                    for z in z_element:
                        # set_dc_offset(z, "single", dc)
                        play("const"*amp((dc-gc.get_offset(z,config))/gc.get_const_wf(z,config)), z, flux_settle_time_qua + RO_time_qua)

                    wait(flux_settle_time_qua)  

                    # Readout
                    multiRO_measurement( iqdata_stream, ro_element, weights='rotated_')
                    
            save(n, n_st)

        with stream_processing():
            n_st.save("n")
            multiRO_pre_save( iqdata_stream, ro_element, (freqs_len, flux_len))
            
    #######################

    qm = qm_machine.open_qm(config)
    job = qm.execute(multi_res_spec_vs_flux)
    ro_ch_name = []
    for r_name in ro_element:
        ro_ch_name.append(f"{r_name}_I")
        ro_ch_name.append(f"{r_name}_Q")

    data_list = ro_ch_name + ["n"]   
    results = fetching_tool(job, data_list=data_list, mode="live")
    output_data = {}
    while results.is_processing():
        # Fetch results
        fetch_data = results.fetch_all()
        # Progress bar
        iteration = fetch_data[-1]
        progress_counter(iteration, n_avg, start_time=results.start_time)
        time.sleep(1)
    # Close the quantum machines at the end in order to put all fluxes biases to 0 so that the fridge doesn't heat-up
    fetch_data = results.fetch_all()
    qm.close()
    
    # Creating an xarray dataset
    for r_idx, r_name in enumerate(ro_element):
        output_data[r_name] = ( ["mixer","frequency","flux"],
                               np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
    dataset = xr.Dataset(
        output_data,
        coords={ "mixer":np.array(["I","Q"]), "frequency": freqs_mhz, "flux": fluxes }
    )

    return dataset


def freq_sweep_flux_dep_stable( ro_element:list, z_element:list, config:dict, qm_machine:QuantumMachinesManager, n_avg:int=100, flux_settle_time:int=1000, freq_range:tuple=(-3,3), flux_range:tuple=(-0.3,0.3), flux_resolution:float=0.015, freq_resolution:float=0.05, initializer:tuple=None )->xr.Dataset:
    """
    flux_settle_time: \n
        unit in us \n 
    freq_range: \n
        a tuple ( upper, lower ), unit in MHz. \n
    freq_resolution:
        unit in MHz. \n
    flux_range:\n
        unit in voltage.\n
    flux_resolution: \n
        unit in voltage.\n
    return:
    xarray dataset with \n
    coords: ["mixer","flux","frequency"]\n
    """
    freq_r1_qua = freq_range[0] * u.MHz
    freq_r2_qua = freq_range[1] * u.MHz

    freq_resolution_qua = freq_resolution * u.MHz

    freqs_qua = np.arange( freq_r1_qua, freq_r2_qua, freq_resolution_qua)
    fluxes = np.arange( flux_range[0], flux_range[1], flux_resolution)

    flux_settle_time_qua = flux_settle_time/4*u.us
    freqs_mhz = freqs_qua/1e6 #  Unit in MHz

    freqs_len = freqs_qua.shape[0]
    flux_len = fluxes.shape[0]
    output_data = []
    for flux_amp in fluxes:
        print("flux", flux_amp)
        qua_script = qua_freq_sweep( ro_element, z_element, freqs_qua, flux_amp, n_avg, config, initializer, flux_settle_time_qua )
        fetch_data = run_qua( qm_machine, config, qua_script, ro_element, n_avg)
        output_data.append(np.array(fetch_data[0:-1]))
        
        # print(len(output_data),np.array(fetch_data[0:-1]).shape)
    
    output_data = np.reshape(np.array(output_data), (flux_len, 2, len(ro_element), freqs_len))
    # print(output_data.shape)
    output_data = np.moveaxis(output_data, [0, 1, 2, 3], [3,1,0,2])
    # print(output_data.shape)

    dataset_data = {}
    for r_idx, r_name in enumerate(ro_element):
        print(r_name, output_data[r_idx].shape)
        dataset_data[r_name] = ( ["mixer","frequency","flux"],
                               output_data[r_idx] )
    dataset = xr.Dataset(
        dataset_data,
        coords={ "mixer":np.array(["I","Q"]), "frequency": freqs_mhz, "flux": fluxes }
    )   
    #     ref_ro_IF = {}
    # for r in ro_element:
    #     ref_ro_IF[r] = gc.get_IF(r, config)
    return dataset  

def qua_freq_sweep( ro_element:list, z_element:list, freqs_qua, z_amp, n_avg, config, initializer, flux_settle_time_qua ):
    
    with program() as multi_res_spec_vs_flux:
        # QUA macro to declare the measurement variables and their corresponding streams for a given number of resonators
        iqdata_stream = multiRO_declare( ro_element )

        n = declare(int)
        n_st = declare_stream()
        df = declare(int)  # QUA variable for sweeping the readout frequency detuning around the resonance

        for z in z_element:
            set_dc_offset(z, "single", z_amp)
        wait(flux_settle_time_qua,ro_element)
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(df, freqs_qua)):
                for ro in ro_element:
                    resonator_IF = config['elements'][ro]["intermediate_frequency"]
                    update_frequency(ro, df + resonator_IF)
                    # initializaion
                    if initializer is None:
                        wait(1*u.us,ro_element)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            wait(1*u.us,ro_element)

                    # Operations

                    # Readout
                    multiRO_measurement( iqdata_stream, ro_element, weights='rotated_')
                    
            save(n, n_st)

        with stream_processing():
            n_st.save("n")
            multiRO_pre_save( iqdata_stream, ro_element, (len(freqs_qua),))
    return multi_res_spec_vs_flux

def run_qua( qm_machine, config, qua_script, ro_element, n_avg):

    qm = qm_machine.open_qm(config)
    job = qm.execute( qua_script )
    ro_ch_name = []
    for r_name in ro_element:
        ro_ch_name.append(f"{r_name}_I")
        ro_ch_name.append(f"{r_name}_Q")

    data_list = ro_ch_name + ["n"]   
    results = fetching_tool(job, data_list=data_list, mode="live")
    output_data = {}
    while results.is_processing():
        fetch_data = results.fetch_all()
        # for r_idx, r_name in enumerate(ro_element):
        #     output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])
        iteration = fetch_data[-1]
        # Progress bar
        print(iteration, end="\r")
        progress_counter(iteration, n_avg, start_time=results.get_start_time()) 
    # Close the quantum machines at the end in order to put all fluxes biases to 0 so that the fridge doesn't heat-up
    qm.close()
    
    # Creating an dict for xarray dataset
    fetch_data = results.fetch_all()

    return fetch_data

def plot_flux_dep_resonator( data, freqs, fluxes, ax=None ):
    """
    data shape ( 2, N, M )
    2 is I,Q
    N is fluxes
    M is freq
    """
    idata = data[0]
    qdata = data[1]
    zdata = idata +1j*qdata

    if ax==None:
        fig, ax = plt.subplots()
        ax.set_title('pcolormesh')
        fig.show()
    pcm = ax.pcolormesh(fluxes, freqs, np.abs(zdata), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    ax.set_xlabel("flux")
    ax.set_ylabel("additional IF freq (MHz)")
    plt.colorbar(pcm, label='Value')