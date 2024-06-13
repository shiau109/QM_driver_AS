

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
init_macro = initializer(200000,mode='wait')
ro_elements = ["q0_ro", "q1_ro", "q2_ro", "q3_ro", "q4_ro"]
operate_qubit = ['q4_xy']

save_data = True
save_dir = link_config["path"]["output_root"]
save_name = f"ro_amp_{operate_qubit[0]}"

n_avg = 500

freq_range = (-10, 10)
freq_resolution = 0.1

# Start measurement
from exp.readout_optimization import *
dataset = freq_dep_signal( freq_range, freq_resolution, operate_qubit, ro_elements, n_avg, config, qmm, initializer=init_macro, amp_mod=0.5)    # no progress (n/n_avg) showing

# Data Saving 
if save_data: save_nc(save_dir, save_name, dataset)

# Plot
transposed_data = dataset.transpose("mixer", "state", "frequency")
dfs = transposed_data.coords["frequency"].values
for ro_name, data in transposed_data.data_vars.items():  
    fig = plt.figure()
    ax = fig.subplots(3,1)
    plot_freq_signal( dfs, data, ro_name, ax )
    fig.suptitle(f"{ro_name} RO freq")
if save_data: save_fig(save_dir, save_name)

plt.show()

