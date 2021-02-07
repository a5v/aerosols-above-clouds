#!/usr/bin/env python
"""
Test of the Python wrapper to the DISORT library

Module '_disort' is auto-generated with f2py (version:2).
"""

import numpy as np
#import matplotlib
import disort
import pandas as pd
import atmfunc


##########################################################################################################

if __name__ == '__main__':

    # read Rayleigh optical thickness for 325.8 nm [Ozone fitting window]
    xy     = np.loadtxt('../test/rayleigh_layer_opd.txt')
    #dTau   = xy[::-1,1]  # FROM TOP TO BOTTOM
    #dTau = np.ones(49)


    ##read in data file
    df = pd.read_csv('./reformat_ecmwf_atm/ecmwf_r01.csv')
    df_new = df.T
    df_new = df_new.rename(columns=df_new.iloc[0])
    df_new = df_new.drop(df_new.index[:2])
    

    ##create array of dTau read in from data file
    dTau = np.array([])

    for i in range(20):
        dTau = np.insert(dTau, 0, atmfunc.RdTau(0.56, df_new['*PRE'][5*i], df_new['*PRE'][5*i+5]))

    print(dTau)
    
    
    #z_atm  = xy[::-1,0]  # last altitude value missing, find in header
    #z_atm  = np.insert(z_atm, 0, 120.)
    maxmom = 1000

    N_tau  = len(dTau)
    w0     = np.ones(N_tau)*1.
    iphas  = np.ones(N_tau,dtype='int')*6
    gg     = np.zeros(N_tau)

    cumTau = np.hstack([0.,dTau.cumsum()])
    uTau   = cumTau
    phi    = np.array([0.,60.,120.])
    umu0   = 1./np.sqrt(2.)
    fbeam  = 1./umu0  # Ensures fluxes to be normalized to one
    phi0   = 0.0
    albedo = 0.1
    umu    = np.array([-1.,-0.5,0.5,1.])
    prnt   = np.array([True, True, True, False, True])
    #prnt   = np.array([False, False, False, False, False])


    ##creating arrays of phase functions to use (Rayleigh scattering)
    p = np.zeros((len(dTau), maxmom))
    for i in range(len(p)):
        p[i][0] = int(1)
        p[i][2] =  0.1


    dTau_R = dTau
    w0_R = w0
    uphas_R = p

    ##set optical depth of the aerosol
    dTau_A = 0.1

    ##read in aerosols data

    df_a = pd.read_csv('./aerosols/a1.csv', header = None)

    w0_A = df_a[0][2]
    uphas_A = df_a[3:]


    # aerosol_layer = 19
    ##combine optical thickness, single scatter albedo and phase moments
    dTau_t = dTau_R
    dTau_t[19] = atmfunc.comb_dTau(dTau_R[19], dTau_A)

    w0_t = w0_R
    w0_t[19] = atmfunc.comb_w0(dTau_R[19], dTau_A, w0_A)

    uphas_t = uphas_R
    for i in range(len(uphas_t[19])):
        uphas_t[19][i] = atmfunc.comb_uphas(dTau_R[19], dTau_A, w0_A, uphas_R[19][i], np.float(uphas_A[0][i+3]))


    cumTau = np.hstack([0.,dTau_t.cumsum()])
    uTau   = cumTau

    

    [rfldir, rfldn, flup, dfdt, uavg, uu, albmed, trnmed] =\
                                      disort.run(dTau = dTau_t, w0=w0_t, iphas=iphas, uphas=uphas_t, gg=gg,
                                                 umu0=umu0, phi0=phi0, albedo=albedo, fbeam=fbeam,
                                                 utau=uTau, umu=umu, maxmom = maxmom, phi=phi, prnt=prnt)

    





    
    rfltot = rfldir + rfldn
    print '\n# Energy conservation, R(TOA)+T(BOA)*(1-albedo) ~ 1:  %.3f' % (flup[0] + rfltot[-1]*(1.-albedo))

    # plt.figure()
    # plt.plot(rfltot, z_atm)

    # plt.figure()
    # plt.plot(flup, z_atm)



    
