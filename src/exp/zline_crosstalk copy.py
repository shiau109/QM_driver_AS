from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qualang_tools.loops import from_array
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import warnings
warnings.filterwarnings("ignore")
import exp.config_par as gc
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
import xarray as xr
import numpy as np
from exp.QMMeasurement import QMMeasurement

warnings.filterwarnings("ignore")
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
from exp.config_par import get_offset

class FluxCrosstalk( QMMeasurement ):

    """
    Parameters:
    measure flux crosstalk with the given Z flux(voltage) range.\n

    expect_crosstalk:\n
    no unit.\n

    z_modify_range:\n
    unit in V.\n

    z_points:\n
    How many points is z_modify_range divided into.\n

    z_time:\n
    unit in micro second.\n

    measure_method:\n
    ramsey or long drive.\n
    see https://docs.google.com/presentation/d/18QqU46g3KktW5dPgIXpiLrI3leNX1FnE/edit?usp=drive_link&ouid=115212552955966668572&rtpof=true&sd=true\n
    page 2\n

    z_method:\n
    pulse or offset.\n
    The offset mode does not apply corrections from the crosstalk matrix.\n
    Only pulse mode does.\n
    2024/07/22\n

    ro_elements:\n
    who read out.\n

    detector_qubit:\n
    who is driven.\n

    detector_is_coupler:\n
    If detector is coupler, readout is not so easy.\n
    I haven't do this.\n

    crosstalk_qubit:\n
    Who provide its z_line to make flux crosstalk to others.\n 
    """

    def __init__( self, config, qmm: QuantumMachinesManager ):
        super().__init__( config, qmm )

        self.ro_elements = ["q3_ro"]
        self.detector_qubit = "q3"
        self.detector_is_coupler = "False"
        self.crosstalk_qubit = "q4"
        self.initializer = None

        self.expect_crosstalk = 0.01
        self.z_modify_range = 0.2
        self.z_points = 100
        self.z_time = 1

        self.measure_method = "ramsey"   #long_drive
        self.z_method = "pulse"     #offset


    def _get_qua_program( self ):
        self.crosstalk_z_qua = self._lin_z_array( )
        self.detector_z_qua = self.expect_crosstalk*self.crosstalk_z_qua
        self.z_time_cc = self.z_time*u.us//4
        self.pi_length = self._get_pi_length( )
        self.pi_amp_ration = self.pi_length/(self.z_time*u.us)
        if (self.measure_method =="ramsey" & self.z_method=="pulse"):
            with program() as Ramsey_z_pulse:
                iqdata_stream = multiRO_declare( self.ro_elements[0] )
                n = declare(int)
                n_st = declare_stream()

                z_detector = declare(fixed) 
                z_crosstalk = declare(fixed) 


                with for_(n, 0, n < self.shot_num, n + 1):  # QUA for_ loop for averaging
                    with for_(*from_array(z_crosstalk, self.crosstalk_z_qua)):
                        with for_( *from_array(z_detector, self.detector_z_qua) ):
                            # Initialization
                            # Wait for the resonator to deplete
                            if self.initializer is None:
                                wait(10 * u.us, self.ro_elements[0])
                            else:
                                try:
                                    self.initializer[0](*self.initializer[1])
                                except:
                                    print("initializer didn't work!")
                                    wait(1 * u.us, self.ro_elements[0]) 

                            # Opration
                            play( "x90", f"{self.detector_qubit}_xy" )
                            align()
                            wait(5)
                            play("const"*amp(z_crosstalk*2.), f"{self.crosstalk_qubit}_z", self.z_time_cc)         #const 預設0.5, microsecond transfrom to cc
                            play("const"*amp(z_detector*2.), f"{self.detector_qubit}_z", self.z_time_cc)
                            align()
                            wait(5) 
                            play( "x90", f"{self.detector_qubit}_xy" )
                            align()
                            wait(5)  
                            
                            # Readout
                            multiRO_measurement( iqdata_stream, self.ro_elements[0], weights="rotated_") 
                    # Save the averaging iteration to get the progress bar
                    save(n, n_st)

                with stream_processing():
                    # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
                    multiRO_pre_save( iqdata_stream, self.ro_elements[0], (len(self.flux_qua), len(self.evo_time_tick_qua)))
                    n_st.save("iteration")

            return Ramsey_z_pulse
        
        elif(self.measure_method =="long_drive" & self.z_method=="pulse"):
            with program() as LongDrive_z_pulse:
                iqdata_stream = multiRO_declare( self.ro_elements[0] )
                n = declare(int)
                n_st = declare_stream()

                z_detector = declare(fixed) 
                z_crosstalk = declare(fixed) 


                with for_(n, 0, n < self.shot_num, n + 1):  # QUA for_ loop for averaging
                    with for_(*from_array(z_crosstalk, self.crosstalk_z_qua)):
                        with for_( *from_array(z_detector, self.detector_z_qua) ):
                            # Initialization
                            # Wait for the resonator to deplete
                            if self.initializer is None:
                                wait(10 * u.us, self.ro_elements[0])
                            else:
                                try:
                                    self.initializer[0](*self.initializer[1])
                                except:
                                    print("initializer didn't work!")
                                    wait(1 * u.us, self.ro_elements[0]) 

                            # Opration
                            play( "x180"*amp(self.pi_amp_ration), f"{self.detector_qubit}_xy", duration=self.z_time_cc )
                            play("const"*amp(z_crosstalk*2.), f"{self.crosstalk_qubit}_z", self.z_time_cc)         #const 預設0.5
                            play("const"*amp(z_detector*2.), f"{self.detector_qubit}_z", self.z_time_cc)
                            align()
                            wait(5)
                            
                            # Readout
                            multiRO_measurement( iqdata_stream, self.ro_elements[0], weights="rotated_") 
                    # Save the averaging iteration to get the progress bar
                    save(n, n_st)

                with stream_processing():
                    # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
                    multiRO_pre_save( iqdata_stream, self.ro_elements[0], (len(self.flux_qua), len(self.evo_time_tick_qua)))
                    n_st.save("iteration")

            return LongDrive_z_pulse
        
        elif(self.measure_method =="ramsey" & self.z_method=="offset"):
            with program() as Ramsey_z_offset:
                iqdata_stream = multiRO_declare( self.ro_elements[0] )
                n = declare(int)
                n_st = declare_stream()

                z_detector = declare(fixed) 
                z_crosstalk = declare(fixed) 


                with for_(n, 0, n < self.shot_num, n + 1):  # QUA for_ loop for averaging
                    with for_(*from_array(z_crosstalk, self.crosstalk_z_qua)):
                        with for_( *from_array(z_detector, self.detector_z_qua) ):
                            # Initialization
                            # Wait for the resonator to deplete
                            if self.initializer is None:
                                wait(10 * u.us, self.ro_elements[0])
                            else:
                                try:
                                    self.initializer[0](*self.initializer[1])
                                except:
                                    print("initializer didn't work!")
                                    wait(1 * u.us, self.ro_elements[0]) 

                            # Opration
                            play( "x90", f"{self.detector_qubit}_xy" )
                            align()
                            wait(5)
                            set_dc_offset( f"{self.crosstalk_qubit}_z", "single", get_offset(f"{self.crosstalk_qubit}_z",self.config)+z_crosstalk )
                            set_dc_offset( f"{self.detector_qubit}_z", "single", get_offset(f"{self.detector_qubit}_z",self.config)+z_detector )
                            wait(self.z_time_cc) 
                            align()
                            wait(5) 
                            set_dc_offset( f"{self.crosstalk_qubit}_z", "single", get_offset(f"{self.crosstalk_qubit}_z",self.config) )
                            set_dc_offset( f"{self.detector_qubit}_z", "single", get_offset(f"{self.detector_qubit}_z",self.config) )
                            align()
                            wait(5)
                            play( "x90", f"{self.detector_qubit}_xy" )
                            align()
                            wait(5) 
                            
                            # Readout
                            multiRO_measurement( iqdata_stream, self.ro_elements[0], weights="rotated_") 
                    # Save the averaging iteration to get the progress bar
                    save(n, n_st)

                with stream_processing():
                    # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
                    multiRO_pre_save( iqdata_stream, self.ro_elements[0], (len(self.flux_qua), len(self.evo_time_tick_qua)))
                    n_st.save("iteration")

            return Ramsey_z_offset

        elif(self.measure_method =="long_drive" & self.z_method=="offset"):
            with program() as LongDrive_z_offset:
                iqdata_stream = multiRO_declare( self.ro_elements[0] )
                n = declare(int)
                n_st = declare_stream()

                z_detector = declare(fixed) 
                z_crosstalk = declare(fixed) 


                with for_(n, 0, n < self.shot_num, n + 1):  # QUA for_ loop for averaging
                    with for_(*from_array(z_crosstalk, self.crosstalk_z_qua)):
                        with for_( *from_array(z_detector, self.detector_z_qua) ):
                            # Initialization
                            # Wait for the resonator to deplete
                            if self.initializer is None:
                                wait(10 * u.us, self.ro_elements[0])
                            else:
                                try:
                                    self.initializer[0](*self.initializer[1])
                                except:
                                    print("initializer didn't work!")
                                    wait(1 * u.us, self.ro_elements[0]) 

                            # Opration
                            set_dc_offset( f"{self.crosstalk_qubit}_z", "single", get_offset(f"{self.crosstalk_qubit}_z",self.config)+z_crosstalk )
                            set_dc_offset( f"{self.detector_qubit}_z", "single", get_offset(f"{self.detector_qubit}_z",self.config)+z_detector )
                            align()
                            wait(5)
                            play( "x180"*amp(self.pi_amp_ration), f"{self.detector_qubit}_xy", duration=self.z_time_cc )
                            align()
                            wait(5)
                            set_dc_offset( f"{self.crosstalk_qubit}_z", "single", get_offset(f"{self.crosstalk_qubit}_z",self.config) )
                            set_dc_offset( f"{self.detector_qubit}_z", "single", get_offset(f"{self.detector_qubit}_z",self.config) )
                            align()
                            wait(5)
                            
                            # Readout
                            multiRO_measurement( iqdata_stream, self.ro_elements[0], weights="rotated_") 
                    # Save the averaging iteration to get the progress bar
                    save(n, n_st)

                with stream_processing():
                    # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
                    multiRO_pre_save( iqdata_stream, self.ro_elements[0], (len(self.flux_qua), len(self.evo_time_tick_qua)))
                    n_st.save("iteration")

            return LongDrive_z_offset

        else:
            print("unknown measure_method or z_method")

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
            output_data[r_name] = ( ["mixer","flux","time"],
                                np.array([self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]]) )
        dataset = xr.Dataset(
            output_data,
            coords={"mixer":np.array(["I","Q"]), "flux": self.flux_qua, "time": 4*self.evo_time_tick_qua}
        )

        self._attribute_config()
        dataset.attrs["ro_LO"] = self.ref_ro_LO
        dataset.attrs["ro_IF"] = self.ref_ro_IF
        dataset.attrs["xy_LO"] = self.ref_xy_LO
        dataset.attrs["xy_IF"] = self.ref_xy_IF
        dataset.attrs["z_offset"] = self.z_offset

        dataset.attrs["z_amp_const"] = self.z_amp
        return dataset
    
    def _attribute_config( self ):
        self.ref_ro_IF = []
        self.ref_ro_LO = []
        for r in self.ro_elements:
            self.ref_ro_IF.append(gc.get_IF(r, self.config))
            self.ref_ro_LO.append(gc.get_LO(r, self.config))

        self.ref_xy_IF = []
        self.ref_xy_LO = []
        for xy in self.zz_detector_xy:
            self.ref_xy_IF.append(gc.get_IF(xy, self.config))
            self.ref_xy_LO.append(gc.get_LO(xy, self.config))
        for xy in self.zz_source_xy:
            self.ref_xy_IF.append(gc.get_IF(xy, self.config))
            self.ref_xy_LO.append(gc.get_LO(xy, self.config))

        self.z_offset = []
        self.z_amp = []
        for z in self.coupler_z:
            self.z_offset.append( gc.get_offset(z, self.config ))
            self.z_amp.append(gc.get_const_wf(z, self.config ))
 
    def _lin_z_array( self ):
        return np.arange( -self.z_modify_range, self.z_modify_range, self.z_points )

    def _get_pi_length( self ):
        pi_pulse_name = self.config["elements"][f"{self.detector_qubit}_xy"]["operations"][f"{self.detector_qubit}_xy_x180_pulse"]
        pi_length = self.config["pulses"][pi_pulse_name]["length"]
        return pi_length

