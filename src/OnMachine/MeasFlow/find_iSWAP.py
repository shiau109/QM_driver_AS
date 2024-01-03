


qubit_in_e = 2  # Qubit number to put in |e> at the beginning of the sequence
qubit_to_flux_tune = 1  # Qubit number to flux-tune

n_avg = 1300  # The number of averages
ts = np.arange(4, 200, 1)  # The flux pulse durations in clock cycles (4ns) - Must be larger than 4 clock cycles.
amps = np.arange(-0.315, -0.298, 0.0002) / const_flux_amp  # The flux amplitude pre-factor
# Flux offset
flux_bias = config["controllers"]["con1"]["analog_outputs"][
    config["elements"][f"q{qubit_to_flux_tune}_z"]["singleInput"]["port"][1]
]["offset"]
