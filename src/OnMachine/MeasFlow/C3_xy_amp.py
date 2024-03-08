


# Dynamic config
from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from ab.QM_config_dynamic import initializer

spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, _ = spec.buildup_qmm()
init_macro = initializer(100000,mode='wait')


n_avg = 400

ro_element = ["q3_ro"]
q_name =  "q3_xy"
sequence_repeat = 1
amp_modify_range = 0.4/float(sequence_repeat)
from exp.SQGate_calibration import *
drag_coef = 0.5
# output_data = DRAG_calibration_Yale( drag_coef, q_name, ro_element, config, qmm, n_avg=n_avg)
output_data = amp_calibration( amp_modify_range, q_name, ro_element, config, qmm, n_avg=n_avg, sequence_repeat=sequence_repeat, simulate=False, mode='live')

    #   Data Saving   # 
save_data = False
if save_data:
    from exp.save_data import save_npz
    import sys
    save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
    # save_npz(save_dir, save_progam_name, output_data)

# # Plot
plt.show()