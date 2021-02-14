#!/usr/bin/env python
"""
Analysis of a single layer of the cloud
"""

import numpy as np
import pandas as pd
import disort
import csv


# scat.out contains 8 data sets containing the wavelength, effective radius, single-scatter albedo and
# first 1000 Legendre polynomials for each data set



##########################################################################################################

if __name__ == '__main__':

    ##DISORT CONFIGURATION

    umu0 = 0.698  #cosine of solar zenith angle (Default: 1.)
    fbeam  = 1./umu0  # Ensures fluxes to be normalized to one
    phi0   = 0.0 #solar azimuth angle (Default: 0.)
    albedo = 0 #surface albedo (Default: 0.1)

    phi = np.array([63.9]) #viewing azimuth angle where to output the RT fields (Default: 0.)
    umu = np.array([0.883])  #cosine of viewing zenith angle where to output the RT fields (Default: 1.) 

    
    #prnt   = np.array([True, True, True, False, True])
    prnt   = np.array([False, False, False, False, False])
    maxmom = 1000


    dTau_range = []
    
    for i in range(50):
        a = 2**(i-10)
        x = np.array([a])
        dTau_range.append(x)

    N_tau  = 1
    iphas  = np.ones(N_tau,dtype='int')*6
    gg     = np.zeros(N_tau)
    

    ##READ IN WATER.CSV DATA FILE
    ##REFORMAT DATA TO BE USED BY DISORT AND SAVED

    df = pd.read_csv('./aerosols/water.csv', header = None)

    n_data = df.shape[1]

    wvl_data = []
    effr_data = []
    w0_data = []
    p_data = []

    
    for i in range(n_data):
        wvl_data.append(float(df[i][0:1]))
        effr_data.append(float(df[i][1:2]))
        w0_data.append(df[i][2:3])
        p_data.append(df[i][3:])    
    
    
    w0_array = []
    p_array =[]
    
    for i in range(n_data):
        p = p_data[i]
        w0 = w0_data[i]
        
        p = np.array(p)
        w0 = np.array(w0)

        p_array.append(p)
        w0_array.append(w0)
        


    ##CALLING DISORT
    rfldir_array = []
    rfldn_array = []
    flup_array = []
    dfdt_array = []
    uavg_array = []
    uu_array = []
    albmed_array = []
    trnmed_array = []


    for j in range(n_data):    

        list = []
        
        for i in range (len(dTau_range)):
            [rfldir, rfldn, flup, dfdt, uavg, uu, albmed, trnmed] =\
                disort.run(dTau=dTau_range[i], iphas=iphas,  uphas=[p_array[j]], w0=[w0_array[j]], gg=gg,
                           umu0=umu0, phi0=phi0, albedo=albedo, fbeam=fbeam,
                           umu=umu, phi=phi, maxmom=maxmom, prnt=prnt)

            # rfldir_array.append(rfldir)
            # rfldn_array.append(rfldn)
            # flup_array.append(flup)
            # dfdt_array.append(dfdt)
            # uavg_array.append(uavg)
            list.append(uu)
            # albmed_array.append(albmed)
            # trnmed_array.append(trnmed)
        #print(list)
        uu_array.append(list)


    ##SAVE DATA
    uu_save =[]

    for j in range(len(uu_array)):
        x = []

        y = []
        y.append(wvl_data[j])
        y.append(effr_data[j])
        x.append(y)
        
        for i in range(len(uu_array[j])):
            x.append(uu_array[j][i][0][0][0])
        uu_save.append(x)

    dTau_save = []

    for i in range(len(dTau_range)):
        dTau_save.append(dTau_range[i][0])


    with open('./atmospheres/test_water.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(dTau_save)
        for i in range(len(uu_save)):
            writer.writerow(uu_save[i])
