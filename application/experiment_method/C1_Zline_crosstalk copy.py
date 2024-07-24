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
save_dir = link_config["path"]["output_root"]

import matplotlib.pyplot as plt

from visualization.zline_crosstalk_plot import plot_crosstalk_3Dscalar

import xarray as xr

# Set parameters
from exp.zline_crosstalk_copy import FluxCrosstalk
my_exp = FluxCrosstalk(config, qmm)
my_exp.detector_qubit = "q3"
my_exp.detector_is_coupler = "False"
my_exp.crosstalk_qubit = "q4"
my_exp.ro_elements = [f"{my_exp.detector_qubit}_ro"]

my_exp.expect_crosstalk = 0.04
my_exp.z_modify_range = 0.3
my_exp.z_resolution = 0.003
my_exp.z_time = 200

my_exp.measure_method = "long_drive"   #long_drive, ramsey
my_exp.z_method = "pulse"     #offset, pulse

my_exp.initializer = initializer(200000,mode='wait')
dataset = my_exp.run( 50 )
print(dataset)

save_data = True
file_name = f"detector_{my_exp.detector_qubit}_crosstalk_{my_exp.crosstalk_qubit}_{my_exp.measure_method}_{my_exp.z_method}_expectcrosstalk_{my_exp.expect_crosstalk}_{my_exp.z_time}mius"
if save_data: save_nc( save_dir, file_name, dataset)

# Plot
# dataset = xr.open_dataset(r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240719_DR3_5Q4C_0430#7\check\20240724_2212_detector_q3_crosstalk_q4_ramsey_pulse_expectcrosstalk_0.04_5mius.nc")
plot_crosstalk_3Dscalar(dataset)
if save_data: save_fig( save_dir, file_name)
plt.show()