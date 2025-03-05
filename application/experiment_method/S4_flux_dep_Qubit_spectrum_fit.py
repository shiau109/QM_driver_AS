import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from qualang_tools.plot import Fit

def cos_fit(x, f, A, m, theta):
    return f+A*np.cos(m*x+theta)

def rotated_hyperbola(x, x0, y0, a, b, theta):
    """旋转双曲线的显式形式"""
    y_prime = x0+np.sqrt(a**2 + (b**2 * (x - x0)**2) / a**2)
    y_rot = y0 + np.sin(theta) * y_prime
    return y_rot

def analysis_crosstalk_value_fitting(dataset):
    """
    z1 is shape (N,),  crosstalk voltage (other)
    z2 is shape (M,), compensation voltage (self)
    data with shape (N,M)
    """
    z1 = dataset.coords["flux"].values[:25]
    z2 = dataset.coords["frequency"].values[:]
    # data = dataset[0, :, :].values.T
    idata = dataset_q[0, :, :25].values
    qdata = dataset_q[1, :, :25].values
    data = -abs(idata+1j*qdata)
    # offset = np.mean(data)
    # data -= offset

    x_vals = []
    y_vals = []
    # 对每一条 crosstalk voltage 的数据进行处理
    for i in range(data.shape[1]):  # 迭代每一列 (对应不同的 crosstalk voltage)
        col_data = data[:, i]
        try:
            fit = Fit()
            res = fit.transmission_resonator_spectroscopy(z2 * 1e9, col_data, plot=False)
            y_vals.append(res["f"][0] * 1e-9)  # 取出对应的 detector voltage
            x_vals.append(z1[i])  # 取出当前的 crosstalk voltage
        except:
            pass
    # 估计初始值
    # f0 = np.mean(y_vals)  # f 可以设为 y 的均值
    # A0 = (np.max(y_vals) - np.min(y_vals)) / 2  # A 设为 y 值的半幅值
    # m0 = 2 * np.pi / (np.max(x_vals) - np.min(x_vals))  # m 设为 2π/数据范围
    # theta0 = 0  # 假设初始相位为 0
    # popt, pcov = curve_fit(cos_fit, x_vals, y_vals, p0=[f0, A0, m0, theta0])
    # f, A, m, theta = popt

    # print(f"f={f}\nA={A}\nm={m}\ntheta={theta}\n")
    p0 = [-0.3, 1.2, 1, 1, np.pi/2]
    try:
        popt, pcov = curve_fit(rotated_hyperbola, x_vals, y_vals, p0=p0)
    except:
        pass
    print(f"x0={p0[0]}\ny0={p0[1]}\na={p0[2]}\nb={p0[3]}\ntheta={p0[4]}\n")

    # 返回拟合线的参数和数据点以便后续使用
    return x_vals, y_vals, p0#, f, A, m, theta

import xarray as xr
dataset = xr.open_dataset(r"C:\Users\admin\SynologyDrive\02 Data\Fridge Data\Qubit\20241107_DR3_5Q4C_0430#7\save_data\g_qr\20241114_171612_Find_Flux_Period\Find_Flux_Period.nc")
folder_label = "S4_flux_dep_Qubit_spectrum" #your data and plots will be saved under a new folder with this name
# from exp.save_data import DataPackager
# save_dir = link_config["path"]["output_root"]
# dp = DataPackager( save_dir, folder_label )
# #Save data
# dp.save_config(config)
# dp.save_nc(dataset,folder_label)

# # Plot
# save_figure = 1
print(dataset)
# from exp.plotting import PainterFluxDepQubit
# painter = PainterFluxDepQubit()
# figs = painter.plot(dataset,folder_label)
# if save_figure: dp.save_figs( figs )


from visualization.zline_crosstalk_plot import plot_crosstalk_fitting

# 獲取所有的 data_vars keys
data_vars = list(dataset.data_vars.keys())
figures = []

for q in data_vars:
    print(f"Processing {q}...")
    dataset_q = dataset[q]
    quantized_flux = 1  #q3, q4, q7, q8
    # dataset_q = dataset_q.assign_coords(amp_ratio=dataset_q.coords["amp_ratio"].values * dataset.attrs["z_amp_const"])/quantized_flux

    # x_vals, y_vals, f, A, m, theta = analysis_crosstalk_value_fitting(dataset_q)
    x_vals, y_vals, p0 = analysis_crosstalk_value_fitting(dataset_q)



    # 提取需要的數據
    z1 = dataset_q.coords["flux"].values
    z2 = dataset_q.coords["frequency"].values
    # data = dataset_q[0, :, :].values.T
    idata = dataset_q[0, :, :].values
    qdata = dataset_q[1, :, :].values
    data = abs(idata+1j*qdata)
    # 繪製 colormesh 圖表
    fig, ax = plt.subplots(figsize=(10, 8))
    pmesh = ax.pcolormesh(z1, z2, data, shading='auto', cmap='RdBu')

    # 繪製最大值點
    ax.scatter(x_vals, y_vals, color='yellow', edgecolor='black')
    x_fit = np.linspace(min(x_vals), max(x_vals), 300)[1:]  # 生成平滑的 x 轴数据
    # # x_fit = np.linspace(-0.7, 0.7, 300)[1:]  # 生成平滑的 x 轴数据
    # y_fit = cos_fit(x_fit, f, A, m, theta)
    y_fit = rotated_hyperbola(x_fit, p0[0], p0[1] ,p0[2], p0[3], p0[4])
    ax.plot(x_fit, y_fit, color='black', linestyle='dashed', linewidth=2)

    # # 計算並限制擬合線的範圍
    # x_fit = np.linspace(min(z1), max(z1), 100)
    # y_fit = slope * x_fit + intercept

    # # 找到 y_fit 在 z2 範圍內的部分
    # mask = (y_fit >= min(z2)) & (y_fit <= max(z2))
    # x_fit = x_fit[mask]
    # y_fit = y_fit[mask]

    # ax.plot(x_fit, y_fit, color='black', linestyle='--', label=f'Fit: y = {slope:.3f} * x + {intercept:.3f}')

    # # 圖表細節
    # ax.set_title(f'{q}\ncrosstalk:{-1*slope}', fontsize=15)
    # ax.set_xlabel(f'Crosstalk_z Voltage ({dataset.attrs["crosstalk_qubit"]})', fontsize=15)
    # ax.set_ylabel(f'Detector_z Voltage ({dataset.attrs["detector_qubit"]})', fontsize=15)
    fig.colorbar(pmesh, ax=ax, label=q)
    ax.grid(True)

    # 添加到 figures 列表
    figures.append((q, fig))
plt.show()

