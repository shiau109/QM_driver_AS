
# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

import matplotlib.pyplot as plt

# Set parameters

save_dir = link_config["path"]["output_root"]

from exp.rofreq_sweep import ROFreqSweep
my_exp = ROFreqSweep(config, qmm)
my_exp.freq_range = (-400, 400)
my_exp.resolution = 0.1
my_exp.initializer = initializer(2000,mode='wait')
dataarray = my_exp.run( 10 )
# Plot
import numpy as np
dataarray = dataarray.sel(q_idx='q0_ro')
idata = dataarray.sel(mixer='I').values
qdata = dataarray.sel(mixer='Q').values
zdata = idata+1j*qdata
plt.plot(dataarray.coords["frequency"].values,np.abs(zdata))
plt.show()    
 

    
