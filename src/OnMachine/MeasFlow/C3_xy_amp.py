


# Scan the DRAG coefficient pre-factor

# drag_coef = drag_coef_q1
# Check that the DRAG coefficient is not 0
# assert drag_coef != 0, "The DRAG coefficient 'drag_coef' must be different from 0 in the config."
from OnMachine.Octave_Config.QM_config_dynamic import Circuit_info, QM_config, initializer
from OnMachine.MeasFlow.ConfigBuildUp import spec_loca, config_loca, qubit_num
spec = Circuit_info(qubit_num)
config = QM_config()
spec.import_spec(spec_loca)
config.import_config(config_loca)

qmm,_ = spec.buildup_qmm()
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
init_macro = initializer( 100*u.us,mode='wait')    
n_avg = 400

ro_element = ["q2_ro"]
q_name =  "q2_xy"
sequence_repeat = 1
amp_modify_range = 0.25/float(sequence_repeat)
from exp.SQGate_calibration import *
# output_data = DRAG_calibration_Yale( drag_coef, q_name, ro_element, config, qmm, n_avg=n_avg)
output_data =  amp_calibration( amp_modify_range, q_name, ro_element, config.get_config(), qmm, n_avg=n_avg, sequence_repeat=sequence_repeat, simulate=False, mode='live')

    #   Data Saving   # 
save_data = False
if save_data:
    from exp.save_data import save_npz
    import sys
    save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
    # save_npz(save_dir, save_progam_name, output_data)

# # Plot
plt.show()