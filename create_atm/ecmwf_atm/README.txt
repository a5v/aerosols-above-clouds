Contains the set of RTTOV profiles converted to RFM .atm file format by
IDL program ecmatm.pro

#81: min values
#82: max values
#83: mean values

Also, from Rob Hargreaves, additional species

day_ecmwf.atm - only contains those molecules from day.atm that are not
                included in each ECMWF profile.
c2h4_ecmwf.atm - same data as c2h4.atm in the /rfm/atm folder.
hcooh_ecmwf.atm - profile obtained from Lucy and contains more levels
                than hcooh.atm file in the /rfm/atm folder.

Note that the 'altitude' grid in all these profiles is just an arbitrary index
used for interpolation - all profiles are actually interpolated from log
pressure profiles.

