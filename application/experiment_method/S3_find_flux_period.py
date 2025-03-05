# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from exp.rofreq_sweep_flux_dep import FluxDepCavity

from ab.QM_config_dynamic import initializer
import matplotlib.pyplot as plt
# Start meausrement
my_exp = FluxDepCavity(config, qmm)
my_exp.ro_elements = ["q0_ro","q1_ro"] #
my_exp.z_elements = ["q0_z"]
my_exp.initializer = initializer(50000,mode='wait')
my_exp.z_amp_ratio_range = (-2, 2)
my_exp.z_amp_ratio_resolution = 0.1
my_exp.freq_range = (-5,+ 5)
my_exp.freq_resolution = 0.5

dataarray = my_exp.run( 400 )

#Save data
save_data = 1
folder_label = "Find_Flux_Period" #your data and plots will be saved under a new folder with this name
if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataarray,folder_label)
    

# Plot
save_figure = 1
from exp.plotting import PainterFindFluxPeriod
painter = PainterFindFluxPeriod()
figs = painter.plot(dataarray,folder_label)
if save_figure: dp.save_figs( figs )
