from QM_config_dynamic import QM_config, Circuit_info
from qualang_tools.units import unit
from numpy import pi

u = unit(coerce_to_integer=True)

myConfig = QM_config()
the_spec = Circuit_info(q_num=4)
choose = 1

# initialize the dynamic configuration
if choose == 0: 
    # Update z 
    z1 = the_spec.update_ZInfo_for(target_q='q1',controller='con1',con_channel=5,offset=0,OFFbias=0.016,idle=0)
    z2 = the_spec.update_ZInfo_for(target_q='q2',controller='con1',con_channel=6,offset=0,OFFbias=-0.141,idle=0)
    z3 = the_spec.update_ZInfo_for(target_q='q3',controller='con1',con_channel=9,offset=0.211,OFFbias=0,idle=0.1431)
    z4 = the_spec.update_ZInfo_for(target_q='q4',controller='con1',con_channel=10,offset=0.217,OFFbias=0,idle=0)

    # Update the xy 
    the_spec.update_aXyInfo_for("q1",func='gauss')
    the_spec.update_aXyInfo_for("q2",func='gauss')
    the_spec.update_aXyInfo_for("q3",func='gauss')
    the_spec.update_aXyInfo_for("q4",func='gauss')

    # Update the T1 and T2 for q1 and q2 in the spec (if needed)
    # the_spec.update_DecoInfo_for(target_q="q1",T1=5,T2=3)
    # the_spec.update_DecoInfo_for(target_q="q2",T1=5,T2=3)

    # Update XY info
    the_spec.update_XyInfoS_for("q1",[0.046,40,3.955-0.201-0.072,-80+34.7+24.1+13.6-2.31,0,-200,0])
    the_spec.update_XyInfoS_for("q2",[0.0575,40,4.385,-80-15.1+24.1-1,0,-200,0])
    the_spec.update_XyInfoS_for("q3",[0.046,40,3.955-0.201-0.072,-80+34.7+24.1+13.6-2.31,0,-200,0])
    the_spec.update_XyInfoS_for("q4",[0.0575,40,4.385,-80-15.1+24.1-1,0,-200,0])

    # Update RO info
    the_spec.update_RoInfo_for("q1",LO=5.9,IF= -158.112,amp=0.006,time=288,len=2000, ge_hold=0.000909, rotated=(148.6 / 180)*pi)
    the_spec.update_RoInfo_for("q2",LO=5.9,IF= 129.397,amp=0.0095, ge_hold=0.000229, rotated=(45.9 / 180)*pi)
    the_spec.update_RoInfo_for("q3",LO=6.4,IF= -45.468,amp=0.015, ge_hold=0, rotated=(0 / 180)*pi)
    the_spec.update_RoInfo_for("q4",LO=6.4,IF= 225.425,amp=0.012, ge_hold=2.419e-04, rotated=(0 / 180)*pi)

    # Update the wiring info
    the_spec.update_WireInfo_for("q1",ro_mixer='octave_octave1_1',xy_mixer='octave_octave1_2',up_I=("con1", 1),up_Q=("con1", 2),down_I=("con1", 1),down_Q=("con1", 2),xy_I=("con1", 3),xy_Q=("con1", 4))
    the_spec.update_WireInfo_for("q2",ro_mixer='octave_octave1_1',xy_mixer='octave_octave1_4',up_I=("con1", 1),up_Q=("con1", 2),down_I=("con1", 1),down_Q=("con1", 2),xy_I=("con1", 7),xy_Q=("con1", 8))
    the_spec.update_WireInfo_for("q3",ro_mixer='octave_octave1_1',xy_mixer='octave_octave1_3',up_I=("con1", 1),up_Q=("con1", 2),down_I=("con1", 1),down_Q=("con1", 2),xy_I=("con1", 3),xy_Q=("con1", 4))
    the_spec.update_WireInfo_for("q4",ro_mixer='octave_octave1_1',xy_mixer='octave_octave1_5',up_I=("con1", 1),up_Q=("con1", 2),down_I=("con1", 1),down_Q=("con1", 2),xy_I=("con1", 7),xy_Q=("con1", 8))

    # Inntialize the controller
    myConfig.set_wiring("con1")

    # Update the z bias into the controller
    myConfig.update_z_offset(Zinfo=z1,mode='OFFbias')
    myConfig.update_z_offset(Zinfo=z2,mode='OFFbias')
    myConfig.update_z_offset(Zinfo=z3,mode='idle')
    myConfig.update_z_offset(Zinfo=z4,mode='offset')

    # Create the XY and RO channels for a qubit
    myConfig.create_qubit("q1",the_spec.RoInfo,the_spec.XyInfo,the_spec.WireInfo)
    myConfig.create_qubit("q2",the_spec.RoInfo,the_spec.XyInfo,the_spec.WireInfo)
    myConfig.create_qubit("q3",the_spec.RoInfo,the_spec.XyInfo,the_spec.WireInfo)
    myConfig.create_qubit("q4",the_spec.RoInfo,the_spec.XyInfo,the_spec.WireInfo)

    # update RO integration weights
    myConfig.update_integrationWeight(target_q='q1',updated_RO_spec=the_spec.RoInfo,from_which_value='rotated')
    myConfig.update_integrationWeight(target_q='q2',updated_RO_spec=the_spec.RoInfo,from_which_value='rotated')

    # update the downconvertion in the controller
    myConfig.update_downconverter(channel=1,offset= 0.0156584060058594, gain_db= 0)
    myConfig.update_downconverter(channel=2,offset= 0.00627351550292969, gain_db= 0)

    the_spec.export_spec("TESTspec_1128")
    myConfig.export_config("TESTconfig_1128")

else:
    the_spec.import_spec("TESTspec_1128")
    myConfig.import_config("TESTconfig_1128")

    # print(myConfig.get_config()['pulses'])
    ### for some useful update

    # Update the controll mixer corections
    myConfig.update_mixer_correction(target_q='q1',correct=(0.995,0.002,0.015,0.989),mode='xy')

    # Update the control frequency like IF or LO
    myConfig.update_controlFreq(the_spec.update_aXyInfo_for("q2",LO=5.5,IF=2000))

    # Update the pi pulse amp or len...
    the_spec.update_aXyInfo_for("q1",amp=0.34,len=33)
    myConfig.update_controlWaveform(the_spec.XyInfo)

    # Update the RO frequency
    myConfig.update_ReadoutFreqs(the_spec.update_RoInfo_for(target_q='q2',IF=280))
    myConfig.update_ReadoutFreqs(the_spec.update_RoInfo_for(target_q='q2',LO=7))

    # Update the RO amp or others
    the_spec.update_RoInfo_for(target_q='q2',amp=0.01,ge_hold=0.02)
    the_spec.update_RoInfo_for(target_q='q1',rotated=0.087)
    the_spec.update_RoInfo_for(target_q='AnyQ',len=2500,time=700)
    myConfig.update_Readout(RoInfo=the_spec.RoInfo,integration_weights_from='rotated')
    
    # Update the RO mixer corections
    myConfig.update_mixer_correction(target_q='q2',correct=(0.995,0.002,0.015,0.989),mode='ro')

    # Update the RO wiring channels
    myConfig.update_wiring_channels(target_q="q1",mode="ro",I=("con1",100),Q=("con1",999))

    print(myConfig.get_config())
