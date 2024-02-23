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
    I1: np.ndarray
    I2: np.ndarray
    Q1: np.ndarray
    Q2: np.ndarray

    def __post_init__(self):
        self.data = xr.Dataset(
            data_vars={"state": (["average"], self.state),
                       "I1": (["average"], self.I1),
                       "I2": (["average"], self.I2),
                       "Q1": (["average"], self.Q1),
                       "Q2": (["average"], self.Q2),     
                       },
            coords={
                "average": range(self.num_averages),
            },
        )

    def plot_hist(self,count=None):
        plt.figure()
        self.data.state.plot.hist(xticks=range(4))
        plt.xticks(range(4), ['|00>', '|10>', '|01>', '|11>'])
        plt.tight_layout()
        if count != None:
            self.get_hist_value(count)
        
    def get_hist_value(self,count_list):
        hist_value = self.data.state.values
        value = 0
        for count in count_list:
            value += len(hist_value[hist_value==count])
        print(value)
        return value
        
