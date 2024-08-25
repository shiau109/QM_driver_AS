from qm.qua import *
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import xarray as xr
import numpy as np
from analysis.zline_crosstalk_analysis import analysis_crosstalk_value_fft, analysis_crosstalk_value_fitting
from qualang_tools.plot.fitting import Fit


def plot_crosstalk_2points(data):
    """
    Plot zline crosstalk data.
    
    Parameters:
    data (xarray.Dataset): Data in shape (M, 2)
        - M is the crosstalk z point.
        - 2 is the detector z point.
    """
    q = list(data.data_vars.keys())
    crosstalk_z = data.coords["crosstalk_z"].values
    detector_z = data.coords["detector_z"].values
    crosstalk_qubit = data.attrs["crosstalk_qubit"]
    detector_qubit = data.attrs["detector_qubit"]

    fig, ax = plt.subplots(2, 1)

    ax[0].plot(crosstalk_z, data[q][0, :, 0], color="red", linewidth=5)
    fit = Fit()
    ana_dict = fit.reflection_resonator_spectroscopy(crosstalk_z, data[q][0, :, 0], plot=False)
    freq_minus = ana_dict['f'][0]*1e3
    ax[0].set_titile(f"{detector_qubit}_ro")
    ax[0].set_xlabel(f"{crosstalk_qubit}_z Delta Voltage (mV)", fontsize=15)
    ax[0].set_ylabel(f"I", fontsize=15)

    ax[1].plot(crosstalk_z, data[q][0, :, 1], color="red", linewidth=5)
    fit = Fit()
    ana_dict = fit.reflection_resonator_spectroscopy(crosstalk_z, data[q][0, :, 1], plot=False)
    freq_plus = ana_dict['f'][0]*1e3
    ax[1].set_titile(f"{detector_qubit}_ro")
    ax[1].set_xlabel(f"{crosstalk_qubit}_z Delta Voltage (mV)", fontsize=15)
    ax[1].set_ylabel(f"I", fontsize=15)

    crosstalk=(freq_plus - freq_minus)/(detector_z[1] - detector_z[0])
    
    return crosstalk


def plot_crosstalk_3Dscalar(data):
    """
    Plot zline crosstalk data and return the figure and axis.

    Parameters:
    data (xarray.Dataset): Data in shape (M, N)
        - M is the crosstalk z point.
        - N is the detector z point.

    Returns:
    List of tuples (fig, ax, q): List of figure and axis objects along with the corresponding variable name.
    """
    q_list = list(data.data_vars.keys())
    crosstalk_z = data.coords["crosstalk_z"].values
    detector_z = data.coords["detector_z"].values
    crosstalk_qubit = data.attrs["crosstalk_qubit"]
    detector_qubit = data.attrs["detector_qubit"]
    expect_crosstalk = data.attrs["expect_crosstalk"]

    figures = []
    
    for q in q_list:
        fig, ax = plt.subplots()
        picture = ax.pcolormesh(crosstalk_z * 1e3, detector_z * 1e3, data[q][0, :, :].T, cmap='RdBu')

        ax.set_title(f"{q}", fontsize=15)
        ax.set_xlabel(f"{crosstalk_qubit}_z Delta Voltage (mV)", fontsize=15)
        ax.set_ylabel(f"{detector_qubit}_z Delta Voltage (mV)", fontsize=15)
        ax.set_aspect(1 / expect_crosstalk)

        # 添加 colorbar
        cbar = fig.colorbar(picture, ax=ax)
        cbar.set_label("Intensity", fontsize=15)
        cbar.ax.tick_params(labelsize=12)

        figures.append((fig, ax, q))

    return figures



def plot_analysis( data ):
    """
    Plot zline crosstalk data.
    
    Parameters:
    data (xarray.Dataset): Data in shape (M, N)
        - M is the crosstalk z point.
        - N is the detector z point.
    """
    fig, ax = plt.subplots(ncols=2)
    fig.set_size_inches(10, 5)

    # crosstalk, freq_axes, mag = analysis_crosstalk_value_fft( data )
    crosstalk, intercept = analysis_crosstalk_value_fitting( data )

    _plot_rawdata( data, crosstalk, ax[0] )

    # _plot_2Dfft( freq_axes[0], freq_axes[1], mag.transpose(), ax[1] )

def _plot_rawdata( dataset, slope, ax=None ):
    """
    x is crosstalk voltage (other)\n
    y is compensation voltage (self)
    """
    q = list(dataset.data_vars.keys())[0]
    x = dataset.coords["crosstalk_z"]
    y = dataset.coords["detector_z"]
    z = dataset[q][0, :, :].T
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



# Load the NetCDF file
file_path = r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240814_DR3_5Q4C_0430#7\compensation_test\20240825_2032_detector_q4_crosstalk_q1_long_drive_pulse_expectcrosstalk_0.05_20mius.nc"

dataset = xr.open_dataset(file_path)

# # Access data
# raw_data = dataset[list(dataset.data_vars)[0]].values  # Extract the q3_ro data
# other_info = {
#     'paras': {
#         'd_z_target_amp': dataset['detector_z'].values,
#         'd_z_crosstalk_amp': dataset['crosstalk_z'].values
#     }
# }

# # Process the data
# d_z_target_amp = other_info["paras"]["d_z_target_amp"]
# d_z_crosstalk_amp = other_info["paras"]["d_z_crosstalk_amp"]
# data = raw_data[0, :, :]  # Extract the first layer of the data for 'mixer' dimension

# # Ensure the shapes are as expected
# d_z_target_amp = d_z_target_amp[:]
# d_z_crosstalk_amp = d_z_crosstalk_amp[:]
# data = data[:, :]

# # Print the shapes to verify
# print(data.shape, d_z_target_amp.shape, d_z_crosstalk_amp.shape)

plot_analysis(dataset)

plt.show()








# import xarray as xr

# # 假設 ds1 和 ds2 是你已經讀取的 xarray Dataset
# ds1 = xr.open_dataset(r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240814_DR3_5Q4C_0430#7\raw_data\20240822_0128_detector_q4_crosstalk_q8_long_drive_pulse_expectcrosstalk_0.05_20mius.nc")  # 如果你從文件讀取資料集
# ds2 = xr.open_dataset(r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240814_DR3_5Q4C_0430#7\raw_data\20240822_0138_detector_q4_crosstalk_q8_long_drive_pulse_expectcrosstalk_0.05_20mius.nc")  # 如果你從文件讀取資料集

# # 複製 ds1 創建 ds3
# ds3 = ds1.copy()

# # 取出 q8_ro 變數
# q8_ro_ds1 = ds1['q4_ro']
# q8_ro_ds2 = ds2['q4_ro']

# # 在 mixer 維度上分別選取 'I' 和 'Q'，並進行相減操作
# q8_ro_diff_I = q8_ro_ds1.sel(mixer='I') - q8_ro_ds2.sel(mixer='I')
# q8_ro_diff_Q = q8_ro_ds1.sel(mixer='Q') - q8_ro_ds2.sel(mixer='Q')

# # 覆蓋 ds3 中的 'I' 和 'Q' 數據
# ds3['q4_ro'].loc[{'mixer': 'I'}] = q8_ro_diff_I
# ds3['q4_ro'].loc[{'mixer': 'Q'}] = q8_ro_diff_Q

# print(ds3)
# plot_analysis(ds3)
# plt.show()









# import xarray as xr
# data = xr.open_dataset(r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240719_DR3_5Q4C_0430#7\raw_data\20240730_1334_detector_q8_crosstalk_q3_long_drive_pulse_expectcrosstalk_1_20mius.nc")
# # 调用函数生成图像
# figures = plot_crosstalk_3Dscalar(data)

# # 保存每个图像
# for fig, ax, q in figures:
#     plt.figure(fig.number)  # 设置当前图形对象
#     plt.show()  # 显示图像