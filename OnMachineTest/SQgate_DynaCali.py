# import sys
# sys.path.append('./exp')
# sys.path.append('./analysis')
from QM_config_dynamic import QM_config, Circuit_info, initializer
from qm.QuantumMachinesManager import QuantumMachinesManager

from SQGate_calibration_dConfig import amp_calibration
from allxy_dConfig import AllXY_executor
from Ramsey_freq_calibration_dConfig import Ramsey_freq_calibration, plot_ana_result

from fitting_method import find_amp_minima, math_eqns
from numpy import mean, ndarray, arange
import matplotlib.pyplot as plt
from set_octave import OctaveUnit, octave_declaration
import time

# thermalization by 5*T1
 



# Update a new amp
def refresh_amp(target_q:str,specs:Circuit_info,config:QM_config,amp_modi_scale:float,mode:str='180'):
    if mode == '180':
        old_amp = float(specs.get_spec_forConfig('xy')[target_q][f'pi_amp'])
        specs.update_aXyInfo_for(target_q,amp=old_amp*amp_modi_scale)
        config.update_controlWaveform(specs.get_spec_forConfig('xy'),target_q)
    else:
        old_half_scale = float(specs.get_spec_forConfig('xy')[target_q]["half_pi_ampScale"]["90"] )
        specs.update_aXyInfo_for(target_q,half=amp_modi_scale*old_half_scale)
        config.update_controlWaveform(specs.get_spec_forConfig('xy'),target_q)

    return specs, config

def refresh_Q_IF(target_q:str,specs:Circuit_info,config:QM_config,IF_modi:float):
    '''
        IF_modi in MHZ
    '''
    old_if = specs.get_spec_forConfig('xy')[target_q]['qubit_IF']*1e-6
    print(f"old IF: {old_if} MHz")
    config.update_controlFreq(specs.update_aXyInfo_for(target_q=target_q,IF=old_if+IF_modi))

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
    
def amp_cali_examine(config:QM_config,qm_machine:QuantumMachinesManager, init_macro:tuple):
    sequence_repeat = 30
    amp_modify_range = 0.25/float(sequence_repeat)
    results = amp_calibration(amp_modify_range, q_name, ro_element, config.get_config(), qm_machine, n_avg=500, sequence_repeat=sequence_repeat, simulate=False, mode='wait', init_macro)
    x = results['x']
    y_90 = results[ro_element[0]][0].transpose()[0] 
    y_180 = results[ro_element[0]][0].transpose()[1]
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




def amp_CaliFlow(target_q:str, spec:Circuit_info, config:QM_config, qm_machine:QuantumMachinesManager, request:str='basic', init_macro:tuple=None):
    '''
        operations: 180 for X180 operation, 90 for X90 operation.\n
        request: 'basic' for max(N) = 10, 'medium' for max(N) = 30, 'tough' for max(N) = 60
    '''
    # initialize
    precision_N_idx = 0
    if request == 'basic':
        N_candidate = [1, 9]
    elif request == 'medium':
        N_candidate = [18, 30]
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
        results = amp_calibration(amp_modify_range, q_name, ro_element, config.get_config(), qm_machine, 500, sequence_repeat, False, 'wait', init_macro)
        # fig, ax = plt.subplots(2, len(ro_element))
        x = results['x']
        # for r_idx, r_name in enumerate(ro_element):
        #     ax[r_idx*2].cla()
        #     ax[r_idx*2+1].cla()
        #     for op_idx, op in enumerate(["x90","x180"]):
        #         ax[r_idx*2].plot(x, results[r_name][0].transpose()[op_idx], label=op)
        #         ax[r_idx*2+1].plot(x, results[r_name][1].transpose()[op_idx], label=op)
        #     plt.show()
        
        
        y_90 = results[ro_element[0]][0].transpose()[0] 
        y_180 = results[ro_element[0]][0].transpose()[1]
        amp_scale_180,fit_paras_180 = find_amp_minima(x,y_180,'continuous')
        amp_scale_90,fit_paras_90 = find_amp_minima(x,y_90,'continuous')

        print(f"**** N={ sequence_repeat}, scale180={amp_scale_180}, scalse90={amp_scale_90} ****")
        
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

        # Update amp
        spec,config = refresh_amp(target_q,spec,config,amp_scale_180,'180')
        spec,config = refresh_amp(target_q,spec,config,amp_scale_90/amp_scale_180,'90')

        print("**************After Cali amp:")
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
        
    
    # plot and check 
    print("Exam:")
    amp_cali_examine(config,qm_machine,init_macro)
    
    return spec, config


def break_optimize_condition(new_ans, ans_rec_list, threshold=0.05):
    if len(ans_rec_list)<= 2:
        return False
    else:
        counted = ans_rec_list[-2:]
        old_dif = abs(counted[0]-counted[-1])
        new_dif = abs(new_ans-counted[-1])
        # from numpy import std, array
        # up_limit = sum(counted)/3+threshold*std(array(counted))
        # buttom_limit = sum(counted)/3-threshold*std(array(counted))
        # if new_ans >= buttom_limit and new_ans <= up_limit:
        #     return True
        # else:
        #     return False
        if new_dif < threshold*old_dif:
            return True
        else:
            return False
        

def AutoCaliFlow(target_q:str,spec:Circuit_info,config:QM_config,qm_machine:QuantumMachinesManager, init_macro:tuple=None):
        xyw = spec.get_spec_forConfig('xy')[target_q]['pi_len']
        # ret = AllXY_executor(q_name,ro_element[0],xyw,dyna_config.get_config(),qmm,mode='wait')

        # start_time = time.time()
        level = 'basic'

        amp_rec = []
        freq_rec = []
        detu_ans = []
        amp_ans = []
        iter = 6
        virtual_detune = 1 # Unit in MHz
        jump_out = False

        while True:
            amp_rec.append(float(spec.get_spec_forConfig('xy')[target_q][f'pi_amp']))
            freq_rec.append(float(spec.get_spec_forConfig('xy')[target_q][f'qubit_IF']))
            spec,config = amp_CaliFlow(target_q,spec,config,qm_machine,level, init_macro)
            # allXY_ret = AllXY_executor(q_name,ro_element[0],xyw,10000,dyna_config.get_config(),qmm,mode='wait')
            amp_ans.append(float(spec.get_spec_forConfig('xy')[target_q][f'pi_amp']))


            # after check detuning < 15 kHz, after amp calibrattion break
            if jump_out :
                print('detune < 15kHz, and amp had been calied with the tough N!')
                final_spec, final_config = spec, config
                break


            n_avg = 1000  # Number of averages
            
            output_data, evo_time = Ramsey_freq_calibration( virtual_detune, [q_name], ro_element,config.get_config(), qm_machine, n_avg=n_avg, simulate=False, mode='live', initializer=init_macro)
            ans = plot_ana_result(evo_time,output_data[ro_element[0]][0],virtual_detune)

            spec,config = refresh_Q_IF(target_q,spec,config,ans)
            print(f"detune={ans} MHz")
            if abs(float(ans)) < 0.5: # 500 kHz
                level = 'medium'
                
            
            if abs(float(ans)) < 0.015: # 50 kHz
                level = 'tough'
                jump_out = True
                

            

            detu_ans.append(ans)
        
            if break_optimize_condition(ans,detu_ans) and break_optimize_condition(float(spec.get_spec_forConfig('xy')[target_q][f'pi_amp']),amp_ans):
                print('Break conditions satisfied!')
                final_spec, final_config = spec, config
                break
            if iter <= 0:
                final_spec, final_config = spec, config
                break

            iter -= 1
        
        # end_time = time.time()
        #print(f"Optimization completed! Time cost: {end_time-start_time}s")

        log_plot(amp_rec, freq_rec)
        return final_spec, final_config
        

if __name__ == '__main__':

    qop_ip = '192.168.1.105'
    qop_port = None
    cluster_name = 'QPX_2'
    target_q = 'q1'
    ro_element = [f'{target_q}_ro']
    q_name =  f"{target_q}_xy"

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
    

    # load config file
    dyna_config = QM_config()
    dyna_config.import_config(path=r'.\TEST\BETAsite\QM\OPXPlus\3_5q Tune up\Standard Configuration\Config_Allidle_1205')
    the_specs = Circuit_info(q_num=5)
    the_specs.import_spec(path=r'.\TEST\BETAsite\QM\OPXPlus\3_5q Tune up\Standard Configuration\Spec_Allidle_1205')
    initial_macro = initializer((the_specs.give_WaitTime_with_q(target_q,5),),mode='wait')
    the_specs, dyna_config = AutoCaliFlow(target_q,the_specs,dyna_config,qmm,initial_macro)
    
    the_specs.export_spec(path=r'.\TEST\BETAsite\QM\OPXPlus\3_5q Tune up\Standard Configuration\Spec_1205_Calied')
    dyna_config.export_config(path=r'.\TEST\BETAsite\QM\OPXPlus\3_5q Tune up\Standard Configuration\Config_1205_Calied')
    print(the_specs.get_ReadableSpec_fromQ(target_q,'xy'))
    xyw = the_specs.get_spec_forConfig('xy')[target_q]['pi_len']
    ret = AllXY_executor(q_name,ro_element[0],xyw,10000,dyna_config.get_config(),qmm,mode='live',initializer=initial_macro)
