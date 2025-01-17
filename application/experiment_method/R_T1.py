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

from exp.relaxation_time import exp_relaxation_time


#Set parameters
my_exp = exp_relaxation_time(config, qmm)
my_exp.initializer = initializer(50000,mode='wait')
my_exp.ro_elements = ["q1_ro"]
my_exp.xy_elements = ["q1_xy"]
my_exp.max_time = 40
my_exp.time_resolution = 0.4
my_exp.shot_num = 400

#Repetition T1
from exp.repetition_measurement import RepetitionMeasurement
re_exp = RepetitionMeasurement()
re_exp.exp_list = [my_exp]
re_exp.exp_name = ["T1_relaxation"]

dataset = re_exp.run(100)
#Save data
save_data = 1
folder_label = "T1_rep" #your data and plots will be saved under a new folder with this name
if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset[re_exp.exp_name[0]],"T1_rep")

#To plot the result of multiple measurements (2D graph and histogram), use the following block of code
#================================================================================================#
from exp.plotting import PainterT1Repeat
painter = PainterT1Repeat()
dataset = dataset['T1_relaxation']
figs = painter.plot(dataset,folder_label)
if save_data: dp.save_figs( figs )
