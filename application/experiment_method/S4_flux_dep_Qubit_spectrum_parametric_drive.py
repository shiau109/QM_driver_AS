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
from exp.plotting import plot_and_save_flux_dep_Qubit

# Start meausrement
from exp.xyfreq_sweep_flux_dep_parametric_drive import XYFreqFlux
my_exp = XYFreqFlux(config, qmm)
my_exp.ro_elements = ["q1_ro"]
my_exp.xy_elements = ["q1_xy"]
my_exp.z_elements = ["q1_z"]
my_exp.initializer = initializer(10000,mode='wait')
my_exp.xy_driving_time = 20
my_exp.xy_amp_mod = 0.1
# my_exp.z_amp_ratio_range = (-0.0127*5+1 -0.1, -0.0127*5+1 +0.1
my_exp.z_amp_ratio_range = (-3, +3)
my_exp.z_amp_ratio_resolution = 0.1
my_exp.freq_range = (-400,+ 40)
my_exp.freq_resolution = 4
my_exp.sweep_type = "z_pulse"

my_exp.parametric_drive = 0 # whether to apply parametric drive
my_exp.drive_element = "q1_z"

dataset = my_exp.run( 100 )

#Save data
save_data = 1
folder_label = "S4_flux_dep_Qubit_spectrum-q1" #your data and plots will be saved under a new folder with this name
if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,folder_label)

# Plot
save_figure = 1
from exp.plotting import PainterFluxDepQubit
painter = PainterFluxDepQubit()
figs = painter.plot(dataset,folder_label)
if save_figure: dp.save_figs( figs )