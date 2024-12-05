"""
octave_introduction.py: shows the basic commands to control the octave's clock, synthesizers, up-converters, triggers,
down-converters and calibration
"""

from qm.octave.octave_manager import ClockMode
from qm.qua import *

#################################
# Step 0 : Octave configuration #
#################################


# Dynamic config
from pathlib import Path
# Get the current file path
current_file = Path(__file__).resolve()
# Get the parent directory
link_path = current_file.parent/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config
config_obj, spec = import_config( link_path )
qmm, octave_config = spec.buildup_qmm()

octave_name = "octave1"
elements = ["q0_xy"]
ports = [2]
gains = [0] # -20<gain<20
config = config_obj.get_config()

from exp.config_par import get_LO
for i, el in enumerate(elements):
    port = ports[i]
    gain = gains[i]
    freq_LO = get_LO(el,config)
    print(f"octave RF port{port}")
    print(f"gain={gain}dB")
    print(f"LO frequency={freq_LO/1e9}")

    config_obj.octaves[octave_name].RF_outputs[port].gain=gain
    config_obj.octaves[octave_name].RF_outputs[port].LO_frequency=freq_LO
# The elements used to test the ports of the Octave

# The configuration used here
config = config_obj.get_config()
qm = qmm.open_qm(config)
qm.octave.set_clock(octave_name, clock_mode=ClockMode.Internal)


# Simple test program that plays a continuous wave through all ports
with program() as hello_octave:
    with infinite_loop_():
        for el in elements:
            play("const", el)

#################################
# Step 5 : checking calibration #
#################################
import time

print("-" * 37 + " Play before calibration")
# Step 5.1: Connect RF1 and run these lines in order to see the uncalibrated signal first
job = qm.execute(hello_octave)
time.sleep(5)  # The program will run for 10 seconds
job.halt()
# Step 5.2: Run this in order to calibrate
for element in elements:
    print("-" * 37 + f" Calibrates {element}")
    qm.calibrate_element(element)  # can provide many IFs for specific LO
# Step 5.3: Run these and look at the spectrum analyzer and check if you get 1 peak at LO+IF (i.e. 6.05GHz)
print("-" * 37 + " Play after calibration")
job = qm.execute(hello_octave)
time.sleep(5)  # The program will run for 30 seconds
job.halt()

from QM_driver_AS.ultitly.config_io import output_config
output_config( link_path, config_obj )