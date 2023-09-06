#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )
from scipy.integrate import trapezoid

from UtilitiesModule import GetFileArray, GetData, ComputeAngleAverage, \
                            Overwrite

#### ========== User Input ==========

rootDirectory = '/lump/data/accretionShockStudy/newData/2D/'

M    = '2.8'
Rpns = '020'
Rs   = '7.00e1'

ID = '2D_M{:}_Rpns{:}_Rs{:}'.format( M, Rpns, Rs )

verbose = False

#### ====== End of User Input =======

Rs = np.float64( Rs )

field = 'LateralMomentumFluxInRadialDirection'

useLogScale = True

ID_GR = 'GR' + ID
ID_NR = 'NR' + ID

# Get mesh
plotfileBaseName = ID_GR + '.plt'
plotfileDirectory = rootDirectory + ID_GR + '/'
plotfileArray = GetFileArray( plotfileDirectory, plotfileBaseName )
plotfile      = plotfileDirectory + plotfileArray[0]
time, data, dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
  = GetData( plotfile, field+'GR', verbose = False )

ind = np.where( ( X1 < 0.9 * Rs ) & ( X1 > 0.8 * Rs ) )[0]

OW = Overwrite( 'LatFlux_{:}.dat'.format( ID_GR ) )
if( OW ):

    plotfileBaseNameGR  = ID_GR + '.plt'
    plotfileDirectoryGR = rootDirectory + ID_GR + '/'
    plotfileArrayGR     = GetFileArray \
                            ( plotfileDirectoryGR, plotfileBaseNameGR )
    nSS_GR              = plotfileArrayGR.shape[0]

    plotfileBaseNameNR  = ID_NR + '.plt'
    plotfileDirectoryNR = rootDirectory + ID_NR + '/'
    plotfileArrayNR     = GetFileArray \
                            ( plotfileDirectoryNR, plotfileBaseNameNR )
    nSS_NR              = plotfileArrayNR.shape[0]

    nSS = min( nSS_GR, nSS_NR )

    AA_GR  = np.empty( nSS, np.float64 )
    timeGR = np.empty( nSS, np.float64 )

    AA_NR  = np.empty( nSS, np.float64 )
    timeNR = np.empty( nSS, np.float64 )

    for iSS in range( nSS ):

        if verbose: print('')
        print( '{:}/{:}'.format( iSS+1, nSS ) )

        plotfile = plotfileDirectoryGR + plotfileArrayGR[iSS]
        timeGR[iSS], dataGR, dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
          = GetData( plotfile, field+'GR', verbose = False )

        AA = ComputeAngleAverage \
                ( dataGR[ind,:,0], X2, dX2, dX3 )

        # AA includes \sqrt{\gamma} = \psi^6 * r^2
        AA_GR[iSS] \
          = 4.0 * np.pi \
              * trapezoid \
                  ( AA, \
                    x = X1[ind], dx = dX1[0] )

        del dataGR

        plotfile = plotfileDirectoryNR + plotfileArrayNR[iSS]
        timeNR[iSS], dataNR, dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
          = GetData( plotfile, field+'NR', verbose = False )

        AA = ComputeAngleAverage \
                ( dataNR[ind,:,0], X2, dX2, dX3 )

        AA_NR[iSS] \
          = 4.0 * np.pi \
              * trapezoid \
                  ( AA, \
                    x = X1[ind], dx = dX1[0] )


        del dataNR

    np.savetxt( '../plottingData_new/LatFlux_{:}.dat'.format( ID_GR ), \
                np.vstack( ( timeGR, AA_GR ) ) )
    np.savetxt( '../plottingData_new/LatFlux_{:}.dat'.format( ID_NR ), \
                np.vstack( ( timeNR, AA_NR ) ) )

#timeGR, dataGR = np.loadtxt( 'LatFlux_{:}.dat'.format( ID_GR ) )
#timeNR, dataNR = np.loadtxt( 'LatFlux_{:}.dat'.format( ID_NR ) )

#### Plotting
#
#fig, ax  = plt.subplots( 1, 1 )#, figsize = (12,8) )
#
#ax.plot( timeGR[:-1], dataGR[:-1], label = 'GR' )
#ax.plot( timeNR[:-1], dataNR[:-1], label = 'NR' )
#if( useLogScale ):
#    ax.set_yscale( 'symlog', linthresh = 1.0e40 )
#    saveFigAs = '/home/kkadoogan/fig.{:}_{:}_SymLog_VsCoordinateTime.png'.format( field, ID )
#else:
#    saveFigAs = '/home/kkadoogan/fig.{:}_{:}_Linear_VsCoordinateTime.png'.format( field, ID )
#
#ax.legend()
#
#ax.grid()
#
#ax.set_xlabel( r'$\mathrm{Coordinate\ Time}\,\left[\mathrm{ms}\right]$' )
#
##plt.savefig( saveFigAs, dpi = 300 )
#plt.show()
#plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
