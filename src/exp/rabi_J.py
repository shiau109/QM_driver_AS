from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
import sys
import pathlib
QM_script_root = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(QM_script_root)
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import warnings

warnings.filterwarnings("ignore")

def freq_time_rabi( dfs, time, q_name, ro_elements,Qi,qmm, initializer = None, simulate=False):

    with program() as rabi:

        iqdata_stream = multiRO_declare(ro_elements)
        t = declare(int)  
        df = declare()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(df, dfs)):
                # Update the frequency of the two resonator elements

                with for_( t, time):  
                    # Init
                    if initializer is None:
                        wait(100*u.us)
                        #wait(thermalization_time * u.ns)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            print("Initializer didn't work!")
                            wait(100*u.us)
                        
                    # Operation
                    for q in q_name:
                        play("x180", q, t)
                    align()
                    # Measurement
                    for r in ro_element:
                        update_frequency(r, df + center_IF[r])
                    multiRO_measurement(iqdata_stream, ro_element, weights="rotated_",amp_modify=0.5)

        with stream_processing():
            n_st.save("n")
            for i in q_id:
                I_st[q_id.index(i)].buffer(len(times)).average().save(f"I{i+1}")
                Q_st[q_id.index(i)].buffer(len(times)).average().save(f"Q{i+1}")
    if simulate:
        simulation_config = SimulationConfig(duration=10_000)  
        job = qmm.simulate(config, rabi, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(rabi)
        fig = plt.figure()
        interrupt_on_close(fig, job)
        I_list, Q_list = [f"I{i+1}" for i in q_id], [f"Q{i+1}" for i in q_id]
        results = fetching_tool(job, I_list + Q_list + ["n"], mode="live")
        while results.is_processing():
            all_results = results.fetch_all()
            n = all_results[-1]
            I, Q = all_results[0:len(q_id)], all_results[len(q_id):len(q_id)*2]
            for i in q_id:
                I[q_id.index(i)] = u.demod2volts(I[q_id.index(i)], readout_len)
                Q[q_id.index(i)] = u.demod2volts(Q[q_id.index(i)], readout_len)
            progress_counter(n, n_avg, start_time=results.start_time)
            live_plotting(I,Q,plot_index)    
        qm.close()
        plt.show()
        return I, Q

def live_plotting(I,Q,plot_index):
    plt.suptitle("Time Rabi \n number of average = " + str(n_avg))
    plt.subplot(121)
    plt.cla()
    plt.plot(4 * times, I[plot_index])
    plt.title(f"Qubit {Qi}")
    plt.xlabel("Qubit pulse duration [ns]")
    plt.ylabel("I quadrature [V]")
    plt.tight_layout()
    plt.subplot(122)
    plt.cla()
    plt.plot(4 * times, Q[plot_index])
    plt.title(f"Qubit {Qi}")
    plt.xlabel("Qubit pulse duration [ns]")
    plt.ylabel("Q quadrature [V]")
    plt.tight_layout()
    plt.pause(1.0)

def pi_length_fitting(I,Q,plot_index):
    try:
        from qualang_tools.plot.fitting import Fit
        fit = Fit()
        fit.rabi(4 * times, I[plot_index], plot=True)
        plt.xlabel("Qubit pulse duration [ns]")
        plt.ylabel("I quadrature [V]")
        plt.title(f"Qubit {Qi}")
        plt.show()
        plt.cla()
        fit.rabi(4 * times, Q[plot_index], plot=True)
        plt.xlabel("Qubit pulse duration [ns]")
        plt.ylabel("Q quadrature [V]")
        plt.title(f"Qubit {Qi}")
        plt.tight_layout()
        plt.show()
    except (Exception,):
        pass

times = np.arange(4, 200, 1)  
n_avg = 1000
q_id = [1,2,3,4]
Qi = 4
simulate = False 
operation_flux_point = [0, -3.000e-01, -0.2525, -0.3433, -3.400e-01] 
for i in q_id: 
    if i == Qi-1: plot_index = q_id.index(i)  

qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
I,Q = time_rabi(q_id,Qi,simulate,qmm)
pi_length_fitting(I,Q,plot_index)