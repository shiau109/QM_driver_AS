# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer
init_macro = initializer(100000,mode='wait')


import matplotlib.pyplot as plt

from exp.readout_fidelity import ROFidelity

my_exp = ROFidelity(config, qmm)
my_exp.initializer = initializer(200000,mode='wait')
my_exp.ro_elements = ["q0_ro","q1_ro"]
my_exp.xy_elements = ['q0_xy','q1_xy']

dataset = my_exp.run(1000)


save_data = True
save_dir = link_config["path"]["output_root"]
save_name = f"ro_amp_{my_exp.xy_elements[0]}"
folder_label = "readout_fidelity"
# Start measurement

# Data Saving 
if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,folder_label)

from exp.plotting import plot_and_save_readout_fidelity
figs = plot_and_save_readout_fidelity(dataset, folder_label, save_data)
dp.save_figs( figs )



 
