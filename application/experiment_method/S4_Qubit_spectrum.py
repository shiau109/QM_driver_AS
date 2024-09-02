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

# Start meausrement
from exp.xyfreq_sweep import XYFreq
my_exp = XYFreq(config, qmm)
my_exp.ro_elements = ["q5_ro"]
my_exp.xy_elements = ['q5_xy']
my_exp.initializer=initializer(10000,mode='wait')
my_exp.xy_driving_time = 20
my_exp.xy_amp_mod = 0.2
my_exp.freq_range = (-400,400)
my_exp.freq_resolution = 4
my_exp.sweep_type = "overlap"
dataset = my_exp.run( 500 )

save_data = True
save_name = f"Spectrum_{my_exp.sweep_type}"
folder_label = "Flux_dep_Qubit_0821_q2" #your data and plots with be saved under a new folder with this name
save_dir = link_config["path"]["output_root"]

if save_data: 
    save_dir = create_folder(save_dir, folder_label)
    save_nc( save_dir, save_name, dataset)

# Plot
from exp.xyfreq_sweep import plot_ana_flux_dep_qubit_1D
ro_name = my_exp.ro_elements[0]
data = dataset[ro_name].values
print(data.shape)

dfs = dataset.coords["frequency"]
freq_LO = dataset.attrs["xy_LO"][0]
freq_IF = dataset.attrs["xy_IF"][0]

plot_ana_flux_dep_qubit_1D( data, dfs, freq_LO, freq_IF)   
plt.show()