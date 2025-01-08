from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

import matplotlib.pyplot as plt

from exp.relaxation_time import exp_relaxation_time

#Set parameters
my_exp1 = exp_relaxation_time(config, qmm)
my_exp1.initializer = initializer(120000,mode='wait')
my_exp1.ro_elements = ["q4_ro"]
my_exp1.xy_elements = ["q4_xy"]
my_exp1.max_time = 100
my_exp1.time_resolution = 0.5
my_exp1.shot_num = 500

from exp.randomized_banchmarking_sq import randomized_banchmarking_sq

my_exp2 = randomized_banchmarking_sq(config, qmm)
my_exp2.initializer = initializer(120000,mode='wait')
# pi_len = the_specs.get_spec_forConfig('xy')['q1']['pi_len']
##############################
# Program-specific variables #
##############################
my_exp2.xy_elements = ["q4_xy"]
my_exp2.ro_elements = ["q4_ro"]
# threshold = the_specs.get_spec_forConfig('ro')[xy_element]['ge_threshold']

my_exp2.gate_length = 40
my_exp2.n_avg = 300  # Number of averaging loops for each random sequence
my_exp2.max_circuit_depth = 500  # Maximum circuit depth
my_exp2.depth_scale = 'lin' # 'lin', 'exp'
my_exp2.base_clifford = 3  #  Play each sequence with a depth step equals to 'delta_clifford - Must be >= 2
assert my_exp2.base_clifford > 1, 'base must > 1'
my_exp2.seed = 345322  # Pseudo-random number generator seed
my_exp2.state_discrimination = True
my_exp2.threshold = -1.787e-03
my_exp2.shot_num = 80

from exp.repetition_measurement import RepetitionMeasurement
re_exp = RepetitionMeasurement()
re_exp.exp_list = [ my_exp2, my_exp1]
re_exp.exp_name = [ "1QRB", "T1"]
dataset = re_exp.run(90)

#Save data
save_data = 1
folder_label = "T1_with_1QRB_repeat" #your data and plots will be saved under a new folder with this name
if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    for name in re_exp.exp_name:
        dp.save_nc(dataset[name],f"T1_with_1QRB_repeat_{name}")

from exp.plotting import Painter1QRBRepeatWithT1
painter = Painter1QRBRepeatWithT1()
painter.state_discrimination = my_exp2.state_discrimination
figs = painter.plot_rep(dataset,folder_label)
if save_data: dp.save_figs( figs )

# plot_SQRB_result( x, value_avg, error_avg )

# plt.show()