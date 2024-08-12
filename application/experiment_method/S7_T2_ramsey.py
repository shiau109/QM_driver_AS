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
import numpy as np
import matplotlib.pyplot as plt
from exp.ramsey_class import exp_ramsey


#Set parameters
my_exp = exp_ramsey(config, qmm)
from ab.QM_config_dynamic import initializer
my_exp.initializer = initializer(300000,mode='wait')
my_exp.ro_element = ["q0_ro", "q1_ro", "q2_ro", "q3_ro", "q4_ro"]
my_exp.n_avg = 200
my_exp.virtual_detune = 1
my_exp.max_time = 10
my_exp.time_resolution = 0.1
dataset = my_exp.run(400)

from exp.save_data import save_nc, save_fig
from exp.plotting import plot_and_save_t2_ramsey_singleRun, plot_and_save_t2_ramsey_repeateRun
save_data = True
save_dir = link_config["path"]["output_root"]
folder_label = "T2_ramsey_1" #your data and plots with be saved under a new folder with this name
save_name = f"{my_exp.xy_elements[0]}_T2"
if save_data: 
    folder_save_dir = create_folder(save_dir, folder_label)
    save_nc( folder_save_dir, save_name, dataset)

# Plot
time = (dataset.coords["time"].values)/1000
plot_and_save_t2_ramsey_singleRun(dataset, time, folder_save_dir, save_data)


from exp.repetition_measurement import RepetitionMeasurement
re_exp = RepetitionMeasurement()
re_exp.exp_list = [my_exp]
re_exp.exp_name = ["T2"]
my_exp.shot_num = 400
dataset = re_exp.run(50)
save_name = f"{my_exp.xy_elements[0]}_ramseyT2_stat"
if save_data: save_nc( folder_save_dir, save_name, dataset["Ramsey"])

#To plot the result of multiple measurements (2D graph and histogram), use the following block of code
#================================================================================================#
import qcat.visualization.qubit_relaxation as qv
print(dir(qv))
dataset.data_vars.items()
single_name = "q0_ro"
plot_and_save_t2_ramsey_repeateRun(dataset, time, single_name, folder_save_dir, save_data)