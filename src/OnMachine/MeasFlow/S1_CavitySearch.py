
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt


# 20231215 Test complete :Ratis
# 20240202 Test complete :Jacky

# Dynamic config
from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from ab.QM_config_dynamic import initializer

spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, _ = spec.buildup_qmm()
init_macro = initializer(1000,mode='wait')

# Measurement
from exp.rofreq_sweep import *
freq_range = (-300, 0)
resolution = 1
dataset = frequency_sweep(config,qmm,n_avg=1000,freq_range=freq_range, resolution=resolution,initializer=init_macro)  

# Plot
idata = dataset["q0_ro"].sel(mixer='I').values
qdata = dataset["q0_ro"].sel(mixer='Q').values
zdata = idata+1j*qdata
plt.plot(dataset.coords["frequency"].values,np.abs(zdata))
plt.show()    
 

    
