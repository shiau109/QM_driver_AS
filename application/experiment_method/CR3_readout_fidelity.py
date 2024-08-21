# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer
init_macro = initializer(400000,mode='wait')

from exp.save_data import save_nc, save_fig, create_folder
save_dir = link_config["path"]["output_root"]

import matplotlib.pyplot as plt

# Set parameters
ro_elements = ["q0_ro", "q1_ro", "q2_ro", "q3_ro", "q4_ro"]
q_elements = ['q4_xy']

save_data = True
save_name = f"ro_fidelity_{q_elements[0]}"
folder_label = "ro_fidelity_1"
shot_num = 10000


from exp.readout_fidelity import readout_fidelity

import numpy as np
dataset = readout_fidelity( q_elements, ro_elements, shot_num, config, qmm, init_macro)  


if save_data: 
    folder_save_dir = create_folder(save_dir, folder_label)
    save_nc(folder_save_dir, save_name, dataset)

from exp.plotting import plot_and_save_readout_fidelity
plot_and_save_readout_fidelity(dataset, folder_save_dir, save_data)



 