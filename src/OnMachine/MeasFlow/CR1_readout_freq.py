
from qm.qua import *
import matplotlib.pyplot as plt
import warnings
from exp.readout_optimization import *
warnings.filterwarnings("ignore")

from datetime import datetime
import sys


# Dynamic config
from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from ab.QM_config_dynamic import initializer

spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, _ = spec.buildup_qmm()
init_macro = initializer(100000,mode='wait')

# ro_elements = ['q0_ro','q1_ro','q2_ro']
ro_elements = ["q6_ro"]
operate_qubit = ['q6_xy']
n_avg = 500

freq_range = (-3, 3)
freq_resolution = 0.01
dataset = freq_dep_signal( freq_range, freq_resolution, operate_qubit, ro_elements, n_avg, config, qmm, initializer=init_macro, amp_mod=1.0)    # no progress (n/n_avg) showing
transposed_data = dataset.transpose("mixer", "state", "frequency")

dfs = transposed_data.coords["frequency"].values
for ro_name, data in transposed_data.data_vars.items():  
    fig = plt.figure()
    ax = fig.subplots(3,1)
    plot_freq_signal( dfs, data, ro_name, ax )
    fig.suptitle(f"{ro_name} RO freq")



#   Data Saving   # 

save_data = True
if save_data:
    from exp.save_data import save_nc, save_fig
    import sys
    save_dir = r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240510_DR4_5Q4C_0411#6\00 raw data"
    save_name = f"ro_freq_{operate_qubit[0]}"
    save_nc(save_dir, save_name, dataset)
    save_fig(save_dir, save_name)

plt.show()

