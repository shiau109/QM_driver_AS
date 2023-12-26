
# Single QUA script generated at 2023-12-22 15:01:30.925076
# QUA library version: 1.1.3

from qm.qua import *

with program() as prog:
    v1 = declare(int, )
    v2 = declare(int, )
    v3 = declare(int, )
    v4 = declare(int, )
    v5 = declare(int, )
    v6 = declare(int, )
    input_stream___gates_len_is__ = declare_input_stream(int, '__gates_len_is__', size=1)
    input_stream_q3_xy_is = declare_input_stream(int, 'q3_xy_is', size=4096)
    input_stream_q2_z_is = declare_input_stream(int, 'q2_z_is', size=4096)
    input_stream_q2_xy_is = declare_input_stream(int, 'q2_xy_is', size=4096)
    a1 = declare(int, value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    v7 = declare(int, )
    v8 = declare(int, )
    v9 = declare(int, )
    v10 = declare(fixed, )
    v11 = declare(fixed, )
    v12 = declare(fixed, )
    v13 = declare(fixed, )
    v14 = declare(bool, )
    v15 = declare(bool, )
    assign(v6, 0)
    with for_each_((v1),(a1)):
        with for_(v2,0,(v2<20),(v2+1)):
            assign(v6, (v6+1))
            r1 = declare_stream()
            save(v6, r1)
            advance_input_stream(input_stream___gates_len_is__)
            advance_input_stream(input_stream_q3_xy_is)
            advance_input_stream(input_stream_q2_z_is)
            advance_input_stream(input_stream_q2_xy_is)
            assign(v5, input_stream___gates_len_is__[0])
            with for_(v3,0,(v3<2000),(v3+1)):
                wait(4, )
                align()
                align()
                with for_(v7,0,(v7<v5),(v7+1)):
                    with if_((input_stream_q3_xy_is[v7]==0), unsafe=True):
                        play("baked_Op_0", "q3_xy")
                    with elif_((input_stream_q3_xy_is[v7]==1)):
                        play("baked_Op_6", "q3_xy")
                        frame_rotation_2pi(0.15410555555555555, "q3_xy")
                    with elif_((input_stream_q3_xy_is[v7]==2)):
                        play("baked_Op_24", "q3_xy")
                        frame_rotation_2pi(0.3082111111111111, "q3_xy")
                    with elif_((input_stream_q3_xy_is[v7]==3)):
                        play("baked_Op_42", "q3_xy")
                        frame_rotation_2pi(0.46231666666666665, "q3_xy")
                with for_(v8,0,(v8<v5),(v8+1)):
                    with if_((input_stream_q2_z_is[v8]==0), unsafe=True):
                        play("baked_Op_0", "q2_z")
                    with elif_((input_stream_q2_z_is[v8]==1)):
                        play("baked_Op_6", "q2_z")
                    with elif_((input_stream_q2_z_is[v8]==2)):
                        play("baked_Op_24", "q2_z")
                    with elif_((input_stream_q2_z_is[v8]==3)):
                        play("baked_Op_42", "q2_z")
                with for_(v9,0,(v9<v5),(v9+1)):
                    with if_((input_stream_q2_xy_is[v9]==0), unsafe=True):
                        play("baked_Op_0", "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==1)):
                        play("baked_Op_1", "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==2)):
                        play("baked_Op_2", "q2_xy")
                        frame_rotation_2pi(1.0, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==3)):
                        play("baked_Op_3", "q2_xy")
                        frame_rotation_2pi(-0.5, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==4)):
                        play("baked_Op_4", "q2_xy")
                        frame_rotation_2pi(0.5, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==5)):
                        play("baked_Op_5", "q2_xy")
                        frame_rotation_2pi(0.5, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==6)):
                        play("baked_Op_6", "q2_xy")
                        frame_rotation_2pi(0.068175, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==7)):
                        play("baked_Op_7", "q2_xy")
                        frame_rotation_2pi(0.568175, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==8)):
                        play("baked_Op_8", "q2_xy")
                        frame_rotation_2pi(-0.43182499999999996, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==9)):
                        play("baked_Op_9", "q2_xy")
                        frame_rotation_2pi(0.068175, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==10)):
                        play("baked_Op_10", "q2_xy")
                        frame_rotation_2pi(0.568175, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==11)):
                        play("baked_Op_11", "q2_xy")
                        frame_rotation_2pi(-0.43182499999999996, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==12)):
                        play("baked_Op_12", "q2_xy")
                        frame_rotation_2pi(1.068175, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==13)):
                        play("baked_Op_13", "q2_xy")
                        frame_rotation_2pi(1.568175, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==14)):
                        play("baked_Op_14", "q2_xy")
                        frame_rotation_2pi(0.568175, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==15)):
                        play("baked_Op_15", "q2_xy")
                        frame_rotation_2pi(-0.43182499999999996, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==16)):
                        play("baked_Op_16", "q2_xy")
                        frame_rotation_2pi(0.06817500000000001, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==17)):
                        play("baked_Op_17", "q2_xy")
                        frame_rotation_2pi(-0.931825, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==18)):
                        play("baked_Op_18", "q2_xy")
                        frame_rotation_2pi(0.568175, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==19)):
                        play("baked_Op_19", "q2_xy")
                        frame_rotation_2pi(1.068175, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==20)):
                        play("baked_Op_20", "q2_xy")
                        frame_rotation_2pi(0.06817500000000001, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==21)):
                        play("baked_Op_21", "q2_xy")
                        frame_rotation_2pi(0.568175, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==22)):
                        play("baked_Op_22", "q2_xy")
                        frame_rotation_2pi(1.068175, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==23)):
                        play("baked_Op_23", "q2_xy")
                        frame_rotation_2pi(0.06817500000000001, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==24)):
                        play("baked_Op_24", "q2_xy")
                        frame_rotation_2pi(-0.36365, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==25)):
                        play("baked_Op_25", "q2_xy")
                        frame_rotation_2pi(-1.36365, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==26)):
                        play("baked_Op_26", "q2_xy")
                        frame_rotation_2pi(-0.8636499999999999, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==27)):
                        play("baked_Op_27", "q2_xy")
                        frame_rotation_2pi(0.13635000000000003, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==28)):
                        play("baked_Op_28", "q2_xy")
                        frame_rotation_2pi(-0.8636499999999999, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==29)):
                        play("baked_Op_29", "q2_xy")
                        frame_rotation_2pi(-0.36365, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==30)):
                        play("baked_Op_30", "q2_xy")
                        frame_rotation_2pi(0.1363500000000003, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==31)):
                        play("baked_Op_31", "q2_xy")
                        frame_rotation_2pi(-0.8636499999999998, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==32)):
                        play("baked_Op_32", "q2_xy")
                        frame_rotation_2pi(-0.3636499999999998, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==33)):
                        play("baked_Op_33", "q2_xy")
                        frame_rotation_2pi(0.13635000000000003, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==34)):
                        play("baked_Op_34", "q2_xy")
                        frame_rotation_2pi(-0.8636499999999999, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==35)):
                        play("baked_Op_35", "q2_xy")
                        frame_rotation_2pi(-0.36365, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==36)):
                        play("baked_Op_36", "q2_xy")
                        frame_rotation_2pi(-0.36365, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==37)):
                        play("baked_Op_37", "q2_xy")
                        frame_rotation_2pi(-1.36365, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==38)):
                        play("baked_Op_38", "q2_xy")
                        frame_rotation_2pi(-0.8636499999999999, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==39)):
                        play("baked_Op_39", "q2_xy")
                        frame_rotation_2pi(0.13635000000000003, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==40)):
                        play("baked_Op_40", "q2_xy")
                        frame_rotation_2pi(-0.8636499999999999, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==41)):
                        play("baked_Op_41", "q2_xy")
                        frame_rotation_2pi(-0.36365, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==42)):
                        play("baked_Op_42", "q2_xy")
                        frame_rotation_2pi(-1.7954750000000002, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==43)):
                        play("baked_Op_43", "q2_xy")
                        frame_rotation_2pi(-1.7954750000000002, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==44)):
                        play("baked_Op_44", "q2_xy")
                        frame_rotation_2pi(-0.7954749999999998, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==45)):
                        play("baked_Op_45", "q2_xy")
                        frame_rotation_2pi(-2.295475, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==46)):
                        play("baked_Op_46", "q2_xy")
                        frame_rotation_2pi(-1.2954750000000002, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==47)):
                        play("baked_Op_47", "q2_xy")
                        frame_rotation_2pi(-1.2954750000000002, "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==48)):
                        play("baked_Op_48", "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==49)):
                        play("baked_Op_49", "q2_xy")
                    with elif_((input_stream_q2_xy_is[v9]==50)):
                        play("baked_Op_50", "q2_xy")
                        frame_rotation_2pi(1.0, "q2_xy")
                align()
                measure("readout"*amp(1.0), "rr2", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", v10), dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", v12))
                measure("readout"*amp(1.0), "rr3", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", v11), dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", v13))
                assign(v14, (v10>8.003e-05))
                assign(v15, (v11>-0.0003386))
                assign(v4, ((Cast.to_int(v15)<<1)+Cast.to_int(v14)))
                r2 = declare_stream()
                save(v4, r2)
    with stream_processing():
        r2.buffer(13, 20, 2000).save("state")
        r1.save("progress")


config = {
    "version": 1,
    "controllers": {
        "con1": {
            "analog_outputs": {
                "1": {
                    "offset": 0.0,
                },
                "2": {
                    "offset": 0.0,
                },
                "3": {
                    "offset": 0.0,
                },
                "4": {
                    "offset": 0.0,
                },
                "5": {
                    "offset": -0.34,
                },
                "6": {
                    "offset": -0.3529,
                },
                "7": {
                    "offset": 0.0,
                },
                "8": {
                    "offset": 0.0,
                },
                "9": {
                    "offset": -0.3421,
                },
                "10": {
                    "offset": -0.3433,
                },
            },
            "digital_outputs": {
                "1": {},
                "3": {},
                "5": {},
                "7": {},
                "10": {},
            },
            "analog_inputs": {
                "1": {
                    "offset": 0.014816313000633604,
                    "gain_db": 0,
                },
                "2": {
                    "offset": 0.013283161315917969,
                    "gain_db": 0,
                },
            },
        },
    },
    "elements": {
        "rr1": {
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "lo_frequency": 5950000000,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": -214210000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q1",
            },
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 200,
            "smearing": 0,
        },
        "rr2": {
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "lo_frequency": 5950000000,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": 75079000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q2",
            },
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 200,
            "smearing": 0,
        },
        "rr3": {
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "lo_frequency": 5950000000,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": -103970000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q3",
            },
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 200,
            "smearing": 0,
        },
        "rr4": {
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "lo_frequency": 5950000000,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": 163060000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q4",
            },
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 200,
            "smearing": 0,
        },
        "rr5": {
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "lo_frequency": 5950000000,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": -25800000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q5",
            },
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 200,
            "smearing": 0,
        },
        "q1_xy": {
            "mixInputs": {
                "I": ('con1', 3),
                "Q": ('con1', 4),
                "lo_frequency": 4055000000.0,
                "mixer": "octave_octave1_2",
            },
            "intermediate_frequency": -116555000.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q1",
                "x90": "x90_pulse_q1",
                "-x90": "-x90_pulse_q1",
                "y90": "y90_pulse_q1",
                "y180": "y180_pulse_q1",
                "-y90": "-y90_pulse_q1",
            },
        },
        "q2_xy": {
            "mixInputs": {
                "I": ('con1', 7),
                "Q": ('con1', 8),
                "lo_frequency": 4300000000.0,
                "mixer": "octave_octave1_4",
            },
            "intermediate_frequency": -101584000.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q2",
                "x90": "x90_pulse_q2",
                "-x90": "-x90_pulse_q2",
                "y90": "y90_pulse_q2",
                "y180": "y180_pulse_q2",
                "-y90": "-y90_pulse_q2",
                "baked_Op_0": "q2_xy_baked_pulse_0",
                "baked_Op_1": "q2_xy_baked_pulse_1",
                "baked_Op_2": "q2_xy_baked_pulse_2",
                "baked_Op_3": "q2_xy_baked_pulse_3",
                "baked_Op_4": "q2_xy_baked_pulse_4",
                "baked_Op_5": "q2_xy_baked_pulse_5",
                "baked_Op_6": "q2_xy_baked_pulse_6",
                "baked_Op_7": "q2_xy_baked_pulse_7",
                "baked_Op_8": "q2_xy_baked_pulse_8",
                "baked_Op_9": "q2_xy_baked_pulse_9",
                "baked_Op_10": "q2_xy_baked_pulse_10",
                "baked_Op_11": "q2_xy_baked_pulse_11",
                "baked_Op_12": "q2_xy_baked_pulse_12",
                "baked_Op_13": "q2_xy_baked_pulse_13",
                "baked_Op_14": "q2_xy_baked_pulse_14",
                "baked_Op_15": "q2_xy_baked_pulse_15",
                "baked_Op_16": "q2_xy_baked_pulse_16",
                "baked_Op_17": "q2_xy_baked_pulse_17",
                "baked_Op_18": "q2_xy_baked_pulse_18",
                "baked_Op_19": "q2_xy_baked_pulse_19",
                "baked_Op_20": "q2_xy_baked_pulse_20",
                "baked_Op_21": "q2_xy_baked_pulse_21",
                "baked_Op_22": "q2_xy_baked_pulse_22",
                "baked_Op_23": "q2_xy_baked_pulse_23",
                "baked_Op_24": "q2_xy_baked_pulse_24",
                "baked_Op_25": "q2_xy_baked_pulse_25",
                "baked_Op_26": "q2_xy_baked_pulse_26",
                "baked_Op_27": "q2_xy_baked_pulse_27",
                "baked_Op_28": "q2_xy_baked_pulse_28",
                "baked_Op_29": "q2_xy_baked_pulse_29",
                "baked_Op_30": "q2_xy_baked_pulse_30",
                "baked_Op_31": "q2_xy_baked_pulse_31",
                "baked_Op_32": "q2_xy_baked_pulse_32",
                "baked_Op_33": "q2_xy_baked_pulse_33",
                "baked_Op_34": "q2_xy_baked_pulse_34",
                "baked_Op_35": "q2_xy_baked_pulse_35",
                "baked_Op_36": "q2_xy_baked_pulse_36",
                "baked_Op_37": "q2_xy_baked_pulse_37",
                "baked_Op_38": "q2_xy_baked_pulse_38",
                "baked_Op_39": "q2_xy_baked_pulse_39",
                "baked_Op_40": "q2_xy_baked_pulse_40",
                "baked_Op_41": "q2_xy_baked_pulse_41",
                "baked_Op_42": "q2_xy_baked_pulse_42",
                "baked_Op_43": "q2_xy_baked_pulse_43",
                "baked_Op_44": "q2_xy_baked_pulse_44",
                "baked_Op_45": "q2_xy_baked_pulse_45",
                "baked_Op_46": "q2_xy_baked_pulse_46",
                "baked_Op_47": "q2_xy_baked_pulse_47",
                "baked_Op_48": "q2_xy_baked_pulse_48",
                "baked_Op_49": "q2_xy_baked_pulse_49",
                "baked_Op_50": "q2_xy_baked_pulse_50",
            },
        },
        "q3_xy": {
            "mixInputs": {
                "I": ('con1', 3),
                "Q": ('con1', 4),
                "lo_frequency": 3850000000.0,
                "mixer": "octave_octave1_3",
            },
            "intermediate_frequency": -317621000.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q3",
                "x90": "x90_pulse_q3",
                "-x90": "-x90_pulse_q3",
                "y90": "y90_pulse_q3",
                "y180": "y180_pulse_q3",
                "-y90": "-y90_pulse_q3",
                "baked_Op_0": "q3_xy_baked_pulse_0",
                "baked_Op_1": "q3_xy_baked_pulse_1",
                "baked_Op_2": "q3_xy_baked_pulse_2",
                "baked_Op_3": "q3_xy_baked_pulse_3",
                "baked_Op_4": "q3_xy_baked_pulse_4",
                "baked_Op_5": "q3_xy_baked_pulse_5",
                "baked_Op_6": "q3_xy_baked_pulse_6",
                "baked_Op_7": "q3_xy_baked_pulse_7",
                "baked_Op_8": "q3_xy_baked_pulse_8",
                "baked_Op_9": "q3_xy_baked_pulse_9",
                "baked_Op_10": "q3_xy_baked_pulse_10",
                "baked_Op_11": "q3_xy_baked_pulse_11",
                "baked_Op_12": "q3_xy_baked_pulse_12",
                "baked_Op_13": "q3_xy_baked_pulse_13",
                "baked_Op_14": "q3_xy_baked_pulse_14",
                "baked_Op_15": "q3_xy_baked_pulse_15",
                "baked_Op_16": "q3_xy_baked_pulse_16",
                "baked_Op_17": "q3_xy_baked_pulse_17",
                "baked_Op_18": "q3_xy_baked_pulse_18",
                "baked_Op_19": "q3_xy_baked_pulse_19",
                "baked_Op_20": "q3_xy_baked_pulse_20",
                "baked_Op_21": "q3_xy_baked_pulse_21",
                "baked_Op_22": "q3_xy_baked_pulse_22",
                "baked_Op_23": "q3_xy_baked_pulse_23",
                "baked_Op_24": "q3_xy_baked_pulse_24",
                "baked_Op_25": "q3_xy_baked_pulse_25",
                "baked_Op_26": "q3_xy_baked_pulse_26",
                "baked_Op_27": "q3_xy_baked_pulse_27",
                "baked_Op_28": "q3_xy_baked_pulse_28",
                "baked_Op_29": "q3_xy_baked_pulse_29",
                "baked_Op_30": "q3_xy_baked_pulse_30",
                "baked_Op_31": "q3_xy_baked_pulse_31",
                "baked_Op_32": "q3_xy_baked_pulse_32",
                "baked_Op_33": "q3_xy_baked_pulse_33",
                "baked_Op_34": "q3_xy_baked_pulse_34",
                "baked_Op_35": "q3_xy_baked_pulse_35",
                "baked_Op_36": "q3_xy_baked_pulse_36",
                "baked_Op_37": "q3_xy_baked_pulse_37",
                "baked_Op_38": "q3_xy_baked_pulse_38",
                "baked_Op_39": "q3_xy_baked_pulse_39",
                "baked_Op_40": "q3_xy_baked_pulse_40",
                "baked_Op_41": "q3_xy_baked_pulse_41",
                "baked_Op_42": "q3_xy_baked_pulse_42",
                "baked_Op_43": "q3_xy_baked_pulse_43",
                "baked_Op_44": "q3_xy_baked_pulse_44",
                "baked_Op_45": "q3_xy_baked_pulse_45",
                "baked_Op_46": "q3_xy_baked_pulse_46",
                "baked_Op_47": "q3_xy_baked_pulse_47",
                "baked_Op_48": "q3_xy_baked_pulse_48",
                "baked_Op_49": "q3_xy_baked_pulse_49",
                "baked_Op_50": "q3_xy_baked_pulse_50",
            },
        },
        "q4_xy": {
            "mixInputs": {
                "I": ('con1', 7),
                "Q": ('con1', 8),
                "lo_frequency": 3950000000.0,
                "mixer": "octave_octave1_5",
            },
            "intermediate_frequency": -89863100.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q4",
                "x90": "x90_pulse_q4",
                "-x90": "-x90_pulse_q4",
                "y90": "y90_pulse_q4",
                "y180": "y180_pulse_q4",
                "-y90": "-y90_pulse_q4",
            },
        },
        "q5_xy": {
            "mixInputs": {
                "I": ('con1', 7),
                "Q": ('con1', 8),
                "lo_frequency": 4750000000.0,
                "mixer": "octave_octave2_1",
            },
            "intermediate_frequency": -92000000.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q5",
                "x90": "x90_pulse_q5",
                "-x90": "-x90_pulse_q5",
                "y90": "y90_pulse_q5",
                "y180": "y180_pulse_q5",
                "-y90": "-y90_pulse_q5",
            },
        },
        "q1_z": {
            "singleInput": {
                "port": ('con1', 5),
            },
            "operations": {
                "const": "const_flux_pulse",
            },
        },
        "q2_z": {
            "singleInput": {
                "port": ('con1', 6),
            },
            "operations": {
                "const": "const_flux_pulse",
                "cz_1_2": "gft_cz_pulse_1_2_q2",
                "cz": "cz_flux_pulse",
                "baked_Op_0": "q2_z_baked_pulse_0",
                "baked_Op_1": "q2_z_baked_pulse_1",
                "baked_Op_2": "q2_z_baked_pulse_2",
                "baked_Op_3": "q2_z_baked_pulse_3",
                "baked_Op_4": "q2_z_baked_pulse_4",
                "baked_Op_5": "q2_z_baked_pulse_5",
                "baked_Op_6": "q2_z_baked_pulse_6",
                "baked_Op_7": "q2_z_baked_pulse_7",
                "baked_Op_8": "q2_z_baked_pulse_8",
                "baked_Op_9": "q2_z_baked_pulse_9",
                "baked_Op_10": "q2_z_baked_pulse_10",
                "baked_Op_11": "q2_z_baked_pulse_11",
                "baked_Op_12": "q2_z_baked_pulse_12",
                "baked_Op_13": "q2_z_baked_pulse_13",
                "baked_Op_14": "q2_z_baked_pulse_14",
                "baked_Op_15": "q2_z_baked_pulse_15",
                "baked_Op_16": "q2_z_baked_pulse_16",
                "baked_Op_17": "q2_z_baked_pulse_17",
                "baked_Op_18": "q2_z_baked_pulse_18",
                "baked_Op_19": "q2_z_baked_pulse_19",
                "baked_Op_20": "q2_z_baked_pulse_20",
                "baked_Op_21": "q2_z_baked_pulse_21",
                "baked_Op_22": "q2_z_baked_pulse_22",
                "baked_Op_23": "q2_z_baked_pulse_23",
                "baked_Op_24": "q2_z_baked_pulse_24",
                "baked_Op_25": "q2_z_baked_pulse_25",
                "baked_Op_26": "q2_z_baked_pulse_26",
                "baked_Op_27": "q2_z_baked_pulse_27",
                "baked_Op_28": "q2_z_baked_pulse_28",
                "baked_Op_29": "q2_z_baked_pulse_29",
                "baked_Op_30": "q2_z_baked_pulse_30",
                "baked_Op_31": "q2_z_baked_pulse_31",
                "baked_Op_32": "q2_z_baked_pulse_32",
                "baked_Op_33": "q2_z_baked_pulse_33",
                "baked_Op_34": "q2_z_baked_pulse_34",
                "baked_Op_35": "q2_z_baked_pulse_35",
                "baked_Op_36": "q2_z_baked_pulse_36",
                "baked_Op_37": "q2_z_baked_pulse_37",
                "baked_Op_38": "q2_z_baked_pulse_38",
                "baked_Op_39": "q2_z_baked_pulse_39",
                "baked_Op_40": "q2_z_baked_pulse_40",
                "baked_Op_41": "q2_z_baked_pulse_41",
                "baked_Op_42": "q2_z_baked_pulse_42",
                "baked_Op_43": "q2_z_baked_pulse_43",
                "baked_Op_44": "q2_z_baked_pulse_44",
                "baked_Op_45": "q2_z_baked_pulse_45",
                "baked_Op_46": "q2_z_baked_pulse_46",
                "baked_Op_47": "q2_z_baked_pulse_47",
                "baked_Op_48": "q2_z_baked_pulse_48",
                "baked_Op_49": "q2_z_baked_pulse_49",
                "baked_Op_50": "q2_z_baked_pulse_50",
            },
        },
        "q3_z": {
            "singleInput": {
                "port": ('con1', 9),
            },
            "operations": {
                "const": "const_flux_pulse",
            },
        },
        "q4_z": {
            "singleInput": {
                "port": ('con1', 10),
            },
            "operations": {
                "const": "const_flux_pulse",
            },
        },
        "q5_z": {
            "singleInput": {
                "port": ('con1', 5),
            },
            "operations": {
                "const": "const_flux_pulse",
            },
        },
    },
    "pulses": {
        "const_flux_pulse": {
            "operation": "control",
            "length": 200,
            "waveforms": {
                "single": "const_flux_wf",
            },
        },
        "const_pulse": {
            "operation": "control",
            "length": 100,
            "waveforms": {
                "I": "const_wf",
                "Q": "zero_wf",
            },
        },
        "saturation_pulse": {
            "operation": "control",
            "length": 1000,
            "waveforms": {
                "I": "saturation_wf",
                "Q": "zero_wf",
            },
        },
        "cz_flux_pulse": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "single": "cz_wf",
            },
        },
        "x90_pulse_q1": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q1",
                "Q": "x90_Q_wf_q1",
            },
        },
        "x180_pulse_q1": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q1",
                "Q": "x180_Q_wf_q1",
            },
        },
        "-x90_pulse_q1": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q1",
                "Q": "minus_x90_Q_wf_q1",
            },
        },
        "y90_pulse_q1": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q1",
                "Q": "y90_Q_wf_q1",
            },
        },
        "y180_pulse_q1": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q1",
                "Q": "y180_Q_wf_q1",
            },
        },
        "-y90_pulse_q1": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q1",
                "Q": "minus_y90_Q_wf_q1",
            },
        },
        "readout_pulse_q1": {
            "operation": "measurement",
            "length": 1700,
            "waveforms": {
                "I": "readout_wf_q1",
                "Q": "zero_wf",
            },
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q1",
                "rotated_sin": "rotated_sine_weights_q1",
                "rotated_minus_sin": "rotated_minus_sine_weights_q1",
                "opt_cos": "opt_cosine_weights_q1",
                "opt_sin": "opt_sine_weights_q1",
                "opt_minus_sin": "opt_minus_sine_weights_q1",
            },
            "digital_marker": "ON",
        },
        "x90_pulse_q2": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q2",
                "Q": "x90_Q_wf_q2",
            },
        },
        "x180_pulse_q2": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q2",
                "Q": "x180_Q_wf_q2",
            },
        },
        "-x90_pulse_q2": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q2",
                "Q": "minus_x90_Q_wf_q2",
            },
        },
        "y90_pulse_q2": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q2",
                "Q": "y90_Q_wf_q2",
            },
        },
        "y180_pulse_q2": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q2",
                "Q": "y180_Q_wf_q2",
            },
        },
        "-y90_pulse_q2": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q2",
                "Q": "minus_y90_Q_wf_q2",
            },
        },
        "readout_pulse_q2": {
            "operation": "measurement",
            "length": 1700,
            "waveforms": {
                "I": "readout_wf_q2",
                "Q": "zero_wf",
            },
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q2",
                "rotated_sin": "rotated_sine_weights_q2",
                "rotated_minus_sin": "rotated_minus_sine_weights_q2",
                "opt_cos": "opt_cosine_weights_q2",
                "opt_sin": "opt_sine_weights_q2",
                "opt_minus_sin": "opt_minus_sine_weights_q2",
            },
            "digital_marker": "ON",
        },
        "x90_pulse_q3": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q3",
                "Q": "x90_Q_wf_q3",
            },
        },
        "x180_pulse_q3": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q3",
                "Q": "x180_Q_wf_q3",
            },
        },
        "-x90_pulse_q3": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q3",
                "Q": "minus_x90_Q_wf_q3",
            },
        },
        "y90_pulse_q3": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q3",
                "Q": "y90_Q_wf_q3",
            },
        },
        "y180_pulse_q3": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q3",
                "Q": "y180_Q_wf_q3",
            },
        },
        "-y90_pulse_q3": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q3",
                "Q": "minus_y90_Q_wf_q3",
            },
        },
        "readout_pulse_q3": {
            "operation": "measurement",
            "length": 1700,
            "waveforms": {
                "I": "readout_wf_q3",
                "Q": "zero_wf",
            },
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q3",
                "rotated_sin": "rotated_sine_weights_q3",
                "rotated_minus_sin": "rotated_minus_sine_weights_q3",
                "opt_cos": "opt_cosine_weights_q3",
                "opt_sin": "opt_sine_weights_q3",
                "opt_minus_sin": "opt_minus_sine_weights_q3",
            },
            "digital_marker": "ON",
        },
        "x90_pulse_q4": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q4",
                "Q": "x90_Q_wf_q4",
            },
        },
        "x180_pulse_q4": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q4",
                "Q": "x180_Q_wf_q4",
            },
        },
        "-x90_pulse_q4": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q4",
                "Q": "minus_x90_Q_wf_q4",
            },
        },
        "y90_pulse_q4": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q4",
                "Q": "y90_Q_wf_q4",
            },
        },
        "y180_pulse_q4": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q4",
                "Q": "y180_Q_wf_q4",
            },
        },
        "-y90_pulse_q4": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q4",
                "Q": "minus_y90_Q_wf_q4",
            },
        },
        "readout_pulse_q4": {
            "operation": "measurement",
            "length": 1700,
            "waveforms": {
                "I": "readout_wf_q4",
                "Q": "zero_wf",
            },
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q4",
                "rotated_sin": "rotated_sine_weights_q4",
                "rotated_minus_sin": "rotated_minus_sine_weights_q4",
                "opt_cos": "opt_cosine_weights_q4",
                "opt_sin": "opt_sine_weights_q4",
                "opt_minus_sin": "opt_minus_sine_weights_q4",
            },
            "digital_marker": "ON",
        },
        "x90_pulse_q5": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q5",
                "Q": "x90_Q_wf_q5",
            },
        },
        "x180_pulse_q5": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q5",
                "Q": "x180_Q_wf_q5",
            },
        },
        "-x90_pulse_q5": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q5",
                "Q": "minus_x90_Q_wf_q5",
            },
        },
        "y90_pulse_q5": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q5",
                "Q": "y90_Q_wf_q5",
            },
        },
        "y180_pulse_q5": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q5",
                "Q": "y180_Q_wf_q5",
            },
        },
        "-y90_pulse_q5": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q5",
                "Q": "minus_y90_Q_wf_q5",
            },
        },
        "readout_pulse_q5": {
            "operation": "measurement",
            "length": 1700,
            "waveforms": {
                "I": "readout_wf_q5",
                "Q": "zero_wf",
            },
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q5",
                "rotated_sin": "rotated_sine_weights_q5",
                "rotated_minus_sin": "rotated_minus_sine_weights_q5",
                "opt_cos": "opt_cosine_weights_q5",
                "opt_sin": "opt_sine_weights_q5",
                "opt_minus_sin": "opt_minus_sine_weights_q5",
            },
            "digital_marker": "ON",
        },
        "gft_cz_pulse_1_2_q2": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "single": "gft_cz_wf_1_2_q2",
            },
        },
        "g_cz_pulse_1_2_q2": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "g_cz_wf_1_2_q2",
            },
        },
        "q2_xy_baked_pulse_0": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_0",
                "Q": "q2_xy_baked_wf_Q_0",
            },
        },
        "q3_xy_baked_pulse_0": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_0",
                "Q": "q3_xy_baked_wf_Q_0",
            },
        },
        "q2_z_baked_pulse_0": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_0",
            },
        },
        "q2_xy_baked_pulse_1": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_1",
                "Q": "q2_xy_baked_wf_Q_1",
            },
        },
        "q3_xy_baked_pulse_1": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_1",
                "Q": "q3_xy_baked_wf_Q_1",
            },
        },
        "q2_z_baked_pulse_1": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_1",
            },
        },
        "q2_xy_baked_pulse_2": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_2",
                "Q": "q2_xy_baked_wf_Q_2",
            },
        },
        "q3_xy_baked_pulse_2": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_2",
                "Q": "q3_xy_baked_wf_Q_2",
            },
        },
        "q2_z_baked_pulse_2": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_2",
            },
        },
        "q2_xy_baked_pulse_3": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_3",
                "Q": "q2_xy_baked_wf_Q_3",
            },
        },
        "q3_xy_baked_pulse_3": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_3",
                "Q": "q3_xy_baked_wf_Q_3",
            },
        },
        "q2_z_baked_pulse_3": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_3",
            },
        },
        "q2_xy_baked_pulse_4": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_4",
                "Q": "q2_xy_baked_wf_Q_4",
            },
        },
        "q3_xy_baked_pulse_4": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_4",
                "Q": "q3_xy_baked_wf_Q_4",
            },
        },
        "q2_z_baked_pulse_4": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_4",
            },
        },
        "q2_xy_baked_pulse_5": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_5",
                "Q": "q2_xy_baked_wf_Q_5",
            },
        },
        "q3_xy_baked_pulse_5": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_5",
                "Q": "q3_xy_baked_wf_Q_5",
            },
        },
        "q2_z_baked_pulse_5": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_5",
            },
        },
        "q2_xy_baked_pulse_6": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_6",
                "Q": "q2_xy_baked_wf_Q_6",
            },
        },
        "q3_xy_baked_pulse_6": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_6",
                "Q": "q3_xy_baked_wf_Q_6",
            },
        },
        "q2_z_baked_pulse_6": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_6",
            },
        },
        "q2_xy_baked_pulse_7": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_7",
                "Q": "q2_xy_baked_wf_Q_7",
            },
        },
        "q3_xy_baked_pulse_7": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_7",
                "Q": "q3_xy_baked_wf_Q_7",
            },
        },
        "q2_z_baked_pulse_7": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_7",
            },
        },
        "q2_xy_baked_pulse_8": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_8",
                "Q": "q2_xy_baked_wf_Q_8",
            },
        },
        "q3_xy_baked_pulse_8": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_8",
                "Q": "q3_xy_baked_wf_Q_8",
            },
        },
        "q2_z_baked_pulse_8": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_8",
            },
        },
        "q2_xy_baked_pulse_9": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_9",
                "Q": "q2_xy_baked_wf_Q_9",
            },
        },
        "q3_xy_baked_pulse_9": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_9",
                "Q": "q3_xy_baked_wf_Q_9",
            },
        },
        "q2_z_baked_pulse_9": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_9",
            },
        },
        "q2_xy_baked_pulse_10": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_10",
                "Q": "q2_xy_baked_wf_Q_10",
            },
        },
        "q3_xy_baked_pulse_10": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_10",
                "Q": "q3_xy_baked_wf_Q_10",
            },
        },
        "q2_z_baked_pulse_10": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_10",
            },
        },
        "q2_xy_baked_pulse_11": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_11",
                "Q": "q2_xy_baked_wf_Q_11",
            },
        },
        "q3_xy_baked_pulse_11": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_11",
                "Q": "q3_xy_baked_wf_Q_11",
            },
        },
        "q2_z_baked_pulse_11": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_11",
            },
        },
        "q2_xy_baked_pulse_12": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_12",
                "Q": "q2_xy_baked_wf_Q_12",
            },
        },
        "q3_xy_baked_pulse_12": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_12",
                "Q": "q3_xy_baked_wf_Q_12",
            },
        },
        "q2_z_baked_pulse_12": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_12",
            },
        },
        "q2_xy_baked_pulse_13": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_13",
                "Q": "q2_xy_baked_wf_Q_13",
            },
        },
        "q3_xy_baked_pulse_13": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_13",
                "Q": "q3_xy_baked_wf_Q_13",
            },
        },
        "q2_z_baked_pulse_13": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_13",
            },
        },
        "q2_xy_baked_pulse_14": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_14",
                "Q": "q2_xy_baked_wf_Q_14",
            },
        },
        "q3_xy_baked_pulse_14": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_14",
                "Q": "q3_xy_baked_wf_Q_14",
            },
        },
        "q2_z_baked_pulse_14": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_14",
            },
        },
        "q2_xy_baked_pulse_15": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_15",
                "Q": "q2_xy_baked_wf_Q_15",
            },
        },
        "q3_xy_baked_pulse_15": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_15",
                "Q": "q3_xy_baked_wf_Q_15",
            },
        },
        "q2_z_baked_pulse_15": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_15",
            },
        },
        "q2_xy_baked_pulse_16": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_16",
                "Q": "q2_xy_baked_wf_Q_16",
            },
        },
        "q3_xy_baked_pulse_16": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_16",
                "Q": "q3_xy_baked_wf_Q_16",
            },
        },
        "q2_z_baked_pulse_16": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_16",
            },
        },
        "q2_xy_baked_pulse_17": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_17",
                "Q": "q2_xy_baked_wf_Q_17",
            },
        },
        "q3_xy_baked_pulse_17": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_17",
                "Q": "q3_xy_baked_wf_Q_17",
            },
        },
        "q2_z_baked_pulse_17": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_17",
            },
        },
        "q2_xy_baked_pulse_18": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_18",
                "Q": "q2_xy_baked_wf_Q_18",
            },
        },
        "q3_xy_baked_pulse_18": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_18",
                "Q": "q3_xy_baked_wf_Q_18",
            },
        },
        "q2_z_baked_pulse_18": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_18",
            },
        },
        "q2_xy_baked_pulse_19": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_19",
                "Q": "q2_xy_baked_wf_Q_19",
            },
        },
        "q3_xy_baked_pulse_19": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_19",
                "Q": "q3_xy_baked_wf_Q_19",
            },
        },
        "q2_z_baked_pulse_19": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_19",
            },
        },
        "q2_xy_baked_pulse_20": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_20",
                "Q": "q2_xy_baked_wf_Q_20",
            },
        },
        "q3_xy_baked_pulse_20": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_20",
                "Q": "q3_xy_baked_wf_Q_20",
            },
        },
        "q2_z_baked_pulse_20": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_20",
            },
        },
        "q2_xy_baked_pulse_21": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_21",
                "Q": "q2_xy_baked_wf_Q_21",
            },
        },
        "q3_xy_baked_pulse_21": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_21",
                "Q": "q3_xy_baked_wf_Q_21",
            },
        },
        "q2_z_baked_pulse_21": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_21",
            },
        },
        "q2_xy_baked_pulse_22": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_22",
                "Q": "q2_xy_baked_wf_Q_22",
            },
        },
        "q3_xy_baked_pulse_22": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_22",
                "Q": "q3_xy_baked_wf_Q_22",
            },
        },
        "q2_z_baked_pulse_22": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_22",
            },
        },
        "q2_xy_baked_pulse_23": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_23",
                "Q": "q2_xy_baked_wf_Q_23",
            },
        },
        "q3_xy_baked_pulse_23": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_23",
                "Q": "q3_xy_baked_wf_Q_23",
            },
        },
        "q2_z_baked_pulse_23": {
            "operation": "control",
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_23",
            },
        },
        "q2_xy_baked_pulse_24": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_24",
                "Q": "q2_xy_baked_wf_Q_24",
            },
        },
        "q3_xy_baked_pulse_24": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_24",
                "Q": "q3_xy_baked_wf_Q_24",
            },
        },
        "q2_z_baked_pulse_24": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_24",
            },
        },
        "q2_xy_baked_pulse_25": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_25",
                "Q": "q2_xy_baked_wf_Q_25",
            },
        },
        "q3_xy_baked_pulse_25": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_25",
                "Q": "q3_xy_baked_wf_Q_25",
            },
        },
        "q2_z_baked_pulse_25": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_25",
            },
        },
        "q2_xy_baked_pulse_26": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_26",
                "Q": "q2_xy_baked_wf_Q_26",
            },
        },
        "q3_xy_baked_pulse_26": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_26",
                "Q": "q3_xy_baked_wf_Q_26",
            },
        },
        "q2_z_baked_pulse_26": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_26",
            },
        },
        "q2_xy_baked_pulse_27": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_27",
                "Q": "q2_xy_baked_wf_Q_27",
            },
        },
        "q3_xy_baked_pulse_27": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_27",
                "Q": "q3_xy_baked_wf_Q_27",
            },
        },
        "q2_z_baked_pulse_27": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_27",
            },
        },
        "q2_xy_baked_pulse_28": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_28",
                "Q": "q2_xy_baked_wf_Q_28",
            },
        },
        "q3_xy_baked_pulse_28": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_28",
                "Q": "q3_xy_baked_wf_Q_28",
            },
        },
        "q2_z_baked_pulse_28": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_28",
            },
        },
        "q2_xy_baked_pulse_29": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_29",
                "Q": "q2_xy_baked_wf_Q_29",
            },
        },
        "q3_xy_baked_pulse_29": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_29",
                "Q": "q3_xy_baked_wf_Q_29",
            },
        },
        "q2_z_baked_pulse_29": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_29",
            },
        },
        "q2_xy_baked_pulse_30": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_30",
                "Q": "q2_xy_baked_wf_Q_30",
            },
        },
        "q3_xy_baked_pulse_30": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_30",
                "Q": "q3_xy_baked_wf_Q_30",
            },
        },
        "q2_z_baked_pulse_30": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_30",
            },
        },
        "q2_xy_baked_pulse_31": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_31",
                "Q": "q2_xy_baked_wf_Q_31",
            },
        },
        "q3_xy_baked_pulse_31": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_31",
                "Q": "q3_xy_baked_wf_Q_31",
            },
        },
        "q2_z_baked_pulse_31": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_31",
            },
        },
        "q2_xy_baked_pulse_32": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_32",
                "Q": "q2_xy_baked_wf_Q_32",
            },
        },
        "q3_xy_baked_pulse_32": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_32",
                "Q": "q3_xy_baked_wf_Q_32",
            },
        },
        "q2_z_baked_pulse_32": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_32",
            },
        },
        "q2_xy_baked_pulse_33": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_33",
                "Q": "q2_xy_baked_wf_Q_33",
            },
        },
        "q3_xy_baked_pulse_33": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_33",
                "Q": "q3_xy_baked_wf_Q_33",
            },
        },
        "q2_z_baked_pulse_33": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_33",
            },
        },
        "q2_xy_baked_pulse_34": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_34",
                "Q": "q2_xy_baked_wf_Q_34",
            },
        },
        "q3_xy_baked_pulse_34": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_34",
                "Q": "q3_xy_baked_wf_Q_34",
            },
        },
        "q2_z_baked_pulse_34": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_34",
            },
        },
        "q2_xy_baked_pulse_35": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_35",
                "Q": "q2_xy_baked_wf_Q_35",
            },
        },
        "q3_xy_baked_pulse_35": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_35",
                "Q": "q3_xy_baked_wf_Q_35",
            },
        },
        "q2_z_baked_pulse_35": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_35",
            },
        },
        "q2_xy_baked_pulse_36": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_36",
                "Q": "q2_xy_baked_wf_Q_36",
            },
        },
        "q3_xy_baked_pulse_36": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_36",
                "Q": "q3_xy_baked_wf_Q_36",
            },
        },
        "q2_z_baked_pulse_36": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_36",
            },
        },
        "q2_xy_baked_pulse_37": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_37",
                "Q": "q2_xy_baked_wf_Q_37",
            },
        },
        "q3_xy_baked_pulse_37": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_37",
                "Q": "q3_xy_baked_wf_Q_37",
            },
        },
        "q2_z_baked_pulse_37": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_37",
            },
        },
        "q2_xy_baked_pulse_38": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_38",
                "Q": "q2_xy_baked_wf_Q_38",
            },
        },
        "q3_xy_baked_pulse_38": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_38",
                "Q": "q3_xy_baked_wf_Q_38",
            },
        },
        "q2_z_baked_pulse_38": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_38",
            },
        },
        "q2_xy_baked_pulse_39": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_39",
                "Q": "q2_xy_baked_wf_Q_39",
            },
        },
        "q3_xy_baked_pulse_39": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_39",
                "Q": "q3_xy_baked_wf_Q_39",
            },
        },
        "q2_z_baked_pulse_39": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_39",
            },
        },
        "q2_xy_baked_pulse_40": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_40",
                "Q": "q2_xy_baked_wf_Q_40",
            },
        },
        "q3_xy_baked_pulse_40": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_40",
                "Q": "q3_xy_baked_wf_Q_40",
            },
        },
        "q2_z_baked_pulse_40": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_40",
            },
        },
        "q2_xy_baked_pulse_41": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_41",
                "Q": "q2_xy_baked_wf_Q_41",
            },
        },
        "q3_xy_baked_pulse_41": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_41",
                "Q": "q3_xy_baked_wf_Q_41",
            },
        },
        "q2_z_baked_pulse_41": {
            "operation": "control",
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_41",
            },
        },
        "q2_xy_baked_pulse_42": {
            "operation": "control",
            "length": 356,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_42",
                "Q": "q2_xy_baked_wf_Q_42",
            },
        },
        "q3_xy_baked_pulse_42": {
            "operation": "control",
            "length": 356,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_42",
                "Q": "q3_xy_baked_wf_Q_42",
            },
        },
        "q2_z_baked_pulse_42": {
            "operation": "control",
            "length": 356,
            "waveforms": {
                "single": "q2_z_baked_wf_42",
            },
        },
        "q2_xy_baked_pulse_43": {
            "operation": "control",
            "length": 356,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_43",
                "Q": "q2_xy_baked_wf_Q_43",
            },
        },
        "q3_xy_baked_pulse_43": {
            "operation": "control",
            "length": 356,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_43",
                "Q": "q3_xy_baked_wf_Q_43",
            },
        },
        "q2_z_baked_pulse_43": {
            "operation": "control",
            "length": 356,
            "waveforms": {
                "single": "q2_z_baked_wf_43",
            },
        },
        "q2_xy_baked_pulse_44": {
            "operation": "control",
            "length": 356,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_44",
                "Q": "q2_xy_baked_wf_Q_44",
            },
        },
        "q3_xy_baked_pulse_44": {
            "operation": "control",
            "length": 356,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_44",
                "Q": "q3_xy_baked_wf_Q_44",
            },
        },
        "q2_z_baked_pulse_44": {
            "operation": "control",
            "length": 356,
            "waveforms": {
                "single": "q2_z_baked_wf_44",
            },
        },
        "q2_xy_baked_pulse_45": {
            "operation": "control",
            "length": 356,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_45",
                "Q": "q2_xy_baked_wf_Q_45",
            },
        },
        "q3_xy_baked_pulse_45": {
            "operation": "control",
            "length": 356,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_45",
                "Q": "q3_xy_baked_wf_Q_45",
            },
        },
        "q2_z_baked_pulse_45": {
            "operation": "control",
            "length": 356,
            "waveforms": {
                "single": "q2_z_baked_wf_45",
            },
        },
        "q2_xy_baked_pulse_46": {
            "operation": "control",
            "length": 356,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_46",
                "Q": "q2_xy_baked_wf_Q_46",
            },
        },
        "q3_xy_baked_pulse_46": {
            "operation": "control",
            "length": 356,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_46",
                "Q": "q3_xy_baked_wf_Q_46",
            },
        },
        "q2_z_baked_pulse_46": {
            "operation": "control",
            "length": 356,
            "waveforms": {
                "single": "q2_z_baked_wf_46",
            },
        },
        "q2_xy_baked_pulse_47": {
            "operation": "control",
            "length": 356,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_47",
                "Q": "q2_xy_baked_wf_Q_47",
            },
        },
        "q3_xy_baked_pulse_47": {
            "operation": "control",
            "length": 356,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_47",
                "Q": "q3_xy_baked_wf_Q_47",
            },
        },
        "q2_z_baked_pulse_47": {
            "operation": "control",
            "length": 356,
            "waveforms": {
                "single": "q2_z_baked_wf_47",
            },
        },
        "q2_xy_baked_pulse_48": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_48",
                "Q": "q2_xy_baked_wf_Q_48",
            },
        },
        "q3_xy_baked_pulse_48": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_48",
                "Q": "q3_xy_baked_wf_Q_48",
            },
        },
        "q2_z_baked_pulse_48": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_48",
            },
        },
        "q2_xy_baked_pulse_49": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_49",
                "Q": "q2_xy_baked_wf_Q_49",
            },
        },
        "q3_xy_baked_pulse_49": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_49",
                "Q": "q3_xy_baked_wf_Q_49",
            },
        },
        "q2_z_baked_pulse_49": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_49",
            },
        },
        "q2_xy_baked_pulse_50": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_50",
                "Q": "q2_xy_baked_wf_Q_50",
            },
        },
        "q3_xy_baked_pulse_50": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_50",
                "Q": "q3_xy_baked_wf_Q_50",
            },
        },
        "q2_z_baked_pulse_50": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_50",
            },
        },
    },
    "waveforms": {
        "const_wf": {
            "type": "constant",
            "sample": 0.27,
        },
        "saturation_wf": {
            "type": "constant",
            "sample": 0.1,
        },
        "const_flux_wf": {
            "type": "constant",
            "sample": 0.5,
        },
        "zero_wf": {
            "type": "constant",
            "sample": 0.0,
        },
        "cz_wf": {
            "type": "constant",
            "sample": 0.1755,
        },
        "x90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0006444587008155979, 0.0013789582933809714, 0.0022051982768183614, 0.0031222127073087685, 0.004125919855569243, 0.005208759218787376, 0.006359454317362786, 0.007562936707760972, 0.00880046014810808, 0.010049923940608054, 0.011286411594113968, 0.012482935924108854, 0.01361136568670365, 0.014643493214701668, 0.015552188778029734, 0.01631257696424561, 0.016903164482871647, 0.0173068482813562] + [0.0175117380691362] * 2 + [0.0173068482813562, 0.016903164482871647, 0.01631257696424561, 0.015552188778029734, 0.014643493214701668, 0.01361136568670365, 0.012482935924108854, 0.011286411594113968, 0.010049923940608054, 0.00880046014810808, 0.007562936707760972, 0.006359454317362786, 0.005208759218787376, 0.004125919855569243, 0.0031222127073087685, 0.0022051982768183614, 0.0013789582933809714, 0.0006444587008155979, 0.0],
        },
        "x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.000294371015801747, -0.00033771326152687455, -0.0003824612517831482, -0.00042742842419887534, -0.000471192393133838, -0.0005121282664652718, -0.0005484609868057831, -0.0005783360545561637, -0.0005999063142135595, -0.0006114307617658487, -0.0006113797347661263, -0.0005985395640585965, -0.0005721089728557221, -0.0005317793467624805, -0.0004777915535380474, -0.0004109632775403929, -0.0003326827832700226, -0.00024486748742062145, -0.00014988848327730165, -5.046496252607702e-05, 5.046496252607702e-05, 0.00014988848327730165, 0.00024486748742062145, 0.0003326827832700226, 0.0004109632775403929, 0.0004777915535380474, 0.0005317793467624805, 0.0005721089728557221, 0.0005985395640585965, 0.0006113797347661263, 0.0006114307617658487, 0.0005999063142135595, 0.0005783360545561637, 0.0005484609868057831, 0.0005121282664652718, 0.000471192393133838, 0.00042742842419887534, 0.0003824612517831482, 0.00033771326152687455, 0.000294371015801747],
        },
        "x180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0012889174016311958, 0.002757916586761943, 0.004410396553636723, 0.006244425414617537, 0.008251839711138485, 0.010417518437574751, 0.012718908634725572, 0.015125873415521945, 0.01760092029621616, 0.020099847881216108, 0.022572823188227936, 0.02496587184821771, 0.0272227313734073, 0.029286986429403337, 0.03110437755605947, 0.03262515392849122, 0.033806328965743294, 0.0346136965627124] + [0.0350234761382724] * 2 + [0.0346136965627124, 0.033806328965743294, 0.03262515392849122, 0.03110437755605947, 0.029286986429403337, 0.0272227313734073, 0.02496587184821771, 0.022572823188227936, 0.020099847881216108, 0.01760092029621616, 0.015125873415521945, 0.012718908634725572, 0.010417518437574751, 0.008251839711138485, 0.006244425414617537, 0.004410396553636723, 0.002757916586761943, 0.0012889174016311958, 0.0],
        },
        "x180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.000588742031603494, -0.0006754265230537491, -0.0007649225035662964, -0.0008548568483977507, -0.000942384786267676, -0.0010242565329305435, -0.0010969219736115662, -0.0011566721091123273, -0.001199812628427119, -0.0012228615235316974, -0.0012227594695322526, -0.001197079128117193, -0.0011442179457114442, -0.001063558693524961, -0.0009555831070760948, -0.0008219265550807858, -0.0006653655665400452, -0.0004897349748412429, -0.0002997769665546033, -0.00010092992505215404, 0.00010092992505215404, 0.0002997769665546033, 0.0004897349748412429, 0.0006653655665400452, 0.0008219265550807858, 0.0009555831070760948, 0.001063558693524961, 0.0011442179457114442, 0.001197079128117193, 0.0012227594695322526, 0.0012228615235316974, 0.001199812628427119, 0.0011566721091123273, 0.0010969219736115662, 0.0010242565329305435, 0.000942384786267676, 0.0008548568483977507, 0.0007649225035662964, 0.0006754265230537491, 0.000588742031603494],
        },
        "minus_x90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.0006444587008155979, -0.0013789582933809714, -0.0022051982768183614, -0.0031222127073087685, -0.004125919855569243, -0.005208759218787376, -0.006359454317362786, -0.007562936707760972, -0.00880046014810808, -0.010049923940608054, -0.011286411594113968, -0.012482935924108854, -0.01361136568670365, -0.014643493214701668, -0.015552188778029734, -0.01631257696424561, -0.016903164482871647, -0.0173068482813562] + [-0.0175117380691362] * 2 + [-0.0173068482813562, -0.016903164482871647, -0.01631257696424561, -0.015552188778029734, -0.014643493214701668, -0.01361136568670365, -0.012482935924108854, -0.011286411594113968, -0.010049923940608054, -0.00880046014810808, -0.007562936707760972, -0.006359454317362786, -0.005208759218787376, -0.004125919855569243, -0.0031222127073087685, -0.0022051982768183614, -0.0013789582933809714, -0.0006444587008155979, 0.0],
        },
        "minus_x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.000294371015801747, 0.00033771326152687455, 0.0003824612517831482, 0.00042742842419887534, 0.000471192393133838, 0.0005121282664652718, 0.0005484609868057831, 0.0005783360545561637, 0.0005999063142135595, 0.0006114307617658487, 0.0006113797347661263, 0.0005985395640585965, 0.0005721089728557221, 0.0005317793467624805, 0.0004777915535380474, 0.0004109632775403929, 0.0003326827832700226, 0.00024486748742062145, 0.00014988848327730165, 5.046496252607702e-05, -5.046496252607702e-05, -0.00014988848327730165, -0.00024486748742062145, -0.0003326827832700226, -0.0004109632775403929, -0.0004777915535380474, -0.0005317793467624805, -0.0005721089728557221, -0.0005985395640585965, -0.0006113797347661263, -0.0006114307617658487, -0.0005999063142135595, -0.0005783360545561637, -0.0005484609868057831, -0.0005121282664652718, -0.000471192393133838, -0.00042742842419887534, -0.0003824612517831482, -0.00033771326152687455, -0.000294371015801747],
        },
        "y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.000294371015801747, 0.00033771326152687455, 0.0003824612517831482, 0.00042742842419887534, 0.000471192393133838, 0.0005121282664652718, 0.0005484609868057831, 0.0005783360545561637, 0.0005999063142135595, 0.0006114307617658487, 0.0006113797347661263, 0.0005985395640585965, 0.0005721089728557221, 0.0005317793467624805, 0.0004777915535380474, 0.0004109632775403929, 0.0003326827832700226, 0.00024486748742062145, 0.00014988848327730165, 5.046496252607702e-05, -5.046496252607702e-05, -0.00014988848327730165, -0.00024486748742062145, -0.0003326827832700226, -0.0004109632775403929, -0.0004777915535380474, -0.0005317793467624805, -0.0005721089728557221, -0.0005985395640585965, -0.0006113797347661263, -0.0006114307617658487, -0.0005999063142135595, -0.0005783360545561637, -0.0005484609868057831, -0.0005121282664652718, -0.000471192393133838, -0.00042742842419887534, -0.0003824612517831482, -0.00033771326152687455, -0.000294371015801747],
        },
        "y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0006444587008155979, 0.0013789582933809714, 0.0022051982768183614, 0.0031222127073087685, 0.004125919855569243, 0.005208759218787376, 0.006359454317362786, 0.007562936707760972, 0.00880046014810808, 0.010049923940608054, 0.011286411594113968, 0.012482935924108854, 0.01361136568670365, 0.014643493214701668, 0.015552188778029734, 0.01631257696424561, 0.016903164482871647, 0.0173068482813562] + [0.0175117380691362] * 2 + [0.0173068482813562, 0.016903164482871647, 0.01631257696424561, 0.015552188778029734, 0.014643493214701668, 0.01361136568670365, 0.012482935924108854, 0.011286411594113968, 0.010049923940608054, 0.00880046014810808, 0.007562936707760972, 0.006359454317362786, 0.005208759218787376, 0.004125919855569243, 0.0031222127073087685, 0.0022051982768183614, 0.0013789582933809714, 0.0006444587008155979, 0.0],
        },
        "y180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.000588742031603494, 0.0006754265230537491, 0.0007649225035662964, 0.0008548568483977507, 0.000942384786267676, 0.0010242565329305435, 0.0010969219736115662, 0.0011566721091123273, 0.001199812628427119, 0.0012228615235316974, 0.0012227594695322526, 0.001197079128117193, 0.0011442179457114442, 0.001063558693524961, 0.0009555831070760948, 0.0008219265550807858, 0.0006653655665400452, 0.0004897349748412429, 0.0002997769665546033, 0.00010092992505215404, -0.00010092992505215404, -0.0002997769665546033, -0.0004897349748412429, -0.0006653655665400452, -0.0008219265550807858, -0.0009555831070760948, -0.001063558693524961, -0.0011442179457114442, -0.001197079128117193, -0.0012227594695322526, -0.0012228615235316974, -0.001199812628427119, -0.0011566721091123273, -0.0010969219736115662, -0.0010242565329305435, -0.000942384786267676, -0.0008548568483977507, -0.0007649225035662964, -0.0006754265230537491, -0.000588742031603494],
        },
        "y180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0012889174016311958, 0.002757916586761943, 0.004410396553636723, 0.006244425414617537, 0.008251839711138485, 0.010417518437574751, 0.012718908634725572, 0.015125873415521945, 0.01760092029621616, 0.020099847881216108, 0.022572823188227936, 0.02496587184821771, 0.0272227313734073, 0.029286986429403337, 0.03110437755605947, 0.03262515392849122, 0.033806328965743294, 0.0346136965627124] + [0.0350234761382724] * 2 + [0.0346136965627124, 0.033806328965743294, 0.03262515392849122, 0.03110437755605947, 0.029286986429403337, 0.0272227313734073, 0.02496587184821771, 0.022572823188227936, 0.020099847881216108, 0.01760092029621616, 0.015125873415521945, 0.012718908634725572, 0.010417518437574751, 0.008251839711138485, 0.006244425414617537, 0.004410396553636723, 0.002757916586761943, 0.0012889174016311958, 0.0],
        },
        "minus_y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.000294371015801747, -0.00033771326152687455, -0.0003824612517831482, -0.00042742842419887534, -0.000471192393133838, -0.0005121282664652718, -0.0005484609868057831, -0.0005783360545561637, -0.0005999063142135595, -0.0006114307617658487, -0.0006113797347661263, -0.0005985395640585965, -0.0005721089728557221, -0.0005317793467624805, -0.0004777915535380474, -0.0004109632775403929, -0.0003326827832700226, -0.00024486748742062145, -0.00014988848327730165, -5.046496252607702e-05, 5.046496252607702e-05, 0.00014988848327730165, 0.00024486748742062145, 0.0003326827832700226, 0.0004109632775403929, 0.0004777915535380474, 0.0005317793467624805, 0.0005721089728557221, 0.0005985395640585965, 0.0006113797347661263, 0.0006114307617658487, 0.0005999063142135595, 0.0005783360545561637, 0.0005484609868057831, 0.0005121282664652718, 0.000471192393133838, 0.00042742842419887534, 0.0003824612517831482, 0.00033771326152687455, 0.000294371015801747],
        },
        "minus_y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.0006444587008155979, -0.0013789582933809714, -0.0022051982768183614, -0.0031222127073087685, -0.004125919855569243, -0.005208759218787376, -0.006359454317362786, -0.007562936707760972, -0.00880046014810808, -0.010049923940608054, -0.011286411594113968, -0.012482935924108854, -0.01361136568670365, -0.014643493214701668, -0.015552188778029734, -0.01631257696424561, -0.016903164482871647, -0.0173068482813562] + [-0.0175117380691362] * 2 + [-0.0173068482813562, -0.016903164482871647, -0.01631257696424561, -0.015552188778029734, -0.014643493214701668, -0.01361136568670365, -0.012482935924108854, -0.011286411594113968, -0.010049923940608054, -0.00880046014810808, -0.007562936707760972, -0.006359454317362786, -0.005208759218787376, -0.004125919855569243, -0.0031222127073087685, -0.0022051982768183614, -0.0013789582933809714, -0.0006444587008155979, 0.0],
        },
        "readout_wf_q1": {
            "type": "constant",
            "sample": 0.03,
        },
        "x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007882406922592178, 0.0016866108540323985, 0.0026971891512804734, 0.003818794133239242, 0.005046433416205089, 0.00637085971099852, 0.007778280698460524, 0.009250266089190289, 0.010763887260060829, 0.01229211273596268, 0.013804467030715788, 0.015267941982619701, 0.016648130125177088, 0.01791053051815703, 0.01902196065166925, 0.019951995283104904, 0.020674345860313796, 0.021168093553329027] + [0.021418695287702638] * 2 + [0.021168093553329027, 0.020674345860313796, 0.019951995283104904, 0.01902196065166925, 0.01791053051815703, 0.016648130125177088, 0.015267941982619701, 0.013804467030715788, 0.01229211273596268, 0.010763887260060829, 0.009250266089190289, 0.007778280698460524, 0.00637085971099852, 0.005046433416205089, 0.003818794133239242, 0.0026971891512804734, 0.0016866108540323985, 0.0007882406922592178, 0.0],
        },
        "x90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0003799551396356434, 0.00043589851769465753, 0.0004936563402164494, 0.0005516970689468364, 0.0006081847801517076, 0.000661022167777625, 0.0007079181021233454, 0.0007464789145994111, 0.0007743204159027276, 0.0007891954302346503, 0.0007891295678712929, 0.0007725563028681557, 0.000738441398777516, 0.000686386516023601, 0.0006167025511898322, 0.0005304449185586393, 0.0004294055004955612, 0.00031605917492159293, 0.00019346639626965594, 6.513692195911263e-05, -6.513692195911263e-05, -0.00019346639626965594, -0.00031605917492159293, -0.0004294055004955612, -0.0005304449185586393, -0.0006167025511898322, -0.000686386516023601, -0.000738441398777516, -0.0007725563028681557, -0.0007891295678712929, -0.0007891954302346503, -0.0007743204159027276, -0.0007464789145994111, -0.0007079181021233454, -0.000661022167777625, -0.0006081847801517076, -0.0005516970689468364, -0.0004936563402164494, -0.00043589851769465753, -0.0003799551396356434],
        },
        "x180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0015760768444548542, 0.00337235610740649, 0.005392994053965991, 0.0076356283889478915, 0.010090276907130893, 0.012738449776040096, 0.015552569435837084, 0.018495784766494085, 0.0215222502891611, 0.024577916926684592, 0.027601849347301578, 0.030528048168025384, 0.033287716114425325, 0.03581186901257599, 0.03803415887258986, 0.03989375082406045, 0.04133808125447058, 0.04232532323982649] + [0.04282639809501372] * 2 + [0.04232532323982649, 0.04133808125447058, 0.03989375082406045, 0.03803415887258986, 0.03581186901257599, 0.033287716114425325, 0.030528048168025384, 0.027601849347301578, 0.024577916926684592, 0.0215222502891611, 0.018495784766494085, 0.015552569435837084, 0.012738449776040096, 0.010090276907130893, 0.0076356283889478915, 0.005392994053965991, 0.00337235610740649, 0.0015760768444548542, 0.0],
        },
        "x180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.000759715279091957, 0.0008715733240080147, 0.0009870593266423386, 0.0011031109965010243, 0.0012160574283467086, 0.0013217050864497337, 0.001415472887258803, 0.0014925747220710902, 0.0015482434358915463, 0.001577985830416096, 0.0015778541394911943, 0.0015447161151986492, 0.0014765038154327629, 0.0013724207654774103, 0.001233088598941415, 0.0010606176027310227, 0.0008585906219493171, 0.0006319561422840313, 0.00038683350191778473, 0.00013024041441527076, -0.00013024041441527076, -0.00038683350191778473, -0.0006319561422840313, -0.0008585906219493171, -0.0010606176027310227, -0.001233088598941415, -0.0013724207654774103, -0.0014765038154327629, -0.0015447161151986492, -0.0015778541394911943, -0.001577985830416096, -0.0015482434358915463, -0.0014925747220710902, -0.001415472887258803, -0.0013217050864497337, -0.0012160574283467086, -0.0011031109965010243, -0.0009870593266423386, -0.0008715733240080147, -0.000759715279091957],
        },
        "minus_x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.0007882406922592178, -0.0016866108540323985, -0.0026971891512804734, -0.003818794133239242, -0.005046433416205089, -0.00637085971099852, -0.007778280698460524, -0.009250266089190289, -0.010763887260060829, -0.01229211273596268, -0.013804467030715788, -0.015267941982619701, -0.016648130125177088, -0.01791053051815703, -0.01902196065166925, -0.019951995283104904, -0.020674345860313796, -0.021168093553329027] + [-0.021418695287702638] * 2 + [-0.021168093553329027, -0.020674345860313796, -0.019951995283104904, -0.01902196065166925, -0.01791053051815703, -0.016648130125177088, -0.015267941982619701, -0.013804467030715788, -0.01229211273596268, -0.010763887260060829, -0.009250266089190289, -0.007778280698460524, -0.00637085971099852, -0.005046433416205089, -0.003818794133239242, -0.0026971891512804734, -0.0016866108540323985, -0.0007882406922592178, 0.0],
        },
        "minus_x90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.0003799551396356434, -0.00043589851769465753, -0.0004936563402164494, -0.0005516970689468364, -0.0006081847801517076, -0.000661022167777625, -0.0007079181021233454, -0.0007464789145994111, -0.0007743204159027276, -0.0007891954302346503, -0.0007891295678712929, -0.0007725563028681557, -0.000738441398777516, -0.000686386516023601, -0.0006167025511898322, -0.0005304449185586393, -0.0004294055004955612, -0.00031605917492159293, -0.00019346639626965594, -6.513692195911263e-05, 6.513692195911263e-05, 0.00019346639626965594, 0.00031605917492159293, 0.0004294055004955612, 0.0005304449185586393, 0.0006167025511898322, 0.000686386516023601, 0.000738441398777516, 0.0007725563028681557, 0.0007891295678712929, 0.0007891954302346503, 0.0007743204159027276, 0.0007464789145994111, 0.0007079181021233454, 0.000661022167777625, 0.0006081847801517076, 0.0005516970689468364, 0.0004936563402164494, 0.00043589851769465753, 0.0003799551396356434],
        },
        "y90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.0003799551396356434, -0.00043589851769465753, -0.0004936563402164494, -0.0005516970689468364, -0.0006081847801517076, -0.000661022167777625, -0.0007079181021233454, -0.0007464789145994111, -0.0007743204159027276, -0.0007891954302346503, -0.0007891295678712929, -0.0007725563028681557, -0.000738441398777516, -0.000686386516023601, -0.0006167025511898322, -0.0005304449185586393, -0.0004294055004955612, -0.00031605917492159293, -0.00019346639626965594, -6.513692195911263e-05, 6.513692195911263e-05, 0.00019346639626965594, 0.00031605917492159293, 0.0004294055004955612, 0.0005304449185586393, 0.0006167025511898322, 0.000686386516023601, 0.000738441398777516, 0.0007725563028681557, 0.0007891295678712929, 0.0007891954302346503, 0.0007743204159027276, 0.0007464789145994111, 0.0007079181021233454, 0.000661022167777625, 0.0006081847801517076, 0.0005516970689468364, 0.0004936563402164494, 0.00043589851769465753, 0.0003799551396356434],
        },
        "y90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007882406922592178, 0.0016866108540323985, 0.0026971891512804734, 0.003818794133239242, 0.005046433416205089, 0.00637085971099852, 0.007778280698460524, 0.009250266089190289, 0.010763887260060829, 0.01229211273596268, 0.013804467030715788, 0.015267941982619701, 0.016648130125177088, 0.01791053051815703, 0.01902196065166925, 0.019951995283104904, 0.020674345860313796, 0.021168093553329027] + [0.021418695287702638] * 2 + [0.021168093553329027, 0.020674345860313796, 0.019951995283104904, 0.01902196065166925, 0.01791053051815703, 0.016648130125177088, 0.015267941982619701, 0.013804467030715788, 0.01229211273596268, 0.010763887260060829, 0.009250266089190289, 0.007778280698460524, 0.00637085971099852, 0.005046433416205089, 0.003818794133239242, 0.0026971891512804734, 0.0016866108540323985, 0.0007882406922592178, 0.0],
        },
        "y180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.000759715279091957, -0.0008715733240080147, -0.0009870593266423386, -0.0011031109965010243, -0.0012160574283467086, -0.0013217050864497337, -0.001415472887258803, -0.0014925747220710902, -0.0015482434358915463, -0.001577985830416096, -0.0015778541394911943, -0.0015447161151986492, -0.0014765038154327629, -0.0013724207654774103, -0.001233088598941415, -0.0010606176027310227, -0.0008585906219493171, -0.0006319561422840313, -0.00038683350191778473, -0.00013024041441527076, 0.00013024041441527076, 0.00038683350191778473, 0.0006319561422840313, 0.0008585906219493171, 0.0010606176027310227, 0.001233088598941415, 0.0013724207654774103, 0.0014765038154327629, 0.0015447161151986492, 0.0015778541394911943, 0.001577985830416096, 0.0015482434358915463, 0.0014925747220710902, 0.001415472887258803, 0.0013217050864497337, 0.0012160574283467086, 0.0011031109965010243, 0.0009870593266423386, 0.0008715733240080147, 0.000759715279091957],
        },
        "y180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0015760768444548542, 0.00337235610740649, 0.005392994053965991, 0.0076356283889478915, 0.010090276907130893, 0.012738449776040096, 0.015552569435837084, 0.018495784766494085, 0.0215222502891611, 0.024577916926684592, 0.027601849347301578, 0.030528048168025384, 0.033287716114425325, 0.03581186901257599, 0.03803415887258986, 0.03989375082406045, 0.04133808125447058, 0.04232532323982649] + [0.04282639809501372] * 2 + [0.04232532323982649, 0.04133808125447058, 0.03989375082406045, 0.03803415887258986, 0.03581186901257599, 0.033287716114425325, 0.030528048168025384, 0.027601849347301578, 0.024577916926684592, 0.0215222502891611, 0.018495784766494085, 0.015552569435837084, 0.012738449776040096, 0.010090276907130893, 0.0076356283889478915, 0.005392994053965991, 0.00337235610740649, 0.0015760768444548542, 0.0],
        },
        "minus_y90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0003799551396356434, 0.00043589851769465753, 0.0004936563402164494, 0.0005516970689468364, 0.0006081847801517076, 0.000661022167777625, 0.0007079181021233454, 0.0007464789145994111, 0.0007743204159027276, 0.0007891954302346503, 0.0007891295678712929, 0.0007725563028681557, 0.000738441398777516, 0.000686386516023601, 0.0006167025511898322, 0.0005304449185586393, 0.0004294055004955612, 0.00031605917492159293, 0.00019346639626965594, 6.513692195911263e-05, -6.513692195911263e-05, -0.00019346639626965594, -0.00031605917492159293, -0.0004294055004955612, -0.0005304449185586393, -0.0006167025511898322, -0.000686386516023601, -0.000738441398777516, -0.0007725563028681557, -0.0007891295678712929, -0.0007891954302346503, -0.0007743204159027276, -0.0007464789145994111, -0.0007079181021233454, -0.000661022167777625, -0.0006081847801517076, -0.0005516970689468364, -0.0004936563402164494, -0.00043589851769465753, -0.0003799551396356434],
        },
        "minus_y90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.0007882406922592178, -0.0016866108540323985, -0.0026971891512804734, -0.003818794133239242, -0.005046433416205089, -0.00637085971099852, -0.007778280698460524, -0.009250266089190289, -0.010763887260060829, -0.01229211273596268, -0.013804467030715788, -0.015267941982619701, -0.016648130125177088, -0.01791053051815703, -0.01902196065166925, -0.019951995283104904, -0.020674345860313796, -0.021168093553329027] + [-0.021418695287702638] * 2 + [-0.021168093553329027, -0.020674345860313796, -0.019951995283104904, -0.01902196065166925, -0.01791053051815703, -0.016648130125177088, -0.015267941982619701, -0.013804467030715788, -0.01229211273596268, -0.010763887260060829, -0.009250266089190289, -0.007778280698460524, -0.00637085971099852, -0.005046433416205089, -0.003818794133239242, -0.0026971891512804734, -0.0016866108540323985, -0.0007882406922592178, 0.0],
        },
        "readout_wf_q2": {
            "type": "constant",
            "sample": 0.020999999999999998,
        },
        "x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0012082000004049066, 0.002585204309465838, 0.004134199065933938, 0.0058533733650591715, 0.0077350749782114205, 0.009765129840412657, 0.011922397353141202, 0.014178627927305551, 0.016498677015379354, 0.018841111298125324, 0.02115921854312933, 0.023402404482204656, 0.025517930019990902, 0.027452912786407043, 0.029156491275752396, 0.03058203026798145, 0.03168923518171769, 0.0324460420412965] + [0.03283015950509282] * 2 + [0.0324460420412965, 0.03168923518171769, 0.03058203026798145, 0.029156491275752396, 0.027452912786407043, 0.025517930019990902, 0.023402404482204656, 0.02115921854312933, 0.018841111298125324, 0.016498677015379354, 0.014178627927305551, 0.011922397353141202, 0.009765129840412657, 0.0077350749782114205, 0.0058533733650591715, 0.004134199065933938, 0.002585204309465838, 0.0012082000004049066, 0.0],
        },
        "x90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.000627186912398396, -0.0007195319049878259, -0.0008148719770001034, -0.0009106790385407691, -0.0010039225546385098, -0.0010911405299923232, -0.0011685510271750572, -0.0012322028491760157, -0.001278160446316846, -0.001302714435294774, -0.0013026057171646364, -0.0012752484483153563, -0.001218935428352279, -0.0011330091234179746, -0.0010179827263815232, -0.000875598395608602, -0.0007088139675672238, -0.000521714690435162, -0.0003193524157761579, -0.00010752065363781363, 0.00010752065363781363, 0.0003193524157761579, 0.000521714690435162, 0.0007088139675672238, 0.000875598395608602, 0.0010179827263815232, 0.0011330091234179746, 0.001218935428352279, 0.0012752484483153563, 0.0013026057171646364, 0.001302714435294774, 0.001278160446316846, 0.0012322028491760157, 0.0011685510271750572, 0.0010911405299923232, 0.0010039225546385098, 0.0009106790385407691, 0.0008148719770001034, 0.0007195319049878259, 0.000627186912398396],
        },
        "x180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.002391291440682645, 0.005116683442782459, 0.008182482070131494, 0.011585103147074066, 0.015309401243367481, 0.01932732279151441, 0.023597025933975654, 0.028062598569629983, 0.03265448197007294, 0.037290670555418744, 0.04187871062469931, 0.0463184650810582, 0.050505551746642056, 0.05433530487166164, 0.057707058437906765, 0.06052851116869163, 0.06271991129483957, 0.06421779721186839] + [0.06497804949053503] * 2 + [0.06421779721186839, 0.06271991129483957, 0.06052851116869163, 0.057707058437906765, 0.05433530487166164, 0.050505551746642056, 0.0463184650810582, 0.04187871062469931, 0.037290670555418744, 0.03265448197007294, 0.028062598569629983, 0.023597025933975654, 0.01932732279151441, 0.015309401243367481, 0.011585103147074066, 0.008182482070131494, 0.005116683442782459, 0.002391291440682645, 0.0],
        },
        "x180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.001241339757344673, -0.0014241106481698684, -0.0016128094547255881, -0.0018024325354592163, -0.001986981800373102, -0.0021596052053286952, -0.0023128174709056057, -0.0024387983160336774, -0.00252975842912785, -0.002578356131211824, -0.0025781409543090277, -0.00252399494965929, -0.0024125391951554265, -0.0022424722878139035, -0.002014809948305835, -0.0017330002881911963, -0.001402897511266153, -0.0010325872151116518, -0.0006320681163308418, -0.0002128068355028474, 0.0002128068355028474, 0.0006320681163308418, 0.0010325872151116518, 0.001402897511266153, 0.0017330002881911963, 0.002014809948305835, 0.0022424722878139035, 0.0024125391951554265, 0.00252399494965929, 0.0025781409543090277, 0.002578356131211824, 0.00252975842912785, 0.0024387983160336774, 0.0023128174709056057, 0.0021596052053286952, 0.001986981800373102, 0.0018024325354592163, 0.0016128094547255881, 0.0014241106481698684, 0.001241339757344673],
        },
        "minus_x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.0012082000004049066, -0.002585204309465838, -0.004134199065933938, -0.0058533733650591715, -0.0077350749782114205, -0.009765129840412657, -0.011922397353141202, -0.014178627927305551, -0.016498677015379354, -0.018841111298125324, -0.02115921854312933, -0.023402404482204656, -0.025517930019990902, -0.027452912786407043, -0.029156491275752396, -0.03058203026798145, -0.03168923518171769, -0.0324460420412965] + [-0.03283015950509282] * 2 + [-0.0324460420412965, -0.03168923518171769, -0.03058203026798145, -0.029156491275752396, -0.027452912786407043, -0.025517930019990902, -0.023402404482204656, -0.02115921854312933, -0.018841111298125324, -0.016498677015379354, -0.014178627927305551, -0.011922397353141202, -0.009765129840412657, -0.0077350749782114205, -0.0058533733650591715, -0.004134199065933938, -0.002585204309465838, -0.0012082000004049066, 0.0],
        },
        "minus_x90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.000627186912398396, 0.0007195319049878259, 0.0008148719770001034, 0.0009106790385407691, 0.0010039225546385098, 0.0010911405299923232, 0.0011685510271750572, 0.0012322028491760157, 0.001278160446316846, 0.001302714435294774, 0.0013026057171646364, 0.0012752484483153563, 0.001218935428352279, 0.0011330091234179746, 0.0010179827263815232, 0.000875598395608602, 0.0007088139675672238, 0.000521714690435162, 0.0003193524157761579, 0.00010752065363781363, -0.00010752065363781363, -0.0003193524157761579, -0.000521714690435162, -0.0007088139675672238, -0.000875598395608602, -0.0010179827263815232, -0.0011330091234179746, -0.001218935428352279, -0.0012752484483153563, -0.0013026057171646364, -0.001302714435294774, -0.001278160446316846, -0.0012322028491760157, -0.0011685510271750572, -0.0010911405299923232, -0.0010039225546385098, -0.0009106790385407691, -0.0008148719770001034, -0.0007195319049878259, -0.000627186912398396],
        },
        "y90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.000627186912398396, 0.0007195319049878259, 0.0008148719770001034, 0.0009106790385407691, 0.0010039225546385098, 0.0010911405299923232, 0.0011685510271750572, 0.0012322028491760157, 0.001278160446316846, 0.001302714435294774, 0.0013026057171646364, 0.0012752484483153563, 0.001218935428352279, 0.0011330091234179746, 0.0010179827263815232, 0.000875598395608602, 0.0007088139675672238, 0.000521714690435162, 0.0003193524157761579, 0.00010752065363781363, -0.00010752065363781363, -0.0003193524157761579, -0.000521714690435162, -0.0007088139675672238, -0.000875598395608602, -0.0010179827263815232, -0.0011330091234179746, -0.001218935428352279, -0.0012752484483153563, -0.0013026057171646364, -0.001302714435294774, -0.001278160446316846, -0.0012322028491760157, -0.0011685510271750572, -0.0010911405299923232, -0.0010039225546385098, -0.0009106790385407691, -0.0008148719770001034, -0.0007195319049878259, -0.000627186912398396],
        },
        "y90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0012082000004049066, 0.002585204309465838, 0.004134199065933938, 0.0058533733650591715, 0.0077350749782114205, 0.009765129840412657, 0.011922397353141202, 0.014178627927305551, 0.016498677015379354, 0.018841111298125324, 0.02115921854312933, 0.023402404482204656, 0.025517930019990902, 0.027452912786407043, 0.029156491275752396, 0.03058203026798145, 0.03168923518171769, 0.0324460420412965] + [0.03283015950509282] * 2 + [0.0324460420412965, 0.03168923518171769, 0.03058203026798145, 0.029156491275752396, 0.027452912786407043, 0.025517930019990902, 0.023402404482204656, 0.02115921854312933, 0.018841111298125324, 0.016498677015379354, 0.014178627927305551, 0.011922397353141202, 0.009765129840412657, 0.0077350749782114205, 0.0058533733650591715, 0.004134199065933938, 0.002585204309465838, 0.0012082000004049066, 0.0],
        },
        "y180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.001241339757344673, 0.0014241106481698684, 0.0016128094547255881, 0.0018024325354592163, 0.001986981800373102, 0.0021596052053286952, 0.0023128174709056057, 0.0024387983160336774, 0.00252975842912785, 0.002578356131211824, 0.0025781409543090277, 0.00252399494965929, 0.0024125391951554265, 0.0022424722878139035, 0.002014809948305835, 0.0017330002881911963, 0.001402897511266153, 0.0010325872151116518, 0.0006320681163308418, 0.0002128068355028474, -0.0002128068355028474, -0.0006320681163308418, -0.0010325872151116518, -0.001402897511266153, -0.0017330002881911963, -0.002014809948305835, -0.0022424722878139035, -0.0024125391951554265, -0.00252399494965929, -0.0025781409543090277, -0.002578356131211824, -0.00252975842912785, -0.0024387983160336774, -0.0023128174709056057, -0.0021596052053286952, -0.001986981800373102, -0.0018024325354592163, -0.0016128094547255881, -0.0014241106481698684, -0.001241339757344673],
        },
        "y180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.002391291440682645, 0.005116683442782459, 0.008182482070131494, 0.011585103147074066, 0.015309401243367481, 0.01932732279151441, 0.023597025933975654, 0.028062598569629983, 0.03265448197007294, 0.037290670555418744, 0.04187871062469931, 0.0463184650810582, 0.050505551746642056, 0.05433530487166164, 0.057707058437906765, 0.06052851116869163, 0.06271991129483957, 0.06421779721186839] + [0.06497804949053503] * 2 + [0.06421779721186839, 0.06271991129483957, 0.06052851116869163, 0.057707058437906765, 0.05433530487166164, 0.050505551746642056, 0.0463184650810582, 0.04187871062469931, 0.037290670555418744, 0.03265448197007294, 0.028062598569629983, 0.023597025933975654, 0.01932732279151441, 0.015309401243367481, 0.011585103147074066, 0.008182482070131494, 0.005116683442782459, 0.002391291440682645, 0.0],
        },
        "minus_y90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.000627186912398396, -0.0007195319049878259, -0.0008148719770001034, -0.0009106790385407691, -0.0010039225546385098, -0.0010911405299923232, -0.0011685510271750572, -0.0012322028491760157, -0.001278160446316846, -0.001302714435294774, -0.0013026057171646364, -0.0012752484483153563, -0.001218935428352279, -0.0011330091234179746, -0.0010179827263815232, -0.000875598395608602, -0.0007088139675672238, -0.000521714690435162, -0.0003193524157761579, -0.00010752065363781363, 0.00010752065363781363, 0.0003193524157761579, 0.000521714690435162, 0.0007088139675672238, 0.000875598395608602, 0.0010179827263815232, 0.0011330091234179746, 0.001218935428352279, 0.0012752484483153563, 0.0013026057171646364, 0.001302714435294774, 0.001278160446316846, 0.0012322028491760157, 0.0011685510271750572, 0.0010911405299923232, 0.0010039225546385098, 0.0009106790385407691, 0.0008148719770001034, 0.0007195319049878259, 0.000627186912398396],
        },
        "minus_y90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.0012082000004049066, -0.002585204309465838, -0.004134199065933938, -0.0058533733650591715, -0.0077350749782114205, -0.009765129840412657, -0.011922397353141202, -0.014178627927305551, -0.016498677015379354, -0.018841111298125324, -0.02115921854312933, -0.023402404482204656, -0.025517930019990902, -0.027452912786407043, -0.029156491275752396, -0.03058203026798145, -0.03168923518171769, -0.0324460420412965] + [-0.03283015950509282] * 2 + [-0.0324460420412965, -0.03168923518171769, -0.03058203026798145, -0.029156491275752396, -0.027452912786407043, -0.025517930019990902, -0.023402404482204656, -0.02115921854312933, -0.018841111298125324, -0.016498677015379354, -0.014178627927305551, -0.011922397353141202, -0.009765129840412657, -0.0077350749782114205, -0.0058533733650591715, -0.004134199065933938, -0.002585204309465838, -0.0012082000004049066, 0.0],
        },
        "readout_wf_q3": {
            "type": "constant",
            "sample": 0.0135,
        },
        "x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0026246360206212457, 0.00561597446533303, 0.00898093674990273, 0.012715588951275178, 0.01680330773317002, 0.021213302033273505, 0.02589964702427318, 0.030800974647012896, 0.035840938563688335, 0.0409295310089563, 0.04596527655841962, 0.05083826663843542, 0.05543393335516866, 0.05963739757161887, 0.0633381701801215, 0.06643494305427361, 0.06884018216851553, 0.07048423327233783] + [0.07131867171902846] * 2 + [0.07048423327233783, 0.06884018216851553, 0.06643494305427361, 0.0633381701801215, 0.05963739757161887, 0.05543393335516866, 0.05083826663843542, 0.04596527655841962, 0.0409295310089563, 0.035840938563688335, 0.030800974647012896, 0.02589964702427318, 0.021213302033273505, 0.01680330773317002, 0.012715588951275178, 0.00898093674990273, 0.00561597446533303, 0.0026246360206212457, 0.0],
        },
        "x90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.0019861092078177385, -0.0022785375676130162, -0.0025804504282839827, -0.002883842102023192, -0.0031791158110724476, -0.003455308474715587, -0.0037004438533357266, -0.003902009713960981, -0.004047543373937295, -0.004125298350378418, -0.004124954073297606, -0.004038321966523372, -0.0038599958483315957, -0.00358789351001722, -0.003223640076503164, -0.0027727524307204128, -0.0022445971364926194, -0.0016521109258556435, -0.001011291468258463, -0.000340485038828418, 0.000340485038828418, 0.001011291468258463, 0.0016521109258556435, 0.0022445971364926194, 0.0027727524307204128, 0.003223640076503164, 0.00358789351001722, 0.0038599958483315957, 0.004038321966523372, 0.004124954073297606, 0.004125298350378418, 0.004047543373937295, 0.003902009713960981, 0.0037004438533357266, 0.003455308474715587, 0.0031791158110724476, 0.002883842102023192, 0.0025804504282839827, 0.0022785375676130162, 0.0019861092078177385],
        },
        "x180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.004802803434016331, 0.010276633116185457, 0.016434154497699333, 0.023268168919768663, 0.030748257453465856, 0.038818075745266994, 0.047393586268981804, 0.056362492034498786, 0.06558508740244534, 0.0748966677809916, 0.08411154398773901, 0.09302859507838426, 0.1014381740505941, 0.1091300643603039, 0.11590208274798985, 0.12156884616870442, 0.12597017671006355, 0.12897861453728923] + [0.13050554772183512] * 2 + [0.12897861453728923, 0.12597017671006355, 0.12156884616870442, 0.11590208274798985, 0.1091300643603039, 0.1014381740505941, 0.09302859507838426, 0.08411154398773901, 0.0748966677809916, 0.06558508740244534, 0.056362492034498786, 0.047393586268981804, 0.038818075745266994, 0.030748257453465856, 0.023268168919768663, 0.016434154497699333, 0.010276633116185457, 0.004802803434016331, 0.0],
        },
        "x180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.003634367603238432, -0.004169480251085156, -0.004721948521966005, -0.005277122862727259, -0.005817442195638354, -0.006322845254566657, -0.00677141680086321, -0.007140260785318733, -0.007406571830510348, -0.007548855128053024, -0.0075482251377865725, -0.0073896976403955705, -0.007063379901060598, -0.006565461700368211, -0.0058989168432571435, -0.0050738406359252175, -0.004107372889204763, -0.0030231864402277178, -0.0018505553144826212, -0.000623051234863889, 0.000623051234863889, 0.0018505553144826212, 0.0030231864402277178, 0.004107372889204763, 0.0050738406359252175, 0.0058989168432571435, 0.006565461700368211, 0.007063379901060598, 0.0073896976403955705, 0.0075482251377865725, 0.007548855128053024, 0.007406571830510348, 0.007140260785318733, 0.00677141680086321, 0.006322845254566657, 0.005817442195638354, 0.005277122862727259, 0.004721948521966005, 0.004169480251085156, 0.003634367603238432],
        },
        "minus_x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.0026246360206212457, -0.00561597446533303, -0.00898093674990273, -0.012715588951275178, -0.01680330773317002, -0.021213302033273505, -0.02589964702427318, -0.030800974647012896, -0.035840938563688335, -0.0409295310089563, -0.04596527655841962, -0.05083826663843542, -0.05543393335516866, -0.05963739757161887, -0.0633381701801215, -0.06643494305427361, -0.06884018216851553, -0.07048423327233783] + [-0.07131867171902846] * 2 + [-0.07048423327233783, -0.06884018216851553, -0.06643494305427361, -0.0633381701801215, -0.05963739757161887, -0.05543393335516866, -0.05083826663843542, -0.04596527655841962, -0.0409295310089563, -0.035840938563688335, -0.030800974647012896, -0.02589964702427318, -0.021213302033273505, -0.01680330773317002, -0.012715588951275178, -0.00898093674990273, -0.00561597446533303, -0.0026246360206212457, 0.0],
        },
        "minus_x90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0019861092078177385, 0.0022785375676130162, 0.0025804504282839827, 0.002883842102023192, 0.0031791158110724476, 0.003455308474715587, 0.0037004438533357266, 0.003902009713960981, 0.004047543373937295, 0.004125298350378418, 0.004124954073297606, 0.004038321966523372, 0.0038599958483315957, 0.00358789351001722, 0.003223640076503164, 0.0027727524307204128, 0.0022445971364926194, 0.0016521109258556435, 0.001011291468258463, 0.000340485038828418, -0.000340485038828418, -0.001011291468258463, -0.0016521109258556435, -0.0022445971364926194, -0.0027727524307204128, -0.003223640076503164, -0.00358789351001722, -0.0038599958483315957, -0.004038321966523372, -0.004124954073297606, -0.004125298350378418, -0.004047543373937295, -0.003902009713960981, -0.0037004438533357266, -0.003455308474715587, -0.0031791158110724476, -0.002883842102023192, -0.0025804504282839827, -0.0022785375676130162, -0.0019861092078177385],
        },
        "y90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0019861092078177385, 0.0022785375676130162, 0.0025804504282839827, 0.002883842102023192, 0.0031791158110724476, 0.003455308474715587, 0.0037004438533357266, 0.003902009713960981, 0.004047543373937295, 0.004125298350378418, 0.004124954073297606, 0.004038321966523372, 0.0038599958483315957, 0.00358789351001722, 0.003223640076503164, 0.0027727524307204128, 0.0022445971364926194, 0.0016521109258556435, 0.001011291468258463, 0.000340485038828418, -0.000340485038828418, -0.001011291468258463, -0.0016521109258556435, -0.0022445971364926194, -0.0027727524307204128, -0.003223640076503164, -0.00358789351001722, -0.0038599958483315957, -0.004038321966523372, -0.004124954073297606, -0.004125298350378418, -0.004047543373937295, -0.003902009713960981, -0.0037004438533357266, -0.003455308474715587, -0.0031791158110724476, -0.002883842102023192, -0.0025804504282839827, -0.0022785375676130162, -0.0019861092078177385],
        },
        "y90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0026246360206212457, 0.00561597446533303, 0.00898093674990273, 0.012715588951275178, 0.01680330773317002, 0.021213302033273505, 0.02589964702427318, 0.030800974647012896, 0.035840938563688335, 0.0409295310089563, 0.04596527655841962, 0.05083826663843542, 0.05543393335516866, 0.05963739757161887, 0.0633381701801215, 0.06643494305427361, 0.06884018216851553, 0.07048423327233783] + [0.07131867171902846] * 2 + [0.07048423327233783, 0.06884018216851553, 0.06643494305427361, 0.0633381701801215, 0.05963739757161887, 0.05543393335516866, 0.05083826663843542, 0.04596527655841962, 0.0409295310089563, 0.035840938563688335, 0.030800974647012896, 0.02589964702427318, 0.021213302033273505, 0.01680330773317002, 0.012715588951275178, 0.00898093674990273, 0.00561597446533303, 0.0026246360206212457, 0.0],
        },
        "y180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.003634367603238432, 0.004169480251085156, 0.004721948521966005, 0.005277122862727259, 0.005817442195638354, 0.006322845254566657, 0.00677141680086321, 0.007140260785318733, 0.007406571830510348, 0.007548855128053024, 0.0075482251377865725, 0.0073896976403955705, 0.007063379901060598, 0.006565461700368211, 0.0058989168432571435, 0.0050738406359252175, 0.004107372889204763, 0.0030231864402277178, 0.0018505553144826212, 0.000623051234863889, -0.000623051234863889, -0.0018505553144826212, -0.0030231864402277178, -0.004107372889204763, -0.0050738406359252175, -0.0058989168432571435, -0.006565461700368211, -0.007063379901060598, -0.0073896976403955705, -0.0075482251377865725, -0.007548855128053024, -0.007406571830510348, -0.007140260785318733, -0.00677141680086321, -0.006322845254566657, -0.005817442195638354, -0.005277122862727259, -0.004721948521966005, -0.004169480251085156, -0.003634367603238432],
        },
        "y180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.004802803434016331, 0.010276633116185457, 0.016434154497699333, 0.023268168919768663, 0.030748257453465856, 0.038818075745266994, 0.047393586268981804, 0.056362492034498786, 0.06558508740244534, 0.0748966677809916, 0.08411154398773901, 0.09302859507838426, 0.1014381740505941, 0.1091300643603039, 0.11590208274798985, 0.12156884616870442, 0.12597017671006355, 0.12897861453728923] + [0.13050554772183512] * 2 + [0.12897861453728923, 0.12597017671006355, 0.12156884616870442, 0.11590208274798985, 0.1091300643603039, 0.1014381740505941, 0.09302859507838426, 0.08411154398773901, 0.0748966677809916, 0.06558508740244534, 0.056362492034498786, 0.047393586268981804, 0.038818075745266994, 0.030748257453465856, 0.023268168919768663, 0.016434154497699333, 0.010276633116185457, 0.004802803434016331, 0.0],
        },
        "minus_y90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.0019861092078177385, -0.0022785375676130162, -0.0025804504282839827, -0.002883842102023192, -0.0031791158110724476, -0.003455308474715587, -0.0037004438533357266, -0.003902009713960981, -0.004047543373937295, -0.004125298350378418, -0.004124954073297606, -0.004038321966523372, -0.0038599958483315957, -0.00358789351001722, -0.003223640076503164, -0.0027727524307204128, -0.0022445971364926194, -0.0016521109258556435, -0.001011291468258463, -0.000340485038828418, 0.000340485038828418, 0.001011291468258463, 0.0016521109258556435, 0.0022445971364926194, 0.0027727524307204128, 0.003223640076503164, 0.00358789351001722, 0.0038599958483315957, 0.004038321966523372, 0.004124954073297606, 0.004125298350378418, 0.004047543373937295, 0.003902009713960981, 0.0037004438533357266, 0.003455308474715587, 0.0031791158110724476, 0.002883842102023192, 0.0025804504282839827, 0.0022785375676130162, 0.0019861092078177385],
        },
        "minus_y90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.0026246360206212457, -0.00561597446533303, -0.00898093674990273, -0.012715588951275178, -0.01680330773317002, -0.021213302033273505, -0.02589964702427318, -0.030800974647012896, -0.035840938563688335, -0.0409295310089563, -0.04596527655841962, -0.05083826663843542, -0.05543393335516866, -0.05963739757161887, -0.0633381701801215, -0.06643494305427361, -0.06884018216851553, -0.07048423327233783] + [-0.07131867171902846] * 2 + [-0.07048423327233783, -0.06884018216851553, -0.06643494305427361, -0.0633381701801215, -0.05963739757161887, -0.05543393335516866, -0.05083826663843542, -0.04596527655841962, -0.0409295310089563, -0.035840938563688335, -0.030800974647012896, -0.02589964702427318, -0.021213302033273505, -0.01680330773317002, -0.012715588951275178, -0.00898093674990273, -0.00561597446533303, -0.0026246360206212457, 0.0],
        },
        "readout_wf_q4": {
            "type": "constant",
            "sample": 0.03,
        },
        "x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.007814519092118992, 0.016720847894867323, 0.026739594041163897, 0.03785904477671438, 0.05002970623733462, 0.06315990196105921, 0.07711289663029906, 0.09170597467376958, 0.10671182460534549, 0.12186245978033129, 0.1368557500614042, 0.15136445668464732, 0.16504746835436723, 0.17756274708803105, 0.18858132565569452, 0.19780157202848103, 0.20496286480648152, 0.20985781734020376] + [0.21234225141854074] * 2 + [0.20985781734020376, 0.20496286480648152, 0.19780157202848103, 0.18858132565569452, 0.17756274708803105, 0.16504746835436723, 0.15136445668464732, 0.1368557500614042, 0.12186245978033129, 0.10671182460534549, 0.09170597467376958, 0.07711289663029906, 0.06315990196105921, 0.05002970623733462, 0.03785904477671438, 0.026739594041163897, 0.016720847894867323, 0.007814519092118992, 0.0],
        },
        "x90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0] * 40,
        },
        "x180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.015629038184237984, 0.033441695789734646, 0.053479188082327794, 0.07571808955342876, 0.10005941247466923, 0.12631980392211842, 0.15422579326059813, 0.18341194934753915, 0.21342364921069099, 0.24372491956066258, 0.2737115001228084, 0.30272891336929464, 0.33009493670873447, 0.3551254941760621, 0.37716265131138904, 0.39560314405696206, 0.40992572961296303, 0.4197156346804075] + [0.4246845028370815] * 2 + [0.4197156346804075, 0.40992572961296303, 0.39560314405696206, 0.37716265131138904, 0.3551254941760621, 0.33009493670873447, 0.30272891336929464, 0.2737115001228084, 0.24372491956066258, 0.21342364921069099, 0.18341194934753915, 0.15422579326059813, 0.12631980392211842, 0.10005941247466923, 0.07571808955342876, 0.053479188082327794, 0.033441695789734646, 0.015629038184237984, 0.0],
        },
        "x180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0] * 40,
        },
        "minus_x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.007814519092118992, -0.016720847894867323, -0.026739594041163897, -0.03785904477671438, -0.05002970623733462, -0.06315990196105921, -0.07711289663029906, -0.09170597467376958, -0.10671182460534549, -0.12186245978033129, -0.1368557500614042, -0.15136445668464732, -0.16504746835436723, -0.17756274708803105, -0.18858132565569452, -0.19780157202848103, -0.20496286480648152, -0.20985781734020376] + [-0.21234225141854074] * 2 + [-0.20985781734020376, -0.20496286480648152, -0.19780157202848103, -0.18858132565569452, -0.17756274708803105, -0.16504746835436723, -0.15136445668464732, -0.1368557500614042, -0.12186245978033129, -0.10671182460534549, -0.09170597467376958, -0.07711289663029906, -0.06315990196105921, -0.05002970623733462, -0.03785904477671438, -0.026739594041163897, -0.016720847894867323, -0.007814519092118992, 0.0],
        },
        "minus_x90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0] * 40,
        },
        "y90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0] * 40,
        },
        "y90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.007814519092118992, 0.016720847894867323, 0.026739594041163897, 0.03785904477671438, 0.05002970623733462, 0.06315990196105921, 0.07711289663029906, 0.09170597467376958, 0.10671182460534549, 0.12186245978033129, 0.1368557500614042, 0.15136445668464732, 0.16504746835436723, 0.17756274708803105, 0.18858132565569452, 0.19780157202848103, 0.20496286480648152, 0.20985781734020376] + [0.21234225141854074] * 2 + [0.20985781734020376, 0.20496286480648152, 0.19780157202848103, 0.18858132565569452, 0.17756274708803105, 0.16504746835436723, 0.15136445668464732, 0.1368557500614042, 0.12186245978033129, 0.10671182460534549, 0.09170597467376958, 0.07711289663029906, 0.06315990196105921, 0.05002970623733462, 0.03785904477671438, 0.026739594041163897, 0.016720847894867323, 0.007814519092118992, 0.0],
        },
        "y180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0] * 40,
        },
        "y180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.015629038184237984, 0.033441695789734646, 0.053479188082327794, 0.07571808955342876, 0.10005941247466923, 0.12631980392211842, 0.15422579326059813, 0.18341194934753915, 0.21342364921069099, 0.24372491956066258, 0.2737115001228084, 0.30272891336929464, 0.33009493670873447, 0.3551254941760621, 0.37716265131138904, 0.39560314405696206, 0.40992572961296303, 0.4197156346804075] + [0.4246845028370815] * 2 + [0.4197156346804075, 0.40992572961296303, 0.39560314405696206, 0.37716265131138904, 0.3551254941760621, 0.33009493670873447, 0.30272891336929464, 0.2737115001228084, 0.24372491956066258, 0.21342364921069099, 0.18341194934753915, 0.15422579326059813, 0.12631980392211842, 0.10005941247466923, 0.07571808955342876, 0.053479188082327794, 0.033441695789734646, 0.015629038184237984, 0.0],
        },
        "minus_y90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0] * 40,
        },
        "minus_y90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.007814519092118992, -0.016720847894867323, -0.026739594041163897, -0.03785904477671438, -0.05002970623733462, -0.06315990196105921, -0.07711289663029906, -0.09170597467376958, -0.10671182460534549, -0.12186245978033129, -0.1368557500614042, -0.15136445668464732, -0.16504746835436723, -0.17756274708803105, -0.18858132565569452, -0.19780157202848103, -0.20496286480648152, -0.20985781734020376] + [-0.21234225141854074] * 2 + [-0.20985781734020376, -0.20496286480648152, -0.19780157202848103, -0.18858132565569452, -0.17756274708803105, -0.16504746835436723, -0.15136445668464732, -0.1368557500614042, -0.12186245978033129, -0.10671182460534549, -0.09170597467376958, -0.07711289663029906, -0.06315990196105921, -0.05002970623733462, -0.03785904477671438, -0.026739594041163897, -0.016720847894867323, -0.007814519092118992, 0.0],
        },
        "readout_wf_q5": {
            "type": "constant",
            "sample": 0.02,
        },
        "gft_cz_wf_1_2_q2": {
            "type": "arbitrary",
            "samples": [8.2642507797802e-06, 0.0001272704153343253, 0.0013261881815880992, 0.009350537220869926, 0.04460891818882727, 0.1439993518360818, 0.3145235010372933, 0.464835601738604] + [0.48809590999999997] * 8 + [0.464835601738604, 0.3145235010372933, 0.1439993518360818, 0.04460891818882727, 0.009350537220869926, 0.0013261881815880992, 0.0001272704153343253, 8.2642507797802e-06],
        },
        "g_cz_wf_1_2_q2": {
            "type": "arbitrary",
            "samples": [0.07266709339002213, 0.1125489959561424, 0.16375782284008586, 0.22383040542184623, 0.2874039295891722, 0.3466753136729172, 0.3928345954049229] + [0.41817025007977965] * 2 + [0.3928345954049229, 0.3466753136729172, 0.2874039295891722, 0.22383040542184623, 0.16375782284008586, 0.1125489959561424, 0.07266709339002213],
        },
        "q2_xy_baked_wf_I_0": {
            "type": "arbitrary",
            "samples": [0.0] * 40,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_0": {
            "type": "arbitrary",
            "samples": [0.0] * 40,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_0": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_0": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q2_z_baked_wf_0": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_1": {
            "type": "arbitrary",
            "samples": [0.0, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271, -0.0],
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_1": {
            "type": "arbitrary",
            "samples": [-0.0003798576395459785, -0.00043578666200400735, -0.0004935296633211693, -0.0005515554982505122, -0.0006080287141733543, -0.0006608525432248669, -0.0007077364436294015, -0.0007462873610355451, -0.0007741217179457732, -0.000788992915208048, -0.0007889270697455971, -0.0007723580575993246, -0.0007382519077163814, -0.0006862103827387051, -0.0006165442994707075, -0.0005303088013655113, -0.00042929531097465857, -0.00031597807114201563, -0.00019341675095889237, -6.512020720763538e-05, 6.512020720763538e-05, 0.00019341675095889237, 0.00031597807114201563, 0.00042929531097465857, 0.0005303088013655113, 0.0006165442994707075, 0.0006862103827387051, 0.0007382519077163814, 0.0007723580575993246, 0.0007889270697455971, 0.000788992915208048, 0.0007741217179457732, 0.0007462873610355451, 0.0007077364436294015, 0.0006608525432248669, 0.0006080287141733543, 0.0005515554982505122, 0.0004935296633211693, 0.00043578666200400735, 0.0003798576395459785],
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_1": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_1": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q2_z_baked_wf_1": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_2": {
            "type": "arbitrary",
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20],
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_2": {
            "type": "arbitrary",
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785],
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_2": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_2": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q2_z_baked_wf_2": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_3": {
            "type": "arbitrary",
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20],
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_3": {
            "type": "arbitrary",
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785],
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_3": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_3": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q2_z_baked_wf_3": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 0.0],
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_4": {
            "type": "arbitrary",
            "samples": [0.0003798576395459785, 0.00043578666200400735, 0.0004935296633211693, 0.0005515554982505122, 0.0006080287141733543, 0.0006608525432248669, 0.0007077364436294015, 0.0007462873610355451, 0.0007741217179457732, 0.000788992915208048, 0.0007889270697455971, 0.0007723580575993246, 0.0007382519077163814, 0.0006862103827387051, 0.0006165442994707075, 0.0005303088013655113, 0.00042929531097465857, 0.00031597807114201563, 0.00019341675095889237, 6.512020720763538e-05, -6.512020720763538e-05, -0.00019341675095889237, -0.00031597807114201563, -0.00042929531097465857, -0.0005303088013655113, -0.0006165442994707075, -0.0006862103827387051, -0.0007382519077163814, -0.0007723580575993246, -0.0007889270697455971, -0.000788992915208048, -0.0007741217179457732, -0.0007462873610355451, -0.0007077364436294015, -0.0006608525432248669, -0.0006080287141733543, -0.0005515554982505122, -0.0004935296633211693, -0.00043578666200400735, -0.0003798576395459785],
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_4": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_4": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q2_z_baked_wf_4": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_5": {
            "type": "arbitrary",
            "samples": [0.0] * 40,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_5": {
            "type": "arbitrary",
            "samples": [0.0] * 40,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_5": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_5": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q2_z_baked_wf_5": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_6": {
            "type": "arbitrary",
            "samples": [0.0] * 148,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_6": {
            "type": "arbitrary",
            "samples": [0.0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_6": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_6": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q2_z_baked_wf_6": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 63,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_7": {
            "type": "arbitrary",
            "samples": [0] * 105 + [-0.00015778376362709102, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009117, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.004863811454255249, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709102] + [0] * 3,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_7": {
            "type": "arbitrary",
            "samples": [0] * 105 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789555, 0.0016217826115637818, 0.002138921749805219, 0.0026967740303955536, 0.003289415745753081, 0.003908942525632037, 0.004545532613031832, 0.005187620832681907, 0.005822186296327271, 0.006435148841109958, 0.007011860634169721, 0.007537671049128935, 0.007998535633794194, 0.00838163451640098, 0.008675962590192947, 0.008872853716940653, 0.008966404172880875, 0.008953766494256924, 0.008835293328522899, 0.008614521158764746, 0.008297994944280965, 0.007894945810504669, 0.007416843935897081, 0.006876856847658553, 0.0062892487868441245, 0.005668759247261229, 0.005029998149985528, 0.0043868916083357025, 0.0037522063520680432, 0.0031371732953768216, 0.0025512222418611025, 0.002001831129893861, 0.0014944852749314576, 0.0010327353644391084, 0.0006183379243041822, 0.00025145881453495536, -6.908096354474362e-05, -0.00034553742236856605] + [0] * 3,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_7": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_7": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q2_z_baked_wf_7": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 63,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_8": {
            "type": "arbitrary",
            "samples": [0] * 105 + [-0.0001577837636270911, 0.0005358236462419261, 0.0013288311147143371, 0.0022237650156902507, 0.003220313321556805, 0.004314806824009116, 0.005499787323106856, 0.006763705875530091, 0.008090791755457433, 0.009461126481233454, 0.01085094709073768, 0.012233189208447764, 0.013578264158704062, 0.01485504664661625, 0.016032031846637824, 0.017078604759892795, 0.01796635205879739, 0.018670338762580556, 0.01917027003166739, 0.019451462661092028, 0.019505561409210812, 0.01933095140141051, 0.018932838204992752, 0.018322990034824432, 0.017519159903993792, 0.01654422731086274, 0.015425117354989585, 0.014191568472623336, 0.012874827277601197, 0.011506349901330282, 0.010116583993081482, 0.00873389498912647, 0.007383685659073526, 0.006087740851514874, 0.00486381145425525, 0.0037254344455140884, 0.002681970897594845, 0.0017388319130844834, 0.0008978543256915442, 0.0001577837636270911] + [0] * 3,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_8": {
            "type": "arbitrary",
            "samples": [0] * 105 + [0.000345537422368566, 0.0007237455283559925, 0.001149337124578956, 0.0016217826115637827, 0.0021389217498052194, 0.0026967740303955544, 0.003289415745753082, 0.003908942525632038, 0.004545532613031834, 0.00518762083268191, 0.0058221862963272735, 0.00643514884110996, 0.0070118606341697245, 0.007537671049128939, 0.007998535633794197, 0.008381634516400985, 0.00867596259019295, 0.008872853716940658, 0.00896640417288088, 0.008953766494256929, 0.008835293328522904, 0.008614521158764751, 0.00829799494428097, 0.007894945810504672, 0.007416843935897087, 0.006876856847658557, 0.006289248786844128, 0.005668759247261232, 0.005029998149985531, 0.004386891608335705, 0.0037522063520680463, 0.0031371732953768237, 0.002551222241861104, 0.002001831129893863, 0.0014944852749314585, 0.0010327353644391094, 0.0006183379243041828, 0.00025145881453495585, -6.90809635447434e-05, -0.000345537422368566] + [0] * 3,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_8": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_8": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q2_z_baked_wf_8": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 63,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_9": {
            "type": "arbitrary",
            "samples": [0.0, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271] + [0] * 109,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_9": {
            "type": "arbitrary",
            "samples": [-0.0003798576395459785, -0.00043578666200400735, -0.0004935296633211693, -0.0005515554982505122, -0.0006080287141733543, -0.0006608525432248669, -0.0007077364436294015, -0.0007462873610355451, -0.0007741217179457732, -0.000788992915208048, -0.0007889270697455971, -0.0007723580575993246, -0.0007382519077163814, -0.0006862103827387051, -0.0006165442994707075, -0.0005303088013655113, -0.00042929531097465857, -0.00031597807114201563, -0.00019341675095889237, -6.512020720763538e-05, 6.512020720763538e-05, 0.00019341675095889237, 0.00031597807114201563, 0.00042929531097465857, 0.0005303088013655113, 0.0006165442994707075, 0.0006862103827387051, 0.0007382519077163814, 0.0007723580575993246, 0.0007889270697455971, 0.000788992915208048, 0.0007741217179457732, 0.0007462873610355451, 0.0007077364436294015, 0.0006608525432248669, 0.0006080287141733543, 0.0005515554982505122, 0.0004935296633211693, 0.00043578666200400735, 0.0003798576395459785] + [0] * 108,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_9": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_9": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q2_z_baked_wf_9": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 63,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_10": {
            "type": "arbitrary",
            "samples": [0.0, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271] + [0] * 66 + [-0.00015778376362709102, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009117, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.004863811454255249, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709102] + [0] * 3,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_10": {
            "type": "arbitrary",
            "samples": [-0.0003798576395459785, -0.00043578666200400735, -0.0004935296633211693, -0.0005515554982505122, -0.0006080287141733543, -0.0006608525432248669, -0.0007077364436294015, -0.0007462873610355451, -0.0007741217179457732, -0.000788992915208048, -0.0007889270697455971, -0.0007723580575993246, -0.0007382519077163814, -0.0006862103827387051, -0.0006165442994707075, -0.0005303088013655113, -0.00042929531097465857, -0.00031597807114201563, -0.00019341675095889237, -6.512020720763538e-05, 6.512020720763538e-05, 0.00019341675095889237, 0.00031597807114201563, 0.00042929531097465857, 0.0005303088013655113, 0.0006165442994707075, 0.0006862103827387051, 0.0007382519077163814, 0.0007723580575993246, 0.0007889270697455971, 0.000788992915208048, 0.0007741217179457732, 0.0007462873610355451, 0.0007077364436294015, 0.0006608525432248669, 0.0006080287141733543, 0.0005515554982505122, 0.0004935296633211693, 0.00043578666200400735, 0.0003798576395459785] + [0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789555, 0.0016217826115637818, 0.002138921749805219, 0.0026967740303955536, 0.003289415745753081, 0.003908942525632037, 0.004545532613031832, 0.005187620832681907, 0.005822186296327271, 0.006435148841109958, 0.007011860634169721, 0.007537671049128935, 0.007998535633794194, 0.00838163451640098, 0.008675962590192947, 0.008872853716940653, 0.008966404172880875, 0.008953766494256924, 0.008835293328522899, 0.008614521158764746, 0.008297994944280965, 0.007894945810504669, 0.007416843935897081, 0.006876856847658553, 0.0062892487868441245, 0.005668759247261229, 0.005029998149985528, 0.0043868916083357025, 0.0037522063520680432, 0.0031371732953768216, 0.0025512222418611025, 0.002001831129893861, 0.0014944852749314576, 0.0010327353644391084, 0.0006183379243041822, 0.00025145881453495536, -6.908096354474362e-05, -0.00034553742236856605] + [0] * 3,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_10": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_10": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q2_z_baked_wf_10": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 63,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_11": {
            "type": "arbitrary",
            "samples": [0.0, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271] + [0] * 66 + [-0.0001577837636270911, 0.0005358236462419261, 0.0013288311147143371, 0.0022237650156902507, 0.003220313321556805, 0.004314806824009116, 0.005499787323106856, 0.006763705875530091, 0.008090791755457433, 0.009461126481233454, 0.01085094709073768, 0.012233189208447764, 0.013578264158704062, 0.01485504664661625, 0.016032031846637824, 0.017078604759892795, 0.01796635205879739, 0.018670338762580556, 0.01917027003166739, 0.019451462661092028, 0.019505561409210812, 0.01933095140141051, 0.018932838204992752, 0.018322990034824432, 0.017519159903993792, 0.01654422731086274, 0.015425117354989585, 0.014191568472623336, 0.012874827277601197, 0.011506349901330282, 0.010116583993081482, 0.00873389498912647, 0.007383685659073526, 0.006087740851514874, 0.00486381145425525, 0.0037254344455140884, 0.002681970897594845, 0.0017388319130844834, 0.0008978543256915442, 0.0001577837636270911] + [0] * 3,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_11": {
            "type": "arbitrary",
            "samples": [-0.0003798576395459785, -0.00043578666200400735, -0.0004935296633211693, -0.0005515554982505122, -0.0006080287141733543, -0.0006608525432248669, -0.0007077364436294015, -0.0007462873610355451, -0.0007741217179457732, -0.000788992915208048, -0.0007889270697455971, -0.0007723580575993246, -0.0007382519077163814, -0.0006862103827387051, -0.0006165442994707075, -0.0005303088013655113, -0.00042929531097465857, -0.00031597807114201563, -0.00019341675095889237, -6.512020720763538e-05, 6.512020720763538e-05, 0.00019341675095889237, 0.00031597807114201563, 0.00042929531097465857, 0.0005303088013655113, 0.0006165442994707075, 0.0006862103827387051, 0.0007382519077163814, 0.0007723580575993246, 0.0007889270697455971, 0.000788992915208048, 0.0007741217179457732, 0.0007462873610355451, 0.0007077364436294015, 0.0006608525432248669, 0.0006080287141733543, 0.0005515554982505122, 0.0004935296633211693, 0.00043578666200400735, 0.0003798576395459785] + [0] * 65 + [0.000345537422368566, 0.0007237455283559925, 0.001149337124578956, 0.0016217826115637827, 0.0021389217498052194, 0.0026967740303955544, 0.003289415745753082, 0.003908942525632038, 0.004545532613031834, 0.00518762083268191, 0.0058221862963272735, 0.00643514884110996, 0.0070118606341697245, 0.007537671049128939, 0.007998535633794197, 0.008381634516400985, 0.00867596259019295, 0.008872853716940658, 0.00896640417288088, 0.008953766494256929, 0.008835293328522904, 0.008614521158764751, 0.00829799494428097, 0.007894945810504672, 0.007416843935897087, 0.006876856847658557, 0.006289248786844128, 0.005668759247261232, 0.005029998149985531, 0.004386891608335705, 0.0037522063520680463, 0.0031371732953768237, 0.002551222241861104, 0.002001831129893863, 0.0014944852749314585, 0.0010327353644391094, 0.0006183379243041828, 0.00025145881453495585, -6.90809635447434e-05, -0.000345537422368566] + [0] * 3,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_11": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_11": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q2_z_baked_wf_11": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 63,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_12": {
            "type": "arbitrary",
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20] + [0] * 108,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_12": {
            "type": "arbitrary",
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785] + [0] * 108,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_12": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_12": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q2_z_baked_wf_12": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 63,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_13": {
            "type": "arbitrary",
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20] + [0] * 65 + [-0.000157783763627091, 0.0005358236462419265, 0.0013288311147143378, 0.0022237650156902516, 0.0032203133215568057, 0.004314806824009118, 0.005499787323106857, 0.006763705875530093, 0.008090791755457434, 0.009461126481233456, 0.010850947090737683, 0.012233189208447768, 0.013578264158704065, 0.014855046646616254, 0.016032031846637828, 0.0170786047598928, 0.017966352058797392, 0.01867033876258056, 0.019170270031667394, 0.019451462661092035, 0.01950556140921082, 0.019330951401410515, 0.018932838204992756, 0.018322990034824436, 0.017519159903993796, 0.016544227310862743, 0.015425117354989588, 0.01419156847262334, 0.0128748272776012, 0.011506349901330285, 0.010116583993081484, 0.008733894989126472, 0.007383685659073528, 0.006087740851514875, 0.00486381145425525, 0.0037254344455140893, 0.0026819708975948458, 0.0017388319130844836, 0.0008978543256915441, 0.000157783763627091] + [0] * 3,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_13": {
            "type": "arbitrary",
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785] + [0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789555, 0.0016217826115637818, 0.0021389217498052186, 0.002696774030395553, 0.0032894157457530803, 0.0039089425256320365, 0.004545532613031832, 0.0051876208326819065, 0.005822186296327269, 0.006435148841109956, 0.007011860634169719, 0.007537671049128934, 0.007998535633794192, 0.008381634516400978, 0.008675962590192945, 0.008872853716940651, 0.008966404172880874, 0.008953766494256922, 0.008835293328522897, 0.008614521158764744, 0.008297994944280964, 0.007894945810504667, 0.00741684393589708, 0.006876856847658552, 0.006289248786844123, 0.005668759247261227, 0.0050299981499855265, 0.004386891608335701, 0.0037522063520680424, 0.0031371732953768207, 0.002551222241861101, 0.0020018311298938603, 0.0014944852749314572, 0.0010327353644391077, 0.0006183379243041819, 0.0002514588145349552, -6.908096354474373e-05, -0.00034553742236856605] + [0] * 3,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_13": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_13": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q2_z_baked_wf_13": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 63,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_14": {
            "type": "arbitrary",
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20] + [0] * 65 + [-0.00015778376362709102, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009117, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.004863811454255249, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709102] + [0] * 3,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_14": {
            "type": "arbitrary",
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785] + [0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789555, 0.0016217826115637818, 0.002138921749805219, 0.0026967740303955536, 0.003289415745753081, 0.003908942525632037, 0.004545532613031832, 0.005187620832681907, 0.005822186296327271, 0.006435148841109958, 0.007011860634169721, 0.007537671049128935, 0.007998535633794194, 0.00838163451640098, 0.008675962590192947, 0.008872853716940653, 0.008966404172880875, 0.008953766494256924, 0.008835293328522899, 0.008614521158764746, 0.008297994944280965, 0.007894945810504669, 0.007416843935897081, 0.006876856847658553, 0.0062892487868441245, 0.005668759247261229, 0.005029998149985528, 0.0043868916083357025, 0.0037522063520680432, 0.0031371732953768216, 0.0025512222418611025, 0.002001831129893861, 0.0014944852749314576, 0.0010327353644391084, 0.0006183379243041822, 0.00025145881453495536, -6.908096354474362e-05, -0.00034553742236856605] + [0] * 3,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_14": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_14": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q2_z_baked_wf_14": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 63,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_15": {
            "type": "arbitrary",
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20] + [0] * 108,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_15": {
            "type": "arbitrary",
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785] + [0] * 108,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_15": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_15": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q2_z_baked_wf_15": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 63,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_16": {
            "type": "arbitrary",
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20] + [0] * 65 + [0.0001577837636270911, -0.0005358236462419261, -0.0013288311147143371, -0.0022237650156902507, -0.003220313321556805, -0.004314806824009116, -0.005499787323106856, -0.006763705875530091, -0.008090791755457433, -0.009461126481233454, -0.01085094709073768, -0.012233189208447764, -0.013578264158704062, -0.01485504664661625, -0.016032031846637824, -0.017078604759892795, -0.01796635205879739, -0.018670338762580556, -0.01917027003166739, -0.019451462661092028, -0.019505561409210812, -0.01933095140141051, -0.018932838204992752, -0.018322990034824432, -0.017519159903993792, -0.01654422731086274, -0.015425117354989585, -0.014191568472623336, -0.012874827277601197, -0.011506349901330282, -0.010116583993081482, -0.00873389498912647, -0.007383685659073526, -0.006087740851514874, -0.00486381145425525, -0.0037254344455140884, -0.002681970897594845, -0.0017388319130844834, -0.0008978543256915442, -0.0001577837636270911] + [0] * 3,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_16": {
            "type": "arbitrary",
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785] + [0] * 65 + [-0.000345537422368566, -0.0007237455283559925, -0.001149337124578956, -0.0016217826115637827, -0.0021389217498052194, -0.0026967740303955544, -0.003289415745753082, -0.003908942525632038, -0.004545532613031834, -0.00518762083268191, -0.0058221862963272735, -0.00643514884110996, -0.0070118606341697245, -0.007537671049128939, -0.007998535633794197, -0.008381634516400985, -0.00867596259019295, -0.008872853716940658, -0.00896640417288088, -0.008953766494256929, -0.008835293328522904, -0.008614521158764751, -0.00829799494428097, -0.007894945810504672, -0.007416843935897087, -0.006876856847658557, -0.006289248786844128, -0.005668759247261232, -0.005029998149985531, -0.004386891608335705, -0.0037522063520680463, -0.0031371732953768237, -0.002551222241861104, -0.002001831129893863, -0.0014944852749314585, -0.0010327353644391094, -0.0006183379243041828, -0.00025145881453495585, 6.90809635447434e-05, 0.000345537422368566] + [0] * 3,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_16": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_16": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q2_z_baked_wf_16": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 63,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_17": {
            "type": "arbitrary",
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20] + [0] * 65 + [0.00015778376362709116, -0.0005358236462419261, -0.001328831114714337, -0.0022237650156902507, -0.003220313321556805, -0.004314806824009116, -0.005499787323106856, -0.00676370587553009, -0.008090791755457433, -0.009461126481233454, -0.01085094709073768, -0.012233189208447764, -0.013578264158704062, -0.01485504664661625, -0.016032031846637824, -0.017078604759892795, -0.01796635205879739, -0.018670338762580556, -0.01917027003166739, -0.019451462661092028, -0.019505561409210812, -0.01933095140141051, -0.018932838204992752, -0.018322990034824432, -0.017519159903993792, -0.01654422731086274, -0.015425117354989585, -0.014191568472623336, -0.012874827277601197, -0.011506349901330282, -0.010116583993081482, -0.00873389498912647, -0.007383685659073527, -0.006087740851514874, -0.00486381145425525, -0.0037254344455140884, -0.002681970897594845, -0.0017388319130844836, -0.0008978543256915442, -0.00015778376362709116] + [0] * 3,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_17": {
            "type": "arbitrary",
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785] + [0] * 65 + [-0.000345537422368566, -0.0007237455283559927, -0.001149337124578956, -0.0016217826115637827, -0.00213892174980522, -0.0026967740303955553, -0.003289415745753083, -0.00390894252563204, -0.004545532613031835, -0.005187620832681911, -0.005822186296327275, -0.006435148841109962, -0.007011860634169726, -0.007537671049128941, -0.0079985356337942, -0.008381634516400987, -0.008675962590192954, -0.00887285371694066, -0.008966404172880882, -0.00895376649425693, -0.008835293328522906, -0.008614521158764753, -0.008297994944280972, -0.007894945810504676, -0.007416843935897088, -0.006876856847658559, -0.00628924878684413, -0.005668759247261234, -0.005029998149985533, -0.004386891608335707, -0.003752206352068047, -0.0031371732953768246, -0.002551222241861105, -0.002001831129893864, -0.0014944852749314594, -0.0010327353644391099, -0.000618337924304183, -0.00025145881453495606, 6.90809635447433e-05, 0.000345537422368566] + [0] * 3,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_17": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_17": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q2_z_baked_wf_17": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 63,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_18": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271] + [0] * 109,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_18": {
            "type": "arbitrary",
            "samples": [0.0003798576395459785, 0.00043578666200400735, 0.0004935296633211693, 0.0005515554982505122, 0.0006080287141733543, 0.0006608525432248669, 0.0007077364436294015, 0.0007462873610355451, 0.0007741217179457732, 0.000788992915208048, 0.0007889270697455971, 0.0007723580575993246, 0.0007382519077163814, 0.0006862103827387051, 0.0006165442994707075, 0.0005303088013655113, 0.00042929531097465857, 0.00031597807114201563, 0.00019341675095889237, 6.512020720763538e-05, -6.512020720763538e-05, -0.00019341675095889237, -0.00031597807114201563, -0.00042929531097465857, -0.0005303088013655113, -0.0006165442994707075, -0.0006862103827387051, -0.0007382519077163814, -0.0007723580575993246, -0.0007889270697455971, -0.000788992915208048, -0.0007741217179457732, -0.0007462873610355451, -0.0007077364436294015, -0.0006608525432248669, -0.0006080287141733543, -0.0005515554982505122, -0.0004935296633211693, -0.00043578666200400735, -0.0003798576395459785] + [0] * 108,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_18": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_18": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q2_z_baked_wf_18": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 63,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_19": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271] + [0] * 66 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0] * 3,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_19": {
            "type": "arbitrary",
            "samples": [0.0003798576395459785, 0.00043578666200400735, 0.0004935296633211693, 0.0005515554982505122, 0.0006080287141733543, 0.0006608525432248669, 0.0007077364436294015, 0.0007462873610355451, 0.0007741217179457732, 0.000788992915208048, 0.0007889270697455971, 0.0007723580575993246, 0.0007382519077163814, 0.0006862103827387051, 0.0006165442994707075, 0.0005303088013655113, 0.00042929531097465857, 0.00031597807114201563, 0.00019341675095889237, 6.512020720763538e-05, -6.512020720763538e-05, -0.00019341675095889237, -0.00031597807114201563, -0.00042929531097465857, -0.0005303088013655113, -0.0006165442994707075, -0.0006862103827387051, -0.0007382519077163814, -0.0007723580575993246, -0.0007889270697455971, -0.000788992915208048, -0.0007741217179457732, -0.0007462873610355451, -0.0007077364436294015, -0.0006608525432248669, -0.0006080287141733543, -0.0005515554982505122, -0.0004935296633211693, -0.00043578666200400735, -0.0003798576395459785] + [0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0] * 3,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_19": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_19": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q2_z_baked_wf_19": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 63,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_20": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271] + [0] * 66 + [0.00015778376362709108, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009116, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.00486381145425525, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709108] + [0] * 3,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_20": {
            "type": "arbitrary",
            "samples": [0.0003798576395459785, 0.00043578666200400735, 0.0004935296633211693, 0.0005515554982505122, 0.0006080287141733543, 0.0006608525432248669, 0.0007077364436294015, 0.0007462873610355451, 0.0007741217179457732, 0.000788992915208048, 0.0007889270697455971, 0.0007723580575993246, 0.0007382519077163814, 0.0006862103827387051, 0.0006165442994707075, 0.0005303088013655113, 0.00042929531097465857, 0.00031597807114201563, 0.00019341675095889237, 6.512020720763538e-05, -6.512020720763538e-05, -0.00019341675095889237, -0.00031597807114201563, -0.00042929531097465857, -0.0005303088013655113, -0.0006165442994707075, -0.0006862103827387051, -0.0007382519077163814, -0.0007723580575993246, -0.0007889270697455971, -0.000788992915208048, -0.0007741217179457732, -0.0007462873610355451, -0.0007077364436294015, -0.0006608525432248669, -0.0006080287141733543, -0.0005515554982505122, -0.0004935296633211693, -0.00043578666200400735, -0.0003798576395459785] + [0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789557, -0.0016217826115637823, -0.002138921749805219, -0.002696774030395554, -0.003289415745753081, -0.003908942525632038, -0.0045455326130318325, -0.005187620832681909, -0.005822186296327273, -0.006435148841109959, -0.007011860634169723, -0.007537671049128937, -0.007998535633794195, -0.008381634516400982, -0.008675962590192949, -0.008872853716940654, -0.008966404172880879, -0.008953766494256927, -0.008835293328522903, -0.00861452115876475, -0.008297994944280967, -0.00789494581050467, -0.007416843935897083, -0.006876856847658555, -0.006289248786844126, -0.00566875924726123, -0.00502999814998553, -0.004386891608335704, -0.003752206352068045, -0.0031371732953768224, -0.0025512222418611033, -0.002001831129893862, -0.001494485274931458, -0.0010327353644391088, -0.0006183379243041826, -0.0002514588145349556, 6.908096354474351e-05, 0.00034553742236856605] + [0] * 3,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_20": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_20": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q2_z_baked_wf_20": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 63,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_21": {
            "type": "arbitrary",
            "samples": [0.0] * 148,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_21": {
            "type": "arbitrary",
            "samples": [0.0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_21": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_21": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q2_z_baked_wf_21": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 63,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_22": {
            "type": "arbitrary",
            "samples": [0] * 105 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0] * 3,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_22": {
            "type": "arbitrary",
            "samples": [0] * 105 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0] * 3,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_22": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_22": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q2_z_baked_wf_22": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 63,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_23": {
            "type": "arbitrary",
            "samples": [0] * 105 + [0.00015778376362709108, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009116, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.00486381145425525, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709108] + [0] * 3,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_23": {
            "type": "arbitrary",
            "samples": [0] * 105 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789557, -0.0016217826115637823, -0.002138921749805219, -0.002696774030395554, -0.003289415745753081, -0.003908942525632038, -0.0045455326130318325, -0.005187620832681909, -0.005822186296327273, -0.006435148841109959, -0.007011860634169723, -0.007537671049128937, -0.007998535633794195, -0.008381634516400982, -0.008675962590192949, -0.008872853716940654, -0.008966404172880879, -0.008953766494256927, -0.008835293328522903, -0.00861452115876475, -0.008297994944280967, -0.00789494581050467, -0.007416843935897083, -0.006876856847658555, -0.006289248786844126, -0.00566875924726123, -0.00502999814998553, -0.004386891608335704, -0.003752206352068045, -0.0031371732953768224, -0.0025512222418611033, -0.002001831129893862, -0.001494485274931458, -0.0010327353644391088, -0.0006183379243041826, -0.0002514588145349556, 6.908096354474351e-05, 0.00034553742236856605] + [0] * 3,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_23": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_23": {
            "type": "arbitrary",
            "samples": [0] * 148,
            "is_overridable": False,
        },
        "q2_z_baked_wf_23": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 63,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_24": {
            "type": "arbitrary",
            "samples": [0.0, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271] + [0] * 66 + [-0.00015778376362709108, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009116, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.00486381145425525, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709108] + [0] * 65 + [0.00028705593516813806, -0.00018678531325335427, -0.0007313638374660265, -0.0013491977358940606, -0.0020409004844246254, -0.002804787796534071, -0.0036365358884280635, -0.00452892255227461, -0.005471681673197406, -0.0064514983052773416, -0.007452165040045104, -0.00845491133631501, -0.009438906220329309, -0.010381922093328637, -0.011261134326336944, -0.012054019059648714, -0.0127393013734789, -0.013297898873999259, -0.013713802630057085, -0.013974838835556972, -0.014073260665380763, -0.014006130178820088, -0.01377546399978011, -0.01338813269408848, -0.01285552084903392, -0.0121929713201575, -0.011419051494620048, -0.010554690502106464, -0.009622243207138077, -0.008644539099210863, -0.0076439718824142175, -0.006641679117210861, -0.005656851513146753, -0.004706199496728453, -0.003803591690700294, -0.002959867133955371, -0.0021828115051823046, -0.0014772781184435272, -0.0008454275769439331, -0.00028705593516813806] + [0] * 2,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_24": {
            "type": "arbitrary",
            "samples": [-0.0003798576395459785, -0.00043578666200400735, -0.0004935296633211693, -0.0005515554982505122, -0.0006080287141733543, -0.0006608525432248669, -0.0007077364436294015, -0.0007462873610355451, -0.0007741217179457732, -0.000788992915208048, -0.0007889270697455971, -0.0007723580575993246, -0.0007382519077163814, -0.0006862103827387051, -0.0006165442994707075, -0.0005303088013655113, -0.00042929531097465857, -0.00031597807114201563, -0.00019341675095889237, -6.512020720763538e-05, 6.512020720763538e-05, 0.00019341675095889237, 0.00031597807114201563, 0.00042929531097465857, 0.0005303088013655113, 0.0006165442994707075, 0.0006862103827387051, 0.0007382519077163814, 0.0007723580575993246, 0.0007889270697455971, 0.000788992915208048, 0.0007741217179457732, 0.0007462873610355451, 0.0007077364436294015, 0.0006608525432248669, 0.0006080287141733543, 0.0005515554982505122, 0.0004935296633211693, 0.00043578666200400735, 0.0003798576395459785] + [0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789557, 0.0016217826115637823, 0.002138921749805219, 0.002696774030395554, 0.003289415745753081, 0.003908942525632038, 0.0045455326130318325, 0.005187620832681909, 0.005822186296327273, 0.006435148841109959, 0.007011860634169723, 0.007537671049128937, 0.007998535633794195, 0.008381634516400982, 0.008675962590192949, 0.008872853716940654, 0.008966404172880879, 0.008953766494256927, 0.008835293328522903, 0.00861452115876475, 0.008297994944280967, 0.00789494581050467, 0.007416843935897083, 0.006876856847658555, 0.006289248786844126, 0.00566875924726123, 0.00502999814998553, 0.004386891608335704, 0.003752206352068045, 0.0031371732953768224, 0.0025512222418611033, 0.002001831129893862, 0.001494485274931458, 0.0010327353644391088, 0.0006183379243041826, 0.0002514588145349556, -6.908096354474351e-05, -0.00034553742236856605] + [0] * 65 + [-0.0002487784484359292, -0.0008809232750019345, -0.0015974588866745014, -0.002398952928599652, -0.0032833107305677567, -0.004245387322252832, -0.00527669624670493, -0.006365250140793627, -0.007495563863613571, -0.008648843495784616, -0.009803374023827674, -0.010935105537303865, -0.012018423211070372, -0.01302707140404458, -0.013935188233421202, -0.014718395368408294, -0.015354879800335767, -0.015826400984703847, -0.01611915861024824, -0.016224463430565095, -0.01613916566411604, -0.015865811491772044, -0.015412516802343084, -0.014792566921686038, -0.014023769871586293, -0.013127607085927794, -0.012128238069943915, -0.011051423235100081, -0.00992343158789372, -0.008769997137818475, -0.007615380362032688, -0.006481579781991357, -0.005387724918514692, -0.004349666980908773, -0.003379768978786449, -0.0024868837307194048, -0.0016764974252954485, -0.0009510085794230893, -0.0003101076939226075, 0.0002487784484359292] + [0] * 2,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_24": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_24": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q2_z_baked_wf_24": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 62,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_25": {
            "type": "arbitrary",
            "samples": [0.0, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271] + [0] * 66 + [-0.00015778376362709108, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009116, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.00486381145425525, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709108] + [0] * 65 + [-0.000287055935168138, 0.00018678531325335443, 0.0007313638374660268, 0.0013491977358940609, 0.002040900484424626, 0.0028047877965340718, 0.0036365358884280644, 0.004528922552274611, 0.005471681673197407, 0.006451498305277343, 0.007452165040045105, 0.008454911336315011, 0.00943890622032931, 0.010381922093328638, 0.011261134326336946, 0.012054019059648716, 0.012739301373478904, 0.01329789887399926, 0.013713802630057087, 0.013974838835556974, 0.014073260665380765, 0.01400613017882009, 0.013775463999780111, 0.013388132694088483, 0.012855520849033922, 0.012192971320157502, 0.01141905149462005, 0.010554690502106466, 0.009622243207138078, 0.008644539099210865, 0.007643971882414219, 0.006641679117210862, 0.0056568515131467535, 0.004706199496728454, 0.003803591690700295, 0.0029598671339553712, 0.0021828115051823046, 0.0014772781184435274, 0.0008454275769439332, 0.000287055935168138] + [0] * 2,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_25": {
            "type": "arbitrary",
            "samples": [-0.0003798576395459785, -0.00043578666200400735, -0.0004935296633211693, -0.0005515554982505122, -0.0006080287141733543, -0.0006608525432248669, -0.0007077364436294015, -0.0007462873610355451, -0.0007741217179457732, -0.000788992915208048, -0.0007889270697455971, -0.0007723580575993246, -0.0007382519077163814, -0.0006862103827387051, -0.0006165442994707075, -0.0005303088013655113, -0.00042929531097465857, -0.00031597807114201563, -0.00019341675095889237, -6.512020720763538e-05, 6.512020720763538e-05, 0.00019341675095889237, 0.00031597807114201563, 0.00042929531097465857, 0.0005303088013655113, 0.0006165442994707075, 0.0006862103827387051, 0.0007382519077163814, 0.0007723580575993246, 0.0007889270697455971, 0.000788992915208048, 0.0007741217179457732, 0.0007462873610355451, 0.0007077364436294015, 0.0006608525432248669, 0.0006080287141733543, 0.0005515554982505122, 0.0004935296633211693, 0.00043578666200400735, 0.0003798576395459785] + [0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789557, 0.0016217826115637823, 0.002138921749805219, 0.002696774030395554, 0.003289415745753081, 0.003908942525632038, 0.0045455326130318325, 0.005187620832681909, 0.005822186296327273, 0.006435148841109959, 0.007011860634169723, 0.007537671049128937, 0.007998535633794195, 0.008381634516400982, 0.008675962590192949, 0.008872853716940654, 0.008966404172880879, 0.008953766494256927, 0.008835293328522903, 0.00861452115876475, 0.008297994944280967, 0.00789494581050467, 0.007416843935897083, 0.006876856847658555, 0.006289248786844126, 0.00566875924726123, 0.00502999814998553, 0.004386891608335704, 0.003752206352068045, 0.0031371732953768224, 0.0025512222418611033, 0.002001831129893862, 0.001494485274931458, 0.0010327353644391088, 0.0006183379243041826, 0.0002514588145349556, -6.908096354474351e-05, -0.00034553742236856605] + [0] * 65 + [0.0002487784484359292, 0.0008809232750019345, 0.0015974588866745011, 0.0023989529285996514, 0.0032833107305677563, 0.004245387322252832, 0.005276696246704929, 0.006365250140793626, 0.00749556386361357, 0.008648843495784615, 0.009803374023827673, 0.010935105537303863, 0.01201842321107037, 0.013027071404044578, 0.0139351882334212, 0.014718395368408292, 0.015354879800335765, 0.015826400984703844, 0.016119158610248235, 0.016224463430565092, 0.016139165664116037, 0.01586581149177204, 0.015412516802343082, 0.014792566921686037, 0.014023769871586291, 0.013127607085927792, 0.012128238069943913, 0.01105142323510008, 0.009923431587893718, 0.008769997137818474, 0.007615380362032686, 0.0064815797819913566, 0.005387724918514691, 0.004349666980908772, 0.0033797689787864486, 0.0024868837307194043, 0.001676497425295448, 0.000951008579423089, 0.0003101076939226073, -0.0002487784484359292] + [0] * 2,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_25": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_25": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q2_z_baked_wf_25": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 62,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_26": {
            "type": "arbitrary",
            "samples": [0.0, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271] + [0] * 66 + [-0.00015778376362709108, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009116, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.00486381145425525, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709108] + [0] * 107,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_26": {
            "type": "arbitrary",
            "samples": [-0.0003798576395459785, -0.00043578666200400735, -0.0004935296633211693, -0.0005515554982505122, -0.0006080287141733543, -0.0006608525432248669, -0.0007077364436294015, -0.0007462873610355451, -0.0007741217179457732, -0.000788992915208048, -0.0007889270697455971, -0.0007723580575993246, -0.0007382519077163814, -0.0006862103827387051, -0.0006165442994707075, -0.0005303088013655113, -0.00042929531097465857, -0.00031597807114201563, -0.00019341675095889237, -6.512020720763538e-05, 6.512020720763538e-05, 0.00019341675095889237, 0.00031597807114201563, 0.00042929531097465857, 0.0005303088013655113, 0.0006165442994707075, 0.0006862103827387051, 0.0007382519077163814, 0.0007723580575993246, 0.0007889270697455971, 0.000788992915208048, 0.0007741217179457732, 0.0007462873610355451, 0.0007077364436294015, 0.0006608525432248669, 0.0006080287141733543, 0.0005515554982505122, 0.0004935296633211693, 0.00043578666200400735, 0.0003798576395459785] + [0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789557, 0.0016217826115637823, 0.002138921749805219, 0.002696774030395554, 0.003289415745753081, 0.003908942525632038, 0.0045455326130318325, 0.005187620832681909, 0.005822186296327273, 0.006435148841109959, 0.007011860634169723, 0.007537671049128937, 0.007998535633794195, 0.008381634516400982, 0.008675962590192949, 0.008872853716940654, 0.008966404172880879, 0.008953766494256927, 0.008835293328522903, 0.00861452115876475, 0.008297994944280967, 0.00789494581050467, 0.007416843935897083, 0.006876856847658555, 0.006289248786844126, 0.00566875924726123, 0.00502999814998553, 0.004386891608335704, 0.003752206352068045, 0.0031371732953768224, 0.0025512222418611033, 0.002001831129893862, 0.001494485274931458, 0.0010327353644391088, 0.0006183379243041826, 0.0002514588145349556, -6.908096354474351e-05, -0.00034553742236856605] + [0] * 107,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_26": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_26": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q2_z_baked_wf_26": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 62,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_27": {
            "type": "arbitrary",
            "samples": [-0.000759715279091957, -0.0008715733240080146, -0.0009870593266423384, -0.0011031109965010239, -0.0012160574283467081, -0.001321705086449733, -0.001415472887258802, -0.0014925747220710893, -0.0015482434358915452, -0.0015779858304160947, -0.0015778541394911927, -0.0015447161151986475, -0.001476503815432761, -0.0013724207654774083, -0.0012330885989414128, -0.0010606176027310203, -0.0008585906219493146, -0.0006319561422840288, -0.00038683350191778213, -0.00013024041441526813, 0.0001302404144152734, 0.00038683350191778734, 0.0006319561422840338, 0.0008585906219493196, 0.001060617602731025, 0.001233088598941417, 0.0013724207654774122, 0.0014765038154327648, 0.001544716115198651, 0.0015778541394911958, 0.0015779858304160973, 0.0015482434358915474, 0.001492574722071091, 0.0014154728872588038, 0.0013217050864497344, 0.001216057428346709, 0.0011031109965010247, 0.0009870593266423388, 0.0008715733240080148, 0.000759715279091957] + [0] * 65 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0] * 65 + [-0.000287055935168138, 0.00018678531325335443, 0.0007313638374660268, 0.0013491977358940609, 0.002040900484424626, 0.0028047877965340718, 0.0036365358884280644, 0.004528922552274611, 0.005471681673197407, 0.006451498305277343, 0.007452165040045105, 0.008454911336315011, 0.00943890622032931, 0.010381922093328638, 0.011261134326336946, 0.012054019059648716, 0.012739301373478904, 0.01329789887399926, 0.013713802630057087, 0.013974838835556974, 0.014073260665380765, 0.01400613017882009, 0.013775463999780111, 0.013388132694088483, 0.012855520849033922, 0.012192971320157502, 0.01141905149462005, 0.010554690502106466, 0.009622243207138078, 0.008644539099210865, 0.007643971882414219, 0.006641679117210862, 0.0056568515131467535, 0.004706199496728454, 0.003803591690700295, 0.0029598671339553712, 0.0021828115051823046, 0.0014772781184435274, 0.0008454275769439332, 0.000287055935168138] + [0] * 2,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_27": {
            "type": "arbitrary",
            "samples": [4.651914424016516e-20, 0.0015760768444548542, 0.00337235610740649, 0.005392994053965991, 0.0076356283889478915, 0.010090276907130893, 0.012738449776040096, 0.015552569435837084, 0.018495784766494085, 0.0215222502891611, 0.024577916926684592, 0.027601849347301578, 0.030528048168025384, 0.033287716114425325, 0.03581186901257599, 0.03803415887258986, 0.03989375082406045, 0.04133808125447058, 0.04232532323982649] + [0.04282639809501372] * 2 + [0.04232532323982649, 0.04133808125447058, 0.03989375082406045, 0.03803415887258986, 0.03581186901257599, 0.033287716114425325, 0.030528048168025384, 0.027601849347301578, 0.024577916926684592, 0.0215222502891611, 0.018495784766494085, 0.015552569435837084, 0.012738449776040096, 0.010090276907130893, 0.0076356283889478915, 0.005392994053965991, 0.00337235610740649, 0.0015760768444548542, -4.651914424016516e-20] + [0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0] * 65 + [0.0002487784484359292, 0.0008809232750019345, 0.0015974588866745011, 0.0023989529285996514, 0.0032833107305677563, 0.004245387322252832, 0.005276696246704929, 0.006365250140793626, 0.00749556386361357, 0.008648843495784615, 0.009803374023827673, 0.010935105537303863, 0.01201842321107037, 0.013027071404044578, 0.0139351882334212, 0.014718395368408292, 0.015354879800335765, 0.015826400984703844, 0.016119158610248235, 0.016224463430565092, 0.016139165664116037, 0.01586581149177204, 0.015412516802343082, 0.014792566921686037, 0.014023769871586291, 0.013127607085927792, 0.012128238069943913, 0.01105142323510008, 0.009923431587893718, 0.008769997137818474, 0.007615380362032686, 0.0064815797819913566, 0.005387724918514691, 0.004349666980908772, 0.0033797689787864486, 0.0024868837307194043, 0.001676497425295448, 0.000951008579423089, 0.0003101076939226073, -0.0002487784484359292] + [0] * 2,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_27": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_27": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q2_z_baked_wf_27": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 62,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_28": {
            "type": "arbitrary",
            "samples": [-0.000759715279091957, -0.0008715733240080146, -0.0009870593266423384, -0.0011031109965010239, -0.0012160574283467081, -0.001321705086449733, -0.001415472887258802, -0.0014925747220710893, -0.0015482434358915452, -0.0015779858304160947, -0.0015778541394911927, -0.0015447161151986475, -0.001476503815432761, -0.0013724207654774083, -0.0012330885989414128, -0.0010606176027310203, -0.0008585906219493146, -0.0006319561422840288, -0.00038683350191778213, -0.00013024041441526813, 0.0001302404144152734, 0.00038683350191778734, 0.0006319561422840338, 0.0008585906219493196, 0.001060617602731025, 0.001233088598941417, 0.0013724207654774122, 0.0014765038154327648, 0.001544716115198651, 0.0015778541394911958, 0.0015779858304160973, 0.0015482434358915474, 0.001492574722071091, 0.0014154728872588038, 0.0013217050864497344, 0.001216057428346709, 0.0011031109965010247, 0.0009870593266423388, 0.0008715733240080148, 0.000759715279091957] + [0] * 65 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0] * 65 + [0.000287055935168138, -0.00018678531325335454, -0.000731363837466027, -0.0013491977358940613, -0.0020409004844246263, -0.002804787796534072, -0.0036365358884280653, -0.004528922552274612, -0.005471681673197408, -0.006451498305277344, -0.007452165040045105, -0.008454911336315013, -0.009438906220329312, -0.01038192209332864, -0.011261134326336948, -0.012054019059648717, -0.012739301373478906, -0.013297898873999263, -0.01371380263005709, -0.013974838835556978, -0.014073260665380768, -0.014006130178820093, -0.013775463999780113, -0.013388132694088485, -0.012855520849033924, -0.012192971320157503, -0.011419051494620051, -0.010554690502106468, -0.00962224320713808, -0.008644539099210865, -0.00764397188241422, -0.006641679117210864, -0.005656851513146754, -0.004706199496728455, -0.0038035916907002954, -0.0029598671339553717, -0.002182811505182305, -0.0014772781184435274, -0.0008454275769439333, -0.000287055935168138] + [0] * 2,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_28": {
            "type": "arbitrary",
            "samples": [4.651914424016516e-20, 0.0015760768444548542, 0.00337235610740649, 0.005392994053965991, 0.0076356283889478915, 0.010090276907130893, 0.012738449776040096, 0.015552569435837084, 0.018495784766494085, 0.0215222502891611, 0.024577916926684592, 0.027601849347301578, 0.030528048168025384, 0.033287716114425325, 0.03581186901257599, 0.03803415887258986, 0.03989375082406045, 0.04133808125447058, 0.04232532323982649] + [0.04282639809501372] * 2 + [0.04232532323982649, 0.04133808125447058, 0.03989375082406045, 0.03803415887258986, 0.03581186901257599, 0.033287716114425325, 0.030528048168025384, 0.027601849347301578, 0.024577916926684592, 0.0215222502891611, 0.018495784766494085, 0.015552569435837084, 0.012738449776040096, 0.010090276907130893, 0.0076356283889478915, 0.005392994053965991, 0.00337235610740649, 0.0015760768444548542, -4.651914424016516e-20] + [0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0] * 65 + [-0.00024877844843592924, -0.0008809232750019345, -0.0015974588866745014, -0.0023989529285996514, -0.0032833107305677563, -0.004245387322252832, -0.005276696246704929, -0.006365250140793626, -0.00749556386361357, -0.008648843495784615, -0.009803374023827673, -0.010935105537303863, -0.01201842321107037, -0.013027071404044578, -0.0139351882334212, -0.014718395368408294, -0.015354879800335765, -0.015826400984703844, -0.016119158610248235, -0.016224463430565092, -0.016139165664116037, -0.01586581149177204, -0.015412516802343082, -0.014792566921686037, -0.01402376987158629, -0.013127607085927792, -0.012128238069943913, -0.01105142323510008, -0.009923431587893718, -0.008769997137818474, -0.007615380362032686, -0.0064815797819913566, -0.005387724918514691, -0.004349666980908772, -0.0033797689787864486, -0.0024868837307194043, -0.001676497425295448, -0.0009510085794230889, -0.00031010769392260726, 0.00024877844843592924] + [0] * 2,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_28": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_28": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q2_z_baked_wf_28": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 62,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_29": {
            "type": "arbitrary",
            "samples": [-0.000759715279091957, -0.0008715733240080146, -0.0009870593266423384, -0.0011031109965010239, -0.0012160574283467081, -0.001321705086449733, -0.001415472887258802, -0.0014925747220710893, -0.0015482434358915452, -0.0015779858304160947, -0.0015778541394911927, -0.0015447161151986475, -0.001476503815432761, -0.0013724207654774083, -0.0012330885989414128, -0.0010606176027310203, -0.0008585906219493146, -0.0006319561422840288, -0.00038683350191778213, -0.00013024041441526813, 0.0001302404144152734, 0.00038683350191778734, 0.0006319561422840338, 0.0008585906219493196, 0.001060617602731025, 0.001233088598941417, 0.0013724207654774122, 0.0014765038154327648, 0.001544716115198651, 0.0015778541394911958, 0.0015779858304160973, 0.0015482434358915474, 0.001492574722071091, 0.0014154728872588038, 0.0013217050864497344, 0.001216057428346709, 0.0011031109965010247, 0.0009870593266423388, 0.0008715733240080148, 0.000759715279091957] + [0] * 65 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0] * 107,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_29": {
            "type": "arbitrary",
            "samples": [4.651914424016516e-20, 0.0015760768444548542, 0.00337235610740649, 0.005392994053965991, 0.0076356283889478915, 0.010090276907130893, 0.012738449776040096, 0.015552569435837084, 0.018495784766494085, 0.0215222502891611, 0.024577916926684592, 0.027601849347301578, 0.030528048168025384, 0.033287716114425325, 0.03581186901257599, 0.03803415887258986, 0.03989375082406045, 0.04133808125447058, 0.04232532323982649] + [0.04282639809501372] * 2 + [0.04232532323982649, 0.04133808125447058, 0.03989375082406045, 0.03803415887258986, 0.03581186901257599, 0.033287716114425325, 0.030528048168025384, 0.027601849347301578, 0.024577916926684592, 0.0215222502891611, 0.018495784766494085, 0.015552569435837084, 0.012738449776040096, 0.010090276907130893, 0.0076356283889478915, 0.005392994053965991, 0.00337235610740649, 0.0015760768444548542, -4.651914424016516e-20] + [0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0] * 107,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_29": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_29": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q2_z_baked_wf_29": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 62,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_30": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271] + [0] * 66 + [0.00015778376362709118, -0.000535823646241926, -0.001328831114714337, -0.0022237650156902507, -0.003220313321556805, -0.004314806824009116, -0.005499787323106856, -0.00676370587553009, -0.008090791755457433, -0.009461126481233454, -0.01085094709073768, -0.012233189208447764, -0.013578264158704062, -0.01485504664661625, -0.016032031846637824, -0.017078604759892795, -0.01796635205879739, -0.018670338762580556, -0.01917027003166739, -0.019451462661092028, -0.019505561409210812, -0.01933095140141051, -0.018932838204992752, -0.018322990034824432, -0.017519159903993792, -0.01654422731086274, -0.015425117354989585, -0.014191568472623336, -0.012874827277601197, -0.011506349901330282, -0.010116583993081482, -0.00873389498912647, -0.007383685659073527, -0.006087740851514874, -0.00486381145425525, -0.0037254344455140884, -0.002681970897594845, -0.0017388319130844836, -0.0008978543256915443, -0.00015778376362709118] + [0] * 65 + [-0.00028705593516813844, 0.0001867853132533528, 0.0007313638374660241, 0.0013491977358940567, 0.00204090048442462, 0.002804787796534064, 0.003636535888428055, 0.0045289225522746, 0.005471681673197394, 0.006451498305277328, 0.007452165040045087, 0.008454911336314992, 0.009438906220329288, 0.010381922093328614, 0.011261134326336922, 0.012054019059648691, 0.012739301373478876, 0.013297898873999233, 0.01371380263005706, 0.013974838835556946, 0.014073260665380737, 0.014006130178820062, 0.013775463999780083, 0.013388132694088456, 0.012855520849033897, 0.01219297132015748, 0.011419051494620028, 0.010554690502106447, 0.009622243207138063, 0.00864453909921085, 0.007643971882414205, 0.0066416791172108506, 0.005656851513146744, 0.004706199496728446, 0.003803591690700289, 0.0029598671339553665, 0.0021828115051823016, 0.0014772781184435257, 0.0008454275769439327, 0.00028705593516813844] + [0] * 2,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_30": {
            "type": "arbitrary",
            "samples": [0.0003798576395459785, 0.00043578666200400735, 0.0004935296633211693, 0.0005515554982505122, 0.0006080287141733543, 0.0006608525432248669, 0.0007077364436294015, 0.0007462873610355451, 0.0007741217179457732, 0.000788992915208048, 0.0007889270697455971, 0.0007723580575993246, 0.0007382519077163814, 0.0006862103827387051, 0.0006165442994707075, 0.0005303088013655113, 0.00042929531097465857, 0.00031597807114201563, 0.00019341675095889237, 6.512020720763538e-05, -6.512020720763538e-05, -0.00019341675095889237, -0.00031597807114201563, -0.00042929531097465857, -0.0005303088013655113, -0.0006165442994707075, -0.0006862103827387051, -0.0007382519077163814, -0.0007723580575993246, -0.0007889270697455971, -0.000788992915208048, -0.0007741217179457732, -0.0007462873610355451, -0.0007077364436294015, -0.0006608525432248669, -0.0006080287141733543, -0.0005515554982505122, -0.0004935296633211693, -0.00043578666200400735, -0.0003798576395459785] + [0] * 65 + [-0.000345537422368566, -0.0007237455283559927, -0.001149337124578956, -0.0016217826115637831, -0.0021389217498052203, -0.0026967740303955553, -0.003289415745753083, -0.00390894252563204, -0.004545532613031835, -0.005187620832681912, -0.005822186296327276, -0.006435148841109963, -0.007011860634169727, -0.0075376710491289415, -0.0079985356337942, -0.008381634516400987, -0.008675962590192954, -0.008872853716940661, -0.008966404172880884, -0.008953766494256932, -0.008835293328522908, -0.008614521158764755, -0.008297994944280974, -0.007894945810504676, -0.007416843935897088, -0.00687685684765856, -0.0062892487868441305, -0.005668759247261235, -0.0050299981499855335, -0.004386891608335708, -0.003752206352068048, -0.0031371732953768255, -0.0025512222418611055, -0.002001831129893864, -0.0014944852749314594, -0.0010327353644391099, -0.0006183379243041833, -0.00025145881453495606, 6.908096354474324e-05, 0.000345537422368566] + [0] * 65 + [0.0002487784484359287, 0.0008809232750019349, 0.0015974588866745024, 0.002398952928599654, 0.00328331073056776, 0.004245387322252837, 0.005276696246704936, 0.006365250140793635, 0.00749556386361358, 0.008648843495784627, 0.009803374023827685, 0.01093510553730388, 0.012018423211070387, 0.013027071404044598, 0.013935188233421223, 0.014718395368408315, 0.015354879800335789, 0.01582640098470387, 0.01611915861024826, 0.01622446343056512, 0.016139165664116065, 0.015865811491772065, 0.015412516802343108, 0.01479256692168606, 0.014023769871586314, 0.013127607085927815, 0.012128238069943936, 0.0110514232351001, 0.009923431587893735, 0.008769997137818489, 0.0076153803620326995, 0.006481579781991369, 0.005387724918514702, 0.004349666980908781, 0.0033797689787864555, 0.00248688373071941, 0.0016764974252954522, 0.0009510085794230916, 0.0003101076939226089, -0.0002487784484359287] + [0] * 2,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_30": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_30": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q2_z_baked_wf_30": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 62,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_31": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271] + [0] * 66 + [0.00015778376362709118, -0.000535823646241926, -0.001328831114714337, -0.0022237650156902507, -0.003220313321556805, -0.004314806824009116, -0.005499787323106856, -0.00676370587553009, -0.008090791755457433, -0.009461126481233454, -0.01085094709073768, -0.012233189208447764, -0.013578264158704062, -0.01485504664661625, -0.016032031846637824, -0.017078604759892795, -0.01796635205879739, -0.018670338762580556, -0.01917027003166739, -0.019451462661092028, -0.019505561409210812, -0.01933095140141051, -0.018932838204992752, -0.018322990034824432, -0.017519159903993792, -0.01654422731086274, -0.015425117354989585, -0.014191568472623336, -0.012874827277601197, -0.011506349901330282, -0.010116583993081482, -0.00873389498912647, -0.007383685659073527, -0.006087740851514874, -0.00486381145425525, -0.0037254344455140884, -0.002681970897594845, -0.0017388319130844836, -0.0008978543256915443, -0.00015778376362709118] + [0] * 65 + [0.0002870559351681382, -0.00018678531325335378, -0.0007313638374660256, -0.0013491977358940591, -0.0020409004844246233, -0.0028047877965340683, -0.0036365358884280605, -0.004528922552274606, -0.005471681673197401, -0.006451498305277336, -0.0074521650400450985, -0.008454911336315004, -0.0094389062203293, -0.010381922093328628, -0.011261134326336937, -0.012054019059648705, -0.012739301373478892, -0.013297898873999249, -0.013713802630057077, -0.013974838835556962, -0.014073260665380753, -0.014006130178820079, -0.013775463999780099, -0.013388132694088471, -0.012855520849033911, -0.012192971320157493, -0.011419051494620042, -0.010554690502106459, -0.009622243207138071, -0.00864453909921086, -0.007643971882414214, -0.006641679117210857, -0.00565685151314675, -0.00470619949672845, -0.0038035916907002924, -0.0029598671339553695, -0.0021828115051823033, -0.0014772781184435267, -0.000845427576943933, -0.0002870559351681382] + [0] * 2,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_31": {
            "type": "arbitrary",
            "samples": [0.0003798576395459785, 0.00043578666200400735, 0.0004935296633211693, 0.0005515554982505122, 0.0006080287141733543, 0.0006608525432248669, 0.0007077364436294015, 0.0007462873610355451, 0.0007741217179457732, 0.000788992915208048, 0.0007889270697455971, 0.0007723580575993246, 0.0007382519077163814, 0.0006862103827387051, 0.0006165442994707075, 0.0005303088013655113, 0.00042929531097465857, 0.00031597807114201563, 0.00019341675095889237, 6.512020720763538e-05, -6.512020720763538e-05, -0.00019341675095889237, -0.00031597807114201563, -0.00042929531097465857, -0.0005303088013655113, -0.0006165442994707075, -0.0006862103827387051, -0.0007382519077163814, -0.0007723580575993246, -0.0007889270697455971, -0.000788992915208048, -0.0007741217179457732, -0.0007462873610355451, -0.0007077364436294015, -0.0006608525432248669, -0.0006080287141733543, -0.0005515554982505122, -0.0004935296633211693, -0.00043578666200400735, -0.0003798576395459785] + [0] * 65 + [-0.000345537422368566, -0.0007237455283559927, -0.001149337124578956, -0.0016217826115637831, -0.0021389217498052203, -0.0026967740303955553, -0.003289415745753083, -0.00390894252563204, -0.004545532613031835, -0.005187620832681912, -0.005822186296327276, -0.006435148841109963, -0.007011860634169727, -0.0075376710491289415, -0.0079985356337942, -0.008381634516400987, -0.008675962590192954, -0.008872853716940661, -0.008966404172880884, -0.008953766494256932, -0.008835293328522908, -0.008614521158764755, -0.008297994944280974, -0.007894945810504676, -0.007416843935897088, -0.00687685684765856, -0.0062892487868441305, -0.005668759247261235, -0.0050299981499855335, -0.004386891608335708, -0.003752206352068048, -0.0031371732953768255, -0.0025512222418611055, -0.002001831129893864, -0.0014944852749314594, -0.0010327353644391099, -0.0006183379243041833, -0.00025145881453495606, 6.908096354474324e-05, 0.000345537422368566] + [0] * 65 + [-0.00024877844843592897, -0.0008809232750019347, -0.0015974588866745018, -0.0023989529285996527, -0.003283310730567758, -0.004245387322252834, -0.0052766962467049325, -0.00636525014079363, -0.007495563863613575, -0.00864884349578462, -0.009803374023827678, -0.01093510553730387, -0.012018423211070378, -0.013027071404044587, -0.01393518823342121, -0.014718395368408303, -0.015354879800335775, -0.015826400984703858, -0.016119158610248246, -0.016224463430565102, -0.016139165664116047, -0.01586581149177205, -0.015412516802343094, -0.014792566921686047, -0.014023769871586302, -0.013127607085927803, -0.012128238069943922, -0.011051423235100088, -0.009923431587893725, -0.008769997137818482, -0.007615380362032692, -0.006481579781991362, -0.005387724918514697, -0.0043496669809087755, -0.0033797689787864516, -0.002486883730719407, -0.00167649742529545, -0.0009510085794230902, -0.000310107693922608, 0.00024877844843592897] + [0] * 2,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_31": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_31": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q2_z_baked_wf_31": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 62,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_32": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271] + [0] * 66 + [0.00015778376362709118, -0.000535823646241926, -0.001328831114714337, -0.0022237650156902507, -0.003220313321556805, -0.004314806824009116, -0.005499787323106856, -0.00676370587553009, -0.008090791755457433, -0.009461126481233454, -0.01085094709073768, -0.012233189208447764, -0.013578264158704062, -0.01485504664661625, -0.016032031846637824, -0.017078604759892795, -0.01796635205879739, -0.018670338762580556, -0.01917027003166739, -0.019451462661092028, -0.019505561409210812, -0.01933095140141051, -0.018932838204992752, -0.018322990034824432, -0.017519159903993792, -0.01654422731086274, -0.015425117354989585, -0.014191568472623336, -0.012874827277601197, -0.011506349901330282, -0.010116583993081482, -0.00873389498912647, -0.007383685659073527, -0.006087740851514874, -0.00486381145425525, -0.0037254344455140884, -0.002681970897594845, -0.0017388319130844836, -0.0008978543256915443, -0.00015778376362709118] + [0] * 107,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_32": {
            "type": "arbitrary",
            "samples": [0.0003798576395459785, 0.00043578666200400735, 0.0004935296633211693, 0.0005515554982505122, 0.0006080287141733543, 0.0006608525432248669, 0.0007077364436294015, 0.0007462873610355451, 0.0007741217179457732, 0.000788992915208048, 0.0007889270697455971, 0.0007723580575993246, 0.0007382519077163814, 0.0006862103827387051, 0.0006165442994707075, 0.0005303088013655113, 0.00042929531097465857, 0.00031597807114201563, 0.00019341675095889237, 6.512020720763538e-05, -6.512020720763538e-05, -0.00019341675095889237, -0.00031597807114201563, -0.00042929531097465857, -0.0005303088013655113, -0.0006165442994707075, -0.0006862103827387051, -0.0007382519077163814, -0.0007723580575993246, -0.0007889270697455971, -0.000788992915208048, -0.0007741217179457732, -0.0007462873610355451, -0.0007077364436294015, -0.0006608525432248669, -0.0006080287141733543, -0.0005515554982505122, -0.0004935296633211693, -0.00043578666200400735, -0.0003798576395459785] + [0] * 65 + [-0.000345537422368566, -0.0007237455283559927, -0.001149337124578956, -0.0016217826115637831, -0.0021389217498052203, -0.0026967740303955553, -0.003289415745753083, -0.00390894252563204, -0.004545532613031835, -0.005187620832681912, -0.005822186296327276, -0.006435148841109963, -0.007011860634169727, -0.0075376710491289415, -0.0079985356337942, -0.008381634516400987, -0.008675962590192954, -0.008872853716940661, -0.008966404172880884, -0.008953766494256932, -0.008835293328522908, -0.008614521158764755, -0.008297994944280974, -0.007894945810504676, -0.007416843935897088, -0.00687685684765856, -0.0062892487868441305, -0.005668759247261235, -0.0050299981499855335, -0.004386891608335708, -0.003752206352068048, -0.0031371732953768255, -0.0025512222418611055, -0.002001831129893864, -0.0014944852749314594, -0.0010327353644391099, -0.0006183379243041833, -0.00025145881453495606, 6.908096354474324e-05, 0.000345537422368566] + [0] * 107,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_32": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_32": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q2_z_baked_wf_32": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 62,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_33": {
            "type": "arbitrary",
            "samples": [0.0, 0.0015760768444548542, 0.00337235610740649, 0.005392994053965991, 0.0076356283889478915, 0.010090276907130893, 0.012738449776040096, 0.015552569435837084, 0.018495784766494085, 0.0215222502891611, 0.024577916926684592, 0.027601849347301578, 0.030528048168025384, 0.033287716114425325, 0.03581186901257599, 0.03803415887258986, 0.03989375082406045, 0.04133808125447058, 0.04232532323982649] + [0.04282639809501372] * 2 + [0.04232532323982649, 0.04133808125447058, 0.03989375082406045, 0.03803415887258986, 0.03581186901257599, 0.033287716114425325, 0.030528048168025384, 0.027601849347301578, 0.024577916926684592, 0.0215222502891611, 0.018495784766494085, 0.015552569435837084, 0.012738449776040096, 0.010090276907130893, 0.0076356283889478915, 0.005392994053965991, 0.00337235610740649, 0.0015760768444548542] + [0] * 66 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0] * 65 + [-0.000287055935168138, 0.00018678531325335443, 0.0007313638374660268, 0.0013491977358940609, 0.002040900484424626, 0.0028047877965340718, 0.0036365358884280644, 0.004528922552274611, 0.005471681673197407, 0.006451498305277343, 0.007452165040045105, 0.008454911336315011, 0.00943890622032931, 0.010381922093328638, 0.011261134326336946, 0.012054019059648716, 0.012739301373478904, 0.01329789887399926, 0.013713802630057087, 0.013974838835556974, 0.014073260665380765, 0.01400613017882009, 0.013775463999780111, 0.013388132694088483, 0.012855520849033922, 0.012192971320157502, 0.01141905149462005, 0.010554690502106466, 0.009622243207138078, 0.008644539099210865, 0.007643971882414219, 0.006641679117210862, 0.0056568515131467535, 0.004706199496728454, 0.003803591690700295, 0.0029598671339553712, 0.0021828115051823046, 0.0014772781184435274, 0.0008454275769439332, 0.000287055935168138] + [0] * 2,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_33": {
            "type": "arbitrary",
            "samples": [0.000759715279091957, 0.0008715733240080147, 0.0009870593266423386, 0.0011031109965010243, 0.0012160574283467086, 0.0013217050864497337, 0.001415472887258803, 0.0014925747220710902, 0.0015482434358915463, 0.001577985830416096, 0.0015778541394911943, 0.0015447161151986492, 0.0014765038154327629, 0.0013724207654774103, 0.001233088598941415, 0.0010606176027310227, 0.0008585906219493171, 0.0006319561422840313, 0.00038683350191778473, 0.00013024041441527076, -0.00013024041441527076, -0.00038683350191778473, -0.0006319561422840313, -0.0008585906219493171, -0.0010606176027310227, -0.001233088598941415, -0.0013724207654774103, -0.0014765038154327629, -0.0015447161151986492, -0.0015778541394911943, -0.001577985830416096, -0.0015482434358915463, -0.0014925747220710902, -0.001415472887258803, -0.0013217050864497337, -0.0012160574283467086, -0.0011031109965010243, -0.0009870593266423386, -0.0008715733240080147, -0.000759715279091957] + [0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0] * 65 + [0.0002487784484359292, 0.0008809232750019345, 0.0015974588866745011, 0.0023989529285996514, 0.0032833107305677563, 0.004245387322252832, 0.005276696246704929, 0.006365250140793626, 0.00749556386361357, 0.008648843495784615, 0.009803374023827673, 0.010935105537303863, 0.01201842321107037, 0.013027071404044578, 0.0139351882334212, 0.014718395368408292, 0.015354879800335765, 0.015826400984703844, 0.016119158610248235, 0.016224463430565092, 0.016139165664116037, 0.01586581149177204, 0.015412516802343082, 0.014792566921686037, 0.014023769871586291, 0.013127607085927792, 0.012128238069943913, 0.01105142323510008, 0.009923431587893718, 0.008769997137818474, 0.007615380362032686, 0.0064815797819913566, 0.005387724918514691, 0.004349666980908772, 0.0033797689787864486, 0.0024868837307194043, 0.001676497425295448, 0.000951008579423089, 0.0003101076939226073, -0.0002487784484359292] + [0] * 2,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_33": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_33": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q2_z_baked_wf_33": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 62,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_34": {
            "type": "arbitrary",
            "samples": [0.0, 0.0015760768444548542, 0.00337235610740649, 0.005392994053965991, 0.0076356283889478915, 0.010090276907130893, 0.012738449776040096, 0.015552569435837084, 0.018495784766494085, 0.0215222502891611, 0.024577916926684592, 0.027601849347301578, 0.030528048168025384, 0.033287716114425325, 0.03581186901257599, 0.03803415887258986, 0.03989375082406045, 0.04133808125447058, 0.04232532323982649] + [0.04282639809501372] * 2 + [0.04232532323982649, 0.04133808125447058, 0.03989375082406045, 0.03803415887258986, 0.03581186901257599, 0.033287716114425325, 0.030528048168025384, 0.027601849347301578, 0.024577916926684592, 0.0215222502891611, 0.018495784766494085, 0.015552569435837084, 0.012738449776040096, 0.010090276907130893, 0.0076356283889478915, 0.005392994053965991, 0.00337235610740649, 0.0015760768444548542] + [0] * 66 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0] * 65 + [0.000287055935168138, -0.00018678531325335454, -0.000731363837466027, -0.0013491977358940613, -0.0020409004844246263, -0.002804787796534072, -0.0036365358884280653, -0.004528922552274612, -0.005471681673197408, -0.006451498305277344, -0.007452165040045105, -0.008454911336315013, -0.009438906220329312, -0.01038192209332864, -0.011261134326336948, -0.012054019059648717, -0.012739301373478906, -0.013297898873999263, -0.01371380263005709, -0.013974838835556978, -0.014073260665380768, -0.014006130178820093, -0.013775463999780113, -0.013388132694088485, -0.012855520849033924, -0.012192971320157503, -0.011419051494620051, -0.010554690502106468, -0.00962224320713808, -0.008644539099210865, -0.00764397188241422, -0.006641679117210864, -0.005656851513146754, -0.004706199496728455, -0.0038035916907002954, -0.0029598671339553717, -0.002182811505182305, -0.0014772781184435274, -0.0008454275769439333, -0.000287055935168138] + [0] * 2,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_34": {
            "type": "arbitrary",
            "samples": [0.000759715279091957, 0.0008715733240080147, 0.0009870593266423386, 0.0011031109965010243, 0.0012160574283467086, 0.0013217050864497337, 0.001415472887258803, 0.0014925747220710902, 0.0015482434358915463, 0.001577985830416096, 0.0015778541394911943, 0.0015447161151986492, 0.0014765038154327629, 0.0013724207654774103, 0.001233088598941415, 0.0010606176027310227, 0.0008585906219493171, 0.0006319561422840313, 0.00038683350191778473, 0.00013024041441527076, -0.00013024041441527076, -0.00038683350191778473, -0.0006319561422840313, -0.0008585906219493171, -0.0010606176027310227, -0.001233088598941415, -0.0013724207654774103, -0.0014765038154327629, -0.0015447161151986492, -0.0015778541394911943, -0.001577985830416096, -0.0015482434358915463, -0.0014925747220710902, -0.001415472887258803, -0.0013217050864497337, -0.0012160574283467086, -0.0011031109965010243, -0.0009870593266423386, -0.0008715733240080147, -0.000759715279091957] + [0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0] * 65 + [-0.00024877844843592924, -0.0008809232750019345, -0.0015974588866745014, -0.0023989529285996514, -0.0032833107305677563, -0.004245387322252832, -0.005276696246704929, -0.006365250140793626, -0.00749556386361357, -0.008648843495784615, -0.009803374023827673, -0.010935105537303863, -0.01201842321107037, -0.013027071404044578, -0.0139351882334212, -0.014718395368408294, -0.015354879800335765, -0.015826400984703844, -0.016119158610248235, -0.016224463430565092, -0.016139165664116037, -0.01586581149177204, -0.015412516802343082, -0.014792566921686037, -0.01402376987158629, -0.013127607085927792, -0.012128238069943913, -0.01105142323510008, -0.009923431587893718, -0.008769997137818474, -0.007615380362032686, -0.0064815797819913566, -0.005387724918514691, -0.004349666980908772, -0.0033797689787864486, -0.0024868837307194043, -0.001676497425295448, -0.0009510085794230889, -0.00031010769392260726, 0.00024877844843592924] + [0] * 2,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_34": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_34": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q2_z_baked_wf_34": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 62,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_35": {
            "type": "arbitrary",
            "samples": [0.0, 0.0015760768444548542, 0.00337235610740649, 0.005392994053965991, 0.0076356283889478915, 0.010090276907130893, 0.012738449776040096, 0.015552569435837084, 0.018495784766494085, 0.0215222502891611, 0.024577916926684592, 0.027601849347301578, 0.030528048168025384, 0.033287716114425325, 0.03581186901257599, 0.03803415887258986, 0.03989375082406045, 0.04133808125447058, 0.04232532323982649] + [0.04282639809501372] * 2 + [0.04232532323982649, 0.04133808125447058, 0.03989375082406045, 0.03803415887258986, 0.03581186901257599, 0.033287716114425325, 0.030528048168025384, 0.027601849347301578, 0.024577916926684592, 0.0215222502891611, 0.018495784766494085, 0.015552569435837084, 0.012738449776040096, 0.010090276907130893, 0.0076356283889478915, 0.005392994053965991, 0.00337235610740649, 0.0015760768444548542] + [0] * 66 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0] * 107,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_35": {
            "type": "arbitrary",
            "samples": [0.000759715279091957, 0.0008715733240080147, 0.0009870593266423386, 0.0011031109965010243, 0.0012160574283467086, 0.0013217050864497337, 0.001415472887258803, 0.0014925747220710902, 0.0015482434358915463, 0.001577985830416096, 0.0015778541394911943, 0.0015447161151986492, 0.0014765038154327629, 0.0013724207654774103, 0.001233088598941415, 0.0010606176027310227, 0.0008585906219493171, 0.0006319561422840313, 0.00038683350191778473, 0.00013024041441527076, -0.00013024041441527076, -0.00038683350191778473, -0.0006319561422840313, -0.0008585906219493171, -0.0010606176027310227, -0.001233088598941415, -0.0013724207654774103, -0.0014765038154327629, -0.0015447161151986492, -0.0015778541394911943, -0.001577985830416096, -0.0015482434358915463, -0.0014925747220710902, -0.001415472887258803, -0.0013217050864497337, -0.0012160574283467086, -0.0011031109965010243, -0.0009870593266423386, -0.0008715733240080147, -0.000759715279091957] + [0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0] * 107,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_35": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_35": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q2_z_baked_wf_35": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 62,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_36": {
            "type": "arbitrary",
            "samples": [4.651914424016516e-20, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271, -4.651914424016516e-20] + [0] * 65 + [-0.00015778376362709108, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009116, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.00486381145425525, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709108] + [0] * 65 + [0.00028705593516813806, -0.00018678531325335427, -0.0007313638374660265, -0.0013491977358940606, -0.0020409004844246254, -0.002804787796534071, -0.0036365358884280635, -0.00452892255227461, -0.005471681673197406, -0.0064514983052773416, -0.007452165040045104, -0.00845491133631501, -0.009438906220329309, -0.010381922093328637, -0.011261134326336944, -0.012054019059648714, -0.0127393013734789, -0.013297898873999259, -0.013713802630057085, -0.013974838835556972, -0.014073260665380763, -0.014006130178820088, -0.01377546399978011, -0.01338813269408848, -0.01285552084903392, -0.0121929713201575, -0.011419051494620048, -0.010554690502106464, -0.009622243207138077, -0.008644539099210863, -0.0076439718824142175, -0.006641679117210861, -0.005656851513146753, -0.004706199496728453, -0.003803591690700294, -0.002959867133955371, -0.0021828115051823046, -0.0014772781184435272, -0.0008454275769439331, -0.00028705593516813806] + [0] * 2,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_36": {
            "type": "arbitrary",
            "samples": [-0.0003798576395459785, -0.00043578666200400746, -0.0004935296633211695, -0.0005515554982505125, -0.0006080287141733547, -0.0006608525432248675, -0.0007077364436294022, -0.0007462873610355461, -0.0007741217179457742, -0.0007889929152080493, -0.0007889270697455987, -0.0007723580575993264, -0.0007382519077163833, -0.0006862103827387072, -0.0006165442994707096, -0.0005303088013655136, -0.000429295310974661, -0.0003159780711420182, -0.00019341675095889497, -6.5120207207638e-05, 6.512020720763277e-05, 0.00019341675095888976, 0.0003159780711420131, 0.00042929531097465613, 0.0005303088013655091, 0.0006165442994707053, 0.0006862103827387031, 0.0007382519077163796, 0.0007723580575993229, 0.0007889270697455956, 0.0007889929152080467, 0.0007741217179457721, 0.0007462873610355441, 0.0007077364436294007, 0.0006608525432248662, 0.0006080287141733539, 0.0005515554982505118, 0.0004935296633211691, 0.00043578666200400724, 0.0003798576395459785] + [0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789557, 0.0016217826115637823, 0.002138921749805219, 0.002696774030395554, 0.003289415745753081, 0.003908942525632038, 0.0045455326130318325, 0.005187620832681909, 0.005822186296327273, 0.006435148841109959, 0.007011860634169723, 0.007537671049128937, 0.007998535633794195, 0.008381634516400982, 0.008675962590192949, 0.008872853716940654, 0.008966404172880879, 0.008953766494256927, 0.008835293328522903, 0.00861452115876475, 0.008297994944280967, 0.00789494581050467, 0.007416843935897083, 0.006876856847658555, 0.006289248786844126, 0.00566875924726123, 0.00502999814998553, 0.004386891608335704, 0.003752206352068045, 0.0031371732953768224, 0.0025512222418611033, 0.002001831129893862, 0.001494485274931458, 0.0010327353644391088, 0.0006183379243041826, 0.0002514588145349556, -6.908096354474351e-05, -0.00034553742236856605] + [0] * 65 + [-0.0002487784484359292, -0.0008809232750019345, -0.0015974588866745014, -0.002398952928599652, -0.0032833107305677567, -0.004245387322252832, -0.00527669624670493, -0.006365250140793627, -0.007495563863613571, -0.008648843495784616, -0.009803374023827674, -0.010935105537303865, -0.012018423211070372, -0.01302707140404458, -0.013935188233421202, -0.014718395368408294, -0.015354879800335767, -0.015826400984703847, -0.01611915861024824, -0.016224463430565095, -0.01613916566411604, -0.015865811491772044, -0.015412516802343084, -0.014792566921686038, -0.014023769871586293, -0.013127607085927794, -0.012128238069943915, -0.011051423235100081, -0.00992343158789372, -0.008769997137818475, -0.007615380362032688, -0.006481579781991357, -0.005387724918514692, -0.004349666980908773, -0.003379768978786449, -0.0024868837307194048, -0.0016764974252954485, -0.0009510085794230893, -0.0003101076939226075, 0.0002487784484359292] + [0] * 2,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_36": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_36": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q2_z_baked_wf_36": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 62,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_37": {
            "type": "arbitrary",
            "samples": [4.651914424016516e-20, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271, -4.651914424016516e-20] + [0] * 65 + [-0.00015778376362709108, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009116, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.00486381145425525, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709108] + [0] * 65 + [-0.000287055935168138, 0.00018678531325335443, 0.0007313638374660268, 0.0013491977358940609, 0.002040900484424626, 0.0028047877965340718, 0.0036365358884280644, 0.004528922552274611, 0.005471681673197407, 0.006451498305277343, 0.007452165040045105, 0.008454911336315011, 0.00943890622032931, 0.010381922093328638, 0.011261134326336946, 0.012054019059648716, 0.012739301373478904, 0.01329789887399926, 0.013713802630057087, 0.013974838835556974, 0.014073260665380765, 0.01400613017882009, 0.013775463999780111, 0.013388132694088483, 0.012855520849033922, 0.012192971320157502, 0.01141905149462005, 0.010554690502106466, 0.009622243207138078, 0.008644539099210865, 0.007643971882414219, 0.006641679117210862, 0.0056568515131467535, 0.004706199496728454, 0.003803591690700295, 0.0029598671339553712, 0.0021828115051823046, 0.0014772781184435274, 0.0008454275769439332, 0.000287055935168138] + [0] * 2,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_37": {
            "type": "arbitrary",
            "samples": [-0.0003798576395459785, -0.00043578666200400746, -0.0004935296633211695, -0.0005515554982505125, -0.0006080287141733547, -0.0006608525432248675, -0.0007077364436294022, -0.0007462873610355461, -0.0007741217179457742, -0.0007889929152080493, -0.0007889270697455987, -0.0007723580575993264, -0.0007382519077163833, -0.0006862103827387072, -0.0006165442994707096, -0.0005303088013655136, -0.000429295310974661, -0.0003159780711420182, -0.00019341675095889497, -6.5120207207638e-05, 6.512020720763277e-05, 0.00019341675095888976, 0.0003159780711420131, 0.00042929531097465613, 0.0005303088013655091, 0.0006165442994707053, 0.0006862103827387031, 0.0007382519077163796, 0.0007723580575993229, 0.0007889270697455956, 0.0007889929152080467, 0.0007741217179457721, 0.0007462873610355441, 0.0007077364436294007, 0.0006608525432248662, 0.0006080287141733539, 0.0005515554982505118, 0.0004935296633211691, 0.00043578666200400724, 0.0003798576395459785] + [0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789557, 0.0016217826115637823, 0.002138921749805219, 0.002696774030395554, 0.003289415745753081, 0.003908942525632038, 0.0045455326130318325, 0.005187620832681909, 0.005822186296327273, 0.006435148841109959, 0.007011860634169723, 0.007537671049128937, 0.007998535633794195, 0.008381634516400982, 0.008675962590192949, 0.008872853716940654, 0.008966404172880879, 0.008953766494256927, 0.008835293328522903, 0.00861452115876475, 0.008297994944280967, 0.00789494581050467, 0.007416843935897083, 0.006876856847658555, 0.006289248786844126, 0.00566875924726123, 0.00502999814998553, 0.004386891608335704, 0.003752206352068045, 0.0031371732953768224, 0.0025512222418611033, 0.002001831129893862, 0.001494485274931458, 0.0010327353644391088, 0.0006183379243041826, 0.0002514588145349556, -6.908096354474351e-05, -0.00034553742236856605] + [0] * 65 + [0.0002487784484359292, 0.0008809232750019345, 0.0015974588866745011, 0.0023989529285996514, 0.0032833107305677563, 0.004245387322252832, 0.005276696246704929, 0.006365250140793626, 0.00749556386361357, 0.008648843495784615, 0.009803374023827673, 0.010935105537303863, 0.01201842321107037, 0.013027071404044578, 0.0139351882334212, 0.014718395368408292, 0.015354879800335765, 0.015826400984703844, 0.016119158610248235, 0.016224463430565092, 0.016139165664116037, 0.01586581149177204, 0.015412516802343082, 0.014792566921686037, 0.014023769871586291, 0.013127607085927792, 0.012128238069943913, 0.01105142323510008, 0.009923431587893718, 0.008769997137818474, 0.007615380362032686, 0.0064815797819913566, 0.005387724918514691, 0.004349666980908772, 0.0033797689787864486, 0.0024868837307194043, 0.001676497425295448, 0.000951008579423089, 0.0003101076939226073, -0.0002487784484359292] + [0] * 2,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_37": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_37": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q2_z_baked_wf_37": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 62,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_38": {
            "type": "arbitrary",
            "samples": [4.651914424016516e-20, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271, -4.651914424016516e-20] + [0] * 65 + [-0.00015778376362709108, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009116, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.00486381145425525, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709108] + [0] * 107,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_38": {
            "type": "arbitrary",
            "samples": [-0.0003798576395459785, -0.00043578666200400746, -0.0004935296633211695, -0.0005515554982505125, -0.0006080287141733547, -0.0006608525432248675, -0.0007077364436294022, -0.0007462873610355461, -0.0007741217179457742, -0.0007889929152080493, -0.0007889270697455987, -0.0007723580575993264, -0.0007382519077163833, -0.0006862103827387072, -0.0006165442994707096, -0.0005303088013655136, -0.000429295310974661, -0.0003159780711420182, -0.00019341675095889497, -6.5120207207638e-05, 6.512020720763277e-05, 0.00019341675095888976, 0.0003159780711420131, 0.00042929531097465613, 0.0005303088013655091, 0.0006165442994707053, 0.0006862103827387031, 0.0007382519077163796, 0.0007723580575993229, 0.0007889270697455956, 0.0007889929152080467, 0.0007741217179457721, 0.0007462873610355441, 0.0007077364436294007, 0.0006608525432248662, 0.0006080287141733539, 0.0005515554982505118, 0.0004935296633211691, 0.00043578666200400724, 0.0003798576395459785] + [0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789557, 0.0016217826115637823, 0.002138921749805219, 0.002696774030395554, 0.003289415745753081, 0.003908942525632038, 0.0045455326130318325, 0.005187620832681909, 0.005822186296327273, 0.006435148841109959, 0.007011860634169723, 0.007537671049128937, 0.007998535633794195, 0.008381634516400982, 0.008675962590192949, 0.008872853716940654, 0.008966404172880879, 0.008953766494256927, 0.008835293328522903, 0.00861452115876475, 0.008297994944280967, 0.00789494581050467, 0.007416843935897083, 0.006876856847658555, 0.006289248786844126, 0.00566875924726123, 0.00502999814998553, 0.004386891608335704, 0.003752206352068045, 0.0031371732953768224, 0.0025512222418611033, 0.002001831129893862, 0.001494485274931458, 0.0010327353644391088, 0.0006183379243041826, 0.0002514588145349556, -6.908096354474351e-05, -0.00034553742236856605] + [0] * 107,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_38": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_38": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q2_z_baked_wf_38": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 62,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_39": {
            "type": "arbitrary",
            "samples": [4.651914424016516e-20, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271, -4.651914424016516e-20] + [0] * 65 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0] * 65 + [-0.000287055935168138, 0.00018678531325335443, 0.0007313638374660268, 0.0013491977358940609, 0.002040900484424626, 0.0028047877965340718, 0.0036365358884280644, 0.004528922552274611, 0.005471681673197407, 0.006451498305277343, 0.007452165040045105, 0.008454911336315011, 0.00943890622032931, 0.010381922093328638, 0.011261134326336946, 0.012054019059648716, 0.012739301373478904, 0.01329789887399926, 0.013713802630057087, 0.013974838835556974, 0.014073260665380765, 0.01400613017882009, 0.013775463999780111, 0.013388132694088483, 0.012855520849033922, 0.012192971320157502, 0.01141905149462005, 0.010554690502106466, 0.009622243207138078, 0.008644539099210865, 0.007643971882414219, 0.006641679117210862, 0.0056568515131467535, 0.004706199496728454, 0.003803591690700295, 0.0029598671339553712, 0.0021828115051823046, 0.0014772781184435274, 0.0008454275769439332, 0.000287055935168138] + [0] * 2,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_39": {
            "type": "arbitrary",
            "samples": [-0.0003798576395459785, -0.00043578666200400746, -0.0004935296633211695, -0.0005515554982505125, -0.0006080287141733547, -0.0006608525432248675, -0.0007077364436294022, -0.0007462873610355461, -0.0007741217179457742, -0.0007889929152080493, -0.0007889270697455987, -0.0007723580575993264, -0.0007382519077163833, -0.0006862103827387072, -0.0006165442994707096, -0.0005303088013655136, -0.000429295310974661, -0.0003159780711420182, -0.00019341675095889497, -6.5120207207638e-05, 6.512020720763277e-05, 0.00019341675095888976, 0.0003159780711420131, 0.00042929531097465613, 0.0005303088013655091, 0.0006165442994707053, 0.0006862103827387031, 0.0007382519077163796, 0.0007723580575993229, 0.0007889270697455956, 0.0007889929152080467, 0.0007741217179457721, 0.0007462873610355441, 0.0007077364436294007, 0.0006608525432248662, 0.0006080287141733539, 0.0005515554982505118, 0.0004935296633211691, 0.00043578666200400724, 0.0003798576395459785] + [0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0] * 65 + [0.0002487784484359292, 0.0008809232750019345, 0.0015974588866745011, 0.0023989529285996514, 0.0032833107305677563, 0.004245387322252832, 0.005276696246704929, 0.006365250140793626, 0.00749556386361357, 0.008648843495784615, 0.009803374023827673, 0.010935105537303863, 0.01201842321107037, 0.013027071404044578, 0.0139351882334212, 0.014718395368408292, 0.015354879800335765, 0.015826400984703844, 0.016119158610248235, 0.016224463430565092, 0.016139165664116037, 0.01586581149177204, 0.015412516802343082, 0.014792566921686037, 0.014023769871586291, 0.013127607085927792, 0.012128238069943913, 0.01105142323510008, 0.009923431587893718, 0.008769997137818474, 0.007615380362032686, 0.0064815797819913566, 0.005387724918514691, 0.004349666980908772, 0.0033797689787864486, 0.0024868837307194043, 0.001676497425295448, 0.000951008579423089, 0.0003101076939226073, -0.0002487784484359292] + [0] * 2,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_39": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_39": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q2_z_baked_wf_39": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 62,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_40": {
            "type": "arbitrary",
            "samples": [4.651914424016516e-20, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271, -4.651914424016516e-20] + [0] * 65 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0] * 65 + [0.000287055935168138, -0.00018678531325335454, -0.000731363837466027, -0.0013491977358940613, -0.0020409004844246263, -0.002804787796534072, -0.0036365358884280653, -0.004528922552274612, -0.005471681673197408, -0.006451498305277344, -0.007452165040045105, -0.008454911336315013, -0.009438906220329312, -0.01038192209332864, -0.011261134326336948, -0.012054019059648717, -0.012739301373478906, -0.013297898873999263, -0.01371380263005709, -0.013974838835556978, -0.014073260665380768, -0.014006130178820093, -0.013775463999780113, -0.013388132694088485, -0.012855520849033924, -0.012192971320157503, -0.011419051494620051, -0.010554690502106468, -0.00962224320713808, -0.008644539099210865, -0.00764397188241422, -0.006641679117210864, -0.005656851513146754, -0.004706199496728455, -0.0038035916907002954, -0.0029598671339553717, -0.002182811505182305, -0.0014772781184435274, -0.0008454275769439333, -0.000287055935168138] + [0] * 2,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_40": {
            "type": "arbitrary",
            "samples": [-0.0003798576395459785, -0.00043578666200400746, -0.0004935296633211695, -0.0005515554982505125, -0.0006080287141733547, -0.0006608525432248675, -0.0007077364436294022, -0.0007462873610355461, -0.0007741217179457742, -0.0007889929152080493, -0.0007889270697455987, -0.0007723580575993264, -0.0007382519077163833, -0.0006862103827387072, -0.0006165442994707096, -0.0005303088013655136, -0.000429295310974661, -0.0003159780711420182, -0.00019341675095889497, -6.5120207207638e-05, 6.512020720763277e-05, 0.00019341675095888976, 0.0003159780711420131, 0.00042929531097465613, 0.0005303088013655091, 0.0006165442994707053, 0.0006862103827387031, 0.0007382519077163796, 0.0007723580575993229, 0.0007889270697455956, 0.0007889929152080467, 0.0007741217179457721, 0.0007462873610355441, 0.0007077364436294007, 0.0006608525432248662, 0.0006080287141733539, 0.0005515554982505118, 0.0004935296633211691, 0.00043578666200400724, 0.0003798576395459785] + [0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0] * 65 + [-0.00024877844843592924, -0.0008809232750019345, -0.0015974588866745014, -0.0023989529285996514, -0.0032833107305677563, -0.004245387322252832, -0.005276696246704929, -0.006365250140793626, -0.00749556386361357, -0.008648843495784615, -0.009803374023827673, -0.010935105537303863, -0.01201842321107037, -0.013027071404044578, -0.0139351882334212, -0.014718395368408294, -0.015354879800335765, -0.015826400984703844, -0.016119158610248235, -0.016224463430565092, -0.016139165664116037, -0.01586581149177204, -0.015412516802343082, -0.014792566921686037, -0.01402376987158629, -0.013127607085927792, -0.012128238069943913, -0.01105142323510008, -0.009923431587893718, -0.008769997137818474, -0.007615380362032686, -0.0064815797819913566, -0.005387724918514691, -0.004349666980908772, -0.0033797689787864486, -0.0024868837307194043, -0.001676497425295448, -0.0009510085794230889, -0.00031010769392260726, 0.00024877844843592924] + [0] * 2,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_40": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_40": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q2_z_baked_wf_40": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 62,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_41": {
            "type": "arbitrary",
            "samples": [4.651914424016516e-20, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271, -4.651914424016516e-20] + [0] * 65 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0] * 107,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_41": {
            "type": "arbitrary",
            "samples": [-0.0003798576395459785, -0.00043578666200400746, -0.0004935296633211695, -0.0005515554982505125, -0.0006080287141733547, -0.0006608525432248675, -0.0007077364436294022, -0.0007462873610355461, -0.0007741217179457742, -0.0007889929152080493, -0.0007889270697455987, -0.0007723580575993264, -0.0007382519077163833, -0.0006862103827387072, -0.0006165442994707096, -0.0005303088013655136, -0.000429295310974661, -0.0003159780711420182, -0.00019341675095889497, -6.5120207207638e-05, 6.512020720763277e-05, 0.00019341675095888976, 0.0003159780711420131, 0.00042929531097465613, 0.0005303088013655091, 0.0006165442994707053, 0.0006862103827387031, 0.0007382519077163796, 0.0007723580575993229, 0.0007889270697455956, 0.0007889929152080467, 0.0007741217179457721, 0.0007462873610355441, 0.0007077364436294007, 0.0006608525432248662, 0.0006080287141733539, 0.0005515554982505118, 0.0004935296633211691, 0.00043578666200400724, 0.0003798576395459785] + [0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0] * 107,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_41": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_41": {
            "type": "arbitrary",
            "samples": [0] * 252,
            "is_overridable": False,
        },
        "q2_z_baked_wf_41": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 62,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_42": {
            "type": "arbitrary",
            "samples": [0] * 105 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0] * 65 + [0.00028705593516813795, -0.0001867853132533546, -0.0007313638374660274, -0.0013491977358940617, -0.0020409004844246267, -0.0028047877965340726, -0.003636535888428066, -0.004528922552274613, -0.00547168167319741, -0.006451498305277346, -0.007452165040045108, -0.008454911336315015, -0.009438906220329314, -0.010381922093328642, -0.011261134326336951, -0.012054019059648721, -0.012739301373478907, -0.013297898873999268, -0.013713802630057092, -0.01397483883555698, -0.01407326066538077, -0.014006130178820094, -0.013775463999780115, -0.013388132694088487, -0.012855520849033927, -0.012192971320157507, -0.011419051494620053, -0.01055469050210647, -0.009622243207138082, -0.008644539099210867, -0.007643971882414222, -0.006641679117210864, -0.005656851513146755, -0.0047061994967284556, -0.003803591690700296, -0.002959867133955372, -0.002182811505182305, -0.0014772781184435276, -0.0008454275769439333, -0.00028705593516813795] + [0] * 106,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_42": {
            "type": "arbitrary",
            "samples": [0] * 105 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0] * 65 + [-0.0002487784484359293, -0.0008809232750019345, -0.0015974588866745011, -0.0023989529285996514, -0.003283310730567756, -0.004245387322252831, -0.005276696246704929, -0.006365250140793625, -0.00749556386361357, -0.008648843495784613, -0.00980337402382767, -0.010935105537303862, -0.012018423211070368, -0.013027071404044577, -0.013935188233421198, -0.014718395368408292, -0.015354879800335761, -0.015826400984703844, -0.016119158610248232, -0.01622446343056509, -0.016139165664116033, -0.015865811491772037, -0.01541251680234308, -0.014792566921686033, -0.014023769871586288, -0.01312760708592779, -0.012128238069943911, -0.011051423235100078, -0.009923431587893716, -0.008769997137818472, -0.007615380362032684, -0.006481579781991355, -0.0053877249185146905, -0.00434966698090877, -0.0033797689787864477, -0.002486883730719404, -0.001676497425295448, -0.0009510085794230887, -0.00031010769392260715, 0.0002487784484359293] + [0] * 106,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_42": {
            "type": "arbitrary",
            "samples": [0] * 356,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_42": {
            "type": "arbitrary",
            "samples": [0] * 356,
            "is_overridable": False,
        },
        "q2_z_baked_wf_42": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 61,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_43": {
            "type": "arbitrary",
            "samples": [0.0, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271] + [0] * 66 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0] * 65 + [0.00028705593516813795, -0.0001867853132533546, -0.0007313638374660274, -0.0013491977358940617, -0.0020409004844246267, -0.0028047877965340726, -0.003636535888428066, -0.004528922552274613, -0.00547168167319741, -0.006451498305277346, -0.007452165040045108, -0.008454911336315015, -0.009438906220329314, -0.010381922093328642, -0.011261134326336951, -0.012054019059648721, -0.012739301373478907, -0.013297898873999268, -0.013713802630057092, -0.01397483883555698, -0.01407326066538077, -0.014006130178820094, -0.013775463999780115, -0.013388132694088487, -0.012855520849033927, -0.012192971320157507, -0.011419051494620053, -0.01055469050210647, -0.009622243207138082, -0.008644539099210867, -0.007643971882414222, -0.006641679117210864, -0.005656851513146755, -0.0047061994967284556, -0.003803591690700296, -0.002959867133955372, -0.002182811505182305, -0.0014772781184435276, -0.0008454275769439333, -0.00028705593516813795] + [0] * 106,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_43": {
            "type": "arbitrary",
            "samples": [-0.0003798576395459785, -0.00043578666200400735, -0.0004935296633211693, -0.0005515554982505122, -0.0006080287141733543, -0.0006608525432248669, -0.0007077364436294015, -0.0007462873610355451, -0.0007741217179457732, -0.000788992915208048, -0.0007889270697455971, -0.0007723580575993246, -0.0007382519077163814, -0.0006862103827387051, -0.0006165442994707075, -0.0005303088013655113, -0.00042929531097465857, -0.00031597807114201563, -0.00019341675095889237, -6.512020720763538e-05, 6.512020720763538e-05, 0.00019341675095889237, 0.00031597807114201563, 0.00042929531097465857, 0.0005303088013655113, 0.0006165442994707075, 0.0006862103827387051, 0.0007382519077163814, 0.0007723580575993246, 0.0007889270697455971, 0.000788992915208048, 0.0007741217179457732, 0.0007462873610355451, 0.0007077364436294015, 0.0006608525432248669, 0.0006080287141733543, 0.0005515554982505122, 0.0004935296633211693, 0.00043578666200400735, 0.0003798576395459785] + [0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0] * 65 + [-0.0002487784484359293, -0.0008809232750019345, -0.0015974588866745011, -0.0023989529285996514, -0.003283310730567756, -0.004245387322252831, -0.005276696246704929, -0.006365250140793625, -0.00749556386361357, -0.008648843495784613, -0.00980337402382767, -0.010935105537303862, -0.012018423211070368, -0.013027071404044577, -0.013935188233421198, -0.014718395368408292, -0.015354879800335761, -0.015826400984703844, -0.016119158610248232, -0.01622446343056509, -0.016139165664116033, -0.015865811491772037, -0.01541251680234308, -0.014792566921686033, -0.014023769871586288, -0.01312760708592779, -0.012128238069943911, -0.011051423235100078, -0.009923431587893716, -0.008769997137818472, -0.007615380362032684, -0.006481579781991355, -0.0053877249185146905, -0.00434966698090877, -0.0033797689787864477, -0.002486883730719404, -0.001676497425295448, -0.0009510085794230887, -0.00031010769392260715, 0.0002487784484359293] + [0] * 106,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_43": {
            "type": "arbitrary",
            "samples": [0] * 356,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_43": {
            "type": "arbitrary",
            "samples": [0] * 356,
            "is_overridable": False,
        },
        "q2_z_baked_wf_43": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 61,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_44": {
            "type": "arbitrary",
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20] + [0] * 65 + [0.00015778376362709124, -0.0005358236462419259, -0.0013288311147143367, -0.0022237650156902507, -0.0032203133215568044, -0.004314806824009115, -0.0054997873231068545, -0.0067637058755300895, -0.008090791755457431, -0.009461126481233453, -0.010850947090737677, -0.012233189208447763, -0.01357826415870406, -0.014855046646616249, -0.01603203184663782, -0.017078604759892792, -0.01796635205879739, -0.018670338762580552, -0.019170270031667387, -0.019451462661092028, -0.019505561409210812, -0.019330951401410508, -0.01893283820499275, -0.018322990034824432, -0.01751915990399379, -0.016544227310862736, -0.015425117354989583, -0.014191568472623334, -0.012874827277601196, -0.01150634990133028, -0.01011658399308148, -0.008733894989126472, -0.007383685659073526, -0.006087740851514874, -0.004863811454255249, -0.003725434445514088, -0.002681970897594845, -0.0017388319130844834, -0.0008978543256915442, -0.00015778376362709124] + [0] * 65 + [0.00028705593516813806, -0.000186785313253354, -0.0007313638374660263, -0.00134919773589406, -0.0020409004844246246, -0.0028047877965340696, -0.0036365358884280627, -0.004528922552274608, -0.005471681673197404, -0.00645149830527734, -0.0074521650400451, -0.008454911336315008, -0.009438906220329306, -0.010381922093328633, -0.011261134326336941, -0.012054019059648709, -0.012739301373478897, -0.013297898873999254, -0.01371380263005708, -0.013974838835556967, -0.014073260665380758, -0.014006130178820082, -0.013775463999780104, -0.013388132694088476, -0.012855520849033915, -0.012192971320157496, -0.011419051494620044, -0.01055469050210646, -0.009622243207138075, -0.00864453909921086, -0.007643971882414216, -0.006641679117210859, -0.005656851513146751, -0.004706199496728452, -0.0038035916907002937, -0.00295986713395537, -0.0021828115051823038, -0.001477278118443527, -0.000845427576943933, -0.00028705593516813806] + [0] * 106,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_44": {
            "type": "arbitrary",
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785] + [0] * 65 + [-0.00034553742236856594, -0.0007237455283559927, -0.0011493371245789564, -0.0016217826115637833, -0.0021389217498052207, -0.002696774030395556, -0.0032894157457530842, -0.003908942525632041, -0.004545532613031837, -0.005187620832681913, -0.005822186296327278, -0.0064351488411099654, -0.00701186063416973, -0.007537671049128944, -0.007998535633794204, -0.00838163451640099, -0.008675962590192958, -0.008872853716940665, -0.008966404172880887, -0.008953766494256936, -0.008835293328522911, -0.008614521158764758, -0.008297994944280978, -0.00789494581050468, -0.007416843935897092, -0.006876856847658563, -0.006289248786844133, -0.005668759247261237, -0.005029998149985536, -0.0043868916083357095, -0.0037522063520680497, -0.003137173295376827, -0.002551222241861107, -0.002001831129893865, -0.0014944852749314602, -0.0010327353644391107, -0.0006183379243041838, -0.00025145881453495644, 6.908096354474308e-05, 0.00034553742236856594] + [0] * 65 + [-0.0002487784484359291, -0.0008809232750019345, -0.0015974588866745014, -0.0023989529285996522, -0.0032833107305677567, -0.004245387322252833, -0.005276696246704931, -0.006365250140793628, -0.007495563863613572, -0.008648843495784616, -0.009803374023827673, -0.010935105537303867, -0.012018423211070373, -0.013027071404044582, -0.013935188233421204, -0.014718395368408296, -0.015354879800335768, -0.01582640098470385, -0.01611915861024824, -0.016224463430565095, -0.01613916566411604, -0.015865811491772044, -0.015412516802343087, -0.01479256692168604, -0.014023769871586295, -0.013127607085927796, -0.012128238069943916, -0.011051423235100083, -0.009923431587893721, -0.008769997137818477, -0.007615380362032688, -0.006481579781991359, -0.005387724918514693, -0.004349666980908774, -0.0033797689787864495, -0.0024868837307194056, -0.0016764974252954491, -0.0009510085794230893, -0.0003101076939226077, 0.0002487784484359291] + [0] * 106,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_44": {
            "type": "arbitrary",
            "samples": [0] * 356,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_44": {
            "type": "arbitrary",
            "samples": [0] * 356,
            "is_overridable": False,
        },
        "q2_z_baked_wf_44": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 61,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_45": {
            "type": "arbitrary",
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20] + [0] * 65 + [-0.00015778376362709108, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009116, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.00486381145425525, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709108] + [0] * 65 + [-0.000287055935168138, 0.00018678531325335454, 0.000731363837466027, 0.0013491977358940613, 0.0020409004844246263, 0.002804787796534072, 0.0036365358884280653, 0.004528922552274612, 0.005471681673197408, 0.006451498305277344, 0.007452165040045105, 0.008454911336315013, 0.009438906220329312, 0.01038192209332864, 0.011261134326336948, 0.012054019059648717, 0.012739301373478906, 0.013297898873999263, 0.01371380263005709, 0.013974838835556978, 0.014073260665380768, 0.014006130178820093, 0.013775463999780113, 0.013388132694088485, 0.012855520849033924, 0.012192971320157503, 0.011419051494620051, 0.010554690502106468, 0.00962224320713808, 0.008644539099210865, 0.00764397188241422, 0.006641679117210864, 0.005656851513146754, 0.004706199496728455, 0.0038035916907002954, 0.0029598671339553717, 0.002182811505182305, 0.0014772781184435274, 0.0008454275769439333, 0.000287055935168138] + [0] * 106,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_45": {
            "type": "arbitrary",
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785] + [0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789557, 0.0016217826115637823, 0.002138921749805219, 0.002696774030395554, 0.003289415745753081, 0.003908942525632038, 0.0045455326130318325, 0.005187620832681909, 0.005822186296327273, 0.006435148841109959, 0.007011860634169723, 0.007537671049128937, 0.007998535633794195, 0.008381634516400982, 0.008675962590192949, 0.008872853716940654, 0.008966404172880879, 0.008953766494256927, 0.008835293328522903, 0.00861452115876475, 0.008297994944280967, 0.00789494581050467, 0.007416843935897083, 0.006876856847658555, 0.006289248786844126, 0.00566875924726123, 0.00502999814998553, 0.004386891608335704, 0.003752206352068045, 0.0031371732953768224, 0.0025512222418611033, 0.002001831129893862, 0.001494485274931458, 0.0010327353644391088, 0.0006183379243041826, 0.0002514588145349556, -6.908096354474351e-05, -0.00034553742236856605] + [0] * 65 + [0.00024877844843592924, 0.0008809232750019345, 0.0015974588866745014, 0.0023989529285996514, 0.0032833107305677563, 0.004245387322252832, 0.005276696246704929, 0.006365250140793626, 0.00749556386361357, 0.008648843495784615, 0.009803374023827673, 0.010935105537303863, 0.01201842321107037, 0.013027071404044578, 0.0139351882334212, 0.014718395368408294, 0.015354879800335765, 0.015826400984703844, 0.016119158610248235, 0.016224463430565092, 0.016139165664116037, 0.01586581149177204, 0.015412516802343082, 0.014792566921686037, 0.01402376987158629, 0.013127607085927792, 0.012128238069943913, 0.01105142323510008, 0.009923431587893718, 0.008769997137818474, 0.007615380362032686, 0.0064815797819913566, 0.005387724918514691, 0.004349666980908772, 0.0033797689787864486, 0.0024868837307194043, 0.001676497425295448, 0.0009510085794230889, 0.00031010769392260726, -0.00024877844843592924] + [0] * 106,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_45": {
            "type": "arbitrary",
            "samples": [0] * 356,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_45": {
            "type": "arbitrary",
            "samples": [0] * 356,
            "is_overridable": False,
        },
        "q2_z_baked_wf_45": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 61,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_46": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271] + [0] * 66 + [-0.000157783763627091, 0.0005358236462419265, 0.0013288311147143378, 0.0022237650156902516, 0.0032203133215568057, 0.004314806824009118, 0.005499787323106857, 0.006763705875530093, 0.008090791755457434, 0.009461126481233456, 0.010850947090737683, 0.012233189208447768, 0.013578264158704065, 0.014855046646616254, 0.016032031846637828, 0.0170786047598928, 0.017966352058797392, 0.01867033876258056, 0.019170270031667394, 0.019451462661092035, 0.01950556140921082, 0.019330951401410515, 0.018932838204992756, 0.018322990034824436, 0.017519159903993796, 0.016544227310862743, 0.015425117354989588, 0.01419156847262334, 0.0128748272776012, 0.011506349901330285, 0.010116583993081484, 0.008733894989126472, 0.007383685659073528, 0.006087740851514875, 0.00486381145425525, 0.0037254344455140893, 0.0026819708975948458, 0.0017388319130844836, 0.0008978543256915441, 0.000157783763627091] + [0] * 65 + [-0.0002870559351681379, 0.00018678531325335476, 0.0007313638374660276, 0.001349197735894062, 0.002040900484424627, 0.002804787796534073, 0.003636535888428067, 0.0045289225522746135, 0.005471681673197411, 0.006451498305277347, 0.00745216504004511, 0.008454911336315016, 0.009438906220329316, 0.010381922093328643, 0.011261134326336953, 0.012054019059648723, 0.012739301373478909, 0.01329789887399927, 0.013713802630057096, 0.013974838835556981, 0.014073260665380772, 0.014006130178820098, 0.013775463999780116, 0.013388132694088489, 0.012855520849033929, 0.012192971320157509, 0.011419051494620054, 0.010554690502106471, 0.009622243207138084, 0.008644539099210868, 0.007643971882414223, 0.0066416791172108644, 0.005656851513146756, 0.004706199496728456, 0.0038035916907002963, 0.0029598671339553725, 0.0021828115051823055, 0.0014772781184435278, 0.0008454275769439333, 0.0002870559351681379] + [0] * 106,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_46": {
            "type": "arbitrary",
            "samples": [0.0003798576395459785, 0.00043578666200400735, 0.0004935296633211693, 0.0005515554982505122, 0.0006080287141733543, 0.0006608525432248669, 0.0007077364436294015, 0.0007462873610355451, 0.0007741217179457732, 0.000788992915208048, 0.0007889270697455971, 0.0007723580575993246, 0.0007382519077163814, 0.0006862103827387051, 0.0006165442994707075, 0.0005303088013655113, 0.00042929531097465857, 0.00031597807114201563, 0.00019341675095889237, 6.512020720763538e-05, -6.512020720763538e-05, -0.00019341675095889237, -0.00031597807114201563, -0.00042929531097465857, -0.0005303088013655113, -0.0006165442994707075, -0.0006862103827387051, -0.0007382519077163814, -0.0007723580575993246, -0.0007889270697455971, -0.000788992915208048, -0.0007741217179457732, -0.0007462873610355451, -0.0007077364436294015, -0.0006608525432248669, -0.0006080287141733543, -0.0005515554982505122, -0.0004935296633211693, -0.00043578666200400735, -0.0003798576395459785] + [0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789555, 0.0016217826115637818, 0.0021389217498052186, 0.002696774030395553, 0.0032894157457530803, 0.0039089425256320365, 0.004545532613031832, 0.0051876208326819065, 0.005822186296327269, 0.006435148841109956, 0.007011860634169719, 0.007537671049128934, 0.007998535633794192, 0.008381634516400978, 0.008675962590192945, 0.008872853716940651, 0.008966404172880874, 0.008953766494256922, 0.008835293328522897, 0.008614521158764744, 0.008297994944280964, 0.007894945810504667, 0.00741684393589708, 0.006876856847658552, 0.006289248786844123, 0.005668759247261227, 0.0050299981499855265, 0.004386891608335701, 0.0037522063520680424, 0.0031371732953768207, 0.002551222241861101, 0.0020018311298938603, 0.0014944852749314572, 0.0010327353644391077, 0.0006183379243041819, 0.0002514588145349552, -6.908096354474373e-05, -0.00034553742236856605] + [0] * 65 + [0.00024877844843592935, 0.0008809232750019343, 0.0015974588866745011, 0.0023989529285996514, 0.0032833107305677554, 0.004245387322252831, 0.005276696246704929, 0.006365250140793624, 0.007495563863613569, 0.008648843495784611, 0.009803374023827669, 0.010935105537303862, 0.012018423211070366, 0.013027071404044575, 0.013935188233421197, 0.01471839536840829, 0.015354879800335761, 0.01582640098470384, 0.016119158610248232, 0.01622446343056509, 0.016139165664116033, 0.015865811491772037, 0.015412516802343078, 0.01479256692168603, 0.014023769871586286, 0.013127607085927789, 0.01212823806994391, 0.011051423235100076, 0.009923431587893713, 0.00876999713781847, 0.007615380362032682, 0.006481579781991354, 0.00538772491851469, 0.00434966698090877, 0.003379768978786447, 0.0024868837307194035, 0.0016764974252954474, 0.0009510085794230883, 0.000310107693922607, -0.00024877844843592935] + [0] * 106,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_46": {
            "type": "arbitrary",
            "samples": [0] * 356,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_46": {
            "type": "arbitrary",
            "samples": [0] * 356,
            "is_overridable": False,
        },
        "q2_z_baked_wf_46": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 61,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_47": {
            "type": "arbitrary",
            "samples": [0] * 105 + [-0.000157783763627091, 0.0005358236462419265, 0.0013288311147143378, 0.0022237650156902516, 0.0032203133215568057, 0.004314806824009118, 0.005499787323106857, 0.006763705875530093, 0.008090791755457434, 0.009461126481233456, 0.010850947090737683, 0.012233189208447768, 0.013578264158704065, 0.014855046646616254, 0.016032031846637828, 0.0170786047598928, 0.017966352058797392, 0.01867033876258056, 0.019170270031667394, 0.019451462661092035, 0.01950556140921082, 0.019330951401410515, 0.018932838204992756, 0.018322990034824436, 0.017519159903993796, 0.016544227310862743, 0.015425117354989588, 0.01419156847262334, 0.0128748272776012, 0.011506349901330285, 0.010116583993081484, 0.008733894989126472, 0.007383685659073528, 0.006087740851514875, 0.00486381145425525, 0.0037254344455140893, 0.0026819708975948458, 0.0017388319130844836, 0.0008978543256915441, 0.000157783763627091] + [0] * 65 + [-0.0002870559351681379, 0.00018678531325335476, 0.0007313638374660276, 0.001349197735894062, 0.002040900484424627, 0.002804787796534073, 0.003636535888428067, 0.0045289225522746135, 0.005471681673197411, 0.006451498305277347, 0.00745216504004511, 0.008454911336315016, 0.009438906220329316, 0.010381922093328643, 0.011261134326336953, 0.012054019059648723, 0.012739301373478909, 0.01329789887399927, 0.013713802630057096, 0.013974838835556981, 0.014073260665380772, 0.014006130178820098, 0.013775463999780116, 0.013388132694088489, 0.012855520849033929, 0.012192971320157509, 0.011419051494620054, 0.010554690502106471, 0.009622243207138084, 0.008644539099210868, 0.007643971882414223, 0.0066416791172108644, 0.005656851513146756, 0.004706199496728456, 0.0038035916907002963, 0.0029598671339553725, 0.0021828115051823055, 0.0014772781184435278, 0.0008454275769439333, 0.0002870559351681379] + [0] * 106,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_47": {
            "type": "arbitrary",
            "samples": [0] * 105 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789555, 0.0016217826115637818, 0.0021389217498052186, 0.002696774030395553, 0.0032894157457530803, 0.0039089425256320365, 0.004545532613031832, 0.0051876208326819065, 0.005822186296327269, 0.006435148841109956, 0.007011860634169719, 0.007537671049128934, 0.007998535633794192, 0.008381634516400978, 0.008675962590192945, 0.008872853716940651, 0.008966404172880874, 0.008953766494256922, 0.008835293328522897, 0.008614521158764744, 0.008297994944280964, 0.007894945810504667, 0.00741684393589708, 0.006876856847658552, 0.006289248786844123, 0.005668759247261227, 0.0050299981499855265, 0.004386891608335701, 0.0037522063520680424, 0.0031371732953768207, 0.002551222241861101, 0.0020018311298938603, 0.0014944852749314572, 0.0010327353644391077, 0.0006183379243041819, 0.0002514588145349552, -6.908096354474373e-05, -0.00034553742236856605] + [0] * 65 + [0.00024877844843592935, 0.0008809232750019343, 0.0015974588866745011, 0.0023989529285996514, 0.0032833107305677554, 0.004245387322252831, 0.005276696246704929, 0.006365250140793624, 0.007495563863613569, 0.008648843495784611, 0.009803374023827669, 0.010935105537303862, 0.012018423211070366, 0.013027071404044575, 0.013935188233421197, 0.01471839536840829, 0.015354879800335761, 0.01582640098470384, 0.016119158610248232, 0.01622446343056509, 0.016139165664116033, 0.015865811491772037, 0.015412516802343078, 0.01479256692168603, 0.014023769871586286, 0.013127607085927789, 0.01212823806994391, 0.011051423235100076, 0.009923431587893713, 0.00876999713781847, 0.007615380362032682, 0.006481579781991354, 0.00538772491851469, 0.00434966698090877, 0.003379768978786447, 0.0024868837307194035, 0.0016764974252954474, 0.0009510085794230883, 0.000310107693922607, -0.00024877844843592935] + [0] * 106,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_47": {
            "type": "arbitrary",
            "samples": [0] * 356,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_47": {
            "type": "arbitrary",
            "samples": [0] * 356,
            "is_overridable": False,
        },
        "q2_z_baked_wf_47": {
            "type": "arbitrary",
            "samples": [0] * 60 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 80 + [0.1755] * 25 + [0] * 61,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_48": {
            "type": "arbitrary",
            "samples": [0.0, 0.0015760768444548542, 0.00337235610740649, 0.005392994053965991, 0.0076356283889478915, 0.010090276907130893, 0.012738449776040096, 0.015552569435837084, 0.018495784766494085, 0.0215222502891611, 0.024577916926684592, 0.027601849347301578, 0.030528048168025384, 0.033287716114425325, 0.03581186901257599, 0.03803415887258986, 0.03989375082406045, 0.04133808125447058, 0.04232532323982649] + [0.04282639809501372] * 2 + [0.04232532323982649, 0.04133808125447058, 0.03989375082406045, 0.03803415887258986, 0.03581186901257599, 0.033287716114425325, 0.030528048168025384, 0.027601849347301578, 0.024577916926684592, 0.0215222502891611, 0.018495784766494085, 0.015552569435837084, 0.012738449776040096, 0.010090276907130893, 0.0076356283889478915, 0.005392994053965991, 0.00337235610740649, 0.0015760768444548542, 0.0],
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_48": {
            "type": "arbitrary",
            "samples": [0.000759715279091957, 0.0008715733240080147, 0.0009870593266423386, 0.0011031109965010243, 0.0012160574283467086, 0.0013217050864497337, 0.001415472887258803, 0.0014925747220710902, 0.0015482434358915463, 0.001577985830416096, 0.0015778541394911943, 0.0015447161151986492, 0.0014765038154327629, 0.0013724207654774103, 0.001233088598941415, 0.0010606176027310227, 0.0008585906219493171, 0.0006319561422840313, 0.00038683350191778473, 0.00013024041441527076, -0.00013024041441527076, -0.00038683350191778473, -0.0006319561422840313, -0.0008585906219493171, -0.0010606176027310227, -0.001233088598941415, -0.0013724207654774103, -0.0014765038154327629, -0.0015447161151986492, -0.0015778541394911943, -0.001577985830416096, -0.0015482434358915463, -0.0014925747220710902, -0.001415472887258803, -0.0013217050864497337, -0.0012160574283467086, -0.0011031109965010243, -0.0009870593266423386, -0.0008715733240080147, -0.000759715279091957],
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_48": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_48": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q2_z_baked_wf_48": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_49": {
            "type": "arbitrary",
            "samples": [9.303828848033032e-20, -0.0015760768444548542, -0.00337235610740649, -0.005392994053965991, -0.0076356283889478915, -0.010090276907130893, -0.012738449776040096, -0.015552569435837084, -0.018495784766494085, -0.0215222502891611, -0.024577916926684592, -0.027601849347301578, -0.030528048168025384, -0.033287716114425325, -0.03581186901257599, -0.03803415887258986, -0.03989375082406045, -0.04133808125447058, -0.04232532323982649] + [-0.04282639809501372] * 2 + [-0.04232532323982649, -0.04133808125447058, -0.03989375082406045, -0.03803415887258986, -0.03581186901257599, -0.033287716114425325, -0.030528048168025384, -0.027601849347301578, -0.024577916926684592, -0.0215222502891611, -0.018495784766494085, -0.015552569435837084, -0.012738449776040096, -0.010090276907130893, -0.0076356283889478915, -0.005392994053965991, -0.00337235610740649, -0.0015760768444548542, -9.303828848033032e-20],
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_49": {
            "type": "arbitrary",
            "samples": [-0.000759715279091957, -0.0008715733240080149, -0.000987059326642339, -0.001103110996501025, -0.0012160574283467094, -0.001321705086449735, -0.0014154728872588045, -0.0014925747220710921, -0.0015482434358915485, -0.0015779858304160986, -0.0015778541394911973, -0.0015447161151986527, -0.0014765038154327666, -0.0013724207654774144, -0.0012330885989414193, -0.0010606176027310272, -0.000858590621949322, -0.0006319561422840364, -0.00038683350191778994, -0.000130240414415276, 0.00013024041441526553, 0.00038683350191777953, 0.0006319561422840262, 0.0008585906219493123, 0.0010606176027310181, 0.0012330885989414106, 0.0013724207654774061, 0.0014765038154327592, 0.0015447161151986458, 0.0015778541394911912, 0.0015779858304160934, 0.0015482434358915441, 0.0014925747220710882, 0.0014154728872588015, 0.0013217050864497324, 0.0012160574283467077, 0.0011031109965010237, 0.0009870593266423382, 0.0008715733240080145, 0.000759715279091957],
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_49": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_49": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q2_z_baked_wf_49": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_I_50": {
            "type": "arbitrary",
            "samples": [0.0] * 40,
            "is_overridable": False,
        },
        "q2_xy_baked_wf_Q_50": {
            "type": "arbitrary",
            "samples": [0.0] * 40,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_I_50": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q3_xy_baked_wf_Q_50": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
        "q2_z_baked_wf_50": {
            "type": "arbitrary",
            "samples": [0] * 40,
            "is_overridable": False,
        },
    },
    "digital_waveforms": {
        "ON": {
            "samples": [(1, 0)],
        },
    },
    "integration_weights": {
        "cosine_weights": {
            "cosine": [(0.0, 400), (1.0, 1700)],
            "sine": [(0.0, 400), (0.0, 1700)],
        },
        "sine_weights": {
            "cosine": [(0.0, 400), (0.0, 1700)],
            "sine": [(0.0, 400), (1.0, 1700)],
        },
        "minus_sine_weights": {
            "cosine": [(0.0, 400), (0.0, 1700)],
            "sine": [(0.0, 400), (-1.0, 1700)],
        },
        "rotated_cosine_weights_q1": {
            "cosine": [(0.0, 400), (-0.8535507972753273, 1700)],
            "sine": [(0.0, 400), (0.5210096318405766, 1700)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(0.0, 400), (-0.5210096318405766, 1700)],
            "sine": [(0.0, 400), (-0.8535507972753273, 1700)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(0.0, 400), (0.5210096318405766, 1700)],
            "sine": [(0.0, 400), (0.8535507972753273, 1700)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(0.0, 400), (0.8079898838980305, 1700)],
            "sine": [(0.0, 400), (0.5891963573533421, 1700)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(0.0, 400), (-0.5891963573533421, 1700)],
            "sine": [(0.0, 400), (0.8079898838980305, 1700)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(0.0, 400), (0.5891963573533421, 1700)],
            "sine": [(0.0, 400), (-0.8079898838980305, 1700)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(0.0, 400), (-0.18566661538557747, 1700)],
            "sine": [(0.0, 400), (0.9826127965436152, 1700)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(0.0, 400), (-0.9826127965436152, 1700)],
            "sine": [(0.0, 400), (-0.18566661538557747, 1700)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(0.0, 400), (0.9826127965436152, 1700)],
            "sine": [(0.0, 400), (0.18566661538557747, 1700)],
        },
        "rotated_cosine_weights_q4": {
            "cosine": [(0.0, 400), (1.0, 1700)],
            "sine": [(0.0, 400), (0.0, 1700)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(0.0, 400), (-0.0, 1700)],
            "sine": [(0.0, 400), (1.0, 1700)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(0.0, 400), (0.0, 1700)],
            "sine": [(0.0, 400), (-1.0, 1700)],
        },
        "rotated_cosine_weights_q5": {
            "cosine": [(0.0, 400), (1.0, 1700)],
            "sine": [(0.0, 400), (0.0, 1700)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(0.0, 400), (-0.0, 1700)],
            "sine": [(0.0, 400), (1.0, 1700)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(0.0, 400), (0.0, 1700)],
            "sine": [(0.0, 400), (-1.0, 1700)],
        },
        "opt_cosine_weights_q1": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_sine_weights_q1": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_minus_sine_weights_q1": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_cosine_weights_q2": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_sine_weights_q2": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_minus_sine_weights_q2": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_cosine_weights_q3": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_sine_weights_q3": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_minus_sine_weights_q3": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_cosine_weights_q4": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_sine_weights_q4": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_minus_sine_weights_q4": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_cosine_weights_q5": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_sine_weights_q5": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_minus_sine_weights_q5": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
    },
    "mixers": {
        "octave_octave1_2": [{'intermediate_frequency': -116555000.0, 'lo_frequency': 4055000000.0, 'correction': (1, 0, 0, 1)}],
        "octave_octave1_3": [{'intermediate_frequency': -317621000.0, 'lo_frequency': 3850000000.0, 'correction': (1, 0, 0, 1)}],
        "octave_octave1_4": [{'intermediate_frequency': -101584000.0, 'lo_frequency': 4300000000.0, 'correction': (1, 0, 0, 1)}],
        "octave_octave1_5": [{'intermediate_frequency': -89863100.0, 'lo_frequency': 3950000000.0, 'correction': (1, 0, 0, 1)}],
        "octave_octave2_1": [{'intermediate_frequency': -92000000.0, 'lo_frequency': 4750000000.0, 'correction': (1, 0, 0, 1)}],
        "octave_octave1_1": [
            {'intermediate_frequency': -214210000.0, 'lo_frequency': 5950000000, 'correction': (1, 0, 0, 1)},
            {'intermediate_frequency': 75079000.0, 'lo_frequency': 5950000000, 'correction': (1, 0, 0, 1)},
            {'intermediate_frequency': -103970000.0, 'lo_frequency': 5950000000, 'correction': (1, 0, 0, 1)},
            {'intermediate_frequency': 163060000.0, 'lo_frequency': 5950000000, 'correction': (1, 0, 0, 1)},
            {'intermediate_frequency': -25800000.0, 'lo_frequency': 5950000000, 'correction': (1, 0, 0, 1)},
        ],
    },
}

loaded_config = {
    "version": 1,
    "controllers": {
        "con1": {
            "type": "opx1",
            "analog_outputs": {
                "1": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                },
                "2": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                },
                "3": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                },
                "4": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                },
                "5": {
                    "offset": -0.34,
                    "delay": 0,
                    "shareable": False,
                },
                "6": {
                    "offset": -0.3529,
                    "delay": 0,
                    "shareable": False,
                },
                "7": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                },
                "8": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                },
                "9": {
                    "offset": -0.3421,
                    "delay": 0,
                    "shareable": False,
                },
                "10": {
                    "offset": -0.3433,
                    "delay": 0,
                    "shareable": False,
                },
            },
            "analog_inputs": {
                "1": {
                    "offset": 0.014816313000633604,
                    "gain_db": 0,
                    "shareable": False,
                },
                "2": {
                    "offset": 0.013283161315917969,
                    "gain_db": 0,
                    "shareable": False,
                },
            },
            "digital_outputs": {
                "1": {
                    "shareable": False,
                    "inverted": False,
                },
                "3": {
                    "shareable": False,
                    "inverted": False,
                },
                "5": {
                    "shareable": False,
                    "inverted": False,
                },
                "7": {
                    "shareable": False,
                    "inverted": False,
                },
                "10": {
                    "shareable": False,
                    "inverted": False,
                },
            },
        },
    },
    "oscillators": {},
    "elements": {
        "rr1": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 200,
            "smearing": 0,
            "intermediate_frequency": 214210000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q1",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "octave_octave1_1",
                "lo_frequency": 5950000000.0,
            },
        },
        "rr2": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 200,
            "smearing": 0,
            "intermediate_frequency": 75079000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q2",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "octave_octave1_1",
                "lo_frequency": 5950000000.0,
            },
        },
        "rr3": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 200,
            "smearing": 0,
            "intermediate_frequency": 103970000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q3",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "octave_octave1_1",
                "lo_frequency": 5950000000.0,
            },
        },
        "rr4": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 200,
            "smearing": 0,
            "intermediate_frequency": 163060000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q4",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "octave_octave1_1",
                "lo_frequency": 5950000000.0,
            },
        },
        "rr5": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 200,
            "smearing": 0,
            "intermediate_frequency": 25800000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q5",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "octave_octave1_1",
                "lo_frequency": 5950000000.0,
            },
        },
        "q1_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 116555000.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q1",
                "x90": "x90_pulse_q1",
                "-x90": "-x90_pulse_q1",
                "y90": "y90_pulse_q1",
                "y180": "y180_pulse_q1",
                "-y90": "-y90_pulse_q1",
            },
            "mixInputs": {
                "I": ('con1', 3),
                "Q": ('con1', 4),
                "mixer": "octave_octave1_2",
                "lo_frequency": 4055000000.0,
            },
        },
        "q2_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 101584000.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q2",
                "x90": "x90_pulse_q2",
                "-x90": "-x90_pulse_q2",
                "y90": "y90_pulse_q2",
                "y180": "y180_pulse_q2",
                "-y90": "-y90_pulse_q2",
                "baked_Op_0": "q2_xy_baked_pulse_0",
                "baked_Op_1": "q2_xy_baked_pulse_1",
                "baked_Op_2": "q2_xy_baked_pulse_2",
                "baked_Op_3": "q2_xy_baked_pulse_3",
                "baked_Op_4": "q2_xy_baked_pulse_4",
                "baked_Op_5": "q2_xy_baked_pulse_5",
                "baked_Op_6": "q2_xy_baked_pulse_6",
                "baked_Op_7": "q2_xy_baked_pulse_7",
                "baked_Op_8": "q2_xy_baked_pulse_8",
                "baked_Op_9": "q2_xy_baked_pulse_9",
                "baked_Op_10": "q2_xy_baked_pulse_10",
                "baked_Op_11": "q2_xy_baked_pulse_11",
                "baked_Op_12": "q2_xy_baked_pulse_12",
                "baked_Op_13": "q2_xy_baked_pulse_13",
                "baked_Op_14": "q2_xy_baked_pulse_14",
                "baked_Op_15": "q2_xy_baked_pulse_15",
                "baked_Op_16": "q2_xy_baked_pulse_16",
                "baked_Op_17": "q2_xy_baked_pulse_17",
                "baked_Op_18": "q2_xy_baked_pulse_18",
                "baked_Op_19": "q2_xy_baked_pulse_19",
                "baked_Op_20": "q2_xy_baked_pulse_20",
                "baked_Op_21": "q2_xy_baked_pulse_21",
                "baked_Op_22": "q2_xy_baked_pulse_22",
                "baked_Op_23": "q2_xy_baked_pulse_23",
                "baked_Op_24": "q2_xy_baked_pulse_24",
                "baked_Op_25": "q2_xy_baked_pulse_25",
                "baked_Op_26": "q2_xy_baked_pulse_26",
                "baked_Op_27": "q2_xy_baked_pulse_27",
                "baked_Op_28": "q2_xy_baked_pulse_28",
                "baked_Op_29": "q2_xy_baked_pulse_29",
                "baked_Op_30": "q2_xy_baked_pulse_30",
                "baked_Op_31": "q2_xy_baked_pulse_31",
                "baked_Op_32": "q2_xy_baked_pulse_32",
                "baked_Op_33": "q2_xy_baked_pulse_33",
                "baked_Op_34": "q2_xy_baked_pulse_34",
                "baked_Op_35": "q2_xy_baked_pulse_35",
                "baked_Op_36": "q2_xy_baked_pulse_36",
                "baked_Op_37": "q2_xy_baked_pulse_37",
                "baked_Op_38": "q2_xy_baked_pulse_38",
                "baked_Op_39": "q2_xy_baked_pulse_39",
                "baked_Op_40": "q2_xy_baked_pulse_40",
                "baked_Op_41": "q2_xy_baked_pulse_41",
                "baked_Op_42": "q2_xy_baked_pulse_42",
                "baked_Op_43": "q2_xy_baked_pulse_43",
                "baked_Op_44": "q2_xy_baked_pulse_44",
                "baked_Op_45": "q2_xy_baked_pulse_45",
                "baked_Op_46": "q2_xy_baked_pulse_46",
                "baked_Op_47": "q2_xy_baked_pulse_47",
                "baked_Op_48": "q2_xy_baked_pulse_48",
                "baked_Op_49": "q2_xy_baked_pulse_49",
                "baked_Op_50": "q2_xy_baked_pulse_50",
            },
            "mixInputs": {
                "I": ('con1', 7),
                "Q": ('con1', 8),
                "mixer": "octave_octave1_4",
                "lo_frequency": 4300000000.0,
            },
        },
        "q3_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 317621000.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q3",
                "x90": "x90_pulse_q3",
                "-x90": "-x90_pulse_q3",
                "y90": "y90_pulse_q3",
                "y180": "y180_pulse_q3",
                "-y90": "-y90_pulse_q3",
                "baked_Op_0": "q3_xy_baked_pulse_0",
                "baked_Op_1": "q3_xy_baked_pulse_1",
                "baked_Op_2": "q3_xy_baked_pulse_2",
                "baked_Op_3": "q3_xy_baked_pulse_3",
                "baked_Op_4": "q3_xy_baked_pulse_4",
                "baked_Op_5": "q3_xy_baked_pulse_5",
                "baked_Op_6": "q3_xy_baked_pulse_6",
                "baked_Op_7": "q3_xy_baked_pulse_7",
                "baked_Op_8": "q3_xy_baked_pulse_8",
                "baked_Op_9": "q3_xy_baked_pulse_9",
                "baked_Op_10": "q3_xy_baked_pulse_10",
                "baked_Op_11": "q3_xy_baked_pulse_11",
                "baked_Op_12": "q3_xy_baked_pulse_12",
                "baked_Op_13": "q3_xy_baked_pulse_13",
                "baked_Op_14": "q3_xy_baked_pulse_14",
                "baked_Op_15": "q3_xy_baked_pulse_15",
                "baked_Op_16": "q3_xy_baked_pulse_16",
                "baked_Op_17": "q3_xy_baked_pulse_17",
                "baked_Op_18": "q3_xy_baked_pulse_18",
                "baked_Op_19": "q3_xy_baked_pulse_19",
                "baked_Op_20": "q3_xy_baked_pulse_20",
                "baked_Op_21": "q3_xy_baked_pulse_21",
                "baked_Op_22": "q3_xy_baked_pulse_22",
                "baked_Op_23": "q3_xy_baked_pulse_23",
                "baked_Op_24": "q3_xy_baked_pulse_24",
                "baked_Op_25": "q3_xy_baked_pulse_25",
                "baked_Op_26": "q3_xy_baked_pulse_26",
                "baked_Op_27": "q3_xy_baked_pulse_27",
                "baked_Op_28": "q3_xy_baked_pulse_28",
                "baked_Op_29": "q3_xy_baked_pulse_29",
                "baked_Op_30": "q3_xy_baked_pulse_30",
                "baked_Op_31": "q3_xy_baked_pulse_31",
                "baked_Op_32": "q3_xy_baked_pulse_32",
                "baked_Op_33": "q3_xy_baked_pulse_33",
                "baked_Op_34": "q3_xy_baked_pulse_34",
                "baked_Op_35": "q3_xy_baked_pulse_35",
                "baked_Op_36": "q3_xy_baked_pulse_36",
                "baked_Op_37": "q3_xy_baked_pulse_37",
                "baked_Op_38": "q3_xy_baked_pulse_38",
                "baked_Op_39": "q3_xy_baked_pulse_39",
                "baked_Op_40": "q3_xy_baked_pulse_40",
                "baked_Op_41": "q3_xy_baked_pulse_41",
                "baked_Op_42": "q3_xy_baked_pulse_42",
                "baked_Op_43": "q3_xy_baked_pulse_43",
                "baked_Op_44": "q3_xy_baked_pulse_44",
                "baked_Op_45": "q3_xy_baked_pulse_45",
                "baked_Op_46": "q3_xy_baked_pulse_46",
                "baked_Op_47": "q3_xy_baked_pulse_47",
                "baked_Op_48": "q3_xy_baked_pulse_48",
                "baked_Op_49": "q3_xy_baked_pulse_49",
                "baked_Op_50": "q3_xy_baked_pulse_50",
            },
            "mixInputs": {
                "I": ('con1', 3),
                "Q": ('con1', 4),
                "mixer": "octave_octave1_3",
                "lo_frequency": 3850000000.0,
            },
        },
        "q4_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 89863100.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q4",
                "x90": "x90_pulse_q4",
                "-x90": "-x90_pulse_q4",
                "y90": "y90_pulse_q4",
                "y180": "y180_pulse_q4",
                "-y90": "-y90_pulse_q4",
            },
            "mixInputs": {
                "I": ('con1', 7),
                "Q": ('con1', 8),
                "mixer": "octave_octave1_5",
                "lo_frequency": 3950000000.0,
            },
        },
        "q5_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 92000000.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q5",
                "x90": "x90_pulse_q5",
                "-x90": "-x90_pulse_q5",
                "y90": "y90_pulse_q5",
                "y180": "y180_pulse_q5",
                "-y90": "-y90_pulse_q5",
            },
            "mixInputs": {
                "I": ('con1', 7),
                "Q": ('con1', 8),
                "mixer": "octave_octave2_1",
                "lo_frequency": 4750000000.0,
            },
        },
        "q1_z": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "operations": {
                "const": "const_flux_pulse",
            },
            "singleInput": {
                "port": ('con1', 5),
            },
        },
        "q2_z": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "operations": {
                "const": "const_flux_pulse",
                "cz_1_2": "gft_cz_pulse_1_2_q2",
                "cz": "cz_flux_pulse",
                "baked_Op_0": "q2_z_baked_pulse_0",
                "baked_Op_1": "q2_z_baked_pulse_1",
                "baked_Op_2": "q2_z_baked_pulse_2",
                "baked_Op_3": "q2_z_baked_pulse_3",
                "baked_Op_4": "q2_z_baked_pulse_4",
                "baked_Op_5": "q2_z_baked_pulse_5",
                "baked_Op_6": "q2_z_baked_pulse_6",
                "baked_Op_7": "q2_z_baked_pulse_7",
                "baked_Op_8": "q2_z_baked_pulse_8",
                "baked_Op_9": "q2_z_baked_pulse_9",
                "baked_Op_10": "q2_z_baked_pulse_10",
                "baked_Op_11": "q2_z_baked_pulse_11",
                "baked_Op_12": "q2_z_baked_pulse_12",
                "baked_Op_13": "q2_z_baked_pulse_13",
                "baked_Op_14": "q2_z_baked_pulse_14",
                "baked_Op_15": "q2_z_baked_pulse_15",
                "baked_Op_16": "q2_z_baked_pulse_16",
                "baked_Op_17": "q2_z_baked_pulse_17",
                "baked_Op_18": "q2_z_baked_pulse_18",
                "baked_Op_19": "q2_z_baked_pulse_19",
                "baked_Op_20": "q2_z_baked_pulse_20",
                "baked_Op_21": "q2_z_baked_pulse_21",
                "baked_Op_22": "q2_z_baked_pulse_22",
                "baked_Op_23": "q2_z_baked_pulse_23",
                "baked_Op_24": "q2_z_baked_pulse_24",
                "baked_Op_25": "q2_z_baked_pulse_25",
                "baked_Op_26": "q2_z_baked_pulse_26",
                "baked_Op_27": "q2_z_baked_pulse_27",
                "baked_Op_28": "q2_z_baked_pulse_28",
                "baked_Op_29": "q2_z_baked_pulse_29",
                "baked_Op_30": "q2_z_baked_pulse_30",
                "baked_Op_31": "q2_z_baked_pulse_31",
                "baked_Op_32": "q2_z_baked_pulse_32",
                "baked_Op_33": "q2_z_baked_pulse_33",
                "baked_Op_34": "q2_z_baked_pulse_34",
                "baked_Op_35": "q2_z_baked_pulse_35",
                "baked_Op_36": "q2_z_baked_pulse_36",
                "baked_Op_37": "q2_z_baked_pulse_37",
                "baked_Op_38": "q2_z_baked_pulse_38",
                "baked_Op_39": "q2_z_baked_pulse_39",
                "baked_Op_40": "q2_z_baked_pulse_40",
                "baked_Op_41": "q2_z_baked_pulse_41",
                "baked_Op_42": "q2_z_baked_pulse_42",
                "baked_Op_43": "q2_z_baked_pulse_43",
                "baked_Op_44": "q2_z_baked_pulse_44",
                "baked_Op_45": "q2_z_baked_pulse_45",
                "baked_Op_46": "q2_z_baked_pulse_46",
                "baked_Op_47": "q2_z_baked_pulse_47",
                "baked_Op_48": "q2_z_baked_pulse_48",
                "baked_Op_49": "q2_z_baked_pulse_49",
                "baked_Op_50": "q2_z_baked_pulse_50",
            },
            "singleInput": {
                "port": ('con1', 6),
            },
        },
        "q3_z": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "operations": {
                "const": "const_flux_pulse",
            },
            "singleInput": {
                "port": ('con1', 9),
            },
        },
        "q4_z": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "operations": {
                "const": "const_flux_pulse",
            },
            "singleInput": {
                "port": ('con1', 10),
            },
        },
        "q5_z": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "operations": {
                "const": "const_flux_pulse",
            },
            "singleInput": {
                "port": ('con1', 5),
            },
        },
    },
    "pulses": {
        "const_flux_pulse": {
            "length": 200,
            "waveforms": {
                "single": "const_flux_wf",
            },
            "operation": "control",
        },
        "const_pulse": {
            "length": 100,
            "waveforms": {
                "I": "const_wf",
                "Q": "zero_wf",
            },
            "operation": "control",
        },
        "saturation_pulse": {
            "length": 1000,
            "waveforms": {
                "I": "saturation_wf",
                "Q": "zero_wf",
            },
            "operation": "control",
        },
        "cz_flux_pulse": {
            "length": 24,
            "waveforms": {
                "single": "cz_wf",
            },
            "operation": "control",
        },
        "x90_pulse_q1": {
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q1",
                "Q": "x90_Q_wf_q1",
            },
            "operation": "control",
        },
        "x180_pulse_q1": {
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q1",
                "Q": "x180_Q_wf_q1",
            },
            "operation": "control",
        },
        "-x90_pulse_q1": {
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q1",
                "Q": "minus_x90_Q_wf_q1",
            },
            "operation": "control",
        },
        "y90_pulse_q1": {
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q1",
                "Q": "y90_Q_wf_q1",
            },
            "operation": "control",
        },
        "y180_pulse_q1": {
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q1",
                "Q": "y180_Q_wf_q1",
            },
            "operation": "control",
        },
        "-y90_pulse_q1": {
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q1",
                "Q": "minus_y90_Q_wf_q1",
            },
            "operation": "control",
        },
        "readout_pulse_q1": {
            "length": 1700,
            "waveforms": {
                "I": "readout_wf_q1",
                "Q": "zero_wf",
            },
            "digital_marker": "ON",
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q1",
                "rotated_sin": "rotated_sine_weights_q1",
                "rotated_minus_sin": "rotated_minus_sine_weights_q1",
                "opt_cos": "opt_cosine_weights_q1",
                "opt_sin": "opt_sine_weights_q1",
                "opt_minus_sin": "opt_minus_sine_weights_q1",
            },
            "operation": "measurement",
        },
        "x90_pulse_q2": {
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q2",
                "Q": "x90_Q_wf_q2",
            },
            "operation": "control",
        },
        "x180_pulse_q2": {
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q2",
                "Q": "x180_Q_wf_q2",
            },
            "operation": "control",
        },
        "-x90_pulse_q2": {
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q2",
                "Q": "minus_x90_Q_wf_q2",
            },
            "operation": "control",
        },
        "y90_pulse_q2": {
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q2",
                "Q": "y90_Q_wf_q2",
            },
            "operation": "control",
        },
        "y180_pulse_q2": {
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q2",
                "Q": "y180_Q_wf_q2",
            },
            "operation": "control",
        },
        "-y90_pulse_q2": {
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q2",
                "Q": "minus_y90_Q_wf_q2",
            },
            "operation": "control",
        },
        "readout_pulse_q2": {
            "length": 1700,
            "waveforms": {
                "I": "readout_wf_q2",
                "Q": "zero_wf",
            },
            "digital_marker": "ON",
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q2",
                "rotated_sin": "rotated_sine_weights_q2",
                "rotated_minus_sin": "rotated_minus_sine_weights_q2",
                "opt_cos": "opt_cosine_weights_q2",
                "opt_sin": "opt_sine_weights_q2",
                "opt_minus_sin": "opt_minus_sine_weights_q2",
            },
            "operation": "measurement",
        },
        "x90_pulse_q3": {
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q3",
                "Q": "x90_Q_wf_q3",
            },
            "operation": "control",
        },
        "x180_pulse_q3": {
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q3",
                "Q": "x180_Q_wf_q3",
            },
            "operation": "control",
        },
        "-x90_pulse_q3": {
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q3",
                "Q": "minus_x90_Q_wf_q3",
            },
            "operation": "control",
        },
        "y90_pulse_q3": {
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q3",
                "Q": "y90_Q_wf_q3",
            },
            "operation": "control",
        },
        "y180_pulse_q3": {
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q3",
                "Q": "y180_Q_wf_q3",
            },
            "operation": "control",
        },
        "-y90_pulse_q3": {
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q3",
                "Q": "minus_y90_Q_wf_q3",
            },
            "operation": "control",
        },
        "readout_pulse_q3": {
            "length": 1700,
            "waveforms": {
                "I": "readout_wf_q3",
                "Q": "zero_wf",
            },
            "digital_marker": "ON",
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q3",
                "rotated_sin": "rotated_sine_weights_q3",
                "rotated_minus_sin": "rotated_minus_sine_weights_q3",
                "opt_cos": "opt_cosine_weights_q3",
                "opt_sin": "opt_sine_weights_q3",
                "opt_minus_sin": "opt_minus_sine_weights_q3",
            },
            "operation": "measurement",
        },
        "x90_pulse_q4": {
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q4",
                "Q": "x90_Q_wf_q4",
            },
            "operation": "control",
        },
        "x180_pulse_q4": {
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q4",
                "Q": "x180_Q_wf_q4",
            },
            "operation": "control",
        },
        "-x90_pulse_q4": {
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q4",
                "Q": "minus_x90_Q_wf_q4",
            },
            "operation": "control",
        },
        "y90_pulse_q4": {
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q4",
                "Q": "y90_Q_wf_q4",
            },
            "operation": "control",
        },
        "y180_pulse_q4": {
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q4",
                "Q": "y180_Q_wf_q4",
            },
            "operation": "control",
        },
        "-y90_pulse_q4": {
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q4",
                "Q": "minus_y90_Q_wf_q4",
            },
            "operation": "control",
        },
        "readout_pulse_q4": {
            "length": 1700,
            "waveforms": {
                "I": "readout_wf_q4",
                "Q": "zero_wf",
            },
            "digital_marker": "ON",
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q4",
                "rotated_sin": "rotated_sine_weights_q4",
                "rotated_minus_sin": "rotated_minus_sine_weights_q4",
                "opt_cos": "opt_cosine_weights_q4",
                "opt_sin": "opt_sine_weights_q4",
                "opt_minus_sin": "opt_minus_sine_weights_q4",
            },
            "operation": "measurement",
        },
        "x90_pulse_q5": {
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q5",
                "Q": "x90_Q_wf_q5",
            },
            "operation": "control",
        },
        "x180_pulse_q5": {
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q5",
                "Q": "x180_Q_wf_q5",
            },
            "operation": "control",
        },
        "-x90_pulse_q5": {
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q5",
                "Q": "minus_x90_Q_wf_q5",
            },
            "operation": "control",
        },
        "y90_pulse_q5": {
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q5",
                "Q": "y90_Q_wf_q5",
            },
            "operation": "control",
        },
        "y180_pulse_q5": {
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q5",
                "Q": "y180_Q_wf_q5",
            },
            "operation": "control",
        },
        "-y90_pulse_q5": {
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q5",
                "Q": "minus_y90_Q_wf_q5",
            },
            "operation": "control",
        },
        "readout_pulse_q5": {
            "length": 1700,
            "waveforms": {
                "I": "readout_wf_q5",
                "Q": "zero_wf",
            },
            "digital_marker": "ON",
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q5",
                "rotated_sin": "rotated_sine_weights_q5",
                "rotated_minus_sin": "rotated_minus_sine_weights_q5",
                "opt_cos": "opt_cosine_weights_q5",
                "opt_sin": "opt_sine_weights_q5",
                "opt_minus_sin": "opt_minus_sine_weights_q5",
            },
            "operation": "measurement",
        },
        "gft_cz_pulse_1_2_q2": {
            "length": 24,
            "waveforms": {
                "single": "gft_cz_wf_1_2_q2",
            },
            "operation": "control",
        },
        "g_cz_pulse_1_2_q2": {
            "length": 16,
            "waveforms": {
                "single": "g_cz_wf_1_2_q2",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_0": {
            "length": 40,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_0",
                "Q": "q2_xy_baked_wf_Q_0",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_0": {
            "length": 40,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_0",
                "Q": "q3_xy_baked_wf_Q_0",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_0": {
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_0",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_1": {
            "length": 40,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_1",
                "Q": "q2_xy_baked_wf_Q_1",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_1": {
            "length": 40,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_1",
                "Q": "q3_xy_baked_wf_Q_1",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_1": {
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_1",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_2": {
            "length": 40,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_2",
                "Q": "q2_xy_baked_wf_Q_2",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_2": {
            "length": 40,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_2",
                "Q": "q3_xy_baked_wf_Q_2",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_2": {
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_2",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_3": {
            "length": 40,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_3",
                "Q": "q2_xy_baked_wf_Q_3",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_3": {
            "length": 40,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_3",
                "Q": "q3_xy_baked_wf_Q_3",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_3": {
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_3",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_4": {
            "length": 40,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_4",
                "Q": "q2_xy_baked_wf_Q_4",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_4": {
            "length": 40,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_4",
                "Q": "q3_xy_baked_wf_Q_4",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_4": {
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_4",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_5": {
            "length": 40,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_5",
                "Q": "q2_xy_baked_wf_Q_5",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_5": {
            "length": 40,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_5",
                "Q": "q3_xy_baked_wf_Q_5",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_5": {
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_5",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_6": {
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_6",
                "Q": "q2_xy_baked_wf_Q_6",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_6": {
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_6",
                "Q": "q3_xy_baked_wf_Q_6",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_6": {
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_6",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_7": {
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_7",
                "Q": "q2_xy_baked_wf_Q_7",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_7": {
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_7",
                "Q": "q3_xy_baked_wf_Q_7",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_7": {
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_7",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_8": {
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_8",
                "Q": "q2_xy_baked_wf_Q_8",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_8": {
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_8",
                "Q": "q3_xy_baked_wf_Q_8",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_8": {
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_8",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_9": {
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_9",
                "Q": "q2_xy_baked_wf_Q_9",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_9": {
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_9",
                "Q": "q3_xy_baked_wf_Q_9",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_9": {
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_9",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_10": {
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_10",
                "Q": "q2_xy_baked_wf_Q_10",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_10": {
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_10",
                "Q": "q3_xy_baked_wf_Q_10",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_10": {
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_10",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_11": {
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_11",
                "Q": "q2_xy_baked_wf_Q_11",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_11": {
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_11",
                "Q": "q3_xy_baked_wf_Q_11",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_11": {
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_11",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_12": {
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_12",
                "Q": "q2_xy_baked_wf_Q_12",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_12": {
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_12",
                "Q": "q3_xy_baked_wf_Q_12",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_12": {
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_12",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_13": {
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_13",
                "Q": "q2_xy_baked_wf_Q_13",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_13": {
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_13",
                "Q": "q3_xy_baked_wf_Q_13",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_13": {
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_13",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_14": {
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_14",
                "Q": "q2_xy_baked_wf_Q_14",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_14": {
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_14",
                "Q": "q3_xy_baked_wf_Q_14",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_14": {
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_14",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_15": {
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_15",
                "Q": "q2_xy_baked_wf_Q_15",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_15": {
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_15",
                "Q": "q3_xy_baked_wf_Q_15",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_15": {
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_15",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_16": {
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_16",
                "Q": "q2_xy_baked_wf_Q_16",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_16": {
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_16",
                "Q": "q3_xy_baked_wf_Q_16",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_16": {
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_16",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_17": {
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_17",
                "Q": "q2_xy_baked_wf_Q_17",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_17": {
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_17",
                "Q": "q3_xy_baked_wf_Q_17",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_17": {
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_17",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_18": {
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_18",
                "Q": "q2_xy_baked_wf_Q_18",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_18": {
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_18",
                "Q": "q3_xy_baked_wf_Q_18",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_18": {
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_18",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_19": {
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_19",
                "Q": "q2_xy_baked_wf_Q_19",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_19": {
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_19",
                "Q": "q3_xy_baked_wf_Q_19",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_19": {
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_19",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_20": {
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_20",
                "Q": "q2_xy_baked_wf_Q_20",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_20": {
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_20",
                "Q": "q3_xy_baked_wf_Q_20",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_20": {
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_20",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_21": {
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_21",
                "Q": "q2_xy_baked_wf_Q_21",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_21": {
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_21",
                "Q": "q3_xy_baked_wf_Q_21",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_21": {
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_21",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_22": {
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_22",
                "Q": "q2_xy_baked_wf_Q_22",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_22": {
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_22",
                "Q": "q3_xy_baked_wf_Q_22",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_22": {
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_22",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_23": {
            "length": 148,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_23",
                "Q": "q2_xy_baked_wf_Q_23",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_23": {
            "length": 148,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_23",
                "Q": "q3_xy_baked_wf_Q_23",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_23": {
            "length": 148,
            "waveforms": {
                "single": "q2_z_baked_wf_23",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_24": {
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_24",
                "Q": "q2_xy_baked_wf_Q_24",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_24": {
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_24",
                "Q": "q3_xy_baked_wf_Q_24",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_24": {
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_24",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_25": {
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_25",
                "Q": "q2_xy_baked_wf_Q_25",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_25": {
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_25",
                "Q": "q3_xy_baked_wf_Q_25",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_25": {
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_25",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_26": {
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_26",
                "Q": "q2_xy_baked_wf_Q_26",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_26": {
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_26",
                "Q": "q3_xy_baked_wf_Q_26",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_26": {
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_26",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_27": {
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_27",
                "Q": "q2_xy_baked_wf_Q_27",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_27": {
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_27",
                "Q": "q3_xy_baked_wf_Q_27",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_27": {
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_27",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_28": {
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_28",
                "Q": "q2_xy_baked_wf_Q_28",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_28": {
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_28",
                "Q": "q3_xy_baked_wf_Q_28",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_28": {
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_28",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_29": {
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_29",
                "Q": "q2_xy_baked_wf_Q_29",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_29": {
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_29",
                "Q": "q3_xy_baked_wf_Q_29",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_29": {
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_29",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_30": {
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_30",
                "Q": "q2_xy_baked_wf_Q_30",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_30": {
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_30",
                "Q": "q3_xy_baked_wf_Q_30",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_30": {
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_30",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_31": {
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_31",
                "Q": "q2_xy_baked_wf_Q_31",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_31": {
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_31",
                "Q": "q3_xy_baked_wf_Q_31",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_31": {
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_31",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_32": {
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_32",
                "Q": "q2_xy_baked_wf_Q_32",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_32": {
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_32",
                "Q": "q3_xy_baked_wf_Q_32",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_32": {
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_32",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_33": {
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_33",
                "Q": "q2_xy_baked_wf_Q_33",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_33": {
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_33",
                "Q": "q3_xy_baked_wf_Q_33",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_33": {
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_33",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_34": {
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_34",
                "Q": "q2_xy_baked_wf_Q_34",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_34": {
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_34",
                "Q": "q3_xy_baked_wf_Q_34",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_34": {
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_34",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_35": {
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_35",
                "Q": "q2_xy_baked_wf_Q_35",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_35": {
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_35",
                "Q": "q3_xy_baked_wf_Q_35",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_35": {
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_35",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_36": {
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_36",
                "Q": "q2_xy_baked_wf_Q_36",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_36": {
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_36",
                "Q": "q3_xy_baked_wf_Q_36",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_36": {
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_36",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_37": {
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_37",
                "Q": "q2_xy_baked_wf_Q_37",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_37": {
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_37",
                "Q": "q3_xy_baked_wf_Q_37",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_37": {
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_37",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_38": {
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_38",
                "Q": "q2_xy_baked_wf_Q_38",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_38": {
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_38",
                "Q": "q3_xy_baked_wf_Q_38",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_38": {
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_38",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_39": {
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_39",
                "Q": "q2_xy_baked_wf_Q_39",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_39": {
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_39",
                "Q": "q3_xy_baked_wf_Q_39",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_39": {
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_39",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_40": {
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_40",
                "Q": "q2_xy_baked_wf_Q_40",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_40": {
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_40",
                "Q": "q3_xy_baked_wf_Q_40",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_40": {
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_40",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_41": {
            "length": 252,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_41",
                "Q": "q2_xy_baked_wf_Q_41",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_41": {
            "length": 252,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_41",
                "Q": "q3_xy_baked_wf_Q_41",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_41": {
            "length": 252,
            "waveforms": {
                "single": "q2_z_baked_wf_41",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_42": {
            "length": 356,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_42",
                "Q": "q2_xy_baked_wf_Q_42",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_42": {
            "length": 356,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_42",
                "Q": "q3_xy_baked_wf_Q_42",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_42": {
            "length": 356,
            "waveforms": {
                "single": "q2_z_baked_wf_42",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_43": {
            "length": 356,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_43",
                "Q": "q2_xy_baked_wf_Q_43",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_43": {
            "length": 356,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_43",
                "Q": "q3_xy_baked_wf_Q_43",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_43": {
            "length": 356,
            "waveforms": {
                "single": "q2_z_baked_wf_43",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_44": {
            "length": 356,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_44",
                "Q": "q2_xy_baked_wf_Q_44",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_44": {
            "length": 356,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_44",
                "Q": "q3_xy_baked_wf_Q_44",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_44": {
            "length": 356,
            "waveforms": {
                "single": "q2_z_baked_wf_44",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_45": {
            "length": 356,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_45",
                "Q": "q2_xy_baked_wf_Q_45",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_45": {
            "length": 356,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_45",
                "Q": "q3_xy_baked_wf_Q_45",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_45": {
            "length": 356,
            "waveforms": {
                "single": "q2_z_baked_wf_45",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_46": {
            "length": 356,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_46",
                "Q": "q2_xy_baked_wf_Q_46",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_46": {
            "length": 356,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_46",
                "Q": "q3_xy_baked_wf_Q_46",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_46": {
            "length": 356,
            "waveforms": {
                "single": "q2_z_baked_wf_46",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_47": {
            "length": 356,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_47",
                "Q": "q2_xy_baked_wf_Q_47",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_47": {
            "length": 356,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_47",
                "Q": "q3_xy_baked_wf_Q_47",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_47": {
            "length": 356,
            "waveforms": {
                "single": "q2_z_baked_wf_47",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_48": {
            "length": 40,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_48",
                "Q": "q2_xy_baked_wf_Q_48",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_48": {
            "length": 40,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_48",
                "Q": "q3_xy_baked_wf_Q_48",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_48": {
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_48",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_49": {
            "length": 40,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_49",
                "Q": "q2_xy_baked_wf_Q_49",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_49": {
            "length": 40,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_49",
                "Q": "q3_xy_baked_wf_Q_49",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_49": {
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_49",
            },
            "operation": "control",
        },
        "q2_xy_baked_pulse_50": {
            "length": 40,
            "waveforms": {
                "I": "q2_xy_baked_wf_I_50",
                "Q": "q2_xy_baked_wf_Q_50",
            },
            "operation": "control",
        },
        "q3_xy_baked_pulse_50": {
            "length": 40,
            "waveforms": {
                "I": "q3_xy_baked_wf_I_50",
                "Q": "q3_xy_baked_wf_Q_50",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_50": {
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_50",
            },
            "operation": "control",
        },
    },
    "waveforms": {
        "const_wf": {
            "sample": 0.27,
            "type": "constant",
        },
        "saturation_wf": {
            "sample": 0.1,
            "type": "constant",
        },
        "const_flux_wf": {
            "sample": 0.5,
            "type": "constant",
        },
        "zero_wf": {
            "sample": 0.0,
            "type": "constant",
        },
        "cz_wf": {
            "sample": 0.1755,
            "type": "constant",
        },
        "x90_I_wf_q1": {
            "samples": [0.0, 0.0006444587008155979, 0.0013789582933809714, 0.0022051982768183614, 0.0031222127073087685, 0.004125919855569243, 0.005208759218787376, 0.006359454317362786, 0.007562936707760972, 0.00880046014810808, 0.010049923940608054, 0.011286411594113968, 0.012482935924108854, 0.01361136568670365, 0.014643493214701668, 0.015552188778029734, 0.01631257696424561, 0.016903164482871647, 0.0173068482813562] + [0.0175117380691362] * 2 + [0.0173068482813562, 0.016903164482871647, 0.01631257696424561, 0.015552188778029734, 0.014643493214701668, 0.01361136568670365, 0.012482935924108854, 0.011286411594113968, 0.010049923940608054, 0.00880046014810808, 0.007562936707760972, 0.006359454317362786, 0.005208759218787376, 0.004125919855569243, 0.0031222127073087685, 0.0022051982768183614, 0.0013789582933809714, 0.0006444587008155979, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q1": {
            "samples": [-0.000294371015801747, -0.00033771326152687455, -0.0003824612517831482, -0.00042742842419887534, -0.000471192393133838, -0.0005121282664652718, -0.0005484609868057831, -0.0005783360545561637, -0.0005999063142135595, -0.0006114307617658487, -0.0006113797347661263, -0.0005985395640585965, -0.0005721089728557221, -0.0005317793467624805, -0.0004777915535380474, -0.0004109632775403929, -0.0003326827832700226, -0.00024486748742062145, -0.00014988848327730165, -5.046496252607702e-05, 5.046496252607702e-05, 0.00014988848327730165, 0.00024486748742062145, 0.0003326827832700226, 0.0004109632775403929, 0.0004777915535380474, 0.0005317793467624805, 0.0005721089728557221, 0.0005985395640585965, 0.0006113797347661263, 0.0006114307617658487, 0.0005999063142135595, 0.0005783360545561637, 0.0005484609868057831, 0.0005121282664652718, 0.000471192393133838, 0.00042742842419887534, 0.0003824612517831482, 0.00033771326152687455, 0.000294371015801747],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q1": {
            "samples": [0.0, 0.0012889174016311958, 0.002757916586761943, 0.004410396553636723, 0.006244425414617537, 0.008251839711138485, 0.010417518437574751, 0.012718908634725572, 0.015125873415521945, 0.01760092029621616, 0.020099847881216108, 0.022572823188227936, 0.02496587184821771, 0.0272227313734073, 0.029286986429403337, 0.03110437755605947, 0.03262515392849122, 0.033806328965743294, 0.0346136965627124] + [0.0350234761382724] * 2 + [0.0346136965627124, 0.033806328965743294, 0.03262515392849122, 0.03110437755605947, 0.029286986429403337, 0.0272227313734073, 0.02496587184821771, 0.022572823188227936, 0.020099847881216108, 0.01760092029621616, 0.015125873415521945, 0.012718908634725572, 0.010417518437574751, 0.008251839711138485, 0.006244425414617537, 0.004410396553636723, 0.002757916586761943, 0.0012889174016311958, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q1": {
            "samples": [-0.000588742031603494, -0.0006754265230537491, -0.0007649225035662964, -0.0008548568483977507, -0.000942384786267676, -0.0010242565329305435, -0.0010969219736115662, -0.0011566721091123273, -0.001199812628427119, -0.0012228615235316974, -0.0012227594695322526, -0.001197079128117193, -0.0011442179457114442, -0.001063558693524961, -0.0009555831070760948, -0.0008219265550807858, -0.0006653655665400452, -0.0004897349748412429, -0.0002997769665546033, -0.00010092992505215404, 0.00010092992505215404, 0.0002997769665546033, 0.0004897349748412429, 0.0006653655665400452, 0.0008219265550807858, 0.0009555831070760948, 0.001063558693524961, 0.0011442179457114442, 0.001197079128117193, 0.0012227594695322526, 0.0012228615235316974, 0.001199812628427119, 0.0011566721091123273, 0.0010969219736115662, 0.0010242565329305435, 0.000942384786267676, 0.0008548568483977507, 0.0007649225035662964, 0.0006754265230537491, 0.000588742031603494],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q1": {
            "samples": [0.0, -0.0006444587008155979, -0.0013789582933809714, -0.0022051982768183614, -0.0031222127073087685, -0.004125919855569243, -0.005208759218787376, -0.006359454317362786, -0.007562936707760972, -0.00880046014810808, -0.010049923940608054, -0.011286411594113968, -0.012482935924108854, -0.01361136568670365, -0.014643493214701668, -0.015552188778029734, -0.01631257696424561, -0.016903164482871647, -0.0173068482813562] + [-0.0175117380691362] * 2 + [-0.0173068482813562, -0.016903164482871647, -0.01631257696424561, -0.015552188778029734, -0.014643493214701668, -0.01361136568670365, -0.012482935924108854, -0.011286411594113968, -0.010049923940608054, -0.00880046014810808, -0.007562936707760972, -0.006359454317362786, -0.005208759218787376, -0.004125919855569243, -0.0031222127073087685, -0.0022051982768183614, -0.0013789582933809714, -0.0006444587008155979, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q1": {
            "samples": [0.000294371015801747, 0.00033771326152687455, 0.0003824612517831482, 0.00042742842419887534, 0.000471192393133838, 0.0005121282664652718, 0.0005484609868057831, 0.0005783360545561637, 0.0005999063142135595, 0.0006114307617658487, 0.0006113797347661263, 0.0005985395640585965, 0.0005721089728557221, 0.0005317793467624805, 0.0004777915535380474, 0.0004109632775403929, 0.0003326827832700226, 0.00024486748742062145, 0.00014988848327730165, 5.046496252607702e-05, -5.046496252607702e-05, -0.00014988848327730165, -0.00024486748742062145, -0.0003326827832700226, -0.0004109632775403929, -0.0004777915535380474, -0.0005317793467624805, -0.0005721089728557221, -0.0005985395640585965, -0.0006113797347661263, -0.0006114307617658487, -0.0005999063142135595, -0.0005783360545561637, -0.0005484609868057831, -0.0005121282664652718, -0.000471192393133838, -0.00042742842419887534, -0.0003824612517831482, -0.00033771326152687455, -0.000294371015801747],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q1": {
            "samples": [0.000294371015801747, 0.00033771326152687455, 0.0003824612517831482, 0.00042742842419887534, 0.000471192393133838, 0.0005121282664652718, 0.0005484609868057831, 0.0005783360545561637, 0.0005999063142135595, 0.0006114307617658487, 0.0006113797347661263, 0.0005985395640585965, 0.0005721089728557221, 0.0005317793467624805, 0.0004777915535380474, 0.0004109632775403929, 0.0003326827832700226, 0.00024486748742062145, 0.00014988848327730165, 5.046496252607702e-05, -5.046496252607702e-05, -0.00014988848327730165, -0.00024486748742062145, -0.0003326827832700226, -0.0004109632775403929, -0.0004777915535380474, -0.0005317793467624805, -0.0005721089728557221, -0.0005985395640585965, -0.0006113797347661263, -0.0006114307617658487, -0.0005999063142135595, -0.0005783360545561637, -0.0005484609868057831, -0.0005121282664652718, -0.000471192393133838, -0.00042742842419887534, -0.0003824612517831482, -0.00033771326152687455, -0.000294371015801747],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q1": {
            "samples": [0.0, 0.0006444587008155979, 0.0013789582933809714, 0.0022051982768183614, 0.0031222127073087685, 0.004125919855569243, 0.005208759218787376, 0.006359454317362786, 0.007562936707760972, 0.00880046014810808, 0.010049923940608054, 0.011286411594113968, 0.012482935924108854, 0.01361136568670365, 0.014643493214701668, 0.015552188778029734, 0.01631257696424561, 0.016903164482871647, 0.0173068482813562] + [0.0175117380691362] * 2 + [0.0173068482813562, 0.016903164482871647, 0.01631257696424561, 0.015552188778029734, 0.014643493214701668, 0.01361136568670365, 0.012482935924108854, 0.011286411594113968, 0.010049923940608054, 0.00880046014810808, 0.007562936707760972, 0.006359454317362786, 0.005208759218787376, 0.004125919855569243, 0.0031222127073087685, 0.0022051982768183614, 0.0013789582933809714, 0.0006444587008155979, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q1": {
            "samples": [0.000588742031603494, 0.0006754265230537491, 0.0007649225035662964, 0.0008548568483977507, 0.000942384786267676, 0.0010242565329305435, 0.0010969219736115662, 0.0011566721091123273, 0.001199812628427119, 0.0012228615235316974, 0.0012227594695322526, 0.001197079128117193, 0.0011442179457114442, 0.001063558693524961, 0.0009555831070760948, 0.0008219265550807858, 0.0006653655665400452, 0.0004897349748412429, 0.0002997769665546033, 0.00010092992505215404, -0.00010092992505215404, -0.0002997769665546033, -0.0004897349748412429, -0.0006653655665400452, -0.0008219265550807858, -0.0009555831070760948, -0.001063558693524961, -0.0011442179457114442, -0.001197079128117193, -0.0012227594695322526, -0.0012228615235316974, -0.001199812628427119, -0.0011566721091123273, -0.0010969219736115662, -0.0010242565329305435, -0.000942384786267676, -0.0008548568483977507, -0.0007649225035662964, -0.0006754265230537491, -0.000588742031603494],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q1": {
            "samples": [0.0, 0.0012889174016311958, 0.002757916586761943, 0.004410396553636723, 0.006244425414617537, 0.008251839711138485, 0.010417518437574751, 0.012718908634725572, 0.015125873415521945, 0.01760092029621616, 0.020099847881216108, 0.022572823188227936, 0.02496587184821771, 0.0272227313734073, 0.029286986429403337, 0.03110437755605947, 0.03262515392849122, 0.033806328965743294, 0.0346136965627124] + [0.0350234761382724] * 2 + [0.0346136965627124, 0.033806328965743294, 0.03262515392849122, 0.03110437755605947, 0.029286986429403337, 0.0272227313734073, 0.02496587184821771, 0.022572823188227936, 0.020099847881216108, 0.01760092029621616, 0.015125873415521945, 0.012718908634725572, 0.010417518437574751, 0.008251839711138485, 0.006244425414617537, 0.004410396553636723, 0.002757916586761943, 0.0012889174016311958, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q1": {
            "samples": [-0.000294371015801747, -0.00033771326152687455, -0.0003824612517831482, -0.00042742842419887534, -0.000471192393133838, -0.0005121282664652718, -0.0005484609868057831, -0.0005783360545561637, -0.0005999063142135595, -0.0006114307617658487, -0.0006113797347661263, -0.0005985395640585965, -0.0005721089728557221, -0.0005317793467624805, -0.0004777915535380474, -0.0004109632775403929, -0.0003326827832700226, -0.00024486748742062145, -0.00014988848327730165, -5.046496252607702e-05, 5.046496252607702e-05, 0.00014988848327730165, 0.00024486748742062145, 0.0003326827832700226, 0.0004109632775403929, 0.0004777915535380474, 0.0005317793467624805, 0.0005721089728557221, 0.0005985395640585965, 0.0006113797347661263, 0.0006114307617658487, 0.0005999063142135595, 0.0005783360545561637, 0.0005484609868057831, 0.0005121282664652718, 0.000471192393133838, 0.00042742842419887534, 0.0003824612517831482, 0.00033771326152687455, 0.000294371015801747],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q1": {
            "samples": [0.0, -0.0006444587008155979, -0.0013789582933809714, -0.0022051982768183614, -0.0031222127073087685, -0.004125919855569243, -0.005208759218787376, -0.006359454317362786, -0.007562936707760972, -0.00880046014810808, -0.010049923940608054, -0.011286411594113968, -0.012482935924108854, -0.01361136568670365, -0.014643493214701668, -0.015552188778029734, -0.01631257696424561, -0.016903164482871647, -0.0173068482813562] + [-0.0175117380691362] * 2 + [-0.0173068482813562, -0.016903164482871647, -0.01631257696424561, -0.015552188778029734, -0.014643493214701668, -0.01361136568670365, -0.012482935924108854, -0.011286411594113968, -0.010049923940608054, -0.00880046014810808, -0.007562936707760972, -0.006359454317362786, -0.005208759218787376, -0.004125919855569243, -0.0031222127073087685, -0.0022051982768183614, -0.0013789582933809714, -0.0006444587008155979, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q1": {
            "sample": 0.03,
            "type": "constant",
        },
        "x90_I_wf_q2": {
            "samples": [0.0, 0.0007882406922592178, 0.0016866108540323985, 0.0026971891512804734, 0.003818794133239242, 0.005046433416205089, 0.00637085971099852, 0.007778280698460524, 0.009250266089190289, 0.010763887260060829, 0.01229211273596268, 0.013804467030715788, 0.015267941982619701, 0.016648130125177088, 0.01791053051815703, 0.01902196065166925, 0.019951995283104904, 0.020674345860313796, 0.021168093553329027] + [0.021418695287702638] * 2 + [0.021168093553329027, 0.020674345860313796, 0.019951995283104904, 0.01902196065166925, 0.01791053051815703, 0.016648130125177088, 0.015267941982619701, 0.013804467030715788, 0.01229211273596268, 0.010763887260060829, 0.009250266089190289, 0.007778280698460524, 0.00637085971099852, 0.005046433416205089, 0.003818794133239242, 0.0026971891512804734, 0.0016866108540323985, 0.0007882406922592178, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q2": {
            "samples": [0.0003799551396356434, 0.00043589851769465753, 0.0004936563402164494, 0.0005516970689468364, 0.0006081847801517076, 0.000661022167777625, 0.0007079181021233454, 0.0007464789145994111, 0.0007743204159027276, 0.0007891954302346503, 0.0007891295678712929, 0.0007725563028681557, 0.000738441398777516, 0.000686386516023601, 0.0006167025511898322, 0.0005304449185586393, 0.0004294055004955612, 0.00031605917492159293, 0.00019346639626965594, 6.513692195911263e-05, -6.513692195911263e-05, -0.00019346639626965594, -0.00031605917492159293, -0.0004294055004955612, -0.0005304449185586393, -0.0006167025511898322, -0.000686386516023601, -0.000738441398777516, -0.0007725563028681557, -0.0007891295678712929, -0.0007891954302346503, -0.0007743204159027276, -0.0007464789145994111, -0.0007079181021233454, -0.000661022167777625, -0.0006081847801517076, -0.0005516970689468364, -0.0004936563402164494, -0.00043589851769465753, -0.0003799551396356434],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q2": {
            "samples": [0.0, 0.0015760768444548542, 0.00337235610740649, 0.005392994053965991, 0.0076356283889478915, 0.010090276907130893, 0.012738449776040096, 0.015552569435837084, 0.018495784766494085, 0.0215222502891611, 0.024577916926684592, 0.027601849347301578, 0.030528048168025384, 0.033287716114425325, 0.03581186901257599, 0.03803415887258986, 0.03989375082406045, 0.04133808125447058, 0.04232532323982649] + [0.04282639809501372] * 2 + [0.04232532323982649, 0.04133808125447058, 0.03989375082406045, 0.03803415887258986, 0.03581186901257599, 0.033287716114425325, 0.030528048168025384, 0.027601849347301578, 0.024577916926684592, 0.0215222502891611, 0.018495784766494085, 0.015552569435837084, 0.012738449776040096, 0.010090276907130893, 0.0076356283889478915, 0.005392994053965991, 0.00337235610740649, 0.0015760768444548542, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q2": {
            "samples": [0.000759715279091957, 0.0008715733240080147, 0.0009870593266423386, 0.0011031109965010243, 0.0012160574283467086, 0.0013217050864497337, 0.001415472887258803, 0.0014925747220710902, 0.0015482434358915463, 0.001577985830416096, 0.0015778541394911943, 0.0015447161151986492, 0.0014765038154327629, 0.0013724207654774103, 0.001233088598941415, 0.0010606176027310227, 0.0008585906219493171, 0.0006319561422840313, 0.00038683350191778473, 0.00013024041441527076, -0.00013024041441527076, -0.00038683350191778473, -0.0006319561422840313, -0.0008585906219493171, -0.0010606176027310227, -0.001233088598941415, -0.0013724207654774103, -0.0014765038154327629, -0.0015447161151986492, -0.0015778541394911943, -0.001577985830416096, -0.0015482434358915463, -0.0014925747220710902, -0.001415472887258803, -0.0013217050864497337, -0.0012160574283467086, -0.0011031109965010243, -0.0009870593266423386, -0.0008715733240080147, -0.000759715279091957],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q2": {
            "samples": [0.0, -0.0007882406922592178, -0.0016866108540323985, -0.0026971891512804734, -0.003818794133239242, -0.005046433416205089, -0.00637085971099852, -0.007778280698460524, -0.009250266089190289, -0.010763887260060829, -0.01229211273596268, -0.013804467030715788, -0.015267941982619701, -0.016648130125177088, -0.01791053051815703, -0.01902196065166925, -0.019951995283104904, -0.020674345860313796, -0.021168093553329027] + [-0.021418695287702638] * 2 + [-0.021168093553329027, -0.020674345860313796, -0.019951995283104904, -0.01902196065166925, -0.01791053051815703, -0.016648130125177088, -0.015267941982619701, -0.013804467030715788, -0.01229211273596268, -0.010763887260060829, -0.009250266089190289, -0.007778280698460524, -0.00637085971099852, -0.005046433416205089, -0.003818794133239242, -0.0026971891512804734, -0.0016866108540323985, -0.0007882406922592178, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q2": {
            "samples": [-0.0003799551396356434, -0.00043589851769465753, -0.0004936563402164494, -0.0005516970689468364, -0.0006081847801517076, -0.000661022167777625, -0.0007079181021233454, -0.0007464789145994111, -0.0007743204159027276, -0.0007891954302346503, -0.0007891295678712929, -0.0007725563028681557, -0.000738441398777516, -0.000686386516023601, -0.0006167025511898322, -0.0005304449185586393, -0.0004294055004955612, -0.00031605917492159293, -0.00019346639626965594, -6.513692195911263e-05, 6.513692195911263e-05, 0.00019346639626965594, 0.00031605917492159293, 0.0004294055004955612, 0.0005304449185586393, 0.0006167025511898322, 0.000686386516023601, 0.000738441398777516, 0.0007725563028681557, 0.0007891295678712929, 0.0007891954302346503, 0.0007743204159027276, 0.0007464789145994111, 0.0007079181021233454, 0.000661022167777625, 0.0006081847801517076, 0.0005516970689468364, 0.0004936563402164494, 0.00043589851769465753, 0.0003799551396356434],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q2": {
            "samples": [-0.0003799551396356434, -0.00043589851769465753, -0.0004936563402164494, -0.0005516970689468364, -0.0006081847801517076, -0.000661022167777625, -0.0007079181021233454, -0.0007464789145994111, -0.0007743204159027276, -0.0007891954302346503, -0.0007891295678712929, -0.0007725563028681557, -0.000738441398777516, -0.000686386516023601, -0.0006167025511898322, -0.0005304449185586393, -0.0004294055004955612, -0.00031605917492159293, -0.00019346639626965594, -6.513692195911263e-05, 6.513692195911263e-05, 0.00019346639626965594, 0.00031605917492159293, 0.0004294055004955612, 0.0005304449185586393, 0.0006167025511898322, 0.000686386516023601, 0.000738441398777516, 0.0007725563028681557, 0.0007891295678712929, 0.0007891954302346503, 0.0007743204159027276, 0.0007464789145994111, 0.0007079181021233454, 0.000661022167777625, 0.0006081847801517076, 0.0005516970689468364, 0.0004936563402164494, 0.00043589851769465753, 0.0003799551396356434],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q2": {
            "samples": [0.0, 0.0007882406922592178, 0.0016866108540323985, 0.0026971891512804734, 0.003818794133239242, 0.005046433416205089, 0.00637085971099852, 0.007778280698460524, 0.009250266089190289, 0.010763887260060829, 0.01229211273596268, 0.013804467030715788, 0.015267941982619701, 0.016648130125177088, 0.01791053051815703, 0.01902196065166925, 0.019951995283104904, 0.020674345860313796, 0.021168093553329027] + [0.021418695287702638] * 2 + [0.021168093553329027, 0.020674345860313796, 0.019951995283104904, 0.01902196065166925, 0.01791053051815703, 0.016648130125177088, 0.015267941982619701, 0.013804467030715788, 0.01229211273596268, 0.010763887260060829, 0.009250266089190289, 0.007778280698460524, 0.00637085971099852, 0.005046433416205089, 0.003818794133239242, 0.0026971891512804734, 0.0016866108540323985, 0.0007882406922592178, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q2": {
            "samples": [-0.000759715279091957, -0.0008715733240080147, -0.0009870593266423386, -0.0011031109965010243, -0.0012160574283467086, -0.0013217050864497337, -0.001415472887258803, -0.0014925747220710902, -0.0015482434358915463, -0.001577985830416096, -0.0015778541394911943, -0.0015447161151986492, -0.0014765038154327629, -0.0013724207654774103, -0.001233088598941415, -0.0010606176027310227, -0.0008585906219493171, -0.0006319561422840313, -0.00038683350191778473, -0.00013024041441527076, 0.00013024041441527076, 0.00038683350191778473, 0.0006319561422840313, 0.0008585906219493171, 0.0010606176027310227, 0.001233088598941415, 0.0013724207654774103, 0.0014765038154327629, 0.0015447161151986492, 0.0015778541394911943, 0.001577985830416096, 0.0015482434358915463, 0.0014925747220710902, 0.001415472887258803, 0.0013217050864497337, 0.0012160574283467086, 0.0011031109965010243, 0.0009870593266423386, 0.0008715733240080147, 0.000759715279091957],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q2": {
            "samples": [0.0, 0.0015760768444548542, 0.00337235610740649, 0.005392994053965991, 0.0076356283889478915, 0.010090276907130893, 0.012738449776040096, 0.015552569435837084, 0.018495784766494085, 0.0215222502891611, 0.024577916926684592, 0.027601849347301578, 0.030528048168025384, 0.033287716114425325, 0.03581186901257599, 0.03803415887258986, 0.03989375082406045, 0.04133808125447058, 0.04232532323982649] + [0.04282639809501372] * 2 + [0.04232532323982649, 0.04133808125447058, 0.03989375082406045, 0.03803415887258986, 0.03581186901257599, 0.033287716114425325, 0.030528048168025384, 0.027601849347301578, 0.024577916926684592, 0.0215222502891611, 0.018495784766494085, 0.015552569435837084, 0.012738449776040096, 0.010090276907130893, 0.0076356283889478915, 0.005392994053965991, 0.00337235610740649, 0.0015760768444548542, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q2": {
            "samples": [0.0003799551396356434, 0.00043589851769465753, 0.0004936563402164494, 0.0005516970689468364, 0.0006081847801517076, 0.000661022167777625, 0.0007079181021233454, 0.0007464789145994111, 0.0007743204159027276, 0.0007891954302346503, 0.0007891295678712929, 0.0007725563028681557, 0.000738441398777516, 0.000686386516023601, 0.0006167025511898322, 0.0005304449185586393, 0.0004294055004955612, 0.00031605917492159293, 0.00019346639626965594, 6.513692195911263e-05, -6.513692195911263e-05, -0.00019346639626965594, -0.00031605917492159293, -0.0004294055004955612, -0.0005304449185586393, -0.0006167025511898322, -0.000686386516023601, -0.000738441398777516, -0.0007725563028681557, -0.0007891295678712929, -0.0007891954302346503, -0.0007743204159027276, -0.0007464789145994111, -0.0007079181021233454, -0.000661022167777625, -0.0006081847801517076, -0.0005516970689468364, -0.0004936563402164494, -0.00043589851769465753, -0.0003799551396356434],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q2": {
            "samples": [0.0, -0.0007882406922592178, -0.0016866108540323985, -0.0026971891512804734, -0.003818794133239242, -0.005046433416205089, -0.00637085971099852, -0.007778280698460524, -0.009250266089190289, -0.010763887260060829, -0.01229211273596268, -0.013804467030715788, -0.015267941982619701, -0.016648130125177088, -0.01791053051815703, -0.01902196065166925, -0.019951995283104904, -0.020674345860313796, -0.021168093553329027] + [-0.021418695287702638] * 2 + [-0.021168093553329027, -0.020674345860313796, -0.019951995283104904, -0.01902196065166925, -0.01791053051815703, -0.016648130125177088, -0.015267941982619701, -0.013804467030715788, -0.01229211273596268, -0.010763887260060829, -0.009250266089190289, -0.007778280698460524, -0.00637085971099852, -0.005046433416205089, -0.003818794133239242, -0.0026971891512804734, -0.0016866108540323985, -0.0007882406922592178, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q2": {
            "sample": 0.020999999999999998,
            "type": "constant",
        },
        "x90_I_wf_q3": {
            "samples": [0.0, 0.0012082000004049066, 0.002585204309465838, 0.004134199065933938, 0.0058533733650591715, 0.0077350749782114205, 0.009765129840412657, 0.011922397353141202, 0.014178627927305551, 0.016498677015379354, 0.018841111298125324, 0.02115921854312933, 0.023402404482204656, 0.025517930019990902, 0.027452912786407043, 0.029156491275752396, 0.03058203026798145, 0.03168923518171769, 0.0324460420412965] + [0.03283015950509282] * 2 + [0.0324460420412965, 0.03168923518171769, 0.03058203026798145, 0.029156491275752396, 0.027452912786407043, 0.025517930019990902, 0.023402404482204656, 0.02115921854312933, 0.018841111298125324, 0.016498677015379354, 0.014178627927305551, 0.011922397353141202, 0.009765129840412657, 0.0077350749782114205, 0.0058533733650591715, 0.004134199065933938, 0.002585204309465838, 0.0012082000004049066, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q3": {
            "samples": [-0.000627186912398396, -0.0007195319049878259, -0.0008148719770001034, -0.0009106790385407691, -0.0010039225546385098, -0.0010911405299923232, -0.0011685510271750572, -0.0012322028491760157, -0.001278160446316846, -0.001302714435294774, -0.0013026057171646364, -0.0012752484483153563, -0.001218935428352279, -0.0011330091234179746, -0.0010179827263815232, -0.000875598395608602, -0.0007088139675672238, -0.000521714690435162, -0.0003193524157761579, -0.00010752065363781363, 0.00010752065363781363, 0.0003193524157761579, 0.000521714690435162, 0.0007088139675672238, 0.000875598395608602, 0.0010179827263815232, 0.0011330091234179746, 0.001218935428352279, 0.0012752484483153563, 0.0013026057171646364, 0.001302714435294774, 0.001278160446316846, 0.0012322028491760157, 0.0011685510271750572, 0.0010911405299923232, 0.0010039225546385098, 0.0009106790385407691, 0.0008148719770001034, 0.0007195319049878259, 0.000627186912398396],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q3": {
            "samples": [0.0, 0.002391291440682645, 0.005116683442782459, 0.008182482070131494, 0.011585103147074066, 0.015309401243367481, 0.01932732279151441, 0.023597025933975654, 0.028062598569629983, 0.03265448197007294, 0.037290670555418744, 0.04187871062469931, 0.0463184650810582, 0.050505551746642056, 0.05433530487166164, 0.057707058437906765, 0.06052851116869163, 0.06271991129483957, 0.06421779721186839] + [0.06497804949053503] * 2 + [0.06421779721186839, 0.06271991129483957, 0.06052851116869163, 0.057707058437906765, 0.05433530487166164, 0.050505551746642056, 0.0463184650810582, 0.04187871062469931, 0.037290670555418744, 0.03265448197007294, 0.028062598569629983, 0.023597025933975654, 0.01932732279151441, 0.015309401243367481, 0.011585103147074066, 0.008182482070131494, 0.005116683442782459, 0.002391291440682645, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q3": {
            "samples": [-0.001241339757344673, -0.0014241106481698684, -0.0016128094547255881, -0.0018024325354592163, -0.001986981800373102, -0.0021596052053286952, -0.0023128174709056057, -0.0024387983160336774, -0.00252975842912785, -0.002578356131211824, -0.0025781409543090277, -0.00252399494965929, -0.0024125391951554265, -0.0022424722878139035, -0.002014809948305835, -0.0017330002881911963, -0.001402897511266153, -0.0010325872151116518, -0.0006320681163308418, -0.0002128068355028474, 0.0002128068355028474, 0.0006320681163308418, 0.0010325872151116518, 0.001402897511266153, 0.0017330002881911963, 0.002014809948305835, 0.0022424722878139035, 0.0024125391951554265, 0.00252399494965929, 0.0025781409543090277, 0.002578356131211824, 0.00252975842912785, 0.0024387983160336774, 0.0023128174709056057, 0.0021596052053286952, 0.001986981800373102, 0.0018024325354592163, 0.0016128094547255881, 0.0014241106481698684, 0.001241339757344673],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q3": {
            "samples": [0.0, -0.0012082000004049066, -0.002585204309465838, -0.004134199065933938, -0.0058533733650591715, -0.0077350749782114205, -0.009765129840412657, -0.011922397353141202, -0.014178627927305551, -0.016498677015379354, -0.018841111298125324, -0.02115921854312933, -0.023402404482204656, -0.025517930019990902, -0.027452912786407043, -0.029156491275752396, -0.03058203026798145, -0.03168923518171769, -0.0324460420412965] + [-0.03283015950509282] * 2 + [-0.0324460420412965, -0.03168923518171769, -0.03058203026798145, -0.029156491275752396, -0.027452912786407043, -0.025517930019990902, -0.023402404482204656, -0.02115921854312933, -0.018841111298125324, -0.016498677015379354, -0.014178627927305551, -0.011922397353141202, -0.009765129840412657, -0.0077350749782114205, -0.0058533733650591715, -0.004134199065933938, -0.002585204309465838, -0.0012082000004049066, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q3": {
            "samples": [0.000627186912398396, 0.0007195319049878259, 0.0008148719770001034, 0.0009106790385407691, 0.0010039225546385098, 0.0010911405299923232, 0.0011685510271750572, 0.0012322028491760157, 0.001278160446316846, 0.001302714435294774, 0.0013026057171646364, 0.0012752484483153563, 0.001218935428352279, 0.0011330091234179746, 0.0010179827263815232, 0.000875598395608602, 0.0007088139675672238, 0.000521714690435162, 0.0003193524157761579, 0.00010752065363781363, -0.00010752065363781363, -0.0003193524157761579, -0.000521714690435162, -0.0007088139675672238, -0.000875598395608602, -0.0010179827263815232, -0.0011330091234179746, -0.001218935428352279, -0.0012752484483153563, -0.0013026057171646364, -0.001302714435294774, -0.001278160446316846, -0.0012322028491760157, -0.0011685510271750572, -0.0010911405299923232, -0.0010039225546385098, -0.0009106790385407691, -0.0008148719770001034, -0.0007195319049878259, -0.000627186912398396],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q3": {
            "samples": [0.000627186912398396, 0.0007195319049878259, 0.0008148719770001034, 0.0009106790385407691, 0.0010039225546385098, 0.0010911405299923232, 0.0011685510271750572, 0.0012322028491760157, 0.001278160446316846, 0.001302714435294774, 0.0013026057171646364, 0.0012752484483153563, 0.001218935428352279, 0.0011330091234179746, 0.0010179827263815232, 0.000875598395608602, 0.0007088139675672238, 0.000521714690435162, 0.0003193524157761579, 0.00010752065363781363, -0.00010752065363781363, -0.0003193524157761579, -0.000521714690435162, -0.0007088139675672238, -0.000875598395608602, -0.0010179827263815232, -0.0011330091234179746, -0.001218935428352279, -0.0012752484483153563, -0.0013026057171646364, -0.001302714435294774, -0.001278160446316846, -0.0012322028491760157, -0.0011685510271750572, -0.0010911405299923232, -0.0010039225546385098, -0.0009106790385407691, -0.0008148719770001034, -0.0007195319049878259, -0.000627186912398396],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q3": {
            "samples": [0.0, 0.0012082000004049066, 0.002585204309465838, 0.004134199065933938, 0.0058533733650591715, 0.0077350749782114205, 0.009765129840412657, 0.011922397353141202, 0.014178627927305551, 0.016498677015379354, 0.018841111298125324, 0.02115921854312933, 0.023402404482204656, 0.025517930019990902, 0.027452912786407043, 0.029156491275752396, 0.03058203026798145, 0.03168923518171769, 0.0324460420412965] + [0.03283015950509282] * 2 + [0.0324460420412965, 0.03168923518171769, 0.03058203026798145, 0.029156491275752396, 0.027452912786407043, 0.025517930019990902, 0.023402404482204656, 0.02115921854312933, 0.018841111298125324, 0.016498677015379354, 0.014178627927305551, 0.011922397353141202, 0.009765129840412657, 0.0077350749782114205, 0.0058533733650591715, 0.004134199065933938, 0.002585204309465838, 0.0012082000004049066, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q3": {
            "samples": [0.001241339757344673, 0.0014241106481698684, 0.0016128094547255881, 0.0018024325354592163, 0.001986981800373102, 0.0021596052053286952, 0.0023128174709056057, 0.0024387983160336774, 0.00252975842912785, 0.002578356131211824, 0.0025781409543090277, 0.00252399494965929, 0.0024125391951554265, 0.0022424722878139035, 0.002014809948305835, 0.0017330002881911963, 0.001402897511266153, 0.0010325872151116518, 0.0006320681163308418, 0.0002128068355028474, -0.0002128068355028474, -0.0006320681163308418, -0.0010325872151116518, -0.001402897511266153, -0.0017330002881911963, -0.002014809948305835, -0.0022424722878139035, -0.0024125391951554265, -0.00252399494965929, -0.0025781409543090277, -0.002578356131211824, -0.00252975842912785, -0.0024387983160336774, -0.0023128174709056057, -0.0021596052053286952, -0.001986981800373102, -0.0018024325354592163, -0.0016128094547255881, -0.0014241106481698684, -0.001241339757344673],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q3": {
            "samples": [0.0, 0.002391291440682645, 0.005116683442782459, 0.008182482070131494, 0.011585103147074066, 0.015309401243367481, 0.01932732279151441, 0.023597025933975654, 0.028062598569629983, 0.03265448197007294, 0.037290670555418744, 0.04187871062469931, 0.0463184650810582, 0.050505551746642056, 0.05433530487166164, 0.057707058437906765, 0.06052851116869163, 0.06271991129483957, 0.06421779721186839] + [0.06497804949053503] * 2 + [0.06421779721186839, 0.06271991129483957, 0.06052851116869163, 0.057707058437906765, 0.05433530487166164, 0.050505551746642056, 0.0463184650810582, 0.04187871062469931, 0.037290670555418744, 0.03265448197007294, 0.028062598569629983, 0.023597025933975654, 0.01932732279151441, 0.015309401243367481, 0.011585103147074066, 0.008182482070131494, 0.005116683442782459, 0.002391291440682645, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q3": {
            "samples": [-0.000627186912398396, -0.0007195319049878259, -0.0008148719770001034, -0.0009106790385407691, -0.0010039225546385098, -0.0010911405299923232, -0.0011685510271750572, -0.0012322028491760157, -0.001278160446316846, -0.001302714435294774, -0.0013026057171646364, -0.0012752484483153563, -0.001218935428352279, -0.0011330091234179746, -0.0010179827263815232, -0.000875598395608602, -0.0007088139675672238, -0.000521714690435162, -0.0003193524157761579, -0.00010752065363781363, 0.00010752065363781363, 0.0003193524157761579, 0.000521714690435162, 0.0007088139675672238, 0.000875598395608602, 0.0010179827263815232, 0.0011330091234179746, 0.001218935428352279, 0.0012752484483153563, 0.0013026057171646364, 0.001302714435294774, 0.001278160446316846, 0.0012322028491760157, 0.0011685510271750572, 0.0010911405299923232, 0.0010039225546385098, 0.0009106790385407691, 0.0008148719770001034, 0.0007195319049878259, 0.000627186912398396],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q3": {
            "samples": [0.0, -0.0012082000004049066, -0.002585204309465838, -0.004134199065933938, -0.0058533733650591715, -0.0077350749782114205, -0.009765129840412657, -0.011922397353141202, -0.014178627927305551, -0.016498677015379354, -0.018841111298125324, -0.02115921854312933, -0.023402404482204656, -0.025517930019990902, -0.027452912786407043, -0.029156491275752396, -0.03058203026798145, -0.03168923518171769, -0.0324460420412965] + [-0.03283015950509282] * 2 + [-0.0324460420412965, -0.03168923518171769, -0.03058203026798145, -0.029156491275752396, -0.027452912786407043, -0.025517930019990902, -0.023402404482204656, -0.02115921854312933, -0.018841111298125324, -0.016498677015379354, -0.014178627927305551, -0.011922397353141202, -0.009765129840412657, -0.0077350749782114205, -0.0058533733650591715, -0.004134199065933938, -0.002585204309465838, -0.0012082000004049066, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q3": {
            "sample": 0.0135,
            "type": "constant",
        },
        "x90_I_wf_q4": {
            "samples": [0.0, 0.0026246360206212457, 0.00561597446533303, 0.00898093674990273, 0.012715588951275178, 0.01680330773317002, 0.021213302033273505, 0.02589964702427318, 0.030800974647012896, 0.035840938563688335, 0.0409295310089563, 0.04596527655841962, 0.05083826663843542, 0.05543393335516866, 0.05963739757161887, 0.0633381701801215, 0.06643494305427361, 0.06884018216851553, 0.07048423327233783] + [0.07131867171902846] * 2 + [0.07048423327233783, 0.06884018216851553, 0.06643494305427361, 0.0633381701801215, 0.05963739757161887, 0.05543393335516866, 0.05083826663843542, 0.04596527655841962, 0.0409295310089563, 0.035840938563688335, 0.030800974647012896, 0.02589964702427318, 0.021213302033273505, 0.01680330773317002, 0.012715588951275178, 0.00898093674990273, 0.00561597446533303, 0.0026246360206212457, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q4": {
            "samples": [-0.0019861092078177385, -0.0022785375676130162, -0.0025804504282839827, -0.002883842102023192, -0.0031791158110724476, -0.003455308474715587, -0.0037004438533357266, -0.003902009713960981, -0.004047543373937295, -0.004125298350378418, -0.004124954073297606, -0.004038321966523372, -0.0038599958483315957, -0.00358789351001722, -0.003223640076503164, -0.0027727524307204128, -0.0022445971364926194, -0.0016521109258556435, -0.001011291468258463, -0.000340485038828418, 0.000340485038828418, 0.001011291468258463, 0.0016521109258556435, 0.0022445971364926194, 0.0027727524307204128, 0.003223640076503164, 0.00358789351001722, 0.0038599958483315957, 0.004038321966523372, 0.004124954073297606, 0.004125298350378418, 0.004047543373937295, 0.003902009713960981, 0.0037004438533357266, 0.003455308474715587, 0.0031791158110724476, 0.002883842102023192, 0.0025804504282839827, 0.0022785375676130162, 0.0019861092078177385],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q4": {
            "samples": [0.0, 0.004802803434016331, 0.010276633116185457, 0.016434154497699333, 0.023268168919768663, 0.030748257453465856, 0.038818075745266994, 0.047393586268981804, 0.056362492034498786, 0.06558508740244534, 0.0748966677809916, 0.08411154398773901, 0.09302859507838426, 0.1014381740505941, 0.1091300643603039, 0.11590208274798985, 0.12156884616870442, 0.12597017671006355, 0.12897861453728923] + [0.13050554772183512] * 2 + [0.12897861453728923, 0.12597017671006355, 0.12156884616870442, 0.11590208274798985, 0.1091300643603039, 0.1014381740505941, 0.09302859507838426, 0.08411154398773901, 0.0748966677809916, 0.06558508740244534, 0.056362492034498786, 0.047393586268981804, 0.038818075745266994, 0.030748257453465856, 0.023268168919768663, 0.016434154497699333, 0.010276633116185457, 0.004802803434016331, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q4": {
            "samples": [-0.003634367603238432, -0.004169480251085156, -0.004721948521966005, -0.005277122862727259, -0.005817442195638354, -0.006322845254566657, -0.00677141680086321, -0.007140260785318733, -0.007406571830510348, -0.007548855128053024, -0.0075482251377865725, -0.0073896976403955705, -0.007063379901060598, -0.006565461700368211, -0.0058989168432571435, -0.0050738406359252175, -0.004107372889204763, -0.0030231864402277178, -0.0018505553144826212, -0.000623051234863889, 0.000623051234863889, 0.0018505553144826212, 0.0030231864402277178, 0.004107372889204763, 0.0050738406359252175, 0.0058989168432571435, 0.006565461700368211, 0.007063379901060598, 0.0073896976403955705, 0.0075482251377865725, 0.007548855128053024, 0.007406571830510348, 0.007140260785318733, 0.00677141680086321, 0.006322845254566657, 0.005817442195638354, 0.005277122862727259, 0.004721948521966005, 0.004169480251085156, 0.003634367603238432],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q4": {
            "samples": [0.0, -0.0026246360206212457, -0.00561597446533303, -0.00898093674990273, -0.012715588951275178, -0.01680330773317002, -0.021213302033273505, -0.02589964702427318, -0.030800974647012896, -0.035840938563688335, -0.0409295310089563, -0.04596527655841962, -0.05083826663843542, -0.05543393335516866, -0.05963739757161887, -0.0633381701801215, -0.06643494305427361, -0.06884018216851553, -0.07048423327233783] + [-0.07131867171902846] * 2 + [-0.07048423327233783, -0.06884018216851553, -0.06643494305427361, -0.0633381701801215, -0.05963739757161887, -0.05543393335516866, -0.05083826663843542, -0.04596527655841962, -0.0409295310089563, -0.035840938563688335, -0.030800974647012896, -0.02589964702427318, -0.021213302033273505, -0.01680330773317002, -0.012715588951275178, -0.00898093674990273, -0.00561597446533303, -0.0026246360206212457, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q4": {
            "samples": [0.0019861092078177385, 0.0022785375676130162, 0.0025804504282839827, 0.002883842102023192, 0.0031791158110724476, 0.003455308474715587, 0.0037004438533357266, 0.003902009713960981, 0.004047543373937295, 0.004125298350378418, 0.004124954073297606, 0.004038321966523372, 0.0038599958483315957, 0.00358789351001722, 0.003223640076503164, 0.0027727524307204128, 0.0022445971364926194, 0.0016521109258556435, 0.001011291468258463, 0.000340485038828418, -0.000340485038828418, -0.001011291468258463, -0.0016521109258556435, -0.0022445971364926194, -0.0027727524307204128, -0.003223640076503164, -0.00358789351001722, -0.0038599958483315957, -0.004038321966523372, -0.004124954073297606, -0.004125298350378418, -0.004047543373937295, -0.003902009713960981, -0.0037004438533357266, -0.003455308474715587, -0.0031791158110724476, -0.002883842102023192, -0.0025804504282839827, -0.0022785375676130162, -0.0019861092078177385],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q4": {
            "samples": [0.0019861092078177385, 0.0022785375676130162, 0.0025804504282839827, 0.002883842102023192, 0.0031791158110724476, 0.003455308474715587, 0.0037004438533357266, 0.003902009713960981, 0.004047543373937295, 0.004125298350378418, 0.004124954073297606, 0.004038321966523372, 0.0038599958483315957, 0.00358789351001722, 0.003223640076503164, 0.0027727524307204128, 0.0022445971364926194, 0.0016521109258556435, 0.001011291468258463, 0.000340485038828418, -0.000340485038828418, -0.001011291468258463, -0.0016521109258556435, -0.0022445971364926194, -0.0027727524307204128, -0.003223640076503164, -0.00358789351001722, -0.0038599958483315957, -0.004038321966523372, -0.004124954073297606, -0.004125298350378418, -0.004047543373937295, -0.003902009713960981, -0.0037004438533357266, -0.003455308474715587, -0.0031791158110724476, -0.002883842102023192, -0.0025804504282839827, -0.0022785375676130162, -0.0019861092078177385],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q4": {
            "samples": [0.0, 0.0026246360206212457, 0.00561597446533303, 0.00898093674990273, 0.012715588951275178, 0.01680330773317002, 0.021213302033273505, 0.02589964702427318, 0.030800974647012896, 0.035840938563688335, 0.0409295310089563, 0.04596527655841962, 0.05083826663843542, 0.05543393335516866, 0.05963739757161887, 0.0633381701801215, 0.06643494305427361, 0.06884018216851553, 0.07048423327233783] + [0.07131867171902846] * 2 + [0.07048423327233783, 0.06884018216851553, 0.06643494305427361, 0.0633381701801215, 0.05963739757161887, 0.05543393335516866, 0.05083826663843542, 0.04596527655841962, 0.0409295310089563, 0.035840938563688335, 0.030800974647012896, 0.02589964702427318, 0.021213302033273505, 0.01680330773317002, 0.012715588951275178, 0.00898093674990273, 0.00561597446533303, 0.0026246360206212457, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q4": {
            "samples": [0.003634367603238432, 0.004169480251085156, 0.004721948521966005, 0.005277122862727259, 0.005817442195638354, 0.006322845254566657, 0.00677141680086321, 0.007140260785318733, 0.007406571830510348, 0.007548855128053024, 0.0075482251377865725, 0.0073896976403955705, 0.007063379901060598, 0.006565461700368211, 0.0058989168432571435, 0.0050738406359252175, 0.004107372889204763, 0.0030231864402277178, 0.0018505553144826212, 0.000623051234863889, -0.000623051234863889, -0.0018505553144826212, -0.0030231864402277178, -0.004107372889204763, -0.0050738406359252175, -0.0058989168432571435, -0.006565461700368211, -0.007063379901060598, -0.0073896976403955705, -0.0075482251377865725, -0.007548855128053024, -0.007406571830510348, -0.007140260785318733, -0.00677141680086321, -0.006322845254566657, -0.005817442195638354, -0.005277122862727259, -0.004721948521966005, -0.004169480251085156, -0.003634367603238432],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q4": {
            "samples": [0.0, 0.004802803434016331, 0.010276633116185457, 0.016434154497699333, 0.023268168919768663, 0.030748257453465856, 0.038818075745266994, 0.047393586268981804, 0.056362492034498786, 0.06558508740244534, 0.0748966677809916, 0.08411154398773901, 0.09302859507838426, 0.1014381740505941, 0.1091300643603039, 0.11590208274798985, 0.12156884616870442, 0.12597017671006355, 0.12897861453728923] + [0.13050554772183512] * 2 + [0.12897861453728923, 0.12597017671006355, 0.12156884616870442, 0.11590208274798985, 0.1091300643603039, 0.1014381740505941, 0.09302859507838426, 0.08411154398773901, 0.0748966677809916, 0.06558508740244534, 0.056362492034498786, 0.047393586268981804, 0.038818075745266994, 0.030748257453465856, 0.023268168919768663, 0.016434154497699333, 0.010276633116185457, 0.004802803434016331, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q4": {
            "samples": [-0.0019861092078177385, -0.0022785375676130162, -0.0025804504282839827, -0.002883842102023192, -0.0031791158110724476, -0.003455308474715587, -0.0037004438533357266, -0.003902009713960981, -0.004047543373937295, -0.004125298350378418, -0.004124954073297606, -0.004038321966523372, -0.0038599958483315957, -0.00358789351001722, -0.003223640076503164, -0.0027727524307204128, -0.0022445971364926194, -0.0016521109258556435, -0.001011291468258463, -0.000340485038828418, 0.000340485038828418, 0.001011291468258463, 0.0016521109258556435, 0.0022445971364926194, 0.0027727524307204128, 0.003223640076503164, 0.00358789351001722, 0.0038599958483315957, 0.004038321966523372, 0.004124954073297606, 0.004125298350378418, 0.004047543373937295, 0.003902009713960981, 0.0037004438533357266, 0.003455308474715587, 0.0031791158110724476, 0.002883842102023192, 0.0025804504282839827, 0.0022785375676130162, 0.0019861092078177385],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q4": {
            "samples": [0.0, -0.0026246360206212457, -0.00561597446533303, -0.00898093674990273, -0.012715588951275178, -0.01680330773317002, -0.021213302033273505, -0.02589964702427318, -0.030800974647012896, -0.035840938563688335, -0.0409295310089563, -0.04596527655841962, -0.05083826663843542, -0.05543393335516866, -0.05963739757161887, -0.0633381701801215, -0.06643494305427361, -0.06884018216851553, -0.07048423327233783] + [-0.07131867171902846] * 2 + [-0.07048423327233783, -0.06884018216851553, -0.06643494305427361, -0.0633381701801215, -0.05963739757161887, -0.05543393335516866, -0.05083826663843542, -0.04596527655841962, -0.0409295310089563, -0.035840938563688335, -0.030800974647012896, -0.02589964702427318, -0.021213302033273505, -0.01680330773317002, -0.012715588951275178, -0.00898093674990273, -0.00561597446533303, -0.0026246360206212457, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q4": {
            "sample": 0.03,
            "type": "constant",
        },
        "x90_I_wf_q5": {
            "samples": [0.0, 0.007814519092118992, 0.016720847894867323, 0.026739594041163897, 0.03785904477671438, 0.05002970623733462, 0.06315990196105921, 0.07711289663029906, 0.09170597467376958, 0.10671182460534549, 0.12186245978033129, 0.1368557500614042, 0.15136445668464732, 0.16504746835436723, 0.17756274708803105, 0.18858132565569452, 0.19780157202848103, 0.20496286480648152, 0.20985781734020376] + [0.21234225141854074] * 2 + [0.20985781734020376, 0.20496286480648152, 0.19780157202848103, 0.18858132565569452, 0.17756274708803105, 0.16504746835436723, 0.15136445668464732, 0.1368557500614042, 0.12186245978033129, 0.10671182460534549, 0.09170597467376958, 0.07711289663029906, 0.06315990196105921, 0.05002970623733462, 0.03785904477671438, 0.026739594041163897, 0.016720847894867323, 0.007814519092118992, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q5": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q5": {
            "samples": [0.0, 0.015629038184237984, 0.033441695789734646, 0.053479188082327794, 0.07571808955342876, 0.10005941247466923, 0.12631980392211842, 0.15422579326059813, 0.18341194934753915, 0.21342364921069099, 0.24372491956066258, 0.2737115001228084, 0.30272891336929464, 0.33009493670873447, 0.3551254941760621, 0.37716265131138904, 0.39560314405696206, 0.40992572961296303, 0.4197156346804075] + [0.4246845028370815] * 2 + [0.4197156346804075, 0.40992572961296303, 0.39560314405696206, 0.37716265131138904, 0.3551254941760621, 0.33009493670873447, 0.30272891336929464, 0.2737115001228084, 0.24372491956066258, 0.21342364921069099, 0.18341194934753915, 0.15422579326059813, 0.12631980392211842, 0.10005941247466923, 0.07571808955342876, 0.053479188082327794, 0.033441695789734646, 0.015629038184237984, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q5": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q5": {
            "samples": [0.0, -0.007814519092118992, -0.016720847894867323, -0.026739594041163897, -0.03785904477671438, -0.05002970623733462, -0.06315990196105921, -0.07711289663029906, -0.09170597467376958, -0.10671182460534549, -0.12186245978033129, -0.1368557500614042, -0.15136445668464732, -0.16504746835436723, -0.17756274708803105, -0.18858132565569452, -0.19780157202848103, -0.20496286480648152, -0.20985781734020376] + [-0.21234225141854074] * 2 + [-0.20985781734020376, -0.20496286480648152, -0.19780157202848103, -0.18858132565569452, -0.17756274708803105, -0.16504746835436723, -0.15136445668464732, -0.1368557500614042, -0.12186245978033129, -0.10671182460534549, -0.09170597467376958, -0.07711289663029906, -0.06315990196105921, -0.05002970623733462, -0.03785904477671438, -0.026739594041163897, -0.016720847894867323, -0.007814519092118992, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q5": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q5": {
            "samples": [-0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q5": {
            "samples": [0.0, 0.007814519092118992, 0.016720847894867323, 0.026739594041163897, 0.03785904477671438, 0.05002970623733462, 0.06315990196105921, 0.07711289663029906, 0.09170597467376958, 0.10671182460534549, 0.12186245978033129, 0.1368557500614042, 0.15136445668464732, 0.16504746835436723, 0.17756274708803105, 0.18858132565569452, 0.19780157202848103, 0.20496286480648152, 0.20985781734020376] + [0.21234225141854074] * 2 + [0.20985781734020376, 0.20496286480648152, 0.19780157202848103, 0.18858132565569452, 0.17756274708803105, 0.16504746835436723, 0.15136445668464732, 0.1368557500614042, 0.12186245978033129, 0.10671182460534549, 0.09170597467376958, 0.07711289663029906, 0.06315990196105921, 0.05002970623733462, 0.03785904477671438, 0.026739594041163897, 0.016720847894867323, 0.007814519092118992, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q5": {
            "samples": [-0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q5": {
            "samples": [0.0, 0.015629038184237984, 0.033441695789734646, 0.053479188082327794, 0.07571808955342876, 0.10005941247466923, 0.12631980392211842, 0.15422579326059813, 0.18341194934753915, 0.21342364921069099, 0.24372491956066258, 0.2737115001228084, 0.30272891336929464, 0.33009493670873447, 0.3551254941760621, 0.37716265131138904, 0.39560314405696206, 0.40992572961296303, 0.4197156346804075] + [0.4246845028370815] * 2 + [0.4197156346804075, 0.40992572961296303, 0.39560314405696206, 0.37716265131138904, 0.3551254941760621, 0.33009493670873447, 0.30272891336929464, 0.2737115001228084, 0.24372491956066258, 0.21342364921069099, 0.18341194934753915, 0.15422579326059813, 0.12631980392211842, 0.10005941247466923, 0.07571808955342876, 0.053479188082327794, 0.033441695789734646, 0.015629038184237984, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q5": {
            "samples": [-0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q5": {
            "samples": [0.0, -0.007814519092118992, -0.016720847894867323, -0.026739594041163897, -0.03785904477671438, -0.05002970623733462, -0.06315990196105921, -0.07711289663029906, -0.09170597467376958, -0.10671182460534549, -0.12186245978033129, -0.1368557500614042, -0.15136445668464732, -0.16504746835436723, -0.17756274708803105, -0.18858132565569452, -0.19780157202848103, -0.20496286480648152, -0.20985781734020376] + [-0.21234225141854074] * 2 + [-0.20985781734020376, -0.20496286480648152, -0.19780157202848103, -0.18858132565569452, -0.17756274708803105, -0.16504746835436723, -0.15136445668464732, -0.1368557500614042, -0.12186245978033129, -0.10671182460534549, -0.09170597467376958, -0.07711289663029906, -0.06315990196105921, -0.05002970623733462, -0.03785904477671438, -0.026739594041163897, -0.016720847894867323, -0.007814519092118992, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q5": {
            "sample": 0.02,
            "type": "constant",
        },
        "gft_cz_wf_1_2_q2": {
            "samples": [8.2642507797802e-06, 0.0001272704153343253, 0.0013261881815880992, 0.009350537220869926, 0.04460891818882727, 0.1439993518360818, 0.3145235010372933, 0.464835601738604] + [0.48809590999999997] * 8 + [0.464835601738604, 0.3145235010372933, 0.1439993518360818, 0.04460891818882727, 0.009350537220869926, 0.0013261881815880992, 0.0001272704153343253, 8.2642507797802e-06],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "g_cz_wf_1_2_q2": {
            "samples": [0.07266709339002213, 0.1125489959561424, 0.16375782284008586, 0.22383040542184623, 0.2874039295891722, 0.3466753136729172, 0.3928345954049229] + [0.41817025007977965] * 2 + [0.3928345954049229, 0.3466753136729172, 0.2874039295891722, 0.22383040542184623, 0.16375782284008586, 0.1125489959561424, 0.07266709339002213],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_0": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_0": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_0": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_0": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_0": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_1": {
            "samples": [0.0, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271, -0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_1": {
            "samples": [-0.0003798576395459785, -0.00043578666200400735, -0.0004935296633211693, -0.0005515554982505122, -0.0006080287141733543, -0.0006608525432248669, -0.0007077364436294015, -0.0007462873610355451, -0.0007741217179457732, -0.000788992915208048, -0.0007889270697455971, -0.0007723580575993246, -0.0007382519077163814, -0.0006862103827387051, -0.0006165442994707075, -0.0005303088013655113, -0.00042929531097465857, -0.00031597807114201563, -0.00019341675095889237, -6.512020720763538e-05, 6.512020720763538e-05, 0.00019341675095889237, 0.00031597807114201563, 0.00042929531097465857, 0.0005303088013655113, 0.0006165442994707075, 0.0006862103827387051, 0.0007382519077163814, 0.0007723580575993246, 0.0007889270697455971, 0.000788992915208048, 0.0007741217179457732, 0.0007462873610355451, 0.0007077364436294015, 0.0006608525432248669, 0.0006080287141733543, 0.0005515554982505122, 0.0004935296633211693, 0.00043578666200400735, 0.0003798576395459785],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_1": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_1": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_1": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_2": {
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_2": {
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_2": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_2": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_2": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_3": {
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_3": {
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_3": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_3": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_3": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_4": {
            "samples": [0.0, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_4": {
            "samples": [0.0003798576395459785, 0.00043578666200400735, 0.0004935296633211693, 0.0005515554982505122, 0.0006080287141733543, 0.0006608525432248669, 0.0007077364436294015, 0.0007462873610355451, 0.0007741217179457732, 0.000788992915208048, 0.0007889270697455971, 0.0007723580575993246, 0.0007382519077163814, 0.0006862103827387051, 0.0006165442994707075, 0.0005303088013655113, 0.00042929531097465857, 0.00031597807114201563, 0.00019341675095889237, 6.512020720763538e-05, -6.512020720763538e-05, -0.00019341675095889237, -0.00031597807114201563, -0.00042929531097465857, -0.0005303088013655113, -0.0006165442994707075, -0.0006862103827387051, -0.0007382519077163814, -0.0007723580575993246, -0.0007889270697455971, -0.000788992915208048, -0.0007741217179457732, -0.0007462873610355451, -0.0007077364436294015, -0.0006608525432248669, -0.0006080287141733543, -0.0005515554982505122, -0.0004935296633211693, -0.00043578666200400735, -0.0003798576395459785],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_4": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_4": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_4": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_5": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_5": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_5": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_5": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_5": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_6": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_6": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_6": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_6": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_6": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_7": {
            "samples": [0.0] * 105 + [-0.00015778376362709102, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009117, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.004863811454255249, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709102] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_7": {
            "samples": [0.0] * 105 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789555, 0.0016217826115637818, 0.002138921749805219, 0.0026967740303955536, 0.003289415745753081, 0.003908942525632037, 0.004545532613031832, 0.005187620832681907, 0.005822186296327271, 0.006435148841109958, 0.007011860634169721, 0.007537671049128935, 0.007998535633794194, 0.00838163451640098, 0.008675962590192947, 0.008872853716940653, 0.008966404172880875, 0.008953766494256924, 0.008835293328522899, 0.008614521158764746, 0.008297994944280965, 0.007894945810504669, 0.007416843935897081, 0.006876856847658553, 0.0062892487868441245, 0.005668759247261229, 0.005029998149985528, 0.0043868916083357025, 0.0037522063520680432, 0.0031371732953768216, 0.0025512222418611025, 0.002001831129893861, 0.0014944852749314576, 0.0010327353644391084, 0.0006183379243041822, 0.00025145881453495536, -6.908096354474362e-05, -0.00034553742236856605] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_7": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_7": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_7": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_8": {
            "samples": [0.0] * 105 + [-0.0001577837636270911, 0.0005358236462419261, 0.0013288311147143371, 0.0022237650156902507, 0.003220313321556805, 0.004314806824009116, 0.005499787323106856, 0.006763705875530091, 0.008090791755457433, 0.009461126481233454, 0.01085094709073768, 0.012233189208447764, 0.013578264158704062, 0.01485504664661625, 0.016032031846637824, 0.017078604759892795, 0.01796635205879739, 0.018670338762580556, 0.01917027003166739, 0.019451462661092028, 0.019505561409210812, 0.01933095140141051, 0.018932838204992752, 0.018322990034824432, 0.017519159903993792, 0.01654422731086274, 0.015425117354989585, 0.014191568472623336, 0.012874827277601197, 0.011506349901330282, 0.010116583993081482, 0.00873389498912647, 0.007383685659073526, 0.006087740851514874, 0.00486381145425525, 0.0037254344455140884, 0.002681970897594845, 0.0017388319130844834, 0.0008978543256915442, 0.0001577837636270911] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_8": {
            "samples": [0.0] * 105 + [0.000345537422368566, 0.0007237455283559925, 0.001149337124578956, 0.0016217826115637827, 0.0021389217498052194, 0.0026967740303955544, 0.003289415745753082, 0.003908942525632038, 0.004545532613031834, 0.00518762083268191, 0.0058221862963272735, 0.00643514884110996, 0.0070118606341697245, 0.007537671049128939, 0.007998535633794197, 0.008381634516400985, 0.00867596259019295, 0.008872853716940658, 0.00896640417288088, 0.008953766494256929, 0.008835293328522904, 0.008614521158764751, 0.00829799494428097, 0.007894945810504672, 0.007416843935897087, 0.006876856847658557, 0.006289248786844128, 0.005668759247261232, 0.005029998149985531, 0.004386891608335705, 0.0037522063520680463, 0.0031371732953768237, 0.002551222241861104, 0.002001831129893863, 0.0014944852749314585, 0.0010327353644391094, 0.0006183379243041828, 0.00025145881453495585, -6.90809635447434e-05, -0.000345537422368566] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_8": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_8": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_8": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_9": {
            "samples": [0.0, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271] + [0.0] * 109,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_9": {
            "samples": [-0.0003798576395459785, -0.00043578666200400735, -0.0004935296633211693, -0.0005515554982505122, -0.0006080287141733543, -0.0006608525432248669, -0.0007077364436294015, -0.0007462873610355451, -0.0007741217179457732, -0.000788992915208048, -0.0007889270697455971, -0.0007723580575993246, -0.0007382519077163814, -0.0006862103827387051, -0.0006165442994707075, -0.0005303088013655113, -0.00042929531097465857, -0.00031597807114201563, -0.00019341675095889237, -6.512020720763538e-05, 6.512020720763538e-05, 0.00019341675095889237, 0.00031597807114201563, 0.00042929531097465857, 0.0005303088013655113, 0.0006165442994707075, 0.0006862103827387051, 0.0007382519077163814, 0.0007723580575993246, 0.0007889270697455971, 0.000788992915208048, 0.0007741217179457732, 0.0007462873610355451, 0.0007077364436294015, 0.0006608525432248669, 0.0006080287141733543, 0.0005515554982505122, 0.0004935296633211693, 0.00043578666200400735, 0.0003798576395459785] + [0.0] * 108,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_9": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_9": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_9": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_10": {
            "samples": [0.0, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271] + [0.0] * 66 + [-0.00015778376362709102, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009117, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.004863811454255249, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709102] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_10": {
            "samples": [-0.0003798576395459785, -0.00043578666200400735, -0.0004935296633211693, -0.0005515554982505122, -0.0006080287141733543, -0.0006608525432248669, -0.0007077364436294015, -0.0007462873610355451, -0.0007741217179457732, -0.000788992915208048, -0.0007889270697455971, -0.0007723580575993246, -0.0007382519077163814, -0.0006862103827387051, -0.0006165442994707075, -0.0005303088013655113, -0.00042929531097465857, -0.00031597807114201563, -0.00019341675095889237, -6.512020720763538e-05, 6.512020720763538e-05, 0.00019341675095889237, 0.00031597807114201563, 0.00042929531097465857, 0.0005303088013655113, 0.0006165442994707075, 0.0006862103827387051, 0.0007382519077163814, 0.0007723580575993246, 0.0007889270697455971, 0.000788992915208048, 0.0007741217179457732, 0.0007462873610355451, 0.0007077364436294015, 0.0006608525432248669, 0.0006080287141733543, 0.0005515554982505122, 0.0004935296633211693, 0.00043578666200400735, 0.0003798576395459785] + [0.0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789555, 0.0016217826115637818, 0.002138921749805219, 0.0026967740303955536, 0.003289415745753081, 0.003908942525632037, 0.004545532613031832, 0.005187620832681907, 0.005822186296327271, 0.006435148841109958, 0.007011860634169721, 0.007537671049128935, 0.007998535633794194, 0.00838163451640098, 0.008675962590192947, 0.008872853716940653, 0.008966404172880875, 0.008953766494256924, 0.008835293328522899, 0.008614521158764746, 0.008297994944280965, 0.007894945810504669, 0.007416843935897081, 0.006876856847658553, 0.0062892487868441245, 0.005668759247261229, 0.005029998149985528, 0.0043868916083357025, 0.0037522063520680432, 0.0031371732953768216, 0.0025512222418611025, 0.002001831129893861, 0.0014944852749314576, 0.0010327353644391084, 0.0006183379243041822, 0.00025145881453495536, -6.908096354474362e-05, -0.00034553742236856605] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_10": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_10": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_10": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_11": {
            "samples": [0.0, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271] + [0.0] * 66 + [-0.0001577837636270911, 0.0005358236462419261, 0.0013288311147143371, 0.0022237650156902507, 0.003220313321556805, 0.004314806824009116, 0.005499787323106856, 0.006763705875530091, 0.008090791755457433, 0.009461126481233454, 0.01085094709073768, 0.012233189208447764, 0.013578264158704062, 0.01485504664661625, 0.016032031846637824, 0.017078604759892795, 0.01796635205879739, 0.018670338762580556, 0.01917027003166739, 0.019451462661092028, 0.019505561409210812, 0.01933095140141051, 0.018932838204992752, 0.018322990034824432, 0.017519159903993792, 0.01654422731086274, 0.015425117354989585, 0.014191568472623336, 0.012874827277601197, 0.011506349901330282, 0.010116583993081482, 0.00873389498912647, 0.007383685659073526, 0.006087740851514874, 0.00486381145425525, 0.0037254344455140884, 0.002681970897594845, 0.0017388319130844834, 0.0008978543256915442, 0.0001577837636270911] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_11": {
            "samples": [-0.0003798576395459785, -0.00043578666200400735, -0.0004935296633211693, -0.0005515554982505122, -0.0006080287141733543, -0.0006608525432248669, -0.0007077364436294015, -0.0007462873610355451, -0.0007741217179457732, -0.000788992915208048, -0.0007889270697455971, -0.0007723580575993246, -0.0007382519077163814, -0.0006862103827387051, -0.0006165442994707075, -0.0005303088013655113, -0.00042929531097465857, -0.00031597807114201563, -0.00019341675095889237, -6.512020720763538e-05, 6.512020720763538e-05, 0.00019341675095889237, 0.00031597807114201563, 0.00042929531097465857, 0.0005303088013655113, 0.0006165442994707075, 0.0006862103827387051, 0.0007382519077163814, 0.0007723580575993246, 0.0007889270697455971, 0.000788992915208048, 0.0007741217179457732, 0.0007462873610355451, 0.0007077364436294015, 0.0006608525432248669, 0.0006080287141733543, 0.0005515554982505122, 0.0004935296633211693, 0.00043578666200400735, 0.0003798576395459785] + [0.0] * 65 + [0.000345537422368566, 0.0007237455283559925, 0.001149337124578956, 0.0016217826115637827, 0.0021389217498052194, 0.0026967740303955544, 0.003289415745753082, 0.003908942525632038, 0.004545532613031834, 0.00518762083268191, 0.0058221862963272735, 0.00643514884110996, 0.0070118606341697245, 0.007537671049128939, 0.007998535633794197, 0.008381634516400985, 0.00867596259019295, 0.008872853716940658, 0.00896640417288088, 0.008953766494256929, 0.008835293328522904, 0.008614521158764751, 0.00829799494428097, 0.007894945810504672, 0.007416843935897087, 0.006876856847658557, 0.006289248786844128, 0.005668759247261232, 0.005029998149985531, 0.004386891608335705, 0.0037522063520680463, 0.0031371732953768237, 0.002551222241861104, 0.002001831129893863, 0.0014944852749314585, 0.0010327353644391094, 0.0006183379243041828, 0.00025145881453495585, -6.90809635447434e-05, -0.000345537422368566] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_11": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_11": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_11": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_12": {
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20] + [0.0] * 108,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_12": {
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785] + [0.0] * 108,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_12": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_12": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_12": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_13": {
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20] + [0.0] * 65 + [-0.000157783763627091, 0.0005358236462419265, 0.0013288311147143378, 0.0022237650156902516, 0.0032203133215568057, 0.004314806824009118, 0.005499787323106857, 0.006763705875530093, 0.008090791755457434, 0.009461126481233456, 0.010850947090737683, 0.012233189208447768, 0.013578264158704065, 0.014855046646616254, 0.016032031846637828, 0.0170786047598928, 0.017966352058797392, 0.01867033876258056, 0.019170270031667394, 0.019451462661092035, 0.01950556140921082, 0.019330951401410515, 0.018932838204992756, 0.018322990034824436, 0.017519159903993796, 0.016544227310862743, 0.015425117354989588, 0.01419156847262334, 0.0128748272776012, 0.011506349901330285, 0.010116583993081484, 0.008733894989126472, 0.007383685659073528, 0.006087740851514875, 0.00486381145425525, 0.0037254344455140893, 0.0026819708975948458, 0.0017388319130844836, 0.0008978543256915441, 0.000157783763627091] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_13": {
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785] + [0.0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789555, 0.0016217826115637818, 0.0021389217498052186, 0.002696774030395553, 0.0032894157457530803, 0.0039089425256320365, 0.004545532613031832, 0.0051876208326819065, 0.005822186296327269, 0.006435148841109956, 0.007011860634169719, 0.007537671049128934, 0.007998535633794192, 0.008381634516400978, 0.008675962590192945, 0.008872853716940651, 0.008966404172880874, 0.008953766494256922, 0.008835293328522897, 0.008614521158764744, 0.008297994944280964, 0.007894945810504667, 0.00741684393589708, 0.006876856847658552, 0.006289248786844123, 0.005668759247261227, 0.0050299981499855265, 0.004386891608335701, 0.0037522063520680424, 0.0031371732953768207, 0.002551222241861101, 0.0020018311298938603, 0.0014944852749314572, 0.0010327353644391077, 0.0006183379243041819, 0.0002514588145349552, -6.908096354474373e-05, -0.00034553742236856605] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_13": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_13": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_13": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_14": {
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20] + [0.0] * 65 + [-0.00015778376362709102, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009117, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.004863811454255249, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709102] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_14": {
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785] + [0.0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789555, 0.0016217826115637818, 0.002138921749805219, 0.0026967740303955536, 0.003289415745753081, 0.003908942525632037, 0.004545532613031832, 0.005187620832681907, 0.005822186296327271, 0.006435148841109958, 0.007011860634169721, 0.007537671049128935, 0.007998535633794194, 0.00838163451640098, 0.008675962590192947, 0.008872853716940653, 0.008966404172880875, 0.008953766494256924, 0.008835293328522899, 0.008614521158764746, 0.008297994944280965, 0.007894945810504669, 0.007416843935897081, 0.006876856847658553, 0.0062892487868441245, 0.005668759247261229, 0.005029998149985528, 0.0043868916083357025, 0.0037522063520680432, 0.0031371732953768216, 0.0025512222418611025, 0.002001831129893861, 0.0014944852749314576, 0.0010327353644391084, 0.0006183379243041822, 0.00025145881453495536, -6.908096354474362e-05, -0.00034553742236856605] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_14": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_14": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_14": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_15": {
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20] + [0.0] * 108,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_15": {
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785] + [0.0] * 108,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_15": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_15": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_15": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_16": {
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20] + [0.0] * 65 + [0.0001577837636270911, -0.0005358236462419261, -0.0013288311147143371, -0.0022237650156902507, -0.003220313321556805, -0.004314806824009116, -0.005499787323106856, -0.006763705875530091, -0.008090791755457433, -0.009461126481233454, -0.01085094709073768, -0.012233189208447764, -0.013578264158704062, -0.01485504664661625, -0.016032031846637824, -0.017078604759892795, -0.01796635205879739, -0.018670338762580556, -0.01917027003166739, -0.019451462661092028, -0.019505561409210812, -0.01933095140141051, -0.018932838204992752, -0.018322990034824432, -0.017519159903993792, -0.01654422731086274, -0.015425117354989585, -0.014191568472623336, -0.012874827277601197, -0.011506349901330282, -0.010116583993081482, -0.00873389498912647, -0.007383685659073526, -0.006087740851514874, -0.00486381145425525, -0.0037254344455140884, -0.002681970897594845, -0.0017388319130844834, -0.0008978543256915442, -0.0001577837636270911] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_16": {
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785] + [0.0] * 65 + [-0.000345537422368566, -0.0007237455283559925, -0.001149337124578956, -0.0016217826115637827, -0.0021389217498052194, -0.0026967740303955544, -0.003289415745753082, -0.003908942525632038, -0.004545532613031834, -0.00518762083268191, -0.0058221862963272735, -0.00643514884110996, -0.0070118606341697245, -0.007537671049128939, -0.007998535633794197, -0.008381634516400985, -0.00867596259019295, -0.008872853716940658, -0.00896640417288088, -0.008953766494256929, -0.008835293328522904, -0.008614521158764751, -0.00829799494428097, -0.007894945810504672, -0.007416843935897087, -0.006876856847658557, -0.006289248786844128, -0.005668759247261232, -0.005029998149985531, -0.004386891608335705, -0.0037522063520680463, -0.0031371732953768237, -0.002551222241861104, -0.002001831129893863, -0.0014944852749314585, -0.0010327353644391094, -0.0006183379243041828, -0.00025145881453495585, 6.90809635447434e-05, 0.000345537422368566] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_16": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_16": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_16": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_17": {
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20] + [0.0] * 65 + [0.00015778376362709116, -0.0005358236462419261, -0.001328831114714337, -0.0022237650156902507, -0.003220313321556805, -0.004314806824009116, -0.005499787323106856, -0.00676370587553009, -0.008090791755457433, -0.009461126481233454, -0.01085094709073768, -0.012233189208447764, -0.013578264158704062, -0.01485504664661625, -0.016032031846637824, -0.017078604759892795, -0.01796635205879739, -0.018670338762580556, -0.01917027003166739, -0.019451462661092028, -0.019505561409210812, -0.01933095140141051, -0.018932838204992752, -0.018322990034824432, -0.017519159903993792, -0.01654422731086274, -0.015425117354989585, -0.014191568472623336, -0.012874827277601197, -0.011506349901330282, -0.010116583993081482, -0.00873389498912647, -0.007383685659073527, -0.006087740851514874, -0.00486381145425525, -0.0037254344455140884, -0.002681970897594845, -0.0017388319130844836, -0.0008978543256915442, -0.00015778376362709116] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_17": {
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785] + [0.0] * 65 + [-0.000345537422368566, -0.0007237455283559927, -0.001149337124578956, -0.0016217826115637827, -0.00213892174980522, -0.0026967740303955553, -0.003289415745753083, -0.00390894252563204, -0.004545532613031835, -0.005187620832681911, -0.005822186296327275, -0.006435148841109962, -0.007011860634169726, -0.007537671049128941, -0.0079985356337942, -0.008381634516400987, -0.008675962590192954, -0.00887285371694066, -0.008966404172880882, -0.00895376649425693, -0.008835293328522906, -0.008614521158764753, -0.008297994944280972, -0.007894945810504676, -0.007416843935897088, -0.006876856847658559, -0.00628924878684413, -0.005668759247261234, -0.005029998149985533, -0.004386891608335707, -0.003752206352068047, -0.0031371732953768246, -0.002551222241861105, -0.002001831129893864, -0.0014944852749314594, -0.0010327353644391099, -0.000618337924304183, -0.00025145881453495606, 6.90809635447433e-05, 0.000345537422368566] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_17": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_17": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_17": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_18": {
            "samples": [0.0, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271] + [0.0] * 109,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_18": {
            "samples": [0.0003798576395459785, 0.00043578666200400735, 0.0004935296633211693, 0.0005515554982505122, 0.0006080287141733543, 0.0006608525432248669, 0.0007077364436294015, 0.0007462873610355451, 0.0007741217179457732, 0.000788992915208048, 0.0007889270697455971, 0.0007723580575993246, 0.0007382519077163814, 0.0006862103827387051, 0.0006165442994707075, 0.0005303088013655113, 0.00042929531097465857, 0.00031597807114201563, 0.00019341675095889237, 6.512020720763538e-05, -6.512020720763538e-05, -0.00019341675095889237, -0.00031597807114201563, -0.00042929531097465857, -0.0005303088013655113, -0.0006165442994707075, -0.0006862103827387051, -0.0007382519077163814, -0.0007723580575993246, -0.0007889270697455971, -0.000788992915208048, -0.0007741217179457732, -0.0007462873610355451, -0.0007077364436294015, -0.0006608525432248669, -0.0006080287141733543, -0.0005515554982505122, -0.0004935296633211693, -0.00043578666200400735, -0.0003798576395459785] + [0.0] * 108,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_18": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_18": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_18": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_19": {
            "samples": [0.0, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271] + [0.0] * 66 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_19": {
            "samples": [0.0003798576395459785, 0.00043578666200400735, 0.0004935296633211693, 0.0005515554982505122, 0.0006080287141733543, 0.0006608525432248669, 0.0007077364436294015, 0.0007462873610355451, 0.0007741217179457732, 0.000788992915208048, 0.0007889270697455971, 0.0007723580575993246, 0.0007382519077163814, 0.0006862103827387051, 0.0006165442994707075, 0.0005303088013655113, 0.00042929531097465857, 0.00031597807114201563, 0.00019341675095889237, 6.512020720763538e-05, -6.512020720763538e-05, -0.00019341675095889237, -0.00031597807114201563, -0.00042929531097465857, -0.0005303088013655113, -0.0006165442994707075, -0.0006862103827387051, -0.0007382519077163814, -0.0007723580575993246, -0.0007889270697455971, -0.000788992915208048, -0.0007741217179457732, -0.0007462873610355451, -0.0007077364436294015, -0.0006608525432248669, -0.0006080287141733543, -0.0005515554982505122, -0.0004935296633211693, -0.00043578666200400735, -0.0003798576395459785] + [0.0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_19": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_19": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_19": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_20": {
            "samples": [0.0, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271] + [0.0] * 66 + [0.00015778376362709108, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009116, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.00486381145425525, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709108] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_20": {
            "samples": [0.0003798576395459785, 0.00043578666200400735, 0.0004935296633211693, 0.0005515554982505122, 0.0006080287141733543, 0.0006608525432248669, 0.0007077364436294015, 0.0007462873610355451, 0.0007741217179457732, 0.000788992915208048, 0.0007889270697455971, 0.0007723580575993246, 0.0007382519077163814, 0.0006862103827387051, 0.0006165442994707075, 0.0005303088013655113, 0.00042929531097465857, 0.00031597807114201563, 0.00019341675095889237, 6.512020720763538e-05, -6.512020720763538e-05, -0.00019341675095889237, -0.00031597807114201563, -0.00042929531097465857, -0.0005303088013655113, -0.0006165442994707075, -0.0006862103827387051, -0.0007382519077163814, -0.0007723580575993246, -0.0007889270697455971, -0.000788992915208048, -0.0007741217179457732, -0.0007462873610355451, -0.0007077364436294015, -0.0006608525432248669, -0.0006080287141733543, -0.0005515554982505122, -0.0004935296633211693, -0.00043578666200400735, -0.0003798576395459785] + [0.0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789557, -0.0016217826115637823, -0.002138921749805219, -0.002696774030395554, -0.003289415745753081, -0.003908942525632038, -0.0045455326130318325, -0.005187620832681909, -0.005822186296327273, -0.006435148841109959, -0.007011860634169723, -0.007537671049128937, -0.007998535633794195, -0.008381634516400982, -0.008675962590192949, -0.008872853716940654, -0.008966404172880879, -0.008953766494256927, -0.008835293328522903, -0.00861452115876475, -0.008297994944280967, -0.00789494581050467, -0.007416843935897083, -0.006876856847658555, -0.006289248786844126, -0.00566875924726123, -0.00502999814998553, -0.004386891608335704, -0.003752206352068045, -0.0031371732953768224, -0.0025512222418611033, -0.002001831129893862, -0.001494485274931458, -0.0010327353644391088, -0.0006183379243041826, -0.0002514588145349556, 6.908096354474351e-05, 0.00034553742236856605] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_20": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_20": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_20": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_21": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_21": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_21": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_21": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_21": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_22": {
            "samples": [0.0] * 105 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_22": {
            "samples": [0.0] * 105 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_22": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_22": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_22": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_23": {
            "samples": [0.0] * 105 + [0.00015778376362709108, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009116, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.00486381145425525, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709108] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_23": {
            "samples": [0.0] * 105 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789557, -0.0016217826115637823, -0.002138921749805219, -0.002696774030395554, -0.003289415745753081, -0.003908942525632038, -0.0045455326130318325, -0.005187620832681909, -0.005822186296327273, -0.006435148841109959, -0.007011860634169723, -0.007537671049128937, -0.007998535633794195, -0.008381634516400982, -0.008675962590192949, -0.008872853716940654, -0.008966404172880879, -0.008953766494256927, -0.008835293328522903, -0.00861452115876475, -0.008297994944280967, -0.00789494581050467, -0.007416843935897083, -0.006876856847658555, -0.006289248786844126, -0.00566875924726123, -0.00502999814998553, -0.004386891608335704, -0.003752206352068045, -0.0031371732953768224, -0.0025512222418611033, -0.002001831129893862, -0.001494485274931458, -0.0010327353644391088, -0.0006183379243041826, -0.0002514588145349556, 6.908096354474351e-05, 0.00034553742236856605] + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_23": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_23": {
            "samples": [0.0] * 148,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_23": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_24": {
            "samples": [0.0, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271] + [0.0] * 66 + [-0.00015778376362709108, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009116, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.00486381145425525, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709108] + [0.0] * 65 + [0.00028705593516813806, -0.00018678531325335427, -0.0007313638374660265, -0.0013491977358940606, -0.0020409004844246254, -0.002804787796534071, -0.0036365358884280635, -0.00452892255227461, -0.005471681673197406, -0.0064514983052773416, -0.007452165040045104, -0.00845491133631501, -0.009438906220329309, -0.010381922093328637, -0.011261134326336944, -0.012054019059648714, -0.0127393013734789, -0.013297898873999259, -0.013713802630057085, -0.013974838835556972, -0.014073260665380763, -0.014006130178820088, -0.01377546399978011, -0.01338813269408848, -0.01285552084903392, -0.0121929713201575, -0.011419051494620048, -0.010554690502106464, -0.009622243207138077, -0.008644539099210863, -0.0076439718824142175, -0.006641679117210861, -0.005656851513146753, -0.004706199496728453, -0.003803591690700294, -0.002959867133955371, -0.0021828115051823046, -0.0014772781184435272, -0.0008454275769439331, -0.00028705593516813806] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_24": {
            "samples": [-0.0003798576395459785, -0.00043578666200400735, -0.0004935296633211693, -0.0005515554982505122, -0.0006080287141733543, -0.0006608525432248669, -0.0007077364436294015, -0.0007462873610355451, -0.0007741217179457732, -0.000788992915208048, -0.0007889270697455971, -0.0007723580575993246, -0.0007382519077163814, -0.0006862103827387051, -0.0006165442994707075, -0.0005303088013655113, -0.00042929531097465857, -0.00031597807114201563, -0.00019341675095889237, -6.512020720763538e-05, 6.512020720763538e-05, 0.00019341675095889237, 0.00031597807114201563, 0.00042929531097465857, 0.0005303088013655113, 0.0006165442994707075, 0.0006862103827387051, 0.0007382519077163814, 0.0007723580575993246, 0.0007889270697455971, 0.000788992915208048, 0.0007741217179457732, 0.0007462873610355451, 0.0007077364436294015, 0.0006608525432248669, 0.0006080287141733543, 0.0005515554982505122, 0.0004935296633211693, 0.00043578666200400735, 0.0003798576395459785] + [0.0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789557, 0.0016217826115637823, 0.002138921749805219, 0.002696774030395554, 0.003289415745753081, 0.003908942525632038, 0.0045455326130318325, 0.005187620832681909, 0.005822186296327273, 0.006435148841109959, 0.007011860634169723, 0.007537671049128937, 0.007998535633794195, 0.008381634516400982, 0.008675962590192949, 0.008872853716940654, 0.008966404172880879, 0.008953766494256927, 0.008835293328522903, 0.00861452115876475, 0.008297994944280967, 0.00789494581050467, 0.007416843935897083, 0.006876856847658555, 0.006289248786844126, 0.00566875924726123, 0.00502999814998553, 0.004386891608335704, 0.003752206352068045, 0.0031371732953768224, 0.0025512222418611033, 0.002001831129893862, 0.001494485274931458, 0.0010327353644391088, 0.0006183379243041826, 0.0002514588145349556, -6.908096354474351e-05, -0.00034553742236856605] + [0.0] * 65 + [-0.0002487784484359292, -0.0008809232750019345, -0.0015974588866745014, -0.002398952928599652, -0.0032833107305677567, -0.004245387322252832, -0.00527669624670493, -0.006365250140793627, -0.007495563863613571, -0.008648843495784616, -0.009803374023827674, -0.010935105537303865, -0.012018423211070372, -0.01302707140404458, -0.013935188233421202, -0.014718395368408294, -0.015354879800335767, -0.015826400984703847, -0.01611915861024824, -0.016224463430565095, -0.01613916566411604, -0.015865811491772044, -0.015412516802343084, -0.014792566921686038, -0.014023769871586293, -0.013127607085927794, -0.012128238069943915, -0.011051423235100081, -0.00992343158789372, -0.008769997137818475, -0.007615380362032688, -0.006481579781991357, -0.005387724918514692, -0.004349666980908773, -0.003379768978786449, -0.0024868837307194048, -0.0016764974252954485, -0.0009510085794230893, -0.0003101076939226075, 0.0002487784484359292] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_24": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_24": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_24": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 62,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_25": {
            "samples": [0.0, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271] + [0.0] * 66 + [-0.00015778376362709108, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009116, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.00486381145425525, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709108] + [0.0] * 65 + [-0.000287055935168138, 0.00018678531325335443, 0.0007313638374660268, 0.0013491977358940609, 0.002040900484424626, 0.0028047877965340718, 0.0036365358884280644, 0.004528922552274611, 0.005471681673197407, 0.006451498305277343, 0.007452165040045105, 0.008454911336315011, 0.00943890622032931, 0.010381922093328638, 0.011261134326336946, 0.012054019059648716, 0.012739301373478904, 0.01329789887399926, 0.013713802630057087, 0.013974838835556974, 0.014073260665380765, 0.01400613017882009, 0.013775463999780111, 0.013388132694088483, 0.012855520849033922, 0.012192971320157502, 0.01141905149462005, 0.010554690502106466, 0.009622243207138078, 0.008644539099210865, 0.007643971882414219, 0.006641679117210862, 0.0056568515131467535, 0.004706199496728454, 0.003803591690700295, 0.0029598671339553712, 0.0021828115051823046, 0.0014772781184435274, 0.0008454275769439332, 0.000287055935168138] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_25": {
            "samples": [-0.0003798576395459785, -0.00043578666200400735, -0.0004935296633211693, -0.0005515554982505122, -0.0006080287141733543, -0.0006608525432248669, -0.0007077364436294015, -0.0007462873610355451, -0.0007741217179457732, -0.000788992915208048, -0.0007889270697455971, -0.0007723580575993246, -0.0007382519077163814, -0.0006862103827387051, -0.0006165442994707075, -0.0005303088013655113, -0.00042929531097465857, -0.00031597807114201563, -0.00019341675095889237, -6.512020720763538e-05, 6.512020720763538e-05, 0.00019341675095889237, 0.00031597807114201563, 0.00042929531097465857, 0.0005303088013655113, 0.0006165442994707075, 0.0006862103827387051, 0.0007382519077163814, 0.0007723580575993246, 0.0007889270697455971, 0.000788992915208048, 0.0007741217179457732, 0.0007462873610355451, 0.0007077364436294015, 0.0006608525432248669, 0.0006080287141733543, 0.0005515554982505122, 0.0004935296633211693, 0.00043578666200400735, 0.0003798576395459785] + [0.0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789557, 0.0016217826115637823, 0.002138921749805219, 0.002696774030395554, 0.003289415745753081, 0.003908942525632038, 0.0045455326130318325, 0.005187620832681909, 0.005822186296327273, 0.006435148841109959, 0.007011860634169723, 0.007537671049128937, 0.007998535633794195, 0.008381634516400982, 0.008675962590192949, 0.008872853716940654, 0.008966404172880879, 0.008953766494256927, 0.008835293328522903, 0.00861452115876475, 0.008297994944280967, 0.00789494581050467, 0.007416843935897083, 0.006876856847658555, 0.006289248786844126, 0.00566875924726123, 0.00502999814998553, 0.004386891608335704, 0.003752206352068045, 0.0031371732953768224, 0.0025512222418611033, 0.002001831129893862, 0.001494485274931458, 0.0010327353644391088, 0.0006183379243041826, 0.0002514588145349556, -6.908096354474351e-05, -0.00034553742236856605] + [0.0] * 65 + [0.0002487784484359292, 0.0008809232750019345, 0.0015974588866745011, 0.0023989529285996514, 0.0032833107305677563, 0.004245387322252832, 0.005276696246704929, 0.006365250140793626, 0.00749556386361357, 0.008648843495784615, 0.009803374023827673, 0.010935105537303863, 0.01201842321107037, 0.013027071404044578, 0.0139351882334212, 0.014718395368408292, 0.015354879800335765, 0.015826400984703844, 0.016119158610248235, 0.016224463430565092, 0.016139165664116037, 0.01586581149177204, 0.015412516802343082, 0.014792566921686037, 0.014023769871586291, 0.013127607085927792, 0.012128238069943913, 0.01105142323510008, 0.009923431587893718, 0.008769997137818474, 0.007615380362032686, 0.0064815797819913566, 0.005387724918514691, 0.004349666980908772, 0.0033797689787864486, 0.0024868837307194043, 0.001676497425295448, 0.000951008579423089, 0.0003101076939226073, -0.0002487784484359292] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_25": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_25": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_25": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 62,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_26": {
            "samples": [0.0, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271] + [0.0] * 66 + [-0.00015778376362709108, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009116, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.00486381145425525, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709108] + [0.0] * 107,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_26": {
            "samples": [-0.0003798576395459785, -0.00043578666200400735, -0.0004935296633211693, -0.0005515554982505122, -0.0006080287141733543, -0.0006608525432248669, -0.0007077364436294015, -0.0007462873610355451, -0.0007741217179457732, -0.000788992915208048, -0.0007889270697455971, -0.0007723580575993246, -0.0007382519077163814, -0.0006862103827387051, -0.0006165442994707075, -0.0005303088013655113, -0.00042929531097465857, -0.00031597807114201563, -0.00019341675095889237, -6.512020720763538e-05, 6.512020720763538e-05, 0.00019341675095889237, 0.00031597807114201563, 0.00042929531097465857, 0.0005303088013655113, 0.0006165442994707075, 0.0006862103827387051, 0.0007382519077163814, 0.0007723580575993246, 0.0007889270697455971, 0.000788992915208048, 0.0007741217179457732, 0.0007462873610355451, 0.0007077364436294015, 0.0006608525432248669, 0.0006080287141733543, 0.0005515554982505122, 0.0004935296633211693, 0.00043578666200400735, 0.0003798576395459785] + [0.0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789557, 0.0016217826115637823, 0.002138921749805219, 0.002696774030395554, 0.003289415745753081, 0.003908942525632038, 0.0045455326130318325, 0.005187620832681909, 0.005822186296327273, 0.006435148841109959, 0.007011860634169723, 0.007537671049128937, 0.007998535633794195, 0.008381634516400982, 0.008675962590192949, 0.008872853716940654, 0.008966404172880879, 0.008953766494256927, 0.008835293328522903, 0.00861452115876475, 0.008297994944280967, 0.00789494581050467, 0.007416843935897083, 0.006876856847658555, 0.006289248786844126, 0.00566875924726123, 0.00502999814998553, 0.004386891608335704, 0.003752206352068045, 0.0031371732953768224, 0.0025512222418611033, 0.002001831129893862, 0.001494485274931458, 0.0010327353644391088, 0.0006183379243041826, 0.0002514588145349556, -6.908096354474351e-05, -0.00034553742236856605] + [0.0] * 107,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_26": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_26": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_26": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 62,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_27": {
            "samples": [-0.000759715279091957, -0.0008715733240080146, -0.0009870593266423384, -0.0011031109965010239, -0.0012160574283467081, -0.001321705086449733, -0.001415472887258802, -0.0014925747220710893, -0.0015482434358915452, -0.0015779858304160947, -0.0015778541394911927, -0.0015447161151986475, -0.001476503815432761, -0.0013724207654774083, -0.0012330885989414128, -0.0010606176027310203, -0.0008585906219493146, -0.0006319561422840288, -0.00038683350191778213, -0.00013024041441526813, 0.0001302404144152734, 0.00038683350191778734, 0.0006319561422840338, 0.0008585906219493196, 0.001060617602731025, 0.001233088598941417, 0.0013724207654774122, 0.0014765038154327648, 0.001544716115198651, 0.0015778541394911958, 0.0015779858304160973, 0.0015482434358915474, 0.001492574722071091, 0.0014154728872588038, 0.0013217050864497344, 0.001216057428346709, 0.0011031109965010247, 0.0009870593266423388, 0.0008715733240080148, 0.000759715279091957] + [0.0] * 65 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0.0] * 65 + [-0.000287055935168138, 0.00018678531325335443, 0.0007313638374660268, 0.0013491977358940609, 0.002040900484424626, 0.0028047877965340718, 0.0036365358884280644, 0.004528922552274611, 0.005471681673197407, 0.006451498305277343, 0.007452165040045105, 0.008454911336315011, 0.00943890622032931, 0.010381922093328638, 0.011261134326336946, 0.012054019059648716, 0.012739301373478904, 0.01329789887399926, 0.013713802630057087, 0.013974838835556974, 0.014073260665380765, 0.01400613017882009, 0.013775463999780111, 0.013388132694088483, 0.012855520849033922, 0.012192971320157502, 0.01141905149462005, 0.010554690502106466, 0.009622243207138078, 0.008644539099210865, 0.007643971882414219, 0.006641679117210862, 0.0056568515131467535, 0.004706199496728454, 0.003803591690700295, 0.0029598671339553712, 0.0021828115051823046, 0.0014772781184435274, 0.0008454275769439332, 0.000287055935168138] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_27": {
            "samples": [4.651914424016516e-20, 0.0015760768444548542, 0.00337235610740649, 0.005392994053965991, 0.0076356283889478915, 0.010090276907130893, 0.012738449776040096, 0.015552569435837084, 0.018495784766494085, 0.0215222502891611, 0.024577916926684592, 0.027601849347301578, 0.030528048168025384, 0.033287716114425325, 0.03581186901257599, 0.03803415887258986, 0.03989375082406045, 0.04133808125447058, 0.04232532323982649] + [0.04282639809501372] * 2 + [0.04232532323982649, 0.04133808125447058, 0.03989375082406045, 0.03803415887258986, 0.03581186901257599, 0.033287716114425325, 0.030528048168025384, 0.027601849347301578, 0.024577916926684592, 0.0215222502891611, 0.018495784766494085, 0.015552569435837084, 0.012738449776040096, 0.010090276907130893, 0.0076356283889478915, 0.005392994053965991, 0.00337235610740649, 0.0015760768444548542, -4.651914424016516e-20] + [0.0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0.0] * 65 + [0.0002487784484359292, 0.0008809232750019345, 0.0015974588866745011, 0.0023989529285996514, 0.0032833107305677563, 0.004245387322252832, 0.005276696246704929, 0.006365250140793626, 0.00749556386361357, 0.008648843495784615, 0.009803374023827673, 0.010935105537303863, 0.01201842321107037, 0.013027071404044578, 0.0139351882334212, 0.014718395368408292, 0.015354879800335765, 0.015826400984703844, 0.016119158610248235, 0.016224463430565092, 0.016139165664116037, 0.01586581149177204, 0.015412516802343082, 0.014792566921686037, 0.014023769871586291, 0.013127607085927792, 0.012128238069943913, 0.01105142323510008, 0.009923431587893718, 0.008769997137818474, 0.007615380362032686, 0.0064815797819913566, 0.005387724918514691, 0.004349666980908772, 0.0033797689787864486, 0.0024868837307194043, 0.001676497425295448, 0.000951008579423089, 0.0003101076939226073, -0.0002487784484359292] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_27": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_27": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_27": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 62,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_28": {
            "samples": [-0.000759715279091957, -0.0008715733240080146, -0.0009870593266423384, -0.0011031109965010239, -0.0012160574283467081, -0.001321705086449733, -0.001415472887258802, -0.0014925747220710893, -0.0015482434358915452, -0.0015779858304160947, -0.0015778541394911927, -0.0015447161151986475, -0.001476503815432761, -0.0013724207654774083, -0.0012330885989414128, -0.0010606176027310203, -0.0008585906219493146, -0.0006319561422840288, -0.00038683350191778213, -0.00013024041441526813, 0.0001302404144152734, 0.00038683350191778734, 0.0006319561422840338, 0.0008585906219493196, 0.001060617602731025, 0.001233088598941417, 0.0013724207654774122, 0.0014765038154327648, 0.001544716115198651, 0.0015778541394911958, 0.0015779858304160973, 0.0015482434358915474, 0.001492574722071091, 0.0014154728872588038, 0.0013217050864497344, 0.001216057428346709, 0.0011031109965010247, 0.0009870593266423388, 0.0008715733240080148, 0.000759715279091957] + [0.0] * 65 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0.0] * 65 + [0.000287055935168138, -0.00018678531325335454, -0.000731363837466027, -0.0013491977358940613, -0.0020409004844246263, -0.002804787796534072, -0.0036365358884280653, -0.004528922552274612, -0.005471681673197408, -0.006451498305277344, -0.007452165040045105, -0.008454911336315013, -0.009438906220329312, -0.01038192209332864, -0.011261134326336948, -0.012054019059648717, -0.012739301373478906, -0.013297898873999263, -0.01371380263005709, -0.013974838835556978, -0.014073260665380768, -0.014006130178820093, -0.013775463999780113, -0.013388132694088485, -0.012855520849033924, -0.012192971320157503, -0.011419051494620051, -0.010554690502106468, -0.00962224320713808, -0.008644539099210865, -0.00764397188241422, -0.006641679117210864, -0.005656851513146754, -0.004706199496728455, -0.0038035916907002954, -0.0029598671339553717, -0.002182811505182305, -0.0014772781184435274, -0.0008454275769439333, -0.000287055935168138] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_28": {
            "samples": [4.651914424016516e-20, 0.0015760768444548542, 0.00337235610740649, 0.005392994053965991, 0.0076356283889478915, 0.010090276907130893, 0.012738449776040096, 0.015552569435837084, 0.018495784766494085, 0.0215222502891611, 0.024577916926684592, 0.027601849347301578, 0.030528048168025384, 0.033287716114425325, 0.03581186901257599, 0.03803415887258986, 0.03989375082406045, 0.04133808125447058, 0.04232532323982649] + [0.04282639809501372] * 2 + [0.04232532323982649, 0.04133808125447058, 0.03989375082406045, 0.03803415887258986, 0.03581186901257599, 0.033287716114425325, 0.030528048168025384, 0.027601849347301578, 0.024577916926684592, 0.0215222502891611, 0.018495784766494085, 0.015552569435837084, 0.012738449776040096, 0.010090276907130893, 0.0076356283889478915, 0.005392994053965991, 0.00337235610740649, 0.0015760768444548542, -4.651914424016516e-20] + [0.0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0.0] * 65 + [-0.00024877844843592924, -0.0008809232750019345, -0.0015974588866745014, -0.0023989529285996514, -0.0032833107305677563, -0.004245387322252832, -0.005276696246704929, -0.006365250140793626, -0.00749556386361357, -0.008648843495784615, -0.009803374023827673, -0.010935105537303863, -0.01201842321107037, -0.013027071404044578, -0.0139351882334212, -0.014718395368408294, -0.015354879800335765, -0.015826400984703844, -0.016119158610248235, -0.016224463430565092, -0.016139165664116037, -0.01586581149177204, -0.015412516802343082, -0.014792566921686037, -0.01402376987158629, -0.013127607085927792, -0.012128238069943913, -0.01105142323510008, -0.009923431587893718, -0.008769997137818474, -0.007615380362032686, -0.0064815797819913566, -0.005387724918514691, -0.004349666980908772, -0.0033797689787864486, -0.0024868837307194043, -0.001676497425295448, -0.0009510085794230889, -0.00031010769392260726, 0.00024877844843592924] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_28": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_28": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_28": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 62,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_29": {
            "samples": [-0.000759715279091957, -0.0008715733240080146, -0.0009870593266423384, -0.0011031109965010239, -0.0012160574283467081, -0.001321705086449733, -0.001415472887258802, -0.0014925747220710893, -0.0015482434358915452, -0.0015779858304160947, -0.0015778541394911927, -0.0015447161151986475, -0.001476503815432761, -0.0013724207654774083, -0.0012330885989414128, -0.0010606176027310203, -0.0008585906219493146, -0.0006319561422840288, -0.00038683350191778213, -0.00013024041441526813, 0.0001302404144152734, 0.00038683350191778734, 0.0006319561422840338, 0.0008585906219493196, 0.001060617602731025, 0.001233088598941417, 0.0013724207654774122, 0.0014765038154327648, 0.001544716115198651, 0.0015778541394911958, 0.0015779858304160973, 0.0015482434358915474, 0.001492574722071091, 0.0014154728872588038, 0.0013217050864497344, 0.001216057428346709, 0.0011031109965010247, 0.0009870593266423388, 0.0008715733240080148, 0.000759715279091957] + [0.0] * 65 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0.0] * 107,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_29": {
            "samples": [4.651914424016516e-20, 0.0015760768444548542, 0.00337235610740649, 0.005392994053965991, 0.0076356283889478915, 0.010090276907130893, 0.012738449776040096, 0.015552569435837084, 0.018495784766494085, 0.0215222502891611, 0.024577916926684592, 0.027601849347301578, 0.030528048168025384, 0.033287716114425325, 0.03581186901257599, 0.03803415887258986, 0.03989375082406045, 0.04133808125447058, 0.04232532323982649] + [0.04282639809501372] * 2 + [0.04232532323982649, 0.04133808125447058, 0.03989375082406045, 0.03803415887258986, 0.03581186901257599, 0.033287716114425325, 0.030528048168025384, 0.027601849347301578, 0.024577916926684592, 0.0215222502891611, 0.018495784766494085, 0.015552569435837084, 0.012738449776040096, 0.010090276907130893, 0.0076356283889478915, 0.005392994053965991, 0.00337235610740649, 0.0015760768444548542, -4.651914424016516e-20] + [0.0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0.0] * 107,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_29": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_29": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_29": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 62,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_30": {
            "samples": [0.0, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271] + [0.0] * 66 + [0.00015778376362709118, -0.000535823646241926, -0.001328831114714337, -0.0022237650156902507, -0.003220313321556805, -0.004314806824009116, -0.005499787323106856, -0.00676370587553009, -0.008090791755457433, -0.009461126481233454, -0.01085094709073768, -0.012233189208447764, -0.013578264158704062, -0.01485504664661625, -0.016032031846637824, -0.017078604759892795, -0.01796635205879739, -0.018670338762580556, -0.01917027003166739, -0.019451462661092028, -0.019505561409210812, -0.01933095140141051, -0.018932838204992752, -0.018322990034824432, -0.017519159903993792, -0.01654422731086274, -0.015425117354989585, -0.014191568472623336, -0.012874827277601197, -0.011506349901330282, -0.010116583993081482, -0.00873389498912647, -0.007383685659073527, -0.006087740851514874, -0.00486381145425525, -0.0037254344455140884, -0.002681970897594845, -0.0017388319130844836, -0.0008978543256915443, -0.00015778376362709118] + [0.0] * 65 + [-0.00028705593516813844, 0.0001867853132533528, 0.0007313638374660241, 0.0013491977358940567, 0.00204090048442462, 0.002804787796534064, 0.003636535888428055, 0.0045289225522746, 0.005471681673197394, 0.006451498305277328, 0.007452165040045087, 0.008454911336314992, 0.009438906220329288, 0.010381922093328614, 0.011261134326336922, 0.012054019059648691, 0.012739301373478876, 0.013297898873999233, 0.01371380263005706, 0.013974838835556946, 0.014073260665380737, 0.014006130178820062, 0.013775463999780083, 0.013388132694088456, 0.012855520849033897, 0.01219297132015748, 0.011419051494620028, 0.010554690502106447, 0.009622243207138063, 0.00864453909921085, 0.007643971882414205, 0.0066416791172108506, 0.005656851513146744, 0.004706199496728446, 0.003803591690700289, 0.0029598671339553665, 0.0021828115051823016, 0.0014772781184435257, 0.0008454275769439327, 0.00028705593516813844] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_30": {
            "samples": [0.0003798576395459785, 0.00043578666200400735, 0.0004935296633211693, 0.0005515554982505122, 0.0006080287141733543, 0.0006608525432248669, 0.0007077364436294015, 0.0007462873610355451, 0.0007741217179457732, 0.000788992915208048, 0.0007889270697455971, 0.0007723580575993246, 0.0007382519077163814, 0.0006862103827387051, 0.0006165442994707075, 0.0005303088013655113, 0.00042929531097465857, 0.00031597807114201563, 0.00019341675095889237, 6.512020720763538e-05, -6.512020720763538e-05, -0.00019341675095889237, -0.00031597807114201563, -0.00042929531097465857, -0.0005303088013655113, -0.0006165442994707075, -0.0006862103827387051, -0.0007382519077163814, -0.0007723580575993246, -0.0007889270697455971, -0.000788992915208048, -0.0007741217179457732, -0.0007462873610355451, -0.0007077364436294015, -0.0006608525432248669, -0.0006080287141733543, -0.0005515554982505122, -0.0004935296633211693, -0.00043578666200400735, -0.0003798576395459785] + [0.0] * 65 + [-0.000345537422368566, -0.0007237455283559927, -0.001149337124578956, -0.0016217826115637831, -0.0021389217498052203, -0.0026967740303955553, -0.003289415745753083, -0.00390894252563204, -0.004545532613031835, -0.005187620832681912, -0.005822186296327276, -0.006435148841109963, -0.007011860634169727, -0.0075376710491289415, -0.0079985356337942, -0.008381634516400987, -0.008675962590192954, -0.008872853716940661, -0.008966404172880884, -0.008953766494256932, -0.008835293328522908, -0.008614521158764755, -0.008297994944280974, -0.007894945810504676, -0.007416843935897088, -0.00687685684765856, -0.0062892487868441305, -0.005668759247261235, -0.0050299981499855335, -0.004386891608335708, -0.003752206352068048, -0.0031371732953768255, -0.0025512222418611055, -0.002001831129893864, -0.0014944852749314594, -0.0010327353644391099, -0.0006183379243041833, -0.00025145881453495606, 6.908096354474324e-05, 0.000345537422368566] + [0.0] * 65 + [0.0002487784484359287, 0.0008809232750019349, 0.0015974588866745024, 0.002398952928599654, 0.00328331073056776, 0.004245387322252837, 0.005276696246704936, 0.006365250140793635, 0.00749556386361358, 0.008648843495784627, 0.009803374023827685, 0.01093510553730388, 0.012018423211070387, 0.013027071404044598, 0.013935188233421223, 0.014718395368408315, 0.015354879800335789, 0.01582640098470387, 0.01611915861024826, 0.01622446343056512, 0.016139165664116065, 0.015865811491772065, 0.015412516802343108, 0.01479256692168606, 0.014023769871586314, 0.013127607085927815, 0.012128238069943936, 0.0110514232351001, 0.009923431587893735, 0.008769997137818489, 0.0076153803620326995, 0.006481579781991369, 0.005387724918514702, 0.004349666980908781, 0.0033797689787864555, 0.00248688373071941, 0.0016764974252954522, 0.0009510085794230916, 0.0003101076939226089, -0.0002487784484359287] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_30": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_30": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_30": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 62,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_31": {
            "samples": [0.0, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271] + [0.0] * 66 + [0.00015778376362709118, -0.000535823646241926, -0.001328831114714337, -0.0022237650156902507, -0.003220313321556805, -0.004314806824009116, -0.005499787323106856, -0.00676370587553009, -0.008090791755457433, -0.009461126481233454, -0.01085094709073768, -0.012233189208447764, -0.013578264158704062, -0.01485504664661625, -0.016032031846637824, -0.017078604759892795, -0.01796635205879739, -0.018670338762580556, -0.01917027003166739, -0.019451462661092028, -0.019505561409210812, -0.01933095140141051, -0.018932838204992752, -0.018322990034824432, -0.017519159903993792, -0.01654422731086274, -0.015425117354989585, -0.014191568472623336, -0.012874827277601197, -0.011506349901330282, -0.010116583993081482, -0.00873389498912647, -0.007383685659073527, -0.006087740851514874, -0.00486381145425525, -0.0037254344455140884, -0.002681970897594845, -0.0017388319130844836, -0.0008978543256915443, -0.00015778376362709118] + [0.0] * 65 + [0.0002870559351681382, -0.00018678531325335378, -0.0007313638374660256, -0.0013491977358940591, -0.0020409004844246233, -0.0028047877965340683, -0.0036365358884280605, -0.004528922552274606, -0.005471681673197401, -0.006451498305277336, -0.0074521650400450985, -0.008454911336315004, -0.0094389062203293, -0.010381922093328628, -0.011261134326336937, -0.012054019059648705, -0.012739301373478892, -0.013297898873999249, -0.013713802630057077, -0.013974838835556962, -0.014073260665380753, -0.014006130178820079, -0.013775463999780099, -0.013388132694088471, -0.012855520849033911, -0.012192971320157493, -0.011419051494620042, -0.010554690502106459, -0.009622243207138071, -0.00864453909921086, -0.007643971882414214, -0.006641679117210857, -0.00565685151314675, -0.00470619949672845, -0.0038035916907002924, -0.0029598671339553695, -0.0021828115051823033, -0.0014772781184435267, -0.000845427576943933, -0.0002870559351681382] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_31": {
            "samples": [0.0003798576395459785, 0.00043578666200400735, 0.0004935296633211693, 0.0005515554982505122, 0.0006080287141733543, 0.0006608525432248669, 0.0007077364436294015, 0.0007462873610355451, 0.0007741217179457732, 0.000788992915208048, 0.0007889270697455971, 0.0007723580575993246, 0.0007382519077163814, 0.0006862103827387051, 0.0006165442994707075, 0.0005303088013655113, 0.00042929531097465857, 0.00031597807114201563, 0.00019341675095889237, 6.512020720763538e-05, -6.512020720763538e-05, -0.00019341675095889237, -0.00031597807114201563, -0.00042929531097465857, -0.0005303088013655113, -0.0006165442994707075, -0.0006862103827387051, -0.0007382519077163814, -0.0007723580575993246, -0.0007889270697455971, -0.000788992915208048, -0.0007741217179457732, -0.0007462873610355451, -0.0007077364436294015, -0.0006608525432248669, -0.0006080287141733543, -0.0005515554982505122, -0.0004935296633211693, -0.00043578666200400735, -0.0003798576395459785] + [0.0] * 65 + [-0.000345537422368566, -0.0007237455283559927, -0.001149337124578956, -0.0016217826115637831, -0.0021389217498052203, -0.0026967740303955553, -0.003289415745753083, -0.00390894252563204, -0.004545532613031835, -0.005187620832681912, -0.005822186296327276, -0.006435148841109963, -0.007011860634169727, -0.0075376710491289415, -0.0079985356337942, -0.008381634516400987, -0.008675962590192954, -0.008872853716940661, -0.008966404172880884, -0.008953766494256932, -0.008835293328522908, -0.008614521158764755, -0.008297994944280974, -0.007894945810504676, -0.007416843935897088, -0.00687685684765856, -0.0062892487868441305, -0.005668759247261235, -0.0050299981499855335, -0.004386891608335708, -0.003752206352068048, -0.0031371732953768255, -0.0025512222418611055, -0.002001831129893864, -0.0014944852749314594, -0.0010327353644391099, -0.0006183379243041833, -0.00025145881453495606, 6.908096354474324e-05, 0.000345537422368566] + [0.0] * 65 + [-0.00024877844843592897, -0.0008809232750019347, -0.0015974588866745018, -0.0023989529285996527, -0.003283310730567758, -0.004245387322252834, -0.0052766962467049325, -0.00636525014079363, -0.007495563863613575, -0.00864884349578462, -0.009803374023827678, -0.01093510553730387, -0.012018423211070378, -0.013027071404044587, -0.01393518823342121, -0.014718395368408303, -0.015354879800335775, -0.015826400984703858, -0.016119158610248246, -0.016224463430565102, -0.016139165664116047, -0.01586581149177205, -0.015412516802343094, -0.014792566921686047, -0.014023769871586302, -0.013127607085927803, -0.012128238069943922, -0.011051423235100088, -0.009923431587893725, -0.008769997137818482, -0.007615380362032692, -0.006481579781991362, -0.005387724918514697, -0.0043496669809087755, -0.0033797689787864516, -0.002486883730719407, -0.00167649742529545, -0.0009510085794230902, -0.000310107693922608, 0.00024877844843592897] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_31": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_31": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_31": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 62,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_32": {
            "samples": [0.0, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271] + [0.0] * 66 + [0.00015778376362709118, -0.000535823646241926, -0.001328831114714337, -0.0022237650156902507, -0.003220313321556805, -0.004314806824009116, -0.005499787323106856, -0.00676370587553009, -0.008090791755457433, -0.009461126481233454, -0.01085094709073768, -0.012233189208447764, -0.013578264158704062, -0.01485504664661625, -0.016032031846637824, -0.017078604759892795, -0.01796635205879739, -0.018670338762580556, -0.01917027003166739, -0.019451462661092028, -0.019505561409210812, -0.01933095140141051, -0.018932838204992752, -0.018322990034824432, -0.017519159903993792, -0.01654422731086274, -0.015425117354989585, -0.014191568472623336, -0.012874827277601197, -0.011506349901330282, -0.010116583993081482, -0.00873389498912647, -0.007383685659073527, -0.006087740851514874, -0.00486381145425525, -0.0037254344455140884, -0.002681970897594845, -0.0017388319130844836, -0.0008978543256915443, -0.00015778376362709118] + [0.0] * 107,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_32": {
            "samples": [0.0003798576395459785, 0.00043578666200400735, 0.0004935296633211693, 0.0005515554982505122, 0.0006080287141733543, 0.0006608525432248669, 0.0007077364436294015, 0.0007462873610355451, 0.0007741217179457732, 0.000788992915208048, 0.0007889270697455971, 0.0007723580575993246, 0.0007382519077163814, 0.0006862103827387051, 0.0006165442994707075, 0.0005303088013655113, 0.00042929531097465857, 0.00031597807114201563, 0.00019341675095889237, 6.512020720763538e-05, -6.512020720763538e-05, -0.00019341675095889237, -0.00031597807114201563, -0.00042929531097465857, -0.0005303088013655113, -0.0006165442994707075, -0.0006862103827387051, -0.0007382519077163814, -0.0007723580575993246, -0.0007889270697455971, -0.000788992915208048, -0.0007741217179457732, -0.0007462873610355451, -0.0007077364436294015, -0.0006608525432248669, -0.0006080287141733543, -0.0005515554982505122, -0.0004935296633211693, -0.00043578666200400735, -0.0003798576395459785] + [0.0] * 65 + [-0.000345537422368566, -0.0007237455283559927, -0.001149337124578956, -0.0016217826115637831, -0.0021389217498052203, -0.0026967740303955553, -0.003289415745753083, -0.00390894252563204, -0.004545532613031835, -0.005187620832681912, -0.005822186296327276, -0.006435148841109963, -0.007011860634169727, -0.0075376710491289415, -0.0079985356337942, -0.008381634516400987, -0.008675962590192954, -0.008872853716940661, -0.008966404172880884, -0.008953766494256932, -0.008835293328522908, -0.008614521158764755, -0.008297994944280974, -0.007894945810504676, -0.007416843935897088, -0.00687685684765856, -0.0062892487868441305, -0.005668759247261235, -0.0050299981499855335, -0.004386891608335708, -0.003752206352068048, -0.0031371732953768255, -0.0025512222418611055, -0.002001831129893864, -0.0014944852749314594, -0.0010327353644391099, -0.0006183379243041833, -0.00025145881453495606, 6.908096354474324e-05, 0.000345537422368566] + [0.0] * 107,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_32": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_32": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_32": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 62,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_33": {
            "samples": [0.0, 0.0015760768444548542, 0.00337235610740649, 0.005392994053965991, 0.0076356283889478915, 0.010090276907130893, 0.012738449776040096, 0.015552569435837084, 0.018495784766494085, 0.0215222502891611, 0.024577916926684592, 0.027601849347301578, 0.030528048168025384, 0.033287716114425325, 0.03581186901257599, 0.03803415887258986, 0.03989375082406045, 0.04133808125447058, 0.04232532323982649] + [0.04282639809501372] * 2 + [0.04232532323982649, 0.04133808125447058, 0.03989375082406045, 0.03803415887258986, 0.03581186901257599, 0.033287716114425325, 0.030528048168025384, 0.027601849347301578, 0.024577916926684592, 0.0215222502891611, 0.018495784766494085, 0.015552569435837084, 0.012738449776040096, 0.010090276907130893, 0.0076356283889478915, 0.005392994053965991, 0.00337235610740649, 0.0015760768444548542] + [0.0] * 66 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0.0] * 65 + [-0.000287055935168138, 0.00018678531325335443, 0.0007313638374660268, 0.0013491977358940609, 0.002040900484424626, 0.0028047877965340718, 0.0036365358884280644, 0.004528922552274611, 0.005471681673197407, 0.006451498305277343, 0.007452165040045105, 0.008454911336315011, 0.00943890622032931, 0.010381922093328638, 0.011261134326336946, 0.012054019059648716, 0.012739301373478904, 0.01329789887399926, 0.013713802630057087, 0.013974838835556974, 0.014073260665380765, 0.01400613017882009, 0.013775463999780111, 0.013388132694088483, 0.012855520849033922, 0.012192971320157502, 0.01141905149462005, 0.010554690502106466, 0.009622243207138078, 0.008644539099210865, 0.007643971882414219, 0.006641679117210862, 0.0056568515131467535, 0.004706199496728454, 0.003803591690700295, 0.0029598671339553712, 0.0021828115051823046, 0.0014772781184435274, 0.0008454275769439332, 0.000287055935168138] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_33": {
            "samples": [0.000759715279091957, 0.0008715733240080147, 0.0009870593266423386, 0.0011031109965010243, 0.0012160574283467086, 0.0013217050864497337, 0.001415472887258803, 0.0014925747220710902, 0.0015482434358915463, 0.001577985830416096, 0.0015778541394911943, 0.0015447161151986492, 0.0014765038154327629, 0.0013724207654774103, 0.001233088598941415, 0.0010606176027310227, 0.0008585906219493171, 0.0006319561422840313, 0.00038683350191778473, 0.00013024041441527076, -0.00013024041441527076, -0.00038683350191778473, -0.0006319561422840313, -0.0008585906219493171, -0.0010606176027310227, -0.001233088598941415, -0.0013724207654774103, -0.0014765038154327629, -0.0015447161151986492, -0.0015778541394911943, -0.001577985830416096, -0.0015482434358915463, -0.0014925747220710902, -0.001415472887258803, -0.0013217050864497337, -0.0012160574283467086, -0.0011031109965010243, -0.0009870593266423386, -0.0008715733240080147, -0.000759715279091957] + [0.0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0.0] * 65 + [0.0002487784484359292, 0.0008809232750019345, 0.0015974588866745011, 0.0023989529285996514, 0.0032833107305677563, 0.004245387322252832, 0.005276696246704929, 0.006365250140793626, 0.00749556386361357, 0.008648843495784615, 0.009803374023827673, 0.010935105537303863, 0.01201842321107037, 0.013027071404044578, 0.0139351882334212, 0.014718395368408292, 0.015354879800335765, 0.015826400984703844, 0.016119158610248235, 0.016224463430565092, 0.016139165664116037, 0.01586581149177204, 0.015412516802343082, 0.014792566921686037, 0.014023769871586291, 0.013127607085927792, 0.012128238069943913, 0.01105142323510008, 0.009923431587893718, 0.008769997137818474, 0.007615380362032686, 0.0064815797819913566, 0.005387724918514691, 0.004349666980908772, 0.0033797689787864486, 0.0024868837307194043, 0.001676497425295448, 0.000951008579423089, 0.0003101076939226073, -0.0002487784484359292] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_33": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_33": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_33": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 62,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_34": {
            "samples": [0.0, 0.0015760768444548542, 0.00337235610740649, 0.005392994053965991, 0.0076356283889478915, 0.010090276907130893, 0.012738449776040096, 0.015552569435837084, 0.018495784766494085, 0.0215222502891611, 0.024577916926684592, 0.027601849347301578, 0.030528048168025384, 0.033287716114425325, 0.03581186901257599, 0.03803415887258986, 0.03989375082406045, 0.04133808125447058, 0.04232532323982649] + [0.04282639809501372] * 2 + [0.04232532323982649, 0.04133808125447058, 0.03989375082406045, 0.03803415887258986, 0.03581186901257599, 0.033287716114425325, 0.030528048168025384, 0.027601849347301578, 0.024577916926684592, 0.0215222502891611, 0.018495784766494085, 0.015552569435837084, 0.012738449776040096, 0.010090276907130893, 0.0076356283889478915, 0.005392994053965991, 0.00337235610740649, 0.0015760768444548542] + [0.0] * 66 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0.0] * 65 + [0.000287055935168138, -0.00018678531325335454, -0.000731363837466027, -0.0013491977358940613, -0.0020409004844246263, -0.002804787796534072, -0.0036365358884280653, -0.004528922552274612, -0.005471681673197408, -0.006451498305277344, -0.007452165040045105, -0.008454911336315013, -0.009438906220329312, -0.01038192209332864, -0.011261134326336948, -0.012054019059648717, -0.012739301373478906, -0.013297898873999263, -0.01371380263005709, -0.013974838835556978, -0.014073260665380768, -0.014006130178820093, -0.013775463999780113, -0.013388132694088485, -0.012855520849033924, -0.012192971320157503, -0.011419051494620051, -0.010554690502106468, -0.00962224320713808, -0.008644539099210865, -0.00764397188241422, -0.006641679117210864, -0.005656851513146754, -0.004706199496728455, -0.0038035916907002954, -0.0029598671339553717, -0.002182811505182305, -0.0014772781184435274, -0.0008454275769439333, -0.000287055935168138] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_34": {
            "samples": [0.000759715279091957, 0.0008715733240080147, 0.0009870593266423386, 0.0011031109965010243, 0.0012160574283467086, 0.0013217050864497337, 0.001415472887258803, 0.0014925747220710902, 0.0015482434358915463, 0.001577985830416096, 0.0015778541394911943, 0.0015447161151986492, 0.0014765038154327629, 0.0013724207654774103, 0.001233088598941415, 0.0010606176027310227, 0.0008585906219493171, 0.0006319561422840313, 0.00038683350191778473, 0.00013024041441527076, -0.00013024041441527076, -0.00038683350191778473, -0.0006319561422840313, -0.0008585906219493171, -0.0010606176027310227, -0.001233088598941415, -0.0013724207654774103, -0.0014765038154327629, -0.0015447161151986492, -0.0015778541394911943, -0.001577985830416096, -0.0015482434358915463, -0.0014925747220710902, -0.001415472887258803, -0.0013217050864497337, -0.0012160574283467086, -0.0011031109965010243, -0.0009870593266423386, -0.0008715733240080147, -0.000759715279091957] + [0.0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0.0] * 65 + [-0.00024877844843592924, -0.0008809232750019345, -0.0015974588866745014, -0.0023989529285996514, -0.0032833107305677563, -0.004245387322252832, -0.005276696246704929, -0.006365250140793626, -0.00749556386361357, -0.008648843495784615, -0.009803374023827673, -0.010935105537303863, -0.01201842321107037, -0.013027071404044578, -0.0139351882334212, -0.014718395368408294, -0.015354879800335765, -0.015826400984703844, -0.016119158610248235, -0.016224463430565092, -0.016139165664116037, -0.01586581149177204, -0.015412516802343082, -0.014792566921686037, -0.01402376987158629, -0.013127607085927792, -0.012128238069943913, -0.01105142323510008, -0.009923431587893718, -0.008769997137818474, -0.007615380362032686, -0.0064815797819913566, -0.005387724918514691, -0.004349666980908772, -0.0033797689787864486, -0.0024868837307194043, -0.001676497425295448, -0.0009510085794230889, -0.00031010769392260726, 0.00024877844843592924] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_34": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_34": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_34": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 62,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_35": {
            "samples": [0.0, 0.0015760768444548542, 0.00337235610740649, 0.005392994053965991, 0.0076356283889478915, 0.010090276907130893, 0.012738449776040096, 0.015552569435837084, 0.018495784766494085, 0.0215222502891611, 0.024577916926684592, 0.027601849347301578, 0.030528048168025384, 0.033287716114425325, 0.03581186901257599, 0.03803415887258986, 0.03989375082406045, 0.04133808125447058, 0.04232532323982649] + [0.04282639809501372] * 2 + [0.04232532323982649, 0.04133808125447058, 0.03989375082406045, 0.03803415887258986, 0.03581186901257599, 0.033287716114425325, 0.030528048168025384, 0.027601849347301578, 0.024577916926684592, 0.0215222502891611, 0.018495784766494085, 0.015552569435837084, 0.012738449776040096, 0.010090276907130893, 0.0076356283889478915, 0.005392994053965991, 0.00337235610740649, 0.0015760768444548542] + [0.0] * 66 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0.0] * 107,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_35": {
            "samples": [0.000759715279091957, 0.0008715733240080147, 0.0009870593266423386, 0.0011031109965010243, 0.0012160574283467086, 0.0013217050864497337, 0.001415472887258803, 0.0014925747220710902, 0.0015482434358915463, 0.001577985830416096, 0.0015778541394911943, 0.0015447161151986492, 0.0014765038154327629, 0.0013724207654774103, 0.001233088598941415, 0.0010606176027310227, 0.0008585906219493171, 0.0006319561422840313, 0.00038683350191778473, 0.00013024041441527076, -0.00013024041441527076, -0.00038683350191778473, -0.0006319561422840313, -0.0008585906219493171, -0.0010606176027310227, -0.001233088598941415, -0.0013724207654774103, -0.0014765038154327629, -0.0015447161151986492, -0.0015778541394911943, -0.001577985830416096, -0.0015482434358915463, -0.0014925747220710902, -0.001415472887258803, -0.0013217050864497337, -0.0012160574283467086, -0.0011031109965010243, -0.0009870593266423386, -0.0008715733240080147, -0.000759715279091957] + [0.0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0.0] * 107,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_35": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_35": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_35": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 62,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_36": {
            "samples": [4.651914424016516e-20, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271, -4.651914424016516e-20] + [0.0] * 65 + [-0.00015778376362709108, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009116, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.00486381145425525, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709108] + [0.0] * 65 + [0.00028705593516813806, -0.00018678531325335427, -0.0007313638374660265, -0.0013491977358940606, -0.0020409004844246254, -0.002804787796534071, -0.0036365358884280635, -0.00452892255227461, -0.005471681673197406, -0.0064514983052773416, -0.007452165040045104, -0.00845491133631501, -0.009438906220329309, -0.010381922093328637, -0.011261134326336944, -0.012054019059648714, -0.0127393013734789, -0.013297898873999259, -0.013713802630057085, -0.013974838835556972, -0.014073260665380763, -0.014006130178820088, -0.01377546399978011, -0.01338813269408848, -0.01285552084903392, -0.0121929713201575, -0.011419051494620048, -0.010554690502106464, -0.009622243207138077, -0.008644539099210863, -0.0076439718824142175, -0.006641679117210861, -0.005656851513146753, -0.004706199496728453, -0.003803591690700294, -0.002959867133955371, -0.0021828115051823046, -0.0014772781184435272, -0.0008454275769439331, -0.00028705593516813806] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_36": {
            "samples": [-0.0003798576395459785, -0.00043578666200400746, -0.0004935296633211695, -0.0005515554982505125, -0.0006080287141733547, -0.0006608525432248675, -0.0007077364436294022, -0.0007462873610355461, -0.0007741217179457742, -0.0007889929152080493, -0.0007889270697455987, -0.0007723580575993264, -0.0007382519077163833, -0.0006862103827387072, -0.0006165442994707096, -0.0005303088013655136, -0.000429295310974661, -0.0003159780711420182, -0.00019341675095889497, -6.5120207207638e-05, 6.512020720763277e-05, 0.00019341675095888976, 0.0003159780711420131, 0.00042929531097465613, 0.0005303088013655091, 0.0006165442994707053, 0.0006862103827387031, 0.0007382519077163796, 0.0007723580575993229, 0.0007889270697455956, 0.0007889929152080467, 0.0007741217179457721, 0.0007462873610355441, 0.0007077364436294007, 0.0006608525432248662, 0.0006080287141733539, 0.0005515554982505118, 0.0004935296633211691, 0.00043578666200400724, 0.0003798576395459785] + [0.0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789557, 0.0016217826115637823, 0.002138921749805219, 0.002696774030395554, 0.003289415745753081, 0.003908942525632038, 0.0045455326130318325, 0.005187620832681909, 0.005822186296327273, 0.006435148841109959, 0.007011860634169723, 0.007537671049128937, 0.007998535633794195, 0.008381634516400982, 0.008675962590192949, 0.008872853716940654, 0.008966404172880879, 0.008953766494256927, 0.008835293328522903, 0.00861452115876475, 0.008297994944280967, 0.00789494581050467, 0.007416843935897083, 0.006876856847658555, 0.006289248786844126, 0.00566875924726123, 0.00502999814998553, 0.004386891608335704, 0.003752206352068045, 0.0031371732953768224, 0.0025512222418611033, 0.002001831129893862, 0.001494485274931458, 0.0010327353644391088, 0.0006183379243041826, 0.0002514588145349556, -6.908096354474351e-05, -0.00034553742236856605] + [0.0] * 65 + [-0.0002487784484359292, -0.0008809232750019345, -0.0015974588866745014, -0.002398952928599652, -0.0032833107305677567, -0.004245387322252832, -0.00527669624670493, -0.006365250140793627, -0.007495563863613571, -0.008648843495784616, -0.009803374023827674, -0.010935105537303865, -0.012018423211070372, -0.01302707140404458, -0.013935188233421202, -0.014718395368408294, -0.015354879800335767, -0.015826400984703847, -0.01611915861024824, -0.016224463430565095, -0.01613916566411604, -0.015865811491772044, -0.015412516802343084, -0.014792566921686038, -0.014023769871586293, -0.013127607085927794, -0.012128238069943915, -0.011051423235100081, -0.00992343158789372, -0.008769997137818475, -0.007615380362032688, -0.006481579781991357, -0.005387724918514692, -0.004349666980908773, -0.003379768978786449, -0.0024868837307194048, -0.0016764974252954485, -0.0009510085794230893, -0.0003101076939226075, 0.0002487784484359292] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_36": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_36": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_36": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 62,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_37": {
            "samples": [4.651914424016516e-20, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271, -4.651914424016516e-20] + [0.0] * 65 + [-0.00015778376362709108, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009116, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.00486381145425525, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709108] + [0.0] * 65 + [-0.000287055935168138, 0.00018678531325335443, 0.0007313638374660268, 0.0013491977358940609, 0.002040900484424626, 0.0028047877965340718, 0.0036365358884280644, 0.004528922552274611, 0.005471681673197407, 0.006451498305277343, 0.007452165040045105, 0.008454911336315011, 0.00943890622032931, 0.010381922093328638, 0.011261134326336946, 0.012054019059648716, 0.012739301373478904, 0.01329789887399926, 0.013713802630057087, 0.013974838835556974, 0.014073260665380765, 0.01400613017882009, 0.013775463999780111, 0.013388132694088483, 0.012855520849033922, 0.012192971320157502, 0.01141905149462005, 0.010554690502106466, 0.009622243207138078, 0.008644539099210865, 0.007643971882414219, 0.006641679117210862, 0.0056568515131467535, 0.004706199496728454, 0.003803591690700295, 0.0029598671339553712, 0.0021828115051823046, 0.0014772781184435274, 0.0008454275769439332, 0.000287055935168138] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_37": {
            "samples": [-0.0003798576395459785, -0.00043578666200400746, -0.0004935296633211695, -0.0005515554982505125, -0.0006080287141733547, -0.0006608525432248675, -0.0007077364436294022, -0.0007462873610355461, -0.0007741217179457742, -0.0007889929152080493, -0.0007889270697455987, -0.0007723580575993264, -0.0007382519077163833, -0.0006862103827387072, -0.0006165442994707096, -0.0005303088013655136, -0.000429295310974661, -0.0003159780711420182, -0.00019341675095889497, -6.5120207207638e-05, 6.512020720763277e-05, 0.00019341675095888976, 0.0003159780711420131, 0.00042929531097465613, 0.0005303088013655091, 0.0006165442994707053, 0.0006862103827387031, 0.0007382519077163796, 0.0007723580575993229, 0.0007889270697455956, 0.0007889929152080467, 0.0007741217179457721, 0.0007462873610355441, 0.0007077364436294007, 0.0006608525432248662, 0.0006080287141733539, 0.0005515554982505118, 0.0004935296633211691, 0.00043578666200400724, 0.0003798576395459785] + [0.0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789557, 0.0016217826115637823, 0.002138921749805219, 0.002696774030395554, 0.003289415745753081, 0.003908942525632038, 0.0045455326130318325, 0.005187620832681909, 0.005822186296327273, 0.006435148841109959, 0.007011860634169723, 0.007537671049128937, 0.007998535633794195, 0.008381634516400982, 0.008675962590192949, 0.008872853716940654, 0.008966404172880879, 0.008953766494256927, 0.008835293328522903, 0.00861452115876475, 0.008297994944280967, 0.00789494581050467, 0.007416843935897083, 0.006876856847658555, 0.006289248786844126, 0.00566875924726123, 0.00502999814998553, 0.004386891608335704, 0.003752206352068045, 0.0031371732953768224, 0.0025512222418611033, 0.002001831129893862, 0.001494485274931458, 0.0010327353644391088, 0.0006183379243041826, 0.0002514588145349556, -6.908096354474351e-05, -0.00034553742236856605] + [0.0] * 65 + [0.0002487784484359292, 0.0008809232750019345, 0.0015974588866745011, 0.0023989529285996514, 0.0032833107305677563, 0.004245387322252832, 0.005276696246704929, 0.006365250140793626, 0.00749556386361357, 0.008648843495784615, 0.009803374023827673, 0.010935105537303863, 0.01201842321107037, 0.013027071404044578, 0.0139351882334212, 0.014718395368408292, 0.015354879800335765, 0.015826400984703844, 0.016119158610248235, 0.016224463430565092, 0.016139165664116037, 0.01586581149177204, 0.015412516802343082, 0.014792566921686037, 0.014023769871586291, 0.013127607085927792, 0.012128238069943913, 0.01105142323510008, 0.009923431587893718, 0.008769997137818474, 0.007615380362032686, 0.0064815797819913566, 0.005387724918514691, 0.004349666980908772, 0.0033797689787864486, 0.0024868837307194043, 0.001676497425295448, 0.000951008579423089, 0.0003101076939226073, -0.0002487784484359292] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_37": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_37": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_37": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 62,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_38": {
            "samples": [4.651914424016516e-20, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271, -4.651914424016516e-20] + [0.0] * 65 + [-0.00015778376362709108, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009116, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.00486381145425525, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709108] + [0.0] * 107,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_38": {
            "samples": [-0.0003798576395459785, -0.00043578666200400746, -0.0004935296633211695, -0.0005515554982505125, -0.0006080287141733547, -0.0006608525432248675, -0.0007077364436294022, -0.0007462873610355461, -0.0007741217179457742, -0.0007889929152080493, -0.0007889270697455987, -0.0007723580575993264, -0.0007382519077163833, -0.0006862103827387072, -0.0006165442994707096, -0.0005303088013655136, -0.000429295310974661, -0.0003159780711420182, -0.00019341675095889497, -6.5120207207638e-05, 6.512020720763277e-05, 0.00019341675095888976, 0.0003159780711420131, 0.00042929531097465613, 0.0005303088013655091, 0.0006165442994707053, 0.0006862103827387031, 0.0007382519077163796, 0.0007723580575993229, 0.0007889270697455956, 0.0007889929152080467, 0.0007741217179457721, 0.0007462873610355441, 0.0007077364436294007, 0.0006608525432248662, 0.0006080287141733539, 0.0005515554982505118, 0.0004935296633211691, 0.00043578666200400724, 0.0003798576395459785] + [0.0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789557, 0.0016217826115637823, 0.002138921749805219, 0.002696774030395554, 0.003289415745753081, 0.003908942525632038, 0.0045455326130318325, 0.005187620832681909, 0.005822186296327273, 0.006435148841109959, 0.007011860634169723, 0.007537671049128937, 0.007998535633794195, 0.008381634516400982, 0.008675962590192949, 0.008872853716940654, 0.008966404172880879, 0.008953766494256927, 0.008835293328522903, 0.00861452115876475, 0.008297994944280967, 0.00789494581050467, 0.007416843935897083, 0.006876856847658555, 0.006289248786844126, 0.00566875924726123, 0.00502999814998553, 0.004386891608335704, 0.003752206352068045, 0.0031371732953768224, 0.0025512222418611033, 0.002001831129893862, 0.001494485274931458, 0.0010327353644391088, 0.0006183379243041826, 0.0002514588145349556, -6.908096354474351e-05, -0.00034553742236856605] + [0.0] * 107,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_38": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_38": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_38": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 62,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_39": {
            "samples": [4.651914424016516e-20, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271, -4.651914424016516e-20] + [0.0] * 65 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0.0] * 65 + [-0.000287055935168138, 0.00018678531325335443, 0.0007313638374660268, 0.0013491977358940609, 0.002040900484424626, 0.0028047877965340718, 0.0036365358884280644, 0.004528922552274611, 0.005471681673197407, 0.006451498305277343, 0.007452165040045105, 0.008454911336315011, 0.00943890622032931, 0.010381922093328638, 0.011261134326336946, 0.012054019059648716, 0.012739301373478904, 0.01329789887399926, 0.013713802630057087, 0.013974838835556974, 0.014073260665380765, 0.01400613017882009, 0.013775463999780111, 0.013388132694088483, 0.012855520849033922, 0.012192971320157502, 0.01141905149462005, 0.010554690502106466, 0.009622243207138078, 0.008644539099210865, 0.007643971882414219, 0.006641679117210862, 0.0056568515131467535, 0.004706199496728454, 0.003803591690700295, 0.0029598671339553712, 0.0021828115051823046, 0.0014772781184435274, 0.0008454275769439332, 0.000287055935168138] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_39": {
            "samples": [-0.0003798576395459785, -0.00043578666200400746, -0.0004935296633211695, -0.0005515554982505125, -0.0006080287141733547, -0.0006608525432248675, -0.0007077364436294022, -0.0007462873610355461, -0.0007741217179457742, -0.0007889929152080493, -0.0007889270697455987, -0.0007723580575993264, -0.0007382519077163833, -0.0006862103827387072, -0.0006165442994707096, -0.0005303088013655136, -0.000429295310974661, -0.0003159780711420182, -0.00019341675095889497, -6.5120207207638e-05, 6.512020720763277e-05, 0.00019341675095888976, 0.0003159780711420131, 0.00042929531097465613, 0.0005303088013655091, 0.0006165442994707053, 0.0006862103827387031, 0.0007382519077163796, 0.0007723580575993229, 0.0007889270697455956, 0.0007889929152080467, 0.0007741217179457721, 0.0007462873610355441, 0.0007077364436294007, 0.0006608525432248662, 0.0006080287141733539, 0.0005515554982505118, 0.0004935296633211691, 0.00043578666200400724, 0.0003798576395459785] + [0.0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0.0] * 65 + [0.0002487784484359292, 0.0008809232750019345, 0.0015974588866745011, 0.0023989529285996514, 0.0032833107305677563, 0.004245387322252832, 0.005276696246704929, 0.006365250140793626, 0.00749556386361357, 0.008648843495784615, 0.009803374023827673, 0.010935105537303863, 0.01201842321107037, 0.013027071404044578, 0.0139351882334212, 0.014718395368408292, 0.015354879800335765, 0.015826400984703844, 0.016119158610248235, 0.016224463430565092, 0.016139165664116037, 0.01586581149177204, 0.015412516802343082, 0.014792566921686037, 0.014023769871586291, 0.013127607085927792, 0.012128238069943913, 0.01105142323510008, 0.009923431587893718, 0.008769997137818474, 0.007615380362032686, 0.0064815797819913566, 0.005387724918514691, 0.004349666980908772, 0.0033797689787864486, 0.0024868837307194043, 0.001676497425295448, 0.000951008579423089, 0.0003101076939226073, -0.0002487784484359292] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_39": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_39": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_39": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 62,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_40": {
            "samples": [4.651914424016516e-20, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271, -4.651914424016516e-20] + [0.0] * 65 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0.0] * 65 + [0.000287055935168138, -0.00018678531325335454, -0.000731363837466027, -0.0013491977358940613, -0.0020409004844246263, -0.002804787796534072, -0.0036365358884280653, -0.004528922552274612, -0.005471681673197408, -0.006451498305277344, -0.007452165040045105, -0.008454911336315013, -0.009438906220329312, -0.01038192209332864, -0.011261134326336948, -0.012054019059648717, -0.012739301373478906, -0.013297898873999263, -0.01371380263005709, -0.013974838835556978, -0.014073260665380768, -0.014006130178820093, -0.013775463999780113, -0.013388132694088485, -0.012855520849033924, -0.012192971320157503, -0.011419051494620051, -0.010554690502106468, -0.00962224320713808, -0.008644539099210865, -0.00764397188241422, -0.006641679117210864, -0.005656851513146754, -0.004706199496728455, -0.0038035916907002954, -0.0029598671339553717, -0.002182811505182305, -0.0014772781184435274, -0.0008454275769439333, -0.000287055935168138] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_40": {
            "samples": [-0.0003798576395459785, -0.00043578666200400746, -0.0004935296633211695, -0.0005515554982505125, -0.0006080287141733547, -0.0006608525432248675, -0.0007077364436294022, -0.0007462873610355461, -0.0007741217179457742, -0.0007889929152080493, -0.0007889270697455987, -0.0007723580575993264, -0.0007382519077163833, -0.0006862103827387072, -0.0006165442994707096, -0.0005303088013655136, -0.000429295310974661, -0.0003159780711420182, -0.00019341675095889497, -6.5120207207638e-05, 6.512020720763277e-05, 0.00019341675095888976, 0.0003159780711420131, 0.00042929531097465613, 0.0005303088013655091, 0.0006165442994707053, 0.0006862103827387031, 0.0007382519077163796, 0.0007723580575993229, 0.0007889270697455956, 0.0007889929152080467, 0.0007741217179457721, 0.0007462873610355441, 0.0007077364436294007, 0.0006608525432248662, 0.0006080287141733539, 0.0005515554982505118, 0.0004935296633211691, 0.00043578666200400724, 0.0003798576395459785] + [0.0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0.0] * 65 + [-0.00024877844843592924, -0.0008809232750019345, -0.0015974588866745014, -0.0023989529285996514, -0.0032833107305677563, -0.004245387322252832, -0.005276696246704929, -0.006365250140793626, -0.00749556386361357, -0.008648843495784615, -0.009803374023827673, -0.010935105537303863, -0.01201842321107037, -0.013027071404044578, -0.0139351882334212, -0.014718395368408294, -0.015354879800335765, -0.015826400984703844, -0.016119158610248235, -0.016224463430565092, -0.016139165664116037, -0.01586581149177204, -0.015412516802343082, -0.014792566921686037, -0.01402376987158629, -0.013127607085927792, -0.012128238069943913, -0.01105142323510008, -0.009923431587893718, -0.008769997137818474, -0.007615380362032686, -0.0064815797819913566, -0.005387724918514691, -0.004349666980908772, -0.0033797689787864486, -0.0024868837307194043, -0.001676497425295448, -0.0009510085794230889, -0.00031010769392260726, 0.00024877844843592924] + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_40": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_40": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_40": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 62,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_41": {
            "samples": [4.651914424016516e-20, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271, -4.651914424016516e-20] + [0.0] * 65 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0.0] * 107,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_41": {
            "samples": [-0.0003798576395459785, -0.00043578666200400746, -0.0004935296633211695, -0.0005515554982505125, -0.0006080287141733547, -0.0006608525432248675, -0.0007077364436294022, -0.0007462873610355461, -0.0007741217179457742, -0.0007889929152080493, -0.0007889270697455987, -0.0007723580575993264, -0.0007382519077163833, -0.0006862103827387072, -0.0006165442994707096, -0.0005303088013655136, -0.000429295310974661, -0.0003159780711420182, -0.00019341675095889497, -6.5120207207638e-05, 6.512020720763277e-05, 0.00019341675095888976, 0.0003159780711420131, 0.00042929531097465613, 0.0005303088013655091, 0.0006165442994707053, 0.0006862103827387031, 0.0007382519077163796, 0.0007723580575993229, 0.0007889270697455956, 0.0007889929152080467, 0.0007741217179457721, 0.0007462873610355441, 0.0007077364436294007, 0.0006608525432248662, 0.0006080287141733539, 0.0005515554982505118, 0.0004935296633211691, 0.00043578666200400724, 0.0003798576395459785] + [0.0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0.0] * 107,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_41": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_41": {
            "samples": [0.0] * 252,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_41": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 62,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_42": {
            "samples": [0.0] * 105 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0.0] * 65 + [0.00028705593516813795, -0.0001867853132533546, -0.0007313638374660274, -0.0013491977358940617, -0.0020409004844246267, -0.0028047877965340726, -0.003636535888428066, -0.004528922552274613, -0.00547168167319741, -0.006451498305277346, -0.007452165040045108, -0.008454911336315015, -0.009438906220329314, -0.010381922093328642, -0.011261134326336951, -0.012054019059648721, -0.012739301373478907, -0.013297898873999268, -0.013713802630057092, -0.01397483883555698, -0.01407326066538077, -0.014006130178820094, -0.013775463999780115, -0.013388132694088487, -0.012855520849033927, -0.012192971320157507, -0.011419051494620053, -0.01055469050210647, -0.009622243207138082, -0.008644539099210867, -0.007643971882414222, -0.006641679117210864, -0.005656851513146755, -0.0047061994967284556, -0.003803591690700296, -0.002959867133955372, -0.002182811505182305, -0.0014772781184435276, -0.0008454275769439333, -0.00028705593516813795] + [0.0] * 106,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_42": {
            "samples": [0.0] * 105 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0.0] * 65 + [-0.0002487784484359293, -0.0008809232750019345, -0.0015974588866745011, -0.0023989529285996514, -0.003283310730567756, -0.004245387322252831, -0.005276696246704929, -0.006365250140793625, -0.00749556386361357, -0.008648843495784613, -0.00980337402382767, -0.010935105537303862, -0.012018423211070368, -0.013027071404044577, -0.013935188233421198, -0.014718395368408292, -0.015354879800335761, -0.015826400984703844, -0.016119158610248232, -0.01622446343056509, -0.016139165664116033, -0.015865811491772037, -0.01541251680234308, -0.014792566921686033, -0.014023769871586288, -0.01312760708592779, -0.012128238069943911, -0.011051423235100078, -0.009923431587893716, -0.008769997137818472, -0.007615380362032684, -0.006481579781991355, -0.0053877249185146905, -0.00434966698090877, -0.0033797689787864477, -0.002486883730719404, -0.001676497425295448, -0.0009510085794230887, -0.00031010769392260715, 0.0002487784484359293] + [0.0] * 106,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_42": {
            "samples": [0.0] * 356,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_42": {
            "samples": [0.0] * 356,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_42": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 61,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_43": {
            "samples": [0.0, -0.0007880384222274271, -0.001686178053703245, -0.0026964970269829957, -0.0038178141944739457, -0.005045138453565447, -0.006369224888020048, -0.007776284717918542, -0.009247892383247042, -0.01076112514458055, -0.012288958463342296, -0.013800924673650789, -0.015264024084012692, -0.016643858057212663, -0.017905934506287996, -0.01901707943629493, -0.019946875412030225, -0.02066904062723529, -0.021162661619913245] + [-0.02141319904750686] * 2 + [-0.021162661619913245, -0.02066904062723529, -0.019946875412030225, -0.01901707943629493, -0.017905934506287996, -0.016643858057212663, -0.015264024084012692, -0.013800924673650789, -0.012288958463342296, -0.01076112514458055, -0.009247892383247042, -0.007776284717918542, -0.006369224888020048, -0.005045138453565447, -0.0038178141944739457, -0.0026964970269829957, -0.001686178053703245, -0.0007880384222274271] + [0.0] * 66 + [0.00015778376362709102, -0.0005358236462419262, -0.0013288311147143374, -0.002223765015690251, -0.0032203133215568053, -0.004314806824009117, -0.005499787323106857, -0.006763705875530092, -0.008090791755457434, -0.009461126481233456, -0.010850947090737681, -0.012233189208447766, -0.013578264158704063, -0.014855046646616252, -0.016032031846637824, -0.0170786047598928, -0.017966352058797392, -0.018670338762580556, -0.019170270031667394, -0.01945146266109203, -0.019505561409210816, -0.019330951401410515, -0.018932838204992752, -0.018322990034824436, -0.017519159903993796, -0.01654422731086274, -0.015425117354989587, -0.014191568472623338, -0.012874827277601199, -0.011506349901330284, -0.010116583993081484, -0.008733894989126472, -0.007383685659073527, -0.006087740851514875, -0.004863811454255249, -0.003725434445514089, -0.0026819708975948453, -0.0017388319130844836, -0.0008978543256915441, -0.00015778376362709102] + [0.0] * 65 + [0.00028705593516813795, -0.0001867853132533546, -0.0007313638374660274, -0.0013491977358940617, -0.0020409004844246267, -0.0028047877965340726, -0.003636535888428066, -0.004528922552274613, -0.00547168167319741, -0.006451498305277346, -0.007452165040045108, -0.008454911336315015, -0.009438906220329314, -0.010381922093328642, -0.011261134326336951, -0.012054019059648721, -0.012739301373478907, -0.013297898873999268, -0.013713802630057092, -0.01397483883555698, -0.01407326066538077, -0.014006130178820094, -0.013775463999780115, -0.013388132694088487, -0.012855520849033927, -0.012192971320157507, -0.011419051494620053, -0.01055469050210647, -0.009622243207138082, -0.008644539099210867, -0.007643971882414222, -0.006641679117210864, -0.005656851513146755, -0.0047061994967284556, -0.003803591690700296, -0.002959867133955372, -0.002182811505182305, -0.0014772781184435276, -0.0008454275769439333, -0.00028705593516813795] + [0.0] * 106,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_43": {
            "samples": [-0.0003798576395459785, -0.00043578666200400735, -0.0004935296633211693, -0.0005515554982505122, -0.0006080287141733543, -0.0006608525432248669, -0.0007077364436294015, -0.0007462873610355451, -0.0007741217179457732, -0.000788992915208048, -0.0007889270697455971, -0.0007723580575993246, -0.0007382519077163814, -0.0006862103827387051, -0.0006165442994707075, -0.0005303088013655113, -0.00042929531097465857, -0.00031597807114201563, -0.00019341675095889237, -6.512020720763538e-05, 6.512020720763538e-05, 0.00019341675095889237, 0.00031597807114201563, 0.00042929531097465857, 0.0005303088013655113, 0.0006165442994707075, 0.0006862103827387051, 0.0007382519077163814, 0.0007723580575993246, 0.0007889270697455971, 0.000788992915208048, 0.0007741217179457732, 0.0007462873610355451, 0.0007077364436294015, 0.0006608525432248669, 0.0006080287141733543, 0.0005515554982505122, 0.0004935296633211693, 0.00043578666200400735, 0.0003798576395459785] + [0.0] * 65 + [-0.00034553742236856605, -0.0007237455283559925, -0.0011493371245789555, -0.0016217826115637818, -0.002138921749805219, -0.0026967740303955536, -0.003289415745753081, -0.003908942525632037, -0.004545532613031832, -0.005187620832681907, -0.005822186296327271, -0.006435148841109958, -0.007011860634169721, -0.007537671049128935, -0.007998535633794194, -0.00838163451640098, -0.008675962590192947, -0.008872853716940653, -0.008966404172880875, -0.008953766494256924, -0.008835293328522899, -0.008614521158764746, -0.008297994944280965, -0.007894945810504669, -0.007416843935897081, -0.006876856847658553, -0.0062892487868441245, -0.005668759247261229, -0.005029998149985528, -0.0043868916083357025, -0.0037522063520680432, -0.0031371732953768216, -0.0025512222418611025, -0.002001831129893861, -0.0014944852749314576, -0.0010327353644391084, -0.0006183379243041822, -0.00025145881453495536, 6.908096354474362e-05, 0.00034553742236856605] + [0.0] * 65 + [-0.0002487784484359293, -0.0008809232750019345, -0.0015974588866745011, -0.0023989529285996514, -0.003283310730567756, -0.004245387322252831, -0.005276696246704929, -0.006365250140793625, -0.00749556386361357, -0.008648843495784613, -0.00980337402382767, -0.010935105537303862, -0.012018423211070368, -0.013027071404044577, -0.013935188233421198, -0.014718395368408292, -0.015354879800335761, -0.015826400984703844, -0.016119158610248232, -0.01622446343056509, -0.016139165664116033, -0.015865811491772037, -0.01541251680234308, -0.014792566921686033, -0.014023769871586288, -0.01312760708592779, -0.012128238069943911, -0.011051423235100078, -0.009923431587893716, -0.008769997137818472, -0.007615380362032684, -0.006481579781991355, -0.0053877249185146905, -0.00434966698090877, -0.0033797689787864477, -0.002486883730719404, -0.001676497425295448, -0.0009510085794230887, -0.00031010769392260715, 0.0002487784484359293] + [0.0] * 106,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_43": {
            "samples": [0.0] * 356,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_43": {
            "samples": [0.0] * 356,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_43": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 61,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_44": {
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20] + [0.0] * 65 + [0.00015778376362709124, -0.0005358236462419259, -0.0013288311147143367, -0.0022237650156902507, -0.0032203133215568044, -0.004314806824009115, -0.0054997873231068545, -0.0067637058755300895, -0.008090791755457431, -0.009461126481233453, -0.010850947090737677, -0.012233189208447763, -0.01357826415870406, -0.014855046646616249, -0.01603203184663782, -0.017078604759892792, -0.01796635205879739, -0.018670338762580552, -0.019170270031667387, -0.019451462661092028, -0.019505561409210812, -0.019330951401410508, -0.01893283820499275, -0.018322990034824432, -0.01751915990399379, -0.016544227310862736, -0.015425117354989583, -0.014191568472623334, -0.012874827277601196, -0.01150634990133028, -0.01011658399308148, -0.008733894989126472, -0.007383685659073526, -0.006087740851514874, -0.004863811454255249, -0.003725434445514088, -0.002681970897594845, -0.0017388319130844834, -0.0008978543256915442, -0.00015778376362709124] + [0.0] * 65 + [0.00028705593516813806, -0.000186785313253354, -0.0007313638374660263, -0.00134919773589406, -0.0020409004844246246, -0.0028047877965340696, -0.0036365358884280627, -0.004528922552274608, -0.005471681673197404, -0.00645149830527734, -0.0074521650400451, -0.008454911336315008, -0.009438906220329306, -0.010381922093328633, -0.011261134326336941, -0.012054019059648709, -0.012739301373478897, -0.013297898873999254, -0.01371380263005708, -0.013974838835556967, -0.014073260665380758, -0.014006130178820082, -0.013775463999780104, -0.013388132694088476, -0.012855520849033915, -0.012192971320157496, -0.011419051494620044, -0.01055469050210646, -0.009622243207138075, -0.00864453909921086, -0.007643971882414216, -0.006641679117210859, -0.005656851513146751, -0.004706199496728452, -0.0038035916907002937, -0.00295986713395537, -0.0021828115051823038, -0.001477278118443527, -0.000845427576943933, -0.00028705593516813806] + [0.0] * 106,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_44": {
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785] + [0.0] * 65 + [-0.00034553742236856594, -0.0007237455283559927, -0.0011493371245789564, -0.0016217826115637833, -0.0021389217498052207, -0.002696774030395556, -0.0032894157457530842, -0.003908942525632041, -0.004545532613031837, -0.005187620832681913, -0.005822186296327278, -0.0064351488411099654, -0.00701186063416973, -0.007537671049128944, -0.007998535633794204, -0.00838163451640099, -0.008675962590192958, -0.008872853716940665, -0.008966404172880887, -0.008953766494256936, -0.008835293328522911, -0.008614521158764758, -0.008297994944280978, -0.00789494581050468, -0.007416843935897092, -0.006876856847658563, -0.006289248786844133, -0.005668759247261237, -0.005029998149985536, -0.0043868916083357095, -0.0037522063520680497, -0.003137173295376827, -0.002551222241861107, -0.002001831129893865, -0.0014944852749314602, -0.0010327353644391107, -0.0006183379243041838, -0.00025145881453495644, 6.908096354474308e-05, 0.00034553742236856594] + [0.0] * 65 + [-0.0002487784484359291, -0.0008809232750019345, -0.0015974588866745014, -0.0023989529285996522, -0.0032833107305677567, -0.004245387322252833, -0.005276696246704931, -0.006365250140793628, -0.007495563863613572, -0.008648843495784616, -0.009803374023827673, -0.010935105537303867, -0.012018423211070373, -0.013027071404044582, -0.013935188233421204, -0.014718395368408296, -0.015354879800335768, -0.01582640098470385, -0.01611915861024824, -0.016224463430565095, -0.01613916566411604, -0.015865811491772044, -0.015412516802343087, -0.01479256692168604, -0.014023769871586295, -0.013127607085927796, -0.012128238069943916, -0.011051423235100083, -0.009923431587893721, -0.008769997137818477, -0.007615380362032688, -0.006481579781991359, -0.005387724918514693, -0.004349666980908774, -0.0033797689787864495, -0.0024868837307194056, -0.0016764974252954491, -0.0009510085794230893, -0.0003101076939226077, 0.0002487784484359291] + [0.0] * 106,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_44": {
            "samples": [0.0] * 356,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_44": {
            "samples": [0.0] * 356,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_44": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 61,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_45": {
            "samples": [-4.651914424016516e-20, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271, 4.651914424016516e-20] + [0.0] * 65 + [-0.00015778376362709108, 0.0005358236462419262, 0.0013288311147143374, 0.002223765015690251, 0.0032203133215568053, 0.004314806824009116, 0.005499787323106857, 0.006763705875530092, 0.008090791755457434, 0.009461126481233456, 0.010850947090737681, 0.012233189208447766, 0.013578264158704063, 0.014855046646616252, 0.016032031846637824, 0.0170786047598928, 0.017966352058797392, 0.018670338762580556, 0.019170270031667394, 0.01945146266109203, 0.019505561409210816, 0.019330951401410515, 0.018932838204992752, 0.018322990034824436, 0.017519159903993796, 0.01654422731086274, 0.015425117354989587, 0.014191568472623338, 0.012874827277601199, 0.011506349901330284, 0.010116583993081484, 0.008733894989126472, 0.007383685659073527, 0.006087740851514875, 0.00486381145425525, 0.003725434445514089, 0.0026819708975948453, 0.0017388319130844836, 0.0008978543256915441, 0.00015778376362709108] + [0.0] * 65 + [-0.000287055935168138, 0.00018678531325335454, 0.000731363837466027, 0.0013491977358940613, 0.0020409004844246263, 0.002804787796534072, 0.0036365358884280653, 0.004528922552274612, 0.005471681673197408, 0.006451498305277344, 0.007452165040045105, 0.008454911336315013, 0.009438906220329312, 0.01038192209332864, 0.011261134326336948, 0.012054019059648717, 0.012739301373478906, 0.013297898873999263, 0.01371380263005709, 0.013974838835556978, 0.014073260665380768, 0.014006130178820093, 0.013775463999780113, 0.013388132694088485, 0.012855520849033924, 0.012192971320157503, 0.011419051494620051, 0.010554690502106468, 0.00962224320713808, 0.008644539099210865, 0.00764397188241422, 0.006641679117210864, 0.005656851513146754, 0.004706199496728455, 0.0038035916907002954, 0.0029598671339553717, 0.002182811505182305, 0.0014772781184435274, 0.0008454275769439333, 0.000287055935168138] + [0.0] * 106,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_45": {
            "samples": [0.0003798576395459785, 0.00043578666200400746, 0.0004935296633211695, 0.0005515554982505125, 0.0006080287141733547, 0.0006608525432248675, 0.0007077364436294022, 0.0007462873610355461, 0.0007741217179457742, 0.0007889929152080493, 0.0007889270697455987, 0.0007723580575993264, 0.0007382519077163833, 0.0006862103827387072, 0.0006165442994707096, 0.0005303088013655136, 0.000429295310974661, 0.0003159780711420182, 0.00019341675095889497, 6.5120207207638e-05, -6.512020720763277e-05, -0.00019341675095888976, -0.0003159780711420131, -0.00042929531097465613, -0.0005303088013655091, -0.0006165442994707053, -0.0006862103827387031, -0.0007382519077163796, -0.0007723580575993229, -0.0007889270697455956, -0.0007889929152080467, -0.0007741217179457721, -0.0007462873610355441, -0.0007077364436294007, -0.0006608525432248662, -0.0006080287141733539, -0.0005515554982505118, -0.0004935296633211691, -0.00043578666200400724, -0.0003798576395459785] + [0.0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789557, 0.0016217826115637823, 0.002138921749805219, 0.002696774030395554, 0.003289415745753081, 0.003908942525632038, 0.0045455326130318325, 0.005187620832681909, 0.005822186296327273, 0.006435148841109959, 0.007011860634169723, 0.007537671049128937, 0.007998535633794195, 0.008381634516400982, 0.008675962590192949, 0.008872853716940654, 0.008966404172880879, 0.008953766494256927, 0.008835293328522903, 0.00861452115876475, 0.008297994944280967, 0.00789494581050467, 0.007416843935897083, 0.006876856847658555, 0.006289248786844126, 0.00566875924726123, 0.00502999814998553, 0.004386891608335704, 0.003752206352068045, 0.0031371732953768224, 0.0025512222418611033, 0.002001831129893862, 0.001494485274931458, 0.0010327353644391088, 0.0006183379243041826, 0.0002514588145349556, -6.908096354474351e-05, -0.00034553742236856605] + [0.0] * 65 + [0.00024877844843592924, 0.0008809232750019345, 0.0015974588866745014, 0.0023989529285996514, 0.0032833107305677563, 0.004245387322252832, 0.005276696246704929, 0.006365250140793626, 0.00749556386361357, 0.008648843495784615, 0.009803374023827673, 0.010935105537303863, 0.01201842321107037, 0.013027071404044578, 0.0139351882334212, 0.014718395368408294, 0.015354879800335765, 0.015826400984703844, 0.016119158610248235, 0.016224463430565092, 0.016139165664116037, 0.01586581149177204, 0.015412516802343082, 0.014792566921686037, 0.01402376987158629, 0.013127607085927792, 0.012128238069943913, 0.01105142323510008, 0.009923431587893718, 0.008769997137818474, 0.007615380362032686, 0.0064815797819913566, 0.005387724918514691, 0.004349666980908772, 0.0033797689787864486, 0.0024868837307194043, 0.001676497425295448, 0.0009510085794230889, 0.00031010769392260726, -0.00024877844843592924] + [0.0] * 106,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_45": {
            "samples": [0.0] * 356,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_45": {
            "samples": [0.0] * 356,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_45": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 61,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_46": {
            "samples": [0.0, 0.0007880384222274271, 0.001686178053703245, 0.0026964970269829957, 0.0038178141944739457, 0.005045138453565447, 0.006369224888020048, 0.007776284717918542, 0.009247892383247042, 0.01076112514458055, 0.012288958463342296, 0.013800924673650789, 0.015264024084012692, 0.016643858057212663, 0.017905934506287996, 0.01901707943629493, 0.019946875412030225, 0.02066904062723529, 0.021162661619913245] + [0.02141319904750686] * 2 + [0.021162661619913245, 0.02066904062723529, 0.019946875412030225, 0.01901707943629493, 0.017905934506287996, 0.016643858057212663, 0.015264024084012692, 0.013800924673650789, 0.012288958463342296, 0.01076112514458055, 0.009247892383247042, 0.007776284717918542, 0.006369224888020048, 0.005045138453565447, 0.0038178141944739457, 0.0026964970269829957, 0.001686178053703245, 0.0007880384222274271] + [0.0] * 66 + [-0.000157783763627091, 0.0005358236462419265, 0.0013288311147143378, 0.0022237650156902516, 0.0032203133215568057, 0.004314806824009118, 0.005499787323106857, 0.006763705875530093, 0.008090791755457434, 0.009461126481233456, 0.010850947090737683, 0.012233189208447768, 0.013578264158704065, 0.014855046646616254, 0.016032031846637828, 0.0170786047598928, 0.017966352058797392, 0.01867033876258056, 0.019170270031667394, 0.019451462661092035, 0.01950556140921082, 0.019330951401410515, 0.018932838204992756, 0.018322990034824436, 0.017519159903993796, 0.016544227310862743, 0.015425117354989588, 0.01419156847262334, 0.0128748272776012, 0.011506349901330285, 0.010116583993081484, 0.008733894989126472, 0.007383685659073528, 0.006087740851514875, 0.00486381145425525, 0.0037254344455140893, 0.0026819708975948458, 0.0017388319130844836, 0.0008978543256915441, 0.000157783763627091] + [0.0] * 65 + [-0.0002870559351681379, 0.00018678531325335476, 0.0007313638374660276, 0.001349197735894062, 0.002040900484424627, 0.002804787796534073, 0.003636535888428067, 0.0045289225522746135, 0.005471681673197411, 0.006451498305277347, 0.00745216504004511, 0.008454911336315016, 0.009438906220329316, 0.010381922093328643, 0.011261134326336953, 0.012054019059648723, 0.012739301373478909, 0.01329789887399927, 0.013713802630057096, 0.013974838835556981, 0.014073260665380772, 0.014006130178820098, 0.013775463999780116, 0.013388132694088489, 0.012855520849033929, 0.012192971320157509, 0.011419051494620054, 0.010554690502106471, 0.009622243207138084, 0.008644539099210868, 0.007643971882414223, 0.0066416791172108644, 0.005656851513146756, 0.004706199496728456, 0.0038035916907002963, 0.0029598671339553725, 0.0021828115051823055, 0.0014772781184435278, 0.0008454275769439333, 0.0002870559351681379] + [0.0] * 106,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_46": {
            "samples": [0.0003798576395459785, 0.00043578666200400735, 0.0004935296633211693, 0.0005515554982505122, 0.0006080287141733543, 0.0006608525432248669, 0.0007077364436294015, 0.0007462873610355451, 0.0007741217179457732, 0.000788992915208048, 0.0007889270697455971, 0.0007723580575993246, 0.0007382519077163814, 0.0006862103827387051, 0.0006165442994707075, 0.0005303088013655113, 0.00042929531097465857, 0.00031597807114201563, 0.00019341675095889237, 6.512020720763538e-05, -6.512020720763538e-05, -0.00019341675095889237, -0.00031597807114201563, -0.00042929531097465857, -0.0005303088013655113, -0.0006165442994707075, -0.0006862103827387051, -0.0007382519077163814, -0.0007723580575993246, -0.0007889270697455971, -0.000788992915208048, -0.0007741217179457732, -0.0007462873610355451, -0.0007077364436294015, -0.0006608525432248669, -0.0006080287141733543, -0.0005515554982505122, -0.0004935296633211693, -0.00043578666200400735, -0.0003798576395459785] + [0.0] * 65 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789555, 0.0016217826115637818, 0.0021389217498052186, 0.002696774030395553, 0.0032894157457530803, 0.0039089425256320365, 0.004545532613031832, 0.0051876208326819065, 0.005822186296327269, 0.006435148841109956, 0.007011860634169719, 0.007537671049128934, 0.007998535633794192, 0.008381634516400978, 0.008675962590192945, 0.008872853716940651, 0.008966404172880874, 0.008953766494256922, 0.008835293328522897, 0.008614521158764744, 0.008297994944280964, 0.007894945810504667, 0.00741684393589708, 0.006876856847658552, 0.006289248786844123, 0.005668759247261227, 0.0050299981499855265, 0.004386891608335701, 0.0037522063520680424, 0.0031371732953768207, 0.002551222241861101, 0.0020018311298938603, 0.0014944852749314572, 0.0010327353644391077, 0.0006183379243041819, 0.0002514588145349552, -6.908096354474373e-05, -0.00034553742236856605] + [0.0] * 65 + [0.00024877844843592935, 0.0008809232750019343, 0.0015974588866745011, 0.0023989529285996514, 0.0032833107305677554, 0.004245387322252831, 0.005276696246704929, 0.006365250140793624, 0.007495563863613569, 0.008648843495784611, 0.009803374023827669, 0.010935105537303862, 0.012018423211070366, 0.013027071404044575, 0.013935188233421197, 0.01471839536840829, 0.015354879800335761, 0.01582640098470384, 0.016119158610248232, 0.01622446343056509, 0.016139165664116033, 0.015865811491772037, 0.015412516802343078, 0.01479256692168603, 0.014023769871586286, 0.013127607085927789, 0.01212823806994391, 0.011051423235100076, 0.009923431587893713, 0.00876999713781847, 0.007615380362032682, 0.006481579781991354, 0.00538772491851469, 0.00434966698090877, 0.003379768978786447, 0.0024868837307194035, 0.0016764974252954474, 0.0009510085794230883, 0.000310107693922607, -0.00024877844843592935] + [0.0] * 106,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_46": {
            "samples": [0.0] * 356,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_46": {
            "samples": [0.0] * 356,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_46": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 61,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_47": {
            "samples": [0.0] * 105 + [-0.000157783763627091, 0.0005358236462419265, 0.0013288311147143378, 0.0022237650156902516, 0.0032203133215568057, 0.004314806824009118, 0.005499787323106857, 0.006763705875530093, 0.008090791755457434, 0.009461126481233456, 0.010850947090737683, 0.012233189208447768, 0.013578264158704065, 0.014855046646616254, 0.016032031846637828, 0.0170786047598928, 0.017966352058797392, 0.01867033876258056, 0.019170270031667394, 0.019451462661092035, 0.01950556140921082, 0.019330951401410515, 0.018932838204992756, 0.018322990034824436, 0.017519159903993796, 0.016544227310862743, 0.015425117354989588, 0.01419156847262334, 0.0128748272776012, 0.011506349901330285, 0.010116583993081484, 0.008733894989126472, 0.007383685659073528, 0.006087740851514875, 0.00486381145425525, 0.0037254344455140893, 0.0026819708975948458, 0.0017388319130844836, 0.0008978543256915441, 0.000157783763627091] + [0.0] * 65 + [-0.0002870559351681379, 0.00018678531325335476, 0.0007313638374660276, 0.001349197735894062, 0.002040900484424627, 0.002804787796534073, 0.003636535888428067, 0.0045289225522746135, 0.005471681673197411, 0.006451498305277347, 0.00745216504004511, 0.008454911336315016, 0.009438906220329316, 0.010381922093328643, 0.011261134326336953, 0.012054019059648723, 0.012739301373478909, 0.01329789887399927, 0.013713802630057096, 0.013974838835556981, 0.014073260665380772, 0.014006130178820098, 0.013775463999780116, 0.013388132694088489, 0.012855520849033929, 0.012192971320157509, 0.011419051494620054, 0.010554690502106471, 0.009622243207138084, 0.008644539099210868, 0.007643971882414223, 0.0066416791172108644, 0.005656851513146756, 0.004706199496728456, 0.0038035916907002963, 0.0029598671339553725, 0.0021828115051823055, 0.0014772781184435278, 0.0008454275769439333, 0.0002870559351681379] + [0.0] * 106,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_47": {
            "samples": [0.0] * 105 + [0.00034553742236856605, 0.0007237455283559925, 0.0011493371245789555, 0.0016217826115637818, 0.0021389217498052186, 0.002696774030395553, 0.0032894157457530803, 0.0039089425256320365, 0.004545532613031832, 0.0051876208326819065, 0.005822186296327269, 0.006435148841109956, 0.007011860634169719, 0.007537671049128934, 0.007998535633794192, 0.008381634516400978, 0.008675962590192945, 0.008872853716940651, 0.008966404172880874, 0.008953766494256922, 0.008835293328522897, 0.008614521158764744, 0.008297994944280964, 0.007894945810504667, 0.00741684393589708, 0.006876856847658552, 0.006289248786844123, 0.005668759247261227, 0.0050299981499855265, 0.004386891608335701, 0.0037522063520680424, 0.0031371732953768207, 0.002551222241861101, 0.0020018311298938603, 0.0014944852749314572, 0.0010327353644391077, 0.0006183379243041819, 0.0002514588145349552, -6.908096354474373e-05, -0.00034553742236856605] + [0.0] * 65 + [0.00024877844843592935, 0.0008809232750019343, 0.0015974588866745011, 0.0023989529285996514, 0.0032833107305677554, 0.004245387322252831, 0.005276696246704929, 0.006365250140793624, 0.007495563863613569, 0.008648843495784611, 0.009803374023827669, 0.010935105537303862, 0.012018423211070366, 0.013027071404044575, 0.013935188233421197, 0.01471839536840829, 0.015354879800335761, 0.01582640098470384, 0.016119158610248232, 0.01622446343056509, 0.016139165664116033, 0.015865811491772037, 0.015412516802343078, 0.01479256692168603, 0.014023769871586286, 0.013127607085927789, 0.01212823806994391, 0.011051423235100076, 0.009923431587893713, 0.00876999713781847, 0.007615380362032682, 0.006481579781991354, 0.00538772491851469, 0.00434966698090877, 0.003379768978786447, 0.0024868837307194035, 0.0016764974252954474, 0.0009510085794230883, 0.000310107693922607, -0.00024877844843592935] + [0.0] * 106,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_47": {
            "samples": [0.0] * 356,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_47": {
            "samples": [0.0] * 356,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_47": {
            "samples": [0.0] * 60 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 80 + [0.1755] * 25 + [0.0] * 61,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_48": {
            "samples": [0.0, 0.0015760768444548542, 0.00337235610740649, 0.005392994053965991, 0.0076356283889478915, 0.010090276907130893, 0.012738449776040096, 0.015552569435837084, 0.018495784766494085, 0.0215222502891611, 0.024577916926684592, 0.027601849347301578, 0.030528048168025384, 0.033287716114425325, 0.03581186901257599, 0.03803415887258986, 0.03989375082406045, 0.04133808125447058, 0.04232532323982649] + [0.04282639809501372] * 2 + [0.04232532323982649, 0.04133808125447058, 0.03989375082406045, 0.03803415887258986, 0.03581186901257599, 0.033287716114425325, 0.030528048168025384, 0.027601849347301578, 0.024577916926684592, 0.0215222502891611, 0.018495784766494085, 0.015552569435837084, 0.012738449776040096, 0.010090276907130893, 0.0076356283889478915, 0.005392994053965991, 0.00337235610740649, 0.0015760768444548542, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_48": {
            "samples": [0.000759715279091957, 0.0008715733240080147, 0.0009870593266423386, 0.0011031109965010243, 0.0012160574283467086, 0.0013217050864497337, 0.001415472887258803, 0.0014925747220710902, 0.0015482434358915463, 0.001577985830416096, 0.0015778541394911943, 0.0015447161151986492, 0.0014765038154327629, 0.0013724207654774103, 0.001233088598941415, 0.0010606176027310227, 0.0008585906219493171, 0.0006319561422840313, 0.00038683350191778473, 0.00013024041441527076, -0.00013024041441527076, -0.00038683350191778473, -0.0006319561422840313, -0.0008585906219493171, -0.0010606176027310227, -0.001233088598941415, -0.0013724207654774103, -0.0014765038154327629, -0.0015447161151986492, -0.0015778541394911943, -0.001577985830416096, -0.0015482434358915463, -0.0014925747220710902, -0.001415472887258803, -0.0013217050864497337, -0.0012160574283467086, -0.0011031109965010243, -0.0009870593266423386, -0.0008715733240080147, -0.000759715279091957],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_48": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_48": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_48": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_49": {
            "samples": [9.303828848033032e-20, -0.0015760768444548542, -0.00337235610740649, -0.005392994053965991, -0.0076356283889478915, -0.010090276907130893, -0.012738449776040096, -0.015552569435837084, -0.018495784766494085, -0.0215222502891611, -0.024577916926684592, -0.027601849347301578, -0.030528048168025384, -0.033287716114425325, -0.03581186901257599, -0.03803415887258986, -0.03989375082406045, -0.04133808125447058, -0.04232532323982649] + [-0.04282639809501372] * 2 + [-0.04232532323982649, -0.04133808125447058, -0.03989375082406045, -0.03803415887258986, -0.03581186901257599, -0.033287716114425325, -0.030528048168025384, -0.027601849347301578, -0.024577916926684592, -0.0215222502891611, -0.018495784766494085, -0.015552569435837084, -0.012738449776040096, -0.010090276907130893, -0.0076356283889478915, -0.005392994053965991, -0.00337235610740649, -0.0015760768444548542, -9.303828848033032e-20],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_49": {
            "samples": [-0.000759715279091957, -0.0008715733240080149, -0.000987059326642339, -0.001103110996501025, -0.0012160574283467094, -0.001321705086449735, -0.0014154728872588045, -0.0014925747220710921, -0.0015482434358915485, -0.0015779858304160986, -0.0015778541394911973, -0.0015447161151986527, -0.0014765038154327666, -0.0013724207654774144, -0.0012330885989414193, -0.0010606176027310272, -0.000858590621949322, -0.0006319561422840364, -0.00038683350191778994, -0.000130240414415276, 0.00013024041441526553, 0.00038683350191777953, 0.0006319561422840262, 0.0008585906219493123, 0.0010606176027310181, 0.0012330885989414106, 0.0013724207654774061, 0.0014765038154327592, 0.0015447161151986458, 0.0015778541394911912, 0.0015779858304160934, 0.0015482434358915441, 0.0014925747220710882, 0.0014154728872588015, 0.0013217050864497324, 0.0012160574283467077, 0.0011031109965010237, 0.0009870593266423382, 0.0008715733240080145, 0.000759715279091957],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_49": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_49": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_49": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_I_50": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_xy_baked_wf_Q_50": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_I_50": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q3_xy_baked_wf_Q_50": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_50": {
            "samples": [0.0] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
    },
    "digital_waveforms": {
        "ON": {
            "samples": [(1, 0)],
        },
    },
    "integration_weights": {
        "cosine_weights": {
            "cosine": [(0.0, 400), (1.0, 1700)],
            "sine": [(0.0, 400), (0.0, 1700)],
        },
        "sine_weights": {
            "cosine": [(0.0, 400), (0.0, 1700)],
            "sine": [(0.0, 400), (1.0, 1700)],
        },
        "minus_sine_weights": {
            "cosine": [(0.0, 400), (0.0, 1700)],
            "sine": [(0.0, 400), (-1.0, 1700)],
        },
        "rotated_cosine_weights_q1": {
            "cosine": [(0.0, 400), (-0.8535507972753273, 1700)],
            "sine": [(0.0, 400), (0.5210096318405766, 1700)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(0.0, 400), (-0.5210096318405766, 1700)],
            "sine": [(0.0, 400), (-0.8535507972753273, 1700)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(0.0, 400), (0.5210096318405766, 1700)],
            "sine": [(0.0, 400), (0.8535507972753273, 1700)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(0.0, 400), (0.8079898838980305, 1700)],
            "sine": [(0.0, 400), (0.5891963573533421, 1700)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(0.0, 400), (-0.5891963573533421, 1700)],
            "sine": [(0.0, 400), (0.8079898838980305, 1700)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(0.0, 400), (0.5891963573533421, 1700)],
            "sine": [(0.0, 400), (-0.8079898838980305, 1700)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(0.0, 400), (-0.18566661538557747, 1700)],
            "sine": [(0.0, 400), (0.9826127965436152, 1700)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(0.0, 400), (-0.9826127965436152, 1700)],
            "sine": [(0.0, 400), (-0.18566661538557747, 1700)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(0.0, 400), (0.9826127965436152, 1700)],
            "sine": [(0.0, 400), (0.18566661538557747, 1700)],
        },
        "rotated_cosine_weights_q4": {
            "cosine": [(0.0, 400), (1.0, 1700)],
            "sine": [(0.0, 400), (0.0, 1700)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(0.0, 400), (0.0, 1700)],
            "sine": [(0.0, 400), (1.0, 1700)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(0.0, 400), (0.0, 1700)],
            "sine": [(0.0, 400), (-1.0, 1700)],
        },
        "rotated_cosine_weights_q5": {
            "cosine": [(0.0, 400), (1.0, 1700)],
            "sine": [(0.0, 400), (0.0, 1700)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(0.0, 400), (0.0, 1700)],
            "sine": [(0.0, 400), (1.0, 1700)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(0.0, 400), (0.0, 1700)],
            "sine": [(0.0, 400), (-1.0, 1700)],
        },
        "opt_cosine_weights_q1": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_sine_weights_q1": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_minus_sine_weights_q1": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_cosine_weights_q2": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_sine_weights_q2": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_minus_sine_weights_q2": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_cosine_weights_q3": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_sine_weights_q3": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_minus_sine_weights_q3": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_cosine_weights_q4": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_sine_weights_q4": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_minus_sine_weights_q4": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_cosine_weights_q5": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_sine_weights_q5": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
        "opt_minus_sine_weights_q5": {
            "cosine": [(1.0, 1700)],
            "sine": [(1.0, 1700)],
        },
    },
    "mixers": {
        "octave_octave1_2": [{'intermediate_frequency': 116555000.0, 'lo_frequency': 4055000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]}],
        "octave_octave1_3": [{'intermediate_frequency': 317621000.0, 'lo_frequency': 3850000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]}],
        "octave_octave1_4": [{'intermediate_frequency': 101584000.0, 'lo_frequency': 4300000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]}],
        "octave_octave1_5": [{'intermediate_frequency': 89863100.0, 'lo_frequency': 3950000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]}],
        "octave_octave2_1": [{'intermediate_frequency': 92000000.0, 'lo_frequency': 4750000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]}],
        "octave_octave1_1": [
            {'intermediate_frequency': 214210000.0, 'lo_frequency': 5950000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
            {'intermediate_frequency': 75079000.0, 'lo_frequency': 5950000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
            {'intermediate_frequency': 103970000.0, 'lo_frequency': 5950000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
            {'intermediate_frequency': 163060000.0, 'lo_frequency': 5950000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
            {'intermediate_frequency': 25800000.0, 'lo_frequency': 5950000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
        ],
    },
}


