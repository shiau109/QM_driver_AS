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
from exp.plotting import plot_and_save_cryoscope_cc

# Set parameters

from exp.cryoscope import Cryoscope
my_exp = Cryoscope(config, qmm)
my_exp.initializer = initializer(200000,mode='wait')
my_exp.ro_elements = ["q0_ro", "q1_ro", "q2_ro", "q3_ro", "q4_ro"]
my_exp.xy_elements = ["q4_xy"]
my_exp.z_elements = ["q4_z"]
my_exp.time_range = ( 20, 800 )
my_exp.resolution = 4
my_exp.amp_modify = 0.44 #x0.5 is voltage     0.44 0.36 0.29
 
dataset = my_exp.run(4000)

save_data = True
save_dir = link_config["path"]["output_root"]
save_name = f"{my_exp.xy_elements[0]}_cryoscope_cc"
folder_label = "cryoscope_cc_1" #your data and plots with be saved under a new folder with this name

if save_data: 
    folder_save_dir = create_folder(save_dir, folder_label)
    save_nc(folder_save_dir, save_name, dataset)

# Plot
plot_and_save_cryoscope_cc(dataset, folder_save_dir, my_exp, save_data)