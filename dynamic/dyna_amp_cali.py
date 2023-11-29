import sys
sys.path.append('./exp')
sys.path.append('./analysis')
from QM_config_dynamic import QM_config, Circuit_info
from qm.QuantumMachinesManager import QuantumMachinesManager
from SQGate_calibration import amp_calibration
from fitting_method import find_amp_minima

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
sequence_repeat = 3
amp_modify_range = 0.25/float(sequence_repeat)

results = amp_calibration(amp_modify_range, q_name, ro_element, dyna_config.get_config(), qmm, n_avg=n_avg, sequence_repeat=sequence_repeat, simulate=False, mode='wait_for_all')
x = results['x']
y = results[ro_element[0]][1].transpose()[1]

amp_scale,_ = find_amp_minima(x,y,'continuous')

# Update a new amp
old_amp = float(the_specs.XyInfo[f'pi_amp_{target_q}'])
the_specs.update_aXyInfo_for(target_q,amp=old_amp*float(amp_scale))
dyna_config.update_controlWaveform(the_specs.XyInfo,target_q)

# Workflow start