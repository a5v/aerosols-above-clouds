#!/usr/bin/env python
"""
Reformat scat.out files into a .csv files ignoring unphysical values
"""

import csv


# scat.out contains 8 data sets containing the wavelength, effective radius, single-scatter albedo and
# first 1000 Legendre polynomials for each data set



##########################################################################################################

if __name__ == '__main__':


    ##READ IN SCAT.OUT DATA FILE
    file = open('./aerosols/scat_water2.out')
    
    scat_file = file.read().split()

    data_points = 1003

    n_data = int(len(scat_file)/data_points)

    data = []

    data_save = []
    
    for i in range(n_data):
        if i >= 4 and i <= 9 or i >= 14 and i <= 19:
            x = []
            for j in range(data_points*i,data_points*i + data_points):
                x.append(scat_file[j])
            data_save.append(x)


    ##reformat data to save in column format
    data_save_improve = []


    for i in range(len(data_save[0])):
        x =[]
        for j in range(len(data_save)):
            x.append(data_save[j][i])
        data_save_improve.append(x)
    


    ##save file
    
    with open('./aerosols/water2_final.csv', 'w') as file:
        writer = csv.writer(file)
        for val in data_save_improve:
            writer.writerow(val)


 
