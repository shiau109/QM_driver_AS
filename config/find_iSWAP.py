import numpy as np
import matplotlib.pyplot as plt

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
excited_q = 'q1_xy'
z_name = ['q3_z']
# Adjust the pulse duration and amplitude to drive the qubit into a mixed state
# saturation_len = 1 * u.us  # In ns (should be < FFT of df)
# saturation_amp = 0.01  # pre-factor to the value defined in the config - restricted to [-2; 2)


n_avg = 1300  # The number of averages
amps = np.arange(-0.04, -0.05, -0.00025)  # The abs flux amplitude absZvolt-offset
time = np.arange(40, 8000, 40) # The flux pulse durations in clock cycles (4ns) - Must be larger than 4 clock cycles.

cc = time/4

from exp.iSWAP_J import exp_coarse_iSWAP, plot_ana_iSWAP_chavron
output_data = exp_coarse_iSWAP( amps, cc, excited_q, ro_elements, z_name, config.get_config(), qmm, n_avg=100, simulate=False, initializer=init_macro )


for r in ro_elements:

    fig, ax = plt.subplots(2)
    plot_ana_iSWAP_chavron( output_data[r], amps, time, ax )
    ax[0].set_title(r)
    ax[1].set_title(r)
plt.show()

from exp.config_par import *
z_offset = get_offset(z_name[0],config.get_config())


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
    save_npz(r"D:\Data\DR2_5Q", "iSWAP_Qc3500", output_data)    

