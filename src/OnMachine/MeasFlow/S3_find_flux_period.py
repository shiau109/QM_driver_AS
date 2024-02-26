

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
init_macro = initializer(1000,mode='wait')

ro_elements = ['q0_ro']
z_elements = ['q1_z']
# dataset = freq_sweep_flux_dep(ro_elements, z_elements, config, qmm, freq_span=100, freq_resolution=0.1, flux_settle_time=1000, flux_span=0.4, flux_resolution=0.01, n_avg=100, initializer=init_macro)
dataset = freq_sweep_flux_dep_stable(ro_elements, z_elements, config, qmm, freq_span=100, freq_resolution=0.1, flux_settle_time=1000, flux_span=0.4, flux_resolution=0.01, n_avg=100, initializer=init_macro)

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
    save_nc(r"D:\Data\5Q4C",f"flux_{ro_elements[0]}_{z_elements[0]}_C1_3",dataset)
