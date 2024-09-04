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
my_exp.initializer = initializer(300000,mode='wait')
my_exp.ro_elements = ["q1_ro"]
my_exp.xy_elements = ["q1_xy"]
my_exp.time_range = ( 40, 1000 )
my_exp.time_resolution = 20
dataset = my_exp.run(10)


#Save data
save_data = 1
if save_data: 
    from exp.save_data import DataPackager
    folder_label = "SpinEchoT2_stat" #your data and plots will be saved under a new folder with this name
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,"SpinEchoT2_stat")

# Plot
from exp.plotting import PainterT2SpinEcho
painter = PainterT2SpinEcho()
figs = painter.plot(dataset,folder_label)
if save_data: dp.save_figs( figs )
# Plot


# plot_and_save_t2_spinEcho(dataset, folder_save_dir, save_data = True )

from exp.repetition_measurement import RepetitionMeasurement
re_exp = RepetitionMeasurement()
re_exp.exp_list = [my_exp]
re_exp.exp_name = ["spin_echo"]
my_exp.shot_num = 40
dataset = re_exp.run(2)

save_data = 1
if save_data: 
    from exp.save_data import DataPackager
    folder_label = "SpinEchoT2_rep" #your data and plots will be saved under a new folder with this name
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,"SpinEchoT2_rep")

#To plot the result of multiple measurements (2D graph and histogram), use the following block of code
#================================================================================================#
from exp.plotting import PainterT2Repeat
painter = PainterT2Repeat()
figs = painter.plot(dataset,folder_label)
if save_data: dp.save_figs( figs )
