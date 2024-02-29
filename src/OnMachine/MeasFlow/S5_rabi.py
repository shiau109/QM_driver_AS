
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

from datetime import datetime
import sys

from exp.rabi import xyfreq_time_rabi, plot_ana_freq_time_rabi, xyfreq_power_rabi
import numpy as np

# Dynamic config
from OnMachine.SetConfig.ConfigBuildUp_new import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from ab.QM_config_dynamic import initializer

spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, _ = spec.buildup_qmm()
init_macro = initializer(100000,mode='wait')


ro_elements = ['q1_ro']
q_name = ['q1_xy']
n_avg = 100

freq_range = (-50,50)
freq_resolution = 1
time_range = (16,400) # ns
time_resolution = 4

amps_range = (0,1.5)
amps_resolution = 0.01

from exp.config_par import *

isPower = True

if isPower:
    dataset = xyfreq_power_rabi( freq_range, freq_resolution, amps_range, amps_resolution, q_name, ro_elements, config, qmm, initializer=init_macro, n_avg=n_avg, simulate=False)
    y = dataset.coords["amplitude"].values
else:
    dataset = xyfreq_time_rabi( freq_range, freq_resolution, time_range, time_resolution, q_name, ro_elements, config, qmm, n_avg=n_avg, initializer=init_macro)
    y = dataset.coords["time"].values

freqs = dataset.coords["frequency"].values
# Plot 
for ro_name, data in dataset.data_vars.items():
    xy_LO = dataset.attrs["ref_xy_LO"][q_name[0]]/1e6
    xy_IF_idle = dataset.attrs["ref_xy_IF"][q_name[0]]/1e6
    fig, ax = plt.subplots(2)
    plot_ana_freq_time_rabi( data, freqs, y, xy_LO, xy_IF_idle, ax )
    ax[0].set_title(ro_name)
    ax[1].set_title(ro_name)
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

save_data = False
if save_data:
    from exp.save_data import save_npz
    import sys
    save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
    save_npz(r"D:\Data\DR2_5Q", "Q1_idle_Rabi", output_data) 