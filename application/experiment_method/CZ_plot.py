import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from qualang_tools.plot import Fit
from matplotlib.ticker import MaxNLocator


def cos_fit(x, f, A, m, theta):
    return f+A*np.cos(m*x+theta)

def analysis_crosstalk_value_fitting(dataset):
    """
    z1 is shape (N,),  crosstalk voltage (other)
    z2 is shape (M,), compensation voltage (self)
    data with shape (N,M)
    """
    z1 = dataset.coords["amp_ratio"].values[:]#26:-18]
    z2 = dataset.coords["frequency"].values[:]
    data = dataset[0, :, :].values.T
    # z1 = dataset_q.coords["flux"].values
    # z2 = dataset_q.coords["frequency"].values
    # idata = dataset_q[0, :, :].values
    # qdata = dataset_q[1, :, :].values
    # data = -abs(idata+1j*qdata)
    # offset = np.mean(data)
    # data -= offset

    x_vals = []
    y_vals = []
    # 对每一条 crosstalk voltage 的数据进行处理
    min = np.min(data)
    max = np.max(data)
    for i in range(data.shape[1]):  # 迭代每一列 (对应不同的 crosstalk voltage)
        col_data = data[:, i]
        if((np.max(col_data)-min)>0.79*(max-min)):
            try:
                fit = Fit()
                res = fit.transmission_resonator_spectroscopy(z2 * 1e9, col_data, plot=False)
                # if(abs(res["f"][1]/res["f"][0])<0.001):
                y_vals.append(res["f"][0] * 1e-9)  # 取出对应的 detector voltage
                x_vals.append(z1[i])  # 取出当前的 crosstalk voltage

            except:
                pass
    # 估计初始值

    indices_to_remove = [19, -7]
    x_vals = np.delete(x_vals, indices_to_remove)
    y_vals = np.delete(y_vals, indices_to_remove)
    
    f0 = np.mean(y_vals)  # f 可以设为 y 的均值
    A0 = (np.max(y_vals) - np.min(y_vals)) / 2  # A 设为 y 值的半幅值
    m0 = 2 * np.pi / (np.max(x_vals) - np.min(x_vals))  # m 设为 2π/数据范围
    theta0 = 0  # 假设初始相位为 0
    try:
        popt, pcov = curve_fit(cos_fit, x_vals, y_vals, p0=[f0, A0, m0, theta0], maxfev=10000)
    except:
        popt = [0, 0, 0, 0]
    f, A, m, theta = popt

    print(f"f={f}\nA={A}\nm={m}\ntheta={theta}\n")

    # 返回拟合线的参数和数据点以便后续使用
    return x_vals, y_vals, f, A, m, theta

import xarray as xr
dataset = xr.open_dataset(r"C:\Users\admin\SynologyDrive\11 Papers\coupler_spectrum&flux_crosstalk\raw_figures\CZ\20241004_015740_CZ\q1q0_cz_couplerz.nc")
print(dataset)



# 獲取所有的 data_vars keys
data_vars = list(dataset.data_vars.keys())
figures = []

for q in data_vars:
    print(f"Processing {q}...")
    dataset_q = dataset[q]
    quantized_flux = 1  #m_q3 = 9.321026490217598, m_q4 = 9.555808516102724, T_q7 = 0.66, T_q8 = 0.69
    dataset_q = dataset_q.assign_coords(c_amps=dataset_q.coords["c_amps"].values * 0.2/0.64)
    dataset_q = dataset_q.assign_coords(amps=dataset_q.coords["amps"].values * 0.2/(2*np.pi/10.246057872281048))

    q = 'q3'
    c = 'c2'
    # x_vals, y_vals, f, A, m, theta = analysis_crosstalk_value_fitting(dataset_q)



    # 提取需要的數據
    z1 = dataset_q.coords["amps"].values[:]
    z2 = dataset_q.coords["c_amps"].values
    data = dataset_q[0, :, :].values
    # z1 = dataset_q.coords["flux"].values
    # z2 = dataset_q.coords["frequency"].values
    # idata = dataset_q[0, :, :].values
    # qdata = dataset_q[1, :, :].values
    # data = -abs(idata+1j*qdata)

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    from matplotlib.ticker import ScalarFormatter

    fig, ax = plt.subplots(figsize=(10, 8))  # 調整為正方形大小
    fig.subplots_adjust(left=0.2)  # 調整左邊的邊界

    pmesh = ax.pcolormesh(z1, z2, data, shading='auto', cmap='RdBu')

    # 設定正方形比例
    # ax.set_aspect('equal', adjustable='box')

    # 繪製擬合曲線
    # ax.scatter(x_vals, y_vals, color='black', linestyle='dashed')
    x_fit = np.linspace(min(z1), max(z1), 300)[1:-4]  
    # y_fit = cos_fit(x_fit, f, A, m, theta)
    # ax.plot(x_fit, y_fit, color='black', linestyle='dashed', linewidth=2)

    # 設定 X 軸和 Y 軸的刻度數量
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))  
    ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))  

    # 設置刻度標籤大小
    ax.tick_params(axis='both', which='major', labelsize=24)

    # 設置 colorbar
    cbar = fig.colorbar(pmesh, ax=ax)
    cbar.set_label(f"{q[0].upper()}$_{q[1]}$ RO", fontsize=24)  # 設定 colorbar 標籤及字體大小
    cbar.locator = ticker.MaxNLocator(nbins=5)
    cbar.ax.tick_params(labelsize=24)

    # 調整 colorbar 的 x10⁻⁵ 位置到正上方
    offset_text = cbar.ax.yaxis.get_offset_text()
    offset_text.set_fontsize(24)  # 設定字體大小
    offset_text.set_position((2.5, 1.05))  # 調整到 colorbar 上方

    # 設定 colorbar 為科學記號 `.2g` 格式
    formatter = ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((0, 0))  # 強制使用科學記號
    formatter.set_scientific(True)
    formatter.set_useOffset(False)  # 避免偏移顯示
    cbar.ax.yaxis.set_major_formatter(formatter)

    # 設定 colorbar 指數部分 (x10⁻⁴) 字體大小
    cbar.ax.yaxis.get_offset_text().set_fontsize(24)

    # 設定 X 軸和 Y 軸的標題
    ax.set_xlabel(f'Q$_4$ quantized flux', fontsize=28)
    ax.set_ylabel(f'{c[0].upper()}$_{c[1]}$ quantized flux', fontsize=28)

    # 設置標題
    ax.set_title(f'{q[0].upper()}$_{q[1]}$', fontsize=32)

    # 顯示網格
    ax.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()

    # 添加到 figures 列表
    figures.append((q, fig))


plt.show()

