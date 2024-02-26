
from qm.qua import *
from qm import SimulationConfig
import matplotlib.pyplot as plt
import warnings
from exp.flux_dep_qubit_spec_J import *
warnings.filterwarnings("ignore")

from datetime import datetime
import sys



# Dynamic config
from OnMachine.MeasFlow.ConfigBuildUp_new import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from OnMachine.Octave_Config.QM_config_dynamic import initializer

spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, _ = spec.buildup_qmm()
init_macro = initializer(1000,mode='wait')


ro_elements = ['q1_ro']
q_name = ['q1_xy']
z_name = ['q1_z']
# Adjust the pulse duration and amplitude to drive the qubit into a mixed state
# saturation_len = 1 * u.us  # In ns (should be < FFT of df)
# saturation_amp = 0.01  # pre-factor to the value defined in the config - restricted to [-2; 2)
n_avg = 200
span = 400 * u.MHz
df = 0.5 * u.MHz
flux_span = 0.1
flux_resolu = 0.005

dfs = np.arange(-span, +span, df)
flux = np.arange(-flux_span,flux_span+flux_resolu,flux_resolu)

output_data, flux, dfs = constant_drive_z_pulse( flux, dfs, q_name, ro_elements, z_name, config, qmm, saturation_ampRatio=0.5, saturation_len=10, n_avg=n_avg, flux_settle_time=10, simulate=False)
# output_data, flux, dfs = const_flux_qubit_spec( flux, dfs, q_name, ro_elements, z_name, config.get_config(), qmm, saturation_ampRatio=0.002, saturation_len=5, n_avg=1000, flux_settle_time=10, simulate=False)
# output_data, flux, dfs = cw_twotone_qubit( flux, dfs, q_name, ro_elements, z_name, config, qmm, saturation_ampRatio=1, saturation_len=5, n_avg=100, flux_settle_time=10, simulate=False)


plt.show()

from exp.config_par import *

# Plot
for r in ro_elements:
    xy_LO = get_LO(q_name[0],config)
    xy_IF_idle = get_IF(q_name[0],config)
    z_offset = get_offset(z_name[0],config)
    fig, ax = plt.subplots(2)
    plot_ana_flux_dep_qubit(output_data[r], flux, dfs, xy_LO, xy_IF_idle, z_offset, ax)
    ax[0].set_title(r)
    ax[1].set_title(r)

plt.show()

z_offset = get_offset(z_name[0],config)
xy_LO = get_LO(q_name[0],config)
xy_IF_idle = get_IF(q_name[0],config)

output_data["setting"] = {
    "z_offset":z_offset,
    "xy_freq_LO":xy_LO,
    "xy_freq_Idle":xy_IF_idle
}

output_data["paras"] = {
    "d_z_amp":flux,
    "d_xy_freq":dfs
}


save_data = False
if save_data:
    from exp.save_data import save_nc  
    save_nc()