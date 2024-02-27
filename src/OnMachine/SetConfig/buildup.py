


qubit_num = 9   

specs = ChannelInfo(qubit_num)
specs.update_HardwareInfo(qop_ip=qop_ip, qop_port=qop_port, octave_port=11250, cluster_name=cluster_name, ctrl_name=("octave1","con1"), port_map=port_mapping, clock="Internal")

config = Configuration()
opxp_hardware = {
    "analog_outputs": {
        1: {"offset": 0.0},  # I readout line
        2: {"offset": 0.0},  # Q readout line
        3: {"offset": 0.0},  # I qubit1 XY
        4: {"offset": 0.0},  # Q qubit1 XY
        5: {"offset": 0.0},  # I qubit2 XY
        6: {"offset": 0.0},  # Q qubit2 XY
        7: {"offset": 0.0},  # I qubit3 XY
        8: {"offset": 0.0},  # Q qubit3 XY
        9: {"offset": 0.0},  # I qubit4 XY
        10: {"offset": 0.0},  # Q qubit4 XY
    },
    "digital_outputs": {
        1: {},
        3: {},
        5: {},
        7: {},
        9: {},
    },
    "analog_inputs": {
        1: {"offset": 0, "gain_db": 0},  # I from down-conversion
        2: {"offset": 0, "gain_db": 0},  # Q from down-conversion
    },
}
from config_component.controller import controller_read_dict
config._controllers["con1"] = controller_read_dict("con1", opxp_hardware)

from config_component.construct import create_qubit, create_roChannel, create_zChannel, create_xyChannel
# create_qubit( config,"q1",specs.get_spec_forConfig('ro'),specs.get_spec_forConfig('xy'),specs.get_spec_forConfig('wire'),specs.get_spec_forConfig('z'))

specs.update_WireInfo_for("q1",xy_I=('con1',9),xy_Q=('con1',10))
for q_i, z_port in enumerate( [3,4,5,6,7,8,9,10,3] ):
    q_name = f"q{q_i}"
    specs.update_WireInfo_for(q_name,z=("con1",z_port))
    create_roChannel( config, f"{q_name}_ro", specs.get_spec_forConfig('ro')[q_name],specs.get_spec_forConfig('wire')[q_name] )
    create_xyChannel( config, f"{q_name}_xy", specs.get_spec_forConfig('xy')[q_name],specs.get_spec_forConfig('wire')[q_name] )
    create_zChannel( config, f"{q_name}_z", specs.get_spec_forConfig('z')[q_name],specs.get_spec_forConfig('wire')[q_name] )

# for q_i, z_port in enumerate( [8,9,10,3] ):
#     dq_name = f"q{q_i+5}"
#     q_name = f"c{q_i+5}"
#     specs.update_WireInfo_for(dq_name,z=("con1",z_port))
#     create_zChannel( config, f"{q_name}_z", specs.get_spec_forConfig('z')["q0"],specs.get_spec_forConfig('wire')[dq_name] )

specs.export_spec(spec_loca)
config.export_config(config_loca)

import json
file_path = 'output.json'
# Open the file in write mode and use json.dump() to export the dictionary to JSON
with open(file_path, 'w') as json_file:
    json.dump(config.get_config(), json_file, indent=2)