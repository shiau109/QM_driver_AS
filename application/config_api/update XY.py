

from pathlib import Path
link_path = Path(__file__).resolve().parent/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config
config_obj, spec = import_config( link_path )

from qspec.update import update_controlFreq, update_controlWaveform

import numpy as np
q_freq = 3.313  +0.025e-3
LO = 3.363
xy_infos = {

# e.g.
# "q0":{   
#     "q_freq": 3.05,   # GHz
#     "LO": 3.0,        # GHz
#     "pi_amp": 0.15,   # factor
#     "pi_len": 40,     # ns 
#     "90_corr": 1
# },

    "q0":{   # unfinish
        "q_freq": q_freq,     # 3.398  -0.116e-3+0.017e-3   02;3.297
        "LO": LO,          # GHz
        "pi_amp": 0.1*0.1*0.909,
        "pi_len": 2000,
        "90_corr": 1
    },
    "q1":{   
        "q_freq": q_freq,    # 
        "LO": LO,          # GHz
        "pi_amp": 0.1,
        "pi_len": 2000,
        "90_corr": 1
    },
    "q2":{   # unfinish, maybe low T1
        "q_freq": q_freq, # 3.15357-0.084e-3    02:3.051
        "LO": LO, # GHz
        "pi_amp": 0.1*0.1*1.13*0.9*1.002*1.061*0.999,
        "pi_len": 2000,
        "90_corr": 0.833*0.937*1.162*1.094*1.009,
        # "wf": "sin",
    },
    "q3":{   # unfinish, maybe low T1
        "q_freq": q_freq, # 3.313
        "LO": LO, # GHz
        "pi_amp": 0.1*0.149*0.5*0.979,
        "pi_len": 2000,
        "90_corr": 0.983*1.026*0.989,
        # "wf": "sin",
    },
}    
updating_qubit = ["q0","q1", "q2","q3"]

# name, q_freq(GHz), LO(GHz), amp, len, half
# update_info = [['q1', 4.526-0.005, 4.60, 0.2*0.9*1.05*1.01, 40, 1.03 ]]
for i in updating_qubit:
    # wiring = spec.get_spec_forConfig('wire')
    q_name = i
    qubit_LO = xy_infos[i]["LO"]
    qubit_RF = xy_infos[i]["q_freq"]
    ref_IF = (qubit_RF-qubit_LO)*1000
    print(f"center {ref_IF} MHz")

    pi_amp = xy_infos[i]["pi_amp"] if "pi_amp" in xy_infos[i].keys() else 0.1
    pi_len = xy_infos[i]["pi_len"] if "pi_len" in xy_infos[i].keys() else 40
    corr_90 = xy_infos[i]["90_corr"] if "90_corr" in xy_infos[i].keys() else 1
    drag_co = xy_infos[i]["drag_coef"] if "drag_coef" in xy_infos[i].keys() else 0.5
    anharm = xy_infos[i]["anharmonicity"] if "anharmonicity" in xy_infos[i].keys() else -200
    AC_stark = xy_infos[i]["AC_stark_detuning"] if "AC_stark_detuning" in xy_infos[i].keys() else 0
    qubit_wf = xy_infos[i]["wf"] if "wf" in xy_infos[i].keys() else 0

    updated_xy_freq = spec.update_aXyInfo_for(target_q=q_name, 
                                              IF=ref_IF,
                                              LO=qubit_LO,
                                              amp=pi_amp, 
                                              len=pi_len, 
                                              half=corr_90,
                                              draga=drag_co,
                                              anh=anharm,
                                              ac=AC_stark,
                                              wf=qubit_wf
                                              )
    
    update_controlFreq(config_obj, updated_xy_freq)
    if np.abs(ref_IF) > 350:
        print("Warning IF > +/-350 MHz, IF is set 350 MHz")
        ref_IF = np.sign(ref_IF)*350

    update_controlWaveform(config_obj, spec.get_spec_forConfig("xy"), target_q=q_name )

from QM_driver_AS.ultitly.config_io import output_config
output_config( link_path, config_obj, spec )
