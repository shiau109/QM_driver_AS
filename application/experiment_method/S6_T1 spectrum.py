# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

from exp.save_data import save_nc, save_fig, create_folder
from exp.plotting import plot_and_save_T1_spectrum

import matplotlib.pyplot as plt

# Set parameters
init_macro = initializer(300000,mode='wait')
ro_elements = ["q0_ro", "q1_ro", "q2_ro", "q3_ro", "q4_ro"]
q_name = ["q4_xy"]
z_name = ['q4_z']

save_data = True
save_dir = link_config["path"]["output_root"]
folder_label = "T1_spectrum_1" #your data and plots with be saved under a new folder with this name
save_name = f"{q_name[0]}_T1spectrum"

n_avg = 200
max_time = 60 #us
time_resolution = 0.6 #us
flux_range = (-0.3, 0.3)
flux_resolution = 0.0015

from exp.z_pulse_relaxation_time import z_pulse_relaxation_time
dataset = z_pulse_relaxation_time( max_time, time_resolution, flux_range, flux_resolution, q_name, z_name, ro_elements, config, qmm, n_avg=n_avg, initializer=init_macro)

if save_data: 
    folder_save_dir = create_folder(save_dir, folder_label)
    save_nc( folder_save_dir, save_name, dataset) 


# Plot
time = dataset.coords["time"].values
flux = dataset.coords["z_voltage"].values

plot_and_save_T1_spectrum(dataset, time, flux, folder_save_dir, save_data)

