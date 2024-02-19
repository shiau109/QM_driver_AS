
from config_component.channel_info import ChannelInfo
from config_component.configuration import Configuration
from config_component.construct import create_qubit
import os
SpecConfig_path = os.getcwd()+'/config/'
########### For other import ################
config_loca = SpecConfig_path+"DR2b_discharge_config" #
spec_loca = SpecConfig_path+"DR2b_discharge_spec"     #
#############################################

cluster_name = "QPX_2"  # Write your cluster_name if version >= QOP220
qop_ip = "192.168.1.105"  # Write the QM router IP address
qop_port = None 
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
}

if __name__ == '__main__':
    qubit_num = 1   

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
    create_qubit(config,"q1",specs.get_spec_forConfig('ro'),specs.get_spec_forConfig('xy'),specs.get_spec_forConfig('wire'),specs.get_spec_forConfig('z'))
    

    specs.export_spec(spec_loca)
    config.export_config(config_loca)

    import json
    file_path = 'output.json'
    # Open the file in write mode and use json.dump() to export the dictionary to JSON
    with open(file_path, 'w') as json_file:
        json.dump(config.get_config(), json_file, indent=2)