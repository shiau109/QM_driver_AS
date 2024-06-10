

from pathlib import Path
link_path = Path(__file__).resolve().parent/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config
config_obj, spec = import_config( link_path )

from config_component.update import update_controlFreq, update_controlWaveform

import numpy as np

xy_infos = [
    {
        "name":"q0",
        "q_freq": 5.263+0.321e-3-0.42e-3-0.253e-3+0.034e-3+0.713e-3-0.018e-3, # GHz
        "LO": 5.3, # GHz
        "pi_amp": 0.2*1.4*1.05*0.9840*0.715,
        "pi_len": 40,
        "90_corr": 1.15*0.9554*0.9651*0.829*1.2
    },{
        "name":"q1",
        "q_freq": 4.740+0.15e-3-2.074e-3+0.101e-3-0.029e-3+0.062e-3-0.062e-3+0.023e-3-0.035e-3, # GHz
        "LO": 4.760, # GHz
        "pi_amp": 0.1*1.259*1.2*0.861*1.0013*1.02,
        "pi_len": 40,
        "90_corr": 1.0255*1.02*0.98
    },{
        "name":"q2",
        "q_freq": 5.073-2.675e-3-0.031e-3, # GHz
        "LO": 5.1, # GHz
        "pi_amp": 0.1*0.862,
        "pi_len": 40,
        "90_corr": 1.0
    },{
        "name":"q3",
        "q_freq": 4.823+0.1e-3+0.052e-3-0.019e-3-0.021e-3, # GHz
        "LO": 4.850, # GHz
        "pi_amp": 0.1*0.798*1.035,
        "pi_len": 40,
        "90_corr": 1.0207*0.9723
    },{
        "name":"q4",
        "q_freq": 5.207-0.269e-3+0.005e-3-0.046e-3+0.04e-3-0.013e-3, # GHz
        "LO": 5.25, # GHz
        "pi_amp": 0.1*1.572*1.0526,
        "pi_len": 40,
        "90_corr": 1.0734*0.9523
    }
    ,
    {
        "name":"q5",
        "q_freq": 7.57, # GHz
        "LO": 7.62, # GHz
        "pi_amp": 0.1,
        "pi_len": 400,
        "90_corr": 1.0
    },{
        "name":"q6",
        "q_freq": 7.323, # GHz
        "LO": 7.36, # GHz
        "pi_amp": 0.1,
        "pi_len": 400,
        "90_corr": 1.0
    },{
        "name":"q7",
        "q_freq": 8.0377, # GHz
        "LO": 8.1, # GHz
        "pi_amp": 0.1,
        "pi_len": 400,
        "90_corr": 1.0
    },{
        "name":"q8",
        "q_freq": 7.985, # GHz
        "LO": 8.05, # GHz
        "pi_amp": 0.1,
        "pi_len": 400,
        "90_corr": 1.0
    },
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
output_config( config_path, config_obj, spec )