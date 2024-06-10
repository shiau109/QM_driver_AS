
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
save_dir = link_config["path"]["output_root"]

import matplotlib.pyplot as plt

# Set parameters
ro_elements = ["q0_ro", "q1_ro", "q2_ro", "q3_ro", "q4_ro"]
operate_qubit = ['q4_xy']

save_data = True
save_name = f"ro_amp_{operate_qubit[0]}"

n_avg = 400
amp_range = (0.1, 1.8)
amp_resolution = 0.01


# Start measurement
from exp.readout_optimization import *
dataset = power_dep_signal( amp_range, amp_resolution, operate_qubit, ro_elements, n_avg, config, qmm, initializer=init_macro)

# Data Saving 
if save_data: save_nc(save_dir, save_name, dataset)
    

transposed_data = dataset.transpose("mixer", "state", "amplitude_ratio")
amps = transposed_data.coords["amplitude_ratio"].values
for ro_name, data in transposed_data.data_vars.items():  
    fig = plt.figure()
    ax = fig.subplots(1,2,sharex=True)
    plot_amp_signal( amps, data, ro_name, ax[0] )
    plot_amp_signal_phase( amps, data, ro_name, ax[1] )
    fig.suptitle(f"{ro_name} RO amplitude")

if save_data: save_fig(save_dir, save_name)
plt.show()

