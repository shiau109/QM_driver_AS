# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer
from exp.relaxation_time import exp_relaxation_time


#Set parameters
my_exp = exp_relaxation_time(config, qmm)
my_exp.initializer = initializer(2000000,mode='wait')
my_exp.ro_elements = ["q0_ro", "q1_ro", "q2_ro", "q3_ro"]
my_exp.xy_elements = ['q1_xy']
my_exp.max_time = 2000
my_exp.time_resolution = 20
dataset = my_exp.run(400)

#Save data
save_data = 1
folder_label = "T1" #your data and plots will be saved under a new folder with this name

if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,"T1")

# Plot
# from exp.plotting import PainterT1Single
# painter = PainterT1Single()
# figs = painter.plot(dataset,folder_label)
# if save_data: dp.save_figs( figs )
from qcat.analysis.qubit.relaxation import  RelaxationAnalysis
import matplotlib.pyplot as plt
figs = []
for ro_name, data in dataset.data_vars.items():
    data.attrs = dataset.attrs
    data.name = ro_name
    my_ana = RelaxationAnalysis(data.sel(mixer="I"))
    my_ana._start_analysis()
    figs.append((data.name,my_ana.fig))

dp.save_figs( figs )

