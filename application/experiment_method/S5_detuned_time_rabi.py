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

# Set parameters
from exp.config_par import *
from exp.rabi import RabiTime
from exp.plotting import plot_and_save_rabi

my_exp = RabiTime(config, qmm)
my_exp.initializer = initializer(20000,mode='wait')

my_exp.ro_elements = ["q3_ro"]
my_exp.xy_elements = ['q3_xy']

my_exp.freq_range = (-20,20)
my_exp.freq_resolution = 2

my_exp.time_range = (16,160) # ns
my_exp.time_resolution = 4

my_exp.process = "time"

dataset = my_exp.run(20)

#Save data
save_data = 1
folder_label = "detuned_time_rabi" #your data and plots will be saved under a new folder with this name
if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,"detuned_time_rabi")


# Plot 
save_figure = 1
from exp.plotting import PainterRabi
painter = PainterRabi('time')
figs = painter.plot(dataset,folder_label)
if save_figure: dp.save_figs( figs )
