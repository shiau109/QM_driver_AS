

# Dynamic config
from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from ab.QM_config_dynamic import initializer

spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, _ = spec.buildup_qmm()
init_macro = initializer(10000,mode='wait')


from exp.ramsey_freq_calibration import *
n_avg = 400  # Number of averages


ro_element = ["q0_ro","q1_ro","q2_ro"]
q_name =  ["q0_xy"]
virtual_detune = 5 # Unit in MHz
output_data, evo_time = ramsey_freq_calibration( virtual_detune, q_name, ro_element, config, qmm, n_avg=n_avg, simulate=False, initializer=init_macro)
#   Data Saving   # 
save_data = False
if save_data:
    from exp.save_data import save_nc
    import sys
    # save_nc(save_dir, save_progam_name, output_data)

# for ro_element, data in output_data.items():
#     plot_ana_result(evo_time,data[0],virtual_detune)
plot_ana_result(evo_time,output_data[ro_element[0]][0],virtual_detune)

# # Plot
plt.show()
