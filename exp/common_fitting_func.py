import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

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




if __name__ == '__main__':
    ### Test S21_notch
    # x = np.linspace(-48e6,-44e6,5000)
    # print(type(S21_notch(x)))
    # plt.plot(x, S21_notch(x, -46.5e6, 9.0e+02, 1.0e+03, 0.0e+00, 0.035))
    # plt.show()
    ### Test resonator_flux
    x = np.linspace(-0.5,0.5,5000)
    # plt.plot(x, resonator_flux(x, 2e6, 5, 2.5, -0.2, 5.734e9))
    flux = np.arange(-0.5, 0.5, 0.001)
    # plt.plot(x, resonator_flux(x, 1.6e6,  4.93558591e+00, 3,  3.67462775e+01, -1.584e8))   
    # plt.show()
    v_period = 0.72
    max_freq = 3.5235
    max_flux = -3.300e-01
    idle_freq = 3.35
    idle_flux = 0.16
    Ec = 0.2
    plt.plot(flux,flux_qubit_spec(flux,v_period=0.7,max_freq=(3.5235e9),max_flux=0.004,idle_freq=(3.2252e9),idle_flux=0.146,Ec=0.2e9))
    plt.show()