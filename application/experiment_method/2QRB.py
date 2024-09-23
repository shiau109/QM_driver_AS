# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

import random
from typing import List

import cirq 
import matplotlib.pyplot as plt
from qm.qua import *
from qm import QuantumMachinesManager
from qualang_tools.bakery.bakery import Baking
from qm.jobs.running_qm_job import RunningQmJob


from ab.QM_config_dynamic import initializer

from exp.two_qubit_rb.TwoQubitRB import TwoQubitRb_AS
my_exp = TwoQubitRb_AS(config, qmm)
my_exp.circuit_depths = [0, 1]
my_exp.num_circuits_per_depth = 2
shot_num = 2
my_exp.preprocess = "shot"
dataset = my_exp.run(shot_num)
print(dataset)
from exp.two_qubit_rb.RBResult import RBResult
res = RBResult(
            circuit_depths=my_exp.circuit_depths,
            num_repeats=my_exp.num_circuits_per_depth,
            num_averages=shot_num,
            state=dataset.coords["state"],
        )
# circuit_depths ~ how many consecutive Clifford gates within one executed circuit
# (https://qiskit.org/documentation/apidoc/circuit.html)
# num_circuits_per_depth ~ how many random circuits within one depth
# num_shots_per_circuit ~ repetitions of the same circuit (averaging)

# res.plot_hist()
# plt.show()

# res.plot_with_fidelity()
# plt.show()

save_dir = link_config["path"]["output_root"]
# verify/save the random sequences created during the experiment
my_exp.save_sequences_to_file(f"{save_dir}/sequences.txt")  # saves the gates used in each random sequence
my_exp.save_command_mapping_to_file(f"{save_dir}/commands.txt")  # saves mapping from "command id" to sequence
# rb.print_sequence()
# rb.print_command_mapping()
# rb.verify_sequences()  # simulates random sequences to ensure they recover to ground state. takes a while...

# # get the interleaved gate fidelity
# from two_qubit_rb.RBResult import get_interleaved_gate_fidelity
# interleaved_gate_fidelity = get_interleaved_gate_fidelity(
#     num_qubits=2,
#     reference_alpha=0.12345,  # replace with value from prior, non-interleaved experiment
#     # interleaved_alpha=res.fit_exponential()[1],  # alpha from the interleaved experiment
# )
# print(f"Interleaved Gate Fidelity: {interleaved_gate_fidelity*100:.3f}")
