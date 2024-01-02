
from qm.qua import *
from qm import SimulationConfig
import matplotlib.pyplot as plt
import warnings
from exp.readout_optimization import *
warnings.filterwarnings("ignore")

from datetime import datetime
import sys



from OnMachine.Octave_Config.QM_config_dynamic import Circuit_info, QM_config, initializer
from OnMachine.BringUp.ConfigBuildUp import spec_loca, config_loca, qubit_num
spec = Circuit_info(qubit_num)
config = QM_config()
spec.import_spec(spec_loca)
config.import_config(config_loca)

qmm,_ = spec.buildup_qmm()
init_macro = initializer(spec.give_depletion_time_for("all"),mode='depletion')

ro_elements = ['q1_ro','q2_ro','q3_ro','q4_ro']
operate_qubit = ['q1_xy']
n_avg = 200

dfs = np.arange(-1e6, 1e6, 0.02e6)
output_data = freq_dep_signal( dfs, operate_qubit, ro_elements, n_avg, config.get_config(), qmm)
for r in ro_elements:
    fig = plt.figure()
    ax = fig.subplots(3,1)
    plot_freq_signal( dfs, output_data[r], r, ax )
plt.show()
    

#   Data Saving   # 
save_data = False
if save_data:
    from exp.save_data import save_npz
    import sys
    save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
    # save_npz(save_dir, save_progam_name, output_data)
