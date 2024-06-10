

# Dynamic config
from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from ab.QM_config_dynamic import initializer

spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, _ = spec.buildup_qmm()
init_macro = initializer(300000,mode='wait')


from exp.Ramsey_freq_calibration import *
n_avg = 100  # Number of averages


ro_element = ["q3_ro"]
q_name =  ["q3_xy"]
virtual_detune = 5 # Unit in MHz
output_data, evo_time = ramsey_freq_calibration( virtual_detune, q_name, ro_element, config, qmm, n_avg=n_avg, simulate=False, initializer=init_macro)


# for ro_element, data in output_data.items():
#     plot_ana_result(evo_time,data[0],virtual_detune)
plot_ana_result(evo_time,output_data[ro_element[0]][0],virtual_detune)

# #   Data Saving   # 

save_data = True
if save_data:
    from exp.save_data import save_npz, save_nc, save_fig
    import sys
    save_dir = r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240521_DR4_5Q4C_0430#7\00 raw data"
    save_name = f"{q_name[0]}_XYfreqCali"
    # save_nc(save_dir, save_name, output_data)
    # save_nc(save_dir, save_name+"_evo_line", evo_time)
    save_fig(save_dir, save_name)

plt.show()

