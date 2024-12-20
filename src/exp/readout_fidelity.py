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
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.analysis import two_state_discriminator
# from exp.macros import qua_declaration, multiplexed_readout, reset_qubit
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save_singleShot
import numpy as np
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
import xarray as xr
import time
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
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            # Save all streamed points for plotting the IQ blobs
            multiRO_pre_save_singleShot( iqdata_stream, ro_element, ( shot_num, 2 ) )

    #####################################
    #  Open Communication with the QOP  #
    #####################################

    qm = qmm.open_qm(config)
    job = qm.execute(iq_blobs)

    ro_ch_name = []
    for r in ro_element:
        ro_ch_name.append(f"{r}_I")
        ro_ch_name.append(f"{r}_Q")
    data_list = ro_ch_name + ["iteration"]   

    results = fetching_tool(job, data_list=data_list, mode="live")
    # Live plotting
    while results.is_processing():
        # Fetch results
        fetch_data = results.fetch_all()
        # Progress bar
        iteration = fetch_data[-1]
        progress_counter(iteration, shot_num, start_time=results.start_time)
        # Plot
        time.sleep(1)

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


