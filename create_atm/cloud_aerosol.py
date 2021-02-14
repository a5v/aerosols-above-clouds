#!/usr/bin/env python
"""
Analysis of aerosol above cloud (water) two layer atmosphere
We fix the optical thickness of the cloud and vary the optical thickness of the aerosol
We vary the effective radius of the aerosol used (this is varied separately) 
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

    
    # prnt   = np.array([True, True, True, False, True])
    prnt   = np.array([True, False, False, False, False])
    maxmom = 1000


    #CREATE LAYERS
    # two layer atmosphere of cloud above aerosol
    
    N_layer  = 2
    iphas  = np.ones(N_layer,dtype='int')*6
    gg     = np.zeros(N_layer)

    
    ##CREATE CLOUD LAYER (0)

    cloud_data_used = 5 # set which dataset of cloud used (from 0 to 5)
    dTau_cloud = 1 # set optical thickness of cloud layer
    
    ###READ IN WATER.CSV DATA FILE
    ###REFORMAT DATA TO BE USED BY DISORT AND SAVED

    df_cloud = pd.read_csv('./aerosols/water.csv', header = None)

    N_cloud = df_cloud.shape[1]

    wvl_data_cloud = []
    effr_data_cloud = []
    w0_data_cloud = []
    uphas_data_cloud = []

    
    for i in range(N_cloud):
        wvl_data_cloud.append(float(df_cloud[i][0:1]))
        effr_data_cloud.append(float(df_cloud[i][1:2]))
        w0_data_cloud.append(float(df_cloud[i][2:3]))
        uphas_data_cloud.append(df_cloud[i][3:])

    
    ##CREATE AEROSOL LAYER (1)
    
    dTau_range_aerosol = [] 
    
    for i in range(8): # set range of optical thicknesses of the aerosol
        a = 2**(i-2)
        x = np.array([a])
        dTau_range_aerosol.append(x)

    N_dTau_aerosol = len(dTau_range_aerosol)

    ###READ IN AEROSOL.CSV DATA FILE
    ###REFORMAT DATA TO BE USED BY DISORT AND SAVED
    
    df_aerosol = pd.read_csv('./aerosols/aerosol.csv', header = None)

    N_aerosol = df_aerosol.shape[1]

    wvl_data_aerosol = []
    effr_data_aerosol = []
    w0_data_aerosol = []
    uphas_data_aerosol = []

    
    for i in range(N_aerosol):
        wvl_data_aerosol.append(float(df_aerosol[i][0:1]))
        effr_data_aerosol.append(float(df_aerosol[i][1:2]))
        w0_data_aerosol.append(float(df_aerosol[i][2:3]))
        uphas_data_aerosol.append(df_aerosol[i][3:])    


    
    ##COMBINE TO CREATE ATMOSPHERE & CALL DISORT

    uu_save = []
    
    for i in range(N_dTau_aerosol): # iterate over range of aerosol optical depth # N_dTau_aerosol
        dTau_atm = np.array([])
        dTau_atm = np.insert(dTau_atm, 0, dTau_range_aerosol[i])
        dTau_atm = np.insert(dTau_atm, 0, dTau_cloud)

        uu_single_dTau = []
        
        for j in range(4): # iterate over aerosol data used for visible # N_aerosol

            w0_atm = np.zeros((N_layer, 1))
            w0_atm[0] = w0_data_cloud[cloud_data_used] # cloud data used (remember to change all four instances of this!!)
            w0_atm[1] = w0_data_aerosol[j]
    
            uphas_atm = np.zeros((N_layer, maxmom))
            uphas_atm[0] = uphas_data_cloud[cloud_data_used] # cloud data used
            uphas_atm[1] = uphas_data_aerosol[j]


            [rfldir, rfldn, flup, dfdt, uavg, uu, albmed, trnmed] =\
                disort.run(dTau=dTau_atm, iphas=iphas,  uphas=uphas_atm, w0=w0_atm, gg=gg,
                           umu0=umu0, phi0=phi0, albedo=albedo, fbeam=fbeam,
                           umu=umu, phi=phi, maxmom=maxmom, prnt=prnt)

            print(uu[0][0][0])
            uu_single_dTau.append(uu[0][0][0])

        # note: different wavelength
        for j in range(4,8): # iterate over aerosol data used for IR # N_aerosol
             

            w0_atm = np.zeros((N_layer, 1))
            w0_atm[0] = w0_data_cloud[cloud_data_used + 6] # cloud data used
            w0_atm[1] = w0_data_aerosol[j]
            
            uphas_atm = np.zeros((N_layer, maxmom))
            uphas_atm[0] = uphas_data_cloud[cloud_data_used + 6] # cloud data used
            uphas_atm[1] = uphas_data_aerosol[j]
            

            [rfldir, rfldn, flup, dfdt, uavg, uu, albmed, trnmed] =\
                disort.run(dTau=dTau_atm, iphas=iphas,  uphas=uphas_atm, w0=w0_atm, gg=gg,
                           umu0=umu0, phi0=phi0, albedo=albedo, fbeam=fbeam,
                           umu=umu, phi=phi, maxmom=maxmom, prnt=prnt)
            
            print(uu[0][0][0])
            uu_single_dTau.append(uu[0][0][0])

        uu_save.append(uu_single_dTau)


name = './atmospheres/ca_'+str(cloud_data_used)+'_'+str(dTau_cloud)+'.csv'
        
with open(name, 'w') as file:
    writer = csv.writer(file)
    for i in range(len(uu_save)):
        writer.writerow(uu_save[i])


        
    # for j in range(n_data):    

    #     list = []
        
    #     for i in range (len(dTau_range)):
    #         [rfldir, rfldn, flup, dfdt, uavg, uu, albmed, trnmed] =\
    #             disort.run(dTau=dTau_range[i], iphas=iphas,  uphas=[p_array[j]], w0=[w0_array[j]], gg=gg,
    #                        umu0=umu0, phi0=phi0, albedo=albedo, fbeam=fbeam,
    #                        umu=umu, phi=phi, maxmom=maxmom, prnt=prnt)

    #         # rfldir_array.append(rfldir)
    #         # rfldn_array.append(rfldn)
    #         # flup_array.append(flup)
    #         # dfdt_array.append(dfdt)
    #         # uavg_array.append(uavg)
    #         list.append(uu)
    #         # albmed_array.append(albmed)
    #         # trnmed_array.append(trnmed)
    #     #print(list)
    #     uu_array.append(list)


    # ##SAVE DATA
    # uu_save =[]

    # for j in range(len(uu_array)):
    #     x = []

    #     y = []
    #     y.append(wvl_data[j])
    #     y.append(effr_data[j])
    #     x.append(y)
        
    #     for i in range(len(uu_array[j])):
    #         x.append(uu_array[j][i][0][0][0])
    #     uu_save.append(x)

    # dTau_save = []

    # for i in range(len(dTau_range)):
    #     dTau_save.append(dTau_range[i][0])


    # with open('./atmospheres/cloud_aerosol.csv', 'w') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(dTau_save)
    #     for i in range(len(uu_save)):
    #         writer.writerow(uu_save[i])
