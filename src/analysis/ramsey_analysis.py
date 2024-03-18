"""
this file will work if 

from qualang_tools.plot.fitting import fit.ramsey

is added to file.
"""
import numpy as np
import scipy.optimize as sco
import matplotlib.pyplot as plt

def damping_osc( x, freq, tau ):
    return np.exp(-x/tau)*np.cos(freq*2*np.pi*x)


def straight_line(x, a, b):
    return a*x+b

def fit_straight_line(xdata, ydata):
    popt, pocv = sco.curve_fit(straight_line, xdata, ydata)
    return popt

if __name__ == '__main__':
    verbose = True
    f_points = 50
    f_range = np.linspace( 4.08, 4.11, f_points)
    decoherence_time = 2000
    evo_time = np.arange( 10, 6000, 4)
    f_q = 4.1

    fake_data = fake_ramsey( f_q, f_range, decoherence_time, evo_time, 0.1)
    print(fake_data.shape)
    a = []
    for i in range(fake_data.shape[0]):
        a.append(ramsey(evo_time, fake_data[i], verbose = True)["f"][0]*1000)
    print("---------------")
    popt1 = fit_straight_line(f_range[0:5], np.array(a)[0:5])
    popt2 = fit_straight_line(f_range[-6:-1], np.array(a)[-6:-1])
    qubit_frequency = (popt2[1]-popt1[1])/(popt1[0]-popt2[0])
    print(qubit_frequency)
    plt.plot(f_range, np.array(a))
    #plt.plot(evo_time, damping_osc(evo_time, *fit_decoherence_time[0]))
    #plt.pcolor(f_range, evo_time, fake_data.transpose())
    plt.show()