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

from exp.relaxation_time import exp_relaxation_time


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

time = (dataset.coords["time"].values)/1000

from qcat.visualization.qubit_relaxation import plot_qubit_relaxation
from qcat.analysis.qubit.relaxation import qubit_relaxation_fitting


for ro_name, data in dataset.data_vars.items():
    print(ro_name)
    fit_result = qubit_relaxation_fitting(time, data.values[0])
    print(fit_result.params)
    fig, ax = plt.subplots()
    plot_qubit_relaxation(time, data[0], ax, fit_result)
plt.show()

from exp.repetition_measurement import RepetitionMeasurement
re_exp = RepetitionMeasurement()
re_exp.exp_list = [my_exp]
re_exp.exp_name = ["T1_relaxation"]
my_exp.shot_num = 400
dataset = re_exp.run(50)
save_name = "_T1_stat"
if save_data: save_nc(save_dir, save_name, dataset["T1"])

#To plot the result of multiple measurements (2D graph and histogram), use the following block of code
#================================================================================================#
print(dataset)

import qcat.visualization.qubit_relaxation as qv
print(dir(qv))

from qcat.visualization.qubit_relaxation import plot_time_dep_qubit_T1_relaxation_2Dmap, plot_qubit_T1_relaxation_hist
from qcat.analysis.qubit.relaxation import qubit_relaxation_fitting
import numpy as np

rep = dataset.coords["repetition"].values
dataset.data_vars.items()
single_name = "q0_ro"
for ro_name, data in [(single_name, dataset["q0_ro"])]:
    acc_T1 = []
    for i in range(rep.shape[-1]):
        fit_result = qubit_relaxation_fitting(time, data.values[0][i])
        acc_T1.append(fit_result.params["T1"].value)
    fig, ax = plt.subplots()
    plot_time_dep_qubit_T1_relaxation_2Dmap( rep, time, data.values[0], ax, fit_result=acc_T1)
    print(acc_T1)
    fig1, ax1 = plt.subplots()

    plot_qubit_T1_relaxation_hist( np.array(acc_T1), ax1 )