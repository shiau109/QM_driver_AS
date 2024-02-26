from OnMachine.MeasFlow.ConfigBuildUp_new import spec_loca, config_loca
from config_component.configuration import import_config, configuration_read_dict
from config_component.channel_info import import_spec


spec = import_spec( spec_loca )
config_obj = import_config( config_loca )

from config_component.update import update_controlFreq

cavities = [['q1',0,4.9]]
for i in cavities:
    # wiring = spec.get_spec_forConfig('wire')
    update_controlFreq(config_obj, spec.update_aXyInfo_for(target_q=i[0],IF=i[1],LO=i[2]))

# f = spec.update_RoInfo_for(target_q="q2",len=800, rotated=(269.5/180)*np.pi )
# config.update_Readout("q2", spec.get_spec_forConfig("ro") ) 
# print(config.get_config()['mixers'])
import json
file_path = 'output.json'
# Open the file in write mode and use json.dump() to export the dictionary to JSON
with open(file_path, 'w') as json_file:
    json.dump(config_obj.get_config(), json_file, indent=2)

spec.export_spec(spec_loca)
config_obj.export_config(config_loca)