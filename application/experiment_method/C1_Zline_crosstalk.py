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


def update_flux_crosstalk(dataset, q_name, z_name, crosstalk_value):
    """
    更新或新增 flux crosstalk 數據，存入 Dataset。

    參數：
        dataset (xr.Dataset): 儲存 flux crosstalk 的 Dataset
        q_name (str): 受影響的 Qbit 名稱
        z_name (str): 施加 Z 控制的名稱
        crosstalk_value (float): Crosstalk 數值

    回傳：
        xr.Dataset: 更新後的 Dataset
    """
    if dataset is None:
        dataset = xr.Dataset(
            {"crosstalk": xr.DataArray(
                data=[[crosstalk_value]],
                coords={"Z": [z_name], "Q": [q_name]},
                dims=["Z", "Q"]
            )}
        )
    else:
        dataset = dataset.reindex({"Z": list(set(dataset.coords["Z"].values) | {z_name}),
                                   "Q": list(set(dataset.coords["Q"].values) | {q_name})},
                                  fill_value=float("nan"))
        dataset["crosstalk"].loc[dict(Z=z_name, Q=q_name)] = crosstalk_value
    
    return dataset


# Set parameters
from exp.zline_crosstalk import FluxCrosstalk
my_exp = FluxCrosstalk(config, qmm)
# my_exp.detector_qubit = "q7"
my_exp.detector_is_coupler = False
# my_exp.crosstalk_qubit = "q2"
my_exp.ro_elements = ["q1_ro"]

my_exp.expect_crosstalk = 0.2
my_exp.detector_bias = 0.1    #coupler:-0.05, qubit:-0.1
my_exp.detector_detune = -80  #q7:-77, q4:-68, q3:-110    #MHz
my_exp.z_modify_range = 0.2
my_exp.z_resolution = 0.008
my_exp.z_time = 0.1


my_exp.measure_method = "long_drive"   #long_drive, ramsey
my_exp.z_method = "pulse"     #offset, pulse

my_exp.initializer = initializer(200000,mode='wait')

datasets = []
crosstalk_dataset = None
# dataarray = xr.open_dataset(r"")
for detector_q in ["q1"]:
    for crosstalk_z in ["q3", "q4", "q0", "q2", "q5"]:
        my_exp.detector_qubit = detector_q
        my_exp.crosstalk_qubit = crosstalk_z
        dataset = my_exp.run( 500 )

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
        analysis_figures, crosstalk = plot_analysis(dataset)
        raw_figures = plot_crosstalk_3Dscalar(dataset)
        from exp.save_data import DataPackager

        dp.save_figs(raw_figures)
        dp.save_figs(analysis_figures)
        # plt.show()

        crosstalk_dataset = update_flux_crosstalk(crosstalk_dataset, my_exp.detector_qubit, my_exp.crosstalk_qubit, crosstalk)    
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
    dp.save_nc(crosstalk_dataset,"crosstalk")