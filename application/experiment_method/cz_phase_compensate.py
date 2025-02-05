# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer
#init_macro = initializer(200000,mode='wait')


import matplotlib.pyplot as plt
import numpy as np
# Set parameters
from exp.cz_phase_diff import CZCompensate
my_exp = CZCompensate(config,qmm)
my_exp.initializer = initializer(100000,mode='wait')

my_exp.ro_element=["q0_ro","q1_ro","q2_ro","q3_ro", "q4_ro"]
my_exp.flux_Qi = 3
my_exp.control_Qi = 2
my_exp.target_Qi = 3
my_exp.flux_Ci = 7 # coupler
my_exp.preprocess = "shot"
threshold_control = 3.275e-5
threshold_target = 1.619e-4#1.619e-4

my_exp.cz_time = 100#160 # ns

my_exp.cz_amps = -0.046
my_exp.c_amps = 0.30
my_exp.phase_resolution = 0.02

dataset = my_exp.run(2000)

folder_label = "CZ_compensate" #your data and plots will be saved under a new folder with this name
save_data = 1
if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    save_name = f"q{my_exp.control_Qi}q{my_exp.target_Qi}_cz_phase_compensate_shot"
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,save_name) 

from exp.cz_phase_diff import cz_phase_compensate_analysis
cz_phase_compensate_analysis(dataset, my_exp.preprocess,my_exp.target_Qi,threshold_target)
#plt.show()