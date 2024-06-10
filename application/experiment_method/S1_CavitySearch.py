
# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer
init_macro = initializer(200000,mode='wait')

from exp.save_data import save_nc, save_fig

import matplotlib.pyplot as plt

# Set parameters
from exp.rofreq_sweep import *

save_dir = link_config["path"]["output_root"]

n_avg = 1000
freq_range = (-300, +300)
resolution = 1
dataset = frequency_sweep(config,qmm,n_avg=n_avg,freq_range=freq_range, resolution=resolution,initializer=init_macro)  

# Plot
idata = dataset["q0_ro"].sel(mixer='I').values
qdata = dataset["q0_ro"].sel(mixer='Q').values
zdata = idata+1j*qdata
plt.plot(dataset.coords["frequency"].values,np.abs(zdata))
plt.show()    
 

    
