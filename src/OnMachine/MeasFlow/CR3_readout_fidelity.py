
from OnMachine.Octave_Config.QM_config_dynamic import Circuit_info, QM_config, initializer
from OnMachine.MeasFlow.ConfigBuildUp import spec_loca, config_loca, qubit_num
spec = Circuit_info(qubit_num)
config = QM_config()
spec.import_spec(spec_loca)
config.import_config(config_loca)

qmm,_ = spec.buildup_qmm()
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
init_macro = initializer( 100*u.us,mode='wait')

resonators = ["q2_ro"]
q_name = ["q2_xy"]
shot_num = 10000

import matplotlib.pyplot as plt
import time
from analysis.state_distribution import train_model, create_img
# start_time = time.time()

from exp.readout_fidelity import readout_fidelity
from qualang_tools.analysis import two_state_discriminator
import numpy as np
output_data = readout_fidelity( q_name, resonators, shot_num, config.get_config(), qmm, init_macro)  
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