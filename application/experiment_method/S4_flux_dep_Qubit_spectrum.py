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

import matplotlib.pyplot as plt
from exp.plotting import plot_and_save_flux_dep_Qubit

# Start meausrement
from exp.xyfreq_sweep_flux_dep import XYFreqFlux
my_exp = XYFreqFlux(config, qmm)
my_exp.ro_elements = ["q1_ro", "q3_ro"]
my_exp.xy_elements = ['q1_xy',"q3_xy"]
my_exp.z_elements = ['q3_z']
my_exp.initializer=initializer(10000,mode='wait')
my_exp.xy_driving_time = 20
my_exp.xy_amp_mod = 0.02
my_exp.z_amp_ratio_range = (-0.1,0.1)
my_exp.z_amp_ratio_resolution = 0.02
my_exp.freq_range = (-400,400)
my_exp.freq_resolution = 4
my_exp.sweep_type = "overlap"
dataset = my_exp.run( 500 )

save_data = True
save_name = f"Spectrum_{my_exp.sweep_type}"
folder_label = "Flux_dep_Qubit_0815_q3_11Gz" #your data and plots with be saved under a new folder with this name
save_dir = link_config["path"]["output_root"]

if save_data: 
    save_dir = create_folder(save_dir, folder_label)
    save_nc( save_dir, save_name, dataset)

# Plot
plot_and_save_flux_dep_Qubit(dataset, save_dir, save_data)