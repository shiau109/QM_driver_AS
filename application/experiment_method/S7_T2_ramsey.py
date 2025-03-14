# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer
from exp.ramsey import Ramsey

#Set parameters
my_exp = Ramsey(config, qmm)
from ab.QM_config_dynamic import initializer
my_exp.initializer = initializer(50000,mode='wait')
my_exp.ro_elements = ["q1_ro"]
my_exp.xy_elements = ["q1_xy"]
my_exp.virtual_detune = 0
my_exp.max_time = 50
my_exp.time_resolution = 0.5
dataarray = my_exp.run(400)

#Save data
save_data = 1
if save_data: 
    from exp.save_data import DataPackager
    folder_label = "ramseyT2_stat" #your data and plots will be saved under a new folder with this name
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataarray,"ramseyT2_stat")

save_plot = 1
if save_plot:
    from data_parser.qcat_temp import QMM_dataset
    from qcat.analysis.qubit.calibration_freq_ramsey import CalibrationRamsey
    figs = []
    for ro_name in dataarray.coords["q_idx"].values:
        data = dataarray.sel(q_idx=ro_name)
        data.attrs = dataarray.attrs
        data.name = ro_name
        # change format
        data = data.sel(mixer="I")
        # Analysis
        my_ana = CalibrationRamsey( data )
        my_ana._start_analysis()

        # Plot
        figs.append((data.name,my_ana.fig))
    dp.save_figs( figs )
