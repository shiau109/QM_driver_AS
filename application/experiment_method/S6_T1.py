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


ro_elements = ["q4_ro"]
q_name = ["q4_xy"]

save_data = True
save_name = f"{q_name[0]}_T1"

n_avg = 1000
repeat = 1
max_time = 50 #us
time_resolution = 0.1 #us

# Start measurement
from exp.relaxation_time import *
if repeat == 1:
    dataset = exp_relaxation_time( max_time, time_resolution, q_name, ro_elements, config, qmm, n_avg=n_avg, initializer=init_macro)
else:
    acc_T1, dataset = statistic_T1_exp( repeat, max_time, time_resolution, q_name, ro_elements, config, qmm, n_avg=n_avg, initializer=init_macro )







if save_data: save_nc(save_dir, save_name, dataset)
    

import matplotlib.pyplot as plt
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

if save_data: save_fig(save_dir, save_name)

plt.show()
