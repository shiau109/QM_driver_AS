# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

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

#Save data
save_data = 1
folder_label = "Flux_dep_Qubit" #your data and plots will be saved under a new folder with this name
if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,"Flux_dep_Qubit")

# Plot
from exp.xyfreq_sweep import plot_ana_flux_dep_qubit_1D
ro_name = my_exp.ro_elements[0]
data = dataset[ro_name].values
print(data.shape)

# dfs = dataset.coords["frequency"]
# freq_LO = dataset.attrs["xy_LO"][0]
# freq_IF = dataset.attrs["xy_IF"][0]

# plot_ana_flux_dep_qubit_1D( data, dfs, freq_LO, freq_IF)   
# plt.show()