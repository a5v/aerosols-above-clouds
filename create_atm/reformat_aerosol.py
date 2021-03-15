#!/usr/bin/env python
"""
Reformat aerosol .out files from Mie code into a .csv files
"""

import csv


# scat.out contains 8 data sets containing the wavelength, effective radius, single-scatter albedo and
# first 1000 Legendre polynomials for each data set



##########################################################################################################

if __name__ == '__main__':


    ##READ IN SCAT.OUT DATA FILE
    aerosol = "a79"
    file = open('./aerosols/' + aerosol +'.out')

    scat_file = file.read().split()

    data_points = 1003

    n_data = int(len(scat_file)/data_points)

    data = []

    data_save = []
    
    for i in range(n_data):
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
    save_name = './aerosols/' + aerosol + '.csv'
    with open(save_name, 'w') as file:
        writer = csv.writer(file)
        for val in data_save_improve:
            writer.writerow(val)


 
