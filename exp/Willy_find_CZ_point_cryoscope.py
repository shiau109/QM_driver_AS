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
        state_g = [declare(bool) for _ in range(len(resonator))]
        state_g_st = [declare_stream() for _ in range(len(resonator))]        
        state_e = [declare(bool) for _ in range(len(resonator))]
        state_e_st = [declare_stream() for _ in range(len(resonator))]
        n = declare(int)
        n_st = declare_stream()
        a = declare(fixed)  
        segment = declare(int)
        flag = declare(bool)  # QUA boolean to switch between x90 and y90
        wait(flux_settle_time * u.ns)
        with for_(n, 0, n < n_avg, n+1):
            with for_(*from_array(a, amps)):
                ## This +1 is inserted because of making segment equal to actual pulse duration
                with for_(segment, t_min+1, segment <= t_max+1, segment + 1): 
                    # with for_(*from_array(phi, Phi)):
                    with for_each_(flag, [True, False]):

                        if not simulate: wait(thermalization_time * u.ns)
                        align()
                        play("x90", f"q{ramsey_Qi}_xy")
                        align()      
                        wait(5)  
                        with switch_(segment):
                            for j in range(0, const_flux_len + 1):
                                with case_(j):
                                    pulse_segments[j].run(amp_array=[(f"q{flux_Qi}_z", a)])          
                        align()
                        wait(5)
                        # Play second X/2 or Y/2
                        with if_(flag):
                            play("x90", f"q{ramsey_Qi}_xy")
                        with else_():
                            play("y90", f"q{ramsey_Qi}_xy")
                        align()  
                        wait(flux_settle_time * u.ns)   
                        multiplexed_readout(I_g, I_st_g, Q_g, Q_st_g, resonators=resonator, weights="rotated_")
                        align()  
                        for i in resonator_index:
                            assign(state_g[i], I_g[i] > ge_threshold[resonator[i]-1])  # ge_threshold[1] related to rr2
                            save(state_g[i], state_g_st[i])

                        if not simulate: wait(thermalization_time * u.ns)   
                        play("x180", f"q{control_Qi}_xy")
                        play("x90", f"q{ramsey_Qi}_xy")
                        align()      
                        wait(5)  
                        with switch_(segment):
                            for j in range(0, const_flux_len + 1):
                                with case_(j):
                                    pulse_segments[j].run(amp_array=[(f"q{flux_Qi}_z", a)])            
                        align()
                        wait(5)
                        with if_(flag):
                            play("x90", f"q{ramsey_Qi}_xy")
                        with else_():
                            play("y90", f"q{ramsey_Qi}_xy")
                        align()
                        wait(flux_settle_time * u.ns)
                        multiplexed_readout(I_e, I_st_e, Q_e, Q_st_e, resonators=resonator, weights="rotated_")
                        for i in resonator_index:
                            assign(state_e[i], I_e[i] > ge_threshold[resonator[i]-1])  # ge_threshold[1] related to rr2
                            save(state_e[i], state_e_st[i])
            save(n, n_st)        
        with stream_processing():
            n_st.save('n')
            for i in resonator_index:
                state_g_st[i].boolean_to_int().buffer( len(amps),len(t_delay),2 ).average().save(f"state_{i}g")
                state_e_st[i].boolean_to_int().buffer( len(amps),len(t_delay),2 ).average().save(f"state_{i}e")
    if simulate:
        job = qmm.simulate(config, cz_ops, SimulationConfig(15000))
        job.get_simulated_samples().con1.plot()
        plt.show()    
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(cz_ops)
        state_glist, state_elist = [f"state_{i}g" for i in resonator_index], [f"state_{i}e" for i in resonator_index]
        results = fetching_tool(job, state_glist + state_elist + ["n"], mode='live')   
        Sxx_g, Syy_g = np.zeros([len(amps), len(t_delay)]), np.zeros([len(amps), len(t_delay)])
        Sxx_e, Syy_e = np.zeros([len(amps), len(t_delay)]), np.zeros([len(amps), len(t_delay)])
        # S_g, S_e = np.zeros([len(amps), len(t_delay)]), np.zeros([len(amps), len(t_delay)])
        while results.is_processing(): 
            all_results = results.fetch_all()
            n = all_results[-1]
            state_g, state_e = all_results[0:len(resonator)], all_results[len(resonator):len(resonator)*2]
            state_g, state_e  = np.array(state_g), np.array(state_e)
            for i in range(len(amps)):
                for j in range(len(t_delay)):
                    Sxx_g[i][j] = state_g[resonator.index(ramsey_Qi), i, j, 0] * 2 - 1
                    Syy_g[i][j] = state_g[resonator.index(ramsey_Qi), i, j, 1] * 2 - 1
                    Sxx_e[i][j] = state_e[resonator.index(ramsey_Qi), i, j, 0] * 2 - 1
                    Syy_e[i][j] = state_e[resonator.index(ramsey_Qi), i, j, 1] * 2 - 1
            S_g  = Sxx_g  + 1j * Syy_g
            S_e  = Sxx_e  + 1j * Syy_e
            S_g = S_g - S_g[-1]
            S_e = S_e - S_e[-1]
            phase_g = np.angle(S_g, deg=True)
            phase_e= np.angle(S_e, deg=True)
            progress_counter(n, n_avg, start_time=results.start_time)
        qm.close()
        return phase_g, phase_e  
## TODO detune 太遠，所以相位fitting很糟，要用virtual detune拉回
type = "square"
simulate = False
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
t_min, t_max = 17, 30
t_delay = np.arange(t_min, t_max + 0.1, 1) 
pulse_segments = baked_waveform(const_flux_len, flux_Qi, type, paras)
amps = np.arange(0.3258, 0.3288, 0.0002) 
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
phase_g, phase_e = CZ_phase_diff(flux_Qi,control_Qi,ramsey_Qi,simulate,qmm)

import xarray as xr

coords = {'flux amp': amps, 'flux duration': t_delay}  # 定义坐标
dims = ['flux amp','flux duration']  # 定义维度
phase_g = xr.DataArray(phase_g, coords=coords, dims=dims)
phase_e = xr.DataArray(phase_e, coords=coords, dims=dims)
ds = xr.Dataset({
    'phase_g':phase_g,
    'phase_e':phase_e, 
    },
    coords=coords
) 
ds.to_netcdf("find_CZ_accurate_point_cryoscope.nc", engine='netcdf4', format='NETCDF4')