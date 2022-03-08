import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from classy import Class
from scipy.optimize import fsolve
from scipy.interpolate import interp1d
import math

k_out = [0.1] # 1/Mpc
#
#m_NH =[0.02193372404432645, 0.023581523497277785, 0.05448475245839577]
gnu=[0, 1e-10, 1e-12]
# Cosmological parameters and other CLASS parameters, updated to Planck 2018, suma de masas 0.06eV

filename='resonance_interaction_1_eV.dat'

common_settings = {# we need to set the output field to something although
                   # the really releveant outpout here will be set with 'k_output_values'
                   'output':'mPk,tCl,pCl,lCl',
                   'P_k_max_1/Mpc':3.0,
                   # value of k we want to polot in [1/Mpc]
                   'k_output_values': str(k_out).strip('[]'),
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
                   'use_ncdm_nsi_files':'1',
                   'ncdm_nsi_filenames':filename,
                   'ncdm_fluid_approximation':3,
                   'YHe':0.25,
                   # other options and settings
                   'compute damping scale':'yes', # needed to output the time of damping scale crossing
                   'lensing':'yes'
                    }
##############
#
# call CLASS
#
M2 = {}
all_k2 = {}
one_k2 = {}
background2 = {}
var_array = gnu
var_num = len(var_array)

# g_eff array values
for i, gnu in enumerate(var_array):
    print (' * Compute with %s=%e ' %('gnu', gnu))
    # call CLASS
    #
    M2[i] = Class()
    M2[i].set(common_settings)
    M2[i].set({'gnu':gnu,'modes':'s,t'})
    M2[i].compute()
    #load perturbations
    all_k2[i]=M2[i].get_perturbations()
    one_k2[i]=all_k2[i]['scalar']
    background[i] = M2[i].get_background()

    ###
