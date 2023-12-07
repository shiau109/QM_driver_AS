
from QM_config_dynamic import QM_config, Circuit_info
from qm.QuantumMachinesManager import QuantumMachinesManager

from SQGate_calibration_dConfig import amp_calibration, DRAG_calibration_Yale
from allxy_dConfig import AllXY_executor
from Ramsey_freq_calibration_dConfig import Ramsey_freq_calibration, plot_ana_result

from fitting_method import find_amp_minima, math_eqns, analysis_drag_a
from numpy import mean, ndarray, arange
import matplotlib.pyplot as plt

import time

# Update a new amp
def refresh_amp(target_q:str,specs:Circuit_info,config:QM_config,amp_modi_scale:float,mode:str='180'):
    if mode == '180':
        old_amp = float(specs.get_spec_forConfig('xy')[target_q][f'pi_amp'])
        specs.update_aXyInfo_for(target_q,amp=old_amp*amp_modi_scale)
        config.update_controlWaveform(specs.get_spec_forConfig('xy'),target_q)
    else:
        old_half_scale = float(specs.get_spec_forConfig('xy')[target_q]["pi_ampScale"]["90"] )
        specs.update_aXyInfo_for(target_q,half=amp_modi_scale*old_half_scale)
        config.update_controlWaveform(specs.get_spec_forConfig('xy'),target_q)

    return specs, config

def refresh_Q_IF(target_q:str,specs:Circuit_info,config:QM_config,IF_modi:float):
    '''
        IF_modi in MHZ
    '''
    old_if = float(specs.get_spec_forConfig('xy')[target_q]['qubit_IF'])*1e-6
    print(f"old IF: {old_if} MHz")
    config.update_controlFreq(specs.update_aXyInfo_for(target_q=target_q,IF=old_if-IF_modi))

    return specs, config

def refresh_Q_dragA(target_q:str,specs:Circuit_info,config:QM_config,new_alpha:float):
    """
        replace the old drag alpha for target_q with the given new_alpha.\n
        target_q: "q2"
    """
    specs.update_aXyInfo_for(target_q,draga=new_alpha)
    config.update_controlWaveform(specs.get_spec_forConfig('xy'),target_q)
    
    return specs, config

def log_plot(amp_, IF_):
    plt.plot(amp_)
    plt.title('Amp log')
    plt.show()
    plt.plot(IF_)
    plt.title('Freq log')
    plt.show()
    


def new_N_condition(x:ndarray,amp_scale:float,sweetspot:int=12):
    if amp_scale > 1-((x[-1]-x[0])/sweetspot)*0.5 and amp_scale < 1+((x[-1]-x[0])/sweetspot)*0.5:
        return True
    else:
        return False
    
def amp_cali_examine(target_q:str,config:QM_config,qm_machine:QuantumMachinesManager,init_macro:tuple=None):
    sequence_repeat = 30
    amp_modify_range = 0.25/float(sequence_repeat)
    results = amp_calibration(amp_modify_range, f"{target_q}_xy", [f"{target_q}_ro"], config.get_config(), qm_machine, n_avg=500, sequence_repeat=sequence_repeat, simulate=False, mode='wait', initilalizer=init_macro)
    x = results['x']
    y_90 = results[f"{target_q}_ro"][0].transpose()[0] 
    y_180 = results[f"{target_q}_ro"][0].transpose()[1]
    amp_scale_180,fit_paras_180 = find_amp_minima(x,y_180,'continuous')
    amp_scale_90,fit_paras_90 = find_amp_minima(x,y_90,'continuous')

    plt.plot(x,y_180,label='180')
    plt.plot(x,y_90,label='90')
    plt.plot(x, math_eqns.cosine(x,*fit_paras_180),label='fit')
    plt.plot(x, math_eqns.cosine(x,*fit_paras_90),label='fit')
    plt.scatter(amp_scale_180, math_eqns.cosine(amp_scale_180,*fit_paras_180),marker='X',s=80 ,label=f'180 ans={amp_scale_180}')
    plt.scatter(amp_scale_90, math_eqns.cosine(amp_scale_90,*fit_paras_90),s=80 ,label=f'90 ans={amp_scale_90}')
    plt.title(f"N={sequence_repeat}, Calibration Examination")
    plt.legend()
    plt.show() 




def amp_CaliFlow(target_q:str,spec:Circuit_info,config:QM_config,qm_machine:QuantumMachinesManager,request:str='basic',init_macro:tuple=None):
    '''
        operations: 180 for X180 operation, 90 for X90 operation.\n
        request: 'basic' for max(N) = 10, 'medium' for max(N) = 30, 'tough' for max(N) = 60
    '''
    # initialize
    precision_N_idx = 0
    if request == 'basic':
        N_candidate = [1, 3]
    elif request == 'medium':
        N_candidate = [3, 9]
    else:
        N_candidate = [30]

    iterations = 0
    max_iteration = 15
    aN_max_iter = 5


    # Workflow start
    while (precision_N_idx <= len(N_candidate)-1) and (iterations < max_iteration):
        print(f'iterations= {iterations}')
        sequence_repeat = N_candidate[precision_N_idx]
        amp_modify_range = 0.25/float(sequence_repeat)


        print("@@@@@@@@@Before Cali amp:")
        print(spec.get_spec_forConfig('xy')[target_q][f'pi_amp'])
        results = amp_calibration(amp_modify_range, f"{target_q}_xy", [f"{target_q}_ro"], config.get_config(), qm_machine, n_avg=500, sequence_repeat=sequence_repeat, simulate=False, mode='wait',initializer=init_macro)
        # fig, ax = plt.subplots(2, len(ro_element))
        x = results['x']
        # for r_idx, r_name in enumerate(ro_element):
        #     ax[r_idx*2].cla()
        #     ax[r_idx*2+1].cla()
        #     for op_idx, op in enumerate(["x90","x180"]):
        #         ax[r_idx*2].plot(x, results[r_name][0].transpose()[op_idx], label=op)
        #         ax[r_idx*2+1].plot(x, results[r_name][1].transpose()[op_idx], label=op)
        #     plt.show()
        
        
        y_90 = results[f"{target_q}_ro"][0].transpose()[0] 
        y_180 = results[f"{target_q}_ro"][0].transpose()[1]
        amp_scale_180,fit_paras_180 = find_amp_minima(x,y_180,'continuous')
        amp_scale_90,fit_paras_90 = find_amp_minima(x,y_90,'continuous')

        print(f"**** N={ sequence_repeat}, scale180={amp_scale_180:.5f}, scalse90={amp_scale_90:.5f} ****")
        
        # plot and check 
        # plt.plot(x,y_180,label='exp')
        # plt.plot(x,y_90,label='exp')
        # plt.plot(x, math_eqns.cosine(x,*fit_paras_180))
        # plt.plot(x, math_eqns.cosine(x,*fit_paras_90))
        # plt.scatter(amp_scale_180, math_eqns.cosine(amp_scale_180,*fit_paras_180),c='red',marker='X',s=80)
        # plt.scatter(amp_scale_90, math_eqns.cosine(amp_scale_90,*fit_paras_90),s=80)
        # plt.title(f'N={sequence_repeat}')
        # plt.legend()
        # plt.show()

        
        print("@@@@@After Cali amp:")
        print(spec.get_spec_forConfig('xy')[target_q][f'pi_amp'])
        
        iterations += 1
        aN_max_iter -= 1
        print("Update complete!")

        if new_N_condition(x,amp_scale_180,2.5):
            if new_N_condition(x,amp_scale_90,2.5):
                precision_N_idx += 1
                aN_max_iter = 5
        
        
        if aN_max_iter <= 0:
            print("single N max iteration break!")
            precision_N_idx += 1
        
        # Update amp
        spec,config = refresh_amp(target_q,spec,config,amp_scale_180,'180')
        spec,config = refresh_amp(target_q,spec,config,amp_scale_90/amp_scale_180,'90')

        
    
    # plot and check 
    # print("Exam:")
    # amp_cali_examine(target_q,config,qm_machine,init_macro)
    
    return spec, config


def break_optimize_condition(new_ans, ans_rec_list, threshold=1):
    if len(ans_rec_list)<= 3:
        return False
    else:
        counted = ans_rec_list[-3:]
        # old_dif = abs(counted[0]-counted[-1])
        # new_dif = abs(new_ans-counted[-1])
        from numpy import std, array
        up_limit = sum(counted)/3+threshold*abs(std(array(counted)))
        buttom_limit = sum(counted)/3-threshold*abs(std(array(counted)))
        if new_ans >= buttom_limit and new_ans <= up_limit:
            return True
        else:
            return False
        # if new_dif < threshold*old_dif:
        #     return True
        # else:
        #     return False


def alpha_calibrate(drag_coef,q_name:str,ro_element:str,n_avg:int,spec:Circuit_info,config:QM_config,qm_machine:QuantumMachinesManager,init_macro:tuple=None):
    output_data = DRAG_calibration_Yale( drag_coef, q_name, [ro_element], config.get_config(), qm_machine, n_avg=n_avg,mode='wait',initializer=init_macro)
    x = output_data['x']
    y1 = output_data[ro_element][0].transpose()[0]
    y2 = output_data[ro_element][0].transpose()[1]
    new_alpha, warnings = analysis_drag_a(x,y1,y2)

    # update alpha and config
    new_spec, new_config = refresh_Q_dragA(target_q,spec,config,float(new_alpha))
    if warnings != 'pass':
        print("In Alpha-Calibration, the crosspoint didn't show up in the given window!")

    return new_spec, new_config

      

def AutoCaliFlow(target_q:str,spec:Circuit_info,config:QM_config,qm_machine:QuantumMachinesManager,virtual_detune:float=2.0,init_macro:tuple=None):
        
    # xyw = spec.get_spec_forConfig('xy')[target_q]['pi_len']
    # ret = AllXY_executor(q_name,ro_element[0],xyw,dyna_config.get_config(),qmm,mode='wait')

    # start_time = time.time()
    level = 'basic'
    # optimize log
    amp_rec = []
    freq_rec = []
    # break condition scouter
    detu_ans = []
    amp_ans = []
    # maximum iterations
    iter = 6

    while True:
        amp_rec.append(float(spec.get_spec_forConfig('xy')[target_q][f'pi_amp']))
        
        spec,config = amp_CaliFlow(target_q,spec,config,qm_machine,level,init_macro)
        # allXY_ret = AllXY_executor(q_name,ro_element[0],xyw,10000,dyna_config.get_config(),qmm,mode='wait')
        amp_ans.append(float(spec.get_spec_forConfig('xy')[target_q][f'pi_amp']))

        n_avg = 600  # Number of averages
        
        output_data, evo_time = Ramsey_freq_calibration( virtual_detune, [f"{target_q}_xy"], [f"{target_q}_ro"],config.get_config(), qm_machine, n_avg=n_avg, simulate=False, mode='live', initializer=init_macro)
        ans = plot_ana_result(evo_time,output_data[f"{target_q}_ro"][0],virtual_detune)
        freq_rec.append(ans)
        spec,config = refresh_Q_IF(target_q,spec,config,ans)
        print(f"detune={-ans} MHz")
        if abs(float(ans)) < 0.5: # 500 kHz
            level = 'medium'
            
        
        if abs(float(ans)) < 0.01: # 10 kHz
            level = 'tough'


        detu_ans.append(ans)

        if break_optimize_condition(ans,detu_ans) and break_optimize_condition(float(spec.get_spec_forConfig('xy')[target_q][f'pi_amp']),amp_ans):
            print('Break conditions satisfied!')
            new_spec, new_config = spec, config
            break
        if iter <= 0:
            new_spec, new_config = spec, config
            break

        iter -= 1
        
    # end_time = time.time()
    #print(f"Optimization completed! Time cost: {end_time-start_time}s")

    log_plot(amp_rec, freq_rec)
    old_drag_alpha = float(spec.get_spec_forConfig('xy')[target_q]["drag_coef"])
    final_spec, final_config = alpha_calibrate(old_drag_alpha,f"{target_q}_xy",f"{target_q}_ro",1000,new_spec,new_config,qm_machine,init_macro)
        
    
    return final_spec, final_config
        

if __name__ == '__main__':
    from set_octave import OctaveUnit, octave_declaration
    from SQRB_dConfig import single_qubit_RB, plot_SQRB_result, ana_SQRB
    from QM_config_dynamic import QM_config, Circuit_info, initializer
    qop_ip = '192.168.1.105'
    qop_port = None
    cluster_name = 'QPX_2'
    target_q = 'q1'
    

    port_mapping = {
        ("con1", 1): ("octave1", "I1"),
        ("con1", 2): ("octave1", "Q1"),
        ("con1", 3): ("octave1", "I2"),
        ("con1", 4): ("octave1", "Q2"),
        ("con1", 5): ("octave1", "I3"),
        ("con1", 6): ("octave1", "Q3"),
        ("con1", 7): ("octave1", "I4"),
        ("con1", 8): ("octave1", "Q4"),
        ("con1", 9): ("octave1", "I5"),
        ("con1", 10): ("octave1", "Q5"),
    }

    octave_1 = OctaveUnit("octave1", qop_ip, port=11250, con="con1", clock="Internal", port_mapping=port_mapping)
    # Add the octaves
    octaves = [octave_1]
    # Configure the Octaves
    octave_config = octave_declaration(octaves)

    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)


    max_circuit_depth = 500  # Maximum circuit depth
    delta_clifford = 10  #  Play each sequence with a depth step equals to 'delta_clifford - Must be > 1
    assert (max_circuit_depth / delta_clifford).is_integer(), "max_circuit_depth / delta_clifford must be an integer."
    seed = 345324  # Pseudo-random number generator seed
    # Flag to enable state discrimination if the readout has been calibrated (rotated blobs and threshold)
    state_discrimination = [1e-3]

    # load config file
    dyna_config = QM_config()
    
    dyna_config.import_config(path=r'/Users/ratiswu/Documents/GitHub/QM_opt/OnMachineTest/Config_Alloffset_1207')
    the_specs = Circuit_info(q_num=5)
    the_specs.import_spec(path=r'/Users/ratiswu/Documents/GitHub/QM_opt/OnMachineTest/Spec_Alloffset_1207')
    xyw = the_specs.get_spec_forConfig('xy')[target_q]['pi_len']
    init_macro = initializer((the_specs.give_WaitTime_with_q(target_q,wait_scale=5),),'wait')

    # RB before Calibrations
    x, value_avg, error_avg = single_qubit_RB( xyw, max_circuit_depth, delta_clifford, f"{target_q}_xy", [f"{target_q}_ro"], dyna_config.get_config(), qmm, 10, 300, initialization_macro=init_macro )
    # plot
    plot_SQRB_result( x, value_avg, error_avg )
    # get gate infidelity only
    # _, gate_infidelity = ana_SQRB( x, value_avg )

    the_specs, dyna_config = AutoCaliFlow(target_q,the_specs,dyna_config,qmm,1.0,init_macro)
    
    the_specs.export_spec(path=r'/Users/ratiswu/Documents/GitHub/QM_opt/OnMachineTest/Spec_1207_Calied')
    dyna_config.export_config(path=r'/Users/ratiswu/Documents/GitHub/QM_opt/OnMachineTest/Config_1207_Calied')
    print(the_specs.get_ReadableSpec_fromQ(target_q,'xy'))
    
    # ret = AllXY_executor(f"{target_q}_xy",f"{target_q}_ro",xyw,10000,dyna_config.get_config(),qmm,mode='live')
    # # RB before Calibrations
    x, value_avg, error_avg = single_qubit_RB( xyw, max_circuit_depth, delta_clifford, f"{target_q}_xy", [f"{target_q}_ro"], dyna_config.get_config(), qmm, 10, 300, initialization_macro=init_macro )
    # # plot
    plot_SQRB_result( x, value_avg, error_avg )

