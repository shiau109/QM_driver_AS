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

# Set parameters
ro_elements = ["q6_ro"]
q_name = ['q6_xy']

n_avg = 1000
virtual_detune = 1

save_data = True
save_dir = link_config["path"]["output_root"]
save_name = f"{q_name[0]}_T2"

from exp.ramsey import exp_ramsey,plot_ramsey_oscillation
dataset = exp_ramsey( 20, 0.04, ro_elements, q_name, n_avg, config, qmm, virtual_detune=virtual_detune, initializer=init_macro)


if save_data: save_nc(save_dir, save_name, dataset)

# Plot
time = dataset.coords["time"].values
for ro_name, data in dataset.data_vars.items():
    fig, ax = plt.subplots(2)
    print(data.shape)
    # xy_LO = dataset.attrs["ref_xy_LO"][q_name[0]]/1e6
    # xy_IF_idle = dataset.attrs["ref_xy_IF"][q_name[0]]/1e6
    plot_ramsey_oscillation(time, data[0], ax[0])
    plot_ramsey_oscillation(time, data[1], ax[1])

if save_data: save_fig(save_dir, save_name, dataset)

plt.show()