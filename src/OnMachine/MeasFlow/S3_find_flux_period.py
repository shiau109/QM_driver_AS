

from qm.qua import *
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from exp.flux_dep_resonator import *

# 20231218 Test complete: Ratis
from OnMachine.Octave_Config.QM_config_dynamic import Circuit_info, QM_config, initializer
from OnMachine.BringUp.ConfigBuildUp import spec_loca, config_loca, qubit_num
spec = Circuit_info(qubit_num)
config = QM_config()
spec.import_spec(spec_loca)
config.import_config(config_loca)

qmm,_ = spec.buildup_qmm()
init_macro = initializer(spec.give_depletion_time_for("all"),mode='depletion')

ro_elements = ['q1_ro','q2_ro','q3_ro']

results, freq_axis, flux_axis = flux_dep_cavity(ro_elements, config.get_config(), qmm, initializer=init_macro)
for r in ro_elements:
    fig, ax = plt.subplots()
    plot_flux_dep_resonator(results[r], freq_axis, flux_axis, ax)
    ax.set_title(r)

plt.show()