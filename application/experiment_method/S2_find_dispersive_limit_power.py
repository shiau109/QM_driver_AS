# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

from exp.save_data import save_nc, save_fig

import matplotlib.pyplot as plt

# Set parameters
from exp.rofreq_sweep_power_dep import ROFreqSweepPowerDep
my_exp = ROFreqSweepPowerDep(config, qmm)
my_exp.initializer = initializer(10000,mode='wait')
my_exp.ro_elements = ["q0_ro", "q1_ro", "q2_ro", "q3_ro", "q4_ro"]
my_exp.freq_range = (-15,15)
my_exp.freq_resolution = 0.1
my_exp.amp_mod_range = (0.1,1.9) # tha value range >0, <2
my_exp.amp_scale = "lin"
dataset = my_exp.run( 100 )

save_data = False
file_name = f"power_dep_resonator_{my_exp.ro_elements[0]}_{len(my_exp.ro_elements)}"
save_dir = link_config["path"]["output_root"]

if save_data: save_nc( save_dir, file_name, dataset)


# Plot
from exp.rofreq_sweep_power_dep import plot_power_dep_resonator
dfs = dataset.coords["frequency"].values
amps = dataset.coords["amp_ratio"].values

for ro_name, data in dataset.data_vars.items():
    fig, ax = plt.subplots()
    plot_power_dep_resonator(dfs, amps, data.values, ax, my_exp.amp_scale)
    ax.set_title(ro_name)
    ax.set_xlabel("additional IF freq (MHz)")
    ax.set_ylabel("amp scale")
if save_data: save_fig( save_dir, file_name)
    
plt.show()
