# import sys
# sys.path.append('./exp')
# sys.path.append('./analysis')
from QM_config_dynamic import QM_config, Circuit_info
from qm.QuantumMachinesManager import QuantumMachinesManager
from SQGate_calibration import amp_calibration
from fitting_method import find_amp_minima, math_eqns
from numpy import mean, ndarray, arange
import matplotlib.pyplot as plt
from set_octave import OctaveUnit, octave_declaration
import time

# Update a new amp
def refresh_amp(specs:dict,config:object,amp_modi_scale:float,mode:str='180'):
    if mode == '180':
        old_amp = float(specs.get_spec_forConfig('xy')[target_q][f'pi_amp'])
        specs.update_aXyInfo_for(target_q,amp=old_amp*amp_modi_scale)
        config.update_controlWaveform(specs.get_spec_forConfig('xy'),target_q)
    else:
        old_half_scale = float(specs.get_spec_forConfig('xy')[target_q]["half_pi_ampScale"]["90"] )
        specs.update_aXyInfo_for(target_q,half=amp_modi_scale*old_half_scale)
        config.update_controlWaveform(specs.get_spec_forConfig('xy'),target_q)

    return specs, config

def refresh_Q_IF(target_q:str,specs:dict,config:object,IF_modi:float):
    '''
        IF_modi in MHZ
    '''
    old_if = specs.get_spec_forConfig('xy')[target_q]['qubit_IF']*1e-6
        
    config.update_controlFreq(specs.update_aXyInfo_for(target_q=target_q,IF=old_if+IF_modi))

    return specs, config
        


def new_N_condition(x:ndarray,amp_scale:float,sweetspot:int=12):
    if amp_scale > 1-((x[-1]-x[0])/sweetspot)*0.5 and amp_scale < 1+((x[-1]-x[0])/sweetspot)*0.5:
        return True
    else:
        return False
    

def Cali_workflow(spec,config,request:str='basic'):
    '''
        operations: 180 for X180 operation, 90 for X90 operation.\n
        request: 'basic' for max(N) = 10, 'advanced' for max(N) = 30
    '''
    # initialize
    precision_N_idx = 0
    if request == 'basic':
        N_candidate = [1, 9]
    else:
        N_candidate = [18, 30, 60]

    iterations = 0
    max_iteration = 15


    # Workflow start
    while (precision_N_idx <= len(N_candidate)-1) and (iterations < max_iteration):
        print(f'iterations= {iterations}')
        sequence_repeat = N_candidate[precision_N_idx]
        amp_modify_range = 0.25/float(sequence_repeat)

        results = amp_calibration(amp_modify_range, q_name, ro_element, config.get_config(), qmm, n_avg=2000, sequence_repeat=sequence_repeat, simulate=False, mode='wait')
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
        
        # # plot and check 
        # plt.plot(x,y,label='exp')
        # plt.plot(x, math_eqns.cosine(x,*fit_paras),label='fit')
        # plt.scatter(amp_scale, math_eqns.cosine(amp_scale,*fit_paras),c='red',marker='X',s=80 ,label='ans')
        # plt.title(f'N={sequence_repeat}')
        # plt.legend()
        # plt.show()

        # Update amp
        spec,config = refresh_amp(spec,config,amp_scale_180,'180')
        spec,config = refresh_amp(spec,config,amp_scale_90/amp_scale_180,'90')

        iterations += 1
        print("Update complete!")

        if new_N_condition(x,amp_scale_180,2.5):
            if new_N_condition(x,amp_scale_90,2.5):
                precision_N_idx += 1
        
    # plot and check 
    # plt.plot(x,y_180,label='180')
    # plt.plot(x,y_90,label='90')
    # plt.plot(x, math_eqns.cosine(x,*fit_paras_180),label='fit')
    # plt.plot(x, math_eqns.cosine(x,*fit_paras_90),label='fit')
    # plt.scatter(amp_scale_180, math_eqns.cosine(amp_scale_180,*fit_paras_180),marker='X',s=80 ,label=f'180 ans={amp_scale_180}')
    # plt.scatter(amp_scale_90, math_eqns.cosine(amp_scale_90,*fit_paras_90),s=80 ,label=f'90 ans={amp_scale_90}')
    
    # plt.legend()
    # plt.show() 

    return spec, config




##############################
######      ALL XY     #######       
##############################

# all XY
from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from configuration import *
import matplotlib.pyplot as plt
import numpy as np
from qm import SimulationConfig
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
import warnings

warnings.filterwarnings("ignore")

###################
#   Data Saving   #
###################
from datetime import datetime
import sys
# save_data = True  # Default = False in configuration file
save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
save_time = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
save_path = f"{save_dir}\{save_time}_{save_progam_name}"

##############################
# Program-specific variables #
##############################
# The resonator to measure the qubit defined above
n_avg = 500000  # The number of 

# # Tune flux and neighboring qubits
# flux_id = 0
# flux_offset = np.zeros(5)
# flux_offset[flux_id] = max_frequency_point[flux_id]
# detune_neighbor = True
# if detune_neighbor == True:
#     if flux_id != 0: flux_offset[flux_id-1] = detune_point[flux_id-1]
#     if flux_id != 4: flux_offset[flux_id+1] = detune_point[flux_id+1]

# All XY sequences. The sequence names must match corresponding operation in the config
sequence = [
    ("I", "I"),
    ("x180", "x180"),
    ("y180", "y180"),
    ("x180", "y180"),
    ("y180", "x180"),
    ("x90", "I"),
    ("y90", "I"),
    ("x90", "y90"),
    ("y90", "x90"),
    ("x90", "y180"),
    ("y90", "x180"),
    ("x180", "y90"),
    ("y180", "x90"),
    ("x90", "x180"),
    ("x180", "x90"),
    ("y90", "y180"),
    ("y180", "y90"),
    ("x180", "I"),
    ("y180", "I"),
    ("x90", "x90"),
    ("y90", "y90"),
]


# All XY macro generating the pulse sequences from a python list.
def allXY(pulses, qb, res, xyw):
    """
    Generate a QUA sequence based on the two operations written in pulses. Used to generate the all XY program.
    **Example:** I, Q = allXY(['I', 'y90'])
    :param pulses: tuple containing a particular set of operations to play. The pulse names must match corresponding
        operations in the config except for the identity operation that must be called 'I'.
    :param qubit: The qubit element as defined in the config.
    :param resonator: The resonator element as defined in the config.
    :return: two QUA variables for the 'I' and 'Q' quadratures measured after the sequence.
    """
    I_xy = declare(fixed)
    Q_xy = declare(fixed)
    if pulses[0] != "I":
        play(pulses[0], qb)  # Either play the sequence
    else:
        wait(xyw // 4, qb)  # or wait if sequence is identity
    if pulses[1] != "I":
        play(pulses[1], qb)  # Either play the sequence
    else:
        wait(xyw // 4, qb)  # or wait if sequence is identity

    align(qb, res)
    # Play through the 2nd resonator to be in the same condition as when the readout was optimized
    # if resonator == "rr1":
    #     align(qubit, "rr2")
    #     measure("readout", "rr2", None)
    # elif resonator == "rr2":
    #     align(qubit, "rr1")
    #     measure("readout", "rr1", None)
    measure(
        "readout",
        res,
        None,
        dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", I_xy),
        dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", Q_xy),
    )
    return I_xy, Q_xy


###################
# The QUA program #
###################
def AllXY_executor(qb,res,xyw,configuration,qm_mache,mode,n_avg=10000):
    with program() as ALL_XY:
        n = declare(int)
        n_st = declare_stream()
        r = Random()  # Pseudo random number generator
        r_ = declare(int)  # Index of the sequence to play
        # The result of each set of gates is saved in its own stream
        I_st = [declare_stream() for _ in range(21)]
        Q_st = [declare_stream() for _ in range(21)]

        # for i in [0,1,2,3]:
        #     # set_dc_offset(f"q{i+1}_z", "single", flux_offset[i])
        #     set_dc_offset(f"q{i+1}_z", "single", max_frequency_point[i])

        with for_(n, 0, n < n_avg, n + 1):
            # Get a value from the pseudo-random number generator on the OPX FPGA
            assign(r_, r.rand_int(21))
            # # Wait for the qubit to decay to the ground state - Can be replaced by active reset
            # wait(thermalization_time * u.ns, qb)
            wait(100 * u.us, qb)
            # Plays a random XY sequence
            # The switch/case method allows to map a python index (here "i") to a QUA number (here "r_") in order to switch
            # between elements in a python list (here "sequence") that cannot be converted into a QUA array (here because it
            # contains strings).
            with switch_(r_):
                for i in range(21):
                    with case_(i):
                        # Play the all-XY sequence corresponding to the drawn random number
                        I, Q = allXY(sequence[i], qb, res, xyw)
                        # Save the 'I' & 'Q' quadratures to their respective streams
                        save(I, I_st[i])
                        save(Q, Q_st[i])
            save(n, n_st)

        with stream_processing():
            n_st.save("n")
            for i in range(21):
                I_st[i].average().save(f"I{i}")
                Q_st[i].average().save(f"Q{i}")

    #####################################
    #  Open Communication with the QOP  #
    #####################################
    

    ###########################
    # Run or Simulate Program #
    ###########################

    simulate = False

    if simulate:
        # Simulates the QUA program for the specified duration
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qm_mache.simulate(configuration, ALL_XY, simulation_config)
        job.get_simulated_samples().con1.plot()

    else:
        # Open the quantum machine
        qm = qm_mache.open_qm(configuration)
        # Send the QUA program to the OPX, which compiles and executes it
        job = qm.execute(ALL_XY)
        # Get results from QUA program
        data_list = ["n"] + list(np.concatenate([[f"I{i}", f"Q{i}"] for i in range(len(sequence))]))
        results = fetching_tool(job, data_list, mode="live")
        # Live plotting
        if mode == 'live':
            fig = plt.figure()
            interrupt_on_close(fig, job)  # Interrupts the job when closing the figure
            while results.is_processing():
                # Fetch results
                res = results.fetch_all()
                I = -np.array(res[1::2])
                Q = -np.array(res[2::2])
                n = res[0]
                # Progress bar
                progress_counter(n, n_avg, start_time=results.start_time)
                # Plot results
                plt.suptitle(f"All XY for qubit {qb}")
                plt.subplot(211)
                plt.cla()
                plt.plot(I, "bx", label="Experimental data")
                plt.plot([np.max(I)] * 5 + [(np.mean(I))] * 12 + [np.min(I)] * 4, "r-", label="Expected value")
                plt.ylabel("I quadrature [a.u.]")
                plt.xticks(ticks=range(len(sequence)), labels=["" for _ in sequence], rotation=45)
                plt.legend()
                plt.subplot(212)
                plt.cla()
                plt.plot(Q, "bx", label="Experimental data")
                plt.plot([np.max(Q)] * 5 + [(np.mean(Q))] * 12 + [np.min(Q)] * 4, "r-", label="Expected value")
                plt.ylabel("Q quadrature [a.u.]")
                plt.xticks(ticks=range(len(sequence)), labels=[str(el) for el in sequence], rotation=45)
                plt.legend()
                plt.tight_layout()
                plt.pause(10)
                if save_data == True:
                    ###################
                    #  Figure Saving  #
                    ################### 
                    figure = plt.gcf() # get current figure
                    figure.set_size_inches(9, 5)
                    plt.tight_layout()
                    plt.pause(10)
                    plt.savefig(f"{save_path}.png", dpi = 500)   
                plt.show()
                plt.close()
        else:
            while results.is_processing():
                # Fetch results
                res = results.fetch_all()
                n = res[0]
                # Progress bar
                progress_counter(n, n_avg, start_time=results.start_time)

        # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
        qm.close()
        return {"I":-np.array(res[1::2]),"Q":-np.array(res[2::2])}




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
    n_avg = 4000

    # load config file
    dyna_config = QM_config()
    dyna_config.import_config(path=r'.\TEST\BETAsite\QM\OPXPlus\3_5q Tune up\Standard Configuration\ampCaliConfig_1201')
    the_specs = Circuit_info(q_num=5)
    the_specs.import_spec(path=r'.\TEST\BETAsite\QM\OPXPlus\3_5q Tune up\Standard Configuration\ampCaliSpec_1201')

    xyw = the_specs.get_spec_forConfig('xy')[target_q]['pi_len']
    ret = AllXY_executor(q_name,ro_element[0],xyw,dyna_config.get_config(),qmm,mode='wait')

    start_time = time.time()
    for level in ['basic','basic','advanced','advanced']:
        the_specs,dyna_config = Cali_workflow(the_specs,dyna_config,level)

        # the_specs.export_spec(path=r'.\TEST\BETAsite\QM\OPXPlus\3_5q Tune up\Standard Configuration\Spec_1201_afterAmpCali')
        # dyna_config.export_config(path=r'.\TEST\BETAsite\QM\OPXPlus\3_5q Tune up\Standard Configuration\Config_1201_afterAmpCali')

        # ramsey opti freq
        from Ramsey_freq_calibration import Ramsey_freq_calibration, plot_ana_result

        n_avg = 1000  # Number of averages
        virtual_detune = 1 # Unit in MHz
        output_data, evo_time = Ramsey_freq_calibration( virtual_detune, [q_name], ro_element,dyna_config.get_config(), qmm, n_avg=n_avg, simulate=False, mode='live')
        ans = plot_ana_result(evo_time,output_data[ro_element[0]][0],virtual_detune)

        the_specs,dyna_config = refresh_Q_IF(target_q=target_q,specs=the_specs,config=dyna_config,IF_modi=ans)
    
    end_time = time.time()
    print(f"Optimization completed! Time cost: {end_time-start_time}s")

    the_specs.export_spec(path=r'.\TEST\BETAsite\QM\OPXPlus\3_5q Tune up\Standard Configuration\Spec_1201_Calied')
    dyna_config.export_config(path=r'.\TEST\BETAsite\QM\OPXPlus\3_5q Tune up\Standard Configuration\Config_1201_Calied')

    # old_if = the_specs.get_spec_forConfig('xy')[target_q]['qubit_IF']*1e-6
    # dyna_config.update_controlFreq(the_specs.update_aXyInfo_for(target_q='q1',IF=old_if-0.8))

    xyw = the_specs.get_spec_forConfig('xy')[target_q]['pi_len']
    ret = AllXY_executor(q_name,ro_element[0],xyw,dyna_config.get_config(),qmm,mode='live')
