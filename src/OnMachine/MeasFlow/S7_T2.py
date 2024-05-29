
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


ro_elements = ["q6_ro"]
q_name = ['q6_xy']
n_avg = 1000
virtual_detune = 1

from exp.ramsey import exp_ramsey,plot_ramsey_oscillation
dataset = exp_ramsey( 20, 0.04, ro_elements, q_name, n_avg, config, qmm, virtual_detune=virtual_detune, initializer=init_macro)


# Plot
time = dataset.coords["time"].values
for ro_name, data in dataset.data_vars.items():
    fig, ax = plt.subplots(2)
    print(data.shape)
    # xy_LO = dataset.attrs["ref_xy_LO"][q_name[0]]/1e6
    # xy_IF_idle = dataset.attrs["ref_xy_IF"][q_name[0]]/1e6
    plot_ramsey_oscillation(time, data[0], ax[0])
    plot_ramsey_oscillation(time, data[1], ax[1])




save_data = True
if save_data:
    from exp.save_data import save_nc, save_fig
    save_dir = r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240521_DR4_5Q4C_0430#7\00 raw data"
    save_name = f"{q_name[0]}_T2"
    save_nc(save_dir, save_name, dataset)
    save_fig(save_dir, save_name)

plt.show()