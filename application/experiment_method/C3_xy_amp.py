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

# Set parameters
init_macro = initializer(200000,mode='wait')

ro_elements = ["q0_ro", "q1_ro", "q2_ro", "q3_ro", "q4_ro"]
q_name =  "q4_xy"


save_data = True
save_dir = link_config["path"]["output_root"]
save_name = f"{q_name}_XYampCali"

n_avg = 500

sequence_repeat = 1
amp_modify_range = 0.4/float(sequence_repeat)
from exp.SQGate_calibration import *
drag_coef = 0.5
# output_data = DRAG_calibration_Yale( drag_coef, q_name, ro_element, config, qmm, n_avg=n_avg)
dataset = amp_calibration( amp_modify_range, q_name, ro_elements, config, qmm, n_avg=n_avg, sequence_repeat=sequence_repeat, simulate=False, mode='live')


#   Data Saving   # 
if save_data: save_nc(save_dir, save_name, dataset)

# Plot
amps = dataset.coords["amplitude_ratio"].values
for ro_name, data in dataset.data_vars.items():
    print(f"ploting {ro_name} with shape {data.shape}")
    fig, ax = plt.subplots()
    # x90data = dataset.sel(sequence='x90').data_vars["zdata"].values
    # x90data = dataset.sel(sequence='x90').data_vars["zdata"].values

    ax.plot(amps,data[0][0], label="x90")
    ax.plot(amps,data[0][1], label="x180")
    fig.legend()

if save_data: save_fig(save_dir, save_name)

plt.show()
