import os
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

# Function to compute phase map from a single dataset
def compute_phase_map(dataset, shot_num, threhold_q3):
    cz_amp = dataset.coords["cz_amp"].values
    c_amp = dataset.coords["c_amp"].values
    data = dataset["q0_ro"].values[0]

    population_gx = np.zeros((len(c_amp), len(cz_amp)))  # ground state x-basis
    population_gy = np.zeros((len(c_amp), len(cz_amp)))  # ground state y-basis
    population_gz = np.zeros((len(c_amp), len(cz_amp)))  # ground state z-basis

    population_ex = np.zeros((len(c_amp), len(cz_amp)))  # excited state x-basis
    population_ey = np.zeros((len(c_amp), len(cz_amp)))  # excited state y-basis
    population_ez = np.zeros((len(c_amp), len(cz_amp)))  # excited state z-basis

    phase_map = np.zeros((len(c_amp), len(cz_amp)))

    for i in range(shot_num):
        for j in range(len(c_amp)):
            for k in range(len(cz_amp)):
                if data[i, j, k, 0, 0] >= threhold_q3:
                    population_gx[j, k] += 1
                if data[i, j, k, 0, 1] >= threhold_q3:
                    population_gy[j, k] += 1
                if data[i, j, k, 0, 2] >= threhold_q3:
                    population_gz[j, k] += 1
                if data[i, j, k, 1, 0] >= threhold_q3:
                    population_ex[j, k] += 1
                if data[i, j, k, 1, 1] >= threhold_q3:
                    population_ey[j, k] += 1
                if data[i, j, k, 1, 2] >= threhold_q3:
                    population_ez[j, k] += 1

    # Normalize by shot number
    population_gx /= shot_num
    population_gy /= shot_num
    population_gz /= shot_num
    population_ex /= shot_num
    population_ey /= shot_num
    population_ez /= shot_num

    # Compute phase map
    for i in range(len(c_amp)):
        for j in range(len(cz_amp)):
            gy = (1 - population_gy[i, j]) - population_gy[i, j]
            gx = (1 - population_gx[i, j]) - population_gx[i, j]
            g_phi = np.arctan2(gy, gx)

            ey = (1 - population_ey[i, j]) - population_ey[i, j]
            ex = (1 - population_ex[i, j]) - population_ex[i, j]
            e_phi = np.arctan2(ey, ex)

            phase_diff = abs(g_phi - e_phi) - np.pi
            phase_map[i, j] = phase_diff


    return phase_map

# Function to process all .nc files in the directory
def process_directory(dir_path, shot_num, threhold_q3):
    phase_maps = []

    for filename in os.listdir(dir_path):
        if filename.endswith(".nc"):
            filepath = os.path.join(dir_path, filename)
            dataset = xr.open_dataset(filepath, engine='netcdf4', format='NETCDF4')
            phase_map = compute_phase_map(dataset, shot_num, threhold_q3)
            phase_maps.append(phase_map)

    # Convert list of phase maps to 3D numpy array (n_files, len(c_amp), len(cz_amp))
    phase_maps = np.array(phase_maps)

    # Compute mean and standard deviation across all files
    mean_phase_map = np.mean(phase_maps, axis=0)
    std_phase_map = np.std(phase_maps, axis=0)

    return mean_phase_map, std_phase_map

# Plotting the mean and std phase maps
def plot_phase_maps(mean_map, std_map, cz_amp, c_amp, threshold=0.1*2*np.pi):
    # Apply threshold to mean map
    mask = abs(mean_map) < threshold
    mean_map_filtered = np.where(mask, mean_map, threshold)
    std_map_filtered = np.where(mask, std_map, np.NaN)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Plot filtered mean phase map
    a1 = ax1.pcolormesh(cz_amp, c_amp, mean_map_filtered, cmap='RdBu', shading='auto')
    ax1.set_xlabel("q2 z")
    ax1.set_ylabel("coupler z")
    plt.colorbar(a1, ax=ax1, label="Mean phase difference - pi")

    # Plot filtered std phase map
    a2 = ax2.pcolormesh(cz_amp, c_amp, std_map_filtered, cmap='RdBu', shading='auto')
    ax2.set_xlabel("q2 z")
    ax2.set_ylabel("coupler z")
    plt.colorbar(a2, ax=ax2, label="STD phase difference - pi")

    plt.tight_layout()
    plt.show()

# Main execution
dir_path = r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240920_DRKe_5Q4C\save_data\CZ_sweet\crosstalk_not_compensated\phase_check\phase\multi"
shot_num = 500
threhold_q3 = 5.865e-05

# Process all .nc files in the directory
mean_phase_map, std_phase_map = process_directory(dir_path, shot_num, threhold_q3)

# Get cz_amp and c_amp from one of the datasets
sample_dataset = xr.open_dataset(os.path.join(dir_path, os.listdir(dir_path)[0]), engine='netcdf4', format='NETCDF4')
cz_amp = sample_dataset.coords["cz_amp"].values
c_amp = sample_dataset.coords["c_amp"].values

# Plot the results
plot_phase_maps(mean_phase_map, std_phase_map, cz_amp, c_amp)
