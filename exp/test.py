import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
from common_fitting_func import *
import numpy as np
from common_fitting_func import *
from macros import qua_declaration, multiplexed_readout
from qualang_tools.bakery import baking
import warnings

warnings.filterwarnings("ignore")

def baked_waveform(waveform, pulse_duration, flux_qubit):
    pulse_segments = []  # Stores the baking objects
    # Create the different baked sequences, each one corresponding to a different truncated duration
    with baking(config, padding_method="right") as b:
        if pulse_duration == 0:  # Otherwise, the baking will be empty and will not be created
            wf = [0.0] * 16
        else:
            wf = waveform.tolist()
        b.add_op("flux_pulse", f"q{flux_qubit}_z", wf)
        b.play("flux_pulse", f"q{flux_qubit}_z")
        # Append the baking object in the list to call it from the QUA program
    pulse_segments.append(b)
    return pulse_segments

const_flux_len = 25
flux_Qi = 2 
flux_waveform = np.array([const_flux_amp] * const_flux_len)
square_pulse_segments = baked_waveform(flux_waveform, const_flux_len, flux_Qi)
for list in square_pulse_segments:
    print('-'*20)
    print(list.get_waveforms_dict())