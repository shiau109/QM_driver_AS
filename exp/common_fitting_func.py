import numpy as np
from scipy.stats import norm
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from exp.configuration import *

def gaussian(x, mu, sigma):
    return norm.pdf(x, mu, sigma)

def S21_notch(f,fr=1e9,Ql=900,Qc=1000.,phi=0.,a=1.):
    '''
    full model for notch type resonances
    '''
    return a*(1.-Ql/Qc*np.exp(1j*phi)/(1.+2j*Ql*(f-fr)/fr))

def S21_notch_real(f,fr=1e9,Ql=900,Qc=1000.,phi=0.,a=1.):
    return np.real(S21_notch(f,fr,Ql,Qc,phi,a))

def S21_notch_imag(f,fr=1e9,Ql=900,Qc=1000.,phi=0.,a=1.):
    return np.imag(S21_notch(f,fr,Ql,Qc,phi,a))

def resonator_flux(flux, IF_max, coeff, gamma, flux_offset, offset_ROF ):
    d = (gamma-1)/(gamma+1)
    phai = (flux + flux_offset) * coeff
    return IF_max * np.sqrt(np.cos(phai)**2 + d**2 * np.sin(phai)**2) + offset_ROF

def flux_qubit_spec(flux,v_period,max_freq,max_flux,idle_freq,idle_flux,Ec):
    v_offset = max_flux
    A_idle = np.cos(((idle_flux-v_offset)/v_period)*np.pi)**2
    E_Jsum = (max_freq+Ec)**2/(8*Ec)
    d = (((idle_freq+Ec)**2/(8*Ec*E_Jsum))**2-A_idle)/(1-A_idle)
    A = np.cos(((flux-v_offset)/v_period)*np.pi)**2
    freq = np.sqrt(8*E_Jsum*np.sqrt(A+(1-A)*d)*Ec)-Ec
    return freq

def flux_qubit_spec_with_d(flux,v_period,max_freq,max_flux,Ec,d):
    v_offset = max_flux
    E_Jsum = (max_freq+Ec)**2/(8*Ec)
    A = np.cos(((flux-v_offset)/v_period)*np.pi)**2
    freq = np.sqrt(8*E_Jsum*np.sqrt(A+(1-A)*d)*Ec)-Ec
    return freq

def cosine_func(x, amplitude, frequency, phase, offset):
    return amplitude * np.cos(2 * np.pi * frequency * x + phase) + offset


if __name__ == '__main__':
    ### Test S21_notch
    # x = np.linspace(-48e6,-44e6,5000)
    # print(type(S21_notch(x)))
    # plt.plot(x, S21_notch(x, -46.5e6, 9.0e+02, 1.0e+03, 0.0e+00, 0.035))
    # plt.show()

    ### Test resonator_flux
    Qi = 3
    flux = np.arange(-0.5, 0.5, 0.001)
    res_F = resonator_flux(-3.100e-01+0.14, *p1[Qi-1])
    res_IF = (res_F - resonator_LO)/1e6
    res_IF = int(res_IF * u.MHz)
    res_IF_cos = cosine_func(flux, 0.4045e6, 1.5, 3, 5.8464515e9)
    print(res_IF)
    plt.plot(flux, resonator_flux(flux, 2.22397609e+06, 4.47370446e+00, 2.20718217e-01, 3.12854012e-01, 5.84462834e+09))   
    plt.plot(flux, res_IF_cos)
    plt.show()

    ##################### Qubit spec ############################ 

    # flux = np.arange(-0.5, 0.5, 0.001)
    # plt.plot(flux,flux_qubit_spec(flux,v_period=0.72,max_freq=(3.8497e9),max_flux=-0.0204,idle_freq=(3.6507e9),idle_flux=0.0917,Ec=0.196e9))
    # plt.show()
    # target_value = 3.724653e9
    # initial_guess = 0.1
    # solution = fsolve(
    #     lambda x: flux_qubit_spec(x, v_period=0.72,max_freq=(3.8497e9),max_flux=-0.0204,idle_freq=(3.6507e9),idle_flux=0.0917,Ec=0.196e9)
    #                    - target_value, initial_guess)

    # print(f"The solution to f(x) = {target_value} is x = {solution[0]}")
    # # Q3
    # The solution to f(x) = 3193100000.0 is x = 0.15361442261694103
    # # Q4  
    # The solution to f(x) = 3724653000.0 is x = 0.06834788688427282