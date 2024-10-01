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
from qm.qua import *

# Set parameters
ro_element = ["q2_ro","q3_ro","q4_ro"]
q_name = ["q2_xy","q3_xy","q4_xy"]
n_avg = 1000
threshold = 5.36e-5

def prepare_state():

    play("x180", "q4_xy" )

    pass

from exp.tomography import StateTomography
my_exp = StateTomography(config, qmm)
my_exp.ro_elements = ["q4_ro"]
my_exp.xy_elements = ["q4_xy"]
my_exp.process = prepare_state
dataset = my_exp.run(1000)

save_data = True
save_dir = link_config["path"]["output_root"]
save_name = f"{ro_element[0]}{ro_element[1]}_state_tomography"

#from exp.tomography import *
#dataset = state_tomography_NQ(q_name,ro_element,prepare_state,n_avg,config,qmm,simulate=False)
if save_data: save_nc(save_dir, save_name, dataset) 

data_i = dataset[ro_element[2]].values[0]#.transpose()
print(data_i.shape)
#vect_dis = calculate_block_vector(data_i, threshold)