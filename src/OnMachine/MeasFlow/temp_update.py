from OnMachine.MeasFlow.ConfigBuildUp_new import spec_loca, config_loca
from config_component.configuration import import_config, configuration_read_dict
from config_component.channel_info import import_spec


spec = import_spec( spec_loca )
config_obj = import_config( config_loca )

from config_component.update import update_ReadoutFreqs, update_Readout
new_LO = 5.9
# init_value of readout amp is 0.2
# 0.065
cavities = [['q0',+110+7, 0.1*0.6*0.2],['q1',+155+5, 0.1*0.6*0.2]]
for i in cavities:
    f = spec.update_RoInfo_for(target_q=i[0],LO=new_LO,IF=i[1])
    print(f)
    update_ReadoutFreqs(config_obj, f)
    spec.update_RoInfo_for(i[0],amp=i[2])
    update_Readout(config_obj, i[0], spec.get_spec_forConfig('ro'))
    config_dict = config_obj.get_config() 

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