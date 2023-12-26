import qpu.backend.phychannel as pch
from qutip import sigmax, sigmay, sigmaz, basis, qeye, tensor, Qobj
from qutip_qip.operations import Gate #Measurement in 0.3.X qutip_qip
from qutip_qip.circuit import QubitCircuit
from qutip_qip.compiler import GateCompiler, Instruction
import numpy as np
import qpu.backend.circuit.backendcircuit as bec
import qpu.backend.component as qcp
from pandas import DataFrame
import pulse_signal.common_Mathfunc as ps 
from qualang_tools.bakery.bakery import Baking
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
import numpy as np
from qualang_tools.bakery import baking
import warnings

x180_wf, y180_wf, x90_wf, y90_wf, minus_x90_wf, minus_y90_wf  = [], [], [], [], [], []
for i in range(5):
    ### x180_wf[0] stands for q1_x180's waveforms
    x180_wf.append( [config["waveforms"][f"x180_I_wf_q{i+1}"]["samples"],config["waveforms"][f"x180_Q_wf_q{i+1}"]["samples"]] )
    y180_wf.append( [config["waveforms"][f"y180_I_wf_q{i+1}"]["samples"],config["waveforms"][f"y180_Q_wf_q{i+1}"]["samples"]] )
    x90_wf.append( [config["waveforms"][f"x90_I_wf_q{i+1}"]["samples"],config["waveforms"][f"x90_Q_wf_q{i+1}"]["samples"]] )
    y90_wf.append( [config["waveforms"][f"y90_I_wf_q{i+1}"]["samples"],config["waveforms"][f"y90_Q_wf_q{i+1}"]["samples"]] )
    minus_x90_wf.append( [config["waveforms"][f"minus_x90_I_wf_q{i+1}"]["samples"],config["waveforms"][f"minus_x90_Q_wf_q{i+1}"]["samples"]] )
    minus_y90_wf.append( [config["waveforms"][f"minus_y90_I_wf_q{i+1}"]["samples"],config["waveforms"][f"minus_y90_Q_wf_q{i+1}"]["samples"]] )

cz_wf = np.array([cz_amp]*(cz_len+1)) # cz_len+1 is the exactly time of z pulse.
cz_wf = cz_wf.tolist()


class TQCompile(GateCompiler):
    """Custom compiler for generating pulses from gates using the base class 
    GateCompiler.

    Args:
        num_qubits (int): The number of qubits in the processor
        params (dict): A dictionary of parameters for gate pulses such as
                       the pulse amplitude.
    """

    def __init__(self, num_qubits, q1_frame_update, q2_frame_update, params):
        super().__init__(num_qubits, params=params)
        self.params = params
        self.gate_compiler = {
            "x180": self.x180_compiler,
            "y180": self.y180_compiler,
            "x90": self.x90_compiler,
            "y90": self.y90_compiler,
            "minus_x90": self.minus_x90_compiler,
            "minus_y90": self.minus_y90_compiler,
            "idle": self.idle_compiler,
            "cz": self.cz_compiler,

        }
        self.q1_frame_update = q1_frame_update
        self.q2_frame_update = q2_frame_update

    def x180_compiler(self,gate,args):
        with baking(config,padding_method="symmetric_l") as b: 
            b.add_op("x180", f"q{gate.targets[0]}_xy", x180_wf[gate.targets[0]-1])
            b.play("x180", f"q{gate.targets[0]}_xy")
            b.run()
            # return b

    def y180_compiler(self,gate,args):
        with baking(config,padding_method="symmetric_l") as b: 
            b.add_op("y180", f"q{gate.targets[0]}_xy", y180_wf[gate.targets[0]-1])
            b.play("y180", f"q{gate.targets[0]}_xy")
            # b.run()
            return b

    def x90_compiler(self,gate,args):
        with baking(config,padding_method="symmetric_l") as b: 
            b.add_op("x90", f"q{gate.targets[0]}_xy", x90_wf[gate.targets[0]-1])
            b.play("x90", f"q{gate.targets[0]}_xy")
            b.run()
            # return b

    def y90_compiler(self,gate,args):
        with baking(config,padding_method="symmetric_l") as b: 
            b.add_op("y90", f"q{gate.targets[0]}_xy", y90_wf[gate.targets[0]-1])
            b.play("y90", f"q{gate.targets[0]}_xy")
            b.run()
            # return b

    def minus_x90_compiler(self,gate,args):
        with baking(config,padding_method="symmetric_l") as b: 
            b.add_op("minus_x90", f"q{gate.targets[0]}_xy", minus_x90_wf[gate.targets[0]-1])
            b.play("minus_x90", f"q{gate.targets[0]}_xy")  
            b.run()
            # return b

    def minus_y90_compiler(self,gate,args):
        with baking(config,padding_method="symmetric_l") as b: 
            b.add_op("minus_y90", f"q{gate.targets[0]}_xy", minus_y90_wf[gate.targets[0]-1])
            b.play("minus_y90", f"q{gate.targets[0]}_xy")  
            b.run()
            # return b

    def idle_compiler(self,gate,args):
        with baking(config,padding_method="symmetric_l") as b:
            b.wait(pi_len, f"q{gate.targets[0]}_xy")
            b.run()
            # return b

    def cz_compiler(self,gate,args):
        ### Crucially Important!! The target of CZ gate is the first element, which we apply flux. That is the higher freq. one.
        with baking(config,padding_method="symmetric_l") as b:
            q1_xy_element = f"q{gate.targets[0]}_xy"  
            q2_xy_element = f"q{gate.controls[0]}_xy"
            q1_z_element = f"q{gate.targets[0]}_z"
            b.add_op("cz",q1_z_element,cz_wf)
            b.wait(20,q1_xy_element,q2_xy_element,q1_z_element) # The unit is 1 ns.
            b.play("cz", q1_z_element)
            b.align(q1_xy_element,q2_xy_element,q1_z_element)
            b.wait(20,q1_xy_element,q2_xy_element,q1_z_element)
            b.frame_rotation_2pi(self.q1_frame_update, q1_xy_element)
            b.frame_rotation_2pi(self.q2_frame_update, q2_xy_element)
            b.align(q1_xy_element,q2_xy_element,q1_z_element)
            b.run()



if __name__ == '__main__':
    mycompiler = TQCompile(2,0,0,params={})
    rg_x0 = Gate("x180", 1)
    rg_y0 = Gate("y180", 1)
    rg_y1 = Gate("y90", 2)
    idle_gate = Gate("idle", 1)
    idle_gate_1 = Gate("idle", 2)
    ### Crucially Important!! The target of CZ gate is the first element, which we apply flux. That is the higher freq. one.
    cz = Gate("cz", 1, 2)

    gate_seq = [
        rg_x0, idle_gate, rg_x0, cz, rg_y1, rg_y1
    ]
    circuit = QubitCircuit(2)
    two_qubit = basis(4, 0)
    for gate in gate_seq:
        circuit.add_gate(gate)

    with program() as prog:
        compiled_data = mycompiler.compile(circuit,schedule_mode='ASAP')
    

    simulate = True
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config) 
    if simulate:
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, prog, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()

