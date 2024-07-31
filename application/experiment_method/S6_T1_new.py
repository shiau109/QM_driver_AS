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

from exp.relaxation_time_class import exp_relaxation_time


#Set parameters
my_exp = exp_relaxation_time(config, qmm)
my_exp.initializer = initializer(300000,mode='wait')
my_exp.ro_element = ["q0_ro", "q1_ro", "q2_ro", "q3_ro", "q4_ro"]
my_exp.n_avg = 200
my_exp.max_time = 10
my_exp.time_resolution = 0.6
dataset = my_exp.run(400)


#saving the data
save_data = True
save_dir = link_config["path"]["output_root"]
save_name = "q4_xy_T1" #change the file name here
if save_data: save_nc(save_dir, save_name, dataset)
    

'''
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
        # print(acc_T1[ro_name].shape)
        # T1_hist( acc_T1[ro_name] )

if save_data: save_fig(save_dir, save_name)

plt.show()
'''

from exp.repetition_measurement import RepetitionMeasurement
re_exp = RepetitionMeasurement()
re_exp.exp_list = [my_exp]
re_exp.exp_name = ["T1_relaxation"]
my_exp.shot_num = 400
dataset = re_exp.run(50)
save_name = "_T1_stat"
if save_data: save_nc(save_dir, save_name, dataset["T1"])