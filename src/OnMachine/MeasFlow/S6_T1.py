
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

from datetime import datetime
import sys

from exp.relaxation_time import exp_relaxation_time
import numpy as np

from OnMachine.Octave_Config.QM_config_dynamic import Circuit_info, QM_config, initializer
from OnMachine.MeasFlow.ConfigBuildUp_old import spec_loca, config_loca, qubit_num
spec = Circuit_info(qubit_num)
config = QM_config()
spec.import_spec(spec_loca)
config.import_config(config_loca)

qmm,_ = spec.buildup_qmm()
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
init_macro = initializer( 100*u.us,mode='wait')

ro_elements = ['q1_ro']
q_name = ['q2_xy']
n_avg = 100

from exp.config_par import *

dataset = exp_relaxation_time( 20, 0.1, q_name, ro_elements, config.get_config(), qmm, n_avg=n_avg)





save_data = False
if save_data:
    from exp.save_data import save_nc
    import sys
    save_nc(r"D:\Data\DR2_5Q", "Q1_idle_Rabi", dataset) 