# Importing packages for plotting
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from classy import Class
from scipy.optimize import fsolve
from scipy.interpolate import interp1d
import math

#
gnu=[0, 1e-10, 1e-11] # Array of coupling constant values.

# Cosmological parameters and other CLASS parameters, updated to Planck 2018
# Sum of netrino masses fixed to 0.06eV
common_settings = {
                   'output':'mPk,tCl,pCl,lCl', 
                   'P_k_max_1/Mpc':3.0,
                   # LCDM parameter parameter values
                   'h':0.6732117,
                   'omega_b':0.02238280,
                   'omega_cdm':0.1201075,
                   'A_s':2.100549e-09 ,
                   'n_s':0.9660499,
                   'tau_reio':0.05430842,
                   'N_ur':0.00641,
                   'N_ncdm':1,
                   'deg_ncdm':3,
                   'm_ncdm': 0.02,
                   #Take fixed value for primordial Helium (instead of automatic BBN adjustment)
                   'YHe': 0.2454006,
                   'gnu':str(gnu).strip('[]'), #Read the array of NSI couplings
                   'use_ncdm_nsi_files':1,     #Option for loading resonance_tables
                   'ncdm_fluid_approximation':3,
                   'YHe':0.25,
                   # other options and settings
                   'compute damping scale':'yes', # needed to output the time of damping scale crossing
                   'lensing':'yes',
                   'tol_ncdm':1.e-3, 
                   'perturbations_sampling_stepsize':0.005,
                   'tol_perturbations_integration':1.0e-7,
                   'perturbations_verbose':1,
                    }
##############
#
# Define arrays for outputs
#
var_array = gnu
var_num = len(var_array)

M = {}
all_k = {}
background= {}
##
M2 = {}
all_k2 = {}
background2= {}
##
M3 = {}
all_k3 = {}
background3= {}
##
M1 = {}
all_k1 = {}
background1= {}
##
M0 = {}
all_k0 = {}
background0= {}

for i, gnu in enumerate(var_array):
    print (' * Compute with %s=%e ' %('gnu', gnu))
    # call CLASS for different mediator masses and gnu
    #
    ### masa del mediador 0.01 eV   
    M0[i] = Class()
    M0[i].set(common_settings)
    M0[i].set({'ncdm_nsi_filenames':'tables_Gamma_resonance/resonance_interaction_10minus2_eV.dat', 'm_med_in_eV':0.01})
    M0[i].set({'gnu':gnu,'modes':'s,t'})
    M0[i].compute()
    #load perturbations
    all_k0[i]=M0[i].get_perturbations()
    background0[i] = M0[i].get_background()
    ### mediator mass = 0.1 eV  
    M1[i] = Class()
    M1[i].set(common_settings)
    M1[i].set({'ncdm_nsi_filenames':'tables_Gamma_resonance/resonance_interaction_10minus1_eV.dat', 'm_med_in_eV':0.1})
    M1[i].set({'gnu':gnu,'modes':'s,t'})
    M1[i].compute()
    #load perturbations
    all_k1[i]=M1[i].get_perturbations()
    background1[i] = M1[i].get_background()
    ### mediator mass = 1eV  
    M[i] = Class()
    M[i].set(common_settings)
    M[i].set({'ncdm_nsi_filenames':'tables_Gamma_resonance/resonance_interaction_1_eV.dat', 'm_med_in_eV':1.0})
    M[i].set({'gnu':gnu,'modes':'s,t'})
    M[i].compute()
    #load perturbations
    all_k[i] = M[i].get_perturbations()
    background[i] = M[i].get_background()
    ### mediator mass 10 eV 
    M2[i] = Class()
    M2[i].set(common_settings)
    M2[i].set({'ncdm_nsi_filenames':'tables_Gamma_resonance/resonance_interaction_10_eV.dat', 'm_med_in_eV':10.0})
    M2[i].set({'gnu':gnu,'modes':'s,t'})
    M2[i].compute()
    #load perturbations
    all_k2[i]=M2[i].get_perturbations()
    background2[i] = M2[i].get_background()
    ###### mediator mass 100eV    
    M3[i] = Class()
    M3[i].set(common_settings)
    M3[i].set({'ncdm_nsi_filenames':'tables_Gamma_resonance/resonance_interaction_100_eV.dat', 'm_med_in_eV':100.0})
    M3[i].set({'gnu':gnu,'modes':'s,t'})
    M3[i].compute()
    #load perturbations
    all_k3[i]=M3[i].get_perturbations()
    background3[i] = M3[i].get_background()
    ###
##

background_tau = background[2]['conf. time [Mpc]'] # read confromal times in background table
background_z = background[2]['z'] # read redshift
quantities = M[2].get_current_derived_parameters(['tau_rec'])
# print times.viewkeys()
tau_rec = quantities['tau_rec']
z_at_tau = interp1d(background_tau,background_z)
z_rec=z_at_tau(tau_rec)
#
background_tau0 = background0[2]['conf. time [Mpc]'] # read confromal times in background table
background_z0 = background0[2]['z'] # read redshift
quantities0 = M0[2].get_current_derived_parameters(['tau_rec'])
# print times.viewkeys()
tau_rec0 = quantities0['tau_rec']
z_at_tau0 = interp1d(background_tau0,background_z0)
z_rec0=z_at_tau0(tau_rec0)

##
factor= 1.57e29 # Conversion of units
plt.loglog(background0[2]['z'],factor*background0[2]['(.)Gamma_of_z']/background0[2]['H [1/Mpc]'],color='#e2c1f3',lw ='2.', label=r'$m_{\varphi}=0.01{\rm eV}$')
plt.loglog(background1[2]['z'],factor*background1[2]['(.)Gamma_of_z']/background1[2]['H [1/Mpc]'],color='#00c69e',lw ='2.', label=r'$m_{\varphi}=0.1{\rm eV}$')
plt.loglog(background[2]['z'],factor*background[2]['(.)Gamma_of_z']/background[2]['H [1/Mpc]'],color='#fe51b0',lw ='2.', label=r'$m_{\varphi}=1{\rm eV}$')
plt.loglog(background2[2]['z'],factor*background2[2]['(.)Gamma_of_z']/background2[2]['H [1/Mpc]'],color='#07bdff',lw ='2.', label=r'$m_{\varphi}=10{\rm eV}$')
plt.loglog(background3[2]['z'],factor*background3[2]['(.)Gamma_of_z']/background3[2]['H [1/Mpc]'],color='#fd7a39',lw ='2.', label=r'$m_{\varphi}=100{\rm eV}$')
plt.loglog(background3[2]['z'],background3[2]['H [1/Mpc]']/background3[2]['H [1/Mpc]'],color='#9b9b9b',lw ='1.')
plt.plot((z_rec, z_rec), (0.5e-11, 1e6), scaley = False,color='#9b9b9b',lw ='1.', linestyle='--' )
#plt.plot((z_rec0, z_rec0), (0.5e-11, 13150), scaley = False)
plt.text(1099,7.3e4 , r'$z_{\rm rec}$')
plt.xlim([0.006, 9e9])
plt.ylim([1.19e-6,5e5])
plt.xlabel(r"$z$", fontsize=16)
plt.ylabel(r"$\Gamma/H$", fontsize=16)
plt.legend(title='$g_{\\nu}=1x10^{-11}$',ncol=1, loc='upper right')

plt.savefig('resonance_scripts/Plots/gamma_overH.png',bbox_inches='tight')

    
    
