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

from visualization.find_ZZfree_plot import plot_ZZfree, plot_tau_X_flux, plot_pureZZ, plot_1D_ramsey, plot_fft, plot_crosstalk_X_frequency

import xarray as xr

# Set parameters
from exp.find_zzfree import ZZCouplerFreqRamsey, ZZCouplerFreqEcho
my_exp = ZZCouplerFreqEcho(config, qmm)
my_exp.ro_elements = ["q3_ro"]
my_exp.zz_detector_xy = ["q3_xy"]
my_exp.zz_source_xy = ["q4_xy"] # conditional x gate
my_exp.coupler_z = ["q8_z"]
my_exp.predict_detune = 0.1 #MHz
my_exp.flux_range = ( -1, 1 )
my_exp.resolution = 0.01


my_exp.initializer = initializer(200000,mode='wait')
dataset = my_exp.run( 100 )

#Save data
save_data = True
folder_label = f"find_ZZfree_{my_exp.zz_detector_xy[0][:2]}_{my_exp.zz_source_xy[0][:2]}"


if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,folder_label)

# Plot
save_figure = 1
# dataset = xr.open_dataset(r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240711_DR3_5Q4C_0430#7\good\20240713_1816_find_ZZfree_q1_q2.nc")
fig = plot_pureZZ(dataset)
if save_figure: dp.save_fig( fig, folder_label )
plt.show()

