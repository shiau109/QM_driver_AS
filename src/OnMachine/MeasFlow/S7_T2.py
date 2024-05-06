
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

import numpy as np

# Dynamic config
from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from ab.QM_config_dynamic import initializer

spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, _ = spec.buildup_qmm()
init_macro = initializer(300000,mode='wait')


ro_elements = ["q0_ro","q1_ro","q2_ro","q3_ro","q4_ro"]
q_name = ['q4_xy']
n_avg = 200
virtual_detune = 5.

from exp.ramsey import exp_ramsey,plot_ramsey_oscillation
dataset = exp_ramsey( 20, 0.2, ro_elements, q_name, n_avg, config, qmm, virtual_detune=virtual_detune, initializer=init_macro)


# Plot
time = dataset.coords["time"].values
for ro_name, data in dataset.data_vars.items():
    fig, ax = plt.subplots(2)
    print(data.shape)
    # xy_LO = dataset.attrs["ref_xy_LO"][q_name[0]]/1e6
    # xy_IF_idle = dataset.attrs["ref_xy_IF"][q_name[0]]/1e6
    plot_ramsey_oscillation(time, data[0], ax[0])
    plot_ramsey_oscillation(time, data[1], ax[1])

plt.show()



save_data = False
if save_data:
    from exp.save_data import save_nc
    import sys
    save_nc(r"D:\Data\DR2_5Q", "Q1_idle_Rabi", dataset) 