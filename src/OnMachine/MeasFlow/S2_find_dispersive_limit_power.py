import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt


# 20231216 Test complete :Ratis
# 20240206 Test complete :Jacky

# Dynamic config
from OnMachine.MeasFlow.ConfigBuildUp_new import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from OnMachine.Octave_Config.QM_config_dynamic import initializer

spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, _ = spec.buildup_qmm()
init_macro = initializer(1000,mode='wait')

# Measurement
n_avg = 100  # The number of averages
ro_elements = ["q1_ro"]
from exp.freq_sweep_power_dep import *
dataset = frequency_sweep_power_dep( ro_elements, config, qmm, n_avg=n_avg, freq_span=100, freq_resolution=0.2, amp_resolution=0.05, amp_max_ratio=0.2, amp_scale="log", initializer=init_macro)  

# dataset = frequency_sweep_power_dep( ro_elements, config, qmm, n_avg=n_avg, freq_span=100, freq_resolution=0.1, amp_resolution=0.05, amp_max_ratio=0.2, amp_scale="log", initializer=init_macro)  

# Plot
dfs = dataset.coords["frequency"].values
amps = dataset.coords["amp_ratio"].values
print()
for ro_name, data in dataset.data_vars.items():
    fig, ax = plt.subplots()
    plot_power_dep_resonator(dfs, amps, data.values, ax)
    ax.set_title(ro_name)
    ax.set_xlabel("additional IF freq (MHz)")
    ax.set_ylabel("amp scale")
plt.show()
 