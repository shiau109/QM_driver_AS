from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
import numpy as np

spec = import_spec( spec_loca )
config_obj = import_config( config_loca )

from config_component.update import update_ReadoutFreqs, update_Readout
new_LO = 5.9
# rin_offset = (+0.0156,+0.0067) # I,Q
rin_offset = (+0,+0) # I,Q
tof = 300
# init_value of readout amp is 0.2
# 
# name, IF, amp, z, len, angle
ro_infos = [
    {
        "name":"q0",
        "IF":+150-33.8,
        "amp":0.3*0.05 *1.5,
        "length":2000,
        "phase":0
    },{
        "name":"q1",
        "IF":+150+1.3+0.3,
        "amp": 0.3*0.05 *1.5*1.4,
        "length":1500,
        "phase":84.7+19+ 110.6
    },{
        "name":"q2",
        "IF":+150+10+8.7,
        "amp": 0.3*0.05 *1.5*1.2,
        "length":1500,
        "phase":84.7+19
    },{
        "name":"q3",
        "IF":+150+2+2,
        "amp": 0.3*0.05,
        "length":2000,
        "phase":84.7+19
    },{
        "name":"q5",
        "IF":+150,
        "amp":0.3*0.1,
        "length":2000,
        "phase":0
    },
    {
        "name":"q8",
        "IF":+10,
        "amp":0.3*0.1,
        "length":2000,
        "phase":0
    },



]
# cavities = [['q0',+150-33, 0.3*0.1, 0, 2000,0],['q1',+150+0.8, 0.3*0.1*1.5*1.5*1.4, 0.038, 560,84.7],['q8',+150+3, 0.01, 0.1, 2000,0],['q5',+150-36, 0.3*0.05, -0.11, 2000,0]]
for i in ro_infos:
    wiring = spec.get_spec_forConfig('wire')

    f = spec.update_RoInfo_for(target_q=i["name"],LO=new_LO,IF=i["IF"])
    update_ReadoutFreqs(config_obj, f)
    ro_rotated_rad = i["phase"]/180*np.pi
    spec.update_RoInfo_for(i["name"],amp=i["amp"], len=i["length"],rotated=ro_rotated_rad, offset=rin_offset, time=tof)
    update_Readout(config_obj, i["name"], spec.get_spec_forConfig('ro'),wiring)
    # print(spec.get_spec_forConfig('ro')["q1"])

    config_dict = config_obj.get_config() 

import json
file_path = 'output.json'
# Open the file in write mode and use json.dump() to export the dictionary to JSON
with open(file_path, 'w') as json_file:
    json.dump(config_obj.get_config(), json_file, indent=2)

spec.export_spec(spec_loca)
config_obj.export_config(config_loca)