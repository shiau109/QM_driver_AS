"""
octave_introduction.py: shows the basic commands to control the octave's clock, synthesizers, up-converters, triggers,
down-converters and calibration
"""

from qm import QuantumMachinesManager
from qm.octave import *
from qm.octave.octave_manager import ClockMode
from qm.qua import *
import os
import time
import matplotlib.pyplot as plt
from qualang_tools.units import unit
from qm import SimulationConfig

# Flags to switch between different modes defined below
check_up_converters = False
check_triggers = False
check_down_converters = False
calibration = True


#################################
# Step 0 : Octave configuration #
#################################


# Dynamic config
from pathlib import Path
# Get the parent directory
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config
config_obj, spec = import_config( link_path )
qmm, octave_config = spec.buildup_qmm()

config = config_obj.get_config()


octave = "octave1"
# The elements used to test the ports of the Octave
element = "q0_xy"
# IF = 50e6  # The IF frequency
# LO = 6e9  # The LO frequency
# The configuration used here
from exp.config_par import get_LO
freq_LO = get_LO(element,config)
print(f"LO frequency={freq_LO/1e9}")
###################
# The QUA program #
###################
with program() as hello_octave:
    with infinite_loop_():

        play("const" * amp(0.1), element)

#######################################
# Execute or Simulate the QUA program #
#######################################
simulate = False
if simulate:
    simulation_config = SimulationConfig(duration=400)  # in clock cycles
    job_sim = qmm.simulate(config, hello_octave, simulation_config)
    job_sim.get_simulated_samples().con1.plot()
    plt.show()
else:
    qm = qmm.open_qm(config)
    job = qm.execute(hello_octave)
    # Execute does not block python! As this is an infinite loop, the job would run forever.
    # In this case, we've put a 10 seconds sleep and then halted the job.
    time.sleep(100)
    job.halt()

