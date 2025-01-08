# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

from exp.plotting import plot_and_save_T1_spectrum

import matplotlib.pyplot as plt

# Set parameters
# init_macro = initializer(200000,mode='wait')
# ro_elements = ["q2_ro"]
# q_name = ["q2_xy"]
# z_name = ['q2_z']

# n_avg = 200
# max_time = 60 #us
# time_resolution = 0.6 #us
# flux_range = (-0.6, 0.6)
# flux_resolution = 0.003

from exp.z_pulse_relaxation_time import z_pulse_relaxation_time
# dataset = z_pulse_relaxation_time( max_time, time_resolution, flux_range, flux_resolution, q_name, z_name, ro_elements, config, qmm, n_avg=n_avg, initializer=init_macro)
my_exp = z_pulse_relaxation_time(config, qmm)
my_exp.max_time = 40
my_exp.time_resolution = 0.4
my_exp.flux_range = [0,0.1] # [-0.08,0.08]
my_exp.flux_resolution = 0.01  # 0.0008
my_exp.q_name = ["q2_xy"]

import exp.config_par as gc

z= "q2_z"
my_exp.ref_z_offset = {z: gc.get_offset(z, config)}

my_exp.ro_elements = ["q2_ro"]

my_exp.initializer = initializer(40000,mode='wait')
dataset = my_exp.run( 400 )

save_data = 1
if save_data: 
    from exp.save_data import DataPackager
    folder_label = "T1_spectrum" #your data and plots will be saved under a new folder with this name
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,"T1_spectrum")


# Plot
from exp.plotting import PainterT1Spectrum
painter = PainterT1Spectrum()
figs = painter.plot(dataset,folder_label)
if save_data: dp.save_figs( figs )


# time = dataset.coords["time"].values
# flux = dataset.coords["z_voltage"].values

# plot_and_save_T1_spectrum(dataset, time, flux, save_dir, save_data)

