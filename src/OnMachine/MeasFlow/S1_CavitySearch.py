"""
        RESONATOR SPECTROSCOPY INDIVIDUAL RESONATORS
This sequence involves measuring the resonator by sending a readout pulse and demodulating the signals to extract the
'I' and 'Q' quadratures across varying readout intermediate frequencies.
The data is then post-processed to determine the resonator resonance frequency.
This frequency can be used to update the readout intermediate frequency in the configuration under "resonator_IF".

Prerequisites:
    - Ensure calibration of the time of flight, offsets, and gains (referenced as "time_of_flight").
    - Calibrate the IQ mixer connected to the readout line (whether it's an external mixer or an Octave port).
    - Define the readout pulse amplitude and duration in the configuration.
    - Specify the expected resonator depletion time in the configuration.

Before proceeding to the next node:
    - Update the readout frequency, labeled as "resonator_IF_q1" and "resonator_IF_q2", in the configuration.
"""

from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.loops import from_array
import warnings
from OnMachine.Octave_Config.QM_config_dynamic import Circuit_info, QM_config, initializer,u
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt

from exp.search_resonators import *

# 20231215 Test complete :Ratis

# Dynamic config
from OnMachine.BringUp.ConfigBuildUp import spec_loca, config_loca, qubit_num
spec = Circuit_info(qubit_num)
config = QM_config()
spec.import_spec(spec_loca)
config.import_config(config_loca)

qmm, _ = spec.buildup_qmm()
init_macro = initializer(spec.give_depletion_time_for("q1"),mode='depletion')
idata, qdata, sweep_range = search_resonators(config.get_config(),["q1_ro"],qmm,n_avg=50,initializer=init_macro)  

# Default config
# init_macro = initializer(spec.give_depletion_time_for("q1"),mode='depletion')
# idata, qdata, sweep_range = search_resonators(config,["q1_ro"],qmm,n_avg=50,initializer=init_macro)  

plot_CS(sweep_range,idata,qdata,plot=True)

    
 

    
