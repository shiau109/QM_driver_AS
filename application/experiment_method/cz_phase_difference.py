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
init_macro = initializer(100000,mode='wait')

ro_element=["q0_ro", "q1_ro"]
flux_Qi = 1
control_Qi = 1
target_Qi = 0
flux_Ci = 3 # coupler
preprocess = "shot"

n_avg = 1000
cz_amps_range = (0.3, 0.6)#(-0.325,-0.275)
cz_amps_resolution = 0.006
cz_amps = 0.4014#-0.302
cz_time_max = 400
cz_time_resolution = 4
cz_time = 100#160 # ns
couplerz_amps_range = (0.1, 0.2)#(-0.22, -0.12)
couplerz_amps_resolution = 0.002
c_amps = 0.1539#-0.202

save_data = True
save_dir = link_config["path"]["output_root"]
save_name = f"q{control_Qi}q{target_Qi}_cz_phasediff_shot"

from exp.cz_phase_diff import CZ_phase_diff, CZ_phase_compensate,CZ_phase_diff_time, CZ_fidelity
dataset = CZ_phase_diff(cz_amps_range,cz_amps_resolution,cz_time,couplerz_amps_range,couplerz_amps_resolution,ro_element,flux_Qi,control_Qi,target_Qi,flux_Ci,preprocess,qmm,config,n_avg=n_avg,initializer=init_macro,simulate=False)
#dataset = CZ_phase_diff_time(cz_amps_range,cz_amps_resolution,cz_time_max,cz_time_resolution,c_amps,ro_element,flux_Qi,control_Qi,target_Qi,flux_Ci,qmm,config,n_avg=n_avg,initializer=init_macro,simulate=False)
# dataset = CZ_phase_compensate(c_amps,cz_amps,cz_time,ro_element,flux_Qi,target_Qi,flux_Ci,preprocess,qmm,config,n_avg=n_avg,initializer=init_macro,simulate=False)
# dataset = CZ_fidelity(2.7109001422032852, -2.2768161756327716, c_amps,cz_amps,cz_time,ro_element,flux_Qi, control_Qi,target_Qi,flux_Ci,preprocess,qmm,config,n_avg=n_avg,initializer=init_macro,simulate=False)

folder_label = "CZ_diff" #your data and plots will be saved under a new folder with this name
if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,save_name) 