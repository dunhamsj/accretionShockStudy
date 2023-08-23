#!/usr/bin/env python3

import numpy as np
from os.path import isfile, isdir
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from FitPowerToModel import FittingFunction
from computeTimeScales import ComputeTimeScales

stage   = 'late'
vsTau   = False
saveFig = True
saveDir = '/home/kkadoogan/'
rootDir = '/home/dunhamsj/Work/Codes/thornado/SandBox/AMReX/' \
            + 'Applications/StandingAccretionShock_NonRelativistic/'

arrShape = (2)

ID = [ 'NR2D_M2.8_Rpns020_Rs6.00e1', \
       'NR2D_M2.8_Rpns021_Rs6.10e1' ]

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = ['#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00']

fig, ax = plt.subplots( 1, 1 )

for i in range( len( ID ) ):

    dataFileName \
      = 'plottingData/{:}_LegendrePowerSpectrum.dat'.format( ID[i] )

    if not isfile( dataFileName ):
        print( '{:} does not exist. Skipping.' \
               .format( dataFileName ) )
        continue

    t, P0, P1, P2, P3, P4 \
      = np.loadtxt( dataFileName )

    if not isfile( dataFileName ):
        print( '{:} does not exist. Skipping.' \
               .format( dataFileName ) )
        continue

    ind = np.where( t <= 50.0 )[0]

    ax.plot( t[ind], P1[ind], '-', color = color[i], \
              label = r'$\texttt{{{:}}}$'.format( ID[i] ) )

ax.grid()
ax.legend()
ax.set_yscale( 'log' )
#ax.set_ylim( 1.0e11, 5.0e26 )
ax.set_xlabel( r'$t/\mathrm{ms}$' )


if saveFig:

    fileName = saveDir + 'fig.PowerInLegendreModes.png'
    plt.savefig( fileName, dpi = 300 )
    print( '\n  Saved figure: {:}'.format( fileName ) )

else:

    plt.show()

import os
os.system( 'rm -rf __pycache__ ' )
