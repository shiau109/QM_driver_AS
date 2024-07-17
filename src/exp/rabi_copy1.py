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

from exp.QMMeasurement import QMMeasurement

class Rabi( QMMeasurement ):
    def __init__( self, config, qmm: QuantumMachinesManager):
        super().__init__( config, qmm )
        freq_range = [1,4]
        freq_resolution = 0.1
        time_range = [4,100]
        time_resolution = 10
        amp_range = [1,4]
        amp_resolution = None
        q_name = None
        ro_element = None
        n_avg = 100
        initializer = None
        simulate = False

        self.freq_range = freq_range
        self.freq_resolution = freq_resolution
        self.time_range =  time_range
        self.time_resolution = time_resolution
        self.amp_range = amp_range
        self.amp_resolution = amp_resolution
        self.q_name = q_name
        self.ro_element = ro_element
        self.n_avg = n_avg
        self.initializer = initializer
        self.simulate = simulate
        self.process = "time"

    def _get_qua_program( self ):
        time_r1_qua = (self.time_range[0]/4) *u.ns
        time_r2_qua = (self.time_range[1]/4) *u.ns

        if self.time_resolution < 4:
            print( "Warning!! time resolution < 4 ns.")
        time_resolution_qua = (self.time_resolution/4) *u.ns
        self.driving_time_qua = np.arange(time_r1_qua, time_r2_qua, time_resolution_qua)
        driving_time = self.driving_time_qua *4

        freq_r1_qua = self.freq_range[0] * u.MHz
        freq_r2_qua = self.freq_range[1] * u.MHz
        freq_resolution_qua = self.freq_resolution * u.MHz
        freqs = np.arange(freq_r1_qua, freq_r2_qua, freq_resolution_qua)
        r_amps = np.arange(self.amp_range[0], self.amp_range[1], self.amp_resolution)

        freqs_mhz = freqs/1e6 # Unit in MHz

        self.ref_xy_IF = {}
        self.ref_xy_LO = {}
        for xy in self.q_name:
            self.ref_xy_IF[xy] = gc.get_IF(xy, self.config)
            self.ref_xy_LO[xy] = gc.get_LO(xy, self.config)

        freq_len = len(freqs)
        amp_len = len(r_amps)
        match self.process:
            case "time":
                time_len = len(self.driving_time_qua)
                with program() as rabi: 

                    iqdata_stream = multiRO_declare(self.ro_element)
                    t = declare(int)  
                    n = declare(int)
                    n_st = declare_stream()
                    df = declare(int)  # QUA variable for the readout frequency
                    with for_(n, 0, n < self.n_avg, n + 1):
                        with for_(*from_array(df, freqs)):
                            # Update the frequency of the xy elements
                            with for_( *from_array(t, self.driving_time_qua) ):  
                                # Init
                                if self.initializer is None:
                                    wait(100*u.us)
                                    #wait(thermalization_time * u.ns)
                                else:
                                    try:
                                        self.initializer[0](*self.initializer[1])
                                    except:
                                        print("Initializer didn't work!")
                                        wait(100*u.us)
                                for q in self.q_name:
                                    update_frequency(q, self.ref_xy_IF[q]+df)

                                # Operation
                                for q in self.q_name:
                                    play("x180", q, t)
                                align()
                                # Measurement
                                multiRO_measurement(iqdata_stream, self.ro_element, weights="rotated_")
                        # Save iteration
                        save(n, n_st)

                    with stream_processing():
                        multiRO_pre_save(iqdata_stream, self.ro_element, (freq_len,time_len) )
                        n_st.save("iteration")
            case _:
                with program() as rabi:
                    iqdata_stream = multiRO_declare(self.ro_element)
                    ra = declare(fixed)  
                    n = declare(int)
                    n_st = declare_stream()
                    df = declare(int)  # QUA variable for the readout frequency
                    with for_(n, 0, n < self.n_avg, n + 1):
                        with for_(*from_array(df, freqs)):
                            # Update the frequency of the xy elements
                            with for_( *from_array(ra, r_amps) ):  
                                # Init
                                if self.initializer is None:
                                    wait(100*u.us)
                                    #wait(thermalization_time * u.ns)
                                else:
                                    try:
                                        self.initializer[0](*self.initializer[1])
                                    except:
                                        print("Initializer didn't work!")
                                        wait(100*u.us)
                                for q in self.q_name:
                                    update_frequency(q, self.ref_xy_IF[q]+df)

                                # Operation
                                for q in self.q_name:
                                    play("x180"*amp(ra), q)
                                align()
                                # Measurement
                                multiRO_measurement(iqdata_stream, self.ro_element, weights="rotated_")
                        # Save iteration
                        save(n, n_st)

                    with stream_processing():
                        n_st.save("iteration")
                        multiRO_pre_save(iqdata_stream, self.ro_element, (freq_len,amp_len) )
        return rabi
    
    def xyfreq_time_rabi( self ):
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
        time_r1_qua = (self.time_range[0]/4) *u.ns
        time_r2_qua = (self.time_range[1]/4) *u.ns

        if self.time_resolution < 4:
            print( "Warning!! time resolution < 4 ns.")
        time_resolution_qua = (self.time_resolution/4) *u.ns
        driving_time_qua = np.arange(time_r1_qua, time_r2_qua, time_resolution_qua)
        driving_time = driving_time_qua *4

        freq_r1_qua = self.freq_range[0] * u.MHz
        freq_r2_qua = self.freq_range[1] * u.MHz
        freq_resolution_qua = self.freq_resolution * u.MHz
        freqs = np.arange(freq_r1_qua, freq_r2_qua, freq_resolution_qua)

        freqs_mhz = freqs/1e6 # Unit in MHz

        self.ref_xy_IF = {}
        self.ref_xy_LO = {}
        for xy in self.q_name:
            self.ref_xy_IF[xy] = gc.get_IF(xy, self.config)
            self.ref_xy_LO[xy] = gc.get_LO(xy, self.config)

        freq_len = len(freqs)
        time_len = len(driving_time_qua)
        with program() as rabi: 

            iqdata_stream = multiRO_declare(self.ro_element)
            t = declare(int)  
            n = declare(int)
            n_st = declare_stream()
            df = declare(int)  # QUA variable for the readout frequency
            with for_(n, 0, n < self.n_avg, n + 1):
                with for_(*from_array(df, freqs)):
                    # Update the frequency of the xy elements
                    with for_( *from_array(t, driving_time_qua) ):  
                        # Init
                        if self.initializer is None:
                            wait(100*u.us)
                            #wait(thermalization_time * u.ns)
                        else:
                            try:
                                self.initializer[0](*self.initializer[1])
                            except:
                                print("Initializer didn't work!")
                                wait(100*u.us)
                        for q in self.q_name:
                            update_frequency(q, self.ref_xy_IF[q]+df)

                        # Operation
                        for q in self.q_name:
                            play("x180", q, t)
                        align()
                        # Measurement
                        multiRO_measurement(iqdata_stream, self.ro_element, weights="rotated_")
                # Save iteration
                save(n, n_st)

            with stream_processing():
                multiRO_pre_save(iqdata_stream, self.ro_element, (freq_len,time_len) )
                n_st.save("iteration")
########################################################################################################
#This part contains 
        if self.simulate:
            simulation_config = SimulationConfig(duration=10_000)  
            job = self.qmm.simulate(self.config, rabi, simulation_config)
            job.get_simulated_samples().con1.plot()
            plt.show()
            # pass
        else:
            qm = self.qmm.open_qm(self.config)
            job = qm.execute(rabi)

            fig, ax = plt.subplots(2, len(self.ro_element))
            if len(self.ro_element) == 1:
                ax = [[ax[0]],[ax[1]]]
            interrupt_on_close(fig, job)

            ro_ch_name = []
            for r_name in self.ro_element:
                ro_ch_name.append(f"{r_name}_I")
                ro_ch_name.append(f"{r_name}_Q")

            data_list = ro_ch_name + ["iteration"]   
            results = fetching_tool(job, data_list=data_list, mode="live")
            output_data = {}
            while results.is_processing():
                fetch_data = results.fetch_all()
                for r_idx, r_name in enumerate(self.ro_element):
                    ax[0][r_idx].cla()
                    ax[1][r_idx].cla()
                    output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])

                    # Plot I
                    # ax[0][r_idx].set_ylabel("I quadrature [V]")
                    self.plot_freq_dep_time_rabi(output_data[r_name], freqs, driving_time, [ax[0][r_idx],ax[1][r_idx]])
                    # # Plot Q
                    # ax[0][r_idx].set_ylabel("Q quadrature [V]")
                    # plot_flux_dep_qubit(output_data[r_name][1], offset_arr, d_freq_arr,ax[1][r_idx]) 

                iteration = fetch_data[-1]
                # Progress bar
                progress_counter(iteration, self.n_avg, start_time=results.get_start_time()) 

                plt.pause(1)

            fetch_data = results.fetch_all()
            output_data = {}
            for r_idx, r_name in enumerate(self.ro_element):
                output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])

            fetch_data = results.fetch_all()
            qm.close()
            # Creating an xarray dataset
########################################################################################################
            output_data = {}
            for r_idx, r_name in enumerate(self.ro_element):
                output_data[r_name] = ( ["mixer","frequency","time"],
                                        np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
            dataset = xr.Dataset(
                output_data,
                coords={ "mixer":np.array(["I","Q"]), "frequency": freqs_mhz, "time": driving_time }
            )
            dataset.attrs["ref_xy_IF"] = list(self.ref_xy_IF.values())
            dataset.attrs["ref_xy_LO"] = list(self.ref_xy_LO.values())
        return dataset
########################################################################################################

    def xyfreq_power_rabi( self ):
        """
        Power Rabi Chavron. \n
        The excitation is using "x180" operation. \n
        Parameters: \n
        self.freq_range \n
        ( upper, lower )\n
        freq_resolution: \n
        unit in MHz. \n
        amp_range \n
        ( upper, lower )\n
        amp_resolution: \n
        dimensionless ratio. \n
        """
        freq_r1_qua = self.freq_range[0] * u.MHz
        freq_r2_qua = self.freq_range[1] * u.MHz
        freq_resolution_qua = self.freq_resolution * u.MHz
        freqs = np.arange(freq_r1_qua, freq_r2_qua, freq_resolution_qua)

        freqs_mhz = freqs/1e6 # Unit in MHz
        r_amps = np.arange(self.amp_range[0], self.amp_range[1], self.amp_resolution)
        ref_xy_IF = {}
        ref_xy_LO = {}
        for xy in self.q_name:
            ref_xy_IF[xy] = gc.get_IF(xy, self.config)
            ref_xy_LO[xy] = gc.get_LO(xy, self.config)

        freq_len = len(freqs)
        amp_len = len(r_amps)

        with program() as rabi:

            iqdata_stream = multiRO_declare(self.ro_element)
            ra = declare(fixed)  
            n = declare(int)
            n_st = declare_stream()
            df = declare(int)  # QUA variable for the readout frequency
            with for_(n, 0, n < self.n_avg, n + 1):
                with for_(*from_array(df, freqs)):
                    # Update the frequency of the xy elements
                    with for_( *from_array(ra, r_amps) ):  
                        # Init
                        if self.initializer is None:
                            wait(100*u.us)
                            #wait(thermalization_time * u.ns)
                        else:
                            try:
                                self.initializer[0](*self.initializer[1])
                            except:
                                print("Initializer didn't work!")
                                wait(100*u.us)
                        for q in self.q_name:
                            update_frequency(q, ref_xy_IF[q]+df)

                        # Operation
                        for q in self.q_name:
                            play("x180"*amp(ra), q)
                        align()
                        # Measurement
                        multiRO_measurement(iqdata_stream, self.ro_element, weights="rotated_")
                # Save iteration
                save(n, n_st)

            with stream_processing():
                n_st.save("iteration")

                multiRO_pre_save(iqdata_stream, self.ro_element, (freq_len,amp_len) )
        if self.simulate:
            simulation_config = SimulationConfig(duration=10_000)  
            job = self.qmm.simulate(self.config, rabi, simulation_config)
            job.get_simulated_samples().con1.plot()
            plt.show()
            # pass
        else:
            qm = self.qmm.open_qm(self.config)
            job = qm.execute(rabi)

            fig, ax = plt.subplots(2, len(self.ro_element))
            if len(self.ro_element) == 1:
                ax = [[ax[0]],[ax[1]]]
            interrupt_on_close(fig, job)

            ro_ch_name = []
            for r_name in self.ro_element:
                ro_ch_name.append(f"{r_name}_I")
                ro_ch_name.append(f"{r_name}_Q")

            data_list = ro_ch_name + ["iteration"]   
            results = fetching_tool(job, data_list=data_list, mode="live")
            output_data = {}
            while results.is_processing():
                fetch_data = results.fetch_all()
                for r_idx, r_name in enumerate(self.ro_element):
                    ax[0][r_idx].cla()
                    ax[1][r_idx].cla()
                    output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])

                    # Plot I
                    # ax[0][r_idx].set_ylabel("I quadrature [V]")
                    self.plot_freq_dep_time_rabi(output_data[r_name], freqs, r_amps, [ax[0][r_idx],ax[1][r_idx]])
                    # # Plot Q
                    # ax[0][r_idx].set_ylabel("Q quadrature [V]")
                    # plot_flux_dep_qubit(output_data[r_name][1], offset_arr, d_freq_arr,ax[1][r_idx]) 

                iteration = fetch_data[-1]
                # Progress bar
                progress_counter(iteration, self.n_avg, start_time=results.get_start_time()) 

                plt.pause(1)

            fetch_data = results.fetch_all()
            qm.close()
            # Creating an xarray dataset
########################################################################################################
            output_data = {}
            for r_idx, r_name in enumerate(self.ro_element):
                output_data[r_name] = ( ["mixer","frequency","amplitude"],
                                        np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )
            dataset = xr.Dataset(
                output_data,
                coords={ "mixer":np.array(["I","Q"]), "frequency": freqs_mhz, "amplitude": r_amps }
            )
            dataset.attrs["ref_xy_IF"] = list(ref_xy_IF.values())
            dataset.attrs["ref_xy_LO"] = list(ref_xy_LO.values())
            return dataset
########################################################################################################
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

    def _get_fetch_data_list( self ):
        ro_ch_name = []
        for r_name in self.ro_elements:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")

        data_list = ro_ch_name + ["iteration"]   
        return data_list

    def _data_formation( self ):
        freqs_mhz = self.qua_freqs/1e6
        driving_time = self.driving_time_qua *4
        output_data = {}
        r_amps = np.arange(self.amp_range[0], self.amp_range[1], self.amp_resolution)
        match self.process:
            case "time":
                for r_idx, r_name in enumerate(self.ro_element):
                    output_data[r_name] = ( ["mixer","frequency","time"],
                        np.array([self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]]) )
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]), "frequency": freqs_mhz, "time": driving_time }
                )
                dataset.attrs["ref_xy_IF"] = list(self.ref_xy_IF.values())
                dataset.attrs["ref_xy_LO"] = list(self.ref_xy_LO.values())
            case _:
                for r_idx, r_name in enumerate(self.ro_element):
                    output_data[r_name] = ( ["mixer","frequency","amplitude"],
                                            np.array([self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]]) )
                dataset = xr.Dataset(
                    output_data,
                    coords={ "mixer":np.array(["I","Q"]), "frequency": freqs_mhz, "amplitude": r_amps }
                )
                dataset.attrs["ref_xy_IF"] = list(self.ref_xy_IF.values())
                dataset.attrs["ref_xy_LO"] = list(self.ref_xy_LO.values())

        return dataset