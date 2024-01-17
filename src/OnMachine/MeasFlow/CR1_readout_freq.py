
from qm.qua import *
import matplotlib.pyplot as plt
import warnings
from exp.readout_optimization import *
warnings.filterwarnings("ignore")

from datetime import datetime
import sys



from OnMachine.Octave_Config.QM_config_dynamic import Circuit_info, QM_config, initializer
from OnMachine.MeasFlow.ConfigBuildUp import spec_loca, config_loca, qubit_num
spec = Circuit_info(qubit_num)
config = QM_config()
spec.import_spec(spec_loca)
config.import_config(config_loca)

qmm,_ = spec.buildup_qmm()
init_macro = initializer( 100*u.us,mode='wait')

ro_elements = ['q2_ro']
operate_qubit = ['q2_xy']
n_avg = 500

dfs = np.arange(-1e6, 1e6, 0.05e6)
output_data = freq_dep_signal( dfs, operate_qubit, ro_elements, n_avg, config.get_config(), qmm, initializer=init_macro)
for r in ro_elements:
    fig = plt.figure()
    ax = fig.subplots(3,1)
    plot_freq_signal( dfs, output_data[r], r, ax )
    fig.suptitle(f"{r} RO freq")

plt.show()


amps = np.arange( 0.2, 1.5, 0.01)
output_data = power_dep_signal( amps, operate_qubit, ro_elements, n_avg, config.get_config(), qmm, initializer=init_macro)

for r in ro_elements:
    fig = plt.figure()
    ax = fig.subplots(1,2,sharex=True)
    plot_amp_signal( amps, output_data[r], r, ax[0] )
    plot_amp_signal_phase( amps, output_data[r], r, ax[1] )
    fig.suptitle(f"{r} RO amplitude")
plt.show()
    

#   Data Saving   # 
save_data = False
if save_data:
    from exp.save_data import save_npz
    import sys
    save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
    # save_npz(save_dir, save_progam_name, output_data)
