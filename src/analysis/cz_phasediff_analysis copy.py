import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

filename = r"C:\Users\admin\SynologyDrive\09 Data\Fridge Data\Qubit\20240920_DRKe_5Q4C\raw_data\20241004_123718_CZ_diff\q1q0_cz_phasediff_shot.nc"
dataset = xr.open_dataset(filename,engine='netcdf4', format='NETCDF4')


# Assuming your dataset is called `dataset`
# Extracting the "I" component for "q0_ro"
print(dataset)
data_q0_I = dataset["q0_ro"].sel(mixer="I")

# Taking the average and standard deviation across "shot"
data_q0_I_avg = data_q0_I.mean(dim="shot")
data_q0_I_std = data_q0_I.std(dim="shot")

# Selecting the first elements of "c_amp" and "cz_amp", and setting "rotate" to 0
data_q0_I_avg_filtered = data_q0_I_avg.sel(c_amp=dataset.coords['c_amp'][0],
                                           cz_amp=dataset.coords['cz_amp'][0])
data_q0_I_std_filtered = data_q0_I_std.sel(c_amp=dataset.coords['c_amp'][0],
                                           cz_amp=dataset.coords['cz_amp'][0])

# Now plot for both `control=0` and `control=1` on the same plot with error bars
phase = dataset.coords['phase']
plt.figure()

# Control = 0 with error bars (sigma)
plt.errorbar(phase, data_q0_I_avg_filtered.sel(control=0),
             #yerr=data_q0_I_std_filtered.sel(control=0),
             label='Control = 0', fmt='-o', capsize=3)

# Control = 1 with error bars (sigma)
plt.errorbar(phase, data_q0_I_avg_filtered.sel(control=1),
             #yerr=data_q0_I_std_filtered.sel(control=1),
             label='Control = 1', fmt='-o', capsize=3)

# Add labels and title
plt.xlabel('Phase')
plt.ylabel('I Component')
plt.title('q0_ro I component over Phase for Control = 0 and 1')
plt.legend()
plt.grid(True)
plt.show()
