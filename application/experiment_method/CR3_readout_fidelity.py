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

from exp.save_data import save_nc, save_fig
save_dir = link_config["path"]["output_root"]

import matplotlib.pyplot as plt

# Set parameters
ro_elements = ["q0_ro", "q1_ro", "q2_ro", "q3_ro", "q4_ro"]
q_elements = ['q4_xy']

save_data = True
save_name = f"ro_fidelity_{q_elements[0]}"

shot_num = 10000


from exp.readout_fidelity import readout_fidelity

import numpy as np
dataset = readout_fidelity( q_elements, ro_elements, shot_num, config, qmm, init_macro)  


if save_data: save_nc(save_dir, save_name, dataset)


from analysis.state_distribution import train_model, create_img
from qualang_tools.analysis import two_state_discriminator
transposed_data = dataset.transpose("mixer", "state", "index")

for ro_name, data in transposed_data.data_vars.items(): # elapsed_time = np.round(end_time-start_time, 1)
    new_data = np.moveaxis(data.values*1000,1,0)
    gmm_model = train_model(new_data)
    fig = plt.figure(constrained_layout=True)
    create_img(new_data, gmm_model)
    two_state_discriminator(data[0][0], data[1][0], data[0][1], data[1][1], True, True)


if save_data: save_fig(save_dir, save_name)

plt.show()

 