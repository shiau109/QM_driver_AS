"""
        IQ BLOBS
This sequence involves measuring the state of the resonator 'N' times, first after thermalization (with the qubit
in the |g> state) and then after applying a pi pulse to the qubit (bringing the qubit to the |e> state) successively.
The resulting IQ blobs are displayed, and the data is processed to determine:
    - The rotation angle required for the integration weights, ensuring that the separation between |g> and |e> states
      aligns with the 'I' quadrature.
    - The threshold along the 'I' quadrature for effective qubit state discrimination.
    - The readout fidelity matrix, which is also influenced by the pi pulse fidelity.

Prerequisites:
    - Having found the resonance frequency of the resonator coupled to the qubit under study (resonator_spectroscopy).
    - Having calibrated qubit pi pulse (x180) by running qubit, spectroscopy, rabi_chevron, power_rabi and updated the config.
    - Set the desired flux bias

Next steps before going to the next node:
    - Update the rotation angle (rotation_angle) in the configuration.
    - Update the g -> e threshold (ge_threshold) in the configuration.
"""

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm.simulate import SimulationConfig
# from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.results import fetching_tool
from qualang_tools.analysis import two_state_discriminator
# from exp.macros import qua_declaration, multiplexed_readout, reset_qubit
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save_singleShot

from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
import xarray as xr
def readout_fidelity( q_name:list, ro_element, shot_num, config, qmm:QuantumMachinesManager, initializer=None):
    """
    Single shot detect
    """
    
    with program() as iq_blobs:

        iqdata_stream = multiRO_declare( ro_element )

        n = declare(int)
        n_st = declare_stream()
        p_idx = declare(int)
        with for_(n, 0, n < shot_num, n + 1):

            with for_each_( p_idx, [0, 1]):  
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
                with switch_(p_idx, unsafe=True):
                    with case_(0):
                        pass
                    with case_(1):
                        for q in q_name:
                            play("x180", q)
                align()
                # Readout
                multiRO_measurement(iqdata_stream, ro_element, weights="rotated_")  

        with stream_processing():
            # Save all streamed points for plotting the IQ blobs
            multiRO_pre_save_singleShot( iqdata_stream, ro_element, ( shot_num, 2 ) )

    #####################################
    #  Open Communication with the QOP  #
    #####################################

    qm = qmm.open_qm(config)
    job = qm.execute(iq_blobs)
    data_list = []
    for r in ro_element:
        data_list.append(f"{r}_I")
        data_list.append(f"{r}_Q")

    
    results = fetching_tool(job, data_list=data_list, mode="wait_for_all")
    fetch_data = results.fetch_all()
    qm.close()
    # Creating an xarray dataset
    output_data = {}
    for r_idx, r_name in enumerate(ro_element):
        output_data[r_name] = ( ["mixer","index","state"],
                                np.array([ fetch_data[r_idx*2][0], fetch_data[r_idx*2+1][0] ]) )
    dataset = xr.Dataset(
        output_data,
        coords={ "mixer":np.array(["I","Q"]), "index": np.arange(shot_num), "state":[0,1] }
    )
    return dataset

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import time
    from analysis.state_distribution import train_model, create_img

    ###################
    ###################


    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
    resonators = ["rr1"]
    n_runs = 10000
    reset = "cooldown"  # can be set to "cooldown" or "active"

    start_time = time.time()
    output_data = readout_fidelity( [0], resonators, n_runs, reset, config, qmm)  
    end_time = time.time()
    elapsed_time = np.round(end_time-start_time, 1)

    for r in resonators:
        
        gmm_model = train_model(output_data[r]*1000)
        fig = plt.figure(constrained_layout=True)
        create_img(output_data[r]*1000, gmm_model)
        # fig.show()
        # plt.show()
        two_state_discriminator(output_data[r][0][0], output_data[r][0][1], output_data[r][1][0], output_data[r][1][1], True, True)

    plt.show()
    #   Data Saving   # 
    save_data = True
    if save_data:
        from exp.save_data import save_npz
        import sys
        save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
        save_npz(save_dir, save_progam_name, output_data)

    plt.show()

