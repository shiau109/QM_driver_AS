
# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

# from exp.save_data import save_nc, save_fig

import matplotlib.pyplot as plt

# Start measurement
from exp.ramsey_freq_calibration import RamseyFreqCalibration
my_exp = RamseyFreqCalibration(config, qmm)
my_exp.ro_elements = ["q2_ro"]
my_exp.xy_elements = ['q2_xy']
my_exp.virtial_detune_freq = 8

my_exp.point_per_period = 20
my_exp.max_period = 6
my_exp.initializer=initializer(50000,mode='wait')

dataset = my_exp.run( 400 )

from exp.ramsey_freq_calibration import plot_ana_result

# if save_data: save_nc( save_dir, save_name, dataset)

# for ro_element, data in output_data.items():
#     plot_ana_result(evo_time,data[0],virtual_detune)
plot_data = dataset["q2_ro"].values[0]
evo_time = dataset.coords["time"].values
plot_ana_result(evo_time,plot_data,my_exp.virtial_detune_freq)
    
# if save_data: save_fig(save_dir, save_name)
plt.show()

