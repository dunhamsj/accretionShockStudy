#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )
from scipy.integrate import trapezoid

from UtilitiesModule import GetFileArray, GetData, ComputeAngleAverage, \
                            Overwrite
from globalVariables import *

#### ========== User Input ==========

rootDirectory = plotfileRootDirectory + '2D/'

M    = '1.8'
Rpns = '020'
Rs   = '7.00e1'

ID = '2D_M{:}_Rpns{:}_Rs{:}'.format( M, Rpns, Rs )

field = 'LateralMomentumFluxInRadialDirection'

verbose = False

#### ====== End of User Input =======

Rs = np.float64( Rs )

def generateData( ID, rel ):

    plotFileBaseName  = ID + '.plt'
    plotFileDirectory = rootDirectory + ID + '/'
    plotFileArray     = GetFileArray( plotFileDirectory, plotFileBaseName )
    nSS               = plotFileArray.shape[0]

    AA   = np.empty( nSS, np.float64 )
    time = np.empty( nSS, np.float64 )

    for iSS in range( nSS ):

        if verbose: print('')
        print( '  {:}/{:}'.format( iSS+1, nSS ) )

        data, dataUnits, X1, X2, X3, dX1, dX2, dX3, xL, xH, nX, time[iSS] \
          = GetData( plotFileDirectory, plotFileBaseName, field+rel, \
                     'spherical', True, argv = [ 'a', plotFileArray[iSS] ], \
                     ReturnTime = True, ReturnMesh = True, Verbose = verbose )

        ind = np.where( ( X1[:,0,0] < 0.9 * Rs ) & ( X1[:,0,0] > 0.8 * Rs ) )[0]


        AA_iSS = ComputeAngleAverage \
                ( data[ind], X2[0,:,0], dX2[0,:,0] )

        # AA includes \sqrt{\gamma}
        AA[iSS] \
          = 4.0 * np.pi \
              * trapezoid \
                  ( AA_iSS, \
                    x = X1[ind,0,0], dx = dX1[0,0,0] )

    header = 'Generated from computeLateralFluxInRadialDirection.py\n' \
               + 'Time [ms], F^{r}_{theta} [cgs]'
    np.savetxt( dataDirectory + 'LatFlux_{:}.dat'.format( ID ), \
                np.vstack( ( time, AA ) ), header = header )

    return

ID_GR = 'GR' + ID
ID_NR = 'NR' + ID

#generateData( ID_GR, 'GR' )
generateData( ID_NR, 'NR' )

timeGR, dataGR = np.loadtxt( dataDirectory + 'LatFlux_{:}.dat'.format( ID_GR ) )
timeNR, dataNR = np.loadtxt( dataDirectory + 'LatFlux_{:}.dat'.format( ID_NR ) )

### Plotting

fig, ax  = plt.subplots( 1, 1 )#, figsize = (12,8) )

ax.plot( timeGR[:-1], dataGR[:-1], label = 'GR' )
ax.plot( timeNR[:-1], dataNR[:-1], label = 'NR' )

ax.set_yscale( 'symlog', linthresh = 1.0e40 )

ax.legend()

ax.grid()

ax.set_xlabel( r'$\mathrm{Coordinate\ Time}\,\left[\mathrm{ms}\right]$' )

#saveFigAs \
#  = '/home/kkadoogan/fig.{:}_{:}_SymLog_VsCoordinateTime.png' \
#    .format( field, ID )
#plt.savefig( saveFigAs, dpi = 300 )
#print( '\n  Saved {:}'.format( saveFigAs ) )

plt.show()
plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
