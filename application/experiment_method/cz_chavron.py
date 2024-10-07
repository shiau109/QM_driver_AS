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

from exp.save_data import DataPackager

import matplotlib.pyplot as plt
import numpy as np
# Set parameters
init_macro = initializer(200000,mode='wait')

ro_element = ["q0_ro","q1_ro"]
flux_Qi = 1
excited_Qi = [1,0]
flux_Ci = 3
n_avg = 50
preprocess = "ave" # ave or shot

time_max = 0.4 # us
time_resolution = 0.004 # us
z_amps_range = (-0.2, 0.2)#(0.3, 0.6)
z_amps_resolution = 0.004
qubit_z = 0.056
coupler_z = 0.14
couplerz_amps_range =(-2, 0.5)#(-2, 0.5)#(0.1, 0.2)
couplerz_amps_resolution = 0.0025

save_data = True
save_dir = link_config["path"]["output_root"]
save_name = f"q{excited_Qi[0]}q{excited_Qi[1]}_cz_couplerz"

from exp.cz_chavron import CZ,CZ_couplerz, CZ_coupler_time
# dataset = CZ(time_max,time_resolution,z_amps_range,z_amps_resolution,ro_element,flux_Qi,excited_Qi,flux_Ci,coupler_z,preprocess,qmm,config,n_avg=n_avg,initializer=init_macro,simulate=False)
dataset = CZ_coupler_time(time_max,time_resolution,couplerz_amps_range,couplerz_amps_resolution,ro_element,flux_Qi,excited_Qi,flux_Ci,qubit_z,preprocess,qmm,config,n_avg=n_avg,initializer=init_macro,simulate=False)
# dataset = CZ_couplerz(z_amps_range,z_amps_resolution,couplerz_amps_range,couplerz_amps_resolution,ro_element,flux_Qi,excited_Qi,flux_Ci,preprocess,qmm,config,n_avg=n_avg,initializer=init_macro,simulate=False)
folder_label = "CZ" #your data and plots will be saved under a new folder with this name
save_data = 1
if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,save_name) 

# Plot
save_figure = 1

time = dataset.coords["time"].values
# coupler_flux = dataset.coords["c_amps"].values
flux = dataset.coords["amps"].values

from exp.cz_chavron import plot_cz_chavron,plot_cz_couplerz
for ro_name, data in dataset.data_vars.items():
    fig, ax = plt.subplots()
    plot_cz_chavron(time,flux,data.values[0],ax)
    # plot_cz_couplerz(flux,coupler_flux,data.values[0],ax)
    if save_figure: dp.save_fig(fig, f"{save_name}_{ro_name}")
plt.show()
