# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()


from exp.single_spin_echo import SpinEcho
# Set parameters
my_exp = SpinEcho( config, qmm )
from ab.QM_config_dynamic import initializer
my_exp.initializer = initializer(500000,mode='wait')
my_exp.ro_elements = ["q0_ro", "q1_ro", "q2_ro", "q3_ro", ]
my_exp.xy_elements = ['q0_xy']
my_exp.time_range = ( 40, 300000 )
my_exp.time_resolution = 3000
dataset = my_exp.run(400)

#Save data
save_data = 1
if save_data: 
    from exp.save_data import DataPackager
    folder_label = "SpinEchoT2_stat" #your data and plots will be saved under a new folder with this name
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,"SpinEchoT2_stat")

from qcat.analysis.qubit.relaxation import  RelaxationAnalysis
import matplotlib.pyplot as plt

for ro_name, data in dataset.data_vars.items():
    data.attrs = dataset.attrs
    data.name = ro_name
    my_ana = RelaxationAnalysis(data.sel(mixer="I"))
    my_ana._start_analysis()
    my_ana._plot_results()
    plt.show()




