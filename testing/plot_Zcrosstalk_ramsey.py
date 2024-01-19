import numpy as np
import matplotlib.pyplot as plt
raw_data = np.load(r'D:\Data\DR2_5Q\1u_Q2Z1_crosstalk_ramsey_20240118_1419.npz', allow_pickle=True)# ["arr_0"].item()
# tomo_data =
other_info = {}
for k, v in raw_data.items():
    print(k, v.shape)
    if k in ["paras","setting"]:
        other_info[k]=v.item()

for k, v in other_info.items():
    print(k)

d_z_target_amp = other_info["paras"]["d_z_target_amp"]
d_z_crosstalk_amp = other_info["paras"]["d_z_crosstalk_amp"]




# Create a 2D numpy array (example data)
data = raw_data["q2_ro"][0]
offset = np.mean(data)
print(offset)
data -= offset


from scipy.interpolate import interp2d
# Create an interpolation function
interp_func = interp2d(d_z_crosstalk_amp, d_z_target_amp, data, kind='linear')

# Define new points for interpolation
new_d_z_target_amp = np.linspace(d_z_target_amp[0], d_z_target_amp[-1], 500)
new_d_z_crosstalk_amp = np.linspace(d_z_crosstalk_amp[0], d_z_crosstalk_amp[-1], 500)

# Interpolate values at new points
new_data = interp_func(new_d_z_crosstalk_amp, new_d_z_target_amp )
# Apply Gaussian smoothing
from scipy.ndimage import gaussian_filter
sigma = 1.0  # Adjust the standard deviation based on your needs
smoothed_data = gaussian_filter(data, sigma=sigma)
# data = smoothed_data
# d_z_target_amp = new_d_z_target_amp
# d_z_crosstalk_amp = new_d_z_crosstalk_amp

# M = d_z_target_amp[0]-d_z_target_amp[-1]
print(data.shape, d_z_target_amp.shape, d_z_crosstalk_amp.shape)
# N = d_z_crosstalk_amp[0]-d_z_crosstalk_amp[1]
M, N = data.shape
f_z_target = np.fft.fftshift(np.fft.fftfreq(M, d=np.abs(d_z_target_amp[0]-d_z_target_amp[1])))
f_z_crosstalk = np.fft.fftshift(np.fft.fftfreq(N, d=np.abs(d_z_crosstalk_amp[0]-d_z_crosstalk_amp[1])))
print(f_z_target.shape, f_z_crosstalk.shape)

# Compute the 2D Fourier Transform

fft_result = np.fft.fft2(data)

# Shift zero frequency components to the center
fft_result_shifted = np.fft.fftshift(fft_result)

# Compute the magnitude spectrum (absolute values)
magnitude_spectrum = np.abs(fft_result_shifted)

max_index = np.argmax(magnitude_spectrum)
max_indices = np.unravel_index(max_index, magnitude_spectrum.shape)
from scipy.interpolate import RegularGridInterpolator

def get_weighted_pos( data, axes ):
    max_index = np.argmax(data)
    indices = np.unravel_index(max_index, data.shape)
    
    edge_min_idx = [indices[0]-2, indices[1]-2]
    edge_max_idx = [indices[0]+2, indices[1]+2]

    partial_amp = data[edge_min_idx[0]:edge_max_idx[0]+1,edge_min_idx[1]:edge_max_idx[1]+1]
    f_z_t_range = axes[0][edge_min_idx[0]:edge_max_idx[0]+1]
    f_z_c_range = axes[1][edge_min_idx[1]:edge_max_idx[1]+1]
    f_z_t_range_new = np.linspace(f_z_t_range[0],f_z_t_range[-1],10)
    f_z_c_range_new = np.linspace(f_z_c_range[0],f_z_c_range[-1],10)
    print(partial_amp.shape, f_z_t_range.shape, f_z_c_range.shape)
    print(f_z_c_range)
    interp = RegularGridInterpolator((f_z_t_range, f_z_c_range), partial_amp, method="cubic",
                                     fill_value=None, bounds_error=False)
    print(f_z_t_range, f_z_t_range_new)
    tv, cv = np.meshgrid(f_z_t_range_new, f_z_c_range_new, indexing="ij")
    f_z_target_pos, f_z_crosstalk_pos = get_max_pos(interp((tv, cv)), [f_z_t_range_new, f_z_c_range_new])

    # tv, cv = np.meshgrid(f_z_t_range_new, f_z_c_range_new, indexing="ij")
    # print(f_z_t_range, f_z_c_range)
    # f_z_target_pos = np.average(tv, weights=partial_amp)
    # f_z_crosstalk_pos = np.average(cv, weights=partial_amp)

    # print(f_z_target_pos, f_z_crosstalk_pos)
    return f_z_target_pos, f_z_crosstalk_pos

def get_max_pos( data, axes ):

    max_index = np.argmax(data)
    max_indices = np.unravel_index(max_index, data.shape)
    f_z_target_pos = axes[0][max_indices[0]]
    f_z_crosstalk_pos = axes[1][max_indices[1]]
    print(max_indices)
    print("Maximum value:", data[max_indices])
    print(f"f_z_target: {axes[0][max_indices[0]]}")
    print(f"f_z_crosstalk: {axes[1][max_indices[1]]}")
    return f_z_target_pos, f_z_crosstalk_pos


get_max_pos(magnitude_spectrum, [f_z_target,f_z_crosstalk])
f_z_target_pos, f_z_crosstalk_pos = get_weighted_pos(magnitude_spectrum, [f_z_target,f_z_crosstalk] )
# f_z_target_pos, f_z_crosstalk_pos = get_max_pos(magnitude_spectrum)
z_slope = f_z_target_pos/f_z_crosstalk_pos
print(f"z_slope: {z_slope}")
# Display the original image and its Fourier Transform
plt.figure(figsize=(12, 6))

plt.subplot(121)
plt.pcolormesh(d_z_crosstalk_amp, d_z_target_amp, data, cmap='gray')
plt.plot([d_z_crosstalk_amp[0],d_z_crosstalk_amp[-1]],[-d_z_crosstalk_amp[0]/z_slope,-d_z_crosstalk_amp[-1]/z_slope])
plt.title('Original Image')

plt.subplot(122)
# plt.pcolormesh(f_z_crosstalk, f_z_target, np.log1p(magnitude_spectrum), cmap='gray')  # Use log scale for better visualization
plt.pcolormesh(f_z_crosstalk, f_z_target, magnitude_spectrum, cmap='gray')  # Use log scale for better visualization
plt.plot([-f_z_crosstalk_pos,f_z_crosstalk_pos],[-f_z_target_pos,f_z_target_pos])

plt.title('2D Fourier Transform (Magnitude Spectrum)')

plt.show()
