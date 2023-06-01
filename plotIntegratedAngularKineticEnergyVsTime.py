#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from UtilitiesModule import GetFileArray, GetData

#### ========== User Input ==========

rootDirectory \
  = '/lump/data/accretionShockStudy/newData/2D/'

ID = '1D_M1.4_Mdot0.3_Rs180'

field = 'AngularKineticEnergy'

# Scale of colorbar
zScale = None
#zScale = 'log'

saveFigAs = '/home/kkadoogan/fig.{:}.png'.format( ID )

verbose = True

#### ====== End of User Input =======

### Integrate

ID = '2D_M2.8_Rpns020_Rs6.00e1'

plotfileBaseNameGR = 'GR' + ID + '.plt'
plotfileDirectoryGR = rootDirectory + 'GR' + ID + '/'
plotfileArrayGR = GetFileArray( plotfileDirectoryGR, plotfileBaseNameGR )
plotfileArrayGR = np.copy( plotfileArrayGR[:-1] )

plotfileBaseNameNR = 'NR' + ID + '.plt'
plotfileDirectoryNR = rootDirectory + 'NR' + ID + '/'
plotfileArrayNR = GetFileArray( plotfileDirectoryNR, plotfileBaseNameNR )
plotfileArrayNR = np.copy( plotfileArrayNR[:-1] )

nSS = plotfileArrayNR.shape[0]

def Integrate( plotfileDirectory, plotfileBaseName, plotfile ):
    sqrtGm, dataUnits, \
    X1, X2, X3, dX1, dX2, dX3, xL, xH, nX, Time \
      = GetData( plotfileDirectory, plotfileBaseName, 'GF_SqrtGm', \
                 'spherical', True, \
                 argv = [ 'a', plotfile[-8:] ], \
                 ReturnTime = True, ReturnMesh = True )
    data, dataUnits, \
    X1, X2, X3, dX1, dX2, dX3, xL, xH, nX, Time \
      = GetData( plotfileDirectory, plotfileBaseName, field, \
                 'spherical', True, \
                 argv = [ 'a', plotfile[-8:] ], \
                 ReturnTime = True, ReturnMesh = True )

    integral = 0.0
    for iX1 in range( nX[0] ):
        for iX2 in range( nX[1] ):
            integral += 2.0 * np.pi * data[iX1,iX2,0] * sqrtGm[iX1,iX2,0] \
                          * dX1[iX1,iX2,0] * dX2[iX1,iX2,0]

    return Time, integral

time = np.empty( nSS, np.float64 )
GR   = np.empty( nSS, np.float64 )
NR   = np.empty( nSS, np.float64 )
for iSS in range( nSS ):
    plotfileGR = plotfileDirectoryGR + plotfileArrayGR[iSS]
    print( '  {:}/{:}'.format( iSS, nSS ) )
    time[iSS], GR[iSS] \
      = Integrate( plotfileDirectoryGR, plotfileBaseNameGR, plotfileGR )

    plotfileNR = plotfileDirectoryNR + plotfileArrayNR[iSS]
    t, NR[iSS] \
      = Integrate( plotfileDirectoryNR, plotfileBaseNameNR, plotfileNR )

np.savetxt( 'GR.dat', np.vstack( ( time, GR ) ) )
np.savetxt( 'NR.dat', np.vstack( ( time, NR ) ) )

time, GR = np.loadtxt( 'GR.dat' )
time, NR = np.loadtxt( 'NR.dat' )

### Plotting

fig, ax  = plt.subplots( 1, 1 )

ax.plot( time, NR - GR )

ax.grid()

if zScale == 'log': ax.set_yscale( 'log' )

ax.set_xlabel( r'$t\ \left[\mathrm{ms}\right]$' )
ax.set_ylabel( r'$\tau_{\mathrm{NR}}-\tau_{\mathrm{GR}}$' )

#plt.show()

plt.savefig( saveFigAs, dpi = 300 )
print( '\n  Saved {:}'.format( saveFigAs ) )

plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
