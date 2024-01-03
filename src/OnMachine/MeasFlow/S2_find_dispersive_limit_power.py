"""
        RESONATOR SPECTROSCOPY VERSUS READOUT AMPLITUDE
This sequence involves measuring the resonator by sending a readout pulse and demodulating the signals to
extract the 'I' and 'Q' quadratures.
This is done across various readout intermediate frequencies and amplitudes.
Based on the results, one can determine if a qubit is coupled to the resonator by noting the resonator frequency
splitting. This information can then be used to adjust the readout amplitude, choosing a readout amplitude value
just before the observed frequency splitting.

Prerequisites:
    - Calibration of the time of flight, offsets, and gains (referenced as "time_of_flight").
    - Calibration of the IQ mixer connected to the readout line (be it an external mixer or an Octave port).
    - Identification of the resonator's resonance frequency (referred to as "resonator_spectroscopy_multiplexed").
    - Configuration of the readout pulse amplitude (the pulse processor will sweep up to twice this value) and duration.
    - Specification of the expected resonator depletion time in the configuration.

Before proceeding to the next node:
    - Update the readout frequency, labeled as "resonator_IF_q", in the configuration.
    - Adjust the readout amplitude, labeled as "readout_amp_q", in the configuration.
"""

from qm.qua import *
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
from exp.power_dep_resonator import *

from datetime import datetime
import sys


# 20231216 Test complete :Ratis
from OnMachine.Octave_Config.QM_config_dynamic import Circuit_info, QM_config, initializer
from OnMachine.MeasFlow.ConfigBuildUp import spec_loca, config_loca, qubit_num
spec = Circuit_info(qubit_num)
config = QM_config()
spec.import_spec(spec_loca)
config.import_config(config_loca)

qmm,_ = spec.buildup_qmm()
init_macro = initializer(spec.give_depletion_time_for("all"),mode='depletion')

n_avg = 200  # The number of averages
# The frequency sweep around the resonators' frequency "resonator_IF_q"

ro_elements = ["q1_ro","q2_ro","q3_ro","q4_ro"]
data = mRO_power_dep_resonator( ro_elements, config.get_config(), qmm, n_avg=200, amp_max_ratio=1.25, initializer=init_macro)  
results = data[0]
dfs = data[1]
amps = data[-1]
for r in ro_elements:
    fig, ax = plt.subplots()
    plot_power_dep_resonator(dfs, amps, results[r], ax)
    ax.set_title(r)
    ax.set_xlabel("additional IF freq (MHz)")
    ax.set_ylabel("amp scale")
plt.show()
 
###################
#   Data Saving   #
###################