
from pathlib import Path
link_path = Path(__file__).resolve().parent/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config
config_obj, spec = import_config( link_path )

from qspec.update import update_z_offset, update_z_crosstalk, update_zWaveform

# [[ 0.99954093  0.00685605 -0.01088031 -0.01185879 -0.01199802]
#  [ 0.02307034  0.99941776 -0.01729353 -0.01564188 -0.01406762]
#  [ 0.01713722  0.01930098  0.99897034 -0.02075049 -0.01185133]
#  [ 0.02022993  0.01678385  0.01898975  0.99923273 -0.02882381]
#  [ 0.01681398  0.01113205  0.00966305 -0.00497131  0.99965561]]

z_infos = {
    "q0":{
        "offset": -0.0,#0.2217,
        "crosstalk":{},
        "z_amp": 0.1,
        "z_len": 1000,
    },
    "q1":{
        "offset": -0.03,#0.0398,#0.1941,
        "crosstalk":{},
        "z_amp": 0.1,
        "z_len": 1000,
    },
    "q2":{
        "offset": 0.071,#0.11,#0.134,#0.07,#0.0398,#0.129,#0.0398,#0.0951+0.0153,#0.0301,#0.1641,
        "crosstalk":{},
        "z_amp": 0.1,
        "z_len": 1000,
    },
    "q3":{
        "offset": 0.062,#0.127,#0.075,#0.171,#0.019,#-0.088,#0.0301,#0.1487,
        "crosstalk":{},
        "z_amp": 0.1,
        "z_len": 1000,
    },
    "q4":{
        "offset": 0.0,#0.256,#0.21,#0.0301,#0.15,#0.0301,#0.1519,
        "crosstalk":{},
        "z_amp": 0.1,
        "z_len": 1000,
    },
    "q5":{
        "offset": 0.0,#0.152,
        "crosstalk":{},
        "z_amp": 0.1,
        "z_len": 1000,
    },
    "q6":{
        "offset": 0.0,#0.16,#0.18+0.02,#0.0688+0.143,#0.186,#0.0688,#0.23,
        "crosstalk":{},
        "z_amp": 0.1,
        "z_len": 1000,
    },
    "q7":{
        "offset": 0.067,#0.094,#+0.026,#0.192+0.036,#0.0301,#0.214,#0.0301,#0.2027,
        "crosstalk":{},
        "z_amp": 0.1,
        "z_len": 1000,
    },
    "q8":{
        "offset": 0.0,#0.079-0.1809-0.08+0.08,#0.0192,#+0.235,#0.184,
        "crosstalk":{},
        "z_amp": 0.1,
        "z_len": 1000,
    }
}
updating_qubit = ["q0","q1","q2","q3","q4","q5","q6","q7","q8"]

for i in updating_qubit:
    q_name = i
    wiring = spec.get_spec_forConfig('wire')

    z_wf = z_infos[i]["z_wf"] if "z_wf" in z_infos[i].keys() else "sin"
    z_amp = z_infos[i]["z_amp"] if "z_amp" in z_infos[i].keys() else 0.5
    z_len = z_infos[i]["z_len"] if "z_amp" in z_infos[i].keys() else 40
    z_freq = z_infos[i]["z_freq"] if "z_freq" in z_infos[i].keys() else 1
    z_phase = z_infos[i]["z_phase"] if "z_phase" in z_infos[i].keys() else 0

    # Tune Z offset
    z_info = spec.update_ZInfo_for(target_q=q_name,
                                   offset=z_infos[i]["offset"],
                                   crosstalk=z_infos[i]["crosstalk"],
                                   wf=z_wf,
                                   amp=z_amp,
                                   len=z_len,
                                   freq=z_freq,
                                   phase=z_phase,
                                   )
    # print(wiring[i[0]])
    update_z_offset( config_obj, z_info, wiring[q_name], mode='offset')
    update_z_crosstalk( config_obj, z_info, wiring[q_name])
    update_zWaveform(config_obj, spec.get_spec_forConfig("z"), target_q=q_name )
    config_dict = config_obj.get_config() 


from QM_driver_AS.ultitly.config_io import output_config
output_config( link_path, config_obj, spec )