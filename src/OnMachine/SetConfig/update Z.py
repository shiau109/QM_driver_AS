from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config, configuration_read_dict
from config_component.channel_info import import_spec
import numpy as np

spec = import_spec( spec_loca )
config_obj = import_config( config_loca )

from config_component.update import update_z_offset

z_infos = [
    {
        "name":"q0",
        "offset":0,
    },{
        "name":"q1",
        "offset":0.027,
    },{
        "name":"q3",
        "offset":0,
    },{
        "name":"q5",
        "offset":-0.12,
    }
]
for i in z_infos:
    wiring = spec.get_spec_forConfig('wire')

    # Tune Z offset
    z_info = spec.update_ZInfo_for(target_q=i["name"],offset=i["offset"])
    # print(wiring[i[0]])
    update_z_offset( config_obj, z_info, wiring[i["name"]], mode='offset')
    config_dict = config_obj.get_config() 

import json
file_path = 'output.json'
# Open the file in write mode and use json.dump() to export the dictionary to JSON
with open(file_path, 'w') as json_file:
    json.dump(config_obj.get_config(), json_file, indent=2)

spec.export_spec(spec_loca)
config_obj.export_config(config_loca)