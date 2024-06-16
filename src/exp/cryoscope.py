
from qm.qua import *
from qm import QuantumMachinesManager


from qualang_tools.loops import from_array

from qualang_tools.units import unit
u = unit(coerce_to_integer=True)

from exp.QMMeasurement import QMMeasurement
from exp.RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save

import xarray as xr

class Cryoscope( QMMeasurement ):
    """
            CRYOSCOPE with 4ns granularity
    The goal of this protocol is to measure the step response of the flux line and design proper FIR and IIR filters
    (implemented on the OPX) to pre-distort the flux pulses and improve the two-qubit gates fidelity.
    Since the flux line ends on the qubit chip, it is not possible to measure the flux pulse after propagation through the
    fridge. The idea is to exploit the flux dependency of the qubit frequency, measured with a modified Ramsey sequence, to
    estimate the flux amplitude received by the qubit as a function of time.

    The sequence consists of a Ramsey sequence ("x90" - idle time - "x90" or "y90") with a fixed dephasing time.
    A flux pulse with varying duration is played during the idle time. The Sx and Sy components of the Bloch vector are
    measured by alternatively closing the Ramsey sequence with a "x90" or "y90" gate in order to extract the qubit dephasing
    as a function of the flux pulse duration.

    The results are then post-processed to retrieve the step function of the flux line which is fitted with an exponential
    function. The corresponding exponential parameters are then used to derive the FIR and IIR filter taps that will
    compensate for the distortions introduced by the flux line (wiring, bias-tee...).
    Such digital filters are then implemented on the OPX. Note that these filters will introduce a global delay on all the
    output channels that may rotate the IQ blobs so that you may need to recalibrate them for state discrimination or
    active reset protocols for instance. You can read more about these filters here:
    https://docs.quantum-machines.co/0.1/qm-qua-sdk/docs/Guides/output_filter/?h=filter#hardware-implementation

    The protocol is inspired from https://doi.org/10.1063/1.5133894, which contains more details about the sequence and
    the post-processing of the data.

    This version sweeps the flux pulse duration using real-time QUA, which means that the flux pulse can be arbitrarily long
    but the step must be larger than 1 clock cycle (4ns) and the minimum pulse duration must be 4 clock cycles (16ns).

    Prerequisites:
        - Having found the resonance frequency of the resonator coupled to the qubit under study (resonator_spectroscopy).
        - Having calibrated qubit gates (x90 and y90) by running qubit spectroscopy, rabi_chevron, power_rabi, Ramsey and updated the configuration.
        - (optional) Having calibrated the readout to perform state discrimination (IQ_blobs).

    Next steps before going to the next node:
        - Update the FIR and IIR filter taps in the configuration (config/controllers/con1/analog_outputs/"filter": {"feedforward": fir, "feedback": iir}).
        - WARNING: the digital filters will add a global delay --> need to recalibrate IQ blobs (rotation_angle & ge_threshold).
    """
    def __init__( self, config, qmm: QuantumMachinesManager ):
        super().__init__( config, qmm )

        self.ro_elements = ["q0_ro"]
        self.z_elements = []
        self.xy_elements = []

        self.initializer = None

        self.xyz_timing_buffer = 80

        self.pad_zeros = ( 20, 0 )

        self.time_range = ( 16, 600 )
        self.resolution = 4
        self.duration_cc_qua = self._lin_cc_array( )
        self.amp_modify = 0.2
    

    def _get_qua_program( self ):
        
        self.duration_cc_qua = self._lin_cc_array( )

        with program() as cryoscope:
            n = declare(int)  # QUA variable for the averaging loop
            t = declare(int)  # QUA variable for the flux pulse duration
            flag = declare(bool)  # QUA boolean to switch between x90 and y90

            iqdata_stream = multiRO_declare( self.ro_elements )

            n_st = declare_stream()  # Stream for the averaging iteration 'n'

            # Outer loop for averaging
            with for_(n, 0, n < self.shot_num, n + 1):
                # Loop over the truncated flux pulse
                with for_(*from_array(t, self.duration_cc_qua)):
                    # Alternate between X/2 and Y/2 pulses
                    with for_each_(flag, [True, False]):

                        # Initialization
                        if self.initializer is None:
                            wait( 100*u.us )
                        else:
                            try:
                                self.initializer[0](*self.initializer[1])
                            except:
                                print("initializer didn't work!")
                                wait( 100*u.us )



                        # Operation
                        # Play first X/2
                        play("x90", self.xy_elements[0])
                        # Play truncated flux pulse
                        align()
                        # Wait some time to ensure that the flux pulse will arrive after the x90 pulse
                        wait( self.xyz_timing_buffer )

                        with if_(t > 3):
                            play("const"*amp(self.amp_modify), self.z_elements[0], duration=t)
                        # Wait for the idle time set slightly above the maximum flux pulse duration to ensure that the 2nd x90
                        # pulse arrives after the longest flux pulse
                        wait( max(self.duration_cc_qua) +self.xyz_timing_buffer, self.xy_elements[0] )
                        # Play second X/2 or Y/2
                        with if_(flag):
                            play("x90", self.xy_elements[0])
                        with else_():
                            play("y90", self.xy_elements[0])

                        # Measure resonator state after the sequence
                        align()
                        # Readout
                        multiRO_measurement( iqdata_stream, self.ro_elements, weights='rotated_' )
                save(n, n_st)

            with stream_processing():
                # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
                multiRO_pre_save( iqdata_stream, self.ro_elements, (len(self.duration_cc_qua), 2))
                n_st.save("iteration")

        return cryoscope
    
    def _get_fetch_data_list( self ):
        ro_ch_name = []
        for r_name in self.ro_elements:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")

        data_list = ro_ch_name + ["iteration"]   
        return data_list
    
    def _data_formation( self ):

        time = self.duration_cc_qua *4
        output_data = {}
        for r_idx, r_name in enumerate(self.ro_elements):
            output_data[r_name] = ( ["mixer","time", "r90"],
                                np.array([self.fetch_data[r_idx*2], self.fetch_data[r_idx*2+1]]) )
        dataset = xr.Dataset(
            output_data,
            coords={ "mixer":np.array(["I","Q"]), "time": time, "r90":np.array(["x","y"]) }
        )
        transposed_data = dataset.transpose("mixer", "r90", "time")

        return transposed_data

    def _lin_cc_array( self ):

        cc_resolution = self.resolution//4

        min_cc = self.time_range[0]//4
        if min_cc < 4: min_cc = 4
        max_cc = self.time_range[1]//4

        pad_zeros_cc = ( self.pad_zeros[0]//4, self.pad_zeros[1]//4 )

        return np.arange( min_cc-pad_zeros_cc[0], max_cc+pad_zeros_cc[1], cc_resolution )
    


####################
# Helper functions #
####################
def exponential_decay(x, a, t):
    """Exponential decay defined as 1 + a * np.exp(-x / t).

    :param x: numpy array for the time vector in ns
    :param a: float for the exponential amplitude
    :param t: float for the exponential decay time in ns
    :return: numpy array for the exponential decay
    """
    return 1 + a * np.exp(-x / t)


def exponential_correction(A, tau, Ts=1e-9):
    """Derive FIR and IIR filter taps based on the exponential coefficients A and tau from 1 + a * np.exp(-x / t).

    :param A: amplitude of the exponential decay.
    :param tau: decay time of the exponential decay.
    :param Ts: sampling period. Default is 1e-9.
    :return: FIR and IIR taps.
    """
    tau = tau * Ts
    k1 = Ts + 2 * tau * (A + 1)
    k2 = Ts - 2 * tau * (A + 1)
    c1 = Ts + 2 * tau
    c2 = Ts - 2 * tau
    feedback_tap = k2 / k1
    feedforward_taps = np.array([c1, c2]) / k1
    return feedforward_taps, feedback_tap


def filter_calc(exponential):
    """Derive FIR and IIR filter taps based on a list of exponential coefficients.

    :param exponential: exponential coefficients defined as [(A1, tau1), (A2, tau2)]
    :return: FIR and IIR taps as [fir], [iir]
    """
    # Initialization based on the number of exponential coefficients
    b = np.zeros((2, len(exponential)))
    feedback_taps = np.zeros(len(exponential))
    # Derive feedback tap for each set of exponential coefficients
    for i, (A, tau) in enumerate(exponential):
        b[:, i], feedback_taps[i] = exponential_correction(A, tau)
    # Derive feedback tap for each set of exponential coefficients
    feedforward_taps = b[:, 0]
    for i in range(len(exponential) - 1):
        feedforward_taps = np.convolve(feedforward_taps, b[:, i + 1])
    # feedforward taps are bounded to +/- 2
    if np.abs(max(feedforward_taps)) >= 2:
        feedforward_taps = 2 * feedforward_taps / max(feedforward_taps)

    return feedforward_taps, feedback_taps


