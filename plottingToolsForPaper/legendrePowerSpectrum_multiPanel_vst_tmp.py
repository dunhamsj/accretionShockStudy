#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )
from os.path import isfile

from FitPowerToModel import FittingFunction
from UtilitiesModule import GetFileArray, GetData

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = ['#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00']

indices = {}
with open( '../plottingData/indices_RshCutOff1.10.dat' ) as f:
    i = -1
    for line in f:
        i += 1
        if i < 2: continue
        x = line.split()
        indices[x[0]] = [ np.int64( x[1] ), np.float64( x[2] ) ]

T_aa = {}
T_ac = {}
with open( '../plottingData/T_SASI.dat' ) as f:
    i = -1
    for line in f:
       i += 1
       if i < 3: continue
       x = line.split()
       T_aa[x[0]] = np.float64( x[1] )
       T_ac[x[0]] = np.float64( x[2] )

IDs = [ 'NR2D_M2.8_Rpns020_Rs6.00e1', \
        'NR2D_M2.8_Rpns021_Rs6.10e1' ]

fig, ax = plt.subplots( 1, 1 )

for i in range( len( IDs ) ):

    ID = IDs[i]

    dataFileName \
      = '../plottingData/{:}_LegendrePowerSpectrum.dat'.format( ID )

    t, P0, P1, P2, P3, P4 \
      = np.loadtxt( dataFileName )

    ax.plot( t, P1, '-', label = ID )

ax.legend()
ax.set_yscale( 'log' )

ax.tick_params( top = True, left = True, right = True, bottom = True )
ax.grid()

ax.set_xlabel( r'$t$ [ms]'     , fontsize = 14 )
ax.set_ylabel( r'$H_{1}$ [cgs]', fontsize = 14 )

#plt.show()

plt.savefig \
( '/home/kkadoogan/fig.LegendrePowerSpectrum.png', dpi = 300 )

plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
