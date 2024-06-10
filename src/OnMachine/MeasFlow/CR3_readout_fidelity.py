# Dynamic config
from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from ab.QM_config_dynamic import initializer

spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, _ = spec.buildup_qmm()
init_macro = initializer(300000,mode='wait')


# resonators = ["q0_ro","q1_ro","q2_ro"]
resonators =  ["q3_ro"]
q_name = ["q3_xy"]
shot_num = 20000

import matplotlib.pyplot as plt
from analysis.state_distribution import train_model, create_img
# start_time = time.time()

from exp.readout_fidelity import readout_fidelity
from qualang_tools.analysis import two_state_discriminator
import numpy as np
dataset = readout_fidelity( q_name, resonators, shot_num, config, qmm, init_macro)  

transposed_data = dataset.transpose("mixer", "state", "index")

for ro_name, data in transposed_data.data_vars.items(): # elapsed_time = np.round(end_time-start_time, 1)
    new_data = np.moveaxis(data.values*1000,1,0)
    gmm_model = train_model(new_data)
    fig = plt.figure(constrained_layout=True)
    create_img(new_data, gmm_model)
    # fig.show()
    # plt.show()
    two_state_discriminator(data[0][0], data[1][0], data[0][1], data[1][1], True, True)


#   Data Saving   # 
save_data = True
if save_data:
    from exp.save_data import save_nc, save_fig
    import sys
    save_dir = r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240521_DR4_5Q4C_0430#7\00 raw data"
    save_name = f"ro_fidelity_{q_name[0]}"
    save_nc(save_dir, save_name, dataset)
    save_fig(save_dir, save_name)

plt.show()

 