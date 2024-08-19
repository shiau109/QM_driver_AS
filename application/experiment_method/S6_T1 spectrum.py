# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

from exp.save_data import save_nc, save_fig


import matplotlib.pyplot as plt

# Set parameters
init_macro = initializer(300000,mode='wait')
ro_elements = ["q0_ro"]
q_name = ["q0_xy"]
z_name = ['q0_z']

save_data = False
save_dir = link_config["path"]["output_root"]
save_name = f"{q_name[0]}_T1spectrum"

n_avg = 200
max_time = 60 #us
time_resolution = 0.6 #us
flux_range = (-0.3, 0.3)
flux_resolution = 0.0015

from exp.z_pulse_relaxation_time import exp_z_pulse_relaxation_time
dataset = exp_z_pulse_relaxation_time( max_time, time_resolution, flux_range, flux_resolution, q_name, z_name, ro_elements, config, qmm, n_avg=n_avg, initializer=init_macro)

if save_data: save_nc(save_dir, save_name, dataset) 


# Plot
time = dataset.coords["time"].values
flux = dataset.coords["z_voltage"].values

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

if save_data: save_fig( save_dir, save_name ) 

plt.show()



