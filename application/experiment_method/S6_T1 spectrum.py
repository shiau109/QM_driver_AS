
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

from exp.z_pulse_relaxation_time import exp_z_pulse_relaxation_time
import numpy as np
from analysis.plot_T1_histogram import tune_flux_t1_spectrum, plot_qubit_flux_decay
# Dynamic config
from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from ab.QM_config_dynamic import initializer

spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, _ = spec.buildup_qmm()
init_macro = initializer(150000,mode='wait')


ro_elements = ["q0_ro"]
q_name = ['q0_xy']
z_name = ['q0_z']
n_avg = 100
max_time = 2 #us
time_resolution = 0.008 #us
from exp.relaxation_time import *
flux_range = (-0.05, 0.05)
flux_resolution = 0.005
dataset = exp_z_pulse_relaxation_time( max_time, time_resolution, flux_range, flux_resolution, q_name, z_name, ro_elements, config, qmm, n_avg=n_avg, initializer=init_macro)

# Plot
time = dataset.coords["time"].values
flux = dataset.coords["z_voltage"].values

print(time.shape, flux.shape)
from exp.relaxation_time import plot_T1
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

plt.show()



save_data = False
if save_data:
    from exp.save_data import save_nc
    import sys
    save_nc(r"D:\Data\03205Q4C_6", f"{q_name}_T1_spectrum", dataset) 