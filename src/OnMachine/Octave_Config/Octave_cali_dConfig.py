"""
This file is used to configure the Octave ports (gain, switch_mode, down-conversion) and calibrate the up-conversion mixers.
You need to run this file in order to update the Octaves with the new parameters.
"""
from OnMachine.Octave_Config.set_octave import ElementsSettings, octave_settings
from OnMachine.Octave_Config.QM_config_dynamic import QM_config, Circuit_info
from OnMachine.MeasFlow.ConfigBuildUp import spec_loca, config_loca

q_num = 4

# Configure the Octave parameters for each element
rr1 = ElementsSettings("q1_ro", gain=0, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
rr2 = ElementsSettings("q2_ro", gain=0, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
rr3 = ElementsSettings("q3_ro", gain=0, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
rr4 = ElementsSettings("q4_ro", gain=0, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
# rr5 = ElementsSettings("rr5", gain=0, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
q1_xy = ElementsSettings("q1_xy", gain=15)
q2_xy = ElementsSettings("q2_xy", gain=15)
# q3_xy = ElementsSettings("q3_xy", gain=15)
# q4_xy = ElementsSettings("q4_xy", gain=20)
# q5_xy = ElementsSettings("q5_xy", gain=20)
# Add the "octave" elements
elements_settings = [rr1,rr2,rr3,rr4,q1_xy,q2_xy]
# elements_settings = [q1_xy,q2_xy]

# elements_settings = [q3_xy]

###################
# Octave settings #
###################
# Configure the Octave according to the elements settings and calibrate

dyna_config = QM_config()
dyna_config.import_config(config_loca)
the_specs = Circuit_info(q_num)
the_specs.import_spec(spec_loca)
qmm, octaves = the_specs.buildup_qmm()

# dyna_config.check_mixerCorrectionPair_for('q1')

octave_settings(
    qmm=qmm,
    config=dyna_config.get_config(),
    octaves=octaves,
    elements_settings=elements_settings,
    calibration=True,
)
qmm.close()

