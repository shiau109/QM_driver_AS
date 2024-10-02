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
import time
from exp.QMMeasurement import QMMeasurement

class XYFreqSecondExcite( QMMeasurement ):
    """

    Parameters:
    ro_elements is RO \n
    xy_elements is XY \n

    freq_range: \n
        is a tuple ( upper bound, lower bound), unit in MHz, ref to idle IF \n
    freq_resolution: \n
        is a float, unit in MHz, ref to idle IF \n
    sweep_type: \n
        enumerate z_pulse, overlap

    return: \n
    dataset \n
    coors: ["mixer","flux","frequency"]\n
    attrs: ref_xy_IF, ref_xy_LO, z_offset\n
    """

    def __init__( self, config, qmm: QuantumMachinesManager ):
        super().__init__( config, qmm )

        self.ro_elements = ["q4_ro"]
        self.xy_elements = ["q4_xy"]
        
        self.preprocess = "ave"
        self.initializer = None
        
        self.sweep_type = "z_pulse"
        self.xy_driving_time = 10
        self.xy_amp_mod = 0.1

        self.freq_range = ( -1, 1 )
        self.freq_resolution = 0.5

        

    def _get_qua_program( self ):
        
        self.qua_freqs = self._lin_freq_array()

        self.qua_xy_driving_time = self.xy_driving_time/4 *u.us
        self._attribute_config()

        with program() as qua_prog:

            iqdata_stream = multiRO_declare( self.ro_elements )
            n = declare(int)  
            n_st = declare_stream()
            df = declare(int)  

            with for_(n, 0, n < self.shot_num, n + 1):

                with for_(*from_array(df, self.qua_freqs)):

                    # Initialization
                    if self.initializer is None:
                        wait(1*u.us, self.ro_elements)
                    else:
                        try:
                            self.initializer[0](*self.initializer[1])
                        except:
                            print("initializer didn't work!")
                            wait(1*u.us, self.ro_elements)

                    # operation
                    for i, xy in enumerate(self.xy_elements):
                        update_frequency( xy, self.ref_xy_IF[i] )
                        play("x180", xy)
                    align()
                    match self.sweep_type:
                        case "z_pulse":
                            self._qua_constant_drive_z_pulse(df)
                        case "overlap":
                            self._qua_constant_drive_overlap(df)
                        case _:
                            self._qua_constant_drive_z_pulse(df)

                    # measurement
                    multiRO_measurement( iqdata_stream, self.ro_elements, weights='rotated_'  )

                    # assign(index, index + 1)
                save(n, n_st)
            with stream_processing():
                n_st.save("iteration")
                multiRO_pre_save( iqdata_stream, self.ro_elements, ( len(self.qua_freqs), ))

        return qua_prog
        

        
    
    def _get_fetch_data_list( self ):
        ro_ch_name = []
        for r_name in self.ro_elements:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")

        data_list = ro_ch_name + ["iteration"]   
        return data_list
    
    def _data_formation( self ):
        freqs_mhz = self.qua_freqs/1e6
        coords = { 
            "mixer":np.array(["I","Q"]), 
            "frequency": freqs_mhz,
            }
        match self.preprocess:
            case "shot":
                dims_order = ["mixer","shot","frequency"]
                coords["shot"] = np.arange(self.shot_num)
            case _:
                dims_order = ["mixer","frequency"]

        output_data = {}
        for r_idx, r_name in enumerate(self.ro_elements):
            data_array = np.array([ self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]])
            output_data[r_name] = ( dims_order, np.squeeze(data_array))

        dataset = xr.Dataset( output_data, coords=coords )

        # dataset = dataset.transpose("mixer", "prepare_state", "frequency", "amp_ratio")

        self._attribute_config()
        dataset.attrs["ro_LO"] = self.ref_ro_LO
        dataset.attrs["ro_IF"] = self.ref_ro_IF
        dataset.attrs["xy_LO"] = self.ref_xy_LO
        dataset.attrs["xy_IF"] = self.ref_xy_IF
        dataset.attrs["z_offset"] = self.z_offset

        return dataset

    def _attribute_config( self ):
        self.ref_ro_IF = []
        self.ref_ro_LO = []
        for r in self.ro_elements:
            self.ref_ro_IF.append(gc.get_IF(r, self.config))
            self.ref_ro_LO.append(gc.get_LO(r, self.config))

        self.ref_xy_IF = []
        self.ref_xy_LO = []
        for xy in self.xy_elements:
            self.ref_xy_IF.append(gc.get_IF(xy, self.config))
            self.ref_xy_LO.append(gc.get_LO(xy, self.config))

        self.z_offset = []


    def _lin_freq_array( self ):

        freq_r1_qua = self.freq_range[0] * u.MHz
        freq_r2_qua = self.freq_range[1] * u.MHz
        freq_resolution_qua = self.freq_resolution * u.MHz
        freqs_qua = np.arange(freq_r1_qua,freq_r2_qua,freq_resolution_qua )
        
        return freqs_qua

    

    def _qua_constant_drive_z_pulse( self, df ):
        
        # operation

        for i, xy in enumerate(self.xy_elements):
            update_frequency( xy, self.ref_xy_IF[i] +df )
            play("const"*amp( self.xy_amp_mod ), xy, duration=self.qua_xy_driving_time)
        align()

    def _qua_constant_drive_overlap( self, df ):
       
        # operation

        # wait(250)
        for i, xy in enumerate(self.xy_elements):
            update_frequency( xy, self.ref_xy_IF[i] +df )
            play("const"*amp( self.xy_amp_mod ), xy, duration=self.qua_xy_driving_time)

        for i, ro in enumerate(self.ro_elements):
            wait( int(self.qua_xy_driving_time-gc.get_ro_length(ro,self.config)//4), ro )

    def _qua_constant_drive_z_pulse_offset( self, df ):
        
        # operation
        for i, xy in enumerate(self.xy_elements):
            update_frequency( xy, self.ref_xy_IF[i] +df )
            play("const"*amp( self.xy_amp_mod ), xy, duration=self.qua_xy_driving_time)
        align()

    def _qua_constant_drive_overlap_offset( self, df ):
        # operation
        # wait(25)
        for i, xy in enumerate(self.xy_elements):
            update_frequency( xy, self.ref_xy_IF +df )
            play("const"*amp( self.xy_amp_mod ), xy, duration=self.qua_xy_driving_time)
        align()
        # wait(25)
        align()



def plot_ana_flux_dep_qubit_1D( data, dfs, freq_LO, freq_IF, ax=None, iq_rotate=0 ):   # 20240530 test by Sean
    """
    data shape ( 2, N )
    2 is I,Q
    N is freq
    """
  
    idata = data[0]
    qdata = data[1]
    zdata = (idata +1j*qdata)*np.exp(1j*(iq_rotate/180)*np.pi)  # data shape ( N, )

    abs_freq = freq_LO+freq_IF+dfs

    if ax==None:
        fig, ax = plt.subplots(2)
        print("create new fig")
        fig.show()

    
    ax[0].plot( abs_freq, np.real(zdata), color='b' )
    ax[1].plot( abs_freq, np.imag(zdata), color='b' )

    ax[1].set_xlabel('XY frequency [MHz]')
    ax[0].set_ylabel('Amplitude [V]')
    ax[1].set_ylabel('Amplitude [V]')

    ax[0].legend()
    ax[1].legend()