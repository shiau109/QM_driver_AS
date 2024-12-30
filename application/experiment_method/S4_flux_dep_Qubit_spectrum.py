# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

# Start meausrement
from exp.xyfreq_sweep_flux_dep import XYFreqFlux
my_exp = XYFreqFlux(config, qmm)
my_exp.ro_elements = ["q4_ro"]
my_exp.xy_elements = ['q4_xy']
my_exp.z_elements = ['q4_z']
my_exp.initializer=initializer(1000,mode='wait')
my_exp.xy_driving_time = 0.04
my_exp.xy_amp_mod = 0.04
my_exp.z_amp_ratio_range = (-0.5,1.5)
my_exp.z_amp_ratio_resolution = 0.04
my_exp.freq_range = (-300,50)
my_exp.freq_resolution = 1
my_exp.sweep_type = "z_pulse"
dataset = my_exp.run( 200 )

#Save data
save_data = 1
folder_label = "S4_flux_dep_Qubit_spectrum" #your data and plots will be saved under a new folder with this name
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