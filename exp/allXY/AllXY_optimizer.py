from sympy import symbols, Matrix, N, refine, Q, expand, simplify, series,re, collect, nsimplify, solve
from sympy.physics.quantum.dagger import Dagger
from sympy.matrices.expressions import Trace
import matplotlib.pyplot as plt
from numpy import array, sqrt, matrix, pi, absolute
from numpy.random import randint as R

from allXY_tool import get_costfuncs, AllXY_nextstep_teller, result_arranger
from AutoAllxy_QM import AllXY_real
from qm.QuantumMachinesManager import QuantumMachinesManager
from set_octave import OctaveUnit, octave_declaration



################################
#    Dynamic configurations    #
################################
from QM_config_dynamic import QM_config, Circuit_info
dyna_config = QM_config()       
spec_recorder = Circuit_info(q_num=4)


spec_recorder.import_spec("Quantum-Control-Applications\Superconducting\Two-Flux-Tunable-Transmons\spec_v1115")
dyna_config.import_config("Quantum-Control-Applications\Superconducting\Two-Flux-Tunable-Transmons\config_v1115")
print(dyna_config.get_config()['waveforms']["const_wf"])
print(spec_recorder.XyInfo['const_amp'])
def update_Qinfo(target,amp_modi_ratio,detune_modi):
    new_amp = spec_recorder.XyInfo[f"pi_amp_{target}"] + spec_recorder.XyInfo[f"pi_amp_{target}"]*amp_modi_ratio
    new_freq = spec_recorder.XyInfo[f"qubit_IF_{target}"]*1e-6 + detune_modi
    spec_recorder.update_aXyInfo_for(target_q=target,amp=new_amp)
    dyna_config.update_controlWaveform(spec_recorder.XyInfo)
    dyna_config.update_controlFreq(spec_recorder.update_aXyInfo_for(target_q=target,IF=new_freq))

    return new_amp

#################################
# pre-defined target variables  #
#################################
target_q = "q4"  # The qubit under study, ""q2_xy
target_res = "q4_ro"  # The resonator to measure the qubit defined above
read_from_signal = 'I' # Read I signal
iteration_threshold = 10
tg = spec_recorder.XyInfo[f'pi_len_{target_q}']

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
print(f"q1 XYL={spec_recorder.XyInfo[f'pi_amp_{target_q}']}")
print(f"q1 xyIF = {spec_recorder.XyInfo[f'qubit_IF_{target_q}']}")
answer = AllXY_real(qb=f"{target_q}_xy",res=target_res,pi_len=tg,signal_target=read_from_signal,configuration=dyna_config.get_config(),qm_mache=qmm,mode='live')
answer = result_arranger(answer)
print(f"ans = {answer}. Start calculating the error...")
amp_modi_ratio, detune_modi = AllXY_nextstep_teller(answer,cost_expres)
print(f"to modified: amp={amp_modi_ratio}, detune={detune_modi}MHz") # 1e12 got by on-machine test
# update the config about amp and detune
'''To check'''
print(f"Start updating parameters...")
new_amp = update_Qinfo(target_q,amp_modi_ratio,detune_modi)
print(f"Update complete!")
# flow records
exp_record = {'0':answer}
amp_error_record = [amp_modi_ratio]
detune_error_record = [detune_modi]

# # optimization flow
# itera = 0
# while abs(amp_modi_ratio) > 1e-3 and abs(detune_modi)*1e3 > 20 : # amp_ratio_error < 0.01 AND detune_error < 20KHz break
#     print(f"iteration= {itera+1}...")
#     if abs(new_amp) < 0.25 and abs(detune_modi) < 50:  # safety guard
#         print("Safty guard pass!")
#         itera += 1
#         # after updating run a new exp 
#         answer = AllXY_real(qb=f"{target_q}_xy",res=target_res,pi_len=tg,signal_target=read_from_signal,configuration=dyna_config.get_config(),qm_mache=qmm)
#         answer = result_arranger(answer)
#         amp_modi_ratio, detune_modi = AllXY_nextstep_teller(answer,cost_expres)
#         amp_error_record.append(amp_modi_ratio)
#         detune_error_record.append(detune_modi)
#         exp_record[str(itera)] = answer
#     else:
#         print("Optimized values break safety boundaries!")
#         itera += 1
#         break
#     # update the config about amp and detune
#     '''To check'''
#     new_amp = update_Qinfo(target_q,amp_modi_ratio,detune_modi)
#     # Iterations counts and conditional break
#     if itera == iteration_threshold+1:
#         print(f"Max Iterations={iteration_threshold} completed!")
#         break
    

# get the optimized answer from terminal
print(f"\nAfter optimization, XYL={spec_recorder.XyInfo[f'pi_amp_{target_q}']}")
print(f"After optimization, Qubit_IF={spec_recorder.XyInfo[f'qubit_IF_{target_q}']} MHz\n")
# spec_recorder.export_spec("optied_spec")
# dyna_config.export_config("optied_config")

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



