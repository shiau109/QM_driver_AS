from QM_config_dynamic import QM_config, Circuit_info
from qualang_tools.units import unit

u = unit(coerce_to_integer=True)

myConfig = QM_config()
# myConfig.set_wiring("con1")
# mRO_common = {
#         "I":("con1",1),
#         "Q":("con1",2),
#         "freq_LO": 5.9, # GHz
#         "mixer": "octave_octave1_1",
#         "time_of_flight": 288, # ns
#         "integration_time": 2000, # ns
#     }
# mRO_individual = [
#     {
#         "name":"rr1", 
#         "freq_RO": int( 5.9-0.158036 ), # GHz
#         "amp": 0.008, # V
#     }
# ]
# myConfig.create_multiplex_readout_channel(mRO_common, mRO_individual )

the_spec = Circuit_info(q_num=4)
# ''' Update z '''
# z1 = the_spec.update_ZInfo_for(target_q='q1',con_channel=5,offset=0,OFFbias=0,idle=0)
# z2 = the_spec.update_ZInfo_for(target_q='q2',con_channel=6,offset=0,OFFbias=0,idle=0)
# z3 = the_spec.update_ZInfo_for(target_q='q3',con_channel=9,offset=0.211,OFFbias=0,idle=0)
# z4 = the_spec.update_ZInfo_for(target_q='q4',con_channel=10,offset=0,OFFbias=0,idle=0)

# ''' Update the xy '''
# the_spec.update_aXyInfo_for("q1",func='gauss')
# the_spec.update_aXyInfo_for("q2",func='gauss')
# the_spec.update_aXyInfo_for("q3",func='gauss')
# the_spec.update_aXyInfo_for("q4",func='gauss')

# the_spec.update_XyInfoS_for("q1",[0.1 * 0.985 * 0.94 *0.935,40,3.955,-80,0,-200,0])
# the_spec.update_XyInfoS_for("q2",[0.1 * 0.425,40,4.215,-82.05-5.93+7+3.45-0.7+0.55,0,-200,0])

# ''' Update the T1 and T2 for q1 and q2 in the spec '''
# the_spec.update_DecoInfo_for(target_q="q1",T1=5,T2=3)
# the_spec.update_DecoInfo_for(target_q="q2",T1=5,T2=3)

# the_spec.export_spec("spec_v1113")
the_spec.import_spec("exp/allXY/spec_v1113")
print(the_spec.spec)

# xy_wiring = [
#     {
#         "name":"q1",
#         "I":("con1", 3),
#         "Q":("con1", 4),
#         "mixer": "octave_octave1_2"
#     },
#     {
#         "name":"q2",
#         "I":("con1", 7),
#         "Q":("con1", 8),
#         "mixer": "octave_octave1_4"
#     }
# ]

# myConfig.create_element_xy(xy_wiring, the_spec.spec["XyInfo"])

# ''' update z bias in config '''
# myConfig.update_z_offset(Zinfo=z1,control_mache="con1",mode='offset')
# myConfig.update_z_offset(Zinfo=z2,control_mache="con1",mode='offset')
# myConfig.update_z_offset(Zinfo=z3,control_mache="con1",mode='offset')
# myConfig.update_z_offset(Zinfo=z4,control_mache="con1",mode='offset')

myConfig.import_config("exp/allXY/config_v1113")
# print(myConfig.get_config())