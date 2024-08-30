# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

import matplotlib.pyplot as plt

from exp.relaxation_time import exp_relaxation_time


#Set parameters
my_exp = exp_relaxation_time(config, qmm)
my_exp.initializer = initializer(30000,mode='wait')
my_exp.ro_elements = ["q1_ro"]
my_exp.xy_elements = ["q1_xy"]
my_exp.max_time = 8
my_exp.time_resolution = 0.02
dataset = my_exp.run(2000)

save_data = 1
if save_data: 
    from exp.save_data import DataPackager
    folder_label = "T1_stat" #your data and plots will be saved under a new folder with this name
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,"T1_stat")

time = (dataset.coords["time"].values)/1000

from qcat.visualization.qubit_relaxation import plot_qubit_relaxation
from qcat.analysis.qubit.relaxation import qubit_relaxation_fitting
from exp.plotting import plot_and_save_t1_singleRun, plot_and_save_t1_repeateRun

#plotting
plot_and_save_t1_singleRun(dataset, time, save_dir, save_data)

from exp.repetition_measurement import RepetitionMeasurement
re_exp = RepetitionMeasurement()
re_exp.exp_list = [my_exp]
re_exp.exp_name = ["T1_relaxation"]
my_exp.shot_num = 2000

dataset = re_exp.run(2)

save_data = 1
if save_data: 
    from exp.save_data import DataPackager
    folder_label = "T1_rep" #your data and plots will be saved under a new folder with this name
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,"T1_rep")

#To plot the result of multiple measurements (2D graph and histogram), use the following block of code
#================================================================================================#
print(dataset)

import qcat.visualization.qubit_relaxation as qv
single_name = my_exp.ro_elements[0]


plot_and_save_t1_repeateRun(dataset["T1_relaxation"], time, single_name, save_dir, save_data)
