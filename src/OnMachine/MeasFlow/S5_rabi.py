
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

from datetime import datetime
import sys

from exp.rabi_J import freq_time_rabi, plot_ana_freq_time_rabi, freq_power_rabi
import numpy as np

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

ro_elements = ['q1_ro','q2_ro','q3_ro','q4_ro']
q_name = ['q1_xy']
n_avg = 100

dfs = np.arange(-100e6, 100e6, 1e6)
time = np.arange(16, 400, 8) # ns
cc = time/4
amps = np.arange(0, 1.5, 0.01)

from exp.config_par import *

output_data = freq_time_rabi( dfs, cc, q_name, ro_elements, config.get_config(), qmm, n_avg=n_avg)
for r in ro_elements:
    xy_LO = get_LO(q_name[0],config.get_config())
    xy_IF_idle = get_IF(q_name[0],config.get_config())
    fig, ax = plt.subplots(2)
    plot_ana_freq_time_rabi( output_data[r], dfs, time, xy_LO, xy_IF_idle, ax )
    ax[0].set_title(r)
    ax[1].set_title(r)
plt.show()


# output_data = freq_power_rabi( dfs, amps, q_name, ro_elements, config.get_config(), qmm, initializer=init_macro, n_avg=n_avg, simulate=False)

# for r in ro_elements:
#     xy_LO = get_LO(q_name[0],config.get_config())
#     xy_IF_idle = get_IF(q_name[0],config.get_config())
#     fig, ax = plt.subplots(2)
#     plot_ana_freq_time_rabi( output_data[r], dfs, amps, xy_LO, xy_IF_idle, ax )
#     ax[0].set_title(r)
#     ax[1].set_title(r)
# plt.show()
    

#   Data Saving   # 
xy_LO = get_LO(q_name[0],config.get_config())
xy_IF_idle = get_IF(q_name[0],config.get_config())

output_data["setting"] = {
    "xy_freq_LO":xy_LO,
    "xy_freq_Idle":xy_IF_idle
}

output_data["paras"] = {
    "xy_time":time,
    "d_xy_freq":dfs
}


save_data = True
if save_data:
    from exp.save_data import save_npz
    import sys
    save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
    save_npz(r"D:\Data\DR2_5Q", "Q1_idle_Rabi", output_data) 