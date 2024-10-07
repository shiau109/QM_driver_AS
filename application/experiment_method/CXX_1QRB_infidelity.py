from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

import matplotlib.pyplot as plt

##############################
# Program-specific variables #
##############################
gate_length = 40
xy_elements = ["q3_xy","q4_xy"]
ro_elements = ["q3_ro","q4_ro"]

# threshold = the_specs.get_spec_forConfig('ro')[xy_element]['ge_threshold']
n_avg = 20  # Number of averaging loops for each random sequence
max_circuit_depth = 100  # Maximum circuit depth
delta_clifford = 1  #  Play each sequence with a depth step equals to 'delta_clifford - Must be > 1

seed = 345324  # Pseudo-random number generator seed
interleaved_gate_index = 2
same_seq = True
shot_num = 20
# Flag to enable state discrimination if the readout has been calibrated (rotated blobs and threshold)
# state_discrimination = [1e-3]

# ------------------------------------------------------------
from exp.randomized_banchmarking_sq import randomized_banchmarking_sq

my_exp = randomized_banchmarking_sq(config, qmm)
my_exp.initializer = initializer(100000,mode='wait')
my_exp.gate_length = gate_length
my_exp.xy_elements = xy_elements
my_exp.ro_elements = ro_elements
# my_exp.threshold = threshold
my_exp.n_avg = n_avg
my_exp.max_circuit_depth = max_circuit_depth 
my_exp.delta_clifford = delta_clifford
assert (my_exp.max_circuit_depth / my_exp.delta_clifford).is_integer(), "max_circuit_depth / delta_clifford must be an integer."
my_exp.seed = seed 
dataset = my_exp.run(shot_num)

from exp.randomized_banchmarking_interleaved_sq import randomized_banchmarking_interleaved_sq

my_exp = randomized_banchmarking_interleaved_sq(config, qmm)
my_exp.initializer = initializer(100000,mode='wait')
my_exp.gate_length = gate_length
my_exp.xy_elements = xy_elements
my_exp.ro_elements = ro_elements
# my_exp.threshold = threshold
my_exp.n_avg = n_avg
my_exp.max_circuit_depth = max_circuit_depth 
my_exp.delta_clifford = delta_clifford
assert (my_exp.max_circuit_depth / my_exp.delta_clifford).is_integer(), "max_circuit_depth / delta_clifford must be an integer."
my_exp.seed = seed 
my_exp.interleaved_gate_index = interleaved_gate_index
dataset_interleaved = my_exp.run(shot_num)

save_data = 1
folder_label = "1QRB_infedelity" #your data and plots will be saved under a new folder with this name

if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,"1QRB")
    dp.save_nc(dataset_interleaved,"1QRB_interleaved")

from exp.plotting import Painter1QRB_infidelity
painter = Painter1QRB_infidelity(my_exp.interleaved_gate_index)
figs = painter.plot(dataset,folder_label,infedelity=dataset_interleaved)
if save_data: dp.save_figs( figs )

# plot_SQRB_result( x, value_avg, error_avg )

# plt.show()