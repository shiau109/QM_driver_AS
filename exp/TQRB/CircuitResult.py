import dataclasses
from scipy.optimize import curve_fit
import numpy as np
import xarray as xr
from matplotlib import pyplot as plt

def power_law(m, a, b, p):
    return a * (p**m) + b

@dataclasses.dataclass
class CircuitResult:
    num_averages: int
    state: np.ndarray

    def __post_init__(self):
        self.data = xr.Dataset(
            data_vars={"state": (["average"], self.state)},
            coords={
                "average": range(self.num_averages),
            },
        )

    def plot_hist(self,count=None):
        plt.figure()
        self.data.state.plot.hist(xticks=range(4))
        plt.tight_layout()
        if count != None:
            self.get_hist_value(count)
        
    def get_hist_value(self,count):
        hist_value = self.data.state.values
        hist_value = len(hist_value[hist_value==count])
        print(hist_value)
        return hist_value
        
