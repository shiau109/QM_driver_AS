
from OnMachine.Octave_Config.QM_config_dynamic import Circuit_info, QM_config, initializer
from OnMachine.MeasFlow.ConfigBuildUp_old import spec_loca, config_loca, qubit_num


spec = Circuit_info(qubit_num)
d_config = QM_config()
spec.import_spec(spec_loca)
d_config.import_config(config_loca)
config = d_config.get_config()
qmm,_ = spec.buildup_qmm()
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
init_macro = initializer( 100*u.us,mode='wait')


from exp.Ramsey_freq_calibration import *
n_avg = 1000  # Number of averages


ro_element = ["q2_ro"]
q_name =  ["q2_xy"]
virtual_detune = 5 # Unit in MHz
output_data, evo_time = Ramsey_freq_calibration( virtual_detune, q_name, ro_element, config, qmm, n_avg=n_avg, simulate=False, initializer=init_macro)
#   Data Saving   # 
save_data = False
if save_data:
    from exp.save_data import save_npz
    import sys
    save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
    # save_npz(save_dir, save_progam_name, output_data)

plot_ana_result(evo_time,output_data[ro_element[0]][0],virtual_detune)
# # Plot
plt.show()
