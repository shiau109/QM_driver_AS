# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

# from exp.save_data import save_nc, save_fig, create_folder
from exp.plotting import plot_and_save_piscope

# Set parameters

from exp.detuned_rabi_flux_pulse import DetunedRabiFluxPulse
my_exp = DetunedRabiFluxPulse(config, qmm)
my_exp.initializer = initializer(200000,mode='wait')
my_exp.ro_elements = ["q1_ro"]
my_exp.xy_elements = ["q1_xy"]
my_exp.z_elements = ["q1_z"]
my_exp.freq_range = (-120, 20)
my_exp.freq_resolution = 2
my_exp.duration = 1200
my_exp.pad_zeros = (0, 0) #ns
my_exp.time_resolution = 4 #ns
# my_exp.amp_modify = 0.29 #x0.5 is voltage     0.44 0.36 0.29
 
dataset = my_exp.run(20)


#Save data
save_data = 1
folder_label = "S9_piscope_q1_bias0V_drive0.13V_time1000ns_freq5MHz_phase30" #your data and plots will be saved under a new folder with this name

if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,folder_label)


# Plot
plot_and_save_piscope(dataset, save_dir, save_data)