
# Single QUA script generated at 2024-01-02 15:42:45.573014
# QUA library version: 1.1.3

from qm.qua import *

with program() as prog:
    v1 = declare(int, )
    v2 = declare(fixed, )
    v3 = declare(fixed, )
    v4 = declare(fixed, )
    v5 = declare(fixed, )
    v6 = declare(fixed, )
    v7 = declare(fixed, )
    v8 = declare(fixed, )
    v9 = declare(fixed, )
    v10 = declare(fixed, )
    v11 = declare(int, )
    v12 = declare(int, value=75154904)
    v13 = declare(int, value=-103174057)
    v14 = declare(int, value=163060379)
    v15 = declare(int, value=-24350583)
    wait((4+(0*(Cast.to_int(v2)+Cast.to_int(v6)))), "rr1")
    wait((4+(0*(Cast.to_int(v3)+Cast.to_int(v7)))), "rr2")
    wait((4+(0*(Cast.to_int(v4)+Cast.to_int(v8)))), "rr3")
    wait((4+(0*(Cast.to_int(v5)+Cast.to_int(v9)))), "rr4")
    set_dc_offset("q2_z", "single", -0.3529)
    update_frequency("rr2", v12, "Hz", False)
    set_dc_offset("q3_z", "single", -0.3421)
    update_frequency("rr3", v13, "Hz", False)
    set_dc_offset("q4_z", "single", -0.3433)
    update_frequency("rr4", v14, "Hz", False)
    set_dc_offset("q5_z", "single", -0.34)
    update_frequency("rr5", v15, "Hz", False)
    wait(25, )
    with for_(v1,0,(v1<500),(v1+1)):
        with for_(v10,0.32,(v10<0.37950000000000006),(v10+0.0010000000000000009)):
            with for_(v11,0,(v11<=50),(v11+1)):
                wait(30000, )
                play("x180", "q2_xy")
                play("x180", "q3_xy")
                align()
                wait(5, )
                with if_((v11==0)):
                    play("baked_Op_0"*amp(v10), "q2_z")
                with elif_((v11==1)):
                    play("baked_Op_1"*amp(v10), "q2_z")
                with elif_((v11==2)):
                    play("baked_Op_2"*amp(v10), "q2_z")
                with elif_((v11==3)):
                    play("baked_Op_3"*amp(v10), "q2_z")
                with elif_((v11==4)):
                    play("baked_Op_4"*amp(v10), "q2_z")
                with elif_((v11==5)):
                    play("baked_Op_5"*amp(v10), "q2_z")
                with elif_((v11==6)):
                    play("baked_Op_6"*amp(v10), "q2_z")
                with elif_((v11==7)):
                    play("baked_Op_7"*amp(v10), "q2_z")
                with elif_((v11==8)):
                    play("baked_Op_8"*amp(v10), "q2_z")
                with elif_((v11==9)):
                    play("baked_Op_9"*amp(v10), "q2_z")
                with elif_((v11==10)):
                    play("baked_Op_10"*amp(v10), "q2_z")
                with elif_((v11==11)):
                    play("baked_Op_11"*amp(v10), "q2_z")
                with elif_((v11==12)):
                    play("baked_Op_12"*amp(v10), "q2_z")
                with elif_((v11==13)):
                    play("baked_Op_13"*amp(v10), "q2_z")
                with elif_((v11==14)):
                    play("baked_Op_14"*amp(v10), "q2_z")
                with elif_((v11==15)):
                    play("baked_Op_15"*amp(v10), "q2_z")
                with elif_((v11==16)):
                    play("baked_Op_16"*amp(v10), "q2_z")
                with elif_((v11==17)):
                    play("baked_Op_17"*amp(v10), "q2_z")
                with elif_((v11==18)):
                    play("baked_Op_18"*amp(v10), "q2_z")
                with elif_((v11==19)):
                    play("baked_Op_19"*amp(v10), "q2_z")
                with elif_((v11==20)):
                    play("baked_Op_20"*amp(v10), "q2_z")
                with elif_((v11==21)):
                    play("baked_Op_21"*amp(v10), "q2_z")
                with elif_((v11==22)):
                    play("baked_Op_22"*amp(v10), "q2_z")
                with elif_((v11==23)):
                    play("baked_Op_23"*amp(v10), "q2_z")
                with elif_((v11==24)):
                    play("baked_Op_24"*amp(v10), "q2_z")
                with elif_((v11==25)):
                    play("baked_Op_25"*amp(v10), "q2_z")
                with elif_((v11==26)):
                    play("baked_Op_26"*amp(v10), "q2_z")
                with elif_((v11==27)):
                    play("baked_Op_27"*amp(v10), "q2_z")
                with elif_((v11==28)):
                    play("baked_Op_28"*amp(v10), "q2_z")
                with elif_((v11==29)):
                    play("baked_Op_29"*amp(v10), "q2_z")
                with elif_((v11==30)):
                    play("baked_Op_30"*amp(v10), "q2_z")
                with elif_((v11==31)):
                    play("baked_Op_31"*amp(v10), "q2_z")
                with elif_((v11==32)):
                    play("baked_Op_32"*amp(v10), "q2_z")
                with elif_((v11==33)):
                    play("baked_Op_33"*amp(v10), "q2_z")
                with elif_((v11==34)):
                    play("baked_Op_34"*amp(v10), "q2_z")
                with elif_((v11==35)):
                    play("baked_Op_35"*amp(v10), "q2_z")
                with elif_((v11==36)):
                    play("baked_Op_36"*amp(v10), "q2_z")
                with elif_((v11==37)):
                    play("baked_Op_37"*amp(v10), "q2_z")
                with elif_((v11==38)):
                    play("baked_Op_38"*amp(v10), "q2_z")
                with elif_((v11==39)):
                    play("baked_Op_39"*amp(v10), "q2_z")
                with elif_((v11==40)):
                    play("baked_Op_40"*amp(v10), "q2_z")
                with elif_((v11==41)):
                    play("baked_Op_41"*amp(v10), "q2_z")
                with elif_((v11==42)):
                    play("baked_Op_42"*amp(v10), "q2_z")
                with elif_((v11==43)):
                    play("baked_Op_43"*amp(v10), "q2_z")
                with elif_((v11==44)):
                    play("baked_Op_44"*amp(v10), "q2_z")
                with elif_((v11==45)):
                    play("baked_Op_45"*amp(v10), "q2_z")
                with elif_((v11==46)):
                    play("baked_Op_46"*amp(v10), "q2_z")
                with elif_((v11==47)):
                    play("baked_Op_47"*amp(v10), "q2_z")
                with elif_((v11==48)):
                    play("baked_Op_48"*amp(v10), "q2_z")
                with elif_((v11==49)):
                    play("baked_Op_49"*amp(v10), "q2_z")
                with elif_((v11==50)):
                    play("baked_Op_50"*amp(v10), "q2_z")
                align()
                wait(5, )
                align()
                measure("readout"*amp(1.0), "rr2", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", v2), dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", v6))
                r2 = declare_stream()
                save(v2, r2)
                r6 = declare_stream()
                save(v6, r6)
                measure("readout"*amp(1.0), "rr3", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", v3), dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", v7))
                r3 = declare_stream()
                save(v3, r3)
                r7 = declare_stream()
                save(v7, r7)
                measure("readout"*amp(1.0), "rr4", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", v4), dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", v8))
                r4 = declare_stream()
                save(v4, r4)
                r8 = declare_stream()
                save(v8, r8)
                measure("readout"*amp(1.0), "rr5", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", v5), dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", v9))
                r5 = declare_stream()
                save(v5, r5)
                r9 = declare_stream()
                save(v9, r9)
        r1 = declare_stream()
        save(v1, r1)
    with stream_processing():
        r1.save("n")
        r2.buffer(60, 51).average().save("I2")
        r6.buffer(60, 51).average().save("Q2")
        r3.buffer(60, 51).average().save("I3")
        r7.buffer(60, 51).average().save("Q3")
        r4.buffer(60, 51).average().save("I4")
        r8.buffer(60, 51).average().save("Q4")
        r5.buffer(60, 51).average().save("I5")
        r9.buffer(60, 51).average().save("Q5")


config = {
    "version": 1,
    "controllers": {
        "con1": {
            "analog_outputs": {
                "1": {
                    "offset": 0.0009765625,
                },
                "2": {
                    "offset": -0.0068359375,
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
            "intermediate_frequency": -101596000.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q2",
                "x90": "x90_pulse_q2",
                "-x90": "-x90_pulse_q2",
                "y90": "y90_pulse_q2",
                "y180": "y180_pulse_q2",
                "-y90": "-y90_pulse_q2",
            },
        },
        "q3_xy": {
            "mixInputs": {
                "I": ('con1', 3),
                "Q": ('con1', 4),
                "lo_frequency": 3850000000.0,
                "mixer": "octave_octave1_3",
            },
            "intermediate_frequency": -317033000.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q3",
                "x90": "x90_pulse_q3",
                "-x90": "-x90_pulse_q3",
                "y90": "y90_pulse_q3",
                "y180": "y180_pulse_q3",
                "-y90": "-y90_pulse_q3",
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
            "length": 20,
            "waveforms": {
                "I": "x90_I_wf_q1",
                "Q": "x90_Q_wf_q1",
            },
        },
        "x180_pulse_q1": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "x180_I_wf_q1",
                "Q": "x180_Q_wf_q1",
            },
        },
        "-x90_pulse_q1": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "minus_x90_I_wf_q1",
                "Q": "minus_x90_Q_wf_q1",
            },
        },
        "y90_pulse_q1": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "y90_I_wf_q1",
                "Q": "y90_Q_wf_q1",
            },
        },
        "y180_pulse_q1": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "y180_I_wf_q1",
                "Q": "y180_Q_wf_q1",
            },
        },
        "-y90_pulse_q1": {
            "operation": "control",
            "length": 20,
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
            "length": 20,
            "waveforms": {
                "I": "x90_I_wf_q2",
                "Q": "x90_Q_wf_q2",
            },
        },
        "x180_pulse_q2": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "x180_I_wf_q2",
                "Q": "x180_Q_wf_q2",
            },
        },
        "-x90_pulse_q2": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "minus_x90_I_wf_q2",
                "Q": "minus_x90_Q_wf_q2",
            },
        },
        "y90_pulse_q2": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "y90_I_wf_q2",
                "Q": "y90_Q_wf_q2",
            },
        },
        "y180_pulse_q2": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "y180_I_wf_q2",
                "Q": "y180_Q_wf_q2",
            },
        },
        "-y90_pulse_q2": {
            "operation": "control",
            "length": 20,
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
            "length": 20,
            "waveforms": {
                "I": "x90_I_wf_q3",
                "Q": "x90_Q_wf_q3",
            },
        },
        "x180_pulse_q3": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "x180_I_wf_q3",
                "Q": "x180_Q_wf_q3",
            },
        },
        "-x90_pulse_q3": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "minus_x90_I_wf_q3",
                "Q": "minus_x90_Q_wf_q3",
            },
        },
        "y90_pulse_q3": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "y90_I_wf_q3",
                "Q": "y90_Q_wf_q3",
            },
        },
        "y180_pulse_q3": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "y180_I_wf_q3",
                "Q": "y180_Q_wf_q3",
            },
        },
        "-y90_pulse_q3": {
            "operation": "control",
            "length": 20,
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
            "length": 20,
            "waveforms": {
                "I": "x90_I_wf_q4",
                "Q": "x90_Q_wf_q4",
            },
        },
        "x180_pulse_q4": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "x180_I_wf_q4",
                "Q": "x180_Q_wf_q4",
            },
        },
        "-x90_pulse_q4": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "minus_x90_I_wf_q4",
                "Q": "minus_x90_Q_wf_q4",
            },
        },
        "y90_pulse_q4": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "y90_I_wf_q4",
                "Q": "y90_Q_wf_q4",
            },
        },
        "y180_pulse_q4": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "y180_I_wf_q4",
                "Q": "y180_Q_wf_q4",
            },
        },
        "-y90_pulse_q4": {
            "operation": "control",
            "length": 20,
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
            "length": 20,
            "waveforms": {
                "I": "x90_I_wf_q5",
                "Q": "x90_Q_wf_q5",
            },
        },
        "x180_pulse_q5": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "x180_I_wf_q5",
                "Q": "x180_Q_wf_q5",
            },
        },
        "-x90_pulse_q5": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "minus_x90_I_wf_q5",
                "Q": "minus_x90_Q_wf_q5",
            },
        },
        "y90_pulse_q5": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "y90_I_wf_q5",
                "Q": "y90_Q_wf_q5",
            },
        },
        "y180_pulse_q5": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "I": "y180_I_wf_q5",
                "Q": "y180_Q_wf_q5",
            },
        },
        "-y90_pulse_q5": {
            "operation": "control",
            "length": 20,
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
        "q2_z_baked_pulse_0": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_0",
            },
        },
        "q2_z_baked_pulse_1": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_1",
            },
        },
        "q2_z_baked_pulse_2": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_2",
            },
        },
        "q2_z_baked_pulse_3": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_3",
            },
        },
        "q2_z_baked_pulse_4": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_4",
            },
        },
        "q2_z_baked_pulse_5": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_5",
            },
        },
        "q2_z_baked_pulse_6": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_6",
            },
        },
        "q2_z_baked_pulse_7": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_7",
            },
        },
        "q2_z_baked_pulse_8": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_8",
            },
        },
        "q2_z_baked_pulse_9": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_9",
            },
        },
        "q2_z_baked_pulse_10": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_10",
            },
        },
        "q2_z_baked_pulse_11": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_11",
            },
        },
        "q2_z_baked_pulse_12": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_12",
            },
        },
        "q2_z_baked_pulse_13": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_13",
            },
        },
        "q2_z_baked_pulse_14": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_14",
            },
        },
        "q2_z_baked_pulse_15": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_15",
            },
        },
        "q2_z_baked_pulse_16": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_16",
            },
        },
        "q2_z_baked_pulse_17": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "single": "q2_z_baked_wf_17",
            },
        },
        "q2_z_baked_pulse_18": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "single": "q2_z_baked_wf_18",
            },
        },
        "q2_z_baked_pulse_19": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "single": "q2_z_baked_wf_19",
            },
        },
        "q2_z_baked_pulse_20": {
            "operation": "control",
            "length": 20,
            "waveforms": {
                "single": "q2_z_baked_wf_20",
            },
        },
        "q2_z_baked_pulse_21": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "single": "q2_z_baked_wf_21",
            },
        },
        "q2_z_baked_pulse_22": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "single": "q2_z_baked_wf_22",
            },
        },
        "q2_z_baked_pulse_23": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "single": "q2_z_baked_wf_23",
            },
        },
        "q2_z_baked_pulse_24": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "single": "q2_z_baked_wf_24",
            },
        },
        "q2_z_baked_pulse_25": {
            "operation": "control",
            "length": 28,
            "waveforms": {
                "single": "q2_z_baked_wf_25",
            },
        },
        "q2_z_baked_pulse_26": {
            "operation": "control",
            "length": 28,
            "waveforms": {
                "single": "q2_z_baked_wf_26",
            },
        },
        "q2_z_baked_pulse_27": {
            "operation": "control",
            "length": 28,
            "waveforms": {
                "single": "q2_z_baked_wf_27",
            },
        },
        "q2_z_baked_pulse_28": {
            "operation": "control",
            "length": 28,
            "waveforms": {
                "single": "q2_z_baked_wf_28",
            },
        },
        "q2_z_baked_pulse_29": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "single": "q2_z_baked_wf_29",
            },
        },
        "q2_z_baked_pulse_30": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "single": "q2_z_baked_wf_30",
            },
        },
        "q2_z_baked_pulse_31": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "single": "q2_z_baked_wf_31",
            },
        },
        "q2_z_baked_pulse_32": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "single": "q2_z_baked_wf_32",
            },
        },
        "q2_z_baked_pulse_33": {
            "operation": "control",
            "length": 36,
            "waveforms": {
                "single": "q2_z_baked_wf_33",
            },
        },
        "q2_z_baked_pulse_34": {
            "operation": "control",
            "length": 36,
            "waveforms": {
                "single": "q2_z_baked_wf_34",
            },
        },
        "q2_z_baked_pulse_35": {
            "operation": "control",
            "length": 36,
            "waveforms": {
                "single": "q2_z_baked_wf_35",
            },
        },
        "q2_z_baked_pulse_36": {
            "operation": "control",
            "length": 36,
            "waveforms": {
                "single": "q2_z_baked_wf_36",
            },
        },
        "q2_z_baked_pulse_37": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_37",
            },
        },
        "q2_z_baked_pulse_38": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_38",
            },
        },
        "q2_z_baked_pulse_39": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_39",
            },
        },
        "q2_z_baked_pulse_40": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_40",
            },
        },
        "q2_z_baked_pulse_41": {
            "operation": "control",
            "length": 44,
            "waveforms": {
                "single": "q2_z_baked_wf_41",
            },
        },
        "q2_z_baked_pulse_42": {
            "operation": "control",
            "length": 44,
            "waveforms": {
                "single": "q2_z_baked_wf_42",
            },
        },
        "q2_z_baked_pulse_43": {
            "operation": "control",
            "length": 44,
            "waveforms": {
                "single": "q2_z_baked_wf_43",
            },
        },
        "q2_z_baked_pulse_44": {
            "operation": "control",
            "length": 44,
            "waveforms": {
                "single": "q2_z_baked_wf_44",
            },
        },
        "q2_z_baked_pulse_45": {
            "operation": "control",
            "length": 48,
            "waveforms": {
                "single": "q2_z_baked_wf_45",
            },
        },
        "q2_z_baked_pulse_46": {
            "operation": "control",
            "length": 48,
            "waveforms": {
                "single": "q2_z_baked_wf_46",
            },
        },
        "q2_z_baked_pulse_47": {
            "operation": "control",
            "length": 48,
            "waveforms": {
                "single": "q2_z_baked_wf_47",
            },
        },
        "q2_z_baked_pulse_48": {
            "operation": "control",
            "length": 48,
            "waveforms": {
                "single": "q2_z_baked_wf_48",
            },
        },
        "q2_z_baked_pulse_49": {
            "operation": "control",
            "length": 52,
            "waveforms": {
                "single": "q2_z_baked_wf_49",
            },
        },
        "q2_z_baked_pulse_50": {
            "operation": "control",
            "length": 52,
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
            "samples": [0.0, 0.0014694319341680283, 0.003302446110579668, 0.005465306961995178, 0.007867580142769207, 0.010360266914041962, 0.012746265974209976, 0.014803720077191503, 0.01631910724476066] + [0.017123493100572245] * 2 + [0.01631910724476066, 0.014803720077191503, 0.012746265974209976, 0.010360266914041962, 0.007867580142769207, 0.005465306961995178, 0.003302446110579668, 0.0014694319341680283, 0.0],
        },
        "x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0006316040056343379, -0.000810002220721428, -0.0009842440123493477, -0.0011286449159734998, -0.001214052138069595, -0.0012132381518087355, -0.0011073596801941049, -0.0008918175378462839, -0.0005796566432847614, -0.00020110429322099118, 0.00020110429322099118, 0.0005796566432847614, 0.0008918175378462839, 0.0011073596801941049, 0.0012132381518087355, 0.001214052138069595, 0.0011286449159734998, 0.0009842440123493477, 0.000810002220721428, 0.0006316040056343379],
        },
        "x180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0029388638683360566, 0.006604892221159336, 0.010930613923990355, 0.015735160285538414, 0.020720533828083924, 0.025492531948419953, 0.029607440154383005, 0.03263821448952132] + [0.03424698620114449] * 2 + [0.03263821448952132, 0.029607440154383005, 0.025492531948419953, 0.020720533828083924, 0.015735160285538414, 0.010930613923990355, 0.006604892221159336, 0.0029388638683360566, 0.0],
        },
        "x180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0012632080112686757, -0.001620004441442856, -0.0019684880246986954, -0.0022572898319469996, -0.00242810427613919, -0.002426476303617471, -0.0022147193603882097, -0.0017836350756925679, -0.0011593132865695228, -0.00040220858644198236, 0.00040220858644198236, 0.0011593132865695228, 0.0017836350756925679, 0.0022147193603882097, 0.002426476303617471, 0.00242810427613919, 0.0022572898319469996, 0.0019684880246986954, 0.001620004441442856, 0.0012632080112686757],
        },
        "minus_x90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.0014694319341680283, -0.003302446110579668, -0.005465306961995178, -0.007867580142769207, -0.010360266914041962, -0.012746265974209976, -0.014803720077191503, -0.01631910724476066] + [-0.017123493100572245] * 2 + [-0.01631910724476066, -0.014803720077191503, -0.012746265974209976, -0.010360266914041962, -0.007867580142769207, -0.005465306961995178, -0.003302446110579668, -0.0014694319341680283, 0.0],
        },
        "minus_x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0006316040056343379, 0.000810002220721428, 0.0009842440123493477, 0.0011286449159734998, 0.001214052138069595, 0.0012132381518087355, 0.0011073596801941049, 0.0008918175378462839, 0.0005796566432847614, 0.00020110429322099118, -0.00020110429322099118, -0.0005796566432847614, -0.0008918175378462839, -0.0011073596801941049, -0.0012132381518087355, -0.001214052138069595, -0.0011286449159734998, -0.0009842440123493477, -0.000810002220721428, -0.0006316040056343379],
        },
        "y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0006316040056343379, 0.000810002220721428, 0.0009842440123493477, 0.0011286449159734998, 0.001214052138069595, 0.0012132381518087355, 0.0011073596801941049, 0.0008918175378462839, 0.0005796566432847614, 0.00020110429322099118, -0.00020110429322099118, -0.0005796566432847614, -0.0008918175378462839, -0.0011073596801941049, -0.0012132381518087355, -0.001214052138069595, -0.0011286449159734998, -0.0009842440123493477, -0.000810002220721428, -0.0006316040056343379],
        },
        "y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0014694319341680283, 0.003302446110579668, 0.005465306961995178, 0.007867580142769207, 0.010360266914041962, 0.012746265974209976, 0.014803720077191503, 0.01631910724476066] + [0.017123493100572245] * 2 + [0.01631910724476066, 0.014803720077191503, 0.012746265974209976, 0.010360266914041962, 0.007867580142769207, 0.005465306961995178, 0.003302446110579668, 0.0014694319341680283, 0.0],
        },
        "y180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0012632080112686757, 0.001620004441442856, 0.0019684880246986954, 0.0022572898319469996, 0.00242810427613919, 0.002426476303617471, 0.0022147193603882097, 0.0017836350756925679, 0.0011593132865695228, 0.00040220858644198236, -0.00040220858644198236, -0.0011593132865695228, -0.0017836350756925679, -0.0022147193603882097, -0.002426476303617471, -0.00242810427613919, -0.0022572898319469996, -0.0019684880246986954, -0.001620004441442856, -0.0012632080112686757],
        },
        "y180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0029388638683360566, 0.006604892221159336, 0.010930613923990355, 0.015735160285538414, 0.020720533828083924, 0.025492531948419953, 0.029607440154383005, 0.03263821448952132] + [0.03424698620114449] * 2 + [0.03263821448952132, 0.029607440154383005, 0.025492531948419953, 0.020720533828083924, 0.015735160285538414, 0.010930613923990355, 0.006604892221159336, 0.0029388638683360566, 0.0],
        },
        "minus_y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0006316040056343379, -0.000810002220721428, -0.0009842440123493477, -0.0011286449159734998, -0.001214052138069595, -0.0012132381518087355, -0.0011073596801941049, -0.0008918175378462839, -0.0005796566432847614, -0.00020110429322099118, 0.00020110429322099118, 0.0005796566432847614, 0.0008918175378462839, 0.0011073596801941049, 0.0012132381518087355, 0.001214052138069595, 0.0011286449159734998, 0.0009842440123493477, 0.000810002220721428, 0.0006316040056343379],
        },
        "minus_y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.0014694319341680283, -0.003302446110579668, -0.005465306961995178, -0.007867580142769207, -0.010360266914041962, -0.012746265974209976, -0.014803720077191503, -0.01631910724476066] + [-0.017123493100572245] * 2 + [-0.01631910724476066, -0.014803720077191503, -0.012746265974209976, -0.010360266914041962, -0.007867580142769207, -0.005465306961995178, -0.003302446110579668, -0.0014694319341680283, 0.0],
        },
        "readout_wf_q1": {
            "type": "constant",
            "sample": 0.03,
        },
        "x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0036903687340989547, 0.008293847158990834, 0.013725710913054138, 0.019758840880460437, 0.026019037838692024, 0.03201129656568023, 0.03717843913073246, 0.04098422100685474] + [0.04300437610449062] * 2 + [0.04098422100685474, 0.03717843913073246, 0.03201129656568023, 0.026019037838692024, 0.019758840880460437, 0.013725710913054138, 0.008293847158990834, 0.0036903687340989547, 0.0],
        },
        "x90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0011588783203718474, 0.0014862065545394347, 0.001805908508642062, 0.0020708578679863986, 0.0022275645658657813, 0.0022260710493231762, 0.0020318033368740282, 0.0016363227609670977, 0.0010635643712987035, 0.00036898975223161474, -0.00036898975223161474, -0.0010635643712987035, -0.0016363227609670977, -0.0020318033368740282, -0.0022260710493231762, -0.0022275645658657813, -0.0020708578679863986, -0.001805908508642062, -0.0014862065545394347, -0.0011588783203718474],
        },
        "x180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.007350189844000168, 0.016519040656404346, 0.02733780503357896, 0.039354124759090094, 0.05182269888250199, 0.06375761444548136, 0.07404912771710057, 0.08162918849419357] + [0.08565277652883854] * 2 + [0.08162918849419357, 0.07404912771710057, 0.06375761444548136, 0.05182269888250199, 0.039354124759090094, 0.02733780503357896, 0.016519040656404346, 0.007350189844000168, 0.0],
        },
        "x180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.002308163837971841, 0.002960110793895892, 0.0035968683174569865, 0.00412457387496209, 0.00443669010567828, 0.004433715435417861, 0.004046788092936593, 0.003259100595567796, 0.0021183249164582092, 0.0007349251320966316, -0.0007349251320966316, -0.0021183249164582092, -0.003259100595567796, -0.004046788092936593, -0.004433715435417861, -0.00443669010567828, -0.00412457387496209, -0.0035968683174569865, -0.002960110793895892, -0.002308163837971841],
        },
        "minus_x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.0036903687340989547, -0.008293847158990834, -0.013725710913054138, -0.019758840880460437, -0.026019037838692024, -0.03201129656568023, -0.03717843913073246, -0.04098422100685474] + [-0.04300437610449062] * 2 + [-0.04098422100685474, -0.03717843913073246, -0.03201129656568023, -0.026019037838692024, -0.019758840880460437, -0.013725710913054138, -0.008293847158990834, -0.0036903687340989547, 0.0],
        },
        "minus_x90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.0011588783203718474, -0.0014862065545394347, -0.001805908508642062, -0.0020708578679863986, -0.0022275645658657813, -0.0022260710493231762, -0.0020318033368740282, -0.0016363227609670977, -0.0010635643712987035, -0.00036898975223161474, 0.00036898975223161474, 0.0010635643712987035, 0.0016363227609670977, 0.0020318033368740282, 0.0022260710493231762, 0.0022275645658657813, 0.0020708578679863986, 0.001805908508642062, 0.0014862065545394347, 0.0011588783203718474],
        },
        "y90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.0011588783203718474, -0.0014862065545394347, -0.001805908508642062, -0.0020708578679863986, -0.0022275645658657813, -0.0022260710493231762, -0.0020318033368740282, -0.0016363227609670977, -0.0010635643712987035, -0.00036898975223161474, 0.00036898975223161474, 0.0010635643712987035, 0.0016363227609670977, 0.0020318033368740282, 0.0022260710493231762, 0.0022275645658657813, 0.0020708578679863986, 0.001805908508642062, 0.0014862065545394347, 0.0011588783203718474],
        },
        "y90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0036903687340989547, 0.008293847158990834, 0.013725710913054138, 0.019758840880460437, 0.026019037838692024, 0.03201129656568023, 0.03717843913073246, 0.04098422100685474] + [0.04300437610449062] * 2 + [0.04098422100685474, 0.03717843913073246, 0.03201129656568023, 0.026019037838692024, 0.019758840880460437, 0.013725710913054138, 0.008293847158990834, 0.0036903687340989547, 0.0],
        },
        "y180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.002308163837971841, -0.002960110793895892, -0.0035968683174569865, -0.00412457387496209, -0.00443669010567828, -0.004433715435417861, -0.004046788092936593, -0.003259100595567796, -0.0021183249164582092, -0.0007349251320966316, 0.0007349251320966316, 0.0021183249164582092, 0.003259100595567796, 0.004046788092936593, 0.004433715435417861, 0.00443669010567828, 0.00412457387496209, 0.0035968683174569865, 0.002960110793895892, 0.002308163837971841],
        },
        "y180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.007350189844000168, 0.016519040656404346, 0.02733780503357896, 0.039354124759090094, 0.05182269888250199, 0.06375761444548136, 0.07404912771710057, 0.08162918849419357] + [0.08565277652883854] * 2 + [0.08162918849419357, 0.07404912771710057, 0.06375761444548136, 0.05182269888250199, 0.039354124759090094, 0.02733780503357896, 0.016519040656404346, 0.007350189844000168, 0.0],
        },
        "minus_y90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0011588783203718474, 0.0014862065545394347, 0.001805908508642062, 0.0020708578679863986, 0.0022275645658657813, 0.0022260710493231762, 0.0020318033368740282, 0.0016363227609670977, 0.0010635643712987035, 0.00036898975223161474, -0.00036898975223161474, -0.0010635643712987035, -0.0016363227609670977, -0.0020318033368740282, -0.0022260710493231762, -0.0022275645658657813, -0.0020708578679863986, -0.001805908508642062, -0.0014862065545394347, -0.0011588783203718474],
        },
        "minus_y90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.0036903687340989547, -0.008293847158990834, -0.013725710913054138, -0.019758840880460437, -0.026019037838692024, -0.03201129656568023, -0.03717843913073246, -0.04098422100685474] + [-0.04300437610449062] * 2 + [-0.04098422100685474, -0.03717843913073246, -0.03201129656568023, -0.026019037838692024, -0.019758840880460437, -0.013725710913054138, -0.008293847158990834, -0.0036903687340989547, 0.0],
        },
        "readout_wf_q2": {
            "type": "constant",
            "sample": 0.020999999999999998,
        },
        "x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.014896835639639595, 0.0334796024056238, 0.05540629520830214, 0.07976010697962901, 0.10503051540707237, 0.12921934308202135, 0.15007744130048106, 0.16544016279902943] + [0.17359488137172774] * 2 + [0.16544016279902943, 0.15007744130048106, 0.12921934308202135, 0.10503051540707237, 0.07976010697962901, 0.05540629520830214, 0.0334796024056238, 0.014896835639639595, 0.0],
        },
        "x90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.012994500842607316, -0.01666483183416049, -0.020249649358951873, -0.023220526122047704, -0.024977678086873876, -0.024960931288154662, -0.022782607724122637, -0.018348084628368743, -0.011925745676710533, -0.004137481530199539, 0.004137481530199539, 0.011925745676710533, 0.018348084628368743, 0.022782607724122637, 0.024960931288154662, 0.024977678086873876, 0.023220526122047704, 0.020249649358951873, 0.01666483183416049, 0.012994500842607316],
        },
        "x180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.024123603756755284, 0.05421612226276259, 0.08972372009517765, 0.12916174031302743, 0.17008407673545983, 0.2092549253832216, 0.24303206495256024, 0.26791011389002795] + [0.2811156834723467] * 2 + [0.26791011389002795, 0.24303206495256024, 0.2092549253832216, 0.17008407673545983, 0.12916174031302743, 0.08972372009517765, 0.05421612226276259, 0.024123603756755284, 0.0],
        },
        "x180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.021043005167469608, -0.02698665740598686, -0.03279183104153566, -0.037602802685229614, -0.04044829543048595, -0.04042117603773241, -0.03689364738776317, -0.029712479480701878, -0.01931228686200115, -0.006700145413421634, 0.006700145413421634, 0.01931228686200115, 0.029712479480701878, 0.03689364738776317, 0.04042117603773241, 0.04044829543048595, 0.037602802685229614, 0.03279183104153566, 0.02698665740598686, 0.021043005167469608],
        },
        "minus_x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.014896835639639595, -0.0334796024056238, -0.05540629520830214, -0.07976010697962901, -0.10503051540707237, -0.12921934308202135, -0.15007744130048106, -0.16544016279902943] + [-0.17359488137172774] * 2 + [-0.16544016279902943, -0.15007744130048106, -0.12921934308202135, -0.10503051540707237, -0.07976010697962901, -0.05540629520830214, -0.0334796024056238, -0.014896835639639595, 0.0],
        },
        "minus_x90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.012994500842607316, 0.01666483183416049, 0.020249649358951873, 0.023220526122047704, 0.024977678086873876, 0.024960931288154662, 0.022782607724122637, 0.018348084628368743, 0.011925745676710533, 0.004137481530199539, -0.004137481530199539, -0.011925745676710533, -0.018348084628368743, -0.022782607724122637, -0.024960931288154662, -0.024977678086873876, -0.023220526122047704, -0.020249649358951873, -0.01666483183416049, -0.012994500842607316],
        },
        "y90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.012994500842607316, 0.01666483183416049, 0.020249649358951873, 0.023220526122047704, 0.024977678086873876, 0.024960931288154662, 0.022782607724122637, 0.018348084628368743, 0.011925745676710533, 0.004137481530199539, -0.004137481530199539, -0.011925745676710533, -0.018348084628368743, -0.022782607724122637, -0.024960931288154662, -0.024977678086873876, -0.023220526122047704, -0.020249649358951873, -0.01666483183416049, -0.012994500842607316],
        },
        "y90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.014896835639639595, 0.0334796024056238, 0.05540629520830214, 0.07976010697962901, 0.10503051540707237, 0.12921934308202135, 0.15007744130048106, 0.16544016279902943] + [0.17359488137172774] * 2 + [0.16544016279902943, 0.15007744130048106, 0.12921934308202135, 0.10503051540707237, 0.07976010697962901, 0.05540629520830214, 0.0334796024056238, 0.014896835639639595, 0.0],
        },
        "y180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.021043005167469608, 0.02698665740598686, 0.03279183104153566, 0.037602802685229614, 0.04044829543048595, 0.04042117603773241, 0.03689364738776317, 0.029712479480701878, 0.01931228686200115, 0.006700145413421634, -0.006700145413421634, -0.01931228686200115, -0.029712479480701878, -0.03689364738776317, -0.04042117603773241, -0.04044829543048595, -0.037602802685229614, -0.03279183104153566, -0.02698665740598686, -0.021043005167469608],
        },
        "y180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.024123603756755284, 0.05421612226276259, 0.08972372009517765, 0.12916174031302743, 0.17008407673545983, 0.2092549253832216, 0.24303206495256024, 0.26791011389002795] + [0.2811156834723467] * 2 + [0.26791011389002795, 0.24303206495256024, 0.2092549253832216, 0.17008407673545983, 0.12916174031302743, 0.08972372009517765, 0.05421612226276259, 0.024123603756755284, 0.0],
        },
        "minus_y90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.012994500842607316, -0.01666483183416049, -0.020249649358951873, -0.023220526122047704, -0.024977678086873876, -0.024960931288154662, -0.022782607724122637, -0.018348084628368743, -0.011925745676710533, -0.004137481530199539, 0.004137481530199539, 0.011925745676710533, 0.018348084628368743, 0.022782607724122637, 0.024960931288154662, 0.024977678086873876, 0.023220526122047704, 0.020249649358951873, 0.01666483183416049, 0.012994500842607316],
        },
        "minus_y90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.014896835639639595, -0.0334796024056238, -0.05540629520830214, -0.07976010697962901, -0.10503051540707237, -0.12921934308202135, -0.15007744130048106, -0.16544016279902943] + [-0.17359488137172774] * 2 + [-0.16544016279902943, -0.15007744130048106, -0.12921934308202135, -0.10503051540707237, -0.07976010697962901, -0.05540629520830214, -0.0334796024056238, -0.014896835639639595, 0.0],
        },
        "readout_wf_q3": {
            "type": "constant",
            "sample": 0.0135,
        },
        "x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.005984439312228475, 0.013449611289316836, 0.022258123752617397, 0.03204167188945293, 0.04219344031112026, 0.05191071012307255, 0.06028994085209555, 0.06646153841165316] + [0.06973749711772612] * 2 + [0.06646153841165316, 0.06028994085209555, 0.05191071012307255, 0.04219344031112026, 0.03204167188945293, 0.022258123752617397, 0.013449611289316836, 0.005984439312228475, 0.0],
        },
        "x90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.004261406401946045, -0.005465051865062377, -0.006640654109041241, -0.007614921101747756, -0.008191160137228851, -0.008185668205207873, -0.007471310486222691, -0.006017056464562899, -0.003910919672118597, -0.0013568424439139993, 0.0013568424439139993, 0.003910919672118597, 0.006017056464562899, 0.007471310486222691, 0.008185668205207873, 0.008191160137228851, 0.007614921101747756, 0.006640654109041241, 0.005465051865062377, 0.004261406401946045],
        },
        "x180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.010950884409728578, 0.024611351356530586, 0.04072998783600022, 0.05863283540011151, 0.07720948673532474, 0.0949910520477832, 0.11032414882904325, 0.12161751283057597] + [0.12761216717487578] * 2 + [0.12161751283057597, 0.11032414882904325, 0.0949910520477832, 0.07720948673532474, 0.05863283540011151, 0.04072998783600022, 0.024611351356530586, 0.010950884409728578, 0.0],
        },
        "x180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.007797918317131542, -0.010000460886148399, -0.012151687361003586, -0.013934491841874829, -0.014988947696583318, -0.014978898047884407, -0.01367169976252139, -0.011010570312843833, -0.007156565056577729, -0.0024828766723649525, 0.0024828766723649525, 0.007156565056577729, 0.011010570312843833, 0.01367169976252139, 0.014978898047884407, 0.014988947696583318, 0.013934491841874829, 0.012151687361003586, 0.010000460886148399, 0.007797918317131542],
        },
        "minus_x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.005984439312228475, -0.013449611289316836, -0.022258123752617397, -0.03204167188945293, -0.04219344031112026, -0.05191071012307255, -0.06028994085209555, -0.06646153841165316] + [-0.06973749711772612] * 2 + [-0.06646153841165316, -0.06028994085209555, -0.05191071012307255, -0.04219344031112026, -0.03204167188945293, -0.022258123752617397, -0.013449611289316836, -0.005984439312228475, 0.0],
        },
        "minus_x90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.004261406401946045, 0.005465051865062377, 0.006640654109041241, 0.007614921101747756, 0.008191160137228851, 0.008185668205207873, 0.007471310486222691, 0.006017056464562899, 0.003910919672118597, 0.0013568424439139993, -0.0013568424439139993, -0.003910919672118597, -0.006017056464562899, -0.007471310486222691, -0.008185668205207873, -0.008191160137228851, -0.007614921101747756, -0.006640654109041241, -0.005465051865062377, -0.004261406401946045],
        },
        "y90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.004261406401946045, 0.005465051865062377, 0.006640654109041241, 0.007614921101747756, 0.008191160137228851, 0.008185668205207873, 0.007471310486222691, 0.006017056464562899, 0.003910919672118597, 0.0013568424439139993, -0.0013568424439139993, -0.003910919672118597, -0.006017056464562899, -0.007471310486222691, -0.008185668205207873, -0.008191160137228851, -0.007614921101747756, -0.006640654109041241, -0.005465051865062377, -0.004261406401946045],
        },
        "y90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.005984439312228475, 0.013449611289316836, 0.022258123752617397, 0.03204167188945293, 0.04219344031112026, 0.05191071012307255, 0.06028994085209555, 0.06646153841165316] + [0.06973749711772612] * 2 + [0.06646153841165316, 0.06028994085209555, 0.05191071012307255, 0.04219344031112026, 0.03204167188945293, 0.022258123752617397, 0.013449611289316836, 0.005984439312228475, 0.0],
        },
        "y180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.007797918317131542, 0.010000460886148399, 0.012151687361003586, 0.013934491841874829, 0.014988947696583318, 0.014978898047884407, 0.01367169976252139, 0.011010570312843833, 0.007156565056577729, 0.0024828766723649525, -0.0024828766723649525, -0.007156565056577729, -0.011010570312843833, -0.01367169976252139, -0.014978898047884407, -0.014988947696583318, -0.013934491841874829, -0.012151687361003586, -0.010000460886148399, -0.007797918317131542],
        },
        "y180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.010950884409728578, 0.024611351356530586, 0.04072998783600022, 0.05863283540011151, 0.07720948673532474, 0.0949910520477832, 0.11032414882904325, 0.12161751283057597] + [0.12761216717487578] * 2 + [0.12161751283057597, 0.11032414882904325, 0.0949910520477832, 0.07720948673532474, 0.05863283540011151, 0.04072998783600022, 0.024611351356530586, 0.010950884409728578, 0.0],
        },
        "minus_y90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.004261406401946045, -0.005465051865062377, -0.006640654109041241, -0.007614921101747756, -0.008191160137228851, -0.008185668205207873, -0.007471310486222691, -0.006017056464562899, -0.003910919672118597, -0.0013568424439139993, 0.0013568424439139993, 0.003910919672118597, 0.006017056464562899, 0.007471310486222691, 0.008185668205207873, 0.008191160137228851, 0.007614921101747756, 0.006640654109041241, 0.005465051865062377, 0.004261406401946045],
        },
        "minus_y90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.005984439312228475, -0.013449611289316836, -0.022258123752617397, -0.03204167188945293, -0.04219344031112026, -0.05191071012307255, -0.06028994085209555, -0.06646153841165316] + [-0.06973749711772612] * 2 + [-0.06646153841165316, -0.06028994085209555, -0.05191071012307255, -0.04219344031112026, -0.03204167188945293, -0.022258123752617397, -0.013449611289316836, -0.005984439312228475, 0.0],
        },
        "readout_wf_q4": {
            "type": "constant",
            "sample": 0.03,
        },
        "x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.017817904994677156, 0.04004450269529871, 0.06627072540839607, 0.09539999251563863, 0.12562558857032988, 0.15455752041617832, 0.17950561150186015, 0.19788075631398627] + [0.20763450565388186] * 2 + [0.19788075631398627, 0.17950561150186015, 0.15455752041617832, 0.12562558857032988, 0.09539999251563863, 0.06627072540839607, 0.04004450269529871, 0.017817904994677156, 0.0],
        },
        "x90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0] * 20,
        },
        "x180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.03563580998935431, 0.08008900539059742, 0.13254145081679214, 0.19079998503127726, 0.25125117714065975, 0.30911504083235664, 0.3590112230037203, 0.39576151262797254] + [0.4152690113077637] * 2 + [0.39576151262797254, 0.3590112230037203, 0.30911504083235664, 0.25125117714065975, 0.19079998503127726, 0.13254145081679214, 0.08008900539059742, 0.03563580998935431, 0.0],
        },
        "x180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0] * 20,
        },
        "minus_x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.017817904994677156, -0.04004450269529871, -0.06627072540839607, -0.09539999251563863, -0.12562558857032988, -0.15455752041617832, -0.17950561150186015, -0.19788075631398627] + [-0.20763450565388186] * 2 + [-0.19788075631398627, -0.17950561150186015, -0.15455752041617832, -0.12562558857032988, -0.09539999251563863, -0.06627072540839607, -0.04004450269529871, -0.017817904994677156, 0.0],
        },
        "minus_x90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0] * 20,
        },
        "y90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0] * 20,
        },
        "y90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.017817904994677156, 0.04004450269529871, 0.06627072540839607, 0.09539999251563863, 0.12562558857032988, 0.15455752041617832, 0.17950561150186015, 0.19788075631398627] + [0.20763450565388186] * 2 + [0.19788075631398627, 0.17950561150186015, 0.15455752041617832, 0.12562558857032988, 0.09539999251563863, 0.06627072540839607, 0.04004450269529871, 0.017817904994677156, 0.0],
        },
        "y180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0] * 20,
        },
        "y180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.03563580998935431, 0.08008900539059742, 0.13254145081679214, 0.19079998503127726, 0.25125117714065975, 0.30911504083235664, 0.3590112230037203, 0.39576151262797254] + [0.4152690113077637] * 2 + [0.39576151262797254, 0.3590112230037203, 0.30911504083235664, 0.25125117714065975, 0.19079998503127726, 0.13254145081679214, 0.08008900539059742, 0.03563580998935431, 0.0],
        },
        "minus_y90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0] * 20,
        },
        "minus_y90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.017817904994677156, -0.04004450269529871, -0.06627072540839607, -0.09539999251563863, -0.12562558857032988, -0.15455752041617832, -0.17950561150186015, -0.19788075631398627] + [-0.20763450565388186] * 2 + [-0.19788075631398627, -0.17950561150186015, -0.15455752041617832, -0.12562558857032988, -0.09539999251563863, -0.06627072540839607, -0.04004450269529871, -0.017817904994677156, 0.0],
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
        "q2_z_baked_wf_0": {
            "type": "arbitrary",
            "samples": [0.0] * 16,
            "is_overridable": False,
        },
        "q2_z_baked_wf_1": {
            "type": "arbitrary",
            "samples": [0.5] + [0] * 15,
            "is_overridable": False,
        },
        "q2_z_baked_wf_2": {
            "type": "arbitrary",
            "samples": [0.5] * 2 + [0] * 14,
            "is_overridable": False,
        },
        "q2_z_baked_wf_3": {
            "type": "arbitrary",
            "samples": [0.5] * 3 + [0] * 13,
            "is_overridable": False,
        },
        "q2_z_baked_wf_4": {
            "type": "arbitrary",
            "samples": [0.5] * 4 + [0] * 12,
            "is_overridable": False,
        },
        "q2_z_baked_wf_5": {
            "type": "arbitrary",
            "samples": [0.5] * 5 + [0] * 11,
            "is_overridable": False,
        },
        "q2_z_baked_wf_6": {
            "type": "arbitrary",
            "samples": [0.5] * 6 + [0] * 10,
            "is_overridable": False,
        },
        "q2_z_baked_wf_7": {
            "type": "arbitrary",
            "samples": [0.5] * 7 + [0] * 9,
            "is_overridable": False,
        },
        "q2_z_baked_wf_8": {
            "type": "arbitrary",
            "samples": [0.5] * 8 + [0] * 8,
            "is_overridable": False,
        },
        "q2_z_baked_wf_9": {
            "type": "arbitrary",
            "samples": [0.5] * 9 + [0] * 7,
            "is_overridable": False,
        },
        "q2_z_baked_wf_10": {
            "type": "arbitrary",
            "samples": [0.5] * 10 + [0] * 6,
            "is_overridable": False,
        },
        "q2_z_baked_wf_11": {
            "type": "arbitrary",
            "samples": [0.5] * 11 + [0] * 5,
            "is_overridable": False,
        },
        "q2_z_baked_wf_12": {
            "type": "arbitrary",
            "samples": [0.5] * 12 + [0] * 4,
            "is_overridable": False,
        },
        "q2_z_baked_wf_13": {
            "type": "arbitrary",
            "samples": [0.5] * 13 + [0] * 3,
            "is_overridable": False,
        },
        "q2_z_baked_wf_14": {
            "type": "arbitrary",
            "samples": [0.5] * 14 + [0] * 2,
            "is_overridable": False,
        },
        "q2_z_baked_wf_15": {
            "type": "arbitrary",
            "samples": [0.5] * 15 + [0],
            "is_overridable": False,
        },
        "q2_z_baked_wf_16": {
            "type": "arbitrary",
            "samples": [0.5] * 16,
            "is_overridable": False,
        },
        "q2_z_baked_wf_17": {
            "type": "arbitrary",
            "samples": [0.5] * 17 + [0] * 3,
            "is_overridable": False,
        },
        "q2_z_baked_wf_18": {
            "type": "arbitrary",
            "samples": [0.5] * 18 + [0] * 2,
            "is_overridable": False,
        },
        "q2_z_baked_wf_19": {
            "type": "arbitrary",
            "samples": [0.5] * 19 + [0],
            "is_overridable": False,
        },
        "q2_z_baked_wf_20": {
            "type": "arbitrary",
            "samples": [0.5] * 20,
            "is_overridable": False,
        },
        "q2_z_baked_wf_21": {
            "type": "arbitrary",
            "samples": [0.5] * 21 + [0] * 3,
            "is_overridable": False,
        },
        "q2_z_baked_wf_22": {
            "type": "arbitrary",
            "samples": [0.5] * 22 + [0] * 2,
            "is_overridable": False,
        },
        "q2_z_baked_wf_23": {
            "type": "arbitrary",
            "samples": [0.5] * 23 + [0],
            "is_overridable": False,
        },
        "q2_z_baked_wf_24": {
            "type": "arbitrary",
            "samples": [0.5] * 24,
            "is_overridable": False,
        },
        "q2_z_baked_wf_25": {
            "type": "arbitrary",
            "samples": [0.5] * 25 + [0] * 3,
            "is_overridable": False,
        },
        "q2_z_baked_wf_26": {
            "type": "arbitrary",
            "samples": [0.5] * 26 + [0] * 2,
            "is_overridable": False,
        },
        "q2_z_baked_wf_27": {
            "type": "arbitrary",
            "samples": [0.5] * 27 + [0],
            "is_overridable": False,
        },
        "q2_z_baked_wf_28": {
            "type": "arbitrary",
            "samples": [0.5] * 28,
            "is_overridable": False,
        },
        "q2_z_baked_wf_29": {
            "type": "arbitrary",
            "samples": [0.5] * 29 + [0] * 3,
            "is_overridable": False,
        },
        "q2_z_baked_wf_30": {
            "type": "arbitrary",
            "samples": [0.5] * 30 + [0] * 2,
            "is_overridable": False,
        },
        "q2_z_baked_wf_31": {
            "type": "arbitrary",
            "samples": [0.5] * 31 + [0],
            "is_overridable": False,
        },
        "q2_z_baked_wf_32": {
            "type": "arbitrary",
            "samples": [0.5] * 32,
            "is_overridable": False,
        },
        "q2_z_baked_wf_33": {
            "type": "arbitrary",
            "samples": [0.5] * 33 + [0] * 3,
            "is_overridable": False,
        },
        "q2_z_baked_wf_34": {
            "type": "arbitrary",
            "samples": [0.5] * 34 + [0] * 2,
            "is_overridable": False,
        },
        "q2_z_baked_wf_35": {
            "type": "arbitrary",
            "samples": [0.5] * 35 + [0],
            "is_overridable": False,
        },
        "q2_z_baked_wf_36": {
            "type": "arbitrary",
            "samples": [0.5] * 36,
            "is_overridable": False,
        },
        "q2_z_baked_wf_37": {
            "type": "arbitrary",
            "samples": [0.5] * 37 + [0] * 3,
            "is_overridable": False,
        },
        "q2_z_baked_wf_38": {
            "type": "arbitrary",
            "samples": [0.5] * 38 + [0] * 2,
            "is_overridable": False,
        },
        "q2_z_baked_wf_39": {
            "type": "arbitrary",
            "samples": [0.5] * 39 + [0],
            "is_overridable": False,
        },
        "q2_z_baked_wf_40": {
            "type": "arbitrary",
            "samples": [0.5] * 40,
            "is_overridable": False,
        },
        "q2_z_baked_wf_41": {
            "type": "arbitrary",
            "samples": [0.5] * 41 + [0] * 3,
            "is_overridable": False,
        },
        "q2_z_baked_wf_42": {
            "type": "arbitrary",
            "samples": [0.5] * 42 + [0] * 2,
            "is_overridable": False,
        },
        "q2_z_baked_wf_43": {
            "type": "arbitrary",
            "samples": [0.5] * 43 + [0],
            "is_overridable": False,
        },
        "q2_z_baked_wf_44": {
            "type": "arbitrary",
            "samples": [0.5] * 44,
            "is_overridable": False,
        },
        "q2_z_baked_wf_45": {
            "type": "arbitrary",
            "samples": [0.5] * 45 + [0] * 3,
            "is_overridable": False,
        },
        "q2_z_baked_wf_46": {
            "type": "arbitrary",
            "samples": [0.5] * 46 + [0] * 2,
            "is_overridable": False,
        },
        "q2_z_baked_wf_47": {
            "type": "arbitrary",
            "samples": [0.5] * 47 + [0],
            "is_overridable": False,
        },
        "q2_z_baked_wf_48": {
            "type": "arbitrary",
            "samples": [0.5] * 48,
            "is_overridable": False,
        },
        "q2_z_baked_wf_49": {
            "type": "arbitrary",
            "samples": [0.5] * 49 + [0] * 3,
            "is_overridable": False,
        },
        "q2_z_baked_wf_50": {
            "type": "arbitrary",
            "samples": [0.5] * 50 + [0] * 2,
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
            "cosine": [(0.0, 400), (0.8746197071393959, 1700)],
            "sine": [(0.0, 400), (0.484809620246337, 1700)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(0.0, 400), (-0.484809620246337, 1700)],
            "sine": [(0.0, 400), (0.8746197071393959, 1700)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(0.0, 400), (0.484809620246337, 1700)],
            "sine": [(0.0, 400), (-0.8746197071393959, 1700)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(0.0, 400), (-0.22835087011065508, 1700)],
            "sine": [(0.0, 400), (0.9735789028731604, 1700)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(0.0, 400), (-0.9735789028731604, 1700)],
            "sine": [(0.0, 400), (-0.22835087011065508, 1700)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(0.0, 400), (0.9735789028731604, 1700)],
            "sine": [(0.0, 400), (0.22835087011065508, 1700)],
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
        "octave_octave1_2": [
            {'intermediate_frequency': -99000000, 'lo_frequency': 3955000000, 'correction': [1.013119876384735, 0.09918718785047531, 0.09893324971199036, 1.0157203152775764]},
            {'intermediate_frequency': -19700000, 'lo_frequency': 4055000000, 'correction': [1.0119290761649609, 0.10491481050848961, 0.10407295450568199, 1.0201146677136421]},
            {'intermediate_frequency': -116555000, 'lo_frequency': 4055000000, 'correction': [1.0, 0.0, 0.0, 1.0]},
            {'intermediate_frequency': -180000000, 'lo_frequency': 3700000000, 'correction': [1.0489636659622192, 0.1246739886701107, 0.1308462880551815, 0.9994818046689034]},
            {'intermediate_frequency': -180000000, 'lo_frequency': 3600000000, 'correction': [1.04962208122015, 0.1469372734427452, 0.15197580307722092, 1.0148234367370605]},
            {'intermediate_frequency': -106900000, 'lo_frequency': 3300000000, 'correction': [1.0321827754378319, 0.14756997302174568, 0.14784042909741402, 1.0302945226430893]},
            {'intermediate_frequency': -75347000, 'lo_frequency': 3600000000, 'correction': [0.9735809303820133, 0.10057862102985382, 0.09262080490589142, 1.057229284197092]},
            {'intermediate_frequency': -75347000, 'lo_frequency': 3300000000, 'correction': [0.8311591409146786, 0.06552650406956673, 0.042722437530756, 1.2748090960085392]},
            {'intermediate_frequency': -75347000, 'lo_frequency': 3400000000, 'correction': [0.8424716293811798, 0.12053202837705612, 0.07945621013641357, 1.2779971845448017]},
            {'intermediate_frequency': -75347000, 'lo_frequency': 3500000000, 'correction': [0.9035251215100288, 0.11854912713170052, 0.09229253605008125, 1.1605717912316322]},
            {'intermediate_frequency': -75347000, 'lo_frequency': 3450000000, 'correction': [1.0572927705943584, 0.16472642496228218, 0.17032818868756294, 1.0225204639136791]},
            {'intermediate_frequency': -75347000, 'lo_frequency': 3490000000, 'correction': [1.0568718202412128, 0.16134490072727203, 0.1671576388180256, 1.020120169967413]},
            {'intermediate_frequency': -75347000, 'lo_frequency': 3470000000, 'correction': [1.0582309402525425, 0.16638235747814178, 0.17209291458129883, 1.0231156758964062]},
            {'intermediate_frequency': -75347000, 'lo_frequency': 3480000000, 'correction': [1.0578176230192184, 0.1646474227309227, 0.17041274160146713, 1.0220300629734993]},
            {'intermediate_frequency': 0, 'lo_frequency': 3400000000, 'correction': [1.0217774510383606, -0.06147767975926399, -0.0634308010339737, 0.990315493196249]},
            {'intermediate_frequency': 0, 'lo_frequency': 3500000000, 'correction': [0.9954007379710674, -0.01472121849656105, -0.014576379209756851, 1.0052916146814823]},
            {'intermediate_frequency': 0, 'lo_frequency': 3300000000, 'correction': [1.0264127254486084, -0.1157689206302166, -0.11727301776409149, 1.0132483467459679]},
            {'intermediate_frequency': -304480000, 'lo_frequency': 3600000000, 'correction': [1.057143833488226, 0.14593342691659927, 0.15306488424539566, 1.0078903697431087]},
            {'intermediate_frequency': -75347000, 'lo_frequency': 3250000000, 'correction': [0.8448452353477478, 0.06274132430553436, 0.04271237924695015, 1.2410151027143002]},
            {'intermediate_frequency': -219319700, 'lo_frequency': 3400000000, 'correction': [0.8503554277122021, 0.14416301622986794, 0.0959322489798069, 1.2778789550065994]},
            {'intermediate_frequency': -212940000, 'lo_frequency': 3400000000, 'correction': [0.8512887433171272, 0.1404735930263996, 0.09394824504852295, 1.2728666476905346]},
            {'intermediate_frequency': -111450000, 'lo_frequency': 3300000000, 'correction': [0.8267116844654083, 0.07013754174113274, 0.04501013085246086, 1.2882327288389206]},
            {'intermediate_frequency': -311450000, 'lo_frequency': 3500000000, 'correction': [0.903420016169548, 0.13715070486068726, 0.10555890202522278, 1.173796709626913]},
            {'intermediate_frequency': -323810000, 'lo_frequency': 3500000000, 'correction': [0.9072245135903358, 0.14272667840123177, 0.11047400906682014, 1.1720869168639183]},
            {'intermediate_frequency': -123450000, 'lo_frequency': 3300000000, 'correction': [0.8232660032808781, 0.0764295905828476, 0.048388704657554626, 1.3003423810005188]},
            {'intermediate_frequency': -44900000, 'lo_frequency': 3600000000, 'correction': [0.972774438560009, 0.09726535901427269, 0.0895751379430294, 1.0562892481684685]},
            {'intermediate_frequency': -44900000, 'lo_frequency': 3300000000, 'correction': [0.8353546001017094, 0.058258358389139175, 0.03857475146651268, 1.2616125121712685]},
            {'intermediate_frequency': -45153000, 'lo_frequency': 3600000000, 'correction': [0.9726689234375954, 0.09730951488018036, 0.08959399908781052, 1.0564316809177399]},
            {'intermediate_frequency': 0, 'lo_frequency': 3450000000, 'correction': [1.0103772543370724, 0.06671024858951569, 0.06720269098877907, 1.002973522990942]},
            {'intermediate_frequency': 0, 'lo_frequency': 3550000000, 'correction': [1.0063092857599258, 0.06578866764903069, 0.06577260792255402, 1.0065549947321415]},
            {'intermediate_frequency': -45153000, 'lo_frequency': 3300000000, 'correction': [0.835892666131258, 0.0580032654106617, 0.03847326338291168, 1.2602129317820072]},
            {'intermediate_frequency': -94914000, 'lo_frequency': 3350000000, 'correction': [0.8321215026080608, 0.10824720561504364, 0.06955806910991669, 1.2949587032198906]},
            {'intermediate_frequency': -180380000, 'lo_frequency': 3400000000, 'correction': [0.8546344377100468, 0.14139743894338608, 0.09542854875326157, 1.2663204222917557]},
            {'intermediate_frequency': -263340000, 'lo_frequency': 2830000000, 'correction': [0.9499963894486427, -0.12157641351222992, -0.10519857704639435, 1.0978965424001217]},
            {'intermediate_frequency': -263340000, 'lo_frequency': 2850000000, 'correction': [0.9729656428098679, -0.14889118820428848, -0.1328480914235115, 1.0904636196792126]},
            {'intermediate_frequency': 0, 'lo_frequency': 2900000000, 'correction': [1.0533747859299183, -0.21467778086662292, -0.2113431952893734, 1.0699949972331524]},
            {'intermediate_frequency': 271700000, 'lo_frequency': 3160000000, 'correction': [0.7852009236812592, 0.1171339750289917, 0.06303155422210693, 1.4591692462563515]},
            {'intermediate_frequency': -100000000, 'lo_frequency': 3600000000, 'correction': [0.9744591005146503, 0.10126551985740662, 0.0933896005153656, 1.056639138609171]},
            {'intermediate_frequency': -71300000, 'lo_frequency': 3600000000, 'correction': [0.9739216528832912, 0.1005404032766819, 0.09265321865677834, 1.0568275637924671]},
            {'intermediate_frequency': -71271000, 'lo_frequency': 3600000000, 'correction': [0.9718846864998341, 0.09998255223035812, 0.09177558869123459, 1.0587947480380535]},
            {'intermediate_frequency': -171355000, 'lo_frequency': 3700000000, 'correction': [1.0683668591082096, 0.09722131118178368, 0.1073865257203579, 0.967235192656517]},
            {'intermediate_frequency': -41355000, 'lo_frequency': 3570000000, 'correction': [0.94725676253438, 0.10438976809382439, 0.0906716100871563, 1.090571939945221]},
            {'intermediate_frequency': -71355000, 'lo_frequency': 3600000000, 'correction': [0.973212119191885, 0.10062005370855331, 0.0925857201218605, 1.0576647818088531]},
            {'intermediate_frequency': -221355000, 'lo_frequency': 3750000000, 'correction': [1.1707491278648376, 0.0713556632399559, 0.09405063837766647, 0.8882404454052448]},
            {'intermediate_frequency': -271355000, 'lo_frequency': 3800000000, 'correction': [1.1806640625, 0.0, 0.0, 0.8681640625]},
            {'intermediate_frequency': -321355000, 'lo_frequency': 3850000000, 'correction': [1.2244436033070087, -0.0264892578125, -0.0382080078125, 0.8488954044878483]},
            {'intermediate_frequency': -317056000, 'lo_frequency': 3850000000, 'correction': [1.2244436033070087, -0.0264892578125, -0.0382080078125, 0.8488954044878483]},
            {'intermediate_frequency': -317506000, 'lo_frequency': 3850000000, 'correction': [1.2244436033070087, -0.0264892578125, -0.0382080078125, 0.8488954044878483]},
            {'intermediate_frequency': -317621000, 'lo_frequency': 3850000000, 'correction': [1.2244436033070087, -0.0264892578125, -0.0382080078125, 0.8488954044878483]},
            {'intermediate_frequency': -316997000, 'lo_frequency': 3850000000, 'correction': [1.2244436033070087, -0.0264892578125, -0.0382080078125, 0.8488954044878483]},
        ],
        "octave_octave1_3": [{'intermediate_frequency': -317033000.0, 'lo_frequency': 3850000000.0, 'correction': (1, 0, 0, 1)}],
        "octave_octave1_4": [
            {'intermediate_frequency': -183200000, 'lo_frequency': 4215000000, 'correction': [1.0195316150784492, 0.1470695324242115, 0.14397891238331795, 1.0414166562259197]},
            {'intermediate_frequency': -124240000, 'lo_frequency': 4215000000, 'correction': [1.0156753063201904, 0.13932431116700172, 0.1361636109650135, 1.0392516888678074]},
            {'intermediate_frequency': -89090000, 'lo_frequency': 4215000000, 'correction': [1.0156761929392815, 0.13591918721795082, 0.13315223529934883, 1.0367823131382465]},
            {'intermediate_frequency': -98700000, 'lo_frequency': 4300000000, 'correction': [1.0164888240396976, 0.15053614974021912, 0.14615928754210472, 1.0469284355640411]},
            {'intermediate_frequency': -199070000, 'lo_frequency': 4400000000, 'correction': [1.0523961372673512, 0.22627202793955803, 0.22010232135653496, 1.0818959400057793]},
            {'intermediate_frequency': -100000000, 'lo_frequency': 3950000000, 'correction': [1.0145268887281418, 0.10615788772702217, 0.10575692728161812, 1.0183733068406582]},
            {'intermediate_frequency': -92000000, 'lo_frequency': 4750000000, 'correction': [1.2626258842647076, -0.06113452836871147, -0.0917474739253521, 0.8413314782083035]},
            {'intermediate_frequency': -104553000, 'lo_frequency': 3950000000, 'correction': [1.0146872736513615, 0.1068982370197773, 0.10648148134350777, 1.0186586380004883]},
            {'intermediate_frequency': -104644000, 'lo_frequency': 3950000000, 'correction': [1.0146501511335373, 0.1067759282886982, 0.10635964944958687, 1.0186213664710522]},
            {'intermediate_frequency': 145356000, 'lo_frequency': 3700000000, 'correction': [1.0465690642595291, 0.12968942895531654, 0.13506833091378212, 1.0048909559845924]},
            {'intermediate_frequency': -104255000, 'lo_frequency': 3950000000, 'correction': [1.0146176889538765, 0.10666890814900398, 0.10625304654240608, 1.0185887776315212]},
            {'intermediate_frequency': -108804000, 'lo_frequency': 3950000000, 'correction': [1.291191428899765, -0.02564239501953125, -0.04029083251953125, 0.8217561803758144]},
            {'intermediate_frequency': -89224000, 'lo_frequency': 3950000000, 'correction': [1.3129526637494564, -0.025405913591384888, -0.04096987843513489, 0.8141777105629444]},
            {'intermediate_frequency': -89843100, 'lo_frequency': 3700000000, 'correction': [1.053178545087576, 0.11116083711385727, 0.11857058852910995, 0.9873629733920097]},
            {'intermediate_frequency': -89843100, 'lo_frequency': 3800000000, 'correction': [1.2052510380744934, 0.08051718771457672, 0.11098207533359528, 0.8744062930345535]},
            {'intermediate_frequency': -83683100, 'lo_frequency': 3950000000, 'correction': [1.3144186958670616, -0.025390625, -0.041015625, 0.813687764108181]},
            {'intermediate_frequency': -89591100, 'lo_frequency': 3950000000, 'correction': [1.3041965961456299, -0.025498896837234497, -0.0406966507434845, 0.8171575255692005]},
            {'intermediate_frequency': 60408900, 'lo_frequency': 3800000000, 'correction': [1.1611689329147339, 0.03826643526554108, 0.050318971276283264, 0.8830426223576069]},
            {'intermediate_frequency': -100000000, 'lo_frequency': 3700000000, 'correction': [1.0544711574912071, 0.11347914859652519, 0.12114669010043144, 0.987732220441103]},
            {'intermediate_frequency': 0, 'lo_frequency': 3650000000, 'correction': [1.0184053964912891, 0.09133800119161606, 0.09241463989019394, 1.006540883332491]},
            {'intermediate_frequency': -204624000, 'lo_frequency': 4400000000, 'correction': [1.3294866308569908, -0.076171875, -0.123046875, 0.823015533387661]},
            {'intermediate_frequency': -100000000, 'lo_frequency': 4300000000, 'correction': [1.3338770642876625, -0.07925070822238922, -0.12846030294895172, 0.8229055926203728]},
            {'intermediate_frequency': -99092000, 'lo_frequency': 4100000000, 'correction': [1.368718508630991, -0.07504212856292725, -0.12667787075042725, 0.8108089417219162]},
            {'intermediate_frequency': -99092000, 'lo_frequency': 3900000000, 'correction': [1.2864418029785156, 0.0, 0.0, 0.8215980529785156]},
            {'intermediate_frequency': -99092000, 'lo_frequency': 3750000000, 'correction': [1.1356204822659492, 0.11233504116535187, 0.13724716007709503, 0.9294908083975315]},
            {'intermediate_frequency': -99092000, 'lo_frequency': 4300000000, 'correction': [1.3338770642876625, -0.07925070822238922, -0.12846030294895172, 0.8229055926203728]},
            {'intermediate_frequency': -100867000, 'lo_frequency': 4300000000, 'correction': [1.3372232988476753, -0.07994802296161652, -0.13003499805927277, 0.8221506550908089]},
            {'intermediate_frequency': -79153000, 'lo_frequency': 4280000000, 'correction': [1.34736917167902, -0.0852380208671093, -0.13982633873820305, 0.8213551342487335]},
            {'intermediate_frequency': -99153000, 'lo_frequency': 4300000000, 'correction': [1.3353672809898853, -0.07920349016785622, -0.12860381975769997, 0.8224152997136116]},
            {'intermediate_frequency': -99071000, 'lo_frequency': 4300000000, 'correction': [1.0, 0.0, 0.0, 1.0]},
            {'intermediate_frequency': -89863100, 'lo_frequency': 3950000000, 'correction': [1.0, 0.0, 0.0, 1.0]},
            {'intermediate_frequency': -100471000, 'lo_frequency': 4300000000, 'correction': [1.3294866308569908, -0.076171875, -0.123046875, 0.823015533387661]},
            {'intermediate_frequency': -101613000, 'lo_frequency': 4300000000, 'correction': [1.3294866308569908, -0.076171875, -0.123046875, 0.823015533387661]},
            {'intermediate_frequency': -101584000, 'lo_frequency': 4300000000, 'correction': [1.3338770642876625, -0.07925070822238922, -0.12846030294895172, 0.8229055926203728]},
            {'intermediate_frequency': -101721000, 'lo_frequency': 4300000000, 'correction': [1.3338770642876625, -0.07925070822238922, -0.12846030294895172, 0.8229055926203728]},
            {'intermediate_frequency': -101616000, 'lo_frequency': 4300000000, 'correction': [1.3289823047816753, -0.077796820551157, -0.1254965104162693, 0.8238523602485657]},
            {'intermediate_frequency': -101596000.0, 'lo_frequency': 4300000000.0, 'correction': (1, 0, 0, 1)},
        ],
        "octave_octave1_5": [{'intermediate_frequency': -89863100.0, 'lo_frequency': 3950000000.0, 'correction': (1, 0, 0, 1)}],
        "octave_octave2_1": [{'intermediate_frequency': -92000000.0, 'lo_frequency': 4750000000.0, 'correction': (1, 0, 0, 1)}],
        "octave_octave1_1": [
            {'intermediate_frequency': -214510000, 'lo_frequency': 5950000000, 'correction': [1.004735816270113, 0.06405084580183029, 0.06387906521558762, 1.0074377059936523]},
            {'intermediate_frequency': -214210000, 'lo_frequency': 5950000000, 'correction': [1.1034728735685349, -0.1470947265625, -0.1666259765625, 0.9741280674934387]},
            {'intermediate_frequency': 75133000, 'lo_frequency': 5950000000, 'correction': [1.0926973298192024, -0.16419601440429688, -0.18030929565429688, 0.9950487911701202]},
            {'intermediate_frequency': 75159000, 'lo_frequency': 5950000000, 'correction': [1.0926973298192024, -0.16419601440429688, -0.18030929565429688, 0.9950487911701202]},
            {'intermediate_frequency': -103150000, 'lo_frequency': 5950000000, 'correction': [1.0855363868176937, -0.14926910400390625, -0.16391754150390625, 0.9885277822613716]},
            {'intermediate_frequency': 163060000, 'lo_frequency': 5950000000, 'correction': [1.1003425158560276, -0.1791229248046875, -0.1967010498046875, 1.002010766416788]},
            {'intermediate_frequency': -25800000, 'lo_frequency': 5950000000, 'correction': [1.0935042686760426, -0.15615427494049072, -0.17281687259674072, 0.9880711510777473]},
            {'intermediate_frequency': 75079000, 'lo_frequency': 5950000000, 'correction': [1.0926973298192024, -0.16419601440429688, -0.18030929565429688, 0.9950487911701202]},
            {'intermediate_frequency': -103170000, 'lo_frequency': 5950000000, 'correction': [1.0855363868176937, -0.14926910400390625, -0.16391754150390625, 0.9885277822613716]},
            {'intermediate_frequency': -103970000, 'lo_frequency': 5950000000, 'correction': [1.0855363868176937, -0.14926910400390625, -0.16391754150390625, 0.9885277822613716]},
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
                    "offset": 0.0009765625,
                    "delay": 0,
                    "shareable": False,
                },
                "2": {
                    "offset": -0.0068359375,
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
            "intermediate_frequency": 101596000.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q2",
                "x90": "x90_pulse_q2",
                "-x90": "-x90_pulse_q2",
                "y90": "y90_pulse_q2",
                "y180": "y180_pulse_q2",
                "-y90": "-y90_pulse_q2",
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
            "intermediate_frequency": 317033000.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q3",
                "x90": "x90_pulse_q3",
                "-x90": "-x90_pulse_q3",
                "y90": "y90_pulse_q3",
                "y180": "y180_pulse_q3",
                "-y90": "-y90_pulse_q3",
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
            "length": 20,
            "waveforms": {
                "I": "x90_I_wf_q1",
                "Q": "x90_Q_wf_q1",
            },
            "operation": "control",
        },
        "x180_pulse_q1": {
            "length": 20,
            "waveforms": {
                "I": "x180_I_wf_q1",
                "Q": "x180_Q_wf_q1",
            },
            "operation": "control",
        },
        "-x90_pulse_q1": {
            "length": 20,
            "waveforms": {
                "I": "minus_x90_I_wf_q1",
                "Q": "minus_x90_Q_wf_q1",
            },
            "operation": "control",
        },
        "y90_pulse_q1": {
            "length": 20,
            "waveforms": {
                "I": "y90_I_wf_q1",
                "Q": "y90_Q_wf_q1",
            },
            "operation": "control",
        },
        "y180_pulse_q1": {
            "length": 20,
            "waveforms": {
                "I": "y180_I_wf_q1",
                "Q": "y180_Q_wf_q1",
            },
            "operation": "control",
        },
        "-y90_pulse_q1": {
            "length": 20,
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
            "length": 20,
            "waveforms": {
                "I": "x90_I_wf_q2",
                "Q": "x90_Q_wf_q2",
            },
            "operation": "control",
        },
        "x180_pulse_q2": {
            "length": 20,
            "waveforms": {
                "I": "x180_I_wf_q2",
                "Q": "x180_Q_wf_q2",
            },
            "operation": "control",
        },
        "-x90_pulse_q2": {
            "length": 20,
            "waveforms": {
                "I": "minus_x90_I_wf_q2",
                "Q": "minus_x90_Q_wf_q2",
            },
            "operation": "control",
        },
        "y90_pulse_q2": {
            "length": 20,
            "waveforms": {
                "I": "y90_I_wf_q2",
                "Q": "y90_Q_wf_q2",
            },
            "operation": "control",
        },
        "y180_pulse_q2": {
            "length": 20,
            "waveforms": {
                "I": "y180_I_wf_q2",
                "Q": "y180_Q_wf_q2",
            },
            "operation": "control",
        },
        "-y90_pulse_q2": {
            "length": 20,
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
            "length": 20,
            "waveforms": {
                "I": "x90_I_wf_q3",
                "Q": "x90_Q_wf_q3",
            },
            "operation": "control",
        },
        "x180_pulse_q3": {
            "length": 20,
            "waveforms": {
                "I": "x180_I_wf_q3",
                "Q": "x180_Q_wf_q3",
            },
            "operation": "control",
        },
        "-x90_pulse_q3": {
            "length": 20,
            "waveforms": {
                "I": "minus_x90_I_wf_q3",
                "Q": "minus_x90_Q_wf_q3",
            },
            "operation": "control",
        },
        "y90_pulse_q3": {
            "length": 20,
            "waveforms": {
                "I": "y90_I_wf_q3",
                "Q": "y90_Q_wf_q3",
            },
            "operation": "control",
        },
        "y180_pulse_q3": {
            "length": 20,
            "waveforms": {
                "I": "y180_I_wf_q3",
                "Q": "y180_Q_wf_q3",
            },
            "operation": "control",
        },
        "-y90_pulse_q3": {
            "length": 20,
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
            "length": 20,
            "waveforms": {
                "I": "x90_I_wf_q4",
                "Q": "x90_Q_wf_q4",
            },
            "operation": "control",
        },
        "x180_pulse_q4": {
            "length": 20,
            "waveforms": {
                "I": "x180_I_wf_q4",
                "Q": "x180_Q_wf_q4",
            },
            "operation": "control",
        },
        "-x90_pulse_q4": {
            "length": 20,
            "waveforms": {
                "I": "minus_x90_I_wf_q4",
                "Q": "minus_x90_Q_wf_q4",
            },
            "operation": "control",
        },
        "y90_pulse_q4": {
            "length": 20,
            "waveforms": {
                "I": "y90_I_wf_q4",
                "Q": "y90_Q_wf_q4",
            },
            "operation": "control",
        },
        "y180_pulse_q4": {
            "length": 20,
            "waveforms": {
                "I": "y180_I_wf_q4",
                "Q": "y180_Q_wf_q4",
            },
            "operation": "control",
        },
        "-y90_pulse_q4": {
            "length": 20,
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
            "length": 20,
            "waveforms": {
                "I": "x90_I_wf_q5",
                "Q": "x90_Q_wf_q5",
            },
            "operation": "control",
        },
        "x180_pulse_q5": {
            "length": 20,
            "waveforms": {
                "I": "x180_I_wf_q5",
                "Q": "x180_Q_wf_q5",
            },
            "operation": "control",
        },
        "-x90_pulse_q5": {
            "length": 20,
            "waveforms": {
                "I": "minus_x90_I_wf_q5",
                "Q": "minus_x90_Q_wf_q5",
            },
            "operation": "control",
        },
        "y90_pulse_q5": {
            "length": 20,
            "waveforms": {
                "I": "y90_I_wf_q5",
                "Q": "y90_Q_wf_q5",
            },
            "operation": "control",
        },
        "y180_pulse_q5": {
            "length": 20,
            "waveforms": {
                "I": "y180_I_wf_q5",
                "Q": "y180_Q_wf_q5",
            },
            "operation": "control",
        },
        "-y90_pulse_q5": {
            "length": 20,
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
        "q2_z_baked_pulse_0": {
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_0",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_1": {
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_1",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_2": {
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_2",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_3": {
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_3",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_4": {
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_4",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_5": {
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_5",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_6": {
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_6",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_7": {
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_7",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_8": {
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_8",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_9": {
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_9",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_10": {
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_10",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_11": {
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_11",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_12": {
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_12",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_13": {
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_13",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_14": {
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_14",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_15": {
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_15",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_16": {
            "length": 16,
            "waveforms": {
                "single": "q2_z_baked_wf_16",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_17": {
            "length": 20,
            "waveforms": {
                "single": "q2_z_baked_wf_17",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_18": {
            "length": 20,
            "waveforms": {
                "single": "q2_z_baked_wf_18",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_19": {
            "length": 20,
            "waveforms": {
                "single": "q2_z_baked_wf_19",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_20": {
            "length": 20,
            "waveforms": {
                "single": "q2_z_baked_wf_20",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_21": {
            "length": 24,
            "waveforms": {
                "single": "q2_z_baked_wf_21",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_22": {
            "length": 24,
            "waveforms": {
                "single": "q2_z_baked_wf_22",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_23": {
            "length": 24,
            "waveforms": {
                "single": "q2_z_baked_wf_23",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_24": {
            "length": 24,
            "waveforms": {
                "single": "q2_z_baked_wf_24",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_25": {
            "length": 28,
            "waveforms": {
                "single": "q2_z_baked_wf_25",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_26": {
            "length": 28,
            "waveforms": {
                "single": "q2_z_baked_wf_26",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_27": {
            "length": 28,
            "waveforms": {
                "single": "q2_z_baked_wf_27",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_28": {
            "length": 28,
            "waveforms": {
                "single": "q2_z_baked_wf_28",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_29": {
            "length": 32,
            "waveforms": {
                "single": "q2_z_baked_wf_29",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_30": {
            "length": 32,
            "waveforms": {
                "single": "q2_z_baked_wf_30",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_31": {
            "length": 32,
            "waveforms": {
                "single": "q2_z_baked_wf_31",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_32": {
            "length": 32,
            "waveforms": {
                "single": "q2_z_baked_wf_32",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_33": {
            "length": 36,
            "waveforms": {
                "single": "q2_z_baked_wf_33",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_34": {
            "length": 36,
            "waveforms": {
                "single": "q2_z_baked_wf_34",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_35": {
            "length": 36,
            "waveforms": {
                "single": "q2_z_baked_wf_35",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_36": {
            "length": 36,
            "waveforms": {
                "single": "q2_z_baked_wf_36",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_37": {
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_37",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_38": {
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_38",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_39": {
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_39",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_40": {
            "length": 40,
            "waveforms": {
                "single": "q2_z_baked_wf_40",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_41": {
            "length": 44,
            "waveforms": {
                "single": "q2_z_baked_wf_41",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_42": {
            "length": 44,
            "waveforms": {
                "single": "q2_z_baked_wf_42",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_43": {
            "length": 44,
            "waveforms": {
                "single": "q2_z_baked_wf_43",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_44": {
            "length": 44,
            "waveforms": {
                "single": "q2_z_baked_wf_44",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_45": {
            "length": 48,
            "waveforms": {
                "single": "q2_z_baked_wf_45",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_46": {
            "length": 48,
            "waveforms": {
                "single": "q2_z_baked_wf_46",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_47": {
            "length": 48,
            "waveforms": {
                "single": "q2_z_baked_wf_47",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_48": {
            "length": 48,
            "waveforms": {
                "single": "q2_z_baked_wf_48",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_49": {
            "length": 52,
            "waveforms": {
                "single": "q2_z_baked_wf_49",
            },
            "operation": "control",
        },
        "q2_z_baked_pulse_50": {
            "length": 52,
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
            "samples": [0.0, 0.0014694319341680283, 0.003302446110579668, 0.005465306961995178, 0.007867580142769207, 0.010360266914041962, 0.012746265974209976, 0.014803720077191503, 0.01631910724476066] + [0.017123493100572245] * 2 + [0.01631910724476066, 0.014803720077191503, 0.012746265974209976, 0.010360266914041962, 0.007867580142769207, 0.005465306961995178, 0.003302446110579668, 0.0014694319341680283, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q1": {
            "samples": [-0.0006316040056343379, -0.000810002220721428, -0.0009842440123493477, -0.0011286449159734998, -0.001214052138069595, -0.0012132381518087355, -0.0011073596801941049, -0.0008918175378462839, -0.0005796566432847614, -0.00020110429322099118, 0.00020110429322099118, 0.0005796566432847614, 0.0008918175378462839, 0.0011073596801941049, 0.0012132381518087355, 0.001214052138069595, 0.0011286449159734998, 0.0009842440123493477, 0.000810002220721428, 0.0006316040056343379],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q1": {
            "samples": [0.0, 0.0029388638683360566, 0.006604892221159336, 0.010930613923990355, 0.015735160285538414, 0.020720533828083924, 0.025492531948419953, 0.029607440154383005, 0.03263821448952132] + [0.03424698620114449] * 2 + [0.03263821448952132, 0.029607440154383005, 0.025492531948419953, 0.020720533828083924, 0.015735160285538414, 0.010930613923990355, 0.006604892221159336, 0.0029388638683360566, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q1": {
            "samples": [-0.0012632080112686757, -0.001620004441442856, -0.0019684880246986954, -0.0022572898319469996, -0.00242810427613919, -0.002426476303617471, -0.0022147193603882097, -0.0017836350756925679, -0.0011593132865695228, -0.00040220858644198236, 0.00040220858644198236, 0.0011593132865695228, 0.0017836350756925679, 0.0022147193603882097, 0.002426476303617471, 0.00242810427613919, 0.0022572898319469996, 0.0019684880246986954, 0.001620004441442856, 0.0012632080112686757],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q1": {
            "samples": [0.0, -0.0014694319341680283, -0.003302446110579668, -0.005465306961995178, -0.007867580142769207, -0.010360266914041962, -0.012746265974209976, -0.014803720077191503, -0.01631910724476066] + [-0.017123493100572245] * 2 + [-0.01631910724476066, -0.014803720077191503, -0.012746265974209976, -0.010360266914041962, -0.007867580142769207, -0.005465306961995178, -0.003302446110579668, -0.0014694319341680283, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q1": {
            "samples": [0.0006316040056343379, 0.000810002220721428, 0.0009842440123493477, 0.0011286449159734998, 0.001214052138069595, 0.0012132381518087355, 0.0011073596801941049, 0.0008918175378462839, 0.0005796566432847614, 0.00020110429322099118, -0.00020110429322099118, -0.0005796566432847614, -0.0008918175378462839, -0.0011073596801941049, -0.0012132381518087355, -0.001214052138069595, -0.0011286449159734998, -0.0009842440123493477, -0.000810002220721428, -0.0006316040056343379],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q1": {
            "samples": [0.0006316040056343379, 0.000810002220721428, 0.0009842440123493477, 0.0011286449159734998, 0.001214052138069595, 0.0012132381518087355, 0.0011073596801941049, 0.0008918175378462839, 0.0005796566432847614, 0.00020110429322099118, -0.00020110429322099118, -0.0005796566432847614, -0.0008918175378462839, -0.0011073596801941049, -0.0012132381518087355, -0.001214052138069595, -0.0011286449159734998, -0.0009842440123493477, -0.000810002220721428, -0.0006316040056343379],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q1": {
            "samples": [0.0, 0.0014694319341680283, 0.003302446110579668, 0.005465306961995178, 0.007867580142769207, 0.010360266914041962, 0.012746265974209976, 0.014803720077191503, 0.01631910724476066] + [0.017123493100572245] * 2 + [0.01631910724476066, 0.014803720077191503, 0.012746265974209976, 0.010360266914041962, 0.007867580142769207, 0.005465306961995178, 0.003302446110579668, 0.0014694319341680283, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q1": {
            "samples": [0.0012632080112686757, 0.001620004441442856, 0.0019684880246986954, 0.0022572898319469996, 0.00242810427613919, 0.002426476303617471, 0.0022147193603882097, 0.0017836350756925679, 0.0011593132865695228, 0.00040220858644198236, -0.00040220858644198236, -0.0011593132865695228, -0.0017836350756925679, -0.0022147193603882097, -0.002426476303617471, -0.00242810427613919, -0.0022572898319469996, -0.0019684880246986954, -0.001620004441442856, -0.0012632080112686757],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q1": {
            "samples": [0.0, 0.0029388638683360566, 0.006604892221159336, 0.010930613923990355, 0.015735160285538414, 0.020720533828083924, 0.025492531948419953, 0.029607440154383005, 0.03263821448952132] + [0.03424698620114449] * 2 + [0.03263821448952132, 0.029607440154383005, 0.025492531948419953, 0.020720533828083924, 0.015735160285538414, 0.010930613923990355, 0.006604892221159336, 0.0029388638683360566, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q1": {
            "samples": [-0.0006316040056343379, -0.000810002220721428, -0.0009842440123493477, -0.0011286449159734998, -0.001214052138069595, -0.0012132381518087355, -0.0011073596801941049, -0.0008918175378462839, -0.0005796566432847614, -0.00020110429322099118, 0.00020110429322099118, 0.0005796566432847614, 0.0008918175378462839, 0.0011073596801941049, 0.0012132381518087355, 0.001214052138069595, 0.0011286449159734998, 0.0009842440123493477, 0.000810002220721428, 0.0006316040056343379],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q1": {
            "samples": [0.0, -0.0014694319341680283, -0.003302446110579668, -0.005465306961995178, -0.007867580142769207, -0.010360266914041962, -0.012746265974209976, -0.014803720077191503, -0.01631910724476066] + [-0.017123493100572245] * 2 + [-0.01631910724476066, -0.014803720077191503, -0.012746265974209976, -0.010360266914041962, -0.007867580142769207, -0.005465306961995178, -0.003302446110579668, -0.0014694319341680283, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q1": {
            "sample": 0.03,
            "type": "constant",
        },
        "x90_I_wf_q2": {
            "samples": [0.0, 0.0036903687340989547, 0.008293847158990834, 0.013725710913054138, 0.019758840880460437, 0.026019037838692024, 0.03201129656568023, 0.03717843913073246, 0.04098422100685474] + [0.04300437610449062] * 2 + [0.04098422100685474, 0.03717843913073246, 0.03201129656568023, 0.026019037838692024, 0.019758840880460437, 0.013725710913054138, 0.008293847158990834, 0.0036903687340989547, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q2": {
            "samples": [0.0011588783203718474, 0.0014862065545394347, 0.001805908508642062, 0.0020708578679863986, 0.0022275645658657813, 0.0022260710493231762, 0.0020318033368740282, 0.0016363227609670977, 0.0010635643712987035, 0.00036898975223161474, -0.00036898975223161474, -0.0010635643712987035, -0.0016363227609670977, -0.0020318033368740282, -0.0022260710493231762, -0.0022275645658657813, -0.0020708578679863986, -0.001805908508642062, -0.0014862065545394347, -0.0011588783203718474],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q2": {
            "samples": [0.0, 0.007350189844000168, 0.016519040656404346, 0.02733780503357896, 0.039354124759090094, 0.05182269888250199, 0.06375761444548136, 0.07404912771710057, 0.08162918849419357] + [0.08565277652883854] * 2 + [0.08162918849419357, 0.07404912771710057, 0.06375761444548136, 0.05182269888250199, 0.039354124759090094, 0.02733780503357896, 0.016519040656404346, 0.007350189844000168, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q2": {
            "samples": [0.002308163837971841, 0.002960110793895892, 0.0035968683174569865, 0.00412457387496209, 0.00443669010567828, 0.004433715435417861, 0.004046788092936593, 0.003259100595567796, 0.0021183249164582092, 0.0007349251320966316, -0.0007349251320966316, -0.0021183249164582092, -0.003259100595567796, -0.004046788092936593, -0.004433715435417861, -0.00443669010567828, -0.00412457387496209, -0.0035968683174569865, -0.002960110793895892, -0.002308163837971841],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q2": {
            "samples": [0.0, -0.0036903687340989547, -0.008293847158990834, -0.013725710913054138, -0.019758840880460437, -0.026019037838692024, -0.03201129656568023, -0.03717843913073246, -0.04098422100685474] + [-0.04300437610449062] * 2 + [-0.04098422100685474, -0.03717843913073246, -0.03201129656568023, -0.026019037838692024, -0.019758840880460437, -0.013725710913054138, -0.008293847158990834, -0.0036903687340989547, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q2": {
            "samples": [-0.0011588783203718474, -0.0014862065545394347, -0.001805908508642062, -0.0020708578679863986, -0.0022275645658657813, -0.0022260710493231762, -0.0020318033368740282, -0.0016363227609670977, -0.0010635643712987035, -0.00036898975223161474, 0.00036898975223161474, 0.0010635643712987035, 0.0016363227609670977, 0.0020318033368740282, 0.0022260710493231762, 0.0022275645658657813, 0.0020708578679863986, 0.001805908508642062, 0.0014862065545394347, 0.0011588783203718474],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q2": {
            "samples": [-0.0011588783203718474, -0.0014862065545394347, -0.001805908508642062, -0.0020708578679863986, -0.0022275645658657813, -0.0022260710493231762, -0.0020318033368740282, -0.0016363227609670977, -0.0010635643712987035, -0.00036898975223161474, 0.00036898975223161474, 0.0010635643712987035, 0.0016363227609670977, 0.0020318033368740282, 0.0022260710493231762, 0.0022275645658657813, 0.0020708578679863986, 0.001805908508642062, 0.0014862065545394347, 0.0011588783203718474],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q2": {
            "samples": [0.0, 0.0036903687340989547, 0.008293847158990834, 0.013725710913054138, 0.019758840880460437, 0.026019037838692024, 0.03201129656568023, 0.03717843913073246, 0.04098422100685474] + [0.04300437610449062] * 2 + [0.04098422100685474, 0.03717843913073246, 0.03201129656568023, 0.026019037838692024, 0.019758840880460437, 0.013725710913054138, 0.008293847158990834, 0.0036903687340989547, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q2": {
            "samples": [-0.002308163837971841, -0.002960110793895892, -0.0035968683174569865, -0.00412457387496209, -0.00443669010567828, -0.004433715435417861, -0.004046788092936593, -0.003259100595567796, -0.0021183249164582092, -0.0007349251320966316, 0.0007349251320966316, 0.0021183249164582092, 0.003259100595567796, 0.004046788092936593, 0.004433715435417861, 0.00443669010567828, 0.00412457387496209, 0.0035968683174569865, 0.002960110793895892, 0.002308163837971841],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q2": {
            "samples": [0.0, 0.007350189844000168, 0.016519040656404346, 0.02733780503357896, 0.039354124759090094, 0.05182269888250199, 0.06375761444548136, 0.07404912771710057, 0.08162918849419357] + [0.08565277652883854] * 2 + [0.08162918849419357, 0.07404912771710057, 0.06375761444548136, 0.05182269888250199, 0.039354124759090094, 0.02733780503357896, 0.016519040656404346, 0.007350189844000168, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q2": {
            "samples": [0.0011588783203718474, 0.0014862065545394347, 0.001805908508642062, 0.0020708578679863986, 0.0022275645658657813, 0.0022260710493231762, 0.0020318033368740282, 0.0016363227609670977, 0.0010635643712987035, 0.00036898975223161474, -0.00036898975223161474, -0.0010635643712987035, -0.0016363227609670977, -0.0020318033368740282, -0.0022260710493231762, -0.0022275645658657813, -0.0020708578679863986, -0.001805908508642062, -0.0014862065545394347, -0.0011588783203718474],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q2": {
            "samples": [0.0, -0.0036903687340989547, -0.008293847158990834, -0.013725710913054138, -0.019758840880460437, -0.026019037838692024, -0.03201129656568023, -0.03717843913073246, -0.04098422100685474] + [-0.04300437610449062] * 2 + [-0.04098422100685474, -0.03717843913073246, -0.03201129656568023, -0.026019037838692024, -0.019758840880460437, -0.013725710913054138, -0.008293847158990834, -0.0036903687340989547, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q2": {
            "sample": 0.020999999999999998,
            "type": "constant",
        },
        "x90_I_wf_q3": {
            "samples": [0.0, 0.014896835639639595, 0.0334796024056238, 0.05540629520830214, 0.07976010697962901, 0.10503051540707237, 0.12921934308202135, 0.15007744130048106, 0.16544016279902943] + [0.17359488137172774] * 2 + [0.16544016279902943, 0.15007744130048106, 0.12921934308202135, 0.10503051540707237, 0.07976010697962901, 0.05540629520830214, 0.0334796024056238, 0.014896835639639595, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q3": {
            "samples": [-0.012994500842607316, -0.01666483183416049, -0.020249649358951873, -0.023220526122047704, -0.024977678086873876, -0.024960931288154662, -0.022782607724122637, -0.018348084628368743, -0.011925745676710533, -0.004137481530199539, 0.004137481530199539, 0.011925745676710533, 0.018348084628368743, 0.022782607724122637, 0.024960931288154662, 0.024977678086873876, 0.023220526122047704, 0.020249649358951873, 0.01666483183416049, 0.012994500842607316],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q3": {
            "samples": [0.0, 0.024123603756755284, 0.05421612226276259, 0.08972372009517765, 0.12916174031302743, 0.17008407673545983, 0.2092549253832216, 0.24303206495256024, 0.26791011389002795] + [0.2811156834723467] * 2 + [0.26791011389002795, 0.24303206495256024, 0.2092549253832216, 0.17008407673545983, 0.12916174031302743, 0.08972372009517765, 0.05421612226276259, 0.024123603756755284, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q3": {
            "samples": [-0.021043005167469608, -0.02698665740598686, -0.03279183104153566, -0.037602802685229614, -0.04044829543048595, -0.04042117603773241, -0.03689364738776317, -0.029712479480701878, -0.01931228686200115, -0.006700145413421634, 0.006700145413421634, 0.01931228686200115, 0.029712479480701878, 0.03689364738776317, 0.04042117603773241, 0.04044829543048595, 0.037602802685229614, 0.03279183104153566, 0.02698665740598686, 0.021043005167469608],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q3": {
            "samples": [0.0, -0.014896835639639595, -0.0334796024056238, -0.05540629520830214, -0.07976010697962901, -0.10503051540707237, -0.12921934308202135, -0.15007744130048106, -0.16544016279902943] + [-0.17359488137172774] * 2 + [-0.16544016279902943, -0.15007744130048106, -0.12921934308202135, -0.10503051540707237, -0.07976010697962901, -0.05540629520830214, -0.0334796024056238, -0.014896835639639595, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q3": {
            "samples": [0.012994500842607316, 0.01666483183416049, 0.020249649358951873, 0.023220526122047704, 0.024977678086873876, 0.024960931288154662, 0.022782607724122637, 0.018348084628368743, 0.011925745676710533, 0.004137481530199539, -0.004137481530199539, -0.011925745676710533, -0.018348084628368743, -0.022782607724122637, -0.024960931288154662, -0.024977678086873876, -0.023220526122047704, -0.020249649358951873, -0.01666483183416049, -0.012994500842607316],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q3": {
            "samples": [0.012994500842607316, 0.01666483183416049, 0.020249649358951873, 0.023220526122047704, 0.024977678086873876, 0.024960931288154662, 0.022782607724122637, 0.018348084628368743, 0.011925745676710533, 0.004137481530199539, -0.004137481530199539, -0.011925745676710533, -0.018348084628368743, -0.022782607724122637, -0.024960931288154662, -0.024977678086873876, -0.023220526122047704, -0.020249649358951873, -0.01666483183416049, -0.012994500842607316],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q3": {
            "samples": [0.0, 0.014896835639639595, 0.0334796024056238, 0.05540629520830214, 0.07976010697962901, 0.10503051540707237, 0.12921934308202135, 0.15007744130048106, 0.16544016279902943] + [0.17359488137172774] * 2 + [0.16544016279902943, 0.15007744130048106, 0.12921934308202135, 0.10503051540707237, 0.07976010697962901, 0.05540629520830214, 0.0334796024056238, 0.014896835639639595, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q3": {
            "samples": [0.021043005167469608, 0.02698665740598686, 0.03279183104153566, 0.037602802685229614, 0.04044829543048595, 0.04042117603773241, 0.03689364738776317, 0.029712479480701878, 0.01931228686200115, 0.006700145413421634, -0.006700145413421634, -0.01931228686200115, -0.029712479480701878, -0.03689364738776317, -0.04042117603773241, -0.04044829543048595, -0.037602802685229614, -0.03279183104153566, -0.02698665740598686, -0.021043005167469608],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q3": {
            "samples": [0.0, 0.024123603756755284, 0.05421612226276259, 0.08972372009517765, 0.12916174031302743, 0.17008407673545983, 0.2092549253832216, 0.24303206495256024, 0.26791011389002795] + [0.2811156834723467] * 2 + [0.26791011389002795, 0.24303206495256024, 0.2092549253832216, 0.17008407673545983, 0.12916174031302743, 0.08972372009517765, 0.05421612226276259, 0.024123603756755284, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q3": {
            "samples": [-0.012994500842607316, -0.01666483183416049, -0.020249649358951873, -0.023220526122047704, -0.024977678086873876, -0.024960931288154662, -0.022782607724122637, -0.018348084628368743, -0.011925745676710533, -0.004137481530199539, 0.004137481530199539, 0.011925745676710533, 0.018348084628368743, 0.022782607724122637, 0.024960931288154662, 0.024977678086873876, 0.023220526122047704, 0.020249649358951873, 0.01666483183416049, 0.012994500842607316],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q3": {
            "samples": [0.0, -0.014896835639639595, -0.0334796024056238, -0.05540629520830214, -0.07976010697962901, -0.10503051540707237, -0.12921934308202135, -0.15007744130048106, -0.16544016279902943] + [-0.17359488137172774] * 2 + [-0.16544016279902943, -0.15007744130048106, -0.12921934308202135, -0.10503051540707237, -0.07976010697962901, -0.05540629520830214, -0.0334796024056238, -0.014896835639639595, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q3": {
            "sample": 0.0135,
            "type": "constant",
        },
        "x90_I_wf_q4": {
            "samples": [0.0, 0.005984439312228475, 0.013449611289316836, 0.022258123752617397, 0.03204167188945293, 0.04219344031112026, 0.05191071012307255, 0.06028994085209555, 0.06646153841165316] + [0.06973749711772612] * 2 + [0.06646153841165316, 0.06028994085209555, 0.05191071012307255, 0.04219344031112026, 0.03204167188945293, 0.022258123752617397, 0.013449611289316836, 0.005984439312228475, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q4": {
            "samples": [-0.004261406401946045, -0.005465051865062377, -0.006640654109041241, -0.007614921101747756, -0.008191160137228851, -0.008185668205207873, -0.007471310486222691, -0.006017056464562899, -0.003910919672118597, -0.0013568424439139993, 0.0013568424439139993, 0.003910919672118597, 0.006017056464562899, 0.007471310486222691, 0.008185668205207873, 0.008191160137228851, 0.007614921101747756, 0.006640654109041241, 0.005465051865062377, 0.004261406401946045],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q4": {
            "samples": [0.0, 0.010950884409728578, 0.024611351356530586, 0.04072998783600022, 0.05863283540011151, 0.07720948673532474, 0.0949910520477832, 0.11032414882904325, 0.12161751283057597] + [0.12761216717487578] * 2 + [0.12161751283057597, 0.11032414882904325, 0.0949910520477832, 0.07720948673532474, 0.05863283540011151, 0.04072998783600022, 0.024611351356530586, 0.010950884409728578, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q4": {
            "samples": [-0.007797918317131542, -0.010000460886148399, -0.012151687361003586, -0.013934491841874829, -0.014988947696583318, -0.014978898047884407, -0.01367169976252139, -0.011010570312843833, -0.007156565056577729, -0.0024828766723649525, 0.0024828766723649525, 0.007156565056577729, 0.011010570312843833, 0.01367169976252139, 0.014978898047884407, 0.014988947696583318, 0.013934491841874829, 0.012151687361003586, 0.010000460886148399, 0.007797918317131542],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q4": {
            "samples": [0.0, -0.005984439312228475, -0.013449611289316836, -0.022258123752617397, -0.03204167188945293, -0.04219344031112026, -0.05191071012307255, -0.06028994085209555, -0.06646153841165316] + [-0.06973749711772612] * 2 + [-0.06646153841165316, -0.06028994085209555, -0.05191071012307255, -0.04219344031112026, -0.03204167188945293, -0.022258123752617397, -0.013449611289316836, -0.005984439312228475, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q4": {
            "samples": [0.004261406401946045, 0.005465051865062377, 0.006640654109041241, 0.007614921101747756, 0.008191160137228851, 0.008185668205207873, 0.007471310486222691, 0.006017056464562899, 0.003910919672118597, 0.0013568424439139993, -0.0013568424439139993, -0.003910919672118597, -0.006017056464562899, -0.007471310486222691, -0.008185668205207873, -0.008191160137228851, -0.007614921101747756, -0.006640654109041241, -0.005465051865062377, -0.004261406401946045],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q4": {
            "samples": [0.004261406401946045, 0.005465051865062377, 0.006640654109041241, 0.007614921101747756, 0.008191160137228851, 0.008185668205207873, 0.007471310486222691, 0.006017056464562899, 0.003910919672118597, 0.0013568424439139993, -0.0013568424439139993, -0.003910919672118597, -0.006017056464562899, -0.007471310486222691, -0.008185668205207873, -0.008191160137228851, -0.007614921101747756, -0.006640654109041241, -0.005465051865062377, -0.004261406401946045],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q4": {
            "samples": [0.0, 0.005984439312228475, 0.013449611289316836, 0.022258123752617397, 0.03204167188945293, 0.04219344031112026, 0.05191071012307255, 0.06028994085209555, 0.06646153841165316] + [0.06973749711772612] * 2 + [0.06646153841165316, 0.06028994085209555, 0.05191071012307255, 0.04219344031112026, 0.03204167188945293, 0.022258123752617397, 0.013449611289316836, 0.005984439312228475, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q4": {
            "samples": [0.007797918317131542, 0.010000460886148399, 0.012151687361003586, 0.013934491841874829, 0.014988947696583318, 0.014978898047884407, 0.01367169976252139, 0.011010570312843833, 0.007156565056577729, 0.0024828766723649525, -0.0024828766723649525, -0.007156565056577729, -0.011010570312843833, -0.01367169976252139, -0.014978898047884407, -0.014988947696583318, -0.013934491841874829, -0.012151687361003586, -0.010000460886148399, -0.007797918317131542],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q4": {
            "samples": [0.0, 0.010950884409728578, 0.024611351356530586, 0.04072998783600022, 0.05863283540011151, 0.07720948673532474, 0.0949910520477832, 0.11032414882904325, 0.12161751283057597] + [0.12761216717487578] * 2 + [0.12161751283057597, 0.11032414882904325, 0.0949910520477832, 0.07720948673532474, 0.05863283540011151, 0.04072998783600022, 0.024611351356530586, 0.010950884409728578, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q4": {
            "samples": [-0.004261406401946045, -0.005465051865062377, -0.006640654109041241, -0.007614921101747756, -0.008191160137228851, -0.008185668205207873, -0.007471310486222691, -0.006017056464562899, -0.003910919672118597, -0.0013568424439139993, 0.0013568424439139993, 0.003910919672118597, 0.006017056464562899, 0.007471310486222691, 0.008185668205207873, 0.008191160137228851, 0.007614921101747756, 0.006640654109041241, 0.005465051865062377, 0.004261406401946045],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q4": {
            "samples": [0.0, -0.005984439312228475, -0.013449611289316836, -0.022258123752617397, -0.03204167188945293, -0.04219344031112026, -0.05191071012307255, -0.06028994085209555, -0.06646153841165316] + [-0.06973749711772612] * 2 + [-0.06646153841165316, -0.06028994085209555, -0.05191071012307255, -0.04219344031112026, -0.03204167188945293, -0.022258123752617397, -0.013449611289316836, -0.005984439312228475, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q4": {
            "sample": 0.03,
            "type": "constant",
        },
        "x90_I_wf_q5": {
            "samples": [0.0, 0.017817904994677156, 0.04004450269529871, 0.06627072540839607, 0.09539999251563863, 0.12562558857032988, 0.15455752041617832, 0.17950561150186015, 0.19788075631398627] + [0.20763450565388186] * 2 + [0.19788075631398627, 0.17950561150186015, 0.15455752041617832, 0.12562558857032988, 0.09539999251563863, 0.06627072540839607, 0.04004450269529871, 0.017817904994677156, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q5": {
            "samples": [0.0] * 20,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q5": {
            "samples": [0.0, 0.03563580998935431, 0.08008900539059742, 0.13254145081679214, 0.19079998503127726, 0.25125117714065975, 0.30911504083235664, 0.3590112230037203, 0.39576151262797254] + [0.4152690113077637] * 2 + [0.39576151262797254, 0.3590112230037203, 0.30911504083235664, 0.25125117714065975, 0.19079998503127726, 0.13254145081679214, 0.08008900539059742, 0.03563580998935431, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q5": {
            "samples": [0.0] * 20,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q5": {
            "samples": [0.0, -0.017817904994677156, -0.04004450269529871, -0.06627072540839607, -0.09539999251563863, -0.12562558857032988, -0.15455752041617832, -0.17950561150186015, -0.19788075631398627] + [-0.20763450565388186] * 2 + [-0.19788075631398627, -0.17950561150186015, -0.15455752041617832, -0.12562558857032988, -0.09539999251563863, -0.06627072540839607, -0.04004450269529871, -0.017817904994677156, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q5": {
            "samples": [0.0] * 20,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q5": {
            "samples": [-0.0] * 20,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q5": {
            "samples": [0.0, 0.017817904994677156, 0.04004450269529871, 0.06627072540839607, 0.09539999251563863, 0.12562558857032988, 0.15455752041617832, 0.17950561150186015, 0.19788075631398627] + [0.20763450565388186] * 2 + [0.19788075631398627, 0.17950561150186015, 0.15455752041617832, 0.12562558857032988, 0.09539999251563863, 0.06627072540839607, 0.04004450269529871, 0.017817904994677156, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q5": {
            "samples": [-0.0] * 20,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q5": {
            "samples": [0.0, 0.03563580998935431, 0.08008900539059742, 0.13254145081679214, 0.19079998503127726, 0.25125117714065975, 0.30911504083235664, 0.3590112230037203, 0.39576151262797254] + [0.4152690113077637] * 2 + [0.39576151262797254, 0.3590112230037203, 0.30911504083235664, 0.25125117714065975, 0.19079998503127726, 0.13254145081679214, 0.08008900539059742, 0.03563580998935431, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q5": {
            "samples": [-0.0] * 20,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q5": {
            "samples": [0.0, -0.017817904994677156, -0.04004450269529871, -0.06627072540839607, -0.09539999251563863, -0.12562558857032988, -0.15455752041617832, -0.17950561150186015, -0.19788075631398627] + [-0.20763450565388186] * 2 + [-0.19788075631398627, -0.17950561150186015, -0.15455752041617832, -0.12562558857032988, -0.09539999251563863, -0.06627072540839607, -0.04004450269529871, -0.017817904994677156, 0.0],
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
        "q2_z_baked_wf_0": {
            "samples": [0.0] * 16,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_1": {
            "samples": [0.5] + [0.0] * 15,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_2": {
            "samples": [0.5] * 2 + [0.0] * 14,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_3": {
            "samples": [0.5] * 3 + [0.0] * 13,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_4": {
            "samples": [0.5] * 4 + [0.0] * 12,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_5": {
            "samples": [0.5] * 5 + [0.0] * 11,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_6": {
            "samples": [0.5] * 6 + [0.0] * 10,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_7": {
            "samples": [0.5] * 7 + [0.0] * 9,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_8": {
            "samples": [0.5] * 8 + [0.0] * 8,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_9": {
            "samples": [0.5] * 9 + [0.0] * 7,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_10": {
            "samples": [0.5] * 10 + [0.0] * 6,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_11": {
            "samples": [0.5] * 11 + [0.0] * 5,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_12": {
            "samples": [0.5] * 12 + [0.0] * 4,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_13": {
            "samples": [0.5] * 13 + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_14": {
            "samples": [0.5] * 14 + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_15": {
            "samples": [0.5] * 15 + [0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_16": {
            "samples": [0.5] * 16,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_17": {
            "samples": [0.5] * 17 + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_18": {
            "samples": [0.5] * 18 + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_19": {
            "samples": [0.5] * 19 + [0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_20": {
            "samples": [0.5] * 20,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_21": {
            "samples": [0.5] * 21 + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_22": {
            "samples": [0.5] * 22 + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_23": {
            "samples": [0.5] * 23 + [0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_24": {
            "samples": [0.5] * 24,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_25": {
            "samples": [0.5] * 25 + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_26": {
            "samples": [0.5] * 26 + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_27": {
            "samples": [0.5] * 27 + [0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_28": {
            "samples": [0.5] * 28,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_29": {
            "samples": [0.5] * 29 + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_30": {
            "samples": [0.5] * 30 + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_31": {
            "samples": [0.5] * 31 + [0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_32": {
            "samples": [0.5] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_33": {
            "samples": [0.5] * 33 + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_34": {
            "samples": [0.5] * 34 + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_35": {
            "samples": [0.5] * 35 + [0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_36": {
            "samples": [0.5] * 36,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_37": {
            "samples": [0.5] * 37 + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_38": {
            "samples": [0.5] * 38 + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_39": {
            "samples": [0.5] * 39 + [0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_40": {
            "samples": [0.5] * 40,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_41": {
            "samples": [0.5] * 41 + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_42": {
            "samples": [0.5] * 42 + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_43": {
            "samples": [0.5] * 43 + [0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_44": {
            "samples": [0.5] * 44,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_45": {
            "samples": [0.5] * 45 + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_46": {
            "samples": [0.5] * 46 + [0.0] * 2,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_47": {
            "samples": [0.5] * 47 + [0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_48": {
            "samples": [0.5] * 48,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_49": {
            "samples": [0.5] * 49 + [0.0] * 3,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "q2_z_baked_wf_50": {
            "samples": [0.5] * 50 + [0.0] * 2,
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
            "cosine": [(0.0, 400), (0.8746197071393959, 1700)],
            "sine": [(0.0, 400), (0.484809620246337, 1700)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(0.0, 400), (-0.484809620246337, 1700)],
            "sine": [(0.0, 400), (0.8746197071393959, 1700)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(0.0, 400), (0.484809620246337, 1700)],
            "sine": [(0.0, 400), (-0.8746197071393959, 1700)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(0.0, 400), (-0.22835087011065508, 1700)],
            "sine": [(0.0, 400), (0.9735789028731604, 1700)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(0.0, 400), (-0.9735789028731604, 1700)],
            "sine": [(0.0, 400), (-0.22835087011065508, 1700)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(0.0, 400), (0.9735789028731604, 1700)],
            "sine": [(0.0, 400), (0.22835087011065508, 1700)],
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
        "octave_octave1_2": [
            {'intermediate_frequency': 99000000.0, 'lo_frequency': 3955000000.0, 'correction': [1.013119876384735, 0.09918718785047531, 0.09893324971199036, 1.0157203152775764]},
            {'intermediate_frequency': 19700000.0, 'lo_frequency': 4055000000.0, 'correction': [1.0119290761649609, 0.10491481050848961, 0.10407295450568199, 1.0201146677136421]},
            {'intermediate_frequency': 116555000.0, 'lo_frequency': 4055000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
            {'intermediate_frequency': 180000000.0, 'lo_frequency': 3700000000.0, 'correction': [1.0489636659622192, 0.1246739886701107, 0.1308462880551815, 0.9994818046689034]},
            {'intermediate_frequency': 180000000.0, 'lo_frequency': 3600000000.0, 'correction': [1.04962208122015, 0.1469372734427452, 0.15197580307722092, 1.0148234367370605]},
            {'intermediate_frequency': 106900000.0, 'lo_frequency': 3300000000.0, 'correction': [1.0321827754378319, 0.14756997302174568, 0.14784042909741402, 1.0302945226430893]},
            {'intermediate_frequency': 75347000.0, 'lo_frequency': 3600000000.0, 'correction': [0.9735809303820133, 0.10057862102985382, 0.09262080490589142, 1.057229284197092]},
            {'intermediate_frequency': 75347000.0, 'lo_frequency': 3300000000.0, 'correction': [0.8311591409146786, 0.06552650406956673, 0.042722437530756, 1.2748090960085392]},
            {'intermediate_frequency': 75347000.0, 'lo_frequency': 3400000000.0, 'correction': [0.8424716293811798, 0.12053202837705612, 0.07945621013641357, 1.2779971845448017]},
            {'intermediate_frequency': 75347000.0, 'lo_frequency': 3500000000.0, 'correction': [0.9035251215100288, 0.11854912713170052, 0.09229253605008125, 1.1605717912316322]},
            {'intermediate_frequency': 75347000.0, 'lo_frequency': 3450000000.0, 'correction': [1.0572927705943584, 0.16472642496228218, 0.17032818868756294, 1.0225204639136791]},
            {'intermediate_frequency': 75347000.0, 'lo_frequency': 3490000000.0, 'correction': [1.0568718202412128, 0.16134490072727203, 0.1671576388180256, 1.020120169967413]},
            {'intermediate_frequency': 75347000.0, 'lo_frequency': 3470000000.0, 'correction': [1.0582309402525425, 0.16638235747814178, 0.17209291458129883, 1.0231156758964062]},
            {'intermediate_frequency': 75347000.0, 'lo_frequency': 3480000000.0, 'correction': [1.0578176230192184, 0.1646474227309227, 0.17041274160146713, 1.0220300629734993]},
            {'intermediate_frequency': 0.0, 'lo_frequency': 3400000000.0, 'correction': [1.0217774510383606, -0.06147767975926399, -0.0634308010339737, 0.990315493196249]},
            {'intermediate_frequency': 0.0, 'lo_frequency': 3500000000.0, 'correction': [0.9954007379710674, -0.01472121849656105, -0.014576379209756851, 1.0052916146814823]},
            {'intermediate_frequency': 0.0, 'lo_frequency': 3300000000.0, 'correction': [1.0264127254486084, -0.1157689206302166, -0.11727301776409149, 1.0132483467459679]},
            {'intermediate_frequency': 304480000.0, 'lo_frequency': 3600000000.0, 'correction': [1.057143833488226, 0.14593342691659927, 0.15306488424539566, 1.0078903697431087]},
            {'intermediate_frequency': 75347000.0, 'lo_frequency': 3250000000.0, 'correction': [0.8448452353477478, 0.06274132430553436, 0.04271237924695015, 1.2410151027143002]},
            {'intermediate_frequency': 219319700.0, 'lo_frequency': 3400000000.0, 'correction': [0.8503554277122021, 0.14416301622986794, 0.0959322489798069, 1.2778789550065994]},
            {'intermediate_frequency': 212940000.0, 'lo_frequency': 3400000000.0, 'correction': [0.8512887433171272, 0.1404735930263996, 0.09394824504852295, 1.2728666476905346]},
            {'intermediate_frequency': 111450000.0, 'lo_frequency': 3300000000.0, 'correction': [0.8267116844654083, 0.07013754174113274, 0.04501013085246086, 1.2882327288389206]},
            {'intermediate_frequency': 311450000.0, 'lo_frequency': 3500000000.0, 'correction': [0.903420016169548, 0.13715070486068726, 0.10555890202522278, 1.173796709626913]},
            {'intermediate_frequency': 323810000.0, 'lo_frequency': 3500000000.0, 'correction': [0.9072245135903358, 0.14272667840123177, 0.11047400906682014, 1.1720869168639183]},
            {'intermediate_frequency': 123450000.0, 'lo_frequency': 3300000000.0, 'correction': [0.8232660032808781, 0.0764295905828476, 0.048388704657554626, 1.3003423810005188]},
            {'intermediate_frequency': 44900000.0, 'lo_frequency': 3600000000.0, 'correction': [0.972774438560009, 0.09726535901427269, 0.0895751379430294, 1.0562892481684685]},
            {'intermediate_frequency': 44900000.0, 'lo_frequency': 3300000000.0, 'correction': [0.8353546001017094, 0.058258358389139175, 0.03857475146651268, 1.2616125121712685]},
            {'intermediate_frequency': 45153000.0, 'lo_frequency': 3600000000.0, 'correction': [0.9726689234375954, 0.09730951488018036, 0.08959399908781052, 1.0564316809177399]},
            {'intermediate_frequency': 0.0, 'lo_frequency': 3450000000.0, 'correction': [1.0103772543370724, 0.06671024858951569, 0.06720269098877907, 1.002973522990942]},
            {'intermediate_frequency': 0.0, 'lo_frequency': 3550000000.0, 'correction': [1.0063092857599258, 0.06578866764903069, 0.06577260792255402, 1.0065549947321415]},
            {'intermediate_frequency': 45153000.0, 'lo_frequency': 3300000000.0, 'correction': [0.835892666131258, 0.0580032654106617, 0.03847326338291168, 1.2602129317820072]},
            {'intermediate_frequency': 94914000.0, 'lo_frequency': 3350000000.0, 'correction': [0.8321215026080608, 0.10824720561504364, 0.06955806910991669, 1.2949587032198906]},
            {'intermediate_frequency': 180380000.0, 'lo_frequency': 3400000000.0, 'correction': [0.8546344377100468, 0.14139743894338608, 0.09542854875326157, 1.2663204222917557]},
            {'intermediate_frequency': 263340000.0, 'lo_frequency': 2830000000.0, 'correction': [0.9499963894486427, -0.12157641351222992, -0.10519857704639435, 1.0978965424001217]},
            {'intermediate_frequency': 263340000.0, 'lo_frequency': 2850000000.0, 'correction': [0.9729656428098679, -0.14889118820428848, -0.1328480914235115, 1.0904636196792126]},
            {'intermediate_frequency': 0.0, 'lo_frequency': 2900000000.0, 'correction': [1.0533747859299183, -0.21467778086662292, -0.2113431952893734, 1.0699949972331524]},
            {'intermediate_frequency': 271700000.0, 'lo_frequency': 3160000000.0, 'correction': [0.7852009236812592, 0.1171339750289917, 0.06303155422210693, 1.4591692462563515]},
            {'intermediate_frequency': 100000000.0, 'lo_frequency': 3600000000.0, 'correction': [0.9744591005146503, 0.10126551985740662, 0.0933896005153656, 1.056639138609171]},
            {'intermediate_frequency': 71300000.0, 'lo_frequency': 3600000000.0, 'correction': [0.9739216528832912, 0.1005404032766819, 0.09265321865677834, 1.0568275637924671]},
            {'intermediate_frequency': 71271000.0, 'lo_frequency': 3600000000.0, 'correction': [0.9718846864998341, 0.09998255223035812, 0.09177558869123459, 1.0587947480380535]},
            {'intermediate_frequency': 171355000.0, 'lo_frequency': 3700000000.0, 'correction': [1.0683668591082096, 0.09722131118178368, 0.1073865257203579, 0.967235192656517]},
            {'intermediate_frequency': 41355000.0, 'lo_frequency': 3570000000.0, 'correction': [0.94725676253438, 0.10438976809382439, 0.0906716100871563, 1.090571939945221]},
            {'intermediate_frequency': 71355000.0, 'lo_frequency': 3600000000.0, 'correction': [0.973212119191885, 0.10062005370855331, 0.0925857201218605, 1.0576647818088531]},
            {'intermediate_frequency': 221355000.0, 'lo_frequency': 3750000000.0, 'correction': [1.1707491278648376, 0.0713556632399559, 0.09405063837766647, 0.8882404454052448]},
            {'intermediate_frequency': 271355000.0, 'lo_frequency': 3800000000.0, 'correction': [1.1806640625, 0.0, 0.0, 0.8681640625]},
            {'intermediate_frequency': 321355000.0, 'lo_frequency': 3850000000.0, 'correction': [1.2244436033070087, -0.0264892578125, -0.0382080078125, 0.8488954044878483]},
            {'intermediate_frequency': 317056000.0, 'lo_frequency': 3850000000.0, 'correction': [1.2244436033070087, -0.0264892578125, -0.0382080078125, 0.8488954044878483]},
            {'intermediate_frequency': 317506000.0, 'lo_frequency': 3850000000.0, 'correction': [1.2244436033070087, -0.0264892578125, -0.0382080078125, 0.8488954044878483]},
            {'intermediate_frequency': 317621000.0, 'lo_frequency': 3850000000.0, 'correction': [1.2244436033070087, -0.0264892578125, -0.0382080078125, 0.8488954044878483]},
            {'intermediate_frequency': 316997000.0, 'lo_frequency': 3850000000.0, 'correction': [1.2244436033070087, -0.0264892578125, -0.0382080078125, 0.8488954044878483]},
        ],
        "octave_octave1_3": [{'intermediate_frequency': 317033000.0, 'lo_frequency': 3850000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]}],
        "octave_octave1_4": [
            {'intermediate_frequency': 183200000.0, 'lo_frequency': 4215000000.0, 'correction': [1.0195316150784492, 0.1470695324242115, 0.14397891238331795, 1.0414166562259197]},
            {'intermediate_frequency': 124240000.0, 'lo_frequency': 4215000000.0, 'correction': [1.0156753063201904, 0.13932431116700172, 0.1361636109650135, 1.0392516888678074]},
            {'intermediate_frequency': 89090000.0, 'lo_frequency': 4215000000.0, 'correction': [1.0156761929392815, 0.13591918721795082, 0.13315223529934883, 1.0367823131382465]},
            {'intermediate_frequency': 98700000.0, 'lo_frequency': 4300000000.0, 'correction': [1.0164888240396976, 0.15053614974021912, 0.14615928754210472, 1.0469284355640411]},
            {'intermediate_frequency': 199070000.0, 'lo_frequency': 4400000000.0, 'correction': [1.0523961372673512, 0.22627202793955803, 0.22010232135653496, 1.0818959400057793]},
            {'intermediate_frequency': 100000000.0, 'lo_frequency': 3950000000.0, 'correction': [1.0145268887281418, 0.10615788772702217, 0.10575692728161812, 1.0183733068406582]},
            {'intermediate_frequency': 92000000.0, 'lo_frequency': 4750000000.0, 'correction': [1.2626258842647076, -0.06113452836871147, -0.0917474739253521, 0.8413314782083035]},
            {'intermediate_frequency': 104553000.0, 'lo_frequency': 3950000000.0, 'correction': [1.0146872736513615, 0.1068982370197773, 0.10648148134350777, 1.0186586380004883]},
            {'intermediate_frequency': 104644000.0, 'lo_frequency': 3950000000.0, 'correction': [1.0146501511335373, 0.1067759282886982, 0.10635964944958687, 1.0186213664710522]},
            {'intermediate_frequency': 145356000.0, 'lo_frequency': 3700000000.0, 'correction': [1.0465690642595291, 0.12968942895531654, 0.13506833091378212, 1.0048909559845924]},
            {'intermediate_frequency': 104255000.0, 'lo_frequency': 3950000000.0, 'correction': [1.0146176889538765, 0.10666890814900398, 0.10625304654240608, 1.0185887776315212]},
            {'intermediate_frequency': 108804000.0, 'lo_frequency': 3950000000.0, 'correction': [1.291191428899765, -0.02564239501953125, -0.04029083251953125, 0.8217561803758144]},
            {'intermediate_frequency': 89224000.0, 'lo_frequency': 3950000000.0, 'correction': [1.3129526637494564, -0.025405913591384888, -0.04096987843513489, 0.8141777105629444]},
            {'intermediate_frequency': 89843100.0, 'lo_frequency': 3700000000.0, 'correction': [1.053178545087576, 0.11116083711385727, 0.11857058852910995, 0.9873629733920097]},
            {'intermediate_frequency': 89843100.0, 'lo_frequency': 3800000000.0, 'correction': [1.2052510380744934, 0.08051718771457672, 0.11098207533359528, 0.8744062930345535]},
            {'intermediate_frequency': 83683100.0, 'lo_frequency': 3950000000.0, 'correction': [1.3144186958670616, -0.025390625, -0.041015625, 0.813687764108181]},
            {'intermediate_frequency': 89591100.0, 'lo_frequency': 3950000000.0, 'correction': [1.3041965961456299, -0.025498896837234497, -0.0406966507434845, 0.8171575255692005]},
            {'intermediate_frequency': 60408900.0, 'lo_frequency': 3800000000.0, 'correction': [1.1611689329147339, 0.03826643526554108, 0.050318971276283264, 0.8830426223576069]},
            {'intermediate_frequency': 100000000.0, 'lo_frequency': 3700000000.0, 'correction': [1.0544711574912071, 0.11347914859652519, 0.12114669010043144, 0.987732220441103]},
            {'intermediate_frequency': 0.0, 'lo_frequency': 3650000000.0, 'correction': [1.0184053964912891, 0.09133800119161606, 0.09241463989019394, 1.006540883332491]},
            {'intermediate_frequency': 204624000.0, 'lo_frequency': 4400000000.0, 'correction': [1.3294866308569908, -0.076171875, -0.123046875, 0.823015533387661]},
            {'intermediate_frequency': 100000000.0, 'lo_frequency': 4300000000.0, 'correction': [1.3338770642876625, -0.07925070822238922, -0.12846030294895172, 0.8229055926203728]},
            {'intermediate_frequency': 99092000.0, 'lo_frequency': 4100000000.0, 'correction': [1.368718508630991, -0.07504212856292725, -0.12667787075042725, 0.8108089417219162]},
            {'intermediate_frequency': 99092000.0, 'lo_frequency': 3900000000.0, 'correction': [1.2864418029785156, 0.0, 0.0, 0.8215980529785156]},
            {'intermediate_frequency': 99092000.0, 'lo_frequency': 3750000000.0, 'correction': [1.1356204822659492, 0.11233504116535187, 0.13724716007709503, 0.9294908083975315]},
            {'intermediate_frequency': 99092000.0, 'lo_frequency': 4300000000.0, 'correction': [1.3338770642876625, -0.07925070822238922, -0.12846030294895172, 0.8229055926203728]},
            {'intermediate_frequency': 100867000.0, 'lo_frequency': 4300000000.0, 'correction': [1.3372232988476753, -0.07994802296161652, -0.13003499805927277, 0.8221506550908089]},
            {'intermediate_frequency': 79153000.0, 'lo_frequency': 4280000000.0, 'correction': [1.34736917167902, -0.0852380208671093, -0.13982633873820305, 0.8213551342487335]},
            {'intermediate_frequency': 99153000.0, 'lo_frequency': 4300000000.0, 'correction': [1.3353672809898853, -0.07920349016785622, -0.12860381975769997, 0.8224152997136116]},
            {'intermediate_frequency': 99071000.0, 'lo_frequency': 4300000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
            {'intermediate_frequency': 89863100.0, 'lo_frequency': 3950000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
            {'intermediate_frequency': 100471000.0, 'lo_frequency': 4300000000.0, 'correction': [1.3294866308569908, -0.076171875, -0.123046875, 0.823015533387661]},
            {'intermediate_frequency': 101613000.0, 'lo_frequency': 4300000000.0, 'correction': [1.3294866308569908, -0.076171875, -0.123046875, 0.823015533387661]},
            {'intermediate_frequency': 101584000.0, 'lo_frequency': 4300000000.0, 'correction': [1.3338770642876625, -0.07925070822238922, -0.12846030294895172, 0.8229055926203728]},
            {'intermediate_frequency': 101721000.0, 'lo_frequency': 4300000000.0, 'correction': [1.3338770642876625, -0.07925070822238922, -0.12846030294895172, 0.8229055926203728]},
            {'intermediate_frequency': 101616000.0, 'lo_frequency': 4300000000.0, 'correction': [1.3289823047816753, -0.077796820551157, -0.1254965104162693, 0.8238523602485657]},
            {'intermediate_frequency': 101596000.0, 'lo_frequency': 4300000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
        ],
        "octave_octave1_5": [{'intermediate_frequency': 89863100.0, 'lo_frequency': 3950000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]}],
        "octave_octave2_1": [{'intermediate_frequency': 92000000.0, 'lo_frequency': 4750000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]}],
        "octave_octave1_1": [
            {'intermediate_frequency': 214510000.0, 'lo_frequency': 5950000000.0, 'correction': [1.004735816270113, 0.06405084580183029, 0.06387906521558762, 1.0074377059936523]},
            {'intermediate_frequency': 214210000.0, 'lo_frequency': 5950000000.0, 'correction': [1.1034728735685349, -0.1470947265625, -0.1666259765625, 0.9741280674934387]},
            {'intermediate_frequency': 75133000.0, 'lo_frequency': 5950000000.0, 'correction': [1.0926973298192024, -0.16419601440429688, -0.18030929565429688, 0.9950487911701202]},
            {'intermediate_frequency': 75159000.0, 'lo_frequency': 5950000000.0, 'correction': [1.0926973298192024, -0.16419601440429688, -0.18030929565429688, 0.9950487911701202]},
            {'intermediate_frequency': 103150000.0, 'lo_frequency': 5950000000.0, 'correction': [1.0855363868176937, -0.14926910400390625, -0.16391754150390625, 0.9885277822613716]},
            {'intermediate_frequency': 163060000.0, 'lo_frequency': 5950000000.0, 'correction': [1.1003425158560276, -0.1791229248046875, -0.1967010498046875, 1.002010766416788]},
            {'intermediate_frequency': 25800000.0, 'lo_frequency': 5950000000.0, 'correction': [1.0935042686760426, -0.15615427494049072, -0.17281687259674072, 0.9880711510777473]},
            {'intermediate_frequency': 75079000.0, 'lo_frequency': 5950000000.0, 'correction': [1.0926973298192024, -0.16419601440429688, -0.18030929565429688, 0.9950487911701202]},
            {'intermediate_frequency': 103170000.0, 'lo_frequency': 5950000000.0, 'correction': [1.0855363868176937, -0.14926910400390625, -0.16391754150390625, 0.9885277822613716]},
            {'intermediate_frequency': 103970000.0, 'lo_frequency': 5950000000.0, 'correction': [1.0855363868176937, -0.14926910400390625, -0.16391754150390625, 0.9885277822613716]},
        ],
    },
}


