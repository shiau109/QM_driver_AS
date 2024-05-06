
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

from exp.relaxation_time import exp_relaxation_time
import numpy as np

# Dynamic config
from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from ab.QM_config_dynamic import initializer

spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, _ = spec.buildup_qmm()
init_macro = initializer(200000,mode='wait')


ro_elements = ["q0_ro","q1_ro","q2_ro","q3_ro","q4_ro"]
q_name = ['q3_xy','q4_xy']
n_avg = 100
repeat = 1
max_time = 80 #us
time_resolution = 0.4 #us
from exp.relaxation_time import *

if repeat == 1:
    dataset = exp_relaxation_time( max_time, time_resolution, q_name, ro_elements, config, qmm, n_avg=n_avg, initializer=init_macro)
else:
    acc_T1, dataset = statistic_T1_exp( repeat, max_time, time_resolution, q_name, ro_elements, config, qmm, n_avg=n_avg, initializer=init_macro )

# Plot
time = dataset.coords["time"].values

if repeat == 1:
    from exp.relaxation_time import plot_T1
    for ro_name, data in dataset.data_vars.items():
        print(ro_name)
        fig, ax = plt.subplots(2)
        plot_T1(time, data)
else:
    from exp.relaxation_time import plot_multiT1, T1_hist
    rep = dataset.coords["repetition"].values

    for ro_name, data in dataset.data_vars.items():
        plot_multiT1( data, rep, time)
        print(acc_T1[ro_name].shape)
        T1_hist( acc_T1[ro_name] )
plt.show()



save_data = True
if save_data:
    from exp.save_data import save_nc
    import sys
    save_nc(r"D:\Data\03205Q4C_6", f"{q_name}_T1", dataset) 