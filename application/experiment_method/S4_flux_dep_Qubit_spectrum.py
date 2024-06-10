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
z_name = ['q4_z']

sweep_type = "z_pulse"      # "z_pulse", "const_z", "two_tone"

saturation_len = 20  # In us (should be < FFT of df)
saturation_ampRatio = 0.5 # pre-factor to the value defined in the config - restricted to [-2; 2)
n_avg = 500

flux_range = (-0.05,0.05)
flux_resolution = 0.005

freq_range = (-300,50)
freq_resolution = 2

save_data = True
save_name = f"Spectrum_{q_name[0]}_{z_name[0]}_{sweep_type}"
save_dir = link_config["path"]["output_root"]
# Start meausrement
from exp.xyfreq_sweep_flux_dep import *
dataset = xyfreq_sweep_flux_dep( flux_range, flux_resolution, freq_range, freq_resolution, q_name, ro_elements, z_name, config, qmm, saturation_ampRatio=saturation_ampRatio, saturation_len=saturation_len, n_avg=n_avg, sweep_type=sweep_type, simulate=False)



if save_data: save_nc( save_dir, save_name, dataset)

# Plot
freqs = dataset.coords["frequency"].values
flux = dataset.coords["flux"].values
for i, (ro_name, data) in enumerate(dataset.data_vars.items()):
    xy_LO = dataset.attrs["xy_LO"][0]/1e6
    xy_IF_idle = dataset.attrs["xy_IF"][0]/1e6
    z_offset = dataset.attrs["z_offset"][0]
    print(ro_name, xy_LO, xy_IF_idle, z_offset, data.shape)
    fig, ax = plt.subplots(2)

    plot_ana_flux_dep_qubit(data, flux, freqs, xy_LO, xy_IF_idle, z_offset, ax)
    # plot_ana_flux_dep_qubit_1D(data, flux, freqs, xy_LO, xy_IF_idle, z_offset, ax) 


    ax[0].set_title(ro_name)
    ax[1].set_title(ro_name)

if save_data: save_fig(save_dir, save_name)

plt.show()