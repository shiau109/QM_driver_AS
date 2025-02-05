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
from exp.cz_chavron import CZChavron
my_exp = CZChavron(config, qmm)
my_exp.ro_elements = ["q0_ro","q1_ro","q2_ro","q3_ro", "q4_ro"]
my_exp.flux_Qi = 3
my_expexcited_Qi = [2,3]
my_expflux_Ci = 7
my_exp.initializer =  initializer(100000,mode='wait')
my_exp.preprocess = "ave" # ave or shot
my_exp.mode = "coupler-qubit"

my_exp.time_max = 0.8 # us
my_exp.time_resolution = 0.008 # us
my_exp.z_amps_range = (-0.06,-0.02)
my_exp.z_amps_resolution = 0.001
my_exp.couplerz_amps_range = (0.28,0.32)
my_exp.couplerz_amps_resolution = 0.001

my_exp.time = 100 # ns
my_exp.z_amps = -0.13
my_exp.couplerz_amps = 0.2

dataset = my_exp.run(500)

from exp.cz_chavron import CZ,CZ_couplerz, CZ_ramsey
#dataset = CZ_ramsey(time_max,time_resolution,couplerz_amps_range,couplerz_amps_resolution,z_amps,ro_element,flux_Qi,excited_Qi,flux_Ci,preprocess,qmm,config,n_avg=n_avg,initializer=init_macro,simulate=False)
#dataset = CZ(time_max,time_resolution,z_amps_range,z_amps_resolution,ro_element,flux_Qi,excited_Qi,flux_Ci,coupler_z,preprocess,qmm,config,n_avg=n_avg,initializer=init_macro,simulate=False)
#dataset = CZ_couplerz(z_amps_range,z_amps_resolution,couplerz_amps_range,couplerz_amps_resolution,ro_element,flux_Qi,excited_Qi,flux_Ci,preprocess,qmm,config,n_avg=n_avg,initializer=init_macro,simulate=False)
folder_label = "CZ_chavron" #your data and plots will be saved under a new folder with this name
save_data = 1
if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    save_name = f"q{my_exp.excited_Qi[0]}q{my_exp.excited_Qi[1]}_cz_chavron"
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,save_name) 

# Plot
save_figure = 1
# import xarray as xr
# import matplotlib.pyplot as plt
# dataset = xr.open_dataset(r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240920_DRKe_5Q4C\save_data\CZ_sweet\crosstalk_not_compensated\20241004_055553_CZ\q1q0_cz_couplerz.nc")

import numpy as np
from exp.cz_chavron import plot_cz_chavron
for ro_name, data in dataset.data_vars.items():
    fig = plot_cz_chavron(dataset, ro_name,my_exp.mode)
    if save_figure: dp.save_fig(fig, f"{save_name}_{ro_name}")
plt.show()
