from QM_config_dynamic import QM_config, Circuit_info
from qualang_tools.units import unit

u = unit(coerce_to_integer=True)

myConfig = QM_config()
the_spec = Circuit_info(q_num=4)
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


# ''' Update z '''
# z1 = the_spec.update_ZInfo_for(target_q='q1',con_channel=5,offset=0,OFFbias=0.016,idle=0)
# z2 = the_spec.update_ZInfo_for(target_q='q2',con_channel=6,offset=0,OFFbias=-0.141,idle=0)
# z3 = the_spec.update_ZInfo_for(target_q='q3',con_channel=9,offset=0.211,OFFbias=0,idle=0.1431)
# z4 = the_spec.update_ZInfo_for(target_q='q4',con_channel=10,offset=0.217,OFFbias=0,idle=0)

# myConfig.update_z_offset(Zinfo=z1,control_mache="con1",mode='OFFbias')
# myConfig.update_z_offset(Zinfo=z2,control_mache="con1",mode='OFFbias')
# myConfig.update_z_offset(Zinfo=z3,control_mache="con1",mode='idle')
# myConfig.update_z_offset(Zinfo=z4,control_mache="con1",mode='offset')

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


# the_spec.update_XyInfoS_for("q3",[0.046,40,3.955-0.201-0.072,-80+34.7+24.1+13.6-2.31,0,-200,0])
# the_spec.update_XyInfoS_for("q4",[0.0575,40,4.385,-80-15.1+24.1-1,0,-200,0])

# xy_wiring = [
#     {
#         "name":"q3",
#         "I":("con1", 3),
#         "Q":("con1", 4),
#         "mixer": "octave_octave1_3"
#     },
#     {
#         "name":"q4",
#         "I":("con1", 7),
#         "Q":("con1", 8),
#         "mixer": "octave_octave1_5"
#     }
# ]

# myConfig.create_element_xy(xy_wiring, the_spec.QsXyInfo)

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
#         "name":"rr3", 
#         "freq_IF": -45.468 , # MHz
#         "amp": 0.015, # V
#     }
# ]
# myConfig.create_multiplex_readout_channel(mRO_common, mRO_individual )
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
#         "name":"rr4", 
#         "freq_IF": 225.425 , # MHz
#         "amp": 0.012, # V
#     }
# ]
# myConfig.create_multiplex_readout_channel(mRO_common, mRO_individual )
# the_spec.export_spec("exp/allXY/spec_v1114")
# myConfig.export_config("exp/allXY/config_v1114")