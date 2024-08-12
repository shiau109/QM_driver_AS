import numpy as np
import matplotlib.pyplot as plt

# Dynamic config
from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from ab.QM_config_dynamic import initializer
from exp.save_data import save_nc, save_fig, create_folder
spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, _ = spec.buildup_qmm()
init_macro = initializer(200000,mode='wait')
link_config = import_link(link_path)


ro_elements = ['q0_ro','q1_ro','q2_ro','q3_ro','q4_ro']
excited_q = 'q3_xy'
z_name = ['q3_z']


n_avg = 100  # The number of averages

# amps = np.arange(0.10, 0.14, 0.002)  # The relative flux amplitude absZvolt-offset
# time = np.arange(40, 8000, 200) # The flux pulse durations in clock cycles (4ns) - Must be larger than 4 clock cycles.

mid = 0.064
ra = 0.01
amps = np.arange(mid-ra, mid+ra, ra/25)  # The relative flux amplitude absZvolt-offset
time = np.arange(16, 2000, 4) # The flux pulse durations in clock cycles (4ns) - Must be larger than 4 clock cycles.
coupler_z = "q8_z"
coupler_amp = +0.037
cc = time/4

from exp.iSWAP_J import exp_coarse_iSWAP, plot_ana_iSWAP_chavron
dataset = exp_coarse_iSWAP( coupler_z, coupler_amp, amps, cc, excited_q, ro_elements, z_name, config, qmm, n_avg=n_avg, simulate=False, initializer=init_macro )

save_data = True
save_dir = link_config["path"]["output_root"]
save_name = f"iSWAP"
folder_label = "find_iSWAP_1"
if save_data: 
    save_dir = create_folder(save_dir, folder_label)
    save_nc(save_dir, save_name, dataset)

time = dataset.coords["time"].values*4
amps = dataset.coords["amplitude"].values
for ro_name, data in dataset.data_vars.items():

    fig, ax = plt.subplots(2)
    plot_ana_iSWAP_chavron( data.values, amps, time, ax )
    ax[0].set_title(ro_name)
    ax[1].set_title(ro_name)

plt.show()



   

