# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

import matplotlib.pyplot as plt

from exp.save_data import save_nc, save_fig

from visualization.find_ZZfree_plot import plot_ZZfree, plot_tau_X_flux, plot_pureZZ, plot_1D_ramsey, plot_fft, plot_crosstalk_X_frequency

import xarray as xr

# Set parameters
from exp.find_zzfree import ZZCouplerFreqRamsey, ZZCouplerFreqEcho
my_exp = ZZCouplerFreqEcho(config, qmm)
my_exp.ro_elements = ["q2_ro"]
my_exp.zz_detector_xy = ["q2_xy"]
my_exp.zz_source_xy = ["q1_xy"] # conditional x gate
my_exp.coupler_z = ["q6_z"]
my_exp.predict_detune = 0.1
my_exp.flux_range = ( -0.25, 0.25 )
my_exp.resolution = 0.001


my_exp.initializer = initializer(200000,mode='wait')
dataset = my_exp.run( 1000 )

save_data = True
file_name = f"find_ZZfree_{my_exp.zz_detector_xy[0][:2]}_{my_exp.zz_source_xy[0][:2]}"
save_dir = link_config["path"]["output_root"]

if save_data: save_nc( save_dir, file_name, dataset)

# Plot
# dataset = xr.open_dataset(r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240711_DR3_5Q4C_0430#7\good\20240713_1816_find_ZZfree_q1_q2.nc")
plot_pureZZ(dataset)
if save_data: save_fig( save_dir, file_name)
plt.show()