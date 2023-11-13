from pathlib import Path
import numpy as np
from set_octave import OctaveUnit, octave_declaration
from qualang_tools.config.waveform_tools import drag_gaussian_pulse_waveforms
from qualang_tools.units import unit
import matplotlib
matplotlib.use('TkAgg')

#######################
# AUXILIARY FUNCTIONS #
#######################
u = unit(coerce_to_integer=True)

######################
# Network parameters #
######################
qop_ip = "192.168.50.126"  # Write the QM router IP address
cluster_name = "QPX_4"  # Write your cluster_name if version >= QOP220
qop_port = None  # Write the QOP port if version < QOP220

# Path to save data
# save_dir = Path().absolute() / "QM" / "INSTALLATION" / "data"
save_dir = r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20231011_DR4_5QX\01 Saved Data\test"

############################
# Set octave configuration #
############################
# Custom port mapping example
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

# The Octave port is 11xxx, where xxx are the last three digits of the Octave internal IP that can be accessed from
# the OPX admin panel if you QOP version is >= QOP220. Otherwise, it is 50 for Octave1, then 51, 52 and so on.
octave_1 = OctaveUnit("octave1", qop_ip, port=11250, con="con1", clock="Internal", port_mapping="default")
# octave_2 = OctaveUnit("octave2", qop_ip, port=11051, con="con1", clock="Internal", port_mapping=port_mapping)

# Add the octaves
octaves = [octave_1]
# Configure the Octaves
octave_config = octave_declaration(octaves)



#####################
# OPX configuration #
#####################

#############################################
#                  Qubits                   #
#############################################
qubit_LO_q1 = 3.955 * u.GHz #4.070 * u.GHz  #(4.070-0.15-0.15) * u.GHz#(4.070 - 0.15- 0.25 - 0.2 - 0.12) * u.GHz
qubit_LO_q2 = 4.215 * u.GHz
qubit_LO_q3 = 3.955 * u.GHz
qubit_LO_q4 = 4.385 * u.GHz
qubit_LO_q5 = 3.95 * u.GHz

# Qubits IF
# qubit_IF_q1 = (-118.43-2.255/2) * u.MHz  # optifined
# qubit_IF_q2 = (216.36) * u.MHz  # optifined
qubit_IF_q1 = -80 * u.MHz#(-80+10.6-6.3-18.4+44.4-6-15.3-3) * u.MHz #(-317.2) * u.MHz   #(-132+4.7+0.1-1.2+1.42) * u.MHz
qubit_IF_q2 =  (-82.05 - 5.93 + 7 + 3.45-0.7 +0.55) * u.MHz
qubit_IF_q3 = -80 * u.MHz
qubit_IF_q4 = -80 * u.MHz
qubit_IF_q5 = -80 * u.MHz
# for comparing 2q:
# qubit_IF_q1 = 0 * u.MHz
# qubit_IF_q2 = 0 * u.MHz

# Mixer parameters
mixer_qubit_g_q1 = 0.00
mixer_qubit_g_q2 = 0.00
mixer_qubit_phi_q1 = 0.0
mixer_qubit_phi_q2 = 0.0

# Relaxation time
qubit1_T1 = int(3 * u.us)
qubit2_T1 = int(3 * u.us)
# thermalization_time = 5 * max(qubit1_T1, qubit2_T1)  # optifined
thermalization_time = 100 * u.us

# CW pulse parameter
const_len = 1000
const_amp = 300 * u.mV

# Saturation_pulse
saturation_len = 5 * u.us
# saturation_amp = 0.27  # optifined
saturation_amp = 0.5


# Pi pulse parameters
pi_len = 40
pi_sigma = pi_len / 4
pi_len_q1 = 40
pi_sigma_q1 = pi_len_q1 / 4
pi_len_q2 = 40
pi_sigma_q2 = pi_len_q2 / 4
# pi_amp_q1 = 0.141  # optifined
# pi_amp_q2 = 0.443  # optifinedS
pi_amp_q1 = 0.1 * 0.985 * 0.94 *0.935
pi_amp_q2 = 0.1 * 0.425#0.1 * 1.114 * 0.94 


# DRAG coefficients
drag_coef_q1 = 0
drag_coef_q2 = 0
anharmonicity_q1 = -200 * u.MHz
anharmonicity_q2 = -200 * u.MHz
AC_stark_detuning_q1 = 0 * u.MHz
AC_stark_detuning_q2 = 0 * u.MHz

# DRAG waveforms
x180_wf_q1, x180_der_wf_q1 = np.array(
    drag_gaussian_pulse_waveforms(pi_amp_q1, pi_len_q1, pi_sigma_q1, drag_coef_q1, anharmonicity_q1, AC_stark_detuning_q1)
)
x180_I_wf_q1 = x180_wf_q1
x180_Q_wf_q1 = x180_der_wf_q1
x180_wf_q2, x180_der_wf_q2 = np.array(
    drag_gaussian_pulse_waveforms(pi_amp_q2, pi_len_q2, pi_sigma_q2, drag_coef_q2, anharmonicity_q2, AC_stark_detuning_q2)
)
x180_I_wf_q2 = x180_wf_q2
x180_Q_wf_q2 = x180_der_wf_q2
# No DRAG when alpha=0, it's just a gaussian.

x90_wf_q1, x90_der_wf_q1 = np.array(
    drag_gaussian_pulse_waveforms(pi_amp_q1 / 2, pi_len_q1, pi_sigma_q1, drag_coef_q1, anharmonicity_q1, AC_stark_detuning_q1)
)
x90_I_wf_q1 = x90_wf_q1
x90_Q_wf_q1 = x90_der_wf_q1
x90_wf_q2, x90_der_wf_q2 = np.array(
    drag_gaussian_pulse_waveforms(pi_amp_q2 / 2, pi_len_q2, pi_sigma_q2, drag_coef_q2, anharmonicity_q2, AC_stark_detuning_q2)
)
x90_I_wf_q2 = x90_wf_q2
x90_Q_wf_q2 = x90_der_wf_q2
# No DRAG when alpha=0, it's just a gaussian.

minus_x90_wf_q1, minus_x90_der_wf_q1 = np.array(
    drag_gaussian_pulse_waveforms(
        -pi_amp_q1 / 2, pi_len_q1, pi_sigma_q1, drag_coef_q1, anharmonicity_q1, AC_stark_detuning_q1
    )
)
minus_x90_I_wf_q1 = minus_x90_wf_q1
minus_x90_Q_wf_q1 = minus_x90_der_wf_q1
minus_x90_wf_q2, minus_x90_der_wf_q2 = np.array(
    drag_gaussian_pulse_waveforms(
        -pi_amp_q2 / 2, pi_len_q2, pi_sigma_q2, drag_coef_q2, anharmonicity_q2, AC_stark_detuning_q2
    )
)
minus_x90_I_wf_q2 = minus_x90_wf_q2
minus_x90_Q_wf_q2 = minus_x90_der_wf_q2
# No DRAG when alpha=0, it's just a gaussian.

y180_wf_q1, y180_der_wf_q1 = np.array(
    drag_gaussian_pulse_waveforms(pi_amp_q1, pi_len_q1, pi_sigma_q1, drag_coef_q1, anharmonicity_q1, AC_stark_detuning_q1)
)
y180_I_wf_q1 = (-1) * y180_der_wf_q1
y180_Q_wf_q1 = y180_wf_q1
y180_wf_q2, y180_der_wf_q2 = np.array(
    drag_gaussian_pulse_waveforms(pi_amp_q2, pi_len_q2, pi_sigma_q2, drag_coef_q2, anharmonicity_q2, AC_stark_detuning_q2)
)
y180_I_wf_q2 = (-1) * y180_der_wf_q2
y180_Q_wf_q2 = y180_wf_q2
# No DRAG when alpha=0, it's just a gaussian.

y90_wf_q1, y90_der_wf_q1 = np.array(
    drag_gaussian_pulse_waveforms(pi_amp_q1 / 2, pi_len_q1, pi_sigma_q1, drag_coef_q1, anharmonicity_q1, AC_stark_detuning_q1)
)
y90_I_wf_q1 = (-1) * y90_der_wf_q1
y90_Q_wf_q1 = y90_wf_q1
y90_wf_q2, y90_der_wf_q2 = np.array(
    drag_gaussian_pulse_waveforms(pi_amp_q2 / 2, pi_len_q2, pi_sigma_q2, drag_coef_q2, anharmonicity_q2, AC_stark_detuning_q2)
)
y90_I_wf_q2 = (-1) * y90_der_wf_q2
y90_Q_wf_q2 = y90_wf_q2
# No DRAG when alpha=0, it's just a gaussian.

minus_y90_wf_q1, minus_y90_der_wf_q1 = np.array(
    drag_gaussian_pulse_waveforms(
        -pi_amp_q1 / 2, pi_len_q1, pi_sigma_q1, drag_coef_q1, anharmonicity_q1, AC_stark_detuning_q1
    )
)
minus_y90_I_wf_q1 = (-1) * minus_y90_der_wf_q1
minus_y90_Q_wf_q1 = minus_y90_wf_q1
minus_y90_wf_q2, minus_y90_der_wf_q2 = np.array(
    drag_gaussian_pulse_waveforms(
        -pi_amp_q2 / 2, pi_len_q2, pi_sigma_q2, drag_coef_q2, anharmonicity_q2, AC_stark_detuning_q2
    )
)
minus_y90_I_wf_q2 = (-1) * minus_y90_der_wf_q2
minus_y90_Q_wf_q2 = minus_y90_wf_q2
# No DRAG when alpha=0, it's just a gaussian.

##########################################
#               Flux line                #
##########################################
flux_settle_time = 300 * u.ns

# max_frequency_point1 = 0.203 + 0.05
# max_frequency_point1 = 0.054+0.158#0.207-0.15#-0.005
# max_frequency_point2 = 0.196#0.188 + 0.019 #- 0.15 
# max_frequency_point3 = 0.203#-0.007
# max_frequency_point4 = 0.145#0.165 + 0.011

max_frequency_point1 = 0#0.208-0.011-0.04-0.014+0.055#-0.016
max_frequency_point2 = 0#0.194-0.008
max_frequency_point3 = 0.2+0.011
max_frequency_point4 = 0

# Resonator frequency versus flux fit parameters according to resonator_spec_vs_flux
# amplitude * np.cos(2 * np.pi * frequency * x + phase) + offset
amplitude_fit1, frequency_fit1, phase_fit1, offset_fit1 = [0, 0, 0, 0]
amplitude_fit2, frequency_fit2, phase_fit2, offset_fit2 = [0, 0, 0, 0]
amplitude_fit3, frequency_fit3, phase_fit3, offset_fit3 = [0, 0, 0, 0]

const_flux_len = 200
const_flux_amp = 0.45

#############################################
#                Resonators                 #
#############################################
resonator_LO = 5.9 * u.GHz
# Resonators IF
# resonator_IF_q1 = int((-246.989 - 1) * u.MHz)  #actually Qubit 1  #-58.9, 134.9, -135.9, -247.6, 39.7
# resonator_IF_q1 = int( -156.941 * u.MHz)
# resonator_IF_q2 = int( 130.3307 * u.MHz)#(130.267-0.556) * u.MHz)  #actually Qubit 2
# resonator_IF_q3 = int( -44.966 * u.MHz)  #actually Qubit 3    #-135.005 - 0.9 + 90
# resonator_IF_q4 = int( 225.408 * u.MHz)  #actually Qubit 4  #135.432 + 90
# resonator_IF_q5 = int( (-58.9 + 90) * u.MHz)  #actually Qubit 5

resonator_IF_q1 = int( -158.036 * u.MHz) #(-156.963-0.09-0.051) * u.MHz
resonator_IF_q2 = int( 129.643 * u.MHz)#(130.267-0.556) * u.MHz)  #actually Qubit 2    #129.67
resonator_IF_q3 = int( -45.164 * u.MHz)  #actually Qubit 3    #-135.005 - 0.9 + 90
resonator_IF_q4 = int( 224.78 * u.MHz)  #actually Qubit 4  #135.432 + 90
resonator_IF_q5 = int( (-58.9 + 90) * u.MHz)  #actually Qubit 5

# Mixer parameters
mixer_resonator_g_q1 = 0.0
mixer_resonator_g_q2 = 0.0
mixer_resonator_phi_q1 = -0.00
mixer_resonator_phi_q2 = -0.00

# Readout pulse parameters
# readout_len = 3200  # optimized
readout_len = 2000

# readout_amp_q1 = 0.07*0.37  # optimized
# readout_amp_q2 = 0.15*0.37  # optimized
# readout_amp_q3 = 0.03
# readout_amp_q4 = 0.03
# readout_amp_q5 = 0.03
# readout_amp_q1 = 0.00325
readout_amp_q1 = 0.008
readout_amp_q2 = 0.01
readout_amp_q3 = 0.015#0.0175
readout_amp_q4 = 0.015#0.0239
readout_amp_q5 = 0.01

# TOF and depletion time
time_of_flight = 288  # must be a multiple of 4
depletion_time = 10 * u.us

# AC Stark Shift
stark_len_rr1 = 2000
ac_stark_amp1 = 0.008
stark_len_rr2 = 2000
ac_stark_amp2 = 0.014

opt_weights = False
if opt_weights:
    from qualang_tools.config.integration_weights_tools import convert_integration_weights

    weights_q1 = np.load("optimal_weights_q1.npz")
    opt_weights_real_q1 = convert_integration_weights(weights_q1["weights_real"])
    opt_weights_minus_imag_q1 = convert_integration_weights(weights_q1["weights_minus_imag"])
    opt_weights_imag_q1 = convert_integration_weights(weights_q1["weights_imag"])
    opt_weights_minus_real_q1 = convert_integration_weights(weights_q1["weights_minus_real"])
    weights_q2 = np.load("optimal_weights_q2.npz")
    opt_weights_real_q2 = convert_integration_weights(weights_q2["weights_real"])
    opt_weights_minus_imag_q2 = convert_integration_weights(weights_q2["weights_minus_imag"])
    opt_weights_imag_q2 = convert_integration_weights(weights_q2["weights_imag"])
    opt_weights_minus_real_q2 = convert_integration_weights(weights_q2["weights_minus_real"])
else:
    opt_weights_real_q1 = [(1.0, readout_len)]
    opt_weights_minus_imag_q1 = [(1.0, readout_len)]
    opt_weights_imag_q1 = [(1.0, readout_len)]
    opt_weights_minus_real_q1 = [(1.0, readout_len)]
    opt_weights_real_q2 = [(1.0, readout_len)]
    opt_weights_minus_imag_q2 = [(1.0, readout_len)]
    opt_weights_imag_q2 = [(1.0, readout_len)]
    opt_weights_minus_real_q2 = [(1.0, readout_len)]

# state discrimination
# rotation_angle_q1 = (13.6 / 180) * np.pi  # optifined
# rotation_angle_q2 = (296.1 / 180) * np.pi  # optifined
rotation_angle_q1 = (274.3 / 180) * np.pi
rotation_angle_q2 = (136.1 / 180) * np.pi
# ge_threshold_q1 = 1.861e-03  # optifined
# ge_threshold_q2 = 1.100e-03  # optifined
ge_threshold_q1 = 1.97e-3
ge_threshold_q2 = 1.24e-3

#############################################
#                  Config                   #
#############################################
config = {
    "version": 1,
    "controllers": {
        "con1": {
            "analog_outputs": {
                1: {"offset": 0.0},  # I readout line
                2: {"offset": 0.0},  # Q readout line
                3: {"offset": 0.0},  # I qubit1 XY
                4: {"offset": 0.0},  # Q qubit1 XY
                5: {"offset": max_frequency_point1},  # qubit1 Z
                6: {"offset": max_frequency_point2},  # qubit2 Z
                7: {"offset": 0.0},  # I qubit2 XY
                8: {"offset": 0.0},  # Q qubit2 XY
                9: {"offset": max_frequency_point3},  # qubit3 Z
                10: {"offset": max_frequency_point4},  # qubit4 Z
            },
            "digital_outputs": {
                1: {},
            },
            "analog_inputs": {
                1: {"offset": 0.0156584060058594, "gain_db": 0},  # I from down-conversion
                2: {"offset": 0.00627351550292969, "gain_db": 0},  # Q from down-conversion
            },
        },
    },
    "elements": {
        "rr1": {
            "mixInputs": {
                "I": ("con1", 1),
                "Q": ("con1", 2),
                "lo_frequency": resonator_LO,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": resonator_IF_q1,  # frequency at offset ch7
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q1",
                "stark": "stark_pulse_rr1",
            },
            "outputs": {
                "out1": ("con1", 1),
                "out2": ("con1", 2),
            },
            "time_of_flight": time_of_flight,
            "smearing": 0,
        },
        "rr2": {
            "mixInputs": {
                "I": ("con1", 1),
                "Q": ("con1", 2),
                "lo_frequency": resonator_LO,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": resonator_IF_q2,  # frequency at offset ch8
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q2",
            },
            "outputs": {
                "out1": ("con1", 1),
                "out2": ("con1", 2),
            },
            "time_of_flight": time_of_flight,
            "smearing": 0,
        },
        "rr3": {
            "mixInputs": {
                "I": ("con1", 1),
                "Q": ("con1", 2),
                "lo_frequency": resonator_LO,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": resonator_IF_q3,  # frequency at offset ch9
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q3",
            },
            "outputs": {
                "out1": ("con1", 1),
                "out2": ("con1", 2),
            },
            "time_of_flight": time_of_flight,
            "smearing": 0,
        },
        "rr4": {
            "mixInputs": {
                "I": ("con1", 1),
                "Q": ("con1", 2),
                "lo_frequency": resonator_LO,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": resonator_IF_q4,  # frequency at offset ch9
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q4",
            },
            "outputs": {
                "out1": ("con1", 1),
                "out2": ("con1", 2),
            },
            "time_of_flight": time_of_flight,
            "smearing": 0,
        },
        "rr5": {
            "mixInputs": {
                "I": ("con1", 1),
                "Q": ("con1", 2),
                "lo_frequency": resonator_LO,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": resonator_IF_q5,  # frequency at offset ch9
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q5",
            },
            "outputs": {
                "out1": ("con1", 1),
                "out2": ("con1", 2),
            },
            "time_of_flight": time_of_flight,
            "smearing": 0,
        },
        "q1_xy": {
            "mixInputs": {
                "I": ("con1", 3),
                "Q": ("con1", 4),
                "lo_frequency": qubit_LO_q1,
                "mixer": "octave_octave1_2",
            },
            "intermediate_frequency": qubit_IF_q1,  # frequency at offset ch7 (max freq)
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
                "I": ("con1", 7),
                "Q": ("con1", 8),
                "lo_frequency": qubit_LO_q2,
                "mixer": "octave_octave1_4",
            },
            "intermediate_frequency": qubit_IF_q2,  # frequency at offset ch8 (max freq)
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
        "q1_ro": {
            "mixInputs": {
                "I": ("con1", 1),
                "Q": ("con1", 2),
                "lo_frequency": resonator_LO,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": resonator_IF_q1,  # frequency at offset ch7 (max freq)
            "operations": {
                "stark": "stark_pulse_rr1",      
            },
        },
        "q2_ro": {
            "mixInputs": {
                "I": ("con1", 1),
                "Q": ("con1", 2),
                "lo_frequency": resonator_LO,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": resonator_IF_q2,  # frequency at offset ch7 (max freq)
            "operations": {
                "stark": "stark_pulse_rr2",      
            },
        },
        "q1_z": {
            "singleInput": {
                "port": ("con1", 5),
            },
            "operations": {
                "const": "const_flux_pulse",
            },
        },
        "q2_z": {
            "singleInput": {
                "port": ("con1", 6),
            },
            "operations": {
                "const": "const_flux_pulse",
            },
        },
        "q3_z": {
            "singleInput": {
                "port": ("con1", 9),
            },
            "operations": {
                "const": "const_flux_pulse",
            },
        },
        "q4_z": {
            "singleInput": {
                "port": ("con1", 10),
            },
            "operations": {
                "const": "const_flux_pulse",
            },
        },
    },
    "pulses": {
        "const_flux_pulse": {
            "operation": "control",
            "length": const_flux_len,
            "waveforms": {
                "single": "const_flux_wf",
            },
        },
        "const_pulse": {
            "operation": "control",
            "length": const_len,
            "waveforms": {
                "I": "const_wf",
                "Q": "zero_wf",
            },
        },
        "stark_pulse_rr1": {
            "operation": "control",
            "length": stark_len_rr1,
            "waveforms": {
                "I": "ac_stark_wf1",
                "Q": "zero_wf",
            },
        },
        "stark_pulse_rr2": {
            "operation": "control",
            "length": stark_len_rr2,
            "waveforms": {
                "I": "ac_stark_wf2",
                "Q": "zero_wf",
            },
        },
        "x90_pulse_q1": {
            "operation": "control",
            "length": pi_len_q1,
            "waveforms": {
                "I": "x90_I_wf_q1",
                "Q": "x90_Q_wf_q1",
            },
        },
        "saturation_pulse": {
            "operation": "control",
            "length": saturation_len,
            "waveforms": {
                "I": "saturation_wf",
                "Q": "zero_wf",
            },
        },
        "x180_pulse_q1": {
            "operation": "control",
            "length": pi_len_q1,
            "waveforms": {
                "I": "x180_I_wf_q1",
                "Q": "x180_Q_wf_q1",
            },
        },
        "-x90_pulse_q1": {
            "operation": "control",
            "length": pi_len_q1,
            "waveforms": {
                "I": "minus_x90_I_wf_q1",
                "Q": "minus_x90_Q_wf_q1",
            },
        },
        "y90_pulse_q1": {
            "operation": "control",
            "length": pi_len_q1,
            "waveforms": {
                "I": "y90_I_wf_q1",
                "Q": "y90_Q_wf_q1",
            },
        },
        "y180_pulse_q1": {
            "operation": "control",
            "length": pi_len_q1,
            "waveforms": {
                "I": "y180_I_wf_q1",
                "Q": "y180_Q_wf_q1",
            },
        },
        "-y90_pulse_q1": {
            "operation": "control",
            "length": pi_len_q1,
            "waveforms": {
                "I": "minus_y90_I_wf_q1",
                "Q": "minus_y90_Q_wf_q1",
            },
        },
        "readout_pulse_q1": {
            "operation": "measurement",
            "length": readout_len,
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
            "length": pi_len_q2,
            "waveforms": {
                "I": "x90_I_wf_q2",
                "Q": "x90_Q_wf_q2",
            },
        },
        "x180_pulse_q2": {
            "operation": "control",
            "length": pi_len_q2,
            "waveforms": {
                "I": "x180_I_wf_q2",
                "Q": "x180_Q_wf_q2",
            },
        },
        "-x90_pulse_q2": {
            "operation": "control",
            "length": pi_len_q2,
            "waveforms": {
                "I": "minus_x90_I_wf_q2",
                "Q": "minus_x90_Q_wf_q2",
            },
        },
        "y90_pulse_q2": {
            "operation": "control",
            "length": pi_len_q2,
            "waveforms": {
                "I": "y90_I_wf_q2",
                "Q": "y90_Q_wf_q2",
            },
        },
        "y180_pulse_q2": {
            "operation": "control",
            "length": pi_len_q2,
            "waveforms": {
                "I": "y180_I_wf_q2",
                "Q": "y180_Q_wf_q2",
            },
        },
        "-y90_pulse_q2": {
            "operation": "control",
            "length": pi_len_q2,
            "waveforms": {
                "I": "minus_y90_I_wf_q2",
                "Q": "minus_y90_Q_wf_q2",
            },
        },
        "readout_pulse_q2": {
            "operation": "measurement",
            "length": readout_len,
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
        "readout_pulse_q3": {
            "operation": "measurement",
            "length": readout_len,
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
        "readout_pulse_q4": {
            "operation": "measurement",
            "length": readout_len,
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
        "readout_pulse_q5": {
            "operation": "measurement",
            "length": readout_len,
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
    },
    "waveforms": {
        "const_wf": {"type": "constant", "sample": const_amp},
        "ac_stark_wf1": {"type": "constant", "sample": ac_stark_amp1},
        "ac_stark_wf2": {"type": "constant", "sample": ac_stark_amp2},
        "saturation_wf": {"type": "constant", "sample": saturation_amp},
        "const_flux_wf": {"type": "constant", "sample": const_flux_amp},
        "zero_wf": {"type": "constant", "sample": 0.0},

        "x90_I_wf_q1": {"type": "arbitrary", "samples": x90_I_wf_q1.tolist()},
        "x90_Q_wf_q1": {"type": "arbitrary", "samples": x90_Q_wf_q1.tolist()},
        "x180_I_wf_q1": {"type": "arbitrary", "samples": x180_I_wf_q1.tolist()},
        "x180_Q_wf_q1": {"type": "arbitrary", "samples": x180_Q_wf_q1.tolist()},
        "minus_x90_I_wf_q1": {"type": "arbitrary", "samples": minus_x90_I_wf_q1.tolist()},
        "minus_x90_Q_wf_q1": {"type": "arbitrary", "samples": minus_x90_Q_wf_q1.tolist()},
        "y90_I_wf_q1": {"type": "arbitrary", "samples": y90_I_wf_q1.tolist()},
        "y90_Q_wf_q1": {"type": "arbitrary", "samples": y90_Q_wf_q1.tolist()},
        "y180_I_wf_q1": {"type": "arbitrary", "samples": y180_I_wf_q1.tolist()},
        "y180_Q_wf_q1": {"type": "arbitrary", "samples": y180_Q_wf_q1.tolist()},
        "minus_y90_I_wf_q1": {"type": "arbitrary", "samples": minus_y90_I_wf_q1.tolist()},
        "minus_y90_Q_wf_q1": {"type": "arbitrary", "samples": minus_y90_Q_wf_q1.tolist()},
        "readout_wf_q1": {"type": "constant", "sample": readout_amp_q1},

        "x90_I_wf_q2": {"type": "arbitrary", "samples": x90_I_wf_q2.tolist()},
        "x90_Q_wf_q2": {"type": "arbitrary", "samples": x90_Q_wf_q2.tolist()},
        "x180_I_wf_q2": {"type": "arbitrary", "samples": x180_I_wf_q2.tolist()},
        "x180_Q_wf_q2": {"type": "arbitrary", "samples": x180_Q_wf_q2.tolist()},
        "minus_x90_I_wf_q2": {"type": "arbitrary", "samples": minus_x90_I_wf_q2.tolist()},
        "minus_x90_Q_wf_q2": {"type": "arbitrary", "samples": minus_x90_Q_wf_q2.tolist()},
        "y90_I_wf_q2": {"type": "arbitrary", "samples": y90_I_wf_q2.tolist()},
        "y90_Q_wf_q2": {"type": "arbitrary", "samples": y90_Q_wf_q2.tolist()},
        "y180_I_wf_q2": {"type": "arbitrary", "samples": y180_I_wf_q2.tolist()},
        "y180_Q_wf_q2": {"type": "arbitrary", "samples": y180_Q_wf_q2.tolist()},
        "minus_y90_I_wf_q2": {"type": "arbitrary", "samples": minus_y90_I_wf_q2.tolist()},
        "minus_y90_Q_wf_q2": {"type": "arbitrary", "samples": minus_y90_Q_wf_q2.tolist()},
        "readout_wf_q2": {"type": "constant", "sample": readout_amp_q2},

        "x90_I_wf_q3": {"type": "arbitrary", "samples": x90_I_wf_q2.tolist()},  #not yet defined for q3
        "x90_Q_wf_q3": {"type": "arbitrary", "samples": x90_Q_wf_q2.tolist()},
        "x180_I_wf_q3": {"type": "arbitrary", "samples": x180_I_wf_q2.tolist()},
        "x180_Q_wf_q3": {"type": "arbitrary", "samples": x180_Q_wf_q2.tolist()},
        "minus_x90_I_wf_q3": {"type": "arbitrary", "samples": minus_x90_I_wf_q2.tolist()},
        "minus_x90_Q_wf_q3": {"type": "arbitrary", "samples": minus_x90_Q_wf_q2.tolist()},
        "y90_I_wf_q3": {"type": "arbitrary", "samples": y90_I_wf_q2.tolist()},
        "y90_Q_wf_q3": {"type": "arbitrary", "samples": y90_Q_wf_q2.tolist()},
        "y180_I_wf_q3": {"type": "arbitrary", "samples": y180_I_wf_q2.tolist()},
        "y180_Q_wf_q3": {"type": "arbitrary", "samples": y180_Q_wf_q2.tolist()},
        "minus_y90_I_wf_q3": {"type": "arbitrary", "samples": minus_y90_I_wf_q2.tolist()},
        "minus_y90_Q_wf_q3": {"type": "arbitrary", "samples": minus_y90_Q_wf_q2.tolist()},
        "readout_wf_q3": {"type": "constant", "sample": readout_amp_q3},
        
        "x90_I_wf_q4": {"type": "arbitrary", "samples": x90_I_wf_q2.tolist()},  #not yet defined for q4
        "x90_Q_wf_q4": {"type": "arbitrary", "samples": x90_Q_wf_q2.tolist()},
        "x180_I_wf_q4": {"type": "arbitrary", "samples": x180_I_wf_q2.tolist()},
        "x180_Q_wf_q4": {"type": "arbitrary", "samples": x180_Q_wf_q2.tolist()},
        "minus_x90_I_wf_q4": {"type": "arbitrary", "samples": minus_x90_I_wf_q2.tolist()},
        "minus_x90_Q_wf_q4": {"type": "arbitrary", "samples": minus_x90_Q_wf_q2.tolist()},
        "y90_I_wf_q4": {"type": "arbitrary", "samples": y90_I_wf_q2.tolist()},
        "y90_Q_wf_q4": {"type": "arbitrary", "samples": y90_Q_wf_q2.tolist()},
        "y180_I_wf_q4": {"type": "arbitrary", "samples": y180_I_wf_q2.tolist()},
        "y180_Q_wf_q4": {"type": "arbitrary", "samples": y180_Q_wf_q2.tolist()},
        "minus_y90_I_wf_q4": {"type": "arbitrary", "samples": minus_y90_I_wf_q2.tolist()},
        "minus_y90_Q_wf_q4": {"type": "arbitrary", "samples": minus_y90_Q_wf_q2.tolist()},
        "readout_wf_q4": {"type": "constant", "sample": readout_amp_q4},

        "x90_I_wf_q5": {"type": "arbitrary", "samples": x90_I_wf_q2.tolist()},  #not yet defined for q5
        "x90_Q_wf_q5": {"type": "arbitrary", "samples": x90_Q_wf_q2.tolist()},
        "x180_I_wf_q5": {"type": "arbitrary", "samples": x180_I_wf_q2.tolist()},
        "x180_Q_wf_q5": {"type": "arbitrary", "samples": x180_Q_wf_q2.tolist()},
        "minus_x90_I_wf_q5": {"type": "arbitrary", "samples": minus_x90_I_wf_q2.tolist()},
        "minus_x90_Q_wf_q5": {"type": "arbitrary", "samples": minus_x90_Q_wf_q2.tolist()},
        "y90_I_wf_q5": {"type": "arbitrary", "samples": y90_I_wf_q2.tolist()},
        "y90_Q_wf_q5": {"type": "arbitrary", "samples": y90_Q_wf_q2.tolist()},
        "y180_I_wf_q5": {"type": "arbitrary", "samples": y180_I_wf_q2.tolist()},
        "y180_Q_wf_q5": {"type": "arbitrary", "samples": y180_Q_wf_q2.tolist()},
        "minus_y90_I_wf_q5": {"type": "arbitrary", "samples": minus_y90_I_wf_q2.tolist()},
        "minus_y90_Q_wf_q5": {"type": "arbitrary", "samples": minus_y90_Q_wf_q2.tolist()},
        "readout_wf_q5": {"type": "constant", "sample": readout_amp_q5},
    },
    "digital_waveforms": {
        "ON": {"samples": [(1, 0)]},
    },
    "integration_weights": {
        "cosine_weights": {
            "cosine": [(1.0, readout_len)],
            "sine": [(0.0, readout_len)],
        },
        "sine_weights": {
            "cosine": [(0.0, readout_len)],
            "sine": [(1.0, readout_len)],
        },
        "minus_sine_weights": {
            "cosine": [(0.0, readout_len)],
            "sine": [(-1.0, readout_len)],
        },
        "rotated_cosine_weights_q1": {
            "cosine": [(np.cos(rotation_angle_q1), readout_len)],
            "sine": [(np.sin(rotation_angle_q1), readout_len)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(-np.sin(rotation_angle_q1), readout_len)],
            "sine": [(np.cos(rotation_angle_q1), readout_len)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(np.sin(rotation_angle_q1), readout_len)],
            "sine": [(-np.cos(rotation_angle_q1), readout_len)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(np.cos(rotation_angle_q2), readout_len)],
            "sine": [(np.sin(rotation_angle_q2), readout_len)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(-np.sin(rotation_angle_q2), readout_len)],
            "sine": [(np.cos(rotation_angle_q2), readout_len)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(np.sin(rotation_angle_q2), readout_len)],
            "sine": [(-np.cos(rotation_angle_q2), readout_len)],
        },
        "opt_cosine_weights_q1": {
            "cosine": opt_weights_real_q1,
            "sine": opt_weights_minus_imag_q1,
        },
        "opt_sine_weights_q1": {
            "cosine": opt_weights_imag_q1,
            "sine": opt_weights_real_q1,
        },
        "opt_minus_sine_weights_q1": {
            "cosine": opt_weights_minus_imag_q1,
            "sine": opt_weights_minus_real_q1,
        },
        "opt_cosine_weights_q2": {
            "cosine": opt_weights_real_q2,
            "sine": opt_weights_minus_imag_q2,
        },
        "opt_sine_weights_q2": {
            "cosine": opt_weights_imag_q2,
            "sine": opt_weights_real_q2,
        },
        "opt_minus_sine_weights_q2": {
            "cosine": opt_weights_minus_imag_q2,
            "sine": opt_weights_minus_real_q2,
        },
    },
    "mixers": {
        "octave_octave1_2": [
            {
                "intermediate_frequency": qubit_IF_q1,
                "lo_frequency": qubit_LO_q1,
                "correction": (1, 0, 0, 1),
            },
        ],
        "octave_octave1_3": [
            {
                "intermediate_frequency": qubit_IF_q3,
                "lo_frequency": qubit_LO_q1,
                "correction": (1, 0, 0, 1),
            }
        ],
        "octave_octave1_4": [
            {
                "intermediate_frequency": qubit_IF_q2,
                "lo_frequency": qubit_LO_q2,
                "correction": (1, 0, 0, 1),
            }
        ],
        "octave_octave1_5": [
            {
                "intermediate_frequency": qubit_IF_q4,
                "lo_frequency": qubit_LO_q2,
                "correction": (1, 0, 0, 1),
            }
        ],
        "octave_octave1_6": [
            {
                "intermediate_frequency": qubit_IF_q5,
                "lo_frequency": qubit_LO_q5,
                "correction": (1, 0, 0, 1),
            }
        ],

        "octave_octave1_1": [
            {
                "intermediate_frequency": resonator_IF_q1,
                "lo_frequency": resonator_LO,
                "correction": (1, 0, 0, 1),
            },
            {
                "intermediate_frequency": resonator_IF_q2,
                "lo_frequency": resonator_LO,
                "correction": (1, 0, 0, 1),
            },
            {
                "intermediate_frequency": resonator_IF_q3,
                "lo_frequency": resonator_LO,
                "correction": (1, 0, 0, 1),
            },
            {
                "intermediate_frequency": resonator_IF_q4,
                "lo_frequency": resonator_LO,
                "correction": (1, 0, 0, 1),
            },
            {
                "intermediate_frequency": resonator_IF_q5,
                "lo_frequency": resonator_LO,
                "correction": (1, 0, 0, 1),
            },
        ],
    },
}

if __name__ == '__main__':
    import pickle
    # define dictionary
    # create a binary pickle file
    path = "Octave_config.pkl" 
    f = open(path,"wb")
    # write the python object (dict) to pickle file
    pickle.dump(config,f)
    # close file
    f.close()