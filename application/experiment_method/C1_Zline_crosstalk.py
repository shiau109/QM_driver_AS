# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

# from exp.save_data import save_fig, create_folder
save_dir = link_config["path"]["output_root"]

import matplotlib.pyplot as plt

from visualization.zline_crosstalk_plot import plot_crosstalk_3Dscalar, plot_analysis, plot_multi_crosstalk_3Dscalar, plot_multi_crosstalk_3Dscalar_with_fit



import xarray as xr

# Set parameters
from exp.zline_crosstalk import FluxCrosstalk
my_exp = FluxCrosstalk(config, qmm)
my_exp.detector_qubit = "q7"
my_exp.detector_is_coupler = False
my_exp.crosstalk_qubit = "q2"
my_exp.ro_elements = ["q7_ro", "q8_ro"]

my_exp.expect_crosstalk = 0.1
my_exp.detector_bias = 0    #coupler:-0.05, qubit:-0.1
my_exp.detector_detune = 0  #q7:-77, q4:-68, q3:-110    #MHz
my_exp.z_modify_range = 0.4
my_exp.z_resolution = 0.016
my_exp.z_time = 0.1


my_exp.measure_method = "long_drive"   #long_drive, ramsey
my_exp.z_method = "pulse"     #offset, pulse

my_exp.initializer = initializer(200000,mode='wait')

datasets = []
for crosstalk_qubit in ["q3", "q4", "q8"]:
    my_exp.crosstalk_qubit = crosstalk_qubit
    dataset = my_exp.run( 1000 )

    datasets.append(dataset)
    save_data = True
    folder_label = f"detector_{my_exp.detector_qubit}_bias{my_exp.detector_bias}V_crosstalk_{my_exp.crosstalk_qubit}_{my_exp.measure_method}_{my_exp.z_method}_expectcrosstalk_{my_exp.expect_crosstalk}_{my_exp.z_time}mius"
    if save_data: 
        from exp.save_data import DataPackager
        save_dir = link_config["path"]["output_root"]
        dp = DataPackager( save_dir, folder_label )
        dp.save_config(config)
        dp.save_nc(dataset,"data")

    # Plot
    analysis_figures = plot_analysis(dataset)
    raw_figures = plot_crosstalk_3Dscalar(dataset)
    from exp.save_data import DataPackager

    dp.save_figs(raw_figures)
    dp.save_figs(analysis_figures)
    # plt.show()

    # #Repetition

    # from exp.repetition_measurement import RepetitionMeasurement
    # re_exp = RepetitionMeasurement()
    # re_exp.exp_list = [my_exp]
    # re_exp.exp_name = ["FluxCrosstalk"]
    # my_exp.shot_num = 500

    # dataset = re_exp.run(100)

    # dataset = dataset['FluxCrosstalk']

    # #Save data
    # save_data = 1
    # if save_data: 
    #     from exp.save_data import DataPackager
    #     save_dir = link_config["path"]["output_root"]
    #     dp = DataPackager( save_dir, folder_label )
    #     dp.save_config(config)
    #     dp.save_nc(dataset,f"1x{re_exp.repetition}")

    # # To plot the result of multiple measurements (2D graph and histogram), use the following block of code
    # # ================================================================================================#
    # from exp.plotting import PainterFluxCrosstalkRepeat
    # painter = PainterFluxCrosstalkRepeat()
    # # import xarray as xr
    # # dataset = xr.open_dataset(r"C:\Users\admin\SynologyDrive\09 Data\Fridge Data\Qubit\20241111_DR4_5Q4C+AS1604\save_data\S6_T1rep\20241114_070103_T1_rep\time = 21672.980446100235.nc")
    # figs = painter.plot(dataset,f"Zline_crosstalk_1x{re_exp.repetition}", False)
    # if save_data: dp.save_figs( figs )
save_dir = link_config["path"]["output_root"]
dp = DataPackager( save_dir, f"detector_{my_exp.detector_qubit}_bias{my_exp.detector_bias}V_{my_exp.measure_method}_{my_exp.z_method}_expectcrosstalk_{my_exp.expect_crosstalk}_{my_exp.z_time}mius" )
figs = plot_multi_crosstalk_3Dscalar_with_fit(datasets)
dp.save_figs( figs )
