from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool, progress_counter
from common_fitting_func import *
import numpy as np
import matplotlib.pyplot as plt
from qualang_tools.bakery import baking
from macros import multiplexed_readout
# from cosine import Cosine
import matplotlib.colors as mcolors

class CloseTo180Normalize(mcolors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=180, scale=10, clip=False):
        self.midpoint = midpoint
        self.scale = scale
        super().__init__(vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.midpoint, self.midpoint, self.vmax], [0, 0.49, 0.51, 1]
        return np.ma.masked_array(np.interp(value, x, y))
    
norm = CloseTo180Normalize(vmin=170, vmax=190, midpoint=180, scale=10)

def baked_waveform(pulse_duration, flux_qubit, type, paras = None):
    pulse_segments = []
    if type == 'square':
        waveform = np.array([const_flux_amp] * const_flux_len)
        for i in range(0, pulse_duration + 1):
            with baking(config, padding_method="symmetric_l") as b:
                if i == 0:  # Otherwise, the baking will be empty and will not be created
                    wf = [0.0] * 16
                else:
                    wf = waveform[:i].tolist()
                b.add_op("flux_pulse", f"q{flux_qubit}_z", wf)
                b.play("flux_pulse", f"q{flux_qubit}_z")
            pulse_segments.append(b)

    elif type == 'eerp':
        for i in range(0, pulse_duration + 1):
            p = [paras[0],paras[1],paras[2]]
            wf = EERP(*p,i).tolist()
            with baking(config, padding_method="symmetric_l") as b:
                b.add_op("flux_pulse", f"q{flux_qubit}_z", wf)
                b.play("flux_pulse", f"q{flux_qubit}_z")
            pulse_segments.append(b)
    return pulse_segments

def CZ_phase_diff(flux_Qi,control_Qi,ramsey_Qi,simulate,qmm):
    with program() as cz_ops:
        I_g = [declare(fixed) for i in range(len(resonator))]
        Q_g = [declare(fixed) for i in range(len(resonator))] 
        I_e = [declare(fixed) for i in range(len(resonator))]
        Q_e = [declare(fixed) for i in range(len(resonator))] 
        I_st_g = [declare_stream() for i in range(len(resonator))]
        Q_st_g = [declare_stream() for i in range(len(resonator))]
        I_st_e = [declare_stream() for i in range(len(resonator))]
        Q_st_e = [declare_stream() for i in range(len(resonator))]
        n = declare(int)
        n_st = declare_stream()
        phi = declare(fixed)
        a = declare(fixed)  
        segment = declare(int)
        wait(flux_settle_time * u.ns)
        with for_(n, 0, n < n_avg, n+1):
            with for_(*from_array(a, amps)):
                ## This +1 is inserted because of making segment equal to actual pulse duration
                with for_(segment, t_min+1, segment <= t_max+1, segment + 1): 
                    with for_(*from_array(phi, Phi)):

                        if not simulate: wait(thermalization_time * u.ns)
                        align()
                        play("x90", f"q{ramsey_Qi}_xy")
                        align()      
                        wait(5)  
                        with switch_(segment):
                            for j in range(0, const_flux_len + 1):
                                with case_(j):
                                    pulse_segments[j].run(amp_array=[(f"q{flux_Qi}_z", a)])  
                        frame_rotation_2pi(phi, f"q{ramsey_Qi}_xy")            
                        align()
                        wait(5)
                        play("x90", f"q{ramsey_Qi}_xy")
                        wait(flux_settle_time * u.ns)
                        multiplexed_readout(I_g, I_st_g, Q_g, Q_st_g, resonators=resonator, weights="rotated_")
                        align() 

                        if not simulate: wait(thermalization_time * u.ns)              
                        play("x180", f"q{control_Qi}_xy")
                        play("x90", f"q{ramsey_Qi}_xy")
                        align()      
                        wait(5)  
                        with switch_(segment):
                            for j in range(0, const_flux_len + 1):
                                with case_(j):
                                    pulse_segments[j].run(amp_array=[(f"q{flux_Qi}_z", a)])  
                        frame_rotation_2pi(phi, f"q{ramsey_Qi}_xy")            
                        align()
                        wait(5)
                        play("x90", f"q{ramsey_Qi}_xy")
                        wait(flux_settle_time * u.ns)
                        align()
                        multiplexed_readout(I_e, I_st_e, Q_e, Q_st_e, resonators=resonator, weights="rotated_")
            save(n, n_st)        
        with stream_processing():
            n_st.save('n')
            for i in resonator_index:
                I_st_g[i].buffer( len(amps),len(t_delay),len(Phi) ).average().save(f"I{i}g")
                I_st_e[i].buffer( len(amps),len(t_delay),len(Phi) ).average().save(f"I{i}e")
    if simulate:
        job = qmm.simulate(config, cz_ops, SimulationConfig(15000))
        job.get_simulated_samples().con1.plot()
        plt.show()    
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(cz_ops)
        # row,col = len(amps),len(t_delay)
        Ig_list, Ie_list= [f"I{i}g" for i in resonator_index], [f"I{i}e" for i in resonator_index]
        results = fetching_tool(job, Ig_list + Ie_list + ["n"], mode='live')   
        # z_phase = np.zeros((row,col))
        # phase_g = np.zeros((row,col))
        # phase_e = np.zeros((row,col))
        # amp_g = np.zeros((row,col))
        # amp_e = np.zeros((row,col))
        # fit_I_g = [[[] for j in range(col)] for i in range(row)]
        # fit_I_e = [[[] for j in range(col)] for i in range(row)]
        while results.is_processing(): 
            all_results = results.fetch_all()
            n = all_results[-1]
            Ig, Ie= all_results[0:len(resonator)], all_results[len(resonator):len(resonator)*2]
            for i in resonator_index:
                Ig[i] = u.demod2volts(Ig[i], readout_len)
                Ie[i] = u.demod2volts(Ie[i], readout_len)
            progress_counter(n, n_avg, start_time=results.start_time)
            # for i in range(row):
            #     for j in range(col):
            #         try:
            #             fit = Cosine(Phi, Ig[plot_index][i][j], plot=False)
            #             phase_g[i][j] = fit.out.get('phase')[0]
            #             amp_g[i][j] = fit.out.get('amp')[0]
            #             fit_I_g[i][j] = fit.fit_type(fit.x, fit.popt) * fit.y_normal
            #             fit = Cosine(Phi, Ie[plot_index][i][j], plot=False)
            #             phase_e[i][j] = fit.out.get('phase')[0]
            #             amp_e[i][j] = fit.out.get('amp')[0]
            #             fit_I_e[i][j] = fit.fit_type(fit.x, fit.popt) * fit.y_normal
            #             dphase = (phase_g[i][j]-phase_e[i][j])/np.pi*180    
            #             z_phase[i][j] = np.abs((dphase)) 
            #         except Exception as e: print(e)  
            # live_plotting(z_phase)
        qm.close()
        plt.show()
        return Ig, Ie

def live_plotting(z_phase):
    plt.clf()
    plt.suptitle(f"q{ramsey_Qi} CZ phase diff. \n Number of average = " + str(n_avg))         
    plt.tight_layout()   
    plt.pcolor(z_phase, cmap='coolwarm', norm=norm)       
    plt.colorbar()
    plt.xticks(np.arange(0.5, z_phase.shape[1], 1), labels=t_delay)
    plt.yticks(np.arange(0.5, z_phase.shape[0], 1), labels=y_ticks_labels)
    plt.xlabel('z pulse duration (ns)')
    plt.ylabel('2 * z pulse amp. (V)')
    plt.pause(1.0)

type = "square"
simulate = True
Phi = np.arange(0, 5, 0.05) # 5 rotations
n_avg = 200
resonator = [2,3]   ###  [2,3] means measuring rr2 and rr3
resonator_index = [resonator.index(i) for i in resonator]
control_Qi = 2
ramsey_Qi = 3
flux_Qi = 2
plot_index = resonator.index(ramsey_Qi)      ### related to resonator_index
edge_width = 10
edge_sigma = 6
paras=[const_flux_amp,edge_sigma,edge_width]
t_min, t_max = 21, 28
t_delay = np.arange(t_min, t_max + 0.1, 1) 
pulse_segments = baked_waveform(const_flux_len, flux_Qi, type, paras)
amps = np.arange(0.3269, 0.3276, 0.00007) 
y_ticks_labels = [f'{value:.5f}' for value in amps]
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
Ig, Ie = CZ_phase_diff(flux_Qi,control_Qi,ramsey_Qi,simulate,qmm)

import xarray as xr

coords = {'flux duration': t_delay, 'flux amp': amps, 'phase': Phi}  # 定义坐标
# phase_coords = {'flux duration': t_delay, 'flux amp': amps} 
dims = ['flux amp','flux duration','phase']  # 定义维度
# phase_dim = ['flux amp','flux duration']
I_g = xr.DataArray(Ig[plot_index], coords=coords, dims=dims)
I_e = xr.DataArray(Ie[plot_index], coords=coords, dims=dims)
# fit_I_g = xr.DataArray(fit_I_g, coords=coords, dims=dims)
# fit_I_e = xr.DataArray(fit_I_e, coords=coords, dims=dims)
# phase_g = xr.DataArray(phase_g, coords=phase_coords, dims=phase_dim)
# phase_e = xr.DataArray(phase_e, coords=phase_coords, dims=phase_dim)
# z_phase = xr.DataArray(z_phase, coords=phase_coords, dims=phase_dim)
# amp_g = xr.DataArray(phase_g, coords=phase_coords, dims=phase_dim)
# amp_e = xr.DataArray(phase_e, coords=phase_coords, dims=phase_dim)
ds = xr.Dataset({
    'I_g':I_g,
    'I_e':I_e,
    # 'fit_I_g':fit_I_g,
    # 'fit_I_e':fit_I_e,
    # 'phase_g':phase_g,
    # 'phase_e':phase_e,
    # 'z_phase':z_phase,
    # 'amp_g':amp_g,
    # 'amp_e':amp_e  
    },
    coords=coords
) 
ds.to_netcdf("find_CZ_accurate_point.nc", engine='netcdf4', format='NETCDF4')