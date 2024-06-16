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

from exp.detuned_rabi_flux_pulse import DetunedRabiFluxPulse
my_exp = DetunedRabiFluxPulse(config, qmm)
my_exp.initializer = initializer(200000,mode='wait')
my_exp.ro_elements = ["q0_ro", "q1_ro", "q2_ro", "q3_ro", "q4_ro"]
my_exp.xy_elements = ["q4_xy"]
my_exp.z_elements = ["q4_z"]
my_exp.freq_range = (-300, 50)
my_exp.freq_resolution = 4
my_exp.duration = 800
my_exp.pad_zeros = (80, 0) #ns
my_exp.time_resolution = 8 #ns
my_exp.amp_modify = 0.29 #x0.5 is voltage     0.44 0.36 0.29
 
dataset = my_exp.run(200)

save_data = True
save_dir = link_config["path"]["output_root"]
save_name = f"{my_exp.xy_elements[0]}_piscope_cc"


if save_data: save_nc(save_dir, save_name, dataset)

# Plot


import numpy as np
from scipy import signal, optimize

time = dataset.coords["pi_timing"].values
freq = dataset.coords["frequency"].values

for ro_name, data in dataset.data_vars.items():
    fig_0, ax_0 = plt.subplots()
    fig, ax = plt.subplots()
    ax.set_title('pcolormesh')
    ax.set_xlabel("T1 (us)")
    ax.set_ylabel("Flux")
    pcm = ax.pcolormesh( freq, time, data.values[0], cmap='RdBu')# , vmin=z_min, vmax=z_max)
    plt.colorbar(pcm, label='Value')

if save_data: save_fig(save_dir, save_name, dataset)

plt.show()