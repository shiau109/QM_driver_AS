from qm.qua import *
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def plot_crosstalk_3Dscalar( data ):
    """
    Plot zline crosstalk data.
    
    Parameters:
    data (xarray.Dataset): Data in shape (M, N)
        - M is the crosstalk z point.
        - N is the detector z point.
    """
    q = list(data.data_vars.keys())[0]
    crosstalk_z = data.coords["crosstalk_z"].values
    detector_z = data.coords["detector_z"].values
    crosstalk_qubit = data.attrs["crosstalk_qubit"]
    detector_qubit = data.attrs["detector_qubit"]
    expect_crosstalk = data.attrs["expect_crosstalk"]

    fig, ax = plt.subplots()
    picture = ax.pcolormesh( crosstalk_z*1e3, detector_z*1e3, data[q][0, :, :].T, cmap='RdBu')

    ax.set_xlabel(f"{crosstalk_qubit}_z Delta Voltage (mV)", fontsize=15)
    ax.set_ylabel(f"{detector_qubit}_z Delta Voltage (mV)", fontsize=15)
    ax.set_aspect(1/expect_crosstalk)

    # 添加 colorbar
    cbar = fig.colorbar(picture, ax=ax)
    cbar.set_label("Intensity", fontsize=15)
    cbar.ax.tick_params(labelsize=12)