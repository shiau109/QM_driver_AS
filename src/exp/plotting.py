
import matplotlib.pyplot as plt
from exp.rofreq_sweep_power_dep import plot_power_dep_resonator
from exp.rofreq_sweep_flux_dep import plot_flux_dep_resonator
import numpy as np
from matplotlib.figure import Figure
from abc import ABC, abstractmethod

from xarray import Dataset, DataArray
class RawDataPainter():

    def __init__( self ):
        self.output_fig = []
        self.mode = "ave"

    @abstractmethod
    def _plot_method( self ):
        pass

    @abstractmethod
    def _data_parser( self ):
        pass

    def plot( self, dataset:Dataset, fig_name:str, show:bool=True ):

        self.output_fig = []

        for ro_name, data in dataset.data_vars.items():

            data.attrs = dataset.attrs
            self.plot_data = data
            self.title = ro_name
            self._data_parser()
            fig = self._plot_method()

            file_name = f"{fig_name}_{ro_name}"
            self.output_fig.append((file_name,fig))
        if show: plt.show()
        return self.output_fig


class PainterPowerDepRes( RawDataPainter ):

    def _data_parser( self ):
        dataarray = self.plot_data
        self.freqs = dataarray.coords["frequency"].values
        self.amp_ratio = dataarray.coords["amp_ratio"].values

        idata = dataarray.values[0]
        qdata = dataarray.values[1]
        self.zdata = idata +1j*qdata

    def _plot_method( self ):
        s21 = self.zdata/self.amp_ratio[:,None]
        freqs = self.freqs
        amp_ratio = self.amp_ratio
        title = self.title
        fig, ax = plt.subplots(2)
        # if yscale == "log":
        #     pcm = ax.pcolormesh(freqs, np.log10(amp_ratio), np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
        # else:
        pcm = ax[0].pcolormesh(freqs, amp_ratio, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
        ax[0].set_title(f"{title} Magnitude")
        ax[0].set_xlabel("Additional IF freq (MHz)")
        ax[0].set_ylabel("Amplitude Ratio")
        plt.colorbar(pcm, label='Value')

        pcm = ax[1].pcolormesh(freqs, amp_ratio, np.angle(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
        ax[0].set_title(f"{title} Phase")
        ax[1].set_xlabel("Additional IF freq (MHz)")
        ax[1].set_ylabel("Amplitude Ratio")
        plt.colorbar(pcm, label='Value')

        return fig
    
#S2
def plot_and_save_dispersive_limit(dataset, folder_save_dir, my_exp, save_data = True):
    dfs = dataset.coords["frequency"].values
    amps = dataset.coords["amp_ratio"].values

    for ro_name, data in dataset.data_vars.items():
        fig, ax = plt.subplots()
        plot_power_dep_resonator(dfs, amps, data.values, ax, my_exp.amp_scale)
        ax.set_title(ro_name)
        ax.set_xlabel("additional IF freq (MHz)")
        ax.set_ylabel("amp scale")
        file_name = f"power_dep_resonator_{ro_name}"
        # if save_data: save_fig( folder_save_dir, file_name)
        
    plt.show()


#S3
def plot_and_save_flux_period(dataset, folder_save_dir = 0, save_data = True):
    dfs = dataset.coords["frequency"].values
    amps = dataset.coords["flux"].values   
    for ro_name, data in dataset.data_vars.items():
        fig, ax = plt.subplots()
        plot_flux_dep_resonator( data.values, dfs, amps, ax)
        ax.set_title(ro_name)
        save_name = f"flux_resonator_{ro_name}"
        # if save_data: save_fig( folder_save_dir, save_name)

    plt.show()

#S4
def plot_and_save_flux_dep_Qubit(dataset, folder_save_dir = 0, save_data = True):
    from exp.xyfreq_sweep_flux_dep import plot_ana_flux_dep_qubit
    freqs = dataset.coords["frequency"].values
    flux = dataset.coords["amp_ratio"].values
    for i, (ro_name, data) in enumerate(dataset.data_vars.items()):
        xy_LO = dataset.attrs["xy_LO"][0]/1e6
        xy_IF_idle = dataset.attrs["xy_IF"][0]/1e6
        z_offset = dataset.attrs["z_offset"][0]
        print(ro_name, xy_LO, xy_IF_idle, z_offset, data.shape)
        fig, ax = plt.subplots(2)

        plot_ana_flux_dep_qubit(data, flux, freqs, xy_LO, xy_IF_idle, z_offset, ax)
        # plot_ana_flux_dep_qubit_1D(data, flux, freqs, xy_LO, xy_IF_idle, z_offset, ax) 


        ax[0].set_title(ro_name)
        ax[1].set_title(ro_name)
        save_name = f"flux_dep_Qubit_{ro_name}"
        # if save_data: save_fig(folder_save_dir, save_name)



    plt.show()

#S5
def plot_and_save_rabi(dataset, freqs, y, name, folder_save_dir = 0, save_data = True ):
    from exp.old_version.rabi import plot_ana_freq_time_rabi 
    for ro_name, data in dataset.data_vars.items():
        xy_LO = dataset.attrs["ref_xy_LO"][0]/1e6
        xy_IF_idle = dataset.attrs["ref_xy_IF"][0]/1e6
        fig, ax = plt.subplots(2)
        plot_ana_freq_time_rabi( data, freqs, y, xy_LO, xy_IF_idle, ax )
        ax[0].set_title(ro_name)
        ax[1].set_title(ro_name)
        save_name = f"detuned_{name}_rabi_{ro_name}"
        # if save_data: save_fig(folder_save_dir, save_name)

    plt.show()

#S6
def plot_and_save_T1_spectrum(dataset, time, flux, folder_save_dir = 0, save_data = True ):
    for ro_name, data in dataset.data_vars.items():
        fig_0, ax_0 = plt.subplots()
        ax_0.plot(time, data.values[0][0])
        print( data.values[0].shape )
        fig, ax = plt.subplots()
        ax.set_title('pcolormesh')
        ax.set_xlabel("T1 (us)")
        ax.set_ylabel("Flux")
        pcm = ax.pcolormesh( time/1000, flux, data.values[0], cmap='RdBu')# , vmin=z_min, vmax=z_max)
        plt.colorbar(pcm, label='Value')
        save_name = f"T1_spectrum_{ro_name}"
        # if save_data: save_fig( folder_save_dir, save_name ) 

    plt.show()

def plot_and_save_t1_singleRun(dataset, time, folder_save_dir = 0, save_data = True ):
    from qcat.visualization.qubit_relaxation import plot_qubit_relaxation
    from qcat.analysis.qubit.relaxation import qubit_relaxation_fitting
    for ro_name, data in dataset.data_vars.items():
        print(ro_name)
        fit_result = qubit_relaxation_fitting(time, data.values[0])
        print(fit_result.params)
        fig, ax = plt.subplots()
        plot_qubit_relaxation(time, data[0], ax, fit_result)
        save_name = f"T1_stat_singleRun_{ro_name}"
        # if save_data: save_fig(folder_save_dir, save_name)
    plt.show()

def plot_and_save_t1_repeateRun(dataset, time, single_name, folder_save_dir = 0, save_data = True ):
    from qcat.visualization.qubit_relaxation import plot_time_dep_qubit_T1_relaxation_2Dmap, plot_qubit_T1_relaxation_hist
    from qcat.analysis.qubit.relaxation import qubit_relaxation_fitting
    import numpy as np
    rep = dataset.coords["repetition"].values
    dataset = dataset.transpose("mixer","repetition","time")
    for ro_name, data in [(single_name, dataset[single_name])]:
        acc_T1 = []
        for i in range(rep.shape[-1]):
            fit_result = qubit_relaxation_fitting(time, data.values[0][i])
            acc_T1.append(fit_result.params["tau"].value)
        fig, ax = plt.subplots()
        plot_time_dep_qubit_T1_relaxation_2Dmap( rep, time, data.values[0], ax, fit_result=acc_T1)
        print(acc_T1)
        save_name = f"T1_2Dmap_{ro_name}"
        # if save_data: save_fig( folder_save_dir, save_name)
        fig1, ax1 = plt.subplots()
        
        plot_qubit_T1_relaxation_hist( np.array(acc_T1), ax1 )
        save_name = f"T1_hist_{ro_name}"
        # if save_data: save_fig( folder_save_dir, save_name)
    plt.show()

#S7
#spin echo
def plot_and_save_t2_spinEcho(dataset, folder_save_dir = 0, save_data = True ):
    from exp.ramsey import plot_ramsey_oscillation
    time = dataset.coords["time"].values
    for ro_name, data in dataset.data_vars.items():
        fig, ax = plt.subplots(2)
        # print(data.shape)
        plot_ramsey_oscillation(time, data[0], ax[0])
        plot_ramsey_oscillation(time, data[1], ax[1])
        # rep = dataset.coords["repetition"].values
        # plot_multiT2( data, rep, time )
        save_name = f"T2_spin_echo_{ro_name}"
        # if save_data: save_fig(folder_save_dir, save_name, dataset)
    plt.show()

#ramsey
def plot_and_save_t2_ramsey_singleRun(dataset, time, folder_save_dir = 0, save_data = True ):
    from qcat.visualization.qubit_relaxation import plot_qubit_relaxation
    from qcat.analysis.qubit.relaxation import qubit_relaxation_fitting

    for ro_name, data in dataset.data_vars.items():
        print(ro_name)
        fit_result = qubit_relaxation_fitting(time, data.values[0])
        print(fit_result.params)
        fig, ax = plt.subplots()
        plot_qubit_relaxation(time, data[0], ax, fit_result)
        save_name = f"T2_ramsey_singleRun_{ro_name}"
        # if save_data: save_fig(folder_save_dir, save_name, dataset)

    plt.show()

def plot_and_save_t2_ramsey_repeateRun(dataset, time, single_name, folder_save_dir = 0, save_data = True ):
    from qcat.visualization.qubit_relaxation import plot_time_dep_qubit_T2_relaxation_2Dmap, plot_qubit_T2_relaxation_hist
    from qcat.analysis.qubit.relaxation import qubit_relaxation_fitting

    rep = dataset.coords["repetition"].values
    for ro_name, data in [(single_name, dataset[single_name])]:
        acc_T2 = []
        for i in range(rep.shape[-1]):
            fit_result = qubit_relaxation_fitting(time, data.values[0][i])
            acc_T2.append(fit_result.params["T2"].value)
        fig, ax = plt.subplots()
        plot_time_dep_qubit_T2_relaxation_2Dmap( rep, time, data.values[0], ax, fit_result=acc_T2)
        print(acc_T2)
        save_name = f"T2_2Dmap_{ro_name}"
        # if save_data: save_fig( folder_save_dir, save_name)
        fig1, ax1 = plt.subplots()

        plot_qubit_T2_relaxation_hist( np.array(acc_T2), ax1 )
        save_name = f"T2_hist_{ro_name}"
        # if save_data: save_fig( folder_save_dir, save_name)
    plt.show()

#S9
#bk
def plot_and_save_cryoscope_bk(dataset, pad_zeros, const_flux_len, folder_save_dir = 0, save_data = True ):
    import numpy as np
    from scipy import signal, optimize
    time = dataset.coords["time"].values
    for ro_name, data in dataset.data_vars.items():
        fig, ax = plt.subplots(3)
        print(data.shape)
        # xy_LO = dataset.attrs["ref_xy_LO"][q_name[0]]/1e6
        rx90_data = data[0][0].values
        ry90_data = data[0][1].values

        rx90_data = rx90_data-np.mean(rx90_data[pad_zeros[0]:])
        ry90_data = ry90_data-np.mean(ry90_data[pad_zeros[0]:])
        zdata = (rx90_data + 1j*ry90_data)
        virtual_detune = 200.
        mod_zdata = zdata*np.exp(1j*time*virtual_detune/1000*np.pi*2)
        phase_origin = np.unwrap(np.angle( zdata ))
        phase = np.unwrap(np.angle( mod_zdata ))
        phase = phase - phase[-1]
        # Filtering and derivative of the phase to get the averaged frequency
        detuning_origin = signal.savgol_filter(phase_origin / 2 / np.pi, 13, 3, deriv=1, delta=0.001)
        detuning = signal.savgol_filter(phase / 2 / np.pi, 13, 3, deriv=1, delta=0.001)
        # Flux line step response in freq domain and voltage domain
        step_response_freq = detuning / np.average(detuning[-int(const_flux_len / 2) :])

        ax[0].plot(time, zdata.real, label="x" )
        ax[0].plot(time, mod_zdata.real, label=f"x-{virtual_detune}" )
        ax[0].plot(time, zdata.imag, label="y" )
        ax[0].plot(time, mod_zdata.imag, label=f"y-{virtual_detune}" )

        ax[1].plot(time, phase_origin, label="0" )
        ax[1].plot(time, phase, label=f"{virtual_detune}")

        ax[2].plot(time, detuning_origin, label="0")
        ax[2].plot(time, detuning-virtual_detune, label=f"{virtual_detune}")

        save_name = f"cryoscope_bk_{ro_name}"
        # if save_data: save_fig(folder_save_dir, save_name, dataset)

    plt.show()

#cc
def plot_and_save_cryoscope_cc(dataset, my_exp, folder_save_dir = 0, save_data = True ):
    import numpy as np
    from scipy import signal

    time = dataset.coords["time"].values
    for ro_name, data in dataset.data_vars.items():
        fig, ax = plt.subplots(3)
        print(data.shape)
        # xy_LO = dataset.attrs["ref_xy_LO"][q_name[0]]/1e6
        rx90_data = data[0][0].values
        ry90_data = data[0][1].values

        rx90_data = rx90_data-np.mean(rx90_data[my_exp.pad_zeros[0]:])
        ry90_data = ry90_data-np.mean(ry90_data[my_exp.pad_zeros[0]:])
        zdata = (rx90_data + 1j*ry90_data)
        virtual_detune = 200.
        mod_zdata = zdata*np.exp(1j*time*virtual_detune/1000*np.pi*2)
        phase_origin = np.unwrap(np.angle( zdata ))
        phase = np.unwrap(np.angle( mod_zdata ))
        phase = phase - phase[-1]
        # Filtering and derivative of the phase to get the averaged frequency
        detuning_origin = signal.savgol_filter(phase_origin / 2 / np.pi, 13, 3, deriv=1, delta=0.001)
        detuning = signal.savgol_filter(phase / 2 / np.pi, 13, 3, deriv=1, delta=0.001)
        # Flux line step response in freq domain and voltage domain

        ax[0].plot(time, zdata.real, label="x" )
        ax[0].plot(time, mod_zdata.real, label=f"x-{virtual_detune}" )
        ax[0].plot(time, zdata.imag, label="y" )
        ax[0].plot(time, mod_zdata.imag, label=f"y-{virtual_detune}" )

        ax[1].plot(time, phase_origin, label="0" )
        ax[1].plot(time, phase, label=f"{virtual_detune}")

        ax[2].plot(time, detuning_origin, label="0")
        ax[2].plot(time, detuning-virtual_detune, label=f"{virtual_detune}")

        save_name = f"cryoscope_cc_{ro_name}"
        # if save_data: save_fig(folder_save_dir, save_name, dataset)

    plt.show()

#piscope
def plot_and_save_piscope(dataset, folder_save_dir = 0, save_data = True ):
    time = dataset.coords["pi_timing"].values
    freq = dataset.coords["frequency"].values

    for ro_name, data in dataset.data_vars.items():
        fig_0, ax_0 = plt.subplots()
        fig, ax = plt.subplots()
        ax.set_title('pcolormesh')
        ax.set_xlabel("T1 (us)")
        ax.set_ylabel("Flux")
        pcm = ax.pcolormesh( freq, time, data.values[0], cmap='RdBu')# , vmin=z_min, vmax=z_max)
        plt.colorbar(pcm, label='Value')

        save_name = f"piscope_{ro_name}"
        # if save_data: save_fig(folder_save_dir, save_name, dataset)

    plt.show()

#C3
def plot_and_save_xy_amp(dataset, folder_save_dir = 0, save_data = True ):
    amps = dataset.coords["amplitude_ratio"].values
    for ro_name, data in dataset.data_vars.items():
        print(f"ploting {ro_name} with shape {data.shape}")
        fig, ax = plt.subplots()
        # x90data = dataset.sel(sequence='x90').data_vars["zdata"].values
        # x90data = dataset.sel(sequence='x90').data_vars["zdata"].values

        ax.plot(amps,data[0][0], label="x90")
        ax.plot(amps,data[0][1], label="x180")
        fig.legend()
        save_name = save_name = f"xy_amp_{ro_name}"
        # if save_data: save_fig(folder_save_dir, save_name)

    plt.show()

#Cr1
def plot_and_save_readout_freq(dataset, my_exp, folder_save_dir = 0, save_data = True ):
    from exp.readout_optimization import plot_freq_signal
    dfs = dataset.coords["frequency"].values
    for ro_name, data in dataset.data_vars.items():

        data = data.values
        if my_exp.preprocess == "shot":
            data = np.average(data, axis=1)
        print(data.shape)
        fig = plt.figure()
        ax = fig.subplots(3,1)
        plot_freq_signal( dfs, data, ro_name, ax )
        fig.suptitle(f"{ro_name} RO freq")
        save_name = save_name = f"ro_freq_{ro_name}"
        # if save_data: save_fig(folder_save_dir, save_name)

    plt.show()

#CR2
def plot_and_save_readout_amp(dataset, folder_save_dir = 0, save_data = True ):
    from exp.readout_optimization import plot_amp_signal, plot_amp_signal_phase
    transposed_data = dataset.transpose("mixer", "state", "amplitude_ratio")
    amps = transposed_data.coords["amplitude_ratio"].values
    for ro_name, data in transposed_data.data_vars.items():  
        fig = plt.figure()
        ax = fig.subplots(1,2,sharex=True)
        plot_amp_signal( amps, data, ro_name, ax[0] )
        plot_amp_signal_phase( amps, data, ro_name, ax[1] )
        fig.suptitle(f"{ro_name} RO amplitude")
        save_name = save_name = f"ro_amp_{ro_name}"
        # if save_data: save_fig(folder_save_dir, save_name)
    plt.show()

#CR3
def plot_and_save_readout_fidelity(dataset, folder_save_dir = 0, save_data = True ):
    from analysis.state_distribution import train_model, create_img
    from qualang_tools.analysis import two_state_discriminator
    transposed_data = dataset.transpose("mixer", "state", "index")

    for ro_name, data in transposed_data.data_vars.items(): # elapsed_time = np.round(end_time-start_time, 1)
        new_data = np.moveaxis(data.values*1000,1,0)
        gmm_model = train_model(new_data)
        fig = plt.figure(constrained_layout=True)
        create_img(new_data, gmm_model)
        two_state_discriminator(data[0][0], data[1][0], data[0][1], data[1][1], True, True)
        save_name = save_name = f"ro_fidelity_{ro_name}"
        # if save_data: save_fig(folder_save_dir, save_name)

    plt.show()

def plot_and_save_readout_mapping(dataset, folder_save_dir = 0, save_data = True ):
    freq = dataset.coords["frequency"].values
    amp = dataset.coords["amp_ratio"].values

    for ro_name, data in dataset.data_vars.items():
        fig, ax = plt.subplots()
        iqdata = data.values[0] +1j*data.values[1]
        dist = np.abs(iqdata[1]-iqdata[0])
        norm_dist = dist/amp
        ax.set_title('pcolormesh')
        # ax.set_xlabel("T1 (us)")
        # ax.set_ylabel("Flux")
        pcm = ax.pcolormesh( freq, amp, dist.transpose(), cmap='RdBu')# , vmin=z_min, vmax=z_max)
        plt.colorbar(pcm, label='Value')
        save_name = save_name = f"ro_mapping_{ro_name}"
        # if save_data: save_fig( folder_save_dir, save_name ) 

    plt.show()

#cz chavron
def plot_and_save_cz_chavron(dataset, save_dir = 0, save_data = True ):
    time = dataset.coords["time"].values
    amps = dataset.coords["amplitude"].values

    from exp.cz_chavron import plot_cz_chavron
    for ro_name, data in dataset.data_vars.items():
        fig, ax = plt.subplots()
        plot_cz_chavron(time,amps,data.values[0],ax)
        save_name = save_name = f"cz_chavron_{ro_name}"
        # if save_data: save_fig( save_dir, save_name ) 
    plt.show()