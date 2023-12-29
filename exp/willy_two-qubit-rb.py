from qutip import sigmax, sigmay, sigmaz, basis, qeye, tensor, Qobj
from qutip_qip.operations import Gate #Measurement in 0.3.X qutip_qip
from qutip_qip.circuit import QubitCircuit
from qutip_qip.compiler import GateCompiler, Instruction
import numpy as np
from pandas import DataFrame
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
from TQRB.util import run_in_thread, pbar
from TQRB.RBResult import RBResult
from qualang_tools.bakery import baking
from TQRB.TQClifford import m_random_Clifford_circuit, get_TQcircuit_random_clifford
from TQRB.TQCompiler import *
import warnings

mycompiler = TQCompile( 2, q1_frame_update=0, q2_frame_update=0, params={} )
circuit = QubitCircuit(2)
circuit_depths = [0,1,2,3]
circuit_repeats = 3
n_avg = 2000
circuit = [[[] for _ in range(circuit_repeats)] for _ in range(len(circuit_depths))]
for i in circuit_depths:
    for j in range(circuit_repeats):
        circuit[i][j] = get_TQcircuit_random_clifford(control=2, target=3, num_gates=i, mode='MR') 

with program() as prog:
    n = declare(int)
    n_st = declare_stream()  
    state = declare(int)
    state_os = declare_stream()
    for i in circuit_depths:
        for j in range(circuit_repeats):
            with for_(n, 0, n < n_avg, n + 1):   
                wait(thermalization_time)
                compiled_data = mycompiler.compile(circuit[i][j],schedule_mode='ASAP')
                align()
                out1, out2 = meas()

                assign(state, (Cast.to_int(out2) << 1) + Cast.to_int(out1))
                save(state, state_os)
                save(n, n_st)
    with stream_processing():
        n_st.save("n")
        state_os.buffer(len(circuit_depths), circuit_repeats, n_avg).save("state")

simulate = False
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config) 
if simulate:
    simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
    job = qmm.simulate(config, prog, simulation_config)
    job.get_simulated_samples().con1.plot()
    plt.show()
else:
    qm = qmm.open_qm(config)
    job = qm.execute(prog)
    full_progress = len(circuit_depths)
    job.result_handles.wait_for_all_values()
    rbresult = RBResult(
        circuit_depths=circuit_depths,
        num_repeats=circuit_repeats,
        num_averages=n_avg,
        state=job.result_handles.get("state").fetch_all(),
    )
    rbresult.plot_hist()
    plt.show()

    rbresult.plot_fidelity()
    plt.show()