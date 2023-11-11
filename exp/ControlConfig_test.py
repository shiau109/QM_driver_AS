from QM_config_dynamic import QM_config, Circuit_info

the_specs = Circuit_info(q_num=2)
# print(the_specs.QsXyInfo)
# test update q1 waveform func to drag
the_specs.update_aXyInfo_for("q1",func='drag')
the_specs.update_aXyInfo_for("q2",func='gauss')
# print("\nUpdate q1 waveform func:\n")
# print(the_specs.QsXyInfo)
# test update all the values for q1
the_specs.update_XyInfoS_for("q1",[0.2,20,4,-80,-0.5,-200,5])
the_specs.update_XyInfoS_for("q2",[0.14,20,4,120,-0.5,-200,5])
# print("\nUpdate q1 pi pulse info:\n")
# print(the_specs.QsXyInfo)

init_config = QM_config()
print("initial config:\n")
print(init_config.get_config())

wiring = [
    {
        "name":"q1",
        "I":("con1", 1),
        "Q":("con1", 2),
        "mixer": "octave_octave1_1"
    },
    {
        "name":"q2",
        "I":("con1", 3),
        "Q":("con1", 4),
        "mixer": "octave_octave1_2"
    }
]
x = the_specs.QsXyInfo
init_config.init_xy_element_xy_element(wiring, x)
# print("\nAfter updating control elements:\n")
# print(init_config.get_config())
init_config.update_control_channels("q1",I=("con2",5),Q=("con2",7))
init_config.update_control_mixer_correction("q2",(0.9,0.2,0.4,-0.9))
# print("\nAfter updating mixer corrections and channels:\n")
# print(init_config.get_config())

the_specs.update_aXyInfo_for("q2",LO=5.5,IF=2000)
x = the_specs.QsXyInfo
print(x)
print("\nAfter updating q2 freq:\n")
print(init_config.get_config())