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
n_avg = 100  # The number of averages
ro_elements = ["q0_ro", "q1_ro", "q2_ro", "q3_ro", "q4_ro"]

save_data = True
file_name = f"power_dep_resonator_{ro_elements[0]}"
save_dir = link_config["path"]["output_root"]

freq_range = (-15,15)
freq_resolution = 0.1
amp_max_ratio = 1.5
amp_resolution = 0.01
amp_scale = "lin"   # "lin", "log"

from exp.rofreq_sweep_power_dep import *
dataset = frequency_sweep_power_dep( ro_elements, config, qmm, n_avg=n_avg, freq_range=freq_range, freq_resolution=freq_resolution, amp_resolution=amp_resolution, amp_max_ratio=amp_max_ratio, amp_scale=amp_scale, initializer=init_macro)  



if save_data: save_nc( save_dir, file_name, dataset)


# Plot
dfs = dataset.coords["frequency"].values
amps = dataset.coords["amp_ratio"].values

for ro_name, data in dataset.data_vars.items():
    fig, ax = plt.subplots()
    plot_power_dep_resonator(dfs, amps, data.values, ax, amp_scale)
    ax.set_title(ro_name)
    ax.set_xlabel("additional IF freq (MHz)")
    ax.set_ylabel("amp scale")
if save_data: save_fig( save_dir, file_name)
    
plt.show()
