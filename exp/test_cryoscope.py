import xarray as xr
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal, optimize


cryo_const_flux_len = 200

ds = xr.load_dataset('cryo_noFilter.nc')

plt.subplot(211)
phase = ds.state_phase
ds.state_phase.plot(label='phase')
plt.xlabel('')
plt.legend()
plt.subplot(212)
ds.state_detuning.plot(label='detuning')
plt.legend()
plt.show()


xplot = np.arange(0, cryo_const_flux_len + 1, 1)
detuning = signal.savgol_filter(phase / 2 / np.pi, 21, 2, deriv=1, delta=10)
step_response_freq = detuning / np.average(detuning[-int(cryo_const_flux_len / 2) :])

plt.subplot(211)
plt.plot(xplot,detuning, label = 'detuning')
plt.legend()

plt.subplot(212)
plt.plot(xplot,step_response_freq, label = 'response_freq')
plt.legend()
plt.show()

# print(type(step_response_freq))
# print(detuning)
# print(np.average(detuning[-int(cryo_const_flux_len / 2) :]))

# detuning = ds.state_detuning
# step_response_freq.plot(label='step_response_freq', marker='.')
# plt.legend()

# plt.show()