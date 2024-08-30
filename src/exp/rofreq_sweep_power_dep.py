from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qualang_tools.loops import from_array
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)

import xarray as xr
import exp.config_par as gc
from exp.QMMeasurement import QMMeasurement

import numpy as np

class ROFreqSweepPowerDep( QMMeasurement ):
    """
    Parameters:\n
    freq_span:\n
        a tuple (upper, lower) Unit in MHz, \n
    amp_max_ratio: \n

    amp_scale: \n
        lin or log \n
    Return: xarray dataset
        coords : frequency, amp_ratio
    """
    def __init__( self, config, qmm: QuantumMachinesManager ):
        super().__init__( config, qmm )

        self.ro_elements = ["q0_ro"]
        # self.z_elements = []
        self.xy_elements = []

        self.initializer = None
        
        self.amp_scale = "lin"

        self.amp_mod_range = ( 0.5, 1.5 )
        self.amp_resolution = 0.05

        self.freq_range = ( -10, 10 )
        self.freq_resolution = 1

        

    def _get_qua_program( self ):
        
        self.amp_ratio = self._get_amp_ratio_array()
        print(self.amp_ratio)
        self.freqs_qua = self._lin_freq_array()
        self._attribute_config()
        

        with program() as multi_res_spec_vs_amp:
        
            iqdata_stream = multiRO_declare( self.ro_elements )
            n = declare(int)
            n_st = declare_stream()
            df = declare(int)
            a = declare(fixed)

            with for_(n, 0, n < self.shot_num, n + 1):
                # with for_(*qua_logspace(a, -1, 0, 2)):
                with for_(*from_array(a, self.amp_ratio)):
                    
                    with for_(*from_array(df, self.freqs_qua)):
                        # Initialization
                        if self.initializer is None:
                            wait(1*u.us, self.ro_elements)
                        else:
                            try:
                                self.initializer[0](*self.initializer[1])
                            except:
                                print("initializer didn't work!")
                                wait(1*u.us, self.ro_elements)

                        # Operation    
                        for i, r in enumerate(self.ro_elements):
                            update_frequency( r, self.ref_ro_IF[i]+df)
                        
                        # Readout
                        multiRO_measurement( iqdata_stream, self.ro_elements, amp_modify=a, weights='rotated_' )

                save(n, n_st)

            with stream_processing():
                n_st.save("iteration")
                # Cast the data into a 2D matrix, average the 2D matrices together and store the results on the OPX processor
                # NOTE that the buffering goes from the most inner loop (left) to the most outer one (right)
                multiRO_pre_save( iqdata_stream, self.ro_elements, (len(self.amp_ratio), len(self.freqs_qua)))



        return multi_res_spec_vs_amp
    
    def _get_fetch_data_list( self ):
        ro_ch_name = []
        for r_name in self.ro_elements:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")

        data_list = ro_ch_name + ["iteration"]   
        return data_list
    
    def _data_formation( self ):

        output_data = {}

        for r_idx, r_name in enumerate(self.ro_elements):
            output_data[r_name] = ( ["mixer","amp_ratio","frequency"],
                                np.array([ self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]]) )

        freqs_mhz = self.freqs_qua/1e6

        match self.amp_scale:
            case "lin": output_amp_ratio = self.amp_ratio
            case "log": output_amp_ratio = self.amp_ratio
            case _: output_amp_ratio = self.amp_ratio

        dataset = xr.Dataset(
            output_data,
            coords={ "mixer":np.array(["I","Q"]), "frequency": freqs_mhz, "amp_ratio": output_amp_ratio }
        )

        dataset.attrs["ro_LO"] = self.ref_ro_LO
        dataset.attrs["ro_IF"] = self.ref_ro_IF

        return dataset

    def _lin_freq_array( self ):

        freq_r1_qua = self.freq_range[0] * u.MHz
        freq_r2_qua = self.freq_range[1] * u.MHz
        freq_resolution_qua = self.freq_resolution * u.MHz
        freqs_qua = np.arange(freq_r1_qua,freq_r2_qua,freq_resolution_qua )
        
        return freqs_qua

    def _lin_amp_ratio_array( self ):
        amp_ratio = np.arange( self.amp_mod_range[0],self.amp_mod_range[1]+self.amp_resolution/2, self.amp_resolution)
        return amp_ratio
    
    def _log_amp_ratio_array( self ):
        amp_num = int( (self.amp_mod_range[1]-self.amp_mod_range[0])/self.amp_resolution )
        amp_ratio = np.logspace(self.amp_mod_range[0], self.amp_mod_range[1], amp_num)
        return amp_ratio
    
    def _get_amp_ratio_array( self ):
        match self.amp_scale:
            case "lin": return self._lin_amp_ratio_array()
            case "log": return  self._log_amp_ratio_array()
            case _: return self._lin_amp_ratio_array()    

    def _attribute_config( self ):
        self.ref_ro_IF = []
        self.ref_ro_LO = []
        for r in self.ro_elements:
            self.ref_ro_IF.append(gc.get_IF(r, self.config))
            self.ref_ro_LO.append(gc.get_LO(r, self.config))
    

def plot_power_dep_resonator( freqs, amp_ratio, data, ax=None, yscale="lin" ):
    """
    data shape ( 2, N, M )
    2 is I,Q
    N is freq
    M is RO amp
    """
    idata = data[0]
    qdata = data[1]
    zdata = idata +1j*qdata
    s21 = zdata/amp_ratio[:,None]

    if ax==None:
        fig, ax = plt.subplots()
        ax.set_title('pcolormesh')
        fig.show()
    if yscale == "log":
        pcm = ax.pcolormesh(freqs, np.log10(amp_ratio), np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    else:
        pcm = ax.pcolormesh(freqs, amp_ratio, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    plt.colorbar(pcm, label='Value')

