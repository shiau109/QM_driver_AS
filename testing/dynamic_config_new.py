import matplotlib.pyplot as plt
from config_component.configuration import Configuration, configuration_read_dict
# from config_component.controller import Controller
# myConfig = Configuration()

import json
"""
# Specify the path to the JSON file
json_file_path = r'testing/OPXp_config_test.json'

# Open the file and load JSON data into a dictionary
with open(json_file_path, 'r') as json_file:
    data_dict = json.load(json_file)

# Print the resulting dictionary
# print(data_dict)
new_config = configuration_read_dict(data_dict)
# myConfig.controllers["con1"] = Controller("con1")
"""
from config_component.channel_info import ChannelInfo
specs = ChannelInfo(1)


new_config = Configuration()
new_config.create_qubit("q1",specs.get_spec_forConfig('ro'),specs.get_spec_forConfig('xy'),specs.get_spec_forConfig('wire'),specs.get_spec_forConfig('z'))


import json
file_path = 'output.json'
# Open the file in write mode and use json.dump() to export the dictionary to JSON
with open(file_path, 'w') as json_file:
    json.dump(new_config.get_config(), json_file, indent=2)

# print(new_config.controllers["con1"].analog_outputs[1].offset)
# for k1, v1 in new_config.elements.items():
#     print(f"element {k1}")
#     for k2, v2 in v1.to_dict()[k1].items():
#         print(k2)

# for k1, v1 in new_config.pulses.items():
#     print(f"pulse {k1}, {v1}")
#     for k2, v2 in v1.to_dict()[k1].items():
#         print(k2)

# for k1, v1 in new_config.waveforms.items():
#     print(f"waveform {k1}")
#     for k2, v2 in v1.to_dict()[k1].items():
#         print(v2)

# for k1, v1 in new_config.integration_weights.items():
#     print(f"integration_weight {k1}")
#     for k2, v2 in v1.to_dict()[k1].items():
#         print(k2)

# for k1, v1 in new_config.mixers.items():
#     print(f"mixer {k1}")
#     for v2 in v1.to_dict():
#         print(v2)
