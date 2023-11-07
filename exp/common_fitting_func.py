import numpy as np
import matplotlib.pyplot as plt

def gaussian(x, A, mu, sigma, offset):
    return A * np.exp(-(x - mu)**2 / (2 * sigma**2)) + offset

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


if __name__ == '__main__':
    ### Test S21_notch
    # x = np.linspace(-48e6,-44e6,5000)
    # print(type(S21_notch(x)))
    # plt.plot(x, S21_notch(x, -46.5e6, 9.0e+02, 1.0e+03, 0.0e+00, 0.035))
    # plt.show()
    ### Test resonator_flux
    x = np.linspace(-0.5,0.5,5000)
    plt.plot(x, resonator_flux(x, 2e6, 5, 2.5, -0.2, 5.734e9))

    # plt.plot(x, resonator_flux(x, 1.6e6,  4.93558591e+00, 3,  3.67462775e+01, -1.584e8))   
    plt.show()