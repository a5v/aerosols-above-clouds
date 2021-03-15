#!/usr/bin/env python
"""
Analysis of an atmosphere containing a layer of cloud
"""

import numpy as np
import pandas as pd
import disort
import csv
import atmfunc


# scat.out contains 8 data sets containing the wavelength, effective radius, single-scatter albedo and
# first 1000 Legendre polynomials for each data set



##########################################################################################################

if __name__ == '__main__':

    ##DISORT CONFIGURATION

    umu0 = np.cos(np.radians(30)) #cosine of solar zenith angle (Default: 1.)
    fbeam  = 1./umu0  # Ensures fluxes to be normalized to one
    phi0   = 0.0 #solar azimuth angle (Default: 0.)
    albedo = 0.05

    # phi = np.array([63.9]) #viewing azimuth angle where to output the RT fields (Default: 0.)
    phi = np.array([0.])
    # umu = np.array([0.883])  #cosine of viewing zenith angle where to output the RT fields (Default: 1.) 
    umu = np.array([np.cos(np.radians(0))])
    
    #prnt   = np.array([True, True, True, False, True])
    prnt   = np.array([True, False, False, False, False])
    maxmom = 1000


    

    #CREATE LAYERS
    ###five layer atmosphere
    ##layer 0: 2.3-100km Rayleigh scattering
    ##layer 1: 2-2.3km aerosol and Rayleigh scattering layer
    ##layer 2: 1.5-2km Rayleigh scattering layer
    ##layer 3: 1-1.5km cloud and Rayleigh scattering layer
    ##layer 4: 0-1km Rayleigh scattering

    # parameters to set
    
    N_layer  = 5 # number of layers
    iphas  = np.ones(N_layer,dtype='int')*6 # user inputted phase functions for all layers
    gg     = np.zeros(N_layer)

    wvl_v = 0.560017
    wvl_ir = 1.59368

    w0_R = 1
    uphas_R = np.zeros((1, maxmom)) # create array with phase moments of Rayleigh scattering
    uphas_R[0][0] = 1
    uphas_R[0][2] = 0.1

    cloud_l = 1 # we fix the cloud and aerosol heights
    cloud_u = 1.5

    aerosol_l = 2
    aerosol_u = 2.3

    aerosol = "a70" # aerosol used from 'a70', 'a76', 'a77', 'a79'
    dTau_aerosol = 0.02 # optical depth of aerosol
    effr_aerosol_index = 0 # indexed from [0.1, 0.5, 1, 2]

    ##CREATE RAYLEIGH LAYER (0)
    
    dTau_R0_v = atmfunc.RdTau(wvl_v, atmfunc.h2p(aerosol_u), atmfunc.h2p(100))
    dTau_R0_ir = atmfunc.RdTau(wvl_ir, atmfunc.h2p(aerosol_u), atmfunc.h2p(100))

    ##CREATE AEROSOL & RAYLEIGH LAYER (1)

    dTau_R1_v = atmfunc.RdTau(wvl_v, atmfunc.h2p(aerosol_l), atmfunc.h2p(aerosol_u))
    dTau_R1_ir = atmfunc.RdTau(wvl_ir, atmfunc.h2p(aerosol_l), atmfunc.h2p(aerosol_u))
    

    ###READ IN WATER.CSV DATA FILE
    ###REFORMAT DATA TO BE USED BY DISORT AND SAVED

    df_aerosol = pd.read_csv('./aerosols/' + aerosol + '.csv', header = None)
    
    N_aerosol = df_aerosol.shape[1]/2

    wvl_data_aerosol = []
    effr_data_aerosol = []
    w0_data_aerosol = []
    uphas_data_aerosol = []

    
    for i in range(N_aerosol*2):
        wvl_data_aerosol.append(float(df_aerosol[i][0:1]))
        effr_data_aerosol.append(float(df_aerosol[i][1:2]))
        w0_data_aerosol.append(float(df_aerosol[i][2:3]))
        uphas_data_aerosol.append(np.array(df_aerosol[i][3:]))



    ##CREATE RAYLEIGH LAYER (2)
    
    dTau_R2_v = atmfunc.RdTau(wvl_v, atmfunc.h2p(cloud_u), atmfunc.h2p(aerosol_l))
    dTau_R2_ir = atmfunc.RdTau(wvl_ir, atmfunc.h2p(cloud_u), atmfunc.h2p(aerosol_l))

    
    
    ##CREATE CLOUD & RAYLEIGH LAYER (3)
    
    dTau_R3_v = atmfunc.RdTau(wvl_v, atmfunc.h2p(cloud_l), atmfunc.h2p(cloud_u))
    dTau_R3_ir = atmfunc.RdTau(wvl_ir, atmfunc.h2p(cloud_l), atmfunc.h2p(cloud_u))


    dTau_range_cloud = [] # set optical thickness of cloud layer

    for i in range(21):
        a = 2**(float(i-6)/2)
        x = np.array([a])
        dTau_range_cloud.append(x)

    N_dTau_cloud = len(dTau_range_cloud)

    ###READ IN WATER.CSV DATA FILE
    ###REFORMAT DATA TO BE USED BY DISORT AND SAVED

    df_cloud = pd.read_csv('./aerosols/water2_final.csv', header = None)
    
    N_cloud = df_cloud.shape[1]/2

    wvl_data_cloud = []
    effr_data_cloud = []
    w0_data_cloud = []
    uphas_data_cloud = []

    
    for i in range(N_cloud*2):
        wvl_data_cloud.append(float(df_cloud[i][0:1]))
        effr_data_cloud.append(float(df_cloud[i][1:2]))
        w0_data_cloud.append(float(df_cloud[i][2:3]))
        uphas_data_cloud.append(np.array(df_cloud[i][3:]))
    

    ##CREATE RAYLEIGH LAYER (4)
    
    dTau_R4_v = atmfunc.RdTau(wvl_v, atmfunc.h2p(0), atmfunc.h2p(cloud_l))
    dTau_R4_ir = atmfunc.RdTau(wvl_ir, atmfunc.h2p(0), atmfunc.h2p(cloud_l))



    
    ###COMBINE TO CREATE ATMOSPHERE & CALL DISORT

    
    uu_save = []
    
    for i in range(N_dTau_cloud): # iterate over range of cloud optical depth # N_dTau_cloud
        dTau_atm_v = np.zeros((N_layer, 1))
        dTau_atm_v[0] = dTau_R0_v # insert optical depths in backwards
        dTau_atm_v[1] = atmfunc.comb_dTau(dTau_R1_v, dTau_aerosol)
        dTau_atm_v[2] = dTau_R2_v
        dTau_atm_v[3] = atmfunc.comb_dTau(dTau_R3_v, dTau_range_cloud[i])
        dTau_atm_v[4] = dTau_R4_v

        dTau_atm_ir = np.zeros((N_layer, 1))
        dTau_atm_ir[0] = dTau_R0_ir # insert optical depths in backwards
        dTau_atm_ir[1] = atmfunc.comb_dTau(dTau_R1_ir, dTau_aerosol)
        dTau_atm_ir[2] = dTau_R2_ir
        dTau_atm_ir[3] = atmfunc.comb_dTau(dTau_R3_ir, dTau_range_cloud[i])
        dTau_atm_ir[4] = dTau_R4_ir

        
        uu_single_dTau = []

        uu_single_dTau.append(dTau_range_cloud[i][0]) # save optical thickness of the cloud

        for j in range(N_cloud): # iterate over cloud data used (visible) # N_cloud # note: wavelength of light is important

            w0_atm = np.zeros((N_layer, 1))
            w0_atm[0] = w0_R
            w0_atm[1] = atmfunc.comb_w0(dTau_R1_v, dTau_aerosol, w0_data_aerosol[effr_aerosol_index]) # aerosol data used
            w0_atm[2] = w0_R
            w0_atm[3] = atmfunc.comb_w0(dTau_R3_v, dTau_range_cloud[i], w0_data_cloud[j]) # cloud data used
            w0_atm[4] = w0_R
    
            uphas_atm = np.zeros((N_layer, maxmom))
            uphas_atm[0] = uphas_R
            for k in range(maxmom):
                uphas_atm[1][k] = atmfunc.comb_uphas(dTau_R1_v, dTau_aerosol, w0_data_aerosol[effr_aerosol_index], uphas_R[0][k], uphas_data_aerosol[effr_aerosol_index][k]) # aerosol data used
            uphas_atm[2] = uphas_R
            for k in range(maxmom):
                uphas_atm[3][k] = atmfunc.comb_uphas(dTau_R3_v, dTau_range_cloud[i][0], w0_data_cloud[j], uphas_R[0][k], uphas_data_cloud[j][k]) # cloud data used
            uphas_atm[4] = uphas_R
            
            [rfldir, rfldn, flup, dfdt, uavg, uu, albmed, trnmed] =\
                disort.run(dTau=dTau_atm_v, iphas=iphas,  uphas=uphas_atm, w0=w0_atm, gg=gg,
                           umu0=umu0, phi0=phi0, albedo=albedo, fbeam=fbeam,
                           umu=umu, phi=phi, maxmom=maxmom, prnt=prnt)

            print(uu[0][0][0])
            uu_single_dTau.append(uu[0][0][0])

        for j in range(N_cloud): # iterate over cloud data used (near-IR wavelength) # N_cloud # note: wavelength of light is important
            w0_atm = np.zeros((N_layer, 1))
            w0_atm[0] = w0_R
            w0_atm[1] = atmfunc.comb_w0(dTau_R1_ir, dTau_aerosol, w0_data_aerosol[effr_aerosol_index+N_aerosol]) # aerosol data used
            w0_atm[2] = w0_R
            w0_atm[3] = atmfunc.comb_w0(dTau_R3_v, dTau_range_cloud[i], w0_data_cloud[j+N_cloud]) # cloud data used
            w0_atm[4] = w0_R
    
            uphas_atm = np.zeros((N_layer, maxmom))
            uphas_atm[0] = uphas_R
            for k in range(maxmom):
                uphas_atm[1][k] = atmfunc.comb_uphas(dTau_R1_v, dTau_aerosol, w0_data_aerosol[effr_aerosol_index+N_aerosol], uphas_R[0][k], uphas_data_aerosol[effr_aerosol_index+N_aerosol][k]) # aerosol data used
            uphas_atm[2] = uphas_R
            for k in range(maxmom):
                uphas_atm[3][k] = atmfunc.comb_uphas(dTau_R3_v, dTau_range_cloud[i][0], w0_data_cloud[j+N_cloud], uphas_R[0][k], uphas_data_cloud[j+N_cloud][k]) # cloud data used
            uphas_atm[4] = uphas_R
            
            [rfldir, rfldn, flup, dfdt, uavg, uu, albmed, trnmed] =\
                disort.run(dTau=dTau_atm_v, iphas=iphas,  uphas=uphas_atm, w0=w0_atm, gg=gg,
                           umu0=umu0, phi0=phi0, albedo=albedo, fbeam=fbeam,
                           umu=umu, phi=phi, maxmom=maxmom, prnt=prnt)

            print(uu[0][0][0])
            uu_single_dTau.append(uu[0][0][0])

            
        uu_save.append(uu_single_dTau)



    name = './atmospheres/aerosol_cloud_atm_' + str(aerosol) + '_' + str(effr_aerosol_index) + '_' + str(dTau_aerosol) + '.csv'
        
    with open(name, 'w') as file:
        writer = csv.writer(file)
        for i in range(N_dTau_cloud):
            writer.writerow(uu_save[i])
    

