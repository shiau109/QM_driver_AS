# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer
init_macro = initializer(200000,mode='wait')

from exp.save_data import save_nc, save_fig

import matplotlib.pyplot as plt
import numpy as np
# Set parameters
init_macro = initializer(300000,mode='wait')

ro_element = ["q0_ro","q1_ro"]
flux_Qi = 1
excited_Qi = [0,1]

n_avg = 200

time_max = 0.1 # us
time_resolution = 0.004 # us
amps_max = 0.3
amps_resolution = 0.003
save_data = True
save_dir = link_config["path"]["output_root"]
save_name = f"q{flux_Qi}_czchavron"

from exp.cz_chavron import CZ
dataset = CZ(time_max,time_resolution,amps_max,amps_resolution,ro_element,flux_Qi,excited_Qi,qmm,config,n_avg=n_avg,initializer=init_macro)

if save_data: save_nc(save_dir, save_name, dataset) 

# Plot
time = dataset.coords["time"].values
amps = dataset.coords["amplitude"].values

from exp.cz_chavron import plot_cz_chavron
for ro_name, data in dataset.data_vars.items():
    fig, ax = plt.subplots()
    plot_cz_chavron(time,amps,data.values[0],ax)

plt.show()