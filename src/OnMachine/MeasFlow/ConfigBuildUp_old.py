
from OnMachine.Octave_Config.QM_config_dynamic import Circuit_info, QM_config
import os
SpecConfig_path = os.getcwd()+'/config/'
########### For other import ################
config_loca = SpecConfig_path+"DR4_config" #
spec_loca = SpecConfig_path+"DR4_spec"     #
qubit_num = 3                               #
#############################################
specs = Circuit_info(qubit_num)
config = QM_config()

cluster_name = "QPX_4"  # Write your cluster_name if version >= QOP220
qop_ip = "192.168.50.126"  # Write the QM router IP address
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
# Update the wiring info
specs.update_WireInfo_for("q1",ro_mixer='octave_octave1_1',xy_mixer='octave_octave1_2',up_I=("con1", 1),up_Q=("con1", 2),down_I=("con1", 1),down_Q=("con1", 2),xy_I=("con1", 3),xy_Q=("con1", 4))
specs.update_WireInfo_for("q2",ro_mixer='octave_octave1_1',xy_mixer='octave_octave1_3',up_I=("con1", 1),up_Q=("con1", 2),down_I=("con1", 1),down_Q=("con1", 2),xy_I=("con1", 7),xy_Q=("con1", 8))
specs.update_WireInfo_for("q3",ro_mixer='octave_octave1_1',xy_mixer='octave_octave1_4',up_I=("con1", 1),up_Q=("con1", 2),down_I=("con1", 1),down_Q=("con1", 2),xy_I=("con1", 7),xy_Q=("con1", 8))
specs.update_WireInfo_for("q4",ro_mixer='octave_octave1_1',xy_mixer='octave_octave1_5',up_I=("con1", 1),up_Q=("con1", 2),down_I=("con1", 1),down_Q=("con1", 2),xy_I=("con1", 7),xy_Q=("con1", 8))

# wiring
specs.update_HardwareInfo(qop_ip=qop_ip, qop_port=qop_port, octave_port=11250, cluster_name=cluster_name, ctrl_name=("octave1","con1"), port_map=port_mapping, clock="Internal")
# Inntialize the controller
config.set_wiring("con1")
# Update z 
z1 = specs.update_ZInfo_for(target_q='q1',controller='con1',con_channel=5,offset=0,OFFbias=0,idle=0)
z2 = specs.update_ZInfo_for(target_q='q2',controller='con1',con_channel=6,offset=0,OFFbias=0,idle=0)
z3 = specs.update_ZInfo_for(target_q='q3',controller='con1',con_channel=9,offset=0,OFFbias=0,idle=0)
z4 = specs.update_ZInfo_for(target_q='q4',controller='con1',con_channel=10,offset=0,OFFbias=0,idle=0)

# Update the z bias into the controller
config.update_z_offset(Zinfo=z1,mode='offset')
config.update_z_offset(Zinfo=z2,mode='offset')
config.update_z_offset(Zinfo=z3,mode='offset')
config.update_z_offset(Zinfo=z4,mode='offset')

# Create the XY and RO channels for a qubit
config.create_qubit("q1",specs.get_spec_forConfig('ro'),specs.get_spec_forConfig('xy'),specs.get_spec_forConfig('wire'),specs.get_spec_forConfig('z'))
config.create_qubit("q2",specs.get_spec_forConfig('ro'),specs.get_spec_forConfig('xy'),specs.get_spec_forConfig('wire'),specs.get_spec_forConfig('z'))
config.create_qubit("q3",specs.get_spec_forConfig('ro'),specs.get_spec_forConfig('xy'),specs.get_spec_forConfig('wire'),specs.get_spec_forConfig('z'))
config.create_qubit("q4",specs.get_spec_forConfig('ro'),specs.get_spec_forConfig('xy'),specs.get_spec_forConfig('wire'),specs.get_spec_forConfig('z'))

# update RO integration weights
config.update_integrationWeight(target_q='q1',updated_RO_spec=specs.get_spec_forConfig('ro'),from_which_value='rotated')
config.update_integrationWeight(target_q='q2',updated_RO_spec=specs.get_spec_forConfig('ro'),from_which_value='rotated')
config.update_integrationWeight(target_q='q3',updated_RO_spec=specs.get_spec_forConfig('ro'),from_which_value='rotated')
config.update_integrationWeight(target_q='q4',updated_RO_spec=specs.get_spec_forConfig('ro'),from_which_value='rotated')

# update the downconvertion in the controller
config.update_downconverter(channel=1,offset=0, gain_db=0)
config.update_downconverter(channel=2,offset=0, gain_db=0)



if __name__ == '__main__':
    specs.export_spec(spec_loca)
    config.export_config(config_loca)

