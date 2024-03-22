import xarray as xr
import numpy as np
import xarray as xr
from matplotlib import pyplot as plt
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

ds = xr.load_dataset('find_CZ_accurate_point_cryoscope.nc')
phase_g = ds.phase_g
phase_e = ds.phase_e
t_delay, amps = ds.coords['flux duration'].values, ds.coords['flux amp']
row, col = len(amps), len(t_delay)
flux_Qi = 2
y_ticks_labels = [f'{value:.5f}' for value in amps]
z_phase = xr.DataArray(phase_g - phase_e, coords=ds.coords, dims=ds.dims)
ds['z_phase'] = (z_phase / np.pi * 180) % 360
z_phase = ds.z_phase

####    Plot for certain duration and amp.
# duration = 20
# two_times_z_amp = 0.326
# phase = z_phase.sel({'flux duration': duration, 'flux amp': two_times_z_amp}, method='nearest').values

# for i, flux_amp_value in enumerate(z_phase.coords['flux amp'].values):
#     for j, flux_duration_value in enumerate(z_phase.coords['flux duration'].values):
#         value = z_phase.isel({'flux amp': i, 'flux duration': j}).values.item()  # 使用 isel 來索引
#         print(f"flux duration {flux_duration_value:.0f}, 2 times flux amp {flux_amp_value:.5f}: {value:.3f}")

# plt.title(f'Z phase diff: {phase:.3f}')
# plt.xlabel('phase cycle')
# plt.ylabel('signal (V)')
# plt.legend()
# plt.show()

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