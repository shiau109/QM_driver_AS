# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()


from exp.single_spin_echo import SpinEcho

# Set parameters
my_exp = SpinEcho( config, qmm )
from ab.QM_config_dynamic import initializer
my_exp.initializer = initializer(300000,mode='wait')
my_exp.ro_elements = ["q1_ro"]
my_exp.xy_elements = ["q1_xy"]
my_exp.time_range = ( 40, 10000 )
my_exp.time_resolution = 20
dataset = my_exp.run(1000)


from exp.save_data import save_nc, save_fig
save_data = True
save_dir = link_config["path"]["output_root"]
save_name = f"{my_exp.xy_elements[0]}_EchoT2"
if save_data: save_nc(save_dir, save_name, dataset)

# Plot
import matplotlib.pyplot as plt

from exp.ramsey import plot_ramsey_oscillation
time = dataset.coords["time"].values
for ro_name, data in dataset.data_vars.items():
    fig, ax = plt.subplots(2)
    # print(data.shape)
    plot_ramsey_oscillation(time, data[0], ax[0])
    plot_ramsey_oscillation(time, data[1], ax[1])
    # rep = dataset.coords["repetition"].values
    # plot_multiT2( data, rep, time )
if save_data: save_fig(save_dir, save_name, dataset)
plt.show()

from exp.repetition_measurement import RepetitionMeasurement
re_exp = RepetitionMeasurement()
re_exp.exp_list = [my_exp]
re_exp.exp_name = ["spin_echo"]
my_exp.shot_num = 400
dataset = re_exp.run(0)
save_name = f"{my_exp.xy_elements[0]}_EchoT2_stat"
if save_data: save_nc(save_dir, save_name, dataset["spin_echo"])

