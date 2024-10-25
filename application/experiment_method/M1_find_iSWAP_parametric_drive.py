import numpy as np
import matplotlib.pyplot as plt

# Dynamic config
# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()


from ab.QM_config_dynamic import initializer

init_macro = initializer(100000,mode='wait')
link_config = import_link(link_path)


ro_elements = ["q0_ro"]
excited_q = "q1_xy"
z_name = ["q0_z"]


n_avg = 100  # The number of averages


mid = 0.25   # Relative to offset
ra = 0.1
amps = np.arange(mid-ra, mid+ra, ra/200)  # Unit in volts, absolute
time = np.arange(16, 400, 4) # The flux pulse durations in clock cycles (4ns) - Must be larger than 4 clock cycles.
coupler_z = "q2_z"
coupler_amp = 0.0
cc = time/4

parametric_drive = 0
drive_z = "q1_z"

simulate = 0
if simulate:    init_macro = initializer(1000,mode='wait')

from exp.iSWAP_parametric_drive import exp_coarse_iSWAP, plot_ana_iSWAP_chavron
dataset = exp_coarse_iSWAP( parametric_drive, drive_z, coupler_z, coupler_amp, amps, cc, excited_q, ro_elements, z_name, config, qmm, n_avg=n_avg, simulate=simulate, initializer=init_macro )

# save_data = 0
# save_dir = link_config["path"]["output_root"]
# save_name = f"iSWAP"
# folder_label = "find_iSWAP_1"
# if save_data: 
#     save_dir = create_folder(save_dir, folder_label)
#     save_nc(save_dir, save_name, dataset)

# time = dataset.coords["time"].values*4
# amps = dataset.coords["amplitude"].values

#Save data
save_data = 1
folder_label = "M1_find_iSWAP_q0_cross_q1_excite_q1" #your data and plots will be saved under a new folder with this name
if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,folder_label)

for ro_name, data in dataset.data_vars.items():

    fig, ax = plt.subplots(2)
    plot_ana_iSWAP_chavron( data.values, amps, time, ax )
    ax[0].set_title(ro_name)
    ax[1].set_title(ro_name)

plt.show()



   

