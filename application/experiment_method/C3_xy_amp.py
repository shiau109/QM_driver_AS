# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

from exp.xy_amp_calibration import XYAmpCalibraion
#Set parameters
my_exp = XYAmpCalibraion(config, qmm)
from ab.QM_config_dynamic import initializer
my_exp.initializer = initializer(100000,mode='wait')
my_exp.ro_elements = ["q1_ro"]
my_exp.xy_elements = ["q1_xy"]
my_exp.sequence_repeat = 30
dataset = my_exp.run(400)
# import xarray as xr
# dataset = xr.open_dataset(r"d:\Data\Qubit\5Q4C0430\20241121_DR3_5Q4C_0430#7_q2q3\20250111_194355_xy_amp\xy_amp.nc")



save_dir = link_config["path"]["output_root"]
save_name = f"{my_exp.xy_elements[0]}_XYampCali"
folder_label = "xy_amp_1"
#Save data
from exp.save_data import DataPackager
save_dir = link_config["path"]["output_root"]
dp = DataPackager( save_dir, folder_label )
save_data = 1
folder_label = "xy_amp" #your data and plots will be saved under a new folder with this name
if save_data: 
    dp.save_config(config)
    dp.save_nc(dataset,folder_label)

# Plot
save_plot = 1
if save_plot:
    from data_parser.qcat_temp import QMM_dataset
    from qcat.analysis.qubit.calibration_xyamp import CalibrationXYAmp
    figs = []
    for sq_data in QMM_dataset(dataset):

        # change format
        sq_data = sq_data.sel(mixer="I").rename({"amplitude_ratio": "amplitude"})
        # Analysis
        my_ana = CalibrationXYAmp( sq_data )
        my_ana._start_analysis()

        # Plot
        figs.append((sq_data.name,my_ana.fig))
    dp.save_figs( figs )