# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

from exp.save_data import save_nc, save_fig, create_folder

import matplotlib.pyplot as plt

from exp.relaxation_time import exp_relaxation_time


#Set parameters
my_exp = exp_relaxation_time(config, qmm)
my_exp.initializer = initializer(20000,mode='wait')
my_exp.ro_elements = ["q1_ro","q3_ro"]
my_exp.xy_elements = ["q1_xy"]
my_exp.max_time = 6
my_exp.time_resolution = 0.06
dataset = my_exp.run(4000)


#saving the data
save_data = True
save_dir = link_config["path"]["output_root"]
save_name = "q1_xy_T1" #change the file name here
folder_label = "T1_stat_0815_q1" #your data and plots with be saved under a new folder with this name

if save_data: 
    folder_save_dir = create_folder(save_dir, folder_label)
    save_nc(save_dir, save_name, dataset)

time = (dataset.coords["time"].values)/1000

from qcat.visualization.qubit_relaxation import plot_qubit_relaxation
from qcat.analysis.qubit.relaxation import qubit_relaxation_fitting
from exp.plotting import plot_and_save_t1_singleRun, plot_and_save_t1_repeateRun

#plotting
plot_and_save_t1_singleRun(dataset, time, folder_save_dir, save_data)

from exp.repetition_measurement import RepetitionMeasurement
re_exp = RepetitionMeasurement()
re_exp.exp_list = [my_exp]
re_exp.exp_name = ["T1_relaxation"]
my_exp.shot_num = 400
dataset = re_exp.run(50)

save_name = "_T1_stat"
if save_data: 
    save_nc( save_dir, save_name, dataset["T1_relaxation"])

#To plot the result of multiple measurements (2D graph and histogram), use the following block of code
#================================================================================================#
print(dataset)

import qcat.visualization.qubit_relaxation as qv
print(dir(qv))
dataset.data_vars.items()
single_name = "q1_ro"

plot_and_save_t1_repeateRun(dataset, time, single_name, save_dir, save_data)