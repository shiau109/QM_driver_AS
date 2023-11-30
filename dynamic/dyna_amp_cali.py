import sys
sys.path.append('./exp')
sys.path.append('./analysis')
from QM_config_dynamic import QM_config, Circuit_info
from qm.QuantumMachinesManager import QuantumMachinesManager
from exp.SQGate_calibration import amp_calibration
from analysis.fitting_method import find_amp_minima, math_eqns
from numpy import mean, ndarray, arange
import matplotlib.pyplot as plt

qop_ip = ''
qop_port = ''
cluster_name = ''
octave_config = ''
target_q = 'q4'
ro_element = [f'{target_q}_ro']
q_name =  f"{target_q}_xy"

qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
n_avg = 4000

# load config file
dyna_config = QM_config.import_config('')
the_specs = Circuit_info.import_spec('')


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
x = arange(0.8,1.25,0.05)
amp_scale = 1.2
precision_N_idx = 0
N_candidate = [3, 30, 100]
iterations = 0
max_iteration = 10

# Workflow start
while (precision_N_idx <= len(N_candidate)-1) and (iterations < max_iteration):
    sequence_repeat = N_candidate[precision_N_idx]
    amp_modify_range = 0.25/float(sequence_repeat)
    
    if new_N_condition(x,amp_scale,12):
        precision_N_idx += 1

    results = amp_calibration(amp_modify_range, q_name, ro_element, dyna_config.get_config(), qmm, n_avg=n_avg, sequence_repeat=sequence_repeat, simulate=False, mode='wait_for_all')
    x = results['x']
    y = results[ro_element[0]][1].transpose()[1]
    amp_scale,fit_paras = find_amp_minima(x,y,'continuous')

    # plot and check 
    plt.plot(x,y,label='exp')
    plt.scatter(x, math_eqns.cosine(amp_scale,*fit_paras),c='red',marker='X',s=80 ,label='ans')
    plt.title(f'N={sequence_repeat}')
    plt.legend()
    plt.show()

    # Update amp
    the_specs,dyna_config = refresh_amp(the_specs,dyna_config,amp_scale)
    iterations += 1


