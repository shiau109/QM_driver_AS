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
from exp.ramsey import Ramsey


#Set parameters
my_exp = Ramsey(config, qmm)
from ab.QM_config_dynamic import initializer
my_exp.initializer = initializer(300000,mode='wait')
my_exp.ro_element = ["q0_ro", "q1_ro", "q2_ro", "q3_ro", "q4_ro"]
my_exp.n_avg = 200
my_exp.virtual_detune = 1
my_exp.max_time = 10
my_exp.time_resolution = 0.1
dataset = my_exp.run(400)

from exp.save_data import save_nc, save_fig
save_data = True
save_dir = link_config["path"]["output_root"]
save_name = f"{my_exp.xy_elements[0]}_T2"
if save_data: save_nc(save_dir, save_name, dataset)

# Plot
time = (dataset.coords["time"].values)/1000
from qcat.visualization.qubit_relaxation import plot_qubit_relaxation
from qcat.analysis.qubit.relaxation import qubit_relaxation_fitting

for ro_name, data in dataset.data_vars.items():
    print(ro_name)
    fit_result = qubit_relaxation_fitting(time, data.values[0])
    print(fit_result.params)
    fig, ax = plt.subplots()
    plot_qubit_relaxation(time, data[0], ax, fit_result)
if save_data: save_fig(save_dir, save_name, dataset)

plt.show()

from exp.repetition_measurement import RepetitionMeasurement
re_exp = RepetitionMeasurement()
re_exp.exp_list = [my_exp]
re_exp.exp_name = ["T2"]
my_exp.shot_num = 400
dataset = re_exp.run(50)
save_name = f"{my_exp.xy_elements[0]}_EchoT2_stat"
if save_data: save_nc(save_dir, save_name, dataset["Ramsey"])

#To plot the result of multiple measurements (2D graph and histogram), use the following block of code
#================================================================================================#
import qcat.visualization.qubit_relaxation as qv
print(dir(qv))

from qcat.visualization.qubit_relaxation import plot_time_dep_qubit_T2_relaxation_2Dmap, plot_qubit_T2_relaxation_hist
from qcat.analysis.qubit.relaxation import qubit_relaxation_fitting


rep = dataset.coords["repetition"].values
dataset.data_vars.items()
single_name = "q0_ro"
for ro_name, data in [(single_name, dataset["q0_ro"])]:
    acc_T1 = []
    for i in range(rep.shape[-1]):
        fit_result = qubit_relaxation_fitting(time, data.values[0][i])
        acc_T1.append(fit_result.params["T1"].value)
    fig, ax = plt.subplots()
    plot_time_dep_qubit_T2_relaxation_2Dmap( rep, time, data.values[0], ax, fit_result=acc_T1)
    print(acc_T1)
    fig1, ax1 = plt.subplots()

    plot_qubit_T2_relaxation_hist( np.array(acc_T1), ax1 )