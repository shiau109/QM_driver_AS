
from qm.qua import *
import matplotlib.pyplot as plt
import warnings
from exp.zline_crosstalk import *
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


n_avg = 1000
expect_crosstalk = 0.01
flux_modify_range = 0.3
target = "q4"
crosstalk = "q3"
mode="ramsey"   #"long"
prob_q_name = f"{target}_xy"
ro_element = f"{target}_ro"
z_line = [f"{target}_z", f"{crosstalk}_z"]
# flux_settle_time = 400 * u.us
print(f"Z {target} offset {get_offset(z_line[0],config)} +/- {flux_modify_range*expect_crosstalk}")
print(f"Z {crosstalk} offset {get_offset(z_line[1],config)} +/- {flux_modify_range}")
if mode=="ramsey":
    evo_time = 3
    output_data, f_t, f_c = ramsey_z_pulse( flux_modify_range, prob_q_name, ro_element, z_line, config, qmm, expect_crosstalk=expect_crosstalk, n_avg=n_avg, initializer=init_macro, simulate=False, evo_time=evo_time)
elif mode=="long":
    evo_time = 10
    amp_ratio = 0.05
    output_data, f_t, f_c = pi_z_pulse( flux_modify_range, prob_q_name, ro_element, z_line, config, qmm, expect_crosstalk=expect_crosstalk, amp_ratio=amp_ratio, n_avg=n_avg, initializer=init_macro, simulate=False, evo_time=evo_time)
else:
    print("no such mode")


for r in [ro_element]:
    fig = plt.figure()
    ax = fig.subplots()
    print(type(f_t), type(f_c), output_data[r].shape )
    plot_crosstalk_3Dscalar( f_c*1000, f_t*1000, output_data[r][0], z_line, ax )
    ax.tick_params(axis='both', labelsize=12)
    ax.set_xlabel(f"{z_line[1]} Delta Voltage (mV)", fontsize=15)
    ax.set_ylabel(f"{z_line[0]} Delta Voltage (mV)", fontsize=15)
    ax.set_aspect(1/expect_crosstalk) 
    fig.suptitle(f"{r} RO freq", fontsize=15)


# amps = np.arange( 0.2, 1.5, 0.01)
# output_data = power_dep_signal( amps, operate_qubit, ro_elements, n_avg, config.get_config(), qmm, initializer=init_macro)

# for r in ro_elements:
#     fig = plt.figure()
#     ax = fig.subplots(1,2,sharex=True)
#     plot_amp_signal( amps, output_data[r], r, ax[0] )
#     plot_amp_signal_phase( amps, output_data[r], r, ax[1] )
#     fig.suptitle(f"{r} RO amplitude")
# plt.show()
    
from exp.config_par import *

#   Data Saving   # 
# z_offset = get_offset(z_line[0],config.get_config())
xy_LO = get_LO(prob_q_name,config)
xy_IF_idle = get_IF(prob_q_name,config)

output_data["setting"] = {
    # "z_offset":z_offset,
    "xy_freq_LO":xy_LO,
    "xy_freq_Idle":xy_IF_idle
}

output_data["paras"] = {
    "d_z_target_amp":f_t,
    "d_z_crosstalk_amp":f_c
}


save_data = True
if save_data:
    from exp.save_data import save_npz, save_fig
    save_dir = r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240521_DR4_5Q4C_0430#7\03 zline_ramsey_1micro"
    save_name = f"target_{target}_crosstalk_{crosstalk}_{mode}_zlinecrosstalk_{expect_crosstalk}"
    save_npz(save_dir, save_name, output_data)
    save_fig(save_dir, save_name)
plt.show()
