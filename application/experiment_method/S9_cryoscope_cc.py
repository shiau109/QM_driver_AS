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

from exp.cryoscope import Cryoscope
my_exp = Cryoscope(config, qmm)
my_exp.initializer = initializer(200000,mode='wait')
my_exp.ro_elements = ["q0_ro", "q1_ro", "q2_ro", "q3_ro", "q4_ro"]
my_exp.xy_elements = ["q4_xy"]
my_exp.z_elements = ["q4_z"]
my_exp.time_range = ( 20, 800 )
my_exp.resolution = 4
my_exp.amp_modify = 0.44 #x0.5 is voltage     0.44 0.36 0.29
 
dataset = my_exp.run(4000)

save_data = True
save_dir = link_config["path"]["output_root"]
save_name = f"{my_exp.xy_elements[0]}_cryoscope_cc"


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

    rx90_data = rx90_data-np.mean(rx90_data[my_exp.pad_zeros[0]:])
    ry90_data = ry90_data-np.mean(ry90_data[my_exp.pad_zeros[0]:])
    zdata = (rx90_data + 1j*ry90_data)
    virtual_detune = 200.
    mod_zdata = zdata*np.exp(1j*time*virtual_detune/1000*np.pi*2)
    phase_origin = np.unwrap(np.angle( zdata ))
    phase = np.unwrap(np.angle( mod_zdata ))
    phase = phase - phase[-1]
    # Filtering and derivative of the phase to get the averaged frequency
    detuning_origin = signal.savgol_filter(phase_origin / 2 / np.pi, 13, 3, deriv=1, delta=0.001)
    detuning = signal.savgol_filter(phase / 2 / np.pi, 13, 3, deriv=1, delta=0.001)
    # Flux line step response in freq domain and voltage domain

    ax[0].plot(time, zdata.real, label="x" )
    ax[0].plot(time, mod_zdata.real, label=f"x-{virtual_detune}" )
    ax[0].plot(time, zdata.imag, label="y" )
    ax[0].plot(time, mod_zdata.imag, label=f"y-{virtual_detune}" )

    ax[1].plot(time, phase_origin, label="0" )
    ax[1].plot(time, phase, label=f"{virtual_detune}")

    ax[2].plot(time, detuning_origin, label="0")
    ax[2].plot(time, detuning-virtual_detune, label=f"{virtual_detune}")

if save_data: save_fig(save_dir, save_name, dataset)

plt.show()