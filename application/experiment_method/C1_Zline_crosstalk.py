# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

from exp.save_data import save_nc, save_fig, create_folder
save_dir = link_config["path"]["output_root"]

import matplotlib.pyplot as plt

from visualization.zline_crosstalk_plot import plot_crosstalk_3Dscalar



import xarray as xr

# Set parameters
from exp.zline_crosstalk import FluxCrosstalk
my_exp = FluxCrosstalk(config, qmm)
my_exp.detector_qubit = "q8"
my_exp.detector_is_coupler = "True"
my_exp.crosstalk_qubit = "q3"
my_exp.ro_elements = [f"{my_exp.detector_qubit}_ro"]

my_exp.expect_crosstalk = 0.25
my_exp.z_modify_range = 0.4
my_exp.z_resolution = 0.008
my_exp.z_time = 20

my_exp.measure_method = "long_drive"   #long_drive, ramsey
my_exp.z_method = "pulse"     #offset, pulse

my_exp.initializer = initializer(200000,mode='wait')
dataset = my_exp.run( 500 )
print(dataset)

save_data = True
folder_label = "Zline_crosstalk_1" #your data and plots with be saved under a new folder with this name
file_name = f"detector_{my_exp.detector_qubit}_crosstalk_{my_exp.crosstalk_qubit}_{my_exp.measure_method}_{my_exp.z_method}_expectcrosstalk_{my_exp.expect_crosstalk}_{my_exp.z_time}mius"
if save_data: 
    folder_save_dir = create_folder(save_dir, folder_label)
    save_nc( folder_save_dir, file_name, dataset)

# Plot
# dataset = xr.open_dataset(r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240719_DR3_5Q4C_0430#7\check\20240724_2212_detector_q3_crosstalk_q4_ramsey_pulse_expectcrosstalk_0.04_5mius.nc")
figures = plot_crosstalk_3Dscalar(dataset)
# 保存每个图像并显示
for fig, ax, q in figures:
    if save_data:
        plt.figure(fig.number)  # 设置当前图形对象
        save_fig( folder_save_dir, f"{q}_{file_name}")
    # plt.show()  # 显示图像