import xarray as xr
import numpy as np
import xarray as xr
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from exp.cosine import Cosine

class CloseTo180Normalize(mcolors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=180, scale=10, clip=False):
        self.midpoint = midpoint
        self.scale = scale
        super().__init__(vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.midpoint, self.midpoint, self.vmax], [0, 0.49, 0.51, 1]
        return np.ma.masked_array(np.interp(value, x, y))
    
norm = CloseTo180Normalize(vmin=170, vmax=190, midpoint=180, scale=10)

ds = xr.load_dataset('find_CZ_accurate_point.nc')
I_g = ds.I_g
I_e = ds.I_e
t_delay, amps, Phi = ds.coords['flux duration'].values, ds.coords['flux amp'], ds.coords['phase']
row, col = len(amps), len(t_delay)

flux_Qi = 2
y_ticks_labels = [f'{value:.5f}' for value in amps]
z_phase, phase_g, phase_e, amp_g, amp_e, diff_amp = np.zeros((row,col)), np.zeros((row,col)), np.zeros((row,col)), np.zeros((row,col)), np.zeros((row,col)), np.zeros((row,col))
fit_I_g, fit_I_e = [[[] for j in range(col)] for i in range(row)], [[[] for j in range(col)] for i in range(row)]

for i in range(row):
    for j in range(col):
        try:
            fit = Cosine(Phi, I_g[i][j], plot=False)
            phase_g[i][j] = fit.out.get('phase')[0]
            amp_g[i][j] = fit.out.get('amp')[0]
            fit_I_g[i][j] = fit.fit_type(fit.x, fit.popt) * fit.y_normal
            fit = Cosine(Phi, I_e[i][j], plot=False)
            phase_e[i][j] = fit.out.get('phase')[0]
            amp_e[i][j] = fit.out.get('amp')[0]
            fit_I_e[i][j] = fit.fit_type(fit.x, fit.popt) * fit.y_normal
            dphase = (phase_g[i][j]-phase_e[i][j])/np.pi*180    
            z_phase[i][j] = np.abs((dphase)) 
            diff_amp[i][j] = np.abs(amp_g[i][j]-amp_e[i][j])
        except Exception as e: print(e)  

coords = {'flux duration': t_delay, 'flux amp': amps, 'phase': Phi}  # 定义坐标
phase_coords = {'flux duration': t_delay, 'flux amp': amps} 
dims = ['flux amp','flux duration','phase']  # 定义维度
phase_dim = ['flux amp','flux duration']
fit_I_g = xr.DataArray(fit_I_g, coords=coords, dims=dims)
fit_I_e = xr.DataArray(fit_I_e, coords=coords, dims=dims)
phase_g = xr.DataArray(phase_g, coords=phase_coords, dims=phase_dim)
phase_e = xr.DataArray(phase_e, coords=phase_coords, dims=phase_dim)
z_phase = xr.DataArray(z_phase, coords=phase_coords, dims=phase_dim)
amp_g = xr.DataArray(amp_g, coords=phase_coords, dims=phase_dim)
amp_e = xr.DataArray(amp_e, coords=phase_coords, dims=phase_dim)
diff_amp = xr.DataArray(diff_amp, coords=phase_coords, dims=phase_dim)
ds = xr.Dataset({
    'I_g':I_g,
    'I_e':I_e,
    'fit_I_g':fit_I_g,
    'fit_I_e':fit_I_e,
    'phase_g':phase_g,
    'phase_e':phase_e,
    'z_phase':z_phase,
    'amp_g':amp_g,
    'amp_e':amp_e,
    'diff_amp':diff_amp  
    },
    coords=coords
) 

####    Plot for certain duration and amp.
duration = 23
two_times_z_amp = 0.32711
phase = z_phase.sel({'flux duration': duration, 'flux amp': two_times_z_amp}, method='nearest').values
exp_e = I_e.sel({'flux duration': duration, 'flux amp': two_times_z_amp}, method='nearest')
exp_g = I_g.sel({'flux duration': duration, 'flux amp': two_times_z_amp}, method='nearest')
fitting_e = fit_I_e.sel({'flux duration': duration, 'flux amp': two_times_z_amp}, method='nearest')
fitting_g = fit_I_g.sel({'flux duration': duration, 'flux amp': two_times_z_amp}, method='nearest')

for i, flux_amp_value in enumerate(z_phase.coords['flux amp'].values):
    for j, flux_duration_value in enumerate(z_phase.coords['flux duration'].values):
        value = z_phase.isel({'flux amp': i, 'flux duration': j}).values.item()  # 使用 isel 來索引
        print(f"flux duration {flux_duration_value:.0f}, 2 times flux amp {flux_amp_value:.5f}: {value:.3f}")

plt.title(f'Z phase diff: {phase:.3f}')
plt.plot(ds.phase,exp_e,'.b')
plt.plot(ds.phase,exp_g,'.r')
plt.plot(ds.phase,fitting_e, '-b', label = 'control on', alpha=0.5)
plt.plot(ds.phase,fitting_g, '-r', label = 'control off', alpha=0.5)
plt.xlabel('phase cycle')
plt.ylabel('signal (V)')
plt.legend()
plt.show()

plt.clf()
plt.suptitle(f"q{flux_Qi} CZ phase diff. " )         
plt.tight_layout()   
plt.pcolor(z_phase.transpose(), cmap='coolwarm', norm=norm)       
plt.colorbar()
plt.xticks(np.arange(0.5, z_phase.shape[0], 1), labels=y_ticks_labels)
plt.yticks(np.arange(0.5, z_phase.shape[1], 1), labels=t_delay)
plt.xlabel('2 * z pulse amp. (V)')
plt.ylabel('z pulse duration (ns)')
plt.show()

plt.clf()
plt.suptitle(f"q{flux_Qi} CZ amp diff. " )         
plt.tight_layout()   
plt.pcolor(diff_amp.transpose())       
plt.colorbar()
plt.xticks(np.arange(0.5, z_phase.shape[0], 1), labels=y_ticks_labels)
plt.yticks(np.arange(0.5, z_phase.shape[1], 1), labels=t_delay)
plt.xlabel('2 * z pulse amp. (V)')
plt.ylabel('z pulse duration (ns)')
plt.show()