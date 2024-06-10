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
ro_elements = ["q0_ro", "q1_ro", "q2_ro", "q3_ro", "q4_ro"]
q_name = "q4_xy"
z_name = "q4_z"

n_avg = 1000
const_flux_len = 200 # unit ns <200
const_flux_amp = 0.18
pad_zeros = (20,0)
save_data = True
save_dir = link_config["path"]["output_root"]
save_name = f"{q_name}_cryoscope_bk"

from exp.cryoscope_bk import cryoscope_bk
dataset = cryoscope_bk( ro_elements, q_name, z_name, const_flux_amp, const_flux_len, n_avg, config, qmm, initializer=init_macro, pad_zeros=pad_zeros)

# "mixer", "r90", "time"

if save_data: save_nc(save_dir, save_name, dataset)

# Plot


import numpy as np
from scipy import signal, optimize

time = dataset.coords["time"].values
for ro_name, data in dataset.data_vars.items():
    fig, ax = plt.subplots(3)
    print(data.shape)
    # xy_LO = dataset.attrs["ref_xy_LO"][q_name[0]]/1e6
    rx90_data = data[0][0].values
    ry90_data = data[0][1].values

    rx90_data = rx90_data-np.mean(rx90_data)
    ry90_data = ry90_data-np.mean(rx90_data)

    phase = np.unwrap(np.angle(rx90_data + 1j*ry90_data))
    phase = phase - phase[-1]
    # Filtering and derivative of the phase to get the averaged frequency
    detuning = signal.savgol_filter(phase / 2 / np.pi, 13, 3, deriv=1, delta=0.001)
    # Flux line step response in freq domain and voltage domain
    step_response_freq = detuning / np.average(detuning[-int(const_flux_len / 2) :])

    ax[0].plot(time, data[0][0].values, label="x" )
    ax[0].plot(time, data[0][1].values, label="y" )
    ax[1].plot(time, phase)
    ax[2].plot(time, detuning)

if save_data: save_fig(save_dir, save_name, dataset)

plt.show()