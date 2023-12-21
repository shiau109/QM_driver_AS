"""
        RESONATOR SPECTROSCOPY VERSUS FLUX
This sequence involves measuring the resonator by sending a readout pulse and demodulating the signals to
extract the 'I' and 'Q' quadratures. This is done across various readout intermediate frequencies and flux biases.
The resonator frequency as a function of flux bias is then extracted and fitted so that the parameters can be stored in the configuration.

This information can then be used to adjust the readout frequency for the maximum frequency point.

Prerequisites:
    - Calibration of the time of flight, offsets, and gains (referenced as "time_of_flight").
    - Calibration of the IQ mixer connected to the readout line (be it an external mixer or an Octave port).
    - Identification of the resonator's resonance frequency (referred to as "resonator_spectroscopy_multiplexed").
    - Configuration of the readout pulse amplitude and duration.
    - Specification of the expected resonator depletion time in the configuration.

Before proceeding to the next node:
    - Update the readout frequency, labeled as "resonator_IF", in the configuration.
    - Adjust the flux bias to the maximum frequency point, labeled as "max_frequency_point", in the configuration.
    - Update the resonator frequency versus flux fit parameters (amplitude_fit, frequency_fit, phase_fit, offset_fit) in the configuration
"""

from qm.qua import *
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from exp.flux_dep_resonator import *

# 20231218 Test complete: Ratis
from OnMachine.Octave_Config.QM_config_dynamic import Circuit_info, QM_config, initializer
from OnMachine.MeasFlow.ConfigBuildUp import spec_loca, config_loca, qubit_num
spec = Circuit_info(qubit_num)
config = QM_config()
spec.import_spec(spec_loca)
config.import_config(config_loca)

qmm,_ = spec.buildup_qmm()
init_macro = initializer(spec.give_depletion_time_for("all"),mode='depletion')

ro_elements = ['q1_ro','q2_ro','q3_ro','q4_ro']
results, freq_axis, flux_axis = flux_dep_cavity(ro_elements, config.get_config(), qmm, initializer=init_macro)
for r in ro_elements:
    fig, ax = plt.subplots()
    plot_flux_dep_resonator(results[r], freq_axis, flux_axis, ax)
    ax.set_title(r)
    ax.set_xlabel("Flux bias")
    ax.set_ylabel("additional IF freq (MHz)")
plt.show()