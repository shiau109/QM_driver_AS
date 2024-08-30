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
from exp.plotting import plot_and_save_flux_period

# Set parameters
init_macro = initializer(10000,mode='wait')
ro_elements = ["q4_ro"]
z_elements = ['q4_z']

save_data = True
folder_label = "Find_Flux_Period__0815_q1" #your data and plots with be saved under a new folder with this name
save_dir = link_config["path"]["output_root"]
save_name = f"flux_resonator_{ro_elements[0]}_{z_elements[0]}"

n_avg = 100
freq_range = (-5,5)
freq_resolution = 0.05 #0.1
flux_range = (-0.3,0.3)
flux_resolution = 0.01 #0.01

from exp.rofreq_sweep_flux_dep import *
dataset = freq_sweep_flux_dep(ro_elements, z_elements, config, qmm, freq_range=freq_range, freq_resolution=freq_resolution, flux_settle_time=1, flux_range=flux_range, flux_resolution=flux_resolution, n_avg=n_avg, initializer=init_macro)
# dataset = freq_sweep_flux_dep_stable(ro_elements, z_elements, config, qmm, freq_range=freq_range, freq_resolution=freq_resolution, flux_settle_time=1, flux_range=flux_range, flux_resolution=flux_resolution, n_avg=n_avg, initializer=init_macro)

if save_data: 
    save_dir = create_folder(save_dir, folder_label)
    save_nc( save_dir, save_name, dataset)
    

# Plot
plot_and_save_flux_period(dataset, save_dir, save_data)
