import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from qualang_tools.plot import Fit
import xarray as xr

def rotated_hyperbola(y, y0, a, b, c):
    """
    旋轉雙曲線的顯式形式
    x = (1/(y-y0) - b*y - c) / a
    """
    return (1/(y - y0) - b*y - c) / a

def analysis_crosstalk_value_fitting(dataset):
    """
    利用 dataset (xarray.DataArray) 中的資料進行擬合。
    假設 dataset 具有 "flux" (crosstalk 電壓) 與 "frequency" (檢測器頻率) 這兩個座標，
    並且數據第一個維度有 I 與 Q 兩個通道。
    
    傳入參數:
      dataset: xarray.DataArray
    
    回傳:
      fit_x (list): 擬合後的 crosstalk 電壓點
      fit_y (list): 擬合後的檢測器頻率點
      popt (list): 旋轉雙曲線擬合參數 [y0, a, b, c]
      coupling_strength: 從參數計算得到的耦合強度（依據原代碼的求解公式）
    """
    # # 提取 x 座標
    # x_coords = np.concatenate([dataset.coords["flux"].values[:12], dataset.coords["flux"].values[14:30]])
    # y_coords = dataset.coords["frequency"].values

    # # 提取對應的 I 和 Q 數據（沿著 axis=1 選擇）
    # i_data = np.concatenate([dataset[0, :, :12].values, dataset[0, :, 14:30].values], axis=1)
    # q_data = np.concatenate([dataset[1, :, :12].values, dataset[1, :, 14:30].values], axis=1)

    # # 計算 -|I + jQ|
    # data = -np.abs(i_data + 1j * q_data)


    # 提取座標
    x_coords = dataset.coords["amp_ratio"].values
    y_coords = dataset.coords["frequency"].values
    
    # 取得 I 與 Q 數據，並轉置使得每一行對應 y 軸
    i_data = dataset[0, :, :].values.T
    q_data = dataset[1, :, :].values.T
    data = np.abs(i_data + 1j*q_data)
    
    fit_x = []  # 儲存每一個 crosstalk 電壓點
    fit_y = []  # 儲存對應的檢測器頻率
    for i in range(data.shape[1]):
        col_data = data[:, i]
        try:
            fit_obj = Fit()
            res = fit_obj.transmission_resonator_spectroscopy(y_coords * 1e9, col_data, plot=False)
            # 將頻率單位轉回 GHz → Hz（或依需求轉換）
            fit_y.append(res["f"][0] * 1e-9)
            fit_x.append(x_coords[i])
        except Exception:
            continue

    # 利用 curve_fit 以擬合函數 rotated_hyperbola 擬合擷取的點 (x = f(y))
    try:
        popt, _ = curve_fit(rotated_hyperbola, fit_y, fit_x)
    except Exception:
        popt = [0, 0, 0, 0]
    
    # 依據擬合參數計算耦合強度（公式依原程式）
    y0, a, b, c = popt
    try:
        x_intersect = -(b*y0 + c) / a
    except:
        x_intersect = 0
    y_intersect = a*x_intersect + c
    if b != 0:
        discriminant = np.sqrt((y_intersect - b*y0)**2 - 4 * b * (-y0*y_intersect - 1))
        coupling_strength = discriminant / (2 * b)
    else:
        coupling_strength = 0
    print(f"Coupling strength = {coupling_strength}")
    
    return fit_x, fit_y, popt, coupling_strength

def clip_line_segment(m, k, x_min, x_max, y_min, y_max):
    """
    計算直線 y = m*x + k 與矩形 [x_min, x_max] x [y_min, y_max] 的交點，
    回傳交點組合 (兩個點) 作為繪製該直線在資料範圍內的線段。
    若交點數少於2則回傳 None。
    """
    candidates = []
    # 與左側垂直邊 (x=x_min) 的交點
    y_at_xmin = m * x_min + k
    if y_min <= y_at_xmin <= y_max:
        candidates.append((x_min, y_at_xmin))
    
    # 與右側垂直邊 (x=x_max) 的交點
    y_at_xmax = m * x_max + k
    if y_min <= y_at_xmax <= y_max:
        candidates.append((x_max, y_at_xmax))
    
    # 與底部水平邊 (y=y_min) 的交點
    if m != 0:
        x_at_ymin = (y_min - k) / m
        if x_min <= x_at_ymin <= x_max:
            candidates.append((x_at_ymin, y_min))
    # 與頂部水平邊 (y=y_max) 的交點
    if m != 0:
        x_at_ymax = (y_max - k) / m
        if x_min <= x_at_ymax <= x_max:
            candidates.append((x_at_ymax, y_max))
    
    # 移除重複點
    candidates = list(set(candidates))
    if len(candidates) < 2:
        return None
    # 按 x 座標排序後回傳最遠的兩點
    candidates.sort(key=lambda point: point[0])
    return candidates[0], candidates[-1]

def plot_clipped_line(ax, m, k, x_min, x_max, y_min, y_max, **plot_kwargs):
    """
    在軸 ax 上繪製直線 y = m*x + k，但僅限於矩形 [x_min, x_max] x [y_min, y_max] 的部分。
    """
    segment = clip_line_segment(m, k, x_min, x_max, y_min, y_max)
    if segment is not None:
        (x0, y0), (x1, y1) = segment
        ax.plot([x0, x1], [y0, y1], **plot_kwargs)

# 主程式
if __name__ == "__main__":
    # 載入資料集（請根據實際路徑調整）
    dataset = xr.open_dataset(r"C:\Users\admin\SynologyDrive\02 Data\Fridge Data\Qubit\20250112_125925_S4_flux_dep_Qubit_spectrum\S4_flux_dep_Qubit_spectrum.nc")
    print(dataset)
    dataset = dataset.assign_coords(amp_ratio=dataset.coords["amp_ratio"].values * dataset.attrs["z_amp_const"]+dataset.attrs["z_offset"])
    figures = []
    
    # 逐一處理 dataset 中的每個 data_var
    for var in reversed(list(dataset.data_vars.keys())):
        print(f"Processing {var}...")
        data_array = dataset[var]

        # 進行擬合，取得擬合點與旋轉雙曲線的參數，以及耦合強度
        fit_x, fit_y, popt, coupling_strength = analysis_crosstalk_value_fitting(data_array)
        
        # 提取繪圖用的座標與數據
        x_coords = data_array.coords["amp_ratio"].values   # x 軸: crosstalk 電壓
        y_coords = data_array.coords["frequency"].values     # y 軸: 檢測器頻率
        
        # 計算幅值：I 與 Q 的複數幅值
        i_data = data_array[0, :, :].values.T
        q_data = data_array[1, :, :].values.T
        amplitude = np.abs(i_data + 1j*q_data)
        
        # 取得資料範圍
        x_min, x_max = np.min(x_coords), np.max(x_coords)
        y_min, y_max = np.min(y_coords), np.max(y_coords)
        
        # 建立圖形
        fig, ax = plt.subplots(figsize=(10, 8))
        pmesh = ax.pcolormesh(x_coords, y_coords, amplitude, shading='auto', cmap='RdBu')
        fig.colorbar(pmesh, ax=ax, label=var)
        
        # 繪製擬合取得的數據點
        ax.scatter(fit_x, fit_y, color='yellow', edgecolor='black', zorder=5, label="Fit Points")
        
        # 繪製擬合的旋轉雙曲線
        # 根據 y 軸範圍產生 y 序列，並排除離奇異點 y0 (popt[0]) 太近的區域
        y0_fit = popt[0]
        y_vals = np.linspace(y_min, y_max, 300)
        epsilon = (y_max - y_min) * 1e-3
        y_vals = y_vals[np.abs(y_vals - y0_fit) > epsilon]
        x_vals = rotated_hyperbola(y_vals, *popt)
        
        # 過濾 x 值在資料範圍內的點
        valid_mask = (x_vals >= x_min) & (x_vals <= x_max) & np.isfinite(x_vals)
        # 為了處理中斷的情形，找出連續的區段來分段繪製
        indices = np.where(valid_mask)[0]
        if indices.size > 0:
            segments = np.split(indices, np.where(np.diff(indices) != 1)[0] + 1)
            for seg in segments:
                ax.plot(x_vals[seg], y_vals[seg], color='black', linestyle='dashed', linewidth=2, label="Fitted Hyperbola")
        
        # 繪製漸近線
        # 漸近線 1：水平線 y = y0 (僅當 y0 在 y 資料範圍內)
        if y_min <= y0_fit <= y_max:
            ax.plot([x_min, x_max], [y0_fit, y0_fit], color='black', linestyle='dashed', linewidth=2, label="Asymptote y = y0")
        
        # 漸近線 2：由 a*x + b*y + c = 0 得 y = (-a*x - c)/b (當 b != 0)
        a_param, b_param, c_param = popt[1], popt[2], popt[3]
        if b_param != 0:
            m_line = -a_param / b_param
            k_line = -c_param / b_param
            plot_clipped_line(ax, m_line, k_line, x_min, x_max, y_min, y_max,
                              color='black', linestyle='dashed', linewidth=2, label="Asymptote a*x+b*y+c=0")
        
        ax.set_xlabel("Flux (V)")
        ax.set_ylabel("Frequency (MHz)")
        ax.set_title(f"{var}\nCoupling Strength: {coupling_strength:.3g}")
        ax.grid(True)
        # ax.legend()
        
        figures.append((var, fig))
    
    plt.show()
