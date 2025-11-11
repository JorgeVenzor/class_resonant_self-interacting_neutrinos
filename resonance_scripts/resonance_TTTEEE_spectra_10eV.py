import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from classy import Class
from scipy.optimize import fsolve
from scipy.interpolate import interp1d
import math

#k_out = [0.1] # 1/Mpc
#
#m_NH =[0.02193372404432645, 0.023581523497277785, 0.05448475245839577]
gnu=[0, 1e-10, 1e-9, 1e-8]
# Cosmological parameters and other CLASS parameters, updated to Planck 2018, suma de masas 0.06eV

#filename="../resonance_interaction_10_eV.dat"

common_settings = {# we need to set the output field to something although
                   # the really releveant outpout here will be set with 'k_output_values'
                   'output':'mPk,tCl,pCl,lCl',
                   'P_k_max_1/Mpc':3.0,
                   # value of k we want to polot in [1/Mpc]
                   #'k_output_values': str(k_out).strip('[]'),
                   # LambdaCDM parameters
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
                # Take fixed value for primordial Helium (instead of automatic BBN adjustment)
                   'YHe': 0.2454006,
                   'gnu':str(gnu).strip('[]'),
                   'use_ncdm_nsi_files':1,
                   'ncdm_nsi_filenames':'tables_resonance/resonance_interaction_10_eV.dat',
                   'm_med_in_eV':10.0,
                   'ncdm_fluid_approximation':3,
                   'l_max_ncdm':16,
                   'YHe':0.25,
                   # other options and settings
                   'compute damping scale':'yes', # needed to output the time of damping scale crossing
                   'lensing':'yes',
                   'tol_ncdm':1.e-3, 
                   #'perturbations_integration_stepsize':10.,
                   'perturbations_sampling_stepsize':0.09,
                   'tol_perturbations_integration':1.0e-9,
                   'hyper_sampling_flat':10.0,
                   'evolver': 1,
                   'perturbations_verbose':2,
                    }
##############
#
# call CLASS
#
M = {}
all_k = {}
one_k = {}
background= {}
var_array = gnu
var_num = len(var_array)

# g_eff array values
for i, gnu in enumerate(var_array):
    print (' * Compute with %s=%e ' %('gnu', gnu))
    # call CLASS
    #
    M[i] = Class()
    M[i].set(common_settings)
    M[i].set({'gnu':gnu,'modes':'s,t'})
    M[i].compute()
    #load perturbations
    all_k[i]=M[i].get_perturbations()
    #one_k[i]=all_k[i]['scalar']
    background[i] = M[i].get_background()

    ###
#CMB lensed spectra    
cl_lens0= M[0].lensed_cl(2500)
cl_lens1= M[1].lensed_cl(2500)
cl_lens2= M[2].lensed_cl(2500)
cl_lens3= M[3].lensed_cl(2500)
# plotting
#################
#
fig, (D_ell, DeltaD, DeltaD2) = plt.subplots(3,sharex=True,figsize=(8,12))
fig.subplots_adjust(hspace=0)
plt.xlim([2,2510])
#
ell_l=cl_lens0['ell']
#Factor for units
factor_l = (2.726e6)*(2.726e6)*ell_l**2*ell_l*(ell_l+1)/2/np.pi
# D_ell suma de masas 0.06
D_ell.plot(ell_l,1e-9*factor_l*cl_lens0['tt'],lw ='2.', color='r',label=r'$\Lambda$CDM, $\Sigma m_{\nu}=0.06{\rm eV}$')
D_ell.plot(ell_l,1e-9*factor_l*cl_lens1['tt'],lw ='2.',color='indigo',label=r'$g_{\rm eff}=1x10^{-10}$, $\Sigma m_{\nu}=0.06{\rm eV}$')
D_ell.plot(ell_l,1e-9*factor_l*cl_lens2['tt'],lw ='2.',color='cyan',label=r'$g_{\rm eff}=5x10^{-9}$, $\Sigma m_{\nu}=0.06{\rm eV}$')
D_ell.plot(ell_l,1e-9*factor_l*cl_lens3['tt'],lw ='2.',color='salmon',label=r'$g_{\rm eff}=1x10^{-8}$, $\Sigma m_{\nu}=0.06{\rm eV}$')

### Delta D_ell, suma de masas 0.06
DeltaD.plot(ell_l,1e-8*factor_l*(cl_lens1['tt']-cl_lens0['tt']),lw ='2.', color='indigo')
DeltaD.plot(ell_l,1e-8*factor_l*(cl_lens2['tt']-cl_lens0['tt']),lw ='2.', color='cyan' )
DeltaD.plot(ell_l,1e-8*factor_l*(cl_lens3['tt']-cl_lens0['tt']),lw ='2.', color='salmon' )

## Delta D_ell/Delta_LCDM: LCDM es considerado con suma de masas 0.06
DeltaD2.plot(ell_l,(cl_lens1['tt']-cl_lens0['tt'])/cl_lens0['tt'],lw ='2.',color='indigo')
DeltaD2.plot(ell_l,(cl_lens2['tt']-cl_lens0['tt'])/cl_lens0['tt'],lw ='2.',color='cyan')
DeltaD2.plot(ell_l,(cl_lens3['tt']-cl_lens0['tt'])/cl_lens0['tt'],lw ='2.',color='salmon')

### Label options
D_ell.legend(title='m_med=10eV',fontsize='10',ncol=2)
#D_ell.set_xticks([ 500, 1000, 1500, 2000],["500", "1000", "1500", "2000"])
D_ell.tick_params(direction='in', top=True, right=True, labeltop=False,length=7,width=1.5)
D_ell.set_ylabel(r"$\ell^2 D_{\ell} [\mu K^2] \,\,\, (\times 10^{-9})$", fontsize=16)
D_ell.set_ylim([-0.495, 2.4])
D_ell.ticklabel_format(useMathText=True)
DeltaD.set_ylabel(r"$\Delta (\ell^2 D_{\ell}) [\mu K^2] \,\,\,(\times 10^{-8}) $", fontsize=16)
DeltaD.tick_params(direction='in', top=True, right=True, labeltop=False,length=7,width=1.5)
DeltaD.ticklabel_format(useMathText=True)
DeltaD2.set_ylabel(r"$\Delta  D_{\ell}/ D_{\ell}^{\Lambda\rm CDM}  \,\,\, $", fontsize=16)
DeltaD2.set_xlabel(r"$\ell  \,\,\, $", fontsize=16)
DeltaD2.tick_params(direction='in', top=True, right=True, labeltop=False,length=7,width=1.5)
#DeltaD2.legend()
plt.savefig('D_ell_TT_resonance_10eVprueba.png',bbox_inches='tight')

    
