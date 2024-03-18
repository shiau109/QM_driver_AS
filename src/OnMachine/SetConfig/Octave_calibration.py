"""
This file is used to configure the Octave ports (gain, switch_mode, down-conversion) and calibrate the up-conversion mixers.
You need to run this file in order to update the Octaves with the new parameters.
"""
from OnMachine.SetConfig.set_octave import ElementsSettings, octave_settings

# Configure the Octave parameters for each element
rr1 = ElementsSettings("q0_ro", gain=0, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
# rr2 = ElementsSettings("q2_ro", gain=0, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
q0_xy = ElementsSettings("q1_xy", gain=18)
q1_xy = ElementsSettings("q2_xy", gain=15)
# q2_xy = ElementsSettings("q2_xy", gain=15)

# Add the "octave" elements
elements_settings = [q0_xy]
# elements_settings = [q2_xy]


###################
# Octave settings #
###################
# Configure the Octave according to the elements settings and calibrate

# Dynamic config
from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec

spec = import_spec( spec_loca )
config = import_config( config_loca ).get_config()
qmm, octaves = spec.buildup_qmm()

# dyna_config.check_mixerCorrectionPair_for('q1')

octave_settings(
    qmm=qmm,
    config=config,
    octaves=octaves,
    elements_settings=elements_settings,
    calibration=True,
)
qmm.close()

