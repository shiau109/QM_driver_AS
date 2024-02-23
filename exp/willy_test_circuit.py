from qutip_qip.circuit import QubitCircuit
import numpy as np
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *
import matplotlib.pyplot as plt
import numpy as np
from TQRB.CircuitResult import CircuitResult
from TQCompiler import *
import warnings

gate_seq = []
for i in range(1500):
    gate_seq.append(q3_x180)    
    gate_seq.append(q2_x180)


# cnot:q2_y90,q2_x180,cz,q2_y90,q2_x180
# gate_seq = [
#     q2_y90,q2_x180,cz,q2_y90,q2_x180
#     # q2_x180,q3_x180
# ]
circuit = QubitCircuit(2)
for gate in gate_seq:
    circuit.add_gate(gate)
n_avg = 2000

mycompiler = TQCompile( 2, q1_frame_update= 0.36, q2_frame_update= 0.84, params={}, cz_type='square' )
with program() as prog:
    n = declare(int)
    n_st = declare_stream()  
    state = declare(int)
    state_os = declare_stream()
    I1_st = declare_stream()
    I2_st = declare_stream()
    Q1_st = declare_stream()
    Q2_st = declare_stream()

    ####  TEST GATE
    with for_(n, 0, n < n_avg, n + 1):  
        wait(thermalization_time)
        compiled_data = mycompiler.compile(circuit,schedule_mode='ASAP')
        align()
        wait(flux_settle_time * u.ns)
        out1, out2, I1_st, I2_st, Q1_st, Q2_st = meas()
        assign(state, (Cast.to_int(out2) << 1) + Cast.to_int(out1))
        save(state, state_os)
        save(n, n_st)
    with stream_processing():
        n_st.save("n")
        state_os.buffer(n_avg).save("state") 
        I1_st.buffer(n_avg).save("I1")
        I2_st.buffer(n_avg).save("I2")
        Q1_st.buffer(n_avg).save("Q1")
        Q2_st.buffer(n_avg).save("Q2")

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
    job.result_handles.wait_for_all_values()
    circuitresult = CircuitResult(
        num_averages=n_avg,
        state=job.result_handles.get("state").fetch_all(),
        I1=job.result_handles.get("I1").fetch_all(),
        I2=job.result_handles.get("I2").fetch_all(),
        Q1=job.result_handles.get("Q1").fetch_all(),
        Q2=job.result_handles.get("Q2").fetch_all(),
    ) 
    circuitresult.plot_hist()
    plt.show()
hist_value = circuitresult.data.state.values
print('state 00: ',len(hist_value[hist_value==0])/n_avg)
print('state 10: ',len(hist_value[hist_value==1])/n_avg)
print('state 01: ',len(hist_value[hist_value==2])/n_avg)
print('state 11: ',len(hist_value[hist_value==3])/n_avg)

import xarray as xr
ds = xr.Dataset()
ds['state'] = circuitresult.data.state
ds['I1'] = circuitresult.data.I1
ds['I2'] = circuitresult.data.I2
ds['Q1'] = circuitresult.data.Q1
ds['Q2'] = circuitresult.data.Q2
print('I1:', ds.I1.sum(("average")).values / (n_avg))
print('Q1:', ds.Q1.sum(("average")).values / (n_avg))
print('I2:', ds.I2.sum(("average")).values / (n_avg))
print('Q2:', ds.Q2.sum(("average")).values / (n_avg))
ds.to_netcdf("test_circuit.nc")
# original_ds = xr.open_dataset("test_circuit.nc")
# updated_ds = xr.concat([original_ds, ds],dim="average")
# original_ds.close()
# updated_ds.to_netcdf("test_circuit.nc", mode='w')