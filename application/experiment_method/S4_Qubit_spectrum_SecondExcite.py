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

# Start meausrement
from exp.xyfreq_sweep_SecondExcite import XYFreqSecondExcite
my_exp = XYFreqSecondExcite(config, qmm)
my_exp.ro_elements = ["q2_ro"]
my_exp.xy_elements = ['q2_xy']
my_exp.initializer=initializer(100000,mode='wait')
my_exp.xy_driving_time = 10
my_exp.xy_amp_mod = 0.03
my_exp.freq_range = (-215.7-1,-215.7+1)   # with respect to omega_01
my_exp.freq_resolution = 0.01
my_exp.sweep_type = "z_pulse"
dataset = my_exp.run( 500 )

#Save data
save_data = 1
folder_label = "Qubit_Spectrum" #your data and plots will be saved under a new folder with this name
if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,"Qubit_Spectrum")


# Plot
save_figure = 1
from exp.plotting import PainterQubitSpectrum
painter = PainterQubitSpectrum()
figs = painter.plot(dataset,folder_label)
if save_figure: dp.save_figs( figs )