# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save



import random
from typing import List

import cirq 
import matplotlib.pyplot as plt
from qm.qua import *
from qm import QuantumMachinesManager
from qualang_tools.bakery.bakery import Baking
# from configuration import *
from exp.two_qubit_rb import TwoQubitRb

##############################
## General helper functions ##
##############################
def multiplexed_readout(I, I_st, Q, Q_st, resonators, sequential=False, amplitude=1.0, weights=""):
    """Perform multiplexed readout on two resonators"""
    if type(resonators) is not list:
        resonators = [resonators]

    for ind, res in enumerate(resonators):
        measure(
            "readout" * amp(amplitude),
            f"q{res}_ro",
            None,
            dual_demod.full(weights + "cos", "out1", weights + "sin", "out2", I[ind]),
            dual_demod.full(weights + "minus_sin", "out1", weights + "cos", "out2", Q[ind]),
        )

        if I_st is not None:
            save(I[ind], I_st[ind])
        if Q_st is not None:
            save(Q[ind], Q_st[ind])

        if sequential and ind < len(resonators) - 1:
            align(f"q{res}_ro", f"q{res+1}_ro")


##############################
##  Two-qubit RB functions  ##
##############################



# single qubit generic gate constructor Z^{z}Z^{a}X^{x}Z^{-a}
# that can reach any point on the Bloch sphere (starting from arbitrary points)
def bake_phased_xz(baker: Baking, q, x, z, a):
    if q == 1:
        q=q3
    elif q==2:
        q=q4
    # else:
    #     print("no such qubit")
    # print(f"q={q}")

    baker.frame_rotation_2pi(a / 2, f"q{q}_xy")
    baker.play("x180", f"q{q}_xy", amp=x)
    baker.frame_rotation_2pi(-(a + z) / 2, f"q{q}_xy")
    # baker.align()






# defines the CZ gate that realizes the mapping |00> -> |00>, |01> -> |01>, |10> -> |10>, |11> -> -|11>
def bake_cz(baker: Baking, q1, q2):
    q1=q3
    q2=q4
    cz_q2_amp = cz_q4_amp
    # single qubit phase corrections in units of 2pi applied after the CZ gate
    qubit1_frame_update = qubit3_frame_update# ask 安哥"  # example values, should be taken from QPU parameters
    qubit2_frame_update = qubit4_frame_update# ask 安哥"  # example values, should be taken from QPU parameters
    # print(f"q={q1}, {q2}")
    
    baker.align()
    # baker.wait(20)
    baker.play("const", f"q{q2}_z", amp=cz_q2_amp)
    baker.play("const", f"q{c}_z", amp=cz_c_amp)

    # baker.play("cz", f"q{q1}_z")
    baker.align()
    baker.frame_rotation_2pi(qubit1_frame_update, f"q{q1}_xy")
    baker.frame_rotation_2pi(qubit2_frame_update, f"q{q2}_xy")
    baker.align()
    # baker.wait(20)



def prep():
    wait(int(200000/4))  # thermal preparation in clock cycles (time = 10 x T1 x 4ns)
    align()


def meas(
        # ro_elements
        ):
    threshold1 = threshold3  # threshold for state discrimination 0 <-> 1 using the I quadrature
    threshold2 = threshold4  # threshold for state discrimination 0 <-> 1 using the I quadrature
    I1 = declare(fixed)
    I2 = declare(fixed)
    Q1 = declare(fixed)
    Q2 = declare(fixed)
    state1 = declare(bool)
    state2 = declare(bool)
    # iqdata_stream = multiRO_declare( ro_elements )

    # multiRO_measurement( iqdata_stream, ro_elements, weights='rotated_'  )
    multiplexed_readout(
        [I1, I2], None, [Q1, Q2], None, resonators=[q3, q4], weights="rotated_"
    )  # readout macro for multiplexed readout
    assign(state1, I1 > threshold1)  # assume that all information is in I
    assign(state2, I2 > threshold2)  # assume that all information is in I
    return state1, state2


##############################
##  Two-qubit RB execution  ##
##############################
# qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name)  # initialize qmm
q3 = 0
threshold3 =  5.865e-05
qubit3_frame_update = -2.2437673593621548/(2*np.pi)

q4 = 1
threshold4 = -1.611e-04
qubit4_frame_update = (2.1733846058127413-0.1659717224962719-0.150026956784108)/(2*np.pi)

c = 3

cz_q4_amp = 0.056
cz_c_amp = 0.14

rb = TwoQubitRb(
    config=config,
    single_qubit_gate_generator=bake_phased_xz,
    two_qubit_gate_generators={"CZ": bake_cz},  # can also provide e.g. "CNOT": bake_cnot
    prep_func=prep,
    measure_func=meas,
    interleaving_gate=None,
    # interleaving_gate=[cirq.CZ(cirq.LineQubit(0), cirq.LineQubit(1))],
    verify_generation=False,
)

res = rb.run(qmm, circuit_depths=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], num_circuits_per_depth=10, num_shots_per_circuit=100)
# res = rb.run(qmm, circuit_depths=[0, 1, 2, 4, 8, 16, 32, 64, 128], num_circuits_per_depth=1000, num_shots_per_circuit=100)

# import xarray as xr
# dataset=xr.open_dataset(r"C:\Users\admin\SynologyDrive\09 Data\Fridge Data\Qubit\20240920_DRKe_5Q4C\raw_data\20240930_000305_2QRB\2QRB.nc")
# print(dataset)
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
    dp.save_nc(res.data,"2QRB")
    # rb.save_sequences_to_file(f"{dp.package
    # _root}/sequences.txt")  # saves the gates used in each random sequence
    # rb.save_command_mapping_to_file(f"{dp.package_root}/commands.txt")  # saves mapping from "command id" to sequence

save_fig = True
if save_fig: 
    hist = res.plot_hist()
    dp.save_fig(hist, "hist")
    fidelity_curve = res.plot_with_fidelity()
    dp.save_fig(fidelity_curve, "fidelity_curve")

if save_data: 
    # from exp.save_data import DataPackager
    # save_dir = link_config["path"]["output_root"]
    # dp = DataPackager( save_dir, folder_label )
    # dp.save_config(config)
    # dp.save_nc(res.data,"2QRB")
    rb.save_sequences_to_file(f"{dp.package_root}/sequences.txt")  # saves the gates used in each random sequence
    rb.save_command_mapping_to_file(f"{dp.package_root}/commands.txt")  # saves mapping from "command id" to sequence
plt.show()

# verify/save the random sequences created during the experiment
# rb.save_sequences_to_file("sequences.txt")  # saves the gates used in each random sequence
# rb.save_command_mapping_to_file("commands.txt")  # saves mapping from "command id" to sequence
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
