
import matplotlib.pyplot as plt
# from exp.rofreq_sweep_power_dep import plot_power_dep_resonator
from exp.rofreq_sweep_flux_dep import plot_flux_dep_resonator
import numpy as np
from matplotlib.figure import Figure
from abc import ABC, abstractmethod
from qualang_tools.plot.fitting import Fit


from xarray import Dataset, DataArray, open_dataset
class RawDataPainter(ABC):

    def __init__( self ):
        self.output_fig = []
        self.mode = "ave"

    @abstractmethod
    def _plot_method( self ):
        pass

    @abstractmethod
    def _data_parser( self ):
        pass

    def plot( self, dataarray:DataArray, fig_name:str, show:bool=True, **kwargs ):

        self.output_fig = []

        for name, value in kwargs.items():
            if name.lower() == 'infidelity':
                for ro_name in list(value.data_vars.keys()):
                    
                    self.plot_data = dataset.data_vars[ro_name]
                    self.plot_data_2 = value.data_vars[ro_name]
                    self.title = ro_name
                    self._data_parser()
                    fig = self._plot_method()

                    file_name = f"{fig_name}_{ro_name}"
                    self.output_fig.append((file_name,fig))
                
                if show: plt.show()
                return self.output_fig
            elif name.lower() == 'opt_result':
                self.best_para = value.x
                self.best_inf = value.fun

        if "repetition" in dataarray.coords:
            self.rep = dataarray.sel(mixer='I').coords["repetition"].values
            for ro_name in dataarray.coords["q_idx"].values:
                    datas = dataarray.sel(q_idx=ro_name)
                    data = datas.transpose("mixer","repetition","x")
                    self.plot_data = data
                    self.title = ro_name
                    self._data_parser()
                    fig = self._plot_method()

                    file_name = f"{fig_name}_{ro_name}"
                    self.output_fig.append((file_name,fig))

        else:
            for ro_name in dataarray.coords["q_idx"].values:
                data = dataarray.sel(q_idx=ro_name)
                data.attrs = dataarray.attrs
                self.plot_data = data
                self.title = ro_name
                self._data_parser()
                fig = self._plot_method()

                file_name = f"{fig_name}_{ro_name}"
                self.output_fig.append((file_name,fig))

        if show: plt.show()
        return self.output_fig

    def plot_rep(self, dataset:dict, fig_name:str, show:bool=True, **kwargs):
        
        self.output_fig = []
        
        if "repetition" in list(dataset.values())[0].coords:
            self.rep = list(dataset.values())[0].coords["repetition"].values
            for ro_name in list(dataset.values())[0].data_vars.keys():
                self.plot_data = {}
                self.title = ro_name
                for exp_name, datas in dataset.items():
                    print(exp_name)
                    data = datas.data_vars[ro_name]
                    data = data.transpose("mixer","repetition","x")
                    self.plot_data[exp_name] = data
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
        # vmax_magnitude = np.max(np.abs(s21))
        pcm = ax[0].pcolormesh(freqs, amp_ratio, np.abs(s21), cmap='RdBu')#, vmax=0.5e-5)
        ax[0].set_title(f"{title} Magnitude")
        ax[0].set_xlabel("Additional IF freq (MHz)")
        ax[0].set_ylabel("Amplitude Ratio")
        plt.colorbar(pcm, label='Value')

        pcm = ax[1].pcolormesh(freqs, amp_ratio, np.angle(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
        ax[1].set_title(f"{title} phase")
        ax[1].set_xlabel("Additional IF freq (MHz)")
        ax[1].set_ylabel("Amplitude Ratio")
        plt.colorbar(pcm, label='Value')

        plt.tight_layout()

        return fig
    
class PainterFindFluxPeriod( RawDataPainter ):

    def _data_parser( self ):
        dataarray = self.plot_data
        self.freqs = dataarray.coords["frequency"].values
        self.flux = dataarray.coords["flux"].values

        idata = dataarray.values[0]
        qdata = dataarray.values[1]
        self.zdata = idata +1j*qdata

    def _plot_method( self ):
        s21 = self.zdata
        freqs = self.freqs
        flux = self.flux
        title = self.title
        fig, ax = plt.subplots(2)
        pcm = ax[0].pcolormesh(flux, freqs, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
        ax[0].set_title(f"{title} Magnitude")
        ax[0].set_xlabel("Flux")
        ax[0].set_ylabel("Additional IF freq (MHz)")
        plt.colorbar(pcm, label='Value')

        pcm = ax[1].pcolormesh(flux, freqs, np.angle(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
        ax[1].set_title(f"{title} Phase")
        ax[1].set_xlabel("Flux")
        ax[1].set_ylabel("Additional IF freq (MHz)")
        plt.colorbar(pcm, label='Value')

        plt.tight_layout()

        return fig

class PainterFluxDepQubit( RawDataPainter ):

    def _data_parser( self ):
        dataarray = self.plot_data
        self.freqs = dataarray.coords["frequency"].values
        self.flux = dataarray.coords["amp_ratio"].values *dataarray.attrs["z_amp_const"]

        self.xy_LO = dataarray.attrs["xy_LO"][0]/1e6
        self.xy_IF_idle = dataarray.attrs["xy_IF"][0]/1e6
        self.z_offset = dataarray.attrs["z_offset"][0]

        idata = dataarray.values[0]
        qdata = dataarray.values[1]
        self.zdata = idata +1j*qdata

    def _plot_method( self ):
        s21 = self.zdata
        freqs = self.freqs
        flux = self.flux
        title = self.title
        fig, ax = plt.subplots(2)

        abs_freq = self.xy_LO+self.xy_IF_idle+freqs
        abs_flux = self.z_offset+flux
        
        # if yscale == "log":
        #     pcm = ax.pcolormesh(freqs, np.log10(amp_ratio), np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
        # else:
        pcm = ax[0].pcolormesh(abs_freq, abs_flux, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
        ax[0].axvline(x=self.xy_LO+self.xy_IF_idle, color='b', linestyle='--', label='ref IF')
        ax[0].axvline(x=self.xy_LO, color='r', linestyle='--', label='LO')
        ax[0].axhline(y=self.z_offset, color='black', linestyle='--', label='idle z')

        ax[0].set_title(f"{title} I value")
        ax[0].set_xlabel("qubit frequency (MHz)")
        ax[0].set_ylabel("voltage (V)")
        cbar = plt.colorbar(pcm, label='Value')
        from matplotlib.ticker import ScalarFormatter
        formatter = ScalarFormatter(useMathText=False)
        formatter.set_powerlimits((-2, 2))  # 设置何时使用科学记号（如 10^-2 到 10^2 范围外）
        cbar.ax.yaxis.set_major_formatter(formatter)
        ax[0].legend()

        pcm = ax[1].pcolormesh(abs_freq, abs_flux, np.angle(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
        ax[1].set_title(f"{title} Phase value")
        ax[1].axvline(x=self.xy_LO+self.xy_IF_idle, color='b', linestyle='--', label='ref IF')
        ax[1].axvline(x=self.xy_LO, color='r', linestyle='--', label='LO')
        ax[1].axhline(y=self.z_offset, color='black', linestyle='--', label='idle z')
        ax[1].set_xlabel("Additional IF freq (MHz)")
        ax[1].set_ylabel("Flux")
        plt.colorbar(pcm, label='Value')
        ax[1].legend()

        plt.tight_layout()

        return fig


class PainterQubitSpec( RawDataPainter ):

    def _data_parser( self ):
        dataarray = self.plot_data
        self.freqs = dataarray.coords["frequency"].values
        self.xy_LO = dataarray.attrs["xy_LO"][0]/1e6
        self.xy_IF_idle = dataarray.attrs["xy_IF"][0]/1e6

        idata = dataarray.values[0]
        qdata = dataarray.values[1]
        self.zdata = idata +1j*qdata

    def _plot_method( self ):
        s21 = self.zdata
        freqs = self.freqs
        title = self.title
        fig, ax = plt.subplots(2)

        abs_freq = self.xy_LO+self.xy_IF_idle+freqs

        # if yscale == "log":
        #     pcm = ax.pcolormesh(freqs, np.log10(amp_ratio), np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
        # else:
        ax[0].plot( abs_freq, np.abs(s21), color='b' )
        ax[0].axvline(x=self.xy_LO+self.xy_IF_idle, color='b', linestyle='--', label='ref IF')
        ax[0].axvline(x=self.xy_LO, color='r', linestyle='--', label='LO')
        ax[0].set_title(f"{title} Mag value")
        ax[0].set_xlabel("XY frequency [MHz]")
        ax[0].set_ylabel("Amplitude [V]")
        ax[0].legend()

        ax[1].plot( abs_freq, np.angle(s21), color='b' )
        ax[1].set_title(f"{title} Phase value")
        ax[1].axvline(x=self.xy_LO+self.xy_IF_idle, color='b', linestyle='--', label='ref IF')
        ax[1].axvline(x=self.xy_LO, color='r', linestyle='--', label='LO')
        ax[1].set_xlabel("XY frequency [MHz]")
        ax[1].set_ylabel("angle [deg]")
        ax[1].legend()

        plt.tight_layout()

        return fig
    
class PainterFluxCheck( RawDataPainter ):

    def _data_parser( self ):
        dataarray = self.plot_data
        self.freqs = dataarray.coords["frequency"].values

        self.xy_LO = dataarray.attrs["xy_LO"][0]/1e6
        self.xy_IF_idle = dataarray.attrs["xy_IF"][0]/1e6
        self.z_offset = dataarray.attrs["z_offset"][0]

        idata = dataarray.values[0]
        qdata = dataarray.values[1]
        self.zdata = idata +1j*qdata

    def _plot_method( self ):
        s21 = self.zdata
        freqs = self.freqs
        title = self.title
        fig, ax = plt.subplots(2)

        abs_freq = self.xy_LO+self.xy_IF_idle+freqs
        
        ax[0].plot(abs_freq, np.real(s21), color='b', label='I value')  
        # Find the maximum value of np.real(s21) and its corresponding frequency
        max_idx = np.argmax(np.real(s21))  # Index of the maximum value
        max_real_s21 = np.real(s21)[max_idx]  # Maximum I value
        max_freq = abs_freq[max_idx]  # Corresponding frequency

        # Annotate the maximum value on the plot
        ax[0].annotate(f"Max at {max_freq:.2f} MHz", 
                    xy=(max_freq, max_real_s21), 
                    xytext=(max_freq, max_real_s21+1e-6),  # Adjust text position
                    arrowprops=dict(facecolor='black', arrowstyle="->"))
        ax[0].set_title(f"{title} I value")
        ax[0].set_ylabel("I value")
        ax[0].set_xlabel("Additional IF freq (MHz)")
        ax[0].legend()

        # 绘制 Q (虚部) 数据的线图
        ax[1].plot(abs_freq, np.imag(s21), color='r', label='Q value')
        ax[1].set_title(f"{title} Q value")
        ax[1].set_ylabel("Q value")
        ax[1].set_xlabel("Additional IF freq (MHz)")
        ax[1].legend()

        return fig

class PainterRabi( RawDataPainter ):
    def __init__(self, Rabi_type):
        self.Rabi_type = Rabi_type
        
    def _data_parser( self ):
        dataarray = self.plot_data
        self.freqs = dataarray.coords["frequency"].values
        if self.Rabi_type == 'time':
            self.xpara = dataarray.coords["time"].values
        elif self.Rabi_type == 'power':
            self.xpara = dataarray.coords["amplitude"].values
        self.freq_LO = dataarray.attrs["ref_xy_LO"][0]/1e6
        self.freq_IF = dataarray.attrs["ref_xy_IF"][0]/1e6

        idata = dataarray.values[0]
        qdata = dataarray.values[1]
        self.zdata = idata +1j*qdata

    def _plot_method( self ):
        s21 = self.zdata
        freqs = self.freqs
        xpara = self.xpara
        title = self.title
        ref_freq = self.freq_LO+self.freq_IF
        fig, ax = plt.subplots(2)

        pcm = ax[0].pcolormesh(xpara, ref_freq+freqs, np.real(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
        ax[0].set_title(f"{title} I value")
        ax[0].set_xlabel(self.Rabi_type)
        ax[0].set_ylabel("Additional IF freq (MHz)")
        plt.colorbar(pcm, label='Value')

        pcm = ax[1].pcolormesh(xpara, ref_freq+freqs, np.imag(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
        ax[1].set_xlabel(self.Rabi_type)
        ax[1].set_title(f"{title} Q value")
        ax[1].set_ylabel("Additional IF freq (MHz)")
        plt.colorbar(pcm, label='Value')
        
        ax[0].axhline(y=ref_freq, color='black', linestyle='--', label='ref IF')
        ax[1].axhline(y=ref_freq, color='black', linestyle='--', label='ref IF')
        ax[0].legend()
        ax[1].legend()

        plt.tight_layout()

        return fig
    
class PainterT1Single( RawDataPainter ):
        
    def _data_parser( self ):
        from qcat.analysis.qubit.relaxation import qubit_relaxation_fitting
    
        dataarray = self.plot_data
        self.time = (dataarray.coords["time"].values)/1000
        idata = dataarray.values[0]
        qdata = dataarray.values[1]
        self.fit_result_i = qubit_relaxation_fitting(self.time, idata)
        self.fit_result_q = qubit_relaxation_fitting(self.time, qdata)
        self.zdata = idata +1j*qdata

    def _plot_method( self ):
        s21 = self.zdata
        time = self.time
        fit_result_i = self.fit_result_i
        fit_result_q = self.fit_result_q
        title = self.title
        fig, ax = plt.subplots(2)

        ax[0].set_title(f"{title} T1 I data")
        ax[0].set_xlabel("Wait time (us)")
        ax[0].set_ylabel(f"voltage (mV)")
        ax[0].plot( time, np.real(s21),"o", label="data",markersize=1)
        if fit_result_i is not None:
            ax[0].plot( time, fit_result_i.best_fit, label="fit")
            tau_value = fit_result_i.params['tau'].value
            ax[0].text(0.05, 0.9, f"T1: {tau_value:.2f} us", transform=ax[0].transAxes, fontsize=10, verticalalignment='top')
        ax[1].set_title(f"{title} T1 Q data")
        ax[1].set_xlabel("Wait time (us)")
        ax[1].set_ylabel(f"voltage (mV)")
        ax[1].plot( time, np.imag(s21),"o", label="data",markersize=1)
        if fit_result_q is not None:
            ax[1].plot( time, fit_result_q.best_fit, label="fit")


        plt.tight_layout()

        return fig
    
class PainterT1Repeat( RawDataPainter ):
        
    def _data_parser( self ):
        from qcat.analysis.qubit.relaxation import qubit_relaxation_fitting
        
        dataarray = self.plot_data
        self.time = (dataarray.coords["time"].values)/1000
        self.acc_T1 = []
        for i in range(self.rep.shape[-1]):
            fit_result = qubit_relaxation_fitting(self.time, dataarray.values[0][i])
            self.acc_T1.append(fit_result.params["tau"].value)
            self.acc_T1_dict[self.title] = self.acc_T1_dict.get(self.title, []) + [fit_result.params["tau"].value]
        self.idata = dataarray.values[0]

        self.mean_t1 = np.mean(self.acc_T1)
        self.err_t1 = np.std(self.acc_T1)
        bin_width = self.mean_t1 *0.05
        start_value = self.mean_t1*0.5
        end_value = self.mean_t1*1.5
        self.custom_bins = [start_value + i * bin_width for i in range(int((end_value - start_value) / bin_width) + 1)]

    def _plot_method( self ):
        idata = self.idata
        acc_T1 = self.acc_T1
        rep = self.rep
        time = self.time
        title = self.title
        custom_bins = self.custom_bins
        total_time = np.sum(time)
        fig, ax = plt.subplots(2)
        print(rep*total_time*20*1e-6/3600)
        ax[0].set_title(f"Time dependent T1")
        ax[0].set_xlabel("Wait time (us)")
        # ax[0].set_ylabel(f"Rep")
        ax[0].set_ylabel(f"hour")
        ax[0].pcolormesh( time, rep*29666.030540704727/5000/3600, idata, cmap='RdBu')
        if acc_T1 is not None:
            ax[0].plot(acc_T1,rep*29666.030540704727/5000/3600)

        ax[1].set_title(f"{title} Histogram")
        ax[1].set_xlabel("T1 time")
        ax[1].set_ylabel(f"Number")
        ax[1].hist(acc_T1, custom_bins, density=False, alpha=0.7, label='Histogram')
        ax[1].text(0.04, 
                   0.96, 
                   f"T1 = {np.format_float_scientific(self.mean_t1, precision=3)}+-{self.err_t1:.2}\n",
                   fontsize=9, 
                   color="black",
                   ha='left', 
                   va='top',
                   transform=ax[1].transAxes,
                   bbox=dict(facecolor='white', alpha=0.5))


        # Calculate mean and standard deviation
        mean_T1 = np.mean(acc_T1)
        std_T1 = np.std(acc_T1)
        
        # Plot mean and standard deviation on the histogram
        ax[1].axvline(mean_T1, color='red', linestyle='--', label=f'Mean: {mean_T1:.2f}')
        ax[1].axvline(mean_T1 - std_T1, color='green', linestyle='--', label=f'-1 Std Dev: {mean_T1 - std_T1:.2f}')
        ax[1].axvline(mean_T1 + std_T1, color='green', linestyle='--', label=f'+1 Std Dev: {mean_T1 + std_T1:.2f}')
        
        # Display mean and std as text
        ax[1].text(mean_T1, ax[1].get_ylim()[1] * 0.8, f"Mean: {mean_T1:.2f}\nStd Dev: {std_T1:.2f}",
                color="black", ha="center", bbox=dict(facecolor="white", alpha=0.6))

        ax[1].legend()

        plt.tight_layout()

        return fig
    
    def plot( self, dataset:Dataset, fig_name:str, show:bool=True ):

        self.output_fig = []
        self.acc_T1_dict = {}
        if "repetition" in dataset.coords:
            self.rep = dataset.coords["repetition"].values
            for ro_name, data in dataset.data_vars.items():
                data = data.transpose("mixer","repetition","time")
                self.plot_data = data
                self.title = ro_name
                self._data_parser()
                fig = self._plot_method()

                file_name = f"{fig_name}_{ro_name}"
                self.output_fig.append((file_name,fig))

        else:
            for ro_name, data in dataset.data_vars.items():
                data.attrs = dataset.attrs
                self.plot_data = data
                self.title = ro_name
                self._data_parser()
                fig = self._plot_method()

                file_name = f"{fig_name}_{ro_name}"
                self.output_fig.append((file_name,fig))
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xlabel("hour\nfrom 12/03 00:30")
        ax.set_ylabel("T1 time")

        for key, acc_T1_values in self.acc_T1_dict.items():
            ax.plot(self.rep*29666.030540704727/5000/3600, acc_T1_values, marker="o", label=key)  # Plot each key's T1 values as a line

        ax.legend()  # Add legend with key names
        file_name = f"{fig_name}_all"
        self.output_fig.append((file_name,fig))

        if show: plt.show()
        return self.output_fig

class PainterT1Spectrum( RawDataPainter ):
        
    def _data_parser( self ):
        from qcat.analysis.qubit.relaxation import qubit_relaxation_fitting
    
        dataarray = self.plot_data
        self.time = (dataarray.coords["time"].values)/1000
        self.flux = dataarray.coords["z_voltage"].values+dataarray.attrs["z_offset"][0]
        idata = dataarray.values[0]
        qdata = dataarray.values[1]
        self.fit_result_i = []
        self.fit_result_q = []
        self.zdata = []
        for i in range(len(idata)):
            self.fit_result_i.append(qubit_relaxation_fitting(self.time, idata[i]))
            self.fit_result_q.append(qubit_relaxation_fitting(self.time, qdata[i]))
            self.zdata.append(idata[i] +1j*qdata[i])

    def _plot_method( self ):
        fig, ax = plt.subplots()
        ax.set_title('pcolormesh')
        ax.set_xlabel("Flux")
        ax.set_ylabel("T1 (us)")
        pcm = ax.pcolormesh(self.flux, self.time, np.real(self.zdata).T, cmap='RdBu')# , vmin=z_min, vmax=z_max)
        plt.colorbar(pcm, label='Value')
        plt.tight_layout()

        return fig
        

class PainterT2Ramsey( RawDataPainter ):
    
    def __init__(self):
        self.T1 = 20
        
    def _data_parser( self ):
        from qcat.analysis.qubit.ramsey import qubit_ramsey_fitting
    
        dataarray = self.plot_data
        self.time = (dataarray.coords["time"].values)/1000 # us
        idata = dataarray.values[0]
        qdata = dataarray.values[1]
        self.fit_result_i = qubit_ramsey_fitting(self.time, self.T1, idata)
        self.fit_result_q = qubit_ramsey_fitting(self.time, self.T1, qdata)

        self.zdata = idata +1j*qdata

    def _plot_method( self ):
        s21 = self.zdata
        time = self.time
        fit_result_i = self.fit_result_i
        fit_result_q = self.fit_result_q
        title = self.title
        fig, ax = plt.subplots(2)

        ax[0].set_title(f"{title} T2 Ramsey I data")
        ax[0].set_xlabel("Wait time (us)")
        ax[0].set_ylabel(f"voltage (mV)")
        ax[0].plot( time, np.real(s21),"o", label="data",markersize=1)
        if fit_result_i is not None:
            ax[0].plot( time, fit_result_i.best_fit, label="fit")
            T_phi = fit_result_i.params['t_phi'].value
            print(f"T_phi = {T_phi}")
            print(f"T2 = {self.T1*T_phi/(2*self.T1+T_phi)}")
            print(f"detune = {fit_result_i.params['detune'].value}")

            tau_value = fit_result_i.params['tau'].value
            ax[0].text(0.05, 0.9, f"T1: {tau_value:.2g} us", transform=ax[0].transAxes, fontsize=10, verticalalignment='top')
        ax[1].set_title(f"{title} T2 Ramsey Q data")
        ax[1].set_xlabel("Wait time (us)")
        ax[1].set_ylabel(f"voltage (mV)")
        ax[1].plot( time, np.imag(s21),"o", label="data",markersize=1)
        if fit_result_q is not None:
            ax[1].plot( time, fit_result_q.best_fit, label="fit")
            T_phi = fit_result_q.params['t_phi'].value
            print(f"T_phi = {T_phi}")
            print(f"T2 = {self.T1*T_phi/(2*self.T1+T_phi)}")
            print(f"detune = {fit_result_i.params['detune'].value}")
            tau_value = fit_result_q.params['tau'].value
            # ax[0].text(0.05, 0.9, f"T1: {tau_value:.2g} us", transform=ax[0].transAxes, fontsize=10, verticalalignment='top')

        plt.tight_layout()
        
        return fig
    
class PainterT2SpinEcho( RawDataPainter ):
        
    def _data_parser( self ):
        from qcat.analysis.qubit.relaxation import qubit_relaxation_fitting
    
        dataarray = self.plot_data
        self.time = (dataarray.coords["time"].values)/1000
        idata = dataarray.values[0]
        qdata = dataarray.values[1]
        self.fit_result_i = qubit_relaxation_fitting(self.time, idata)
        self.fit_result_q = qubit_relaxation_fitting(self.time, qdata)
        self.zdata = idata +1j*qdata

    def _plot_method( self ):
        s21 = self.zdata
        time = self.time
        fit_result_i = self.fit_result_i
        fit_result_q = self.fit_result_q
        title = self.title
        fig, ax = plt.subplots(2)

        ax[0].set_title(f"{title} spin echo I data")
        ax[0].set_xlabel("Wait time (us)")
        ax[0].set_ylabel(f"voltage (mV)")
        ax[0].plot( time, np.real(s21),"o", label="data",markersize=1)
        if fit_result_i is not None:
            ax[0].plot( time, fit_result_i.best_fit, label="fit")
            print(fit_result_i.params['tau'].value)
            tau_value = fit_result_i.params['tau'].value
            ax[0].text(0.05, 0.9, f"T2: {tau_value:.2f} us", transform=ax[0].transAxes, fontsize=10, verticalalignment='top')

        ax[1].set_title(f"{title} spin echo Q data")
        ax[1].set_xlabel("Wait time (us)")
        ax[1].set_ylabel(f"voltage (mV)")
        ax[1].plot( time, np.real(s21),"o", label="data",markersize=1)
        if fit_result_q is not None:
            ax[1].plot( time, fit_result_q.best_fit, label="fit")
            print(fit_result_q.params['tau'].value)

        plt.tight_layout()
        
        return fig

class PainterT2Repeat( RawDataPainter ):
        
    def _data_parser( self ):
        from qcat.analysis.qubit.relaxation import qubit_relaxation_fitting
        
        dataarray = self.plot_data
        self.time = (dataarray.coords["time"].values)/1000
        self.acc_T2 = []
        for i in range(self.rep.shape[-1]):
            fit_result = qubit_relaxation_fitting(self.time, dataarray.values[0][i])
            self.acc_T2.append(fit_result.params["tau"].value)
        self.idata = dataarray.values[0]

        self.mean_t2 = np.mean(self.acc_T2)
        self.err_t2 = np.std(self.acc_T2)
        bin_width = self.mean_t2 *0.05
        start_value = self.mean_t2*0.5
        end_value = self.mean_t2*1.5
        self.custom_bins = [start_value + i * bin_width for i in range(int((end_value - start_value) / bin_width) + 1)]

    def _plot_method( self ):
        idata = self.idata
        acc_T2 = self.acc_T2
        rep = self.rep
        time = self.time
        title = self.title
        custom_bins = self.custom_bins

        fig, ax = plt.subplots(2)

        ax[0].set_title(f"Repeat T2")
        ax[0].set_xlabel("Wait time (us)")
        ax[0].set_ylabel(f"Rep")
        ax[0].pcolormesh( time, rep, idata, cmap='RdBu')
        if acc_T2 is not None:
            ax[0].plot(acc_T2,rep)
        # Calculate mean and standard deviation
        mean_T1 = np.mean(acc_T2)
        std_T1 = np.std(acc_T2)
        
        # Plot mean and standard deviation on the histogram
        ax[1].axvline(mean_T1, color='red', linestyle='--', label=f'Mean: {mean_T1:.2f}')
        ax[1].axvline(mean_T1 - std_T1, color='green', linestyle='--', label=f'-1 Std Dev: {mean_T1 - std_T1:.2f}')
        ax[1].axvline(mean_T1 + std_T1, color='green', linestyle='--', label=f'+1 Std Dev: {mean_T1 + std_T1:.2f}')
        ax[1].set_title(f"{title} Histogram")
        ax[1].set_xlabel("T2 time")
        ax[1].set_ylabel(f"Number")
        ax[1].hist(acc_T2, custom_bins, density=False, alpha=0.7, label='Histogram')
        # Display mean and std as text
 
        ax[1].text(0.04, 
                   0.96, 
                   f"T1 = {np.format_float_scientific(self.mean_t2, precision=3)}+-{self.err_t2:.2}\n",
                   fontsize=9, 
                   color="black",
                   ha='left', 
                   va='top',
                   transform=ax[1].transAxes,
                   bbox=dict(facecolor='white', alpha=0.5))

        ax[1].legend()
        plt.tight_layout()
        
        return fig

def power_law(power, a, p, b):
    return a * (p**power) + b

def ana_SQRB(x, y, state_discrimination ):
    from scipy.optimize import curve_fit
    if state_discrimination == True:
        p0 = [-0.35, 0.95, 0.5]
        def fit_func(power, a, p, b):
            return power_law(power, a, p, b)
    else:
        p0=[-0.0001, 0.0001, 0.0001]
        def fit_func(power, a, p, b):
            return power_law(power, a, p, b)
    pars, cov = curve_fit(
        f=fit_func,
        xdata=x,
        ydata=y,
        p0=p0,
        bounds=(-np.inf, np.inf),
        maxfev=2000,
    )
    stdevs = np.sqrt(np.diag(cov))

    print("#########################")
    print("### Fitted Parameters ###")
    print("#########################")
    if state_discrimination == True:
        print(f"A = {pars[0]:.3} ({stdevs[0]:.1}), P = {pars[1]:.3} ({stdevs[1]:.1}), B = {pars[2]:.3} ({stdevs[2]:.1})")
    else:
        print(f"A = {pars[0]:.3} ({stdevs[0]:.1}), P = {pars[1]:.3} ({stdevs[1]:.1}), B = {pars[2]:.3} ({stdevs[2]:.1})")
    # print("Covariance Matrix")
    # print(cov)
    
    return stdevs, pars

def get_interleaved_gate(interleaved_gate_index):
    if interleaved_gate_index == 0:
        return "I"
    elif interleaved_gate_index == 1:
        return "x180"
    elif interleaved_gate_index == 2:
        return "y180"
    elif interleaved_gate_index == 12:
        return "x90"
    elif interleaved_gate_index == 13:
        return "-x90"
    elif interleaved_gate_index == 14:
        return "y90"
    elif interleaved_gate_index == 15:
        return "-y90"
        

class PainterFluxCrosstalkRepeat( RawDataPainter ):

    def _data_parser( self ):
        from analysis.zline_crosstalk_analysis import analysis_crosstalk_value_fft, analysis_crosstalk_value_fitting, analysis_crosstalk_ellipse
        dataarray = self.plot_data
        print(dataarray)
        self.crosstalk = []
        for i in range(self.rep.shape[-1]):
            rep_data = dataarray.sel(repetition=i)
            if self.dataset.attrs["measure_method"] == "long_drive":
                slope, intercept, x_vals, y_vals = analysis_crosstalk_value_fitting(rep_data)
                try:
                    self.crosstalk.append(-1*slope)
                except:
                    print("no slope")
            else:
                crosstalk, freq_axes, mag = analysis_crosstalk_value_fft( rep_data )
                try:
                    self.crosstalk.append(crosstalk)
                except:
                    print("no crosstalk")

        mean_crosstalk = np.mean(self.crosstalk)
        bin_width = mean_crosstalk *0.05
        start_value = mean_crosstalk*0.5
        end_value = mean_crosstalk*1.5
        self.custom_bins = np.sort([start_value + i * bin_width for i in range(int((end_value - start_value) / bin_width) + 1)])

    def _plot_method( self ):
        crosstalk = self.crosstalk
        rep = self.rep
        title = self.title
        custom_bins = self.custom_bins
        fig, ax = plt.subplots(1)
        ax.set_title(f"Flux Crosstalk rep")
        ax.set_xlabel("Wait time (us)")
        ax.set_ylabel(f"Rep")
        # ax[0].set_ylabel(f"hour")
        print(custom_bins)
        ax.hist(crosstalk, bins="auto", density=False, alpha=0.7, label='Histogram')
        print(crosstalk)


        # Calculate mean and standard deviation
        mean_crosstalk = np.mean(crosstalk)
        std_crosstalk = np.std(crosstalk)
        
        # Plot mean and standard deviation on the histogram
        ax.axvline(mean_crosstalk, color='red', linestyle='--', label=f'Mean: {mean_crosstalk:.5g}')
        ax.axvline(mean_crosstalk - std_crosstalk, color='green', linestyle='--', label=f'-1 Std Dev: {mean_crosstalk - std_crosstalk:.5g}')
        ax.axvline(mean_crosstalk + std_crosstalk, color='green', linestyle='--', label=f'+1 Std Dev: {mean_crosstalk + std_crosstalk:.5g}')
        
        # Display mean and std as text
        ax.text(mean_crosstalk, ax.get_ylim()[1] * 0.8, f"Mean: {mean_crosstalk:.5g}\nStd Dev: {std_crosstalk:.5g}",
                color="black", ha="center", bbox=dict(facecolor="white", alpha=0.6))

        ax.legend()

        plt.tight_layout()

        return fig
    
    def plot( self, dataset:Dataset, fig_name:str, show:bool=True ):

        self.output_fig = []

        if "repetition" in dataset.coords:
            self.rep = dataset.coords["repetition"].values
            self.dataset = dataset
            for ro_name, data in dataset.data_vars.items():
                # data = data.transpose("mixer","repetition","time")
                self.plot_data = data
                self.title = ro_name
                try:
                    self._data_parser()
                    fig = self._plot_method()

                    file_name = f"{fig_name}_{ro_name}"
                    self.output_fig.append((file_name,fig))
                except:
                    print("就畫不出來啊")

        else:
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
class Painter1QRB( RawDataPainter ):
    def __init__(self):
        self.state_discrimination = False

    def _data_parser( self ):
        
        dataarray = self.plot_data
        self.x = dataarray.coords["x"].values
        self.val = dataarray.values[0]
        self.err = dataarray.values[1]

    def _plot_method( self ):
        x = self.x
        val = self.val
        err = self.err
        title = self.title
 
        stdevs, pars = ana_SQRB( x, val, self.state_discrimination)
        one_minus_p = 1 - pars[1]
        r_c = one_minus_p * (1 - 1 / 2**1)
        r_g = r_c / 1.875  # 1.875 is the average number of gates in clifford operation
        r_c_std = stdevs[1] * (1 - 1 / 2**1)
        r_g_std = r_c_std / 1.875

        fig, ax = plt.subplots()
        print(pars)
        ax.errorbar(x, val, yerr=err, marker=".")
        ax.set_title(f"{title} Single qubit RB")
        ax.set_xlabel("Number of Clifford gates")
        ax.set_ylabel("Sequence Fidelity")
        ax.plot( x, power_law(x, *pars),"o", label="data",markersize=1,linestyle="--", linewidth=2)
        ax.set_xscale('log')
        if self.state_discrimination == True:
            ax.plot( x, power_law(x, *pars, 0.5),"o", label="data",markersize=1,linestyle="--", linewidth=2)
        else:
            ax.plot( x, power_law(x, *pars),"o", label="data",markersize=1,linestyle="--", linewidth=2)
        ax.text(0.04, 
                0.96, 
                f"Error rate: 1-p = {np.format_float_scientific(one_minus_p, precision=2)}+-{stdevs[1]:.2}\n"
                f"Clifford set infidelity: r_c = {np.format_float_scientific(r_c, precision=2)}+-{r_c_std:.2}\n"
                f"Gate infidelity: r_g = {np.format_float_scientific(r_g, precision=2)}+-{r_g_std:.2}", 
                fontsize=9, 
                color="black",
                ha='left', 
                va='top',
                transform=ax.transAxes,
                bbox=dict(facecolor='white', alpha=0.5))

        plt.tight_layout()
        
        return fig

class Painter1QRBRepeatWithT1( RawDataPainter ):
    def __init__(self):
        self.state_discrimination = False

    def _data_parser( self ):
        self.plotting_datas = {}
        for exp_name, plot_data in self.plot_data.items():
            match exp_name:
                case '1QRB':
                    self.plotting_datas[exp_name] = {}
                    dataarray = plot_data
                    self.plotting_datas[exp_name]['x'] = dataarray.coords["x"].values
                    self.plotting_datas[exp_name]['val'] = dataarray.values[0]
                    self.plotting_datas[exp_name]['r_g'] = []
                    self.plotting_datas[exp_name]['r_g_std'] = []
                    for i in range(self.rep.shape[-1]):
                        stdevs, pars = ana_SQRB( self.plotting_datas[exp_name]['x'], self.plotting_datas[exp_name]['val'][i], self.state_discrimination)
                        one_minus_p = 1 - pars[1]
                        r_c = one_minus_p * (1 - 1 / 2**1)
                        self.plotting_datas[exp_name]['r_g'].append(r_c / 1.875)  # 1.875 is the average number of gates in clifford operation
                        r_c_std = stdevs[1] * (1 - 1 / 2**1)
                        self.plotting_datas[exp_name]['r_g_std'].append(r_c_std / 1.875)
                        
                case "T1":
                    from qcat.analysis.qubit.relaxation import qubit_relaxation_fitting
                    self.plotting_datas[exp_name] = {}
                    dataarray = plot_data
                    self.plotting_datas[exp_name]['time'] = (dataarray.coords["time"].values)/1000
                    self.plotting_datas[exp_name]['acc_gamma1'] = []
                    for i in range(self.rep.shape[-1]):
                        fit_result = qubit_relaxation_fitting(self.plotting_datas[exp_name]['time'], dataarray.values[0][i])
                        self.plotting_datas[exp_name]['acc_gamma1'].append(1/fit_result.params["tau"].value)
                    self.plotting_datas[exp_name]['idata'] = dataarray.values[0]


    def _plot_method( self ):
        fig, ax1 = plt.subplots()
        for exp_name, datas in self.plotting_datas.items():
            match exp_name:
                case '1QRB':
                    rep = self.rep
                    title = self.title
                    ax1.set_title(f"{title} 1QRB with Gamma 1")
                    ax1.set_xlabel("Repeation times")
                    ax1.set_ylabel("Infidelity")
                    ax1.errorbar(rep, self.plotting_datas[exp_name]['r_g'], yerr=self.plotting_datas[exp_name]['r_g_std'], marker=".")
                    ax1.plot(rep, self.plotting_datas[exp_name]['r_g'],"o", label="data",markersize=1,linestyle="--", linewidth=2)
                    ax1.tick_params(axis='y', labelcolor='blue')
                    
                case 'T1':
                    acc_gamma1 = self.plotting_datas[exp_name]['acc_gamma1']
                    rep = self.rep
                    time = self.plotting_datas[exp_name]['time']
                    title = self.title
                    total_time = np.sum(time)
                    print(rep*total_time*20*1e-6/3600)
                    ax2 = ax1.twinx()
                    ax2.set_ylabel("Gamma1")
                    ax2.plot(rep,acc_gamma1,color='orange')
                    ax2.tick_params(axis='y', labelcolor='orange')
                    

        plt.tight_layout()
    def _ana_SQRB(self, x, y ):
        from scipy.optimize import curve_fit
        if self.state_discrimination == True:
            p0 = [-0.5, 1, 0.5]
            def fit_func(power, a, p, b):
                return power_law(power, a, p, b)
        else:
            p0=[y[0]-y[-1], 1e-3, y[-1]]
            def fit_func(power, a, p, b):
                return power_law(power, a, p, b)
        pars, cov = curve_fit(
            f=fit_func,
            xdata=x,
            ydata=y,
            p0=p0,
            bounds=(-np.inf, np.inf),
            maxfev=2000,
        )
        stdevs = np.sqrt(np.diag(cov))

        print("#########################")
        print("### Fitted Parameters ###")
        print("#########################")
        if self.state_discrimination == True:
            print(f"A = {pars[0]:.3} ({stdevs[0]:.1}), P = {pars[1]:.3} ({stdevs[1]:.1})")
        else:
            print(f"A = {pars[0]:.3} ({stdevs[0]:.1}), P = {pars[1]:.3} ({stdevs[1]:.1}), B = {pars[2]:.3} ({stdevs[2]:.1})")
        # print("Covariance Matrix")
        # print(cov)
        
        return fig

class Painter1QRBInterleaved( RawDataPainter ):

    def __init__(self):
        self.interleaved_gate_index = 0
        self.state_discrimination = False

    def _data_parser( self ):
        
        dataarray = self.plot_data
        self.x = dataarray.coords["x"].values
        self.val = dataarray.values[0]
        self.err = dataarray.values[1]

    def _plot_method( self ):
        x = self.x
        val = self.val
        err = self.err
        title = self.title

        stdevs, pars = ana_SQRB( x, val, self.state_discrimination )
        one_minus_p = 1 - pars[1]
        r_c = one_minus_p * (1 - 1 / 2**1)
        r_g = r_c / 1.875  # 1.875 is the average number of gates in clifford operation
        r_c_std = stdevs[1] * (1 - 1 / 2**1)
        r_g_std = r_c_std / 1.875

        fig, ax = plt.subplots()
        ax.errorbar(x, val, yerr=err, marker=".")
        ax.set_title(f"{title} SQ interleaved RB {get_interleaved_gate(self.interleaved_gate_index)}")
        ax.set_xlabel("Number of Clifford gates")
        ax.set_ylabel("Sequence Fidelity")
        ax.plot( x, power_law(x, *pars),"o", label="data",markersize=1,linestyle="--", linewidth=2)
        ax.text(0.04, 
                0.96, 
                f"Error rate: 1-p = {np.format_float_scientific(one_minus_p, precision=2)}+-{stdevs[1]:.2}\n"
                f"Clifford set infidelity: r_c = {np.format_float_scientific(r_c, precision=2)}+-{r_c_std:.2}\n"
                f"Gate infidelity: r_g = {np.format_float_scientific(r_g, precision=2)}+-{r_g_std:.2}", 
                fontsize=9, 
                color="black",
                ha='left', 
                va='top',
                transform=ax.transAxes,
                bbox=dict(facecolor='white', alpha=0.5))

        plt.tight_layout()
        
        return fig

class Painter1QRBInfidelity( RawDataPainter ):

    def __init__(self):
        self.interleaved_gate_index = 0
        self.state_discrimination = False

    def _data_parser( self ):
        
        dataarray = self.plot_data
        dataarray_2 = self.plot_data_2
        self.x = dataarray.coords["x"].values
        self.val = dataarray.values[0]
        self.err = dataarray.values[1]
        self.val_inl = dataarray_2.values[0]
        self.err_inl = dataarray_2.values[1]

    def _plot_method( self ):
        x = self.x
        val = self.val
        err = self.err
        val_inl = self.val_inl
        err_inl = self.err_inl
        title = self.title

        fig, ax = plt.subplots()
        stdevs, pars = ana_SQRB( x, val, self.state_discrimination)
        stdevs_inl, pars_inl = ana_SQRB( x, val_inl, self.state_discrimination)

        one_minus_p = 1 - pars[1]
        r_c = one_minus_p * (1 - 1 / 2**1)
        r_g = r_c / 1.875  # 1.875 is the average number of gates in clifford operation
        r_c_std = stdevs[1] * (1 - 1 / 2**1)
        r_g_std = r_c_std / 1.875

        one_minus_p_inl = 1 - pars_inl[1]
        r_c_inl = one_minus_p_inl * (1 - 1 / 2**1)
        r_g_inl = r_c_inl / 1.875  # 1.875 is the average number of gates in clifford operation
        r_c_std_inl = stdevs_inl[1] * (1 - 1 / 2**1)
        r_g_std_inl = r_c_std_inl / 1.875

        ax.errorbar(x, val, yerr=err, marker=".")
        ax.errorbar(x, val_inl, yerr=err_inl, marker=".")
        ax.set_title(f"{title} 1QRB gate {get_interleaved_gate(self.interleaved_gate_index)} infidelity")
        ax.set_xlabel("Number of Clifford gates")
        ax.set_ylabel("Sequence Fidelity")
        if self.state_discrimination == True:
            ax.plot( x, power_law(x, *pars),"o", label="data",markersize=1,linestyle="--", linewidth=2)
            ax.plot( x, power_law(x, *pars_inl),"o", label="data_inl",markersize=1,linestyle="--", linewidth=2)
        else:
            ax.plot( x, power_law(x, *pars),"o", label="data",markersize=1,linestyle="--", linewidth=2)
            ax.plot( x, power_law(x, *pars_inl),"o", label="data_inl",markersize=1,linestyle="--", linewidth=2)
        ax.legend()
        ax.text(0.96, 
                0.28, 
                f"Error rate: 1-p = {np.format_float_scientific(one_minus_p, precision=3)}+-{stdevs[1]:.3}\n"
                f"Clifford set infidelity: r_c = {np.format_float_scientific(r_c, precision=3)}+-{r_c_std:.3}\n"
                f"Gate infidelity: r_g = {np.format_float_scientific(r_g, precision=3)}+-{r_g_std:.3}", 
                fontsize=9, 
                color="black",
                ha='right', 
                va='bottom',
                transform=ax.transAxes,
                bbox=dict(facecolor='white', alpha=0.5))
        ax.text(0.96, 
                0.13, 
                f"Inl Error rate: 1-p = {np.format_float_scientific(one_minus_p_inl, precision=3)}+-{stdevs_inl[1]:.3}\n"
                f"Inl Clifford set infidelity: r_c = {np.format_float_scientific(r_c_inl, precision=3)}+-{r_c_std_inl:.3}\n"
                f"Inl Gate infidelity: r_g = {np.format_float_scientific(r_g_inl, precision=3)}+-{r_g_std_inl:.3}", 
                fontsize=9, 
                color="black",
                ha='right', 
                va='bottom',
                transform=ax.transAxes,
                bbox=dict(facecolor='white', alpha=0.5))
        ax.text(0.96, 
                0.05, 
                f"specific gate infidelity = {np.format_float_scientific((1-pars_inl[1]/pars[1]) * (1 / 2**1), precision=3)}+-{pars_inl[1]/pars[1] * ((stdevs[1]/pars[1])**2 + (stdevs_inl[1]/pars_inl[1])**2)**(1/2):.3}",
                fontsize=9, 
                color="black",
                ha='right', 
                va='bottom',
                transform=ax.transAxes,
                bbox=dict(facecolor='white', alpha=0.5))

        plt.tight_layout()
        
        return fig

class Painter1QRBOptimization( RawDataPainter ):

    def __init__(self):
        self.interleaved_gate_index = 0
        
    def _data_parser( self ):
        
        dataarray = self.plot_data
        self.itr = dataarray.coords["iteration"].values
        self.inf = dataarray.values[0]

    def _plot_method( self ):
        itr = self.itr
        inf = self.inf
        title = self.title

        fig, ax = plt.subplots()
        # ax.errorbar(x, val, yerr=err, marker=".")
        ax.set_title(f"{title} 1QRB gate {get_interleaved_gate(self.interleaved_gate_index)} optimization")
        ax.set_xlabel("Number of Iteration")
        ax.set_ylabel("Sequence Fidelity")
        ax.plot( itr, inf,"o", label="data",markersize=1,linestyle="--", linewidth=2)
        ax.text(0.04, 
                0.96, 
                f"Best gate parameters : {self.best_para}\n"
                f"Best gate infidelity : {self.best_inf}\n",
                fontsize=9, 
                color="black",
                ha='left', 
                va='top',
                transform=ax.transAxes,
                bbox=dict(facecolor='white', alpha=0.5))
        
        plt.tight_layout()
        
        return fig

class Painter1QRBShiftOneParam( RawDataPainter ):

    def __init__(self):
        self.param_name = 'amp'
        
    def _data_parser( self ):
        
        dataarray = self.plot_data
        self.param = dataarray.coords[self.param_name].values
        self.inf = dataarray.values[0]
        self.err = dataarray.values[1]

    def _plot_method( self ):
        param = self.param
        inf = self.inf
        err = self.err
        title = self.title

        fig, ax = plt.subplots()
        # ax.errorbar(x, val, yerr=err, marker=".")
        ax.set_title(f"{title} 1QRB gate shift {self.param_name}")
        ax.set_xlabel(f"{self.param_name}")
        ax.set_ylabel("Sequence Fidelity")
        ax.errorbar(param, inf, yerr=err, marker=".")
        ax.plot(param, inf,"o", label="data",markersize=1,linestyle="--", linewidth=2)
        ax.text(0.96, 
                0.05, 
                f"smallest specific gate infidelity = {np.format_float_scientific(inf[np.argmin(inf)], precision=4)}+-{err[np.argmin(inf)]:.4}\n"
                f"{self.param_name} = {param[np.argmin(inf)]}",
                fontsize=9, 
                color="black",
                ha='right', 
                va='bottom',
                transform=ax.transAxes,
                bbox=dict(facecolor='white', alpha=0.5))
        plt.tight_layout()
        
        return fig
        
class PainterXYCali( RawDataPainter ):
    def __init__(self):
        self.process = 'amp'

    def _data_parser( self ):
        dataarray = self.plot_data
        self.sequence = dataarray.coords["sequence"].values
        match self.process:
            case 'amp':
                self.x = dataarray.coords["amplitude_ratio"].values
            case 'freq':
                self.x = dataarray.coords["time"].values
            case 'drag':
                self.x = dataarray.coords["drag_coef"].values
        idata_1 = dataarray.values[0][0]
        qdata_1 = dataarray.values[1][0]
        self.zdata_1 = idata_1 +1j*qdata_1
        idata_2 = dataarray.values[0][1]
        qdata_2 = dataarray.values[1][1]
        self.zdata_2 = idata_2 +1j*qdata_2

    def _plot_method( self ):
        fig, ax = plt.subplots()
        ax.plot(self.x, np.real(self.zdata_1), label=self.sequence[0])
        ax.plot(self.x, np.real(self.zdata_2), label=self.sequence[1])
        fig.legend()
        plt.tight_layout()

        return fig

class Painter1QDB( RawDataPainter ):
    def __init__(self):
        self.gate = 1

    def _data_parser( self ):
        from qcat.analysis.qubit.gate_amp import gate_amp_fitting
        dataarray = self.plot_data
        self.x = dataarray.coords["repeat_time"].values
        idata = dataarray.values[0]
        qdata = dataarray.values[1]
        self.fit_result_i = gate_amp_fitting(self.x, idata)
        self.fit_result_q = gate_amp_fitting(self.x, qdata)
        self.zdata = idata +1j*qdata

    def _plot_method( self ):
        s21 = self.zdata
        fig, ax = plt.subplots()
        ax.plot(self.x, np.real(s21), label=self._gate_match())
        if self.fit_result_i is not None:
            ax.plot( self.x, self.fit_result_i.best_fit, label="fit")
            match self.gate:
                case 3:
                    print(f"period = {self.fit_result_i.params['period'].value}")
                    print(f"amp diff = {1+1/(self.fit_result_i.params['period'].value)}")
        fig.legend()
        plt.tight_layout()

        return fig
    
    def _gate_match(self):
        match self.gate:
            case 1:
                return 'X X'
            case 2:
                return 'X -X'
            case 3:
                return 'Y Y'
            case 4:
                return 'Y -Y'

class PainterSQDBAll( RawDataPainter ):

    def _data_parser( self ):
        from qcat.analysis.qubit.gate_amp import gate_amp_fitting
        dataarray = self.plot_data
        self.x = dataarray.coords["repeat_time"].values
        self.seq = dataarray.coords["sequence"].values
        self.idata = []
        self.fit_result = []
        for data in dataarray.values[0]:
            self.idata.append(data)
            self.fit_result.append(gate_amp_fitting(self.x, data))

    def _plot_method( self ):
        fig, ax = plt.subplots()
        for i in range(len(self.seq)):
            ax.plot(self.x, self.idata[i], label=self.seq[i])
            if self.fit_result[i] is not None:
                ax.plot( self.x, self.fit_result[i].best_fit, label="fit")
            # match self.gate:
            #     case 3:
            #         print(f"period = {self.fit_result_i.params['period'].value}")
            #         print(f"amp diff = {1+1/(self.fit_result_i.params['period'].value)}")
        fig.legend()
        plt.tight_layout()

        return fig

#S2 finished
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

#S3 finished
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

#S4 finished
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

#S5 finished
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
    figs = []
    for ro_name, data in dataset.data_vars.items():
        fig_0, ax_0 = plt.subplots()
        ax_0.plot(time, data.values[0][0])
        print( data.values[0].shape )
        fig, ax = plt.subplots()
        ax.set_title('pcolormesh')
        ax.set_xlabel("T1 (us)")
        ax.set_ylabel("Flux")
        pcm = ax.pcolormesh( time/1000, flux+dataset.attrs["z_offset"][0], data.values[0], cmap='RdBu')# , vmin=z_min, vmax=z_max)
        plt.colorbar(pcm, label='Value')
        save_name = f"T1_spectrum_{ro_name}"
        figs.append((save_name,fig))
        plt.close()
    
    return figs

    
#S6 finished
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

#S6 rep finished
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

#S7 rep
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
class PainterROFreq( RawDataPainter ):

    def _data_parser( self ):

        transposed_data = self.plot_data.transpose("mixer", "prepare_state", "frequency")

        dataarray = transposed_data
        self.prepare_state = dataarray.coords["prepare_state"].values
        self.frequency = dataarray.coords["frequency"].values

        idata = dataarray.values[0]
        qdata = dataarray.values[1]
        self.zdata = transposed_data

    def _plot_method( self ):

        zdata = self.zdata
        frequency = self.frequency
        title = self.title

        fig = plt.figure()
        ax = fig.subplots(3,1,sharex=True)
        from exp.readout_optimization import plot_freq_signal

        plot_freq_signal( frequency, zdata, title, ax )

        fig.suptitle(f"{title} RO freq")
        save_name = f"ro_freq_{title}"
        plt.close()
        return fig

#CR2
class PainterROPower( RawDataPainter ):

    def _data_parser( self ):

        transposed_data = self.plot_data.transpose("mixer", "prepare_state", "amplitude_ratio")

        dataarray = transposed_data
        self.prepare_state = dataarray.coords["prepare_state"].values
        self.r_amp = dataarray.coords["amplitude_ratio"].values

        idata = dataarray.values[0]
        qdata = dataarray.values[1]
        self.zdata = transposed_data

    def _plot_method( self ):
        from exp.readout_optimization import plot_amp_signal, plot_amp_signal_phase

        zdata = self.zdata
        r_amp = self.r_amp
        title = self.title

        fig = plt.figure()
        ax = fig.subplots(1,2,sharex=True)
        # for i in range(2):
        plot_amp_signal( r_amp, zdata, title, ax[0] )
        plot_amp_signal_phase( r_amp, zdata, title, ax[1] )
        fig.suptitle(f"{title} RO amplitude")
        save_name = f"ro_amp_{title}"
        plt.close()
        return fig
    



#CR3
def plot_and_save_readout_fidelity(dataset, folder_save_dir = 0, save_data = True )->list:
    from analysis.state_distribution import train_model, create_img
    from qualang_tools.analysis import two_state_discriminator
    transposed_data = dataset.transpose("mixer", "prepare_state", "shot")


    figs = []
    for ro_name, data in transposed_data.data_vars.items(): # elapsed_time = np.round(end_time-start_time, 1)
        new_data = np.moveaxis(data.values*1000,1,0)
        gmm_model = train_model(new_data)
        # fig = plt.figure(constrained_layout=False)
        fig = create_img(new_data, gmm_model)
        two_state_discriminator(data[0][0], data[1][0], data[0][1], data[1][1], True, True)
        save_name = f"ro_fidelity_{ro_name}"
        figs.append((save_name,fig))
        plt.close()
    return figs

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
    


#Plotting
#Needed value

if __name__ == '__main__':
    # dataset = {}
    # dataset["1QRB"] = open_dataset(r"D:\HW\Quela\QM\QM_data\5Q4C_20241016_2_AS1608\5Q4C_20241016_2_AS1608\20241210_094344_T1_with_1QRB_repeat\T1_with_1QRB_repeat_1QRB.nc")
    # dataset['T1'] = open_dataset(r"D:\HW\Quela\QM\QM_data\5Q4C_20241016_2_AS1608\5Q4C_20241016_2_AS1608\20241210_094344_T1_with_1QRB_repeat\T1_with_1QRB_repeat_T1.nc")
    # folder_label = "1QRB_with_T1_repeat"
    # state_discrimination = True
    # # param_name = 'draga'
    # # interleaved_gate_index = 0


    # # Painting method
    # painter = Painter1QRBRepeatWithT1()
    # painter.state_discrimination = state_discrimination
    # # painter.param_name = param_name
    # # painter.interleaved_gate_index = interleaved_gate_index
    # figs = painter.plot_rep(dataset,folder_label)
    
    dataset = open_dataset(r"D:\HW\Quela\QM\QM_data\5Q4C_20241016_2_AS1608\5Q4C_20241016_2_AS1608\20241211_185323_1QDB_all\1QDB_all.nc")
    folder_label = "SQDB_All"

    # Painting method
    painter = PainterSQDBAll()
    figs = painter.plot(dataset,folder_label)

