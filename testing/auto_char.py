import matplotlib.pyplot as plt
from QM_config_dynamic import QM_config
from qm.QuantumMachinesManager import QuantumMachinesManager
import numpy as np
from set_octave import OctaveUnit, octave_declaration
from qualang_tools.config.waveform_tools import drag_gaussian_pulse_waveforms, flattop_gaussian_waveform, gaussian
from qualang_tools.units import unit

cluster_name = "QPX_3"  # Write your cluster_name if version >= QOP220
qop_ip = "192.168.1.146"  # Write the QM router IP address
qop_port = None  # Write the QOP port if version < QOP220

############################
# Set octave configuration #
############################
# Custom port mapping example
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

# The Octave port is 11xxx, where xxx are the last three digits of the Octave internal IP that can be accessed from
# the OPX admin panel if you QOP version is >= QOP220. Otherwise, it is 50 for Octave1, then 51, 52 and so on.
octave_1 = OctaveUnit("octave1", qop_ip, port=11253, con="con1", clock="Internal", port_mapping=port_mapping)

# Add the octaves
octaves = [octave_1]
# Configure the Octaves
octave_config = octave_declaration(octaves)

qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
u = unit(coerce_to_integer=True)


myConfig = QM_config()
myConfig.set_wiring("con1")
mRO_common = {
        "I":("con1",1),
        "Q":("con1",2),
        "freq_LO": 6, # GHz
        "mixer": "octave_octave1_1",
        "time_of_flight": 200, # ns
        "integration_time": 2000, # ns
    }
mRO_individual = [
    {
        "name":"rr_temp", 
        "freq_RO": 6.01, # GHz
        "amp": 0.05, # V
    }
]

myConfig.update_multiplex_readout_channel(mRO_common, mRO_individual )
search_range = np.arange(-400e6, 400e6, 0.5e6)

test_config = myConfig.get_config()

from search_resonators import search_resonators
idata, qdata, repetition = search_resonators(search_range,test_config,"rr_temp",100,qmm)  
zdata = idata +1j*qdata
print(idata.shape)
plt.plot(search_range, np.abs(zdata),label="Dynamic")
plt.legend()
plt.show()

mRO_individual = [
        {
            "name":"rr1", 
            "freq_RO": 6.11, # GHz
            "amp": 0.008, # V
        },
        {
            "name":"rr2", 
            "freq_RO": 5.91, # GHz
            "amp": 0.0125, # V
        }
    ]




# n_avg = 100  # The number of averages
# # The frequency sweep around the resonators' frequency "resonator_IF_q"

myConfig.update_multiplex_readout_channel(mRO_common, mRO_individual )
# span = 10 * u.MHz
# df = 0.1 * u.MHz
# dfs = np.arange(-span, +span + 0.1, df)
# freq_IF = [ -215.5, 74 ]

# # The readout amplitude sweep (as a pre-factor of the readout amplitude) - must be within [-2; 2)
# a_min = 0.05
# a_max = 1.99
# da = 0.05
# amp_ratio = np.logspace(-2, 0, 10)  # The amplitude vector +da/2 to add a_max to the scan
# amp_log_ratio = np.log10(amp_ratio)
# qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

# test_config = myConfig.get_config()
from find_dispersive_limit_power import mRO_power_dep_resonator
output_data = mRO_power_dep_resonator(freq_IF, dfs, amp_ratio,1000,n_avg,test_config,["rr1","rr2"],qmm)  
idata = output_data["rr1"][0]
qdata = output_data["rr1"][1]
zdata = idata +1j*qdata
s21 = zdata/amp_ratio[:,None]
fig, ax = plt.subplots()
c = ax.pcolormesh(dfs, amp_log_ratio, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
ax.set_title('pcolormesh')
fig.show()
plt.show()