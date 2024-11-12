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

import xarray as xr

from ab.QM_config_dynamic import initializer

def assign_states_and_cleanup(ds):
    # Extract thresholds from dataset attributes
    control_threshold = ds.attrs['control_q_ro_threshold']
    target_threshold = ds.attrs['target_q_ro_threshold']
    
    # Check if q3_ro and q4_ro I-components exceed the thresholds
    state_control = ds[f"{ds.attrs['control_q']}_ro"].sel(mixer='I') > control_threshold
    state_target = ds[f"{ds.attrs['target_q']}_ro"].sel(mixer='I') > target_threshold

    # Convert boolean states to integer values (0 or 1)
    state_control_int = state_control.astype(int)
    state_target_int = state_target.astype(int)
    
    # Combine the two states into a single state variable
    state = (state_control_int << 1) + (state_target_int )
    
    # Create a new dataset containing only the combined state
    new_ds = xr.Dataset(
        {
            "state": (("circuit_depth", "repeat", "average"), state.data)  # Use .data to extract the array
        },
        coords={
            "circuit_depth": ds.circuit_depth,
            "repeat": ds.repeat,
            "average": ds.average
        },
        attrs=ds.attrs  # Keep the original attributes
    )
    
    return new_ds

def bake_phased_xz(baker: Baking, q, x, z, a):
    if q == 1:
        q=my_exp.target_q
    elif q==2:
        q=my_exp.control_q
    else:
        print("no such qubit")
    print(f"q={q}")

    baker.frame_rotation_2pi(a / 2, f"{q}_xy")
    baker.play("x180", f"{q}_xy", amp=x)
    baker.frame_rotation_2pi(-(a + z) / 2, f"{q}_xy")

def bake_cz(baker: Baking, q1, q2):

    # single qubit phase corrections in units of 2pi applied after the CZ gate
    print(f"q={q1}, {q2}")

    baker.play("const", f"{my_exp.control_q}_z", amp=my_exp.cz_control_q_amp)
    baker.play("const", f"{my_exp.coupler}_z", amp=my_exp.cz_coupler_amp)
    baker.align()
    baker.frame_rotation_2pi(my_exp.target_q_frame_correction, f"{my_exp.target_q}_xy")
    baker.frame_rotation_2pi(my_exp.control_q_frame_correction, f"{my_exp.control_q}_xy")
    baker.align()

from exp.two_qubit_rb.TwoQubitRB import TwoQubitRb_AS
my_exp = TwoQubitRb_AS(config, qmm)
my_exp.control_q = "q4"
my_exp.target_q = "q3"
my_exp.coupler = "q8"
my_exp.control_q_frame_correction = 0.8259861205684337/2/np.pi
my_exp.control_q_ro_threshold = 1.479e-04
my_exp.target_q_frame_correction = -2.4383905472625473/2/np.pi
my_exp.target_q_ro_threshold = 4.284e-05
my_exp.single_qubit_gate_generator = bake_phased_xz
my_exp.two_qubit_gate_generators = {"CZ": bake_cz}
my_exp.cz_control_q_amp = -0.3
my_exp.cz_coupler_amp = -0.212
my_exp.circuit_depths = [10, 20]
my_exp.num_circuits_per_depth = 10
my_exp.initializer=initializer(200000,mode='wait')
shot_num = 10
my_exp.preprocess = "shot"
dataset = my_exp.run(shot_num)
# print(dataset)


# Example usage
new_ds = assign_states_and_cleanup(dataset)
# print(new_ds)

from exp.two_qubit_rb.RBResult import RBResult
res = RBResult(
            circuit_depths=my_exp.circuit_depths,
            num_repeats=my_exp.num_circuits_per_depth,
            num_averages=shot_num,
            state=new_ds["state"].data,
        )
# circuit_depths ~ how many consecutive Clifford gates within one executed circuit
# (https://qiskit.org/documentation/apidoc/circuit.html)
# num_circuits_per_depth ~ how many random circuits within one depth
# num_shots_per_circuit ~ repetitions of the same circuit (averaging)
save_data = True
folder_label = f"2QRB" #your data and plots with be saved under a new folder with this name
if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,"2QRB")
    my_exp.save_sequences_to_file(f"{dp.package_root}/sequences.txt")  # saves the gates used in each random sequence
    my_exp.save_command_mapping_to_file(f"{dp.package_root}/commands.txt")  # saves mapping from "command id" to sequence

hist = res.plot_hist()
dp.save_fig(hist, "hist")
plt.show()

fidelity_curve = res.plot_with_fidelity()
dp.save_fig(fidelity_curve, "fidelity_curve")


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
