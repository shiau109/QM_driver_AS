# Dynamic config
from OnMachine.SetConfig.ConfigBuildUp_new import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from ab.QM_config_dynamic import initializer

spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, _ = spec.buildup_qmm()
init_macro = initializer(100000,mode='wait')


resonators = ["q1_ro"]
q_name = ["q1_xy"]
shot_num = 100000

import matplotlib.pyplot as plt
import time
from analysis.state_distribution import train_model, create_img
# start_time = time.time()

from exp.readout_fidelity import readout_fidelity
from qualang_tools.analysis import two_state_discriminator
import numpy as np
output_data = readout_fidelity( q_name, resonators, shot_num, config, qmm, init_macro)  
end_time = time.time()
# elapsed_time = np.round(end_time-start_time, 1)
for r in resonators:
    new_data = np.moveaxis(output_data[r]*1000,1,0)
    gmm_model = train_model(new_data)
    fig = plt.figure(constrained_layout=True)
    create_img(new_data, gmm_model)
    # fig.show()
    # plt.show()
    two_state_discriminator(output_data[r][0][0], output_data[r][1][0], output_data[r][0][1], output_data[r][1][1], True, True)
    # if save_data:
    #     figure = plt.gcf() # get current figure
    #     figure.set_size_inches(12, 10)
    #     plt.tight_layout()
    #     plt.pause(0.1)
    #     plt.savefig(f"{save_path}-{r}.png", dpi = 500)

plt.show()
save_data = True
if save_data:
    from exp.save_data import save_npz
    import sys
    save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
    save_npz(r"D:\Data\DR2_5Q", "ro_fidelity", output_data)   