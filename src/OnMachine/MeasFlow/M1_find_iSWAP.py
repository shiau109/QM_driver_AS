import numpy as np
import matplotlib.pyplot as plt

# Dynamic config
from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from ab.QM_config_dynamic import initializer

spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, _ = spec.buildup_qmm()
init_macro = initializer(150000,mode='wait')

from qualang_tools.units import unit
u = unit(coerce_to_integer=True)


ro_elements = ['q0_ro','q1_ro','q2_ro']
excited_q = 'q1_xy'
z_name = ['q1_z']


n_avg = 200  # The number of averages

# amps = np.arange(0.10, 0.14, 0.002)  # The abs flux amplitude absZvolt-offset
# time = np.arange(40, 8000, 200) # The flux pulse durations in clock cycles (4ns) - Must be larger than 4 clock cycles.

mid = 0.126
ra = 0.002
amps = np.arange(mid-ra, mid+ra, ra/25)  # The abs flux amplitude absZvolt-offset
time = np.arange(40, 800, 8) # The flux pulse durations in clock cycles (4ns) - Must be larger than 4 clock cycles.

cc = time/4

from exp.iSWAP_J import exp_coarse_iSWAP, plot_ana_iSWAP_chavron
output_data = exp_coarse_iSWAP( amps, cc, excited_q, ro_elements, z_name, config, qmm, n_avg=n_avg, simulate=False, initializer=init_macro )


for r in ro_elements:

    fig, ax = plt.subplots(2)
    plot_ana_iSWAP_chavron( output_data[r], amps, time, ax )
    ax[0].set_title(r)
    ax[1].set_title(r)
plt.show()

from exp.config_par import *
z_offset = get_offset(z_name[0],config)


output_data["setting"] = {
    "z_offset":z_offset,
}

output_data["paras"] = {
    "d_z_amp":amps,
    "z_time":time
}


save_data = True
if save_data:
    from exp.save_data import save_npz
    import sys
    save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
    save_npz(r"D:\Data\5Q4C\swap", "Q1Q2", output_data)    

