from sympy import symbols, Matrix, N, refine, Q, expand, simplify, series,re, collect, nsimplify, solve
from sympy.physics.quantum.dagger import Dagger
from sympy.matrices.expressions import Trace
import matplotlib.pyplot as plt
from numpy import array, sqrt, matrix, pi, absolute
from numpy.random import randint as R

from allXY_tool import get_costfuncs, AllXY_nextstep_teller, result_arranger
from AutoAllxy_QM import AllXY_real
import configuration_with_octave as config_octave
from configuration_with_octave import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from set_octave import OctaveUnit, octave_declaration



################################
#    Dynamic configurations    #
################################
from QM_config_dynamic import QM_config, Circuit_info
dyna_config = QM_config()       
spec_recorder = Circuit_info(q_num=4)
spec_recorder.import_spec("exp/allXY/spec_v1113")
dyna_config.import_config("exp/allXY/config_v1113")

#################################
# pre-defined target variables  #
#################################
target_q = "q1_xy"  # The qubit under study, ""q2_xy
target_res = "rr1"  # The resonator to measure the qubit defined above
read_from_signal = 'I' # Read I signal
iteration_threshold = 10
tg = spec_recorder.spec['XyInfo']['pi_len_q1']
q_no = target_q.split("_")[0][-1]
######################
# Network parameters #
######################
qop_ip = "192.168.50.126"  # Write the QM router IP address
cluster_name = "QPX_4"  # Write your cluster_name if version >= QOP220
qop_port = None  # Write the QOP port if version < QOP220
octave_1 = OctaveUnit("octave1", qop_ip, port=11250, con="con1", clock="Internal", port_mapping="default")
# octave_2 = OctaveUnit("octave2", qop_ip, port=11051, con="con1", clock="Internal", port_mapping=port_mapping)
# Add the octaves
octaves = [octave_1]
# Configure the Octaves
octave_config = octave_declaration(octaves)
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

#========== Works start here ========================================#

# get the cost function fbased on the gate time given
print(f"calculating the cost func for tg={tg}...")
cost_expres, theoretical_allXY = get_costfuncs(tg)
print(f"calculation complete!")
# initailize the allXY experiment with manually measured papmeters
print(f"q1 XYL={config_octave.pi_amp_q1}")
print(f"q1 xyIF = {config_octave.qubit_IF_q1}")
answer = AllXY_real(qb=target_q,res=target_res,signal_target=read_from_signal,configration=dyna_config,qm_mache=qmm)
answer = result_arranger(answer)
print(f"ans = {answer}. Start calculating the error...")
amp_modi_ratio, detune_modi = AllXY_nextstep_teller(answer,cost_expres)
print(f"to modified: amp={amp_modi_ratio}, detune={detune_modi}MHz") # 1e12 got by on-machine test
# update the config about amp and detune
'''To check'''
print(f"Start updating parameters...")
update_Qinfo(q_no,amp_modi_ratio,detune_modi*1e6)
print(f"Update complete!")
# flow records
exp_record = {'0':answer}
amp_error_record = [amp_modi_ratio]
detune_error_record = [detune_modi]

# optimization flow
itera = 0
while abs(amp_modi_ratio) > 1e-3 and abs(detune_modi)*1e3 > 20 : # amp_ratio_error < 0.01 AND detune_error < 20KHz break
    print(f"iteration= {itera+1}...")
    if abs(amp_modi_ratio) < 0.5 and abs(detune_modi) < 50:  # safety guard
        print("Safty guard pass!")
        itera += 1
        # after updating run a new exp 
        answer = AllXY_real(qb=target_q,res=target_res,signal_target=read_from_signal)
        answer = result_arranger(answer)
        amp_modi_ratio, detune_modi = AllXY_nextstep_teller(answer,cost_expres)
        amp_error_record.append(amp_modi_ratio)
        detune_error_record.append(detune_modi)
        exp_record[str(itera)] = answer
    else:
        print("Optimized values break safety boundaries!")
        itera += 1
        break
    # update the config about amp and detune
    '''To check'''
    update_Qinfo(q_no,amp_modi_ratio,detune_modi)
    # Iterations counts and conditional break
    if itera == iteration_threshold+1:
        print(f"Max Iterations={iteration_threshold} completed!")
        break
    

# get the optimized answer from terminal
print(f"\nAfter optimization, XYL={config_octave.pi_amp_q1}")
print(f"After optimization, Qubit_IF={config_octave.qubit_IF_q1} MHz\n")

# plot out the details in optimization iterations
plt.figure(figsize=(18, 27))
ax1 = plt.subplot(221)
ax1.grid()
ax1.plot(list(exp_record.keys()),amp_error_record,c='orange')
ax1.set_xlabel("Iterations")
ax1.set_ylabel("Amplitude error (ratio)")
ax1.title.set_text("Amplitude error Optimization")

ax2 = plt.subplot(222)
ax2.grid()
ax2.plot(list(exp_record.keys()),array(detune_error_record),c='green')
ax2.set_xlabel("Iterations")
ax2.set_ylabel("Detune error (MHz)")
ax2.title.set_text("Detuning error Optimization")

ax3 = plt.subplot(212)
ax3.grid()
ax3.plot(list(exp_record["0"].keys()),list(exp_record["0"].values()),label="Un-Optimized",c='orange')
ax3.plot(list(theoretical_allXY.keys()),list(theoretical_allXY.values()),label="Theoretical",c='red',marker="X")
ax3.plot(list(exp_record[str(itera)].keys()),list(exp_record[str(itera)].values()),label=f"Optimized_iter={str(itera)}",c='blue')
ax3.legend()
ax3.title.set_text(f"AllXY Optimization comparisons")
plt.show()



