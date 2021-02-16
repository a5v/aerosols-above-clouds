#!/usr/bin/env python
"""
Analysis of single cloud layer (similar to test_water.py)
We fix the optical thickness of the cloud and vary the optical thickness of the aerosol
We also must fix the wavelength of light and the cloud used (these can be varied separately)
"""

import numpy as np
import pandas as pd
import disort
import csv


# scat.out contains 8 data sets containing the wavelength, effective radius, single-scatter albedo and
# first 1000 Legendre polynomials for each data set



##########################################################################################################

if __name__ == '__main__':

    #DISORT CONFIGURATION

    umu0 = 0.698  # cosine of solar zenith angle (Default: 1.)
    fbeam  = 1./umu0  # Ensures fluxes to be normalized to one
    phi0   = 0.0 # solar azimuth angle (Default: 0.)
    albedo = 0 # surface albedo (Default: 0.1)

    phi = np.array([63.9]) # viewing azimuth angle where to output the RT fields (Default: 0.)
    umu = np.array([0.883])  # cosine of viewing zenith angle where to output the RT fields (Default: 1.) 

    
    prnt   = np.array([True, True, True, False, True])
    # prnt   = np.array([True, False, False, False, False])
    maxmom = 1000


    #CREATE LAYERS
    # single layer atmosphere of cloud 
    
    N_layer  = 1
    iphas  = np.ones(N_layer,dtype='int')*6
    gg     = np.zeros(N_layer)

    
    ##CREATE CLOUD LAYER (0)

    dTau_range_cloud = [] # set optical thickness of cloud layer

    for i in range(8):
        a = 2**(i-2)
        x = np.array([a])
        dTau_range_cloud.append(x)

    N_dTau_cloud = len(dTau_range_cloud)
    
    ###READ IN WATER.CSV DATA FILE
    ###REFORMAT DATA TO BE USED BY DISORT AND SAVED

    df_cloud = pd.read_csv('./aerosols/water.csv', header = None)
    
    N_cloud = df_cloud.shape[1]/2

    wvl_data_cloud = []
    effr_data_cloud = []
    w0_data_cloud = []
    uphas_data_cloud = []

    
    for i in range(N_cloud*2):
        wvl_data_cloud.append(float(df_cloud[i][0:1]))
        effr_data_cloud.append(float(df_cloud[i][1:2]))
        w0_data_cloud.append(float(df_cloud[i][2:3]))
        uphas_data_cloud.append(df_cloud[i][3:])

    
    ##COMBINE TO CREATE ATMOSPHERE (no combination needed for single layer) & CALL DISORT

    uu_save = []
    
    for i in range(N_dTau_cloud): # iterate over range of cloud optical depth # N_dTau_aerosol
        dTau_atm = np.array([])
        dTau_atm = np.insert(dTau_atm, 0, dTau_range_cloud[i])

        uu_single_dTau = []

        uu_single_dTau.append(dTau_range_cloud[i][0]) # save optical thickness of the cloud

        for j in range(N_cloud * 2): # iterate over cloud data used # note: wavelength of light is not needed

            w0_atm = np.zeros((N_layer, 1))
            w0_atm[0] = w0_data_cloud[j] # cloud data used
            
    
            uphas_atm = np.zeros((N_layer, maxmom))
            uphas_atm[0] = uphas_data_cloud[j] # cloud data used

            [rfldir, rfldn, flup, dfdt, uavg, uu, albmed, trnmed] =\
                disort.run(dTau=dTau_atm, iphas=iphas,  uphas=uphas_atm, w0=w0_atm, gg=gg,
                           umu0=umu0, phi0=phi0, albedo=albedo, fbeam=fbeam,
                           umu=umu, phi=phi, maxmom=maxmom, prnt=prnt)

            print(uu[0][0][0])
            uu_single_dTau.append(uu[0][0][0])

        uu_save.append(uu_single_dTau)

    name = './atmospheres/cloud.csv'
        
    with open(name, 'w') as file:
        writer = csv.writer(file)
        for i in range(N_dTau_cloud):
            writer.writerow(uu_save[i])
