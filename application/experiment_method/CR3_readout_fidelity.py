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
my_exp.ro_elements = ["q2_ro"]
my_exp.xy_elements = ['q2_xy']

dataarray = my_exp.run(10000)


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
    dp.save_nc(dataarray,folder_label)

from qcat.visualization.readout_fidelity import plot_readout_fidelity
from qcat.analysis.state_discrimination.readout_fidelity import GMMROFidelity
for ro_name in dataarray.coords["q_idx"].values:
    datas = dataarray.sel(q_idx=ro_name).drop_vars("q_idx")
    my_ana = GMMROFidelity()
    my_ana._import_data(datas)
    print(my_ana.raw_data)
    my_ana._start_analysis()

    plot_readout_fidelity(datas, my_ana, my_ana.export_G1DROFidelity())



 
