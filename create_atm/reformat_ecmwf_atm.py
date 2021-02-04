#!/usr/bin/env python
"""
Test of the Python wrapper to the DISORT library
Module '_disort' is auto-generated with f2py (version:2).
"""

import numpy as np
import disort

import pandas as pd


# scat.out contains 8 data sets containing the wavelength, effective radius, single-scatter albedo and
# first 1000 Legendre polynomials for each data set



##########################################################################################################

if __name__ == '__main__':

    ##DISORT CONFIGURATION
    
    #umu0   = 1./np.sqrt(2.) #cosine of solar zenith angle (Default: 1.)
    umu0 = 0.899
    fbeam  = 1./umu0  # Ensures fluxes to be normalized to one
    phi0   = 0.0 #solar azimuth angle (Default: 0.)
    albedo = 0 #surface albedo (Default: 0.1)

    ##phi = np.array([0.,60.,120.]) #viewing azimuth angle where to output the RT fields (Default: 0.)

    phi = np.array([42.])
    
    ##umu    = np.array([-1.,-0.5,0.5,1.]) #cosine of viewing zenith angle where to output the RT fields (Default: 1.) 

    umu = np.array([0.76])
    
    prnt   = np.array([True, True, True, False, True])
    maxmom = 1000


    dTau_range = []
    
    for i in range(10):
        a = float(i+1)/2
        x = np.array([a])
        dTau_range.append(x)

    print(dTau_range)
        
    dTau = np.array([1])





    
    ecmwf_atm = open('./ecmwf_atm/ecmprf_01.atm')
    strip = ecmwf_atm.read().split()
    
    print(float(len(strip))/103)



    for i in range(6):
        print(strip[i*103+19:i*103+122])
    

    import csv
        
        
    with open('./reformat_ecmwf_atm/ecmwf_r01.csv', 'w') as file:
        writer = csv.writer(file)
        for i in range(20):
            writer.writerow(strip[i*103+19:i*103+122])

        
    

    N_tau  = len(dTau)
    iphas  = np.ones(N_tau,dtype='int')*2
    gg     = np.zeros(N_tau)


    cumTau = np.hstack([0.,dTau.cumsum()])
    uTau   = cumTau #optical thickness where to output the RT fields (Default: 0.)







    

    

    ##READ IN SCAT.OUT DATA FILE
    f = open('scat.out')

    y = f.read().split()

    data_points = 1003

    n_data = len(y)/data_points

    data = []

    for i in range(n_data):
        x = np.array([])
        for j in range(data_points*i,data_points*i + data_points):
            x = np.append(x, np.float64(y[j]))
        data.append(x)

    wl_data = []
    effr_data = []
    w0_data = []
    p_data = []

    for i in range(len(data)):
        wl_data.append(data[i][0:1])
        effr_data.append(data[i][1:2])
        w0_data.append(data[i][2:3])
        p_data.append(data[i][3:])


    # ##READING IN FIRST DATA SET
    # p_0 = []
    # p_0.append(p_data[0])

    # w0_0 = []
    # w0_0.append(w0_data[0])


    # p_0_array = np.array(p_0)
    # w0_0_array = np.array(w0_0)


    
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


    #print(uu_array)

    
    # for i in range(len(uu_array)):
    #     print(uu_array[i])


    # uu_save =[]

    
   

    # for j in range(len(uu_array)):
    #     x = []

    #     y = []
    #     y.append(wl_data[j][0])
    #     y.append(effr_data[j][0])
    #     y.append(w0_data[j][0])

    #     x.append(y)
        
    #     for i in range(len(uu_array[j])):
    #         x.append(uu_array[j][i][0][0][0])
    #     uu_save.append(x)
        
    # print(uu_save)


    

    # dTau_save = []

    # for i in range(len(dTau_range)):
    #     dTau_save.append(dTau_range[i][0])

    # #print(dTau_save)


    
    # import csv


    

    
    
    # with open('./atmospheres/empty_atm.csv', 'w') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(dTau_save)
    #     for i in range(len(uu_save)):
    #         writer.writerow(uu_save[i])

    
        
    # print(wl_data[0][0])

    
    # import csv

    # ### with open('basic_atm.csv', 'w') as file:
    # ###     writer = csv.writer(file)
    # ###     writer.writerow(uu_array)

    
    # # with open('innovators.csv', 'w', newline='') as file:
    # #     writer = csv.writer(file)
    # #     writer.writerow(["SN", "Name", "Contribution"])
    # #     writer.writerow([1, "Linus Torvalds", "Linux Kernel"])
    # #     writer.writerow([2, "Tim Berners-Lee", "World Wide Web"])
    # #     writer.writerow([3, "Guido van Rossum", "Python Programming"])

    # print(wl_data)
    # print(effr_data)
    # print(w0_data)


    # print(type(uu_array[0][0][0][0]))
    # print(len(uu_array))


    # uu_save =[]

    # x = []
    
    # for i in range(len(uu_array)):
    #     x.append(uu_array[i][0][0][0])

    # uu_save.append(x)

    # print(uu_save)

    # with open('basic_atm.csv', 'w') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(uu_save[0])

