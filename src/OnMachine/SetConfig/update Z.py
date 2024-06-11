from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config, configuration_read_dict
from config_component.channel_info import import_spec
import numpy as np

spec = import_spec( spec_loca )
config_obj = import_config( config_loca )

from config_component.update import update_z_offset, update_z_crosstalk

# [[ 0.99956582 -0.00793288  0.00990958  0.0121566   0.01270885]
#  [-0.02475017  0.9994467   0.01588063  0.01586771  0.01475947]
#  [-0.01740157 -0.01997843  0.99897326  0.01981986  0.01199816]
#  [-0.01968006 -0.01632376 -0.02052395  0.99920908  0.02737909]
#  [-0.01611881 -0.01063648 -0.01054133  0.00382096  0.9996285 ]]


z_infos = [
    {
        "name":"q0",
        "offset":0.2217,
        "crosstalk":{}#"6":-0.00793288/0.9994467, "9":0.00990958/0.99897326, "10":1, "4":0.01270885/0.9996285}
    },{
        "name":"q1",
        "offset":0.1941,
        "crosstalk":{}#"5":-0.02475017/0.99956582, "9":0.01588063/0.99897326, "10":1, "4":0.01475947/0.9996285}
    },{
        "name":"q2",
        "offset":0.2063,
        "crosstalk":{}#"5":-0.01740157/0.99956582, "6":-0.01997843/0.9994467, "10":1, "4":0.01199816/0.9996285}
    },{
        "name":"q3",
        "offset":0.1957,
        "crosstalk":{}#"5":-0.01968006/0.99956582, "6":-0.01632376/0.9994467, "9":-0.02052395/0.99897326, "4":0.02737909/0.9996285}
    },{
        "name":"q4",
        "offset":0.1876,#     -0.02,
        "crosstalk":{}#"5":-0.01611881/0.99956582, "6":-0.01063648/0.9994467, "9":-0.01054133/0.99897326, "10":1}
    },{
        "name":"q5",
        "offset":0.152,
        "crosstalk":{}
    },{
        "name":"q6",
        "offset":0.18,
        "crosstalk":{}
    },{
        "name":"q7",
        "offset":0.2027,
        "crosstalk":{}
    },{
        "name":"q8",
        "offset":0.184,
        "crosstalk":{}
    }
]
for i in z_infos:
    wiring = spec.get_spec_forConfig('wire')

    # Tune Z offset
    z_info = spec.update_ZInfo_for(target_q=i["name"],offset=i["offset"])
    # print(wiring[i[0]])
    update_z_offset( config_obj, z_info, wiring[i["name"]], mode='offset')

    z_info = spec.update_ZInfo_for(target_q=i["name"],crosstalk=i["crosstalk"])
    update_z_crosstalk( config_obj, z_info, wiring[i["name"]])
    config_dict = config_obj.get_config() 

import json
file_path = 'output.json'
# Open the file in write mode and use json.dump() to export the dictionary to JSON
with open(file_path, 'w') as json_file:
    json.dump(config_obj.get_config(), json_file, indent=2)

spec.export_spec(spec_loca)
config_obj.export_config(config_loca)