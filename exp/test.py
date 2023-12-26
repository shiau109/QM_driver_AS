from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *
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
from cosine import Cosine

warnings.filterwarnings("ignore")

# with baking(config, padding_method='symmetric_l') as b:
#     b.add_op("x180","q1_xy",[config["waveforms"]["x180_I_wf_q1"]["samples"],config["waveforms"]["x180_Q_wf_q1"]["samples"]])

x180_wf, y180_wf, x90_wf, y90_wf, minus_x90_wf, minus_y90_wf  = [], [], [], [], [], []
for i in range(5):
    ### x180_wf[0] stands for q1_x180's waveforms
    x180_wf.append( [config["waveforms"][f"x180_I_wf_q{i+1}"]["samples"],config["waveforms"][f"x180_Q_wf_q{i+1}"]["samples"]] )
    y180_wf.append( [config["waveforms"][f"y180_I_wf_q{i+1}"]["samples"],config["waveforms"][f"y180_Q_wf_q{i+1}"]["samples"]] )
    x90_wf.append( [config["waveforms"][f"x90_I_wf_q{i+1}"]["samples"],config["waveforms"][f"x90_Q_wf_q{i+1}"]["samples"]] )
    y90_wf.append( [config["waveforms"][f"y90_I_wf_q{i+1}"]["samples"],config["waveforms"][f"y90_Q_wf_q{i+1}"]["samples"]] )
    minus_x90_wf.append( [config["waveforms"][f"minus_x90_I_wf_q{i+1}"]["samples"],config["waveforms"][f"minus_x90_Q_wf_q{i+1}"]["samples"]] )
    minus_y90_wf.append( [config["waveforms"][f"minus_y90_I_wf_q{i+1}"]["samples"],config["waveforms"][f"minus_y90_Q_wf_q{i+1}"]["samples"]] )

def x180(q_element):
    with baking(config,padding_method="symmetric_l") as b: 
        b.add_op("x180", f"q{q_element}_xy", x180_wf[q_element-1])
        b.play("x180", f"q{q_element}_xy")
        b.run()


def y180(q_element):
    with baking(config,padding_method="symmetric_l") as b: 
        b.add_op("y180", f"q{q_element}_xy", y180_wf[q_element-1])
        b.play("y180", f"q{q_element}_xy")
        b.run()

def x90(q_element):
    with baking(config,padding_method="symmetric_l") as b: 
        b.add_op("x90", f"q{q_element}_xy", x90_wf[q_element-1])
        b.play("x90", f"q{q_element}_xy")
        b.run()

def y90(q_element):
    with baking(config,padding_method="symmetric_l") as b: 
        b.add_op("y90", f"q{q_element}_xy", y90_wf[q_element-1])
        b.play("y90", f"q{q_element}_xy")
        b.run()

def minus_x90(q_element):
    with baking(config,padding_method="symmetric_l") as b: 
        b.add_op("minus_x90", f"q{q_element}_xy", minus_x90_wf[q_element-1])
        b.play("minus_x90", f"q{q_element}_xy")  
        b.run()

def minus_y90(q_element):
    with baking(config,padding_method="symmetric_l") as b: 
        b.add_op("minus_y90", f"q{q_element}_xy", minus_y90_wf[q_element-1])
        b.play("minus_y90", f"q{q_element}_xy")  
        b.run()

def idle(q_element):
    with baking(config,padding_method="symmetric_l") as b:
        b.wait(pi_len, f"q{q_element}_xy")
        b.run()

# gate_list = [minus_y90(1),x180(2),idle(2),x90(2)]
pulse_seq = None
with program() as prog:
    minus_y90(1)
    x180(2)
    idle(2)
    x90(2)


simulate = True
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config) 
if simulate:
    simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
    job = qmm.simulate(config, prog, simulation_config)
    job.get_simulated_samples().con1.plot()
    plt.show()
# with baking(config,padding_method="symmetric_l") as b:
#     b.add_op("x180", "q1_xy",[config["waveforms"]["x180_I_wf_q1"]["samples"],config["waveforms"]["x180_Q_wf_q1"]["samples"]])
#     b.add_op("I0", "q1_xy",[[3.0]*20,[3.0]*20])
#     b.add_op("I1", "q2_xy",[[2]*8,[2]*8])
#     b.align()
#     b.play("x180", "q1_xy")
    
#     b.play("I0","q1_xy")
    
#     b.play("I1","q2_xy")
# print(b.get_waveforms_dict())
