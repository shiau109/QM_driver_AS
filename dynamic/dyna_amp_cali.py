import sys
sys.path.append('./exp')
sys.path.append('./analysis')
from QM_config_dynamic import QM_config, Circuit_info
from qm.QuantumMachinesManager import QuantumMachinesManager
from exp.SQGate_calibration import amp_calibration
from analysis.fitting_method import find_amp_minima, math_eqns
from numpy import mean, ndarray, arange
import matplotlib.pyplot as plt
from set_octave import OctaveUnit, octave_declaration
import time

start_time = time.time()

qop_ip = '192.168.1.105'
qop_port = None
cluster_name = 'QPX_2'
target_q = 'q1'
ro_element = [f'{target_q}_ro']
q_name =  f"{target_q}_xy"

port_mapping = {
    ("con1", 1): ("octave1", "I1"),
    ("con1", 2): ("octave1", "Q1"),
    ("con1", 3): ("octave1", "I2"),
    ("con1", 4): ("octave1", "Q2"),
    ("con1", 5): ("octave1", "I3"),
    ("con1", 6): ("octave1", "Q3"),
    ("con1", 7): ("octave1", "I4"),
    ("con1", 8): ("octave1", "Q4"),
    ("con1", 9): ("octave1", "I5"),
    ("con1", 10): ("octave1", "Q5"),
}

octave_1 = OctaveUnit("octave1", qop_ip, port=11250, con="con1", clock="Internal", port_mapping=port_mapping)
# Add the octaves
octaves = [octave_1]
# Configure the Octaves
octave_config = octave_declaration(octaves)

qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
n_avg = 4000

# load config file
dyna_config = QM_config()
dyna_config.import_config(path='dynamic/TESTconfig_forAmp')
the_specs = Circuit_info(q_num=5)
the_specs.import_spec(path='dynamic/TESTspec_forAmp')


# Update a new amp
def refresh_amp(specs:dict,config:object,amp_modi_scale:float):
    old_amp = float(specs.XyInfo[f'pi_amp_{target_q}'])
    specs.update_aXyInfo_for(target_q,amp=old_amp*amp_modi_scale)
    config.update_controlWaveform(specs.XyInfo,target_q)
    return specs, config


def new_N_condition(x:ndarray,amp_scale:float,sweetspot:int=12):
    if amp_scale > 1-(mean(x)/sweetspot)*0.5 and amp_scale < 1+(mean(x)/sweetspot)*0.5:
        return True
    else:
        return False
    
# initialize
precision_N_idx = 0
N_candidate = [1, 3, 10, 30]
iterations = 0
max_iteration = 15

# Workflow start
while (precision_N_idx <= len(N_candidate)-1) and (iterations < max_iteration):
    sequence_repeat = N_candidate[precision_N_idx]
    amp_modify_range = 0.25/float(sequence_repeat)

    results = amp_calibration(amp_modify_range, q_name, ro_element, dyna_config.get_config(), qmm, n_avg=n_avg, sequence_repeat=sequence_repeat, simulate=False, mode='wait_for_all')
    x = results['x']
    # # plot exp results
    # fig, ax = plt.subplots(2, len(ro_element))
    # for r_idx, r_name in enumerate(ro_element):
    #     ax[r_idx*2].cla()
    #     ax[r_idx*2+1].cla()
    #     for op_idx, op in enumerate(["x90","x180"]):
    #         ax[r_idx*2].plot(x, results[r_name][0].transpose()[op_idx], label=op)
    #         ax[r_idx*2+1].plot(x, results[r_name][1].transpose()[op_idx], label=op)
    #     plt.show()
    y = results[ro_element[0]][0].transpose()[1]
    amp_scale,fit_paras = find_amp_minima(x,y,'continuous')

    # Update amp
    the_specs,dyna_config = refresh_amp(the_specs,dyna_config,amp_scale)
    iterations += 1
    if new_N_condition(x,amp_scale,10):
        precision_N_idx += 1

end_time = time.time()

# plot optimized results
plt.plot(x,y,label='exp')
plt.plot(x, math_eqns.cosine(x,*fit_paras), label='fit')
plt.scatter(amp_scale, math_eqns.cosine(amp_scale,*fit_paras),c='red',marker='X',s=80 ,label='ans')
plt.title(f'N={sequence_repeat},fianl amp modified scale={amp_scale}')
plt.legend()
plt.show()

the_specs.export_spec('spec_after_ampCali')
dyna_config.export_config('config_after_ampCali')

print(f"Optimize completed! Time cost: {end_time-start_time}s")

