

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

ro_elements = ['q0_ro','q1_ro']
z_elements = ['q0_z']
dataset = freq_sweep_flux_dep(ro_elements, z_elements, config, qmm, freq_span=50, freq_resolution=0.5, flux_settle_time=10000, flux_span=0.4, flux_resolution=0.01, initializer=init_macro)

# Plot
dfs = dataset.coords["frequency"].values
amps = dataset.coords["flux"].values
for ro_name, data in dataset.data_vars.items():
    fig, ax = plt.subplots()
    plot_flux_dep_resonator( data.values, dfs, amps, ax)
    ax.set_title(ro_name)
plt.show()

save_data = False
if save_data:
    from exp.save_data import save_nc  
    save_nc(r"D:\Data\5Q4C","flux_")
