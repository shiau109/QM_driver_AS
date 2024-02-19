

from qm.qua import *
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from exp.freq_sweep_flux_dep import *

# 20231218 Test complete: Ratis
# 20230217 Test complete: Jacky

# Dynamic config
from OnMachine.MeasFlow.ConfigBuildUp_new import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from OnMachine.Octave_Config.QM_config_dynamic import initializer

spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, _ = spec.buildup_qmm()
init_macro = initializer(spec.give_depletion_time_for("q1"),mode='depletion')

ro_elements = ['q1_ro']
z_elements = ['q1_z']
dataset = freq_sweep_flux_dep(ro_elements, z_elements, config, qmm, initializer=init_macro)

# Plot
dfs = dataset.coords["frequency"].values
amps = dataset.coords["flux"].values
for ro_name, data in dataset.data_vars.items():
    fig, ax = plt.subplots()
    plot_flux_dep_resonator( data.values, dfs, amps, ax)
    ax.set_title(ro_name)
    ax.set_xlabel("additional IF freq (MHz)")
    ax.set_ylabel("amp scale")
plt.show()
