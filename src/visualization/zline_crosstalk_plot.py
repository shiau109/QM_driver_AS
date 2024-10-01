from qm.qua import *
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import xarray as xr
import numpy as np
from analysis.zline_crosstalk_analysis import analysis_crosstalk_value_fft, analysis_crosstalk_value_fitting, analysis_crosstalk_ellipse

def plot_crosstalk_3Dscalar(dataset):
    """
    Plot zline crosstalk data and return the figure and axis.

    Parameters:
    data (xarray.Dataset): Data in shape (M, N)
        - M is the crosstalk z point.
        - N is the detector z point.

    Returns:
    List of tuples (fig, ax, q): List of figure and axis objects along with the corresponding variable name.
    """
    q_list = list(dataset.data_vars.keys())
    crosstalk_z = dataset.coords["crosstalk_z"].values
    detector_z = dataset.coords["detector_z"].values
    crosstalk_qubit = dataset.attrs["crosstalk_qubit"]
    detector_qubit = dataset.attrs["detector_qubit"]
    expect_crosstalk = dataset.attrs["expect_crosstalk"]

    figures = []
    
    for q in q_list:
        fig, ax = plt.subplots()
        picture = ax.pcolormesh(crosstalk_z * 1e3, detector_z * 1e3, dataset[q][0, :, :].T, cmap='RdBu')

        ax.set_title(f"{q}", fontsize=15)
        ax.set_xlabel(f"{crosstalk_qubit}_z Delta Voltage (mV)", fontsize=15)
        ax.set_ylabel(f"{detector_qubit}_z Delta Voltage (mV)", fontsize=15)
        ax.set_aspect(1 / expect_crosstalk)

        # 添加 colorbar
        cbar = fig.colorbar(picture, ax=ax)
        cbar.set_label("Intensity", fontsize=15)
        cbar.ax.tick_params(labelsize=12)

        figures.append((q, fig))

    return figures

def plot_analysis( data ):
    """
    Plot zline crosstalk data.
    
    Parameters:
    data (xarray.Dataset): Data in shape (M, N)
        - M is the crosstalk z point.
        - N is the detector z point.
    """
    if data.attrs["measure_method"] == "long_drive":
        figures = plot_crosstalk_fitting( data )
    else:
        figures = plot_crosstalk_FFT( data )

    return figures

def plot_crosstalk_fitting(dataset):
    """
    Plot zline crosstalk data.
    
    Parameters:
    data (xarray.Dataset): Data in shape (M, N)
        - M is the crosstalk z point.
        - N is the detector z point.
    
    Returns:
    List of tuples (fig, ax, q): List of figure and axis objects along with the corresponding variable name.
    """
    # 獲取所有的 data_vars keys
    data_vars = list(dataset.data_vars.keys())
    figures = []

    for q in data_vars:
        print(f"Processing {q}...")
        dataset_q = dataset[q]

        slope, intercept, x_vals, y_vals = analysis_crosstalk_value_fitting(dataset_q)

        if slope is None or intercept is None:
            print(f"Fitting failed for {q}")
            continue

        # 提取需要的數據
        z1 = dataset.coords["crosstalk_z"].values
        z2 = dataset.coords["detector_z"].values
        data = dataset_q[0, :, :].values.T

        # 繪製 colormesh 圖表
        fig, ax = plt.subplots(figsize=(10, 8))
        pmesh = ax.pcolormesh(z1, z2, data, shading='auto', cmap='RdBu')

        # 繪製最大值點
        ax.scatter(x_vals, y_vals, color='yellow', edgecolor='black', label='Max Points')

        # 計算並限制擬合線的範圍
        x_fit = np.linspace(min(z1), max(z1), 100)
        y_fit = slope * x_fit + intercept

        # 找到 y_fit 在 z2 範圍內的部分
        mask = (y_fit >= min(z2)) & (y_fit <= max(z2))
        x_fit = x_fit[mask]
        y_fit = y_fit[mask]

        ax.plot(x_fit, y_fit, color='black', linestyle='--', label=f'Fit: y = {slope:.3f} * x + {intercept:.3f}')

        # 圖表細節
        ax.set_title(f'{q}', fontsize=15)
        ax.set_xlabel(f'Crosstalk_z Voltage ({dataset.attrs["crosstalk_qubit"]})', fontsize=15)
        ax.set_ylabel(f'Detector_z Voltage ({dataset.attrs["detector_qubit"]})', fontsize=15)
        fig.colorbar(pmesh, ax=ax, label=q)
        ax.legend()
        ax.grid(True)

        # 添加到 figures 列表
        figures.append((q, fig))

    return figures


def plot_crosstalk_FFT(dataset):
    """
    Plot zline crosstalk data.
    
    Parameters:
    data (xarray.Dataset): Data in shape (M, N)
        - M is the crosstalk z point.
        - N is the detector z point.
    """
    # 獲取所有的 data_vars keys
    data_vars = list(dataset.data_vars.keys())
    figures = []

    for q in data_vars:
        fig, ax = plt.subplots(ncols=2)
        fig.set_size_inches(10, 5)
        print(f"Processing {q}...")
        dataset_q = dataset[q]
        crosstalk, freq_axes, mag = analysis_crosstalk_value_fft( dataset_q )

        _plot_rawdata( dataset_q, crosstalk, ax[0] )

        _plot_2Dfft( freq_axes[0], freq_axes[1], mag.transpose(), ax[1] )
        
        figures.append((q, fig))

    return figures

def _plot_rawdata( dataset, slope, ax=None ):
    """
    x is crosstalk voltage (other)\n
    y is compensation voltage (self)
    """
    x = dataset.coords["crosstalk_z"]
    y = dataset.coords["detector_z"]
    z = dataset[0, :, :].T
    ax.pcolormesh(x, y, z, cmap='RdBu')

    # 新增部分：設定 x 和 y 的範圍
    x_min, x_max = min(x), max(x)
    y_min, y_max = min(y), max(y)
    # 根據斜率和x, y的範圍計算斜線的實際起止點
    start_y = x_min * slope + y[len(y)//2]
    end_y = x_max * slope + y[len(y)//2]
    # 調整斜線的起止點以符合 x 和 y 的範圍
    if slope > 0.:
        if start_y < y_min:
            start_x = y_min / slope
            start_y = y_min
        else:
            start_x = x_min
        if end_y > y_max:
            end_x = y_max / slope
            end_y = y_max
        else:
            end_x = x_max
    else:
        if start_y > y_max:
            start_x = y_max / slope
            start_y = y_max
        else:
            start_x = x_min
        if end_y < y_min:
            end_x = y_min / slope
            end_y = y_min
        else:
            end_x = x_max
    # 繪制調整後的斜線
    ax.plot([start_x - y[len(y)//2]/slope, end_x - y[len(y)//2]/slope], [start_y, end_y], color="red", linewidth=5)


    # ax.plot([x[0],x[-1]],[ x[0]*slope + y[len(y)//2], x[-1]*slope + y[len(y)//2] ],color="r",linewidth=5)
    ax.set_title('Original Image')
    ax.set_xlabel(f"Crosstalk Delta Voltage (mV)")
    ax.set_ylabel(f"Compensation Delta Voltage (mV)")

def _plot_2Dfft( x, y, z, ax=None  ):
    """
    x is crosstalk voltage (other)\n
    y is compensation voltage (self)
    """
    # plt.pcolormesh(f_z_crosstalk, f_z_target, np.log1p(magnitude_spectrum), cmap='gray')  # Use log scale for better visualization
    ax.pcolormesh( x, y, z, cmap='gray')  # Use log scale for better visualization
    # ax.plot([-f_z_crosstalk_pos/1000,f_z_crosstalk_pos/1000],[-f_z_target_pos/1000,f_z_target_pos/1000],"o",color="r",markersize=5)
    # ax.plot([-f_z_crosstalk_pos/1000,f_z_crosstalk_pos/1000],[-f_z_target_pos/1000,f_z_target_pos/1000],color="r",linewidth=1)
    ax.set_xlabel(f"crosstalk wavenumber (1/mV)")
    # ax.set_ylabel(f"compensation wavenumber (1/mV)")
    ax.set_title('2D Fourier Transform (Magnitude Spectrum)')




def plot_heatmap_with_ellipse(dataset):
    # Get all data_vars keys
    data_vars = list(dataset.data_vars.keys())
    figures = []

    for q in data_vars:
        print(f"Processing {q}...")
        dataset_q = dataset[q][0, :, :].T

        edge_coords, ellipse_params = analysis_crosstalk_ellipse(dataset_q)

        if edge_coords is None or ellipse_params is None:
            print(f"Analysis failed for {q}")
            continue

        xc, yc, a, b, theta = ellipse_params
        z1 = dataset.coords["crosstalk_z"].values
        z2 = dataset.coords["detector_z"].values
        data = dataset_q

        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 8))
        pmesh = ax.pcolormesh(z1, z2, data, shading='auto', cmap='RdBu')

        # Plot edges
        edge_x_real = np.interp(edge_coords[:, 0], np.arange(data.shape[1]), z1)
        edge_y_real = np.interp(edge_coords[:, 1], np.arange(data.shape[0]), z2)
        ax.scatter(edge_x_real, edge_y_real, color='yellow', s=1, label='Edges')

        # Calculate ellipse boundary
        t = np.linspace(0, 2 * np.pi, 100)
        ellipse_x = a * np.cos(t)
        ellipse_y = b * np.sin(t)
        rot_x = ellipse_x * np.cos(theta) - ellipse_y * np.sin(theta) + xc
        rot_y = ellipse_x * np.sin(theta) + ellipse_y * np.cos(theta) + yc

        # Use interpolation to find the real positions
        rot_x_real = np.interp(rot_x, np.arange(data.shape[1]), z1)
        rot_y_real = np.interp(rot_y, np.arange(data.shape[0]), z2)
        ax.plot(rot_x_real, rot_y_real, 'g--', linewidth=2, label='Fitted Ellipse')

        # Ellipse major axis
        x_endpoints = np.array([a * np.cos(0) * np.cos(theta) - b * np.sin(0) * np.sin(theta) + xc, a * np.cos(np.pi) * np.cos(theta) - b * np.sin(np.pi) * np.sin(theta) + xc])
        y_endpoints = np.array([a * np.cos(0) * np.sin(theta) + b * np.sin(0) * np.cos(theta) + yc, a * np.cos(np.pi) * np.sin(theta) + b * np.sin(np.pi) * np.cos(theta) + yc])

        # Use interpolation to find the real endpoints
        x_endpoints_real = np.interp(x_endpoints, np.arange(data.shape[1]), z1)
        y_endpoints_real = np.interp(y_endpoints, np.arange(data.shape[0]), z2)

        # Plot major axis
        ax.plot(x_endpoints_real, y_endpoints_real, 'b-', linewidth=2, label='Major Axis')

        ax.set_title(f"{q}", fontsize=15)
        ax.set_xlabel(f'Crosstalk_z Delta Voltage ({dataset.attrs["crosstalk_qubit"]})', fontsize=15)
        ax.set_ylabel(f'Detector_z Delta Voltage ({dataset.attrs["detector_qubit"]})', fontsize=15)
        fig.colorbar(pmesh, ax=ax, label=q)
        ax.legend()
        ax.grid(True)

        # Calculate and display slope
        slope = np.tan(theta) * dataset.attrs["expect_crosstalk"]
        ax.text(0.05, 0.95, f"Slope: {slope:.3f}", transform=ax.transAxes, fontsize=12, verticalalignment='top')

        # Print slope
        print(f"Slope for {q}: {slope}")

        figures.append((fig, ax, q))

    return figures







# Load the NetCDF file
# file_path = r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240814_DR3_5Q4C_0430#7\good_20us\20240822_0128_detector_q4_crosstalk_q8_long_drive_pulse_expectcrosstalk_0.05_20mius.nc"

# dataset = xr.open_dataset(file_path)
# analysis_figures = plot_heatmap_with_ellipse(dataset)
# analysis_figures = plot_analysis(dataset)
# raw_figures = plot_crosstalk_3Dscalar(dataset)

# for fig, ax, q in raw_figures:
#     plt.figure(fig.number)  # 设置当前图形对象
#     plt.show()  # 显示图像

# for fig, ax, q in analysis_figures:
#     plt.figure(fig.number)  # 设置当前图形对象
#     plt.show()  # 显示图像




# crosstalk = np.array(
#     [[1., -0.09589142836056969],
#     [-0.039258310703576216, 1.]])
# cancel = np.linalg.inv(crosstalk)
# print(cancel)




# def plot_crosstalk_2points(data):
#     """
#     Plot zline crosstalk data.
    
#     Parameters:
#     data (xarray.Dataset): Data in shape (M, 2)
#         - M is the crosstalk z point.
#         - 2 is the detector z point.
#     """
#     q = list(data.data_vars.keys())
#     crosstalk_z = data.coords["crosstalk_z"].values
#     detector_z = data.coords["detector_z"].values
#     crosstalk_qubit = data.attrs["crosstalk_qubit"]
#     detector_qubit = data.attrs["detector_qubit"]

#     fig, ax = plt.subplots(2, 1)

#     ax[0].plot(crosstalk_z, data[q][0, :, 0], color="red", linewidth=5)
#     fit = Fit()
#     ana_dict = fit.reflection_resonator_spectroscopy(crosstalk_z, data[q][0, :, 0], plot=False)
#     freq_minus = ana_dict['f'][0]*1e3
#     ax[0].set_titile(f"{detector_qubit}_ro")
#     ax[0].set_xlabel(f"{crosstalk_qubit}_z Delta Voltage (mV)", fontsize=15)
#     ax[0].set_ylabel(f"I", fontsize=15)

#     ax[1].plot(crosstalk_z, data[q][0, :, 1], color="red", linewidth=5)
#     fit = Fit()
#     ana_dict = fit.reflection_resonator_spectroscopy(crosstalk_z, data[q][0, :, 1], plot=False)
#     freq_plus = ana_dict['f'][0]*1e3
#     ax[1].set_titile(f"{detector_qubit}_ro")
#     ax[1].set_xlabel(f"{crosstalk_qubit}_z Delta Voltage (mV)", fontsize=15)
#     ax[1].set_ylabel(f"I", fontsize=15)

#     crosstalk=(freq_plus - freq_minus)/(detector_z[1] - detector_z[0])
    
#     return crosstalk