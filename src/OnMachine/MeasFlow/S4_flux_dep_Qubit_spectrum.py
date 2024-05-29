
from qm.qua import *
from qm import SimulationConfig
import matplotlib.pyplot as plt
import warnings
from exp.xyfreq_sweep_flux_dep import *
warnings.filterwarnings("ignore")

from datetime import datetime
import sys



# Dynamic config
from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from ab.QM_config_dynamic import initializer

spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, _ = spec.buildup_qmm()
init_macro = initializer(100000,mode='wait')


ro_elements = ["q4_ro"]
q_name = ['q4_xy']
z_name = ['q4_z']


saturation_len = 2  # In us (should be < FFT of df)
saturation_ampRatio = 2 # pre-factor to the value defined in the config - restricted to [-2; 2)
n_avg = 100

flux_range = (-0.05,0.05)
flux_resolution = 0.001

freq_range = (-150,50)
freq_resolution = 1

sweep_type = "z_pulse"      # "z_pulse", "const_z", "two_tone"
dataset = xyfreq_sweep_flux_dep( flux_range, flux_resolution, freq_range, freq_resolution, q_name, ro_elements, z_name, config, qmm, saturation_ampRatio=saturation_ampRatio, saturation_len=saturation_len, n_avg=n_avg, sweep_type=sweep_type, simulate=False)

# Plot
freqs = dataset.coords["frequency"].values
flux = dataset.coords["flux"].values
for i, (ro_name, data) in enumerate(dataset.data_vars.items()):
    xy_LO = dataset.attrs["xy_LO"][0]/1e6
    xy_IF_idle = dataset.attrs["xy_IF"][0]/1e6
    z_offset = dataset.attrs["z_offset"][0]
    print(ro_name, xy_LO, xy_IF_idle, z_offset, data.shape)
    fig, ax = plt.subplots(2)
    plot_ana_flux_dep_qubit(data, flux, freqs, xy_LO, xy_IF_idle, z_offset, ax)
    ax[0].set_title(ro_name)
    ax[1].set_title(ro_name)

# print( dataset.attrs)

save_data = True
if save_data:
    from exp.save_data import save_nc, save_fig
    save_dir = r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240521_DR4_5Q4C_0430#7\00 raw data"
    save_name = f"Spectrum_{q_name[0]}_{z_name[0]}_{sweep_type}"
    save_nc(save_dir, save_name, dataset)
    save_fig(save_dir, save_name)



plt.show()