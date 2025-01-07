
# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

save_dir = link_config["path"]["output_root"]

import matplotlib.pyplot as plt




# Start measurement
from exp.readout_optimization import *
my_exp = ROAmp(config, qmm)
my_exp.ro_elements = ["q1_ro","q2_ro"]
my_exp.xy_elements = ['q1_xy','q2_xy']
my_exp.amp_mod_range = (0.1, 1.8)
my_exp.amp_resolution = 0.05
my_exp.initializer = initializer(100000,mode='wait')

dataset = my_exp.run(1000)

# Data Saving
save_data = True
folder_label = "ro_amp"
if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,folder_label)
    
save_figure = 1
from exp.plotting import PainterROPower
painter = PainterROPower()
figs = painter.plot(dataset,folder_label)
if save_figure: dp.save_figs( figs )

