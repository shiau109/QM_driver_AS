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
q_name = ['q4_xy']
mode = "power" #"power", "time"

save_data = True
save_name = f"{q_name[0]}_{mode}_Rabi"

n_avg = 500
freq_range = (-50,50)
freq_resolution = 2
time_range = (16,400) # ns
time_resolution = 4

amps_range = (0, 1.9) # max can't >=2
amps_resolution = 0.01

from exp.config_par import *
from exp.rabi import xyfreq_time_rabi, plot_ana_freq_time_rabi, xyfreq_power_rabi


if mode == "power":
    dataset = xyfreq_power_rabi( freq_range, freq_resolution, amps_range, amps_resolution, q_name, ro_elements, config, qmm, initializer=init_macro, n_avg=n_avg, simulate=False)
    y = dataset.coords["amplitude"].values
elif mode == "time":
    dataset = xyfreq_time_rabi( freq_range, freq_resolution, time_range, time_resolution, q_name, ro_elements, config, qmm, n_avg=n_avg, initializer=init_macro)
    y = dataset.coords["time"].values




if save_data: save_nc(save_dir, save_name, dataset)


freqs = dataset.coords["frequency"].values
# Plot 
for ro_name, data in dataset.data_vars.items():
    xy_LO = dataset.attrs["ref_xy_LO"][0]/1e6
    xy_IF_idle = dataset.attrs["ref_xy_IF"][0]/1e6
    fig, ax = plt.subplots(2)
    plot_ana_freq_time_rabi( data, freqs, y, xy_LO, xy_IF_idle, ax )
    ax[0].set_title(ro_name)
    ax[1].set_title(ro_name)

if save_data: save_fig(save_dir, save_name)

plt.show()