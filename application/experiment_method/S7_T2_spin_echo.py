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
my_exp.ro_elements = ["q0_ro", "q1_ro"]
my_exp.xy_elements = ["q1_xy"]
my_exp.time_range = ( 40, 12000 )
my_exp.time_resolution = 60
dataset = my_exp.run(400)


from exp.save_data import save_nc, save_fig, create_folder    
from exp.plotting import plot_and_save_t2_spinEcho
save_data = True
save_dir = link_config["path"]["output_root"]
save_name = f"{my_exp.xy_elements[0]}_EchoT2"
folder_label = "T2_spin_echo_1" #your data and plots with be saved under a new folder with this name
if save_data: 
    folder_save_dir = create_folder(save_dir, folder_label)
    save_nc(folder_save_dir, save_name, dataset)

# Plot
import matplotlib.pyplot as plt

plot_and_save_t2_spinEcho(dataset, folder_save_dir, save_data = True )

from exp.repetition_measurement import RepetitionMeasurement
re_exp = RepetitionMeasurement()
re_exp.exp_list = [my_exp]
re_exp.exp_name = ["spin_echo"]
my_exp.shot_num = 400
dataset = re_exp.run(50)
save_name = f"{my_exp.xy_elements[0]}_EchoT2_stat"
if save_data: 
    save_nc( folder_save_dir, save_name, dataset["spin_echo"])

