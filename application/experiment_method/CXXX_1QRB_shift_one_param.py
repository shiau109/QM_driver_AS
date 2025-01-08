from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

# -------------- Needed function ------------------
import numpy as np
def power_law(power, a, p, b):
    return a * (p**power) + b

def ana_SQRB(x, y ):
    from scipy.optimize import curve_fit
    if state_discrimination == True:
        p0 = [-0.35, 0.95, 0.5]
    else:
        p0=[-0.0001, 0.0001, 0.0001]
    def fit_func(power, a, p, b):
        return power_law(power, a, p, b)
    pars, cov = curve_fit(
        f=fit_func,
        xdata=x,
        ydata=y,
        p0=p0,
        bounds=(-np.inf, np.inf),
        maxfev=2000,
    )
    stdevs = np.sqrt(np.diag(cov))
    
    return stdevs, pars

##############################
# Program-specific variables #
##############################
xy_elements = ["q4_xy"]
ro_elements = ["q4_ro"]
target_q = 'q4'

gate_length = 40
n_avg = 200  # Number of averaging loops for each random sequence
max_circuit_depth = 200  # Maximum circuit depth
base_clifford = 4  #  Play each sequence with a depth step equals to 'delta_clifford - Must be > 1
depth_scale = 'lin' # 'lin', 'exp'
assert base_clifford > 1, 'base must > 1'
seed = 345324  # Pseudo-random number generator seed
shot_num = 100
# Flag to enable state discrimination if the readout has been calibrated (rotated blobs and threshold)
state_discrimination = True
threshold = -1.706e-03

param_name = 'gate_time'
param_center = 480
param_shift = 440
param_resolution = 40
gate_time_times_amp = 2.68913224

# ------------------------------------------------------------
from exp.randomized_banchmarking_sq import randomized_banchmarking_sq
from exp.randomized_banchmarking_interleaved_sq import randomized_banchmarking_interleaved_sq
from qspec.update import update_controlWaveform
from QM_driver_AS.ultitly.config_io import output_config

def infidelity_func():

    my_exp = randomized_banchmarking_sq(config, qmm)
    my_exp.initializer = initializer(100000,mode='wait')
    my_exp.gate_length = param if param_name == 'gate_time' else gate_length
    my_exp.xy_elements = xy_elements
    my_exp.ro_elements = ro_elements
    my_exp.n_avg = n_avg
    my_exp.max_circuit_depth = max_circuit_depth 
    my_exp.depth_scale = depth_scale
    my_exp.base_clifford = base_clifford
    assert my_exp.base_clifford > 1, 'base must > 1'
    my_exp.seed = seed 
    my_exp.state_discrimination = state_discrimination
    my_exp.threshold = threshold
    dataset = my_exp.run(shot_num)

    data1 = dataset.data_vars[f"{target_q}_ro"]

    x = data1.coords["x"].values
    val = data1.values[0]
    err = data1.values[1]

    stdevs, pars = ana_SQRB( x, val )
    one_minus_p = 1 - pars[1]
    r_c = one_minus_p * (1 - 1 / 2**1)
    r_g = r_c / 1.875  # 1.875 is the average number of gates in clifford operation
    r_c_std = stdevs[1] * (1 - 1 / 2**1)
    r_g_std = r_c_std / 1.875

    return r_g, r_g_std

optimization_trace = {"infidelity": [],"error": []}
optimization_trace[param_name] = []
for param in np.linspace(param_center-param_shift, param_center+param_shift, int(2*param_shift/param_resolution + 1)):
    if param_name == 'gate_time':
        param = int(param)
        param1 = gate_time_times_amp/param
        print(f"amp = {param1}")
        spec.update_aXyInfo_for(target_q=target_q, 
                                amp=param1, 
                                len = param,
                                )
    else:
        spec.update_aXyInfo_for(target_q=target_q, 
                                # amp=param, 
                                # ac=param,
                                # wf=param,
                                # len = param,
                                draga=param,
                                )
    update_controlWaveform(config_obj, spec.get_spec_forConfig("xy"), target_q=target_q )
    output_config( link_path, config_obj, spec )
    f_val, err = infidelity_func()
    optimization_trace["infidelity"].append(f_val)
    optimization_trace["error"].append(err)
    optimization_trace[param_name].append(param)

# -------------- _data_formation -------------- 
import xarray as xr
output_data = {}
output_data[f"{target_q}_ro"] = (["mixer", param_name], 
                                 np.array([optimization_trace["infidelity"], 
                                           optimization_trace['error']]))
dataset = xr.Dataset(
    output_data,
    coords={
        "mixer": np.array(["infidelity",'error']),
        param_name: optimization_trace[param_name],
    }
)

save_data = 1
folder_label = "1QRB_shift_one_param" #your data and plots will be saved under a new folder with this name

if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,folder_label)

from exp.plotting import Painter1QRBShiftOneParam
painter = Painter1QRBShiftOneParam()
painter.param_name = param_name
figs = painter.plot(dataset,folder_label)
if save_data: dp.save_figs( figs )
