##file containing functions to calculate atmospheric properties

import numpy as np



##height in km to pressure in hPa (1hPa = 100Pa) converter using hydrostatic equation for an isothermal atmosphere
def h2p(height, ps = 1013.25):
        H = float(7.3)

        pressure = ps * np.exp(-float(height)/H) 

        return pressure


##calculate Rayleigh optical thickness for a layer from pressure of top and bottom of layer and wavelength
##wavelength in micrometers (1micrometer = 10**-6m)
##surface pressure assumed to be 1013.25hPa
def RdTau(wvl, pl, pu, ps=1013.25): 
        RdTau0 = float((float(ps)/1013.0))/(117.03*wvl**4-1.316*wvl**2)

        dTauR = float((pl-pu)*RdTau0)/ps 
        
        return dTauR

##combining the optical depths of aerosol and Rayleigh scattering
def comb_dTau(dTau_R, dTau_A):
        dTau_t = dTau_R +dTau_A
        return dTau_t

##combining the single scatter albedo of the aerosol and Rayleigh scattering
def comb_w0(dTau_R, dTau_A, w0_A):
        w0_t = float(dTau_R + w0_A*dTau_A)/float(dTau_R+dTau_A)
        return w0_t

##combining the Legendre moments of the aerosol and Rayleigh scattering
def comb_uphas(dTau_R, dTau_A, w0_A, uphas_R, uphas_A):
        uphas_t = float(dTau_R*uphas_R +w0_A*dTau_A*uphas_A)/float(dTau_R + w0_A*dTau_A)
        return uphas_t

