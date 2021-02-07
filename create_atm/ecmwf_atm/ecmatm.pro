; Program to convert ECMWF data to individual profiles in RFM format

ECMFIL = '../ECMWF_82_prof_101lev_2013.dat'
FIXFIL = '../ECMWF_trace_prof_101lev_2013.dat'

NPRF = 83
NLEV = 101
NFIX = 12
NVAR = 8

OPENR, LUNECM, FIXFIL, /GET_LUN
REC = ''
READF, LUNECM, REC
DAT = FLTARR(NFIX,NLEV)
READF, LUNECM, DAT
FREE_LUN, LUNECM
DAT = REVERSE ( DAT, 2 ) 
O2 = REFORM ( DAT[1,*] )
NO = REFORM ( DAT[2,*] )
SO2 = REFORM ( DAT[3,*] )
NO2= REFORM ( DAT[4,*] )
HNO3 = REFORM ( DAT[5,*] )
OCS = REFORM ( DAT[6,*] )
N2 = REFORM ( DAT[7,*] )
F11 = REFORM ( DAT[8,*] )
F12 = REFORM ( DAT[9,*] )
F14 = REFORM ( DAT[10,*] )
CCL4 = REFORM ( DAT[11,*] )

OPENR, LUNECM, ECMFIL, /GET_LUN
REC = '!'
WHILE STRMID ( REC, 0, 1 ) EQ '!' DO READF, LUNECM, REC

DAT = FLTARR(NVAR,NLEV)

FOR IPRF = 1, NPRF DO BEGIN
  IF IPRF GT 1 THEN READF, LUNECM, REC
  READF, LUNECM, IYEAR, IMON, IDAY, RLAT, RLON, PSF, LSM
; 'envelope profiles' 81-83 have all time/loc fields set to 1000
  IF IYEAR EQ 1000 THEN BEGIN
    IYEAR = 0
    IMON = 0
    IDAY = 0 
    RLAT = 99.99
    RLON = 999.99
    PSF  = 0.0
    LSM  = 0.0
  ENDIF
  READF, LUNECM, DAT
  DAT = REVERSE ( DAT, 2 ) 
  PRE = REFORM ( DAT[0,*] )
  TEM = REFORM ( DAT[1,*] )
  H2O = REFORM ( DAT[2,*] )
  CO2 = REFORM ( DAT[3,*] )
  O3  = REFORM ( DAT[4,*] )
  N2O = REFORM ( DAT[5,*] )
  CO  = REFORM ( DAT[6,*] )
  CH4 = REFORM ( DAT[7,*] )

  FILATM = 'ecmprf_' + STRING ( IPRF, FORMAT='(I2.2)' ) + '.atm'
  OPENW, LUNATM, FILATM, /GET_LUN
  PRINTF, LUNATM, '! profile#' + STRING ( IPRF, FORMAT='(I2.2)' ) + $
    ' from ' + ECMFIL + ', ' + FIXFIL + ' using ecmatm.pro'
  PRINTF, LUNATM, '! YMD=' + STRING ( IYEAR, FORMAT='(I4)' ) + $
    STRING ( IMON, FORMAT='(I2.2)' ) + STRING ( IDAY, FORMAT='(I2.2)' ) + $
    ' LAT=' + STRING ( RLAT, FORMAT='(F6.2)' ) + $
    ' LON=' + STRING ( RLON, FORMAT='(F7.2)' ) + $
    ' PSF=' + STRING ( PSF, FORMAT='(F7.2)' ) + $
    ' LSM=' + STRING ( LSM, FORMAT='(F7.5)' )
  PRINTF, LUNATM, NLEV, '  = no.levels'
  PRINTF, LUNATM, '*HGT [km]'
  PRINTF, LUNATM, FINDGEN(NLEV)
  PRINTF, LUNATM, '*PRE [mb]'
  PRINTF, LUNATM, PRE
  PRINTF, LUNATM, '*TEM [K]'
  PRINTF, LUNATM, TEM
  PRINTF, LUNATM, '*H2O [ppmv]'
  PRINTF, LUNATM, H2O
  PRINTF, LUNATM, '*CO2 [ppmv]'
  PRINTF, LUNATM, CO2
  PRINTF, LUNATM, '*O3 [ppmv]'
  PRINTF, LUNATM, O3
  PRINTF, LUNATM, '*N2O [ppmv]'
  PRINTF, LUNATM, N2O
  PRINTF, LUNATM, '*CO [ppmv]'
  PRINTF, LUNATM, CO
  PRINTF, LUNATM, '*CH4 [ppmv]'
  PRINTF, LUNATM, CH4

  PRINTF, LUNATM, '*O2 [ppmv]'
  PRINTF, LUNATM, O2
  PRINTF, LUNATM, '*NO [ppmv]'
  PRINTF, LUNATM, NO
  PRINTF, LUNATM, '*SO2 [ppmv]'
  PRINTF, LUNATM, SO2
  PRINTF, LUNATM, '*NO2 [ppmv]'
  PRINTF, LUNATM, NO2
  PRINTF, LUNATM, '*HNO3 [ppmv]'
  PRINTF, LUNATM, HNO3
  PRINTF, LUNATM, '*OCS [ppmv]'
  PRINTF, LUNATM, OCS
  PRINTF, LUNATM, '*N2 [ppmv]'
  PRINTF, LUNATM, N2
  PRINTF, LUNATM, '*F11 [ppmv]'
  PRINTF, LUNATM, F11
  PRINTF, LUNATM, '*F12 [ppmv]'
  PRINTF, LUNATM, F12
  PRINTF, LUNATM, '*F14 [ppmv]'
  PRINTF, LUNATM, F14
  PRINTF, LUNATM, '*CCl4 [ppmv]'
  PRINTF, LUNATM, CCL4

  PRINTF, LUNATM, '*END'
  FREE_LUN, LUNATM
ENDFOR

FREE_LUN, LUNECM

END