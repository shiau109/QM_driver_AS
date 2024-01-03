from qutip_qip.operations import Gate #Measurement in 0.3.X qutip_qip
from qutip_qip.circuit import QubitCircuit
import numpy as np
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *
import matplotlib.pyplot as plt
import numpy as np
from TQRB.RBResult import RBResult
from TQRB.TQClifford import m_random_Clifford_circuit, get_TQcircuit_random_clifford
from TQCompiler import *
from macros import multiplexed_readout
import warnings

def meas():
    threshold1 = 9.172e-05 # threshold for state discrimination 0 <-> 1 using the I quadrature
    threshold2 = -3.678e-04  # threshold for state discrimination 0 <-> 1 using the I quadrature
    I1 = declare(fixed)
    I2 = declare(fixed)
    Q1 = declare(fixed)
    Q2 = declare(fixed)
    state1 = declare(bool)
    state2 = declare(bool)
    multiplexed_readout(
        [I1, I2], None, [Q1, Q2], None, resonators=[2, 3], weights="rotated_"
    )  # readout macro for multiplexed readout
    assign(state1, I1 > threshold1)  # assume that all information is in I
    assign(state2, I2 > threshold2)  # assume that all information is in I
    return state1, state2
# -258.128 / 360
# -18.345 / 360
mycompiler = TQCompile( 2, q1_frame_update= -15/360, q2_frame_update= 0, params={} )
### TEST GATE
# q2_x180 = Gate("RX", 2, arg_value=np.pi)
# q3_x180 = Gate("RX", 3, arg_value=np.pi)
# q2_x90 = Gate("RX", 2, arg_value=np.pi/2)
# q3_x90 = Gate("RX", 3, arg_value=np.pi/2)
# q2_y180 = Gate("RY", 2, arg_value=np.pi)
# q2_y90 = Gate("RY", 2, arg_value=np.pi/2)
# idle_gate = Gate("IDLE", 2)
# ### Crucially Important!! The controls of CZ gate is the first element, which we apply flux. That is the higher freq. one.
# cz = Gate("CZ", controls=2, targets=3)
# gate_seq = [
#     q3_x180,q2_y90,q2_x180,cz,q2_y90,q2_x180
# ]
# circuit = QubitCircuit(2)
# for gate in gate_seq:
#     circuit.add_gate(gate)
# circuit_depths = [0]
# circuit_repeats = 1
# n_avg = 2000

### TEST TQRB
circuit_depths = [0,1,2,3]
circuit_repeats = 1
n_avg = 2000
circuit = [[[] for _ in range(circuit_repeats)] for _ in range(len(circuit_depths))]
for i in circuit_depths:
    for j in tqdm(range(circuit_repeats), desc="Processing", unit="step"):
        circuit[i][j] = get_TQcircuit_random_clifford(control=2, target=3, num_gates=i, mode='ONE') 
print('Entering QUA program')

with program() as prog:
    n = declare(int)
    n_st = declare_stream()  
    state = declare(int)
    state_os = declare_stream()

    ####  TEST GATE
    # with for_(n, 0, n < n_avg, n + 1):  
    #     wait(thermalization_time)
    #     compiled_data = mycompiler.compile(circuit,schedule_mode='ASAP')
    #     align()
    #     wait(flux_settle_time * u.ns)
    #     out1, out2 = meas()
    #     assign(state, (Cast.to_int(out2) << 1) + Cast.to_int(out1))
    #     save(state, state_os)
    #     save(n, n_st)

    ####  TEST TQRB
    for i in circuit_depths:
        for j in tqdm(range(circuit_repeats), desc="Processing", unit="step"):
            with for_(n, 0, n < n_avg, n + 1):   
                wait(thermalization_time)
                compiled_data = mycompiler.compile(circuit[i][j],schedule_mode='ASAP')
                align()
                wait(flux_settle_time * u.ns)
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
    print("!"*20)
    print(type(job.result_handles.get("state").fetch_all()))
    print("!"*20)
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