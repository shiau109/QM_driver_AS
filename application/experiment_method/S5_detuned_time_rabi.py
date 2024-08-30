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

my_exp.ro_elements = ["q1_ro","q3_ro"]
my_exp.xy_elements = ['q1_xy']

my_exp.freq_range = (-40,40)
my_exp.freq_resolution = 2

my_exp.time_range = (16,400) # ns
my_exp.time_resolution = 4

my_exp.process = "time"

dataset = my_exp.run(1000)

save_data = 1
if save_data: 
    from exp.save_data import DataPackager
    folder_label = "detuned_time_rabi" #your data and plots will be saved under a new folder with this name
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,"detuned_time_rabi")

y = dataset.coords["time"].values
freqs = dataset.coords["frequency"].values

# Plot 
plot_and_save_rabi(dataset, freqs, y, save_dir, "time", save_data)