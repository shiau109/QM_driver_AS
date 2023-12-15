"""
This file is used to configure the Octave ports (gain, switch_mode, down-conversion) and calibrate the up-conversion mixers.
You need to run this file in order to update the Octaves with the new parameters.
"""
from set_octave import ElementsSettings, octave_settings
from qm.QuantumMachinesManager import QuantumMachinesManager
from QM_config_dynamic import QM_config, Circuit_info
import os
main_path = os.getcwd()

q_num = 5
config_file_path = main_path+'/OnMachine/Octave_Config/test_config'
spec_file_path = main_path+'/OnMachine/Octave_Config/test_spec'

# Configure the Octave parameters for each element
rr1 = ElementsSettings("q1_ro", gain=0, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
# rr2 = ElementsSettings("rr2", gain=0, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
# rr3 = ElementsSettings("rr3", gain=0, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
# rr4 = ElementsSettings("rr4", gain=0, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
# rr5 = ElementsSettings("rr5", gain=0, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
q1_xy = ElementsSettings("q1_xy", gain=20)
# q2_xy = ElementsSettings("q2_xy", gain=20)
# q3_xy = ElementsSettings("q3_xy", gain=20)
# q4_xy = ElementsSettings("q4_xy", gain=20)
# q5_xy = ElementsSettings("q5_xy", gain=20)
# Add the "octave" elements
elements_settings = [q1_xy, rr1]

###################
# Octave settings #
###################
# Configure the Octave according to the elements settings and calibrate

dyna_config = QM_config()
dyna_config.import_config(config_file_path)
the_specs = Circuit_info(q_num)
the_specs.import_spec(spec_file_path)
qmm, octaves = the_specs.buildup_qmm()

dyna_config.check_mixerCorrectionPair_for('q1')

octave_settings(
    qmm=qmm,
    config=dyna_config.get_config(),
    octaves=octaves,
    elements_settings=elements_settings,
    calibration=True,
)
qmm.close()

