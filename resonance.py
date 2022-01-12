import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy import special
from scipy.integrate import odeint
from scipy.integrate import quad
from scipy.optimize import curve_fit
from scipy.optimize import minimize
from scipy import interpolate
import xlrd
from scipy.interpolate import splev, splrep, interp1d
from astropy import constants as const
from scipy import optimize as op
import scipy.integrate as spi
import scipy.stats as statspy
import scipy.signal
from decimal import Decimal
def fmt(xp, pos):
    a, b = '{:.0e}'.format(xp).split('e')
    b = int(b)
    return r'${} \times 10^{{{}}}$'.format(a, b)
def fmt_2(xp):
    T_photon0=kb*Tgamma0
    V=(xp+1)*T_photon0
    a, b = '{:.0e}'.format(V).split('e')
    b = int(b)
    return r'$10^{{{}}}$'.format(b)

hbar =6.5821e-16 # (eV*s)
c=3e8 #(m/s)
NA=6.02214076e23 #Avogadro's number
kb =8.6173e-05 #(eV/K)
mb = 0.9382e09 # baryon mass in eV (proton mass)
m_e=0.501e6 #electron mass in eV
rho0crit= 7.9092e-11 #the critical density is this value multiplied by h^2
Tgamma0=2.7255 # in Kelvin

def neutrino_number_density(T):
    """
    The neutrino number density in the units of T
    """
    number= (6*scipy.special.zeta(3)*T**3)/(4*np.pi**2.)
    return number

def G_integration(x,s,T):
    """
    Function to be integrated to obtain the function F(s,T)
    """
    A=np.sqrt(x**2-s/T**2)
    up_arg=1+np.exp((-1/2)*(x+A))
    down_arg=1+np.exp((-1/2)*(x-A))
    arg=up_arg/down_arg
    func=np.exp(-x)*(A+np.log(arg))/(1-np.exp(-x))
    return func

def F_vassh(s,T):
    """
    F(s,T)
    """
    integral = quad(G_integration,np.sqrt(s)/T,np.inf,args=(s,T))[0]
    return integral

def thermal_narrow(g,mphi,T):
    """
    This is the thermal average <sigma v_MOL> when the width of the Breit-Wigner goes to zero.
    (Dirac's delta approximation)
    """
    above= 4*np.pi**3*T**2*g**2*mphi**2
    below= (2*np.pi)**6*neutrino_number_density(T)**2
    res= above*F_vassh(mphi**2,T)/below
    return res

def interaction_rate(g,mphi,T):
    """
    Interaction rate Gamma(z)
    """
    Gamma=thermal_narrow(g,mphi,T)*neutrino_number_density(T)
    return Gamma

def plot_interaction_rate(g,save,zmin,zmax):
    z=np.logspace(np.log10(zmax),np.log10(zmin),100)
    T=Tgamma0*kb*(1.+z)
    y1=np.zeros(T.size)
    y2=np.zeros(T.size)
    y3=np.zeros(T.size)
    for i in range (T.size):
        y1[i]=interaction_rate(g,1e-1,T[i])
        y2[i]=interaction_rate(g,1.,T[i])
        y3[i]=interaction_rate(g,1e1,T[i])
    print (z,y1,y2,y3)
    plt.plot(z,y1,label=r'$m_{\phi}=0.1$ eV')
    plt.plot(z,y2,label=r'$m_{\phi}=1$ eV')
    plt.plot(z,y3,label=r'$m_{\phi}=10$ eV')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(zmax,zmin)
    plt.ylim(1e-25,1e-5)
    plt.legend()
    plt.xlabel(r'z',size=14)
    plt.ylabel(r'$\Gamma_{\mathrm{res}}$ [eV]',size=14)
    plt.tick_params(which='major',axis='both',direction='in',right=True,top=True,
                    length=7,width=1.5)
    plt.tick_params(which='minor',axis='both',direction='in',right=True,top=True,
                    length=4,width=1)
    if save:
        plt.savefig('interaction_rate_hy.pdf')
        plt.close('all')
    return 0


def save_data_files(save,mphi,zmin,zmax,name,g=1):
    """
    save a
    """
    name=str(name)
    z=np.logspace(np.log10(zmin),np.log10(zmax),20)
    logz=np.log10(z)
    T=Tgamma0*kb*(1.+z)
    y=np.zeros(T.size)
    for i in range (T.size):
        y[i]=interaction_rate(g,mphi,T[i])
    loginteraction=np.log10(y)
    array=np.column_stack((logz,loginteraction))
    if save:
        np.savetxt(name,array)
    return 0
