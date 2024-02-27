"""
This file is used to configure the Octave ports (gain, switch_mode, down-conversion) and calibrate the up-conversion mixers.
You need to run this file in order to update the Octaves with the new parameters.
"""
from OnMachine.SetConfig.set_octave import ElementsSettings, octave_settings

# Configure the Octave parameters for each element
rr1 = ElementsSettings("q0_ro", gain=0, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
# rr2 = ElementsSettings("q2_ro", gain=0, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
# rr3 = ElementsSettings("q3_ro", gain=0, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
# rr4 = ElementsSettings("q4_ro", gain=0, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
q1_xy = ElementsSettings("q1_xy", gain=15)
# q2_xy = ElementsSettings("q2_xy", gain=15)
# q3_xy = ElementsSettings("q3_xy", gain=15)
# q4_xy = ElementsSettings("q4_xy", gain=20)
# q5_xy = ElementsSettings("q5_xy", gain=20)
# Add the "octave" elements
elements_settings = [q1_xy]
# elements_settings = [q2_xy]

# elements_settings = [q3_xy]

###################
# Octave settings #
###################
# Configure the Octave according to the elements settings and calibrate

# Dynamic config
from OnMachine.MeasFlow.ConfigBuildUp_new import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
spec = import_spec(spec_loca)
config = import_config( config_loca )
qmm, octaves = spec.buildup_qmm()

# dyna_config.check_mixerCorrectionPair_for('q1')

octave_settings(
    qmm=qmm,
    config=config.get_config(),
    octaves=octaves,
    elements_settings=elements_settings,
    calibration=True,
)
qmm.close()

