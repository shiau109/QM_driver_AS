


# Dynamic config
from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from ab.QM_config_dynamic import initializer

spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, _ = spec.buildup_qmm()
init_macro = initializer(300000,mode='wait')


n_avg = 200

ro_element = ["q0_ro","q1_ro","q2_ro","q3_ro","q4_ro"]
q_name =  "q4_xy"
sequence_repeat = 1
amp_modify_range = 0.4/float(sequence_repeat)
from exp.SQGate_calibration import *
drag_coef = 0.5
# output_data = DRAG_calibration_Yale( drag_coef, q_name, ro_element, config, qmm, n_avg=n_avg)
dataset = amp_calibration( amp_modify_range, q_name, ro_element, config, qmm, n_avg=n_avg, sequence_repeat=sequence_repeat, simulate=False, mode='live')


    #   Data Saving   # 
save_data = False
if save_data:
    from exp.save_data import save_nc
    import sys
    save_nc("D:\Data\03205Q4C_6", f"{q_name}_xyamp_cali", dataset)


# Plot
# print(dataset)
transposed_data = dataset.transpose("mixer", "sequence", "amplitude_ratio")
amps = transposed_data.coords["amplitude_ratio"].values

for ro_name, data in transposed_data.data_vars.items():
    print(f"ploting {ro_name} with shape {data.shape}")
    fig, ax = plt.subplots()
    # x90data = dataset.sel(sequence='x90').data_vars["zdata"].values
    # x90data = dataset.sel(sequence='x90').data_vars["zdata"].values

    ax.plot(amps,data[0][0], label="x90")
    ax.plot(amps,data[0][1], label="x180")
    fig.legend()
plt.show()
