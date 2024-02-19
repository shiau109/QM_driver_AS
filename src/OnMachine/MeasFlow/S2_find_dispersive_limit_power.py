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
init_macro = initializer(spec.give_depletion_time_for("q1"),mode='depletion')

# Measurement
n_avg = 100  # The number of averages
ro_elements = ["q1_ro"]
from exp.freq_sweep_power_dep import *
dataset = frequency_sweep_power_dep( ro_elements, config, qmm, n_avg=n_avg, amp_max_ratio=1.25, initializer=init_macro)  

# Plot
dfs = dataset.coords["frequency"].values
amps = dataset.coords["amp_ratio"].values
for ro_name, data in dataset.data_vars.items():
    fig, ax = plt.subplots()
    plot_power_dep_resonator(dfs, amps, data.values, ax)
    ax.set_title(ro_name)
    ax.set_xlabel("additional IF freq (MHz)")
    ax.set_ylabel("amp scale")
plt.show()
 