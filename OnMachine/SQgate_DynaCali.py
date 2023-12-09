
from QM_config_dynamic import QM_config, Circuit_info
from qm.QuantumMachinesManager import QuantumMachinesManager

from SQGate_calibration_dConfig import amp_calibration, DRAG_calibration_Yale, StarkShift_scout, StarkShift_program
from allxy_dConfig import AllXY_executor
from Ramsey_freq_calibration_dConfig import Ramsey_freq_calibration, plot_ana_result

from fitting_method import find_amp_minima, math_eqns, analysis_drag_a, find_AC_minima
from numpy import mean, ndarray, arange, array
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

def refresh_Q_StarkShift(target_q:str,specs:Circuit_info,config:QM_config,new_AC:float):
    specs.update_aXyInfo_for(target_q, AC=new_AC)
    config.update_controlWaveform(specs.get_spec_forConfig('xy'),target_q)
    return specs, config

def log_plot(amp_, IF_):
    plt.plot(amp_)
    plt.title('Amp log')
    plt.ylabel("Amplitude (V)")
    plt.show()
    plt.plot(IF_)
    plt.title('Freq log')
    plt.ylabel("detuning (MHz)")
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
        N_candidate = [5, 9]
    elif request == 'tough':
        N_candidate = [30]
    else:
        N_candidate = [60]

    iterations = 0
    max_iteration = 15
    aN_max_iter = 6


    # Workflow start
    while (precision_N_idx <= len(N_candidate)-1) and (iterations < max_iteration):
        print(f'iterations= {iterations}')
        sequence_repeat = N_candidate[precision_N_idx]
        amp_modify_range = 0.25/float(sequence_repeat)

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


def alpha_CaliFlow(drag_coef,q_name:str,ro_element:str,n_avg:int,spec:Circuit_info,config:QM_config,qm_machine:QuantumMachinesManager,init_macro:tuple=None):
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


def StarkShift_exp(q_name:str, ro_element:list, repeat_sequ_num:int, spec:Circuit_info, config:QM_config, qmm:QuantumMachinesManager, showFig:bool=False,simulate:bool=False, initializer:tuple=None):
    target_q = q_name.split("_")[0].lower()
    # Adjustable paras
    modi_span_range = 30/repeat_sequ_num # in MHz
    fit_point = 21
    # window built up
    df = 2*modi_span_range/fit_point
    old_ACdetuning = float(spec.get_spec_forConfig('xy')[target_q]['AC_stark_detuning'])*1e-6 #in MHz
    ACdetune_range = arange(old_ACdetuning-modi_span_range,old_ACdetuning+modi_span_range+df,df)

    def new_N_condition(ans,threshold=4):

        if old_ACdetuning-modi_span_range/(threshold/2)<ans and ans<old_ACdetuning+modi_span_range/(threshold/2):
            return True
        else:
            return False

    exp_circuit = StarkShift_program(q_name,ro_element,repeat_sequ_num,1000,initializer)
    I_rec = []

    for detu_MHz in ACdetune_range:
        # modify spec and config to exp
        spec, config = refresh_Q_StarkShift(target_q,spec,config,detu_MHz)
        # start exp
        measured_data = StarkShift_scout(exp_circuit,ro_element,config.get_config(),qmm)
        I_rec.append(measured_data[ro_element[0]][0])
    exp_array = array(I_rec)[:,0]
    ans_detu_MHz, popt = find_AC_minima(ACdetune_range,exp_array)
    if showFig:
        save=False
        plot_StarkExpResult(ACdetune_range,exp_array, popt, ans_detu_MHz, savefig=save, N=repeat_sequ_num)

    # recover the old settings 
    spec, config = refresh_Q_StarkShift(target_q,spec,config,old_ACdetuning)
    new_N_instruction = new_N_condition(ans_detu_MHz)
    return ans_detu_MHz, new_N_instruction

# plot ACstarkShift exp result
def plot_StarkExpResult(x:ndarray,exp_array:ndarray,popt:tuple,ans:float,savefig:bool=False,N:str=''):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(x,exp_array)
    ax.plot(x,math_eqns.cosine(x,*popt),label='fit')
    ax.scatter(ans,math_eqns.cosine(ans,*popt),label='Answer')
    ax.legend()
    ax.set_xlabel('Detuning (MHz)')
    ax.set_ylabel('Voltage (V)')
    ax.set_title(f"AC Stark shift exp result and analysis with N {N}")
    if savefig:
        plt.savefig(f'ACstark_N_{N}.png')
    plt.show()

def StarkShift_CaliFlow(q_name:str, ro_element:list, spec:Circuit_info, config:QM_config, qmm:QuantumMachinesManager, showFig:bool=False,simulate:bool=False, initializer:tuple=None):
    sequ_N_idx = 0
    repeat_N = [3, 6, 9]
    max_iter = 5
    aN_max_iter = 5

    while sequ_N_idx<len(repeat_N):
        print(f"================ Iteration_{6-max_iter} ==================")
        print(f"for N={repeat_N[sequ_N_idx]}:")
        print(f"Now drive with AC detuning={float(spec.get_spec_forConfig('xy')[target_q]['AC_stark_detuning'])*1e-6} MHz")
        detune_ans_MHz, new_N_instruction = StarkShift_exp(q_name,ro_element,repeat_N[sequ_N_idx],spec,config,qmm,showFig,initializer=initializer)
        print(f"New N or not: {new_N_instruction}")
        spec, config = refresh_Q_StarkShift(q_name.split("_")[0].lower(),spec,config,detune_ans_MHz)
        print(f"AC detuning had updated with {float(spec.get_spec_forConfig('xy')[target_q]['AC_stark_detuning'])*1e-6} MHz")
        if new_N_instruction or aN_max_iter <= 0:
            sequ_N_idx += 1
            max_iter = 5
            aN_max_iter = 5

        max_iter -= 1
        aN_max_iter -= 1
    
    return spec, config

def AutoCaliFlow(target_q:str,spec:Circuit_info,config:QM_config,qm_machine:QuantumMachinesManager,virtual_detune:float=2.0,init_macro:tuple=None):
        
    xyw = spec.get_spec_forConfig('xy')[target_q]['pi_len']
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
    # some helpful marks
    jump_out = False
    AC_cali = False
    converge_manager = False
    break_mark = True

    # work flows here
    while True:
        amp_rec.append(float(spec.get_spec_forConfig('xy')[target_q][f'pi_amp']))
        
        spec,config = amp_CaliFlow(target_q,spec,config,qm_machine,level,init_macro)
        
        amp_ans.append(float(spec.get_spec_forConfig('xy')[target_q][f'pi_amp']))

        if AC_cali:
            spec, config = StarkShift_CaliFlow(f"{target_q}_xy",[f"{target_q}_ro"],spec,config,qmm,showFig=False,initializer=init_macro)  
            converge_manager = True
        
        if jump_out:
            print("Jump out and amp is calibrated, move onto next step: alpha calibration!")
            new_spec, new_config = spec, config
            break

        n_avg = 600  # Number of averages
        output_data, evo_time = Ramsey_freq_calibration( virtual_detune, [f"{target_q}_xy"], [f"{target_q}_ro"],config.get_config(), qm_machine, n_avg=n_avg, simulate=False, mode='live', initializer=init_macro)
        ans = plot_ana_result(evo_time,output_data[f"{target_q}_ro"][0],virtual_detune)
        freq_rec.append(ans)
        spec,config = refresh_Q_IF(target_q,spec,config,ans)
        print(f"detune={-ans} MHz")

        # level for amp cali switch
        if abs(float(ans)) < 0.5: # 500 kHz
            level = 'medium'
        
        if abs(float(ans)) < 0.01: # 10 kHz
            level = 'tough'
            if float(xyw) <= 16: 
                AC_cali = True
            else:
                converge_manager = True
        
        if abs(float(ans)) < 0.001: # 1kHz
            jump_out = True


        detu_ans.append(ans)

        # Once the break condition had been satisfied, turn on break_mark, ready to break the loop 
        if break_optimize_condition(ans,detu_ans) and break_optimize_condition(float(spec.get_spec_forConfig('xy')[target_q][f'pi_amp']),amp_ans):
            break_mark = True
            level = 'final'

        if break_mark and converge_manager:
            print('Break conditions satisfied!')
            jump_out = True
            iter += 1
            
        if iter <= 0:
            print("Max Optimize iteration break!")
            new_spec, new_config = spec, config
            break

        iter -= 1
        
    # end_time = time.time()
    #print(f"Optimization completed! Time cost: {end_time-start_time}s")

    log_plot(amp_rec, freq_rec)
    old_drag_alpha = float(spec.get_spec_forConfig('xy')[target_q]["drag_coef"])
    # 
    final_spec, final_config = alpha_CaliFlow(old_drag_alpha,f"{target_q}_xy",f"{target_q}_ro",1000,new_spec,new_config,qm_machine,init_macro)
    
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


    max_circuit_depth = 700  # Maximum circuit depth
    delta_clifford = 10  #  Play each sequence with a depth step equals to 'delta_clifford - Must be > 1
    assert (max_circuit_depth / delta_clifford).is_integer(), "max_circuit_depth / delta_clifford must be an integer."
    seed = 345324  # Pseudo-random number generator seed
    # Flag to enable state discrimination if the readout has been calibrated (rotated blobs and threshold)
    state_discrimination = [1e-3]

    # load config file
    dyna_config = QM_config()
    dyna_config.import_config(path=r'/Users/ratiswu/Documents/GitHub/QM_opt/OnMachine/Config_Alloffset_1208')
    the_specs = Circuit_info(q_num=5)
    the_specs.import_spec(path=r'/Users/ratiswu/Documents/GitHub/QM_opt/OnMachine/Spec_Alloffset_1208')
    # # the_specs.update_aXyInfo_for(target_q,amp=the_specs.get_spec_forConfig('xy')[target_q]['pi_amp']*2)
    # # the_specs.update_aXyInfo_for(target_q,len=the_specs.get_spec_forConfig('xy')[target_q]['pi_len']/2)
    # # dyna_config.update_controlWaveform(the_specs.get_spec_forConfig('xy'),target_q)

    xyw = the_specs.get_spec_forConfig('xy')[target_q]['pi_len']
    print(f'pi_len = {xyw}')
    init_macro = initializer((the_specs.give_WaitTime_with_q(target_q,wait_scale=5),),'wait')
    allXY_ret = AllXY_executor(f"{target_q}_xy",f"{target_q}_ro",xyw,20000,dyna_config.get_config(),qmm,mode='live')
    # RB before Calibrations
    x, value_avg, error_avg = single_qubit_RB( xyw, max_circuit_depth, delta_clifford, f"{target_q}_xy", [f"{target_q}_ro"], dyna_config.get_config(), qmm, 10, 300, initialization_macro=init_macro )
    # plot
    plot_SQRB_result( x, value_avg, error_avg )
    # get gate infidelity only
    # _, gate_infidelity = ana_SQRB( x, value_avg )

    the_specs, dyna_config = AutoCaliFlow(target_q,the_specs,dyna_config,qmm,1.0,init_macro)
    
    the_specs.export_spec(path=r'/Users/ratiswu/Documents/GitHub/QM_opt/OnMachine/Spec_Calied_1209')
    dyna_config.export_config(path=r'/Users/ratiswu/Documents/GitHub/QM_opt/OnMachine/Config_Calied_1209')
    print(the_specs.get_ReadableSpec_fromQ(target_q,'xy'))
    
    ret = AllXY_executor(f"{target_q}_xy",f"{target_q}_ro",xyw,20000,dyna_config.get_config(),qmm,mode='live')
    # # RB after Calibrations
    x, value_avg, error_avg = single_qubit_RB( xyw, max_circuit_depth, delta_clifford, f"{target_q}_xy", [f"{target_q}_ro"], dyna_config.get_config(), qmm, 10, 300, initialization_macro=init_macro )
    # # plot
    plot_SQRB_result( x, value_avg, error_avg )