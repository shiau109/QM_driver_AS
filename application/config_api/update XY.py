

from pathlib import Path
link_path = Path(__file__).resolve().parent/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config
config_obj, spec = import_config( link_path )

from config_component.update import update_controlFreq, update_controlWaveform

import numpy as np

xy_infos = [
    {
        "name":"q0",
        "q_freq": 4.65, # GHz
        "LO": 4.8, # GHz
        "pi_amp": 0.2,
        "pi_len": 40,
        "90_corr": 1
    },
    {
        "name":"q3",
        "q_freq": 4.8, # GHz
        "LO": 4.85, # GHz
        "pi_amp": 0.2,
        "pi_len": 40,
        "90_corr": 1
    },{
        "name":"q4",
        "q_freq": 4.736 +1.1e-3 +0.05e-3, # GHz
        "LO": 4.85, # GHz
        "pi_amp": 0.2 *1.12 *0.9935,
        "pi_len": 40,
        "90_corr": 1
    }
    
]
# name, q_freq(GHz), LO(GHz), amp, len, half
# update_info = [['q1', 4.526-0.005, 4.60, 0.2*0.9*1.05*1.01, 40, 1.03 ]]
for i in xy_infos:
    # wiring = spec.get_spec_forConfig('wire')
    q_name = i["name"]
    qubit_LO = i["LO"]
    qubit_RF = i["q_freq"]
    ref_IF = (qubit_RF-qubit_LO)*1000

    print(f"center {ref_IF} MHz")
    pi_amp = i["pi_amp"]
    pi_len = i["pi_len"]

    update_controlFreq(config_obj, spec.update_aXyInfo_for(target_q=q_name,IF=ref_IF,LO=qubit_LO))
    if np.abs(ref_IF) > 350:
        print("Warning IF > +/-350 MHz, IF is set 350 MHz")
        ref_IF = np.sign(ref_IF)*350

    spec.update_aXyInfo_for(target_q=q_name, amp=pi_amp, len=pi_len, half=i["90_corr"])
    update_controlWaveform(config_obj, spec.get_spec_forConfig("xy"), target_q=q_name )

from QM_driver_AS.ultitly.config_io import output_config
output_config( link_path, config_obj, spec )