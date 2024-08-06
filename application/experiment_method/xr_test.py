import numpy as np
import matplotlib.pyplot as plt
import xarray as xr


dataset = xr.open_dataset(r"C:\Users\arthu\20240723_1116_q1_xy_EchoT2.nc")
print(dataset)