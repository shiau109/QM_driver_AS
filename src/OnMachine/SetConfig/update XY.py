from OnMachine.SetConfig.ConfigBuildUp_new import spec_loca, config_loca
from config_component.configuration import import_config, configuration_read_dict
from config_component.channel_info import import_spec


spec = import_spec( spec_loca )
config_obj = import_config( config_loca )

from config_component.update import update_controlFreq, update_controlWaveform

import numpy as np
# name, q_freq(GHz), LO(GHz), amp, len
update_info = [['q1', 4.526, 4.60, 0.2*0.5, 20 ]]
for i in update_info:
    # wiring = spec.get_spec_forConfig('wire')
    q_name = i[0]
    qubit_LO = i[2]
    qubit_RF = i[1]
    ref_IF = (qubit_RF-qubit_LO)*1000

    print(f"center {ref_IF}")
    print(f"amp {i[2]}")
    pi_amp = i[3]
    pi_len = i[4]

    update_controlFreq(config_obj, spec.update_aXyInfo_for(target_q=q_name,IF=ref_IF,LO=qubit_LO))
    if np.abs(ref_IF) > 350:
        print("Warning IF > +/-350 MHz, IF is set 350 MHz")
        ref_IF = np.sign(ref_IF)*350

    spec.update_aXyInfo_for(target_q=q_name, amp=pi_amp, len=pi_len)
    update_controlWaveform(config_obj, spec.get_spec_forConfig("xy"), target_q=q_name )

import json
file_path = 'output.json'
# Open the file in write mode and use json.dump() to export the dictionary to JSON
with open(file_path, 'w') as json_file:
    json.dump(config_obj.get_config(), json_file, indent=2)

spec.export_spec(spec_loca)
config_obj.export_config(config_loca)