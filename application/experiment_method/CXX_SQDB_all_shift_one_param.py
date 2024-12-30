# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

import numpy as np
from QM_driver_AS.ultitly.config_io import import_config, import_link

# Set shifting param
param_name = 'amp'
param_center = 0.06526*1.031+0.002
param_shift = 0.007
param_resolution = 0.001

# Set measuring param
from ab.QM_config_dynamic import initializer
initialize = initializer(150000,mode='wait')
target_q = 'q4'
ro_elements = ['q4_ro']
xy_elements = ["q4_xy"]
sequence_repeat = 800
gate_time = 40
threshold = -1.706e-03
shot_num = 1000

# SQDB function
from exp.SQDB_all import SQ_deterministic_benchmarking_all
def SQDB_func():    
    config = config_obj.get_config()
    qmm, _ = spec.buildup_qmm()
    my_exp = SQ_deterministic_benchmarking_all(config, qmm)
    my_exp.initializer = initialize
    my_exp.ro_elements = ro_elements
    my_exp.xy_elements = xy_elements

    my_exp.sequence_repeat = sequence_repeat     # are variables if process = 'repeat'
    my_exp.gate_time = gate_time
    my_exp.threshold = threshold
    dataset = my_exp.run( shot_num )
    return dataset

# Running 
from qspec.update import update_controlWaveform
from QM_driver_AS.ultitly.config_io import output_config
dataset_trace = []
shift_values = np.linspace(param_center-param_shift, param_center+param_shift, int(2*param_shift/param_resolution + 1))
for param in shift_values:
    link_config = import_link(link_path)
    config_obj, spec = import_config( link_path )
    spec.update_aXyInfo_for(target_q=target_q, 
                            amp=param, 
                            # ac=param,
                            # wf=param,
                            # len = param,
                            # draga=param,
                            )
    update_controlWaveform(config_obj, spec.get_spec_forConfig("xy"), target_q=target_q )
    output_config( link_path, config_obj, spec )
    print(f"{param_name} now is {param}")
    dataset = SQDB_func()
    dataset_trace.append(dataset)

# Data formation
import xarray as xr
condensed_dataset = xr.concat(dataset_trace, dim=param_name)
condensed_dataset.coords[param_name] = shift_values

#Save data
config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()
save_data = 1
folder_label = "SQDB_shift_one_param" #your data and plots will be saved under a new folder with this name
if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(condensed_dataset,folder_label)
    
# Tune back to the original value
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

spec.update_aXyInfo_for(target_q=target_q, 
                        amp=param_center, 
                        # ac=param,
                        # wf=param,
                        # len = param,
                        # draga=param,
                        )
update_controlWaveform(config_obj, spec.get_spec_forConfig("xy"), target_q=target_q )
output_config( link_path, config_obj, spec )
print(f"{param_name} now is back to {param_center}")
# Analyze

# Plot
# save_figure = 1
# from exp.plotting import PainterSQDBAll
# painter = PainterSQDBAll()
# figs = painter.plot(dataset,folder_label)
# if save_figure: dp.save_figs( figs )
