from OnMachine.SetConfig.config_path import *

cluster_name = "Cluster_1"  # Write your cluster_name if version >= QOP220
qop_ip = "192.168.50.91"  # Write the QM router IP address
qop_port = None 

# Default
port_mapping = {
("con1", 1): ("octave1", "I1"),
("con1", 2): ("octave1", "Q1"),
("con1", 3): ("octave1", "I2"),
("con1", 4): ("octave1", "Q2"),
("con1", 5): ("octave1", "I3"),
("con1", 6): ("octave1", "Q3"),
("con1", 7): ("octave1", "I4"),
("con1", 8): ("octave1", "Q4"),
("con1", 9): ("octave1", "I5"),
("con1", 10): ("octave1", "Q5"),

("con2", 1): ("octave2", "I1"),
("con2", 2): ("octave2", "Q1"),
("con2", 3): ("octave2", "I2"),
("con2", 4): ("octave2", "Q2"),
("con2", 5): ("octave2", "I3"),
("con2", 6): ("octave2", "Q3"),
("con2", 7): ("octave2", "I4"),
("con2", 8): ("octave2", "Q4"),
("con2", 9): ("octave2", "I5"),
("con2", 10): ("octave2", "Q5"),
}

qubit_num = 9

specs = ChannelInfo(qubit_num)

# Set QMM
specs.update_HardwareInfo(qop_ip=qop_ip, qop_port=qop_port, cluster_name=cluster_name)
# Set Octave
specs.update_octave( "octave1", ip=qop_ip, port=11250, con="con1", port_map=port_mapping, clock="External_1000MHz")
specs.update_octave( "octave2", ip=qop_ip, port=11249, con="con2", port_map=port_mapping, clock="External_1000MHz")

# Only for opx+
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

config = Configuration()

# Create controller
from config_component.controller import controller_read_dict
config._controllers["con1"] = controller_read_dict("con1", opxp_hardware)
config._controllers["con2"] = controller_read_dict("con2", opxp_hardware)
# Create qubit
from config_component.construct import create_qubit, create_roChannel, create_zChannel, create_xyChannel

for x_wire in [("q1",("con1",7),("con1",8)), ("q2",("con2",1),("con2",2)), ("q3",("con2",3),("con2",4)), ("q4",("con2",7),("con2",8)), ("q7",("con2",1),("con2",2))]:
    specs.update_WireInfo_for(x_wire[0],xy_I=x_wire[1],xy_Q=x_wire[2])

for z_wire in [("q0",("con1",5)), ("q1",("con1",6)), ("q2",("con1",9)), ("q3",("con1",10)), ("q4",("con2",5))]:
    specs.update_WireInfo_for(z_wire[0],z=z_wire[1])

for z_wire in [("q5",("con2",6)), ("q6",("con2",9)), ("q7",("con2",10)), ("q8",("con1",4))]:
    specs.update_WireInfo_for(z_wire[0],z=z_wire[1])

for q_idx in range(qubit_num):
    q_name = f"q{q_idx}"
    create_qubit( config,q_name,specs.get_spec_forConfig('ro'),specs.get_spec_forConfig('xy'),specs.get_spec_forConfig('wire'),specs.get_spec_forConfig('z'))

#     create_roChannel( config, f"{q_name}_ro", specs.get_spec_forConfig('ro')[q_name],specs.get_spec_forConfig('wire')[q_name] )
#     create_xyChannel( config, f"{q_name}_xy", specs.get_spec_forConfig('xy')[q_name],specs.get_spec_forConfig('wire')[q_name] )
#     create_zChannel( config, f"{q_name}_z", specs.get_spec_forConfig('z')[q_name],specs.get_spec_forConfig('wire')[q_name] )

specs.export_spec(spec_loca)
config.export_config(config_loca)

import json
file_path = 'output.json'
# Open the file in write mode and use json.dump() to export the dictionary to JSON
with open(file_path, 'w') as json_file:
    json.dump(config.get_config(), json_file, indent=2)