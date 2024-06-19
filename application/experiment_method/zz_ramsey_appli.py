# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer
init_macro = initializer(200000,mode='wait')

from exp.save_data import save_nc, save_fig

import matplotlib.pyplot as plt

# Set parameters
ro_elements = ["q1_ro"]
q_name = ['q1_xy']
con_xy_element = ["q2_xy"] # conditional x gate

n_avg = 1000
virtual_detune = 1
X = False # w/ or w/o conditional x gate

save_data = True
save_dir = link_config["path"]["output_root"]
save_name = f"{q_name[0]}_zz ramsey"

from exp.zz_ramsey import exp_zz_ramsey
dataset = exp_zz_ramsey(20,0.04,ro_elements,q_name,con_xy_element,n_avg,config,qmm,virtual_detune=virtual_detune,X=X,initializer=init_macro)

if save_data: save_nc(save_dir, save_name, dataset)