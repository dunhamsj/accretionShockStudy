#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from UtilitiesModule import GetFileArray, GetData

#### ========== User Input ==========

rootDirectory \
  = '/lump/data/accretionShockStudy/newData/2D/'

ID = '2D_M2.8_Rpns020_Rs8.75e1'

field = 'AngularKineticEnergy'

# Scale of colorbar
#zScale = None
zScale = 'log'

saveFigAs = '/home/kkadoogan/fig.{:}.png'.format( ID )

verbose = True

#### ====== End of User Input =======

### Integrate

plotfileBaseNameGR = 'GR' + ID + '.plt'
plotfileDirectoryGR = rootDirectory + 'GR' + ID + '/'
plotfileArrayGR = GetFileArray( plotfileDirectoryGR, plotfileBaseNameGR )
plotfileArrayGR = np.copy( plotfileArrayGR[:-1] )

plotfileBaseNameNR = 'NR' + ID + '.plt'
plotfileDirectoryNR = rootDirectory + 'NR' + ID + '/'
plotfileArrayNR = GetFileArray( plotfileDirectoryNR, plotfileBaseNameNR )
plotfileArrayNR = np.copy( plotfileArrayNR[:-1] )

dummy, dataUnits, \
X1, X2, X3, dX1, dX2, dX3, xL, xH, nX \
  = GetData( plotfileDirectoryGR, plotfileBaseNameGR, 'GF_SqrtGm', \
             'spherical', True, \
             ReturnTime = False, ReturnMesh = True )
nX2 = nX[1]
nT = 7
ind = np.empty( nT, dtype = np.int64 )
ind = np.linspace( 0, nX2-1, 7, dtype = np.int64 )

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

    integral = np.zeros( nT, np.float64 )
    for i in range( nT ):
        for iX1 in range( nX[0] ):
            integral[i] += data[iX1,ind[i],0] * sqrtGm[iX1,ind[i],0] \
                             * dX1[iX1,ind[i],0] / np.sin( X2[iX1,ind[i],0] )

    return Time, integral

#nSS = plotfileArrayNR.shape[0]
#time = np.empty( nSS, np.float64 )
#GR   = np.empty( (nT,nSS), np.float64 )
#NR   = np.empty( (nT,nSS), np.float64 )
#for iSS in range( 0, nSS, 1 ):
#
#    print( '  {:}/{:}'.format( iSS, nSS ) )
#
#    plotfileGR = plotfileDirectoryGR + plotfileArrayGR[iSS]
#    time[iSS], GR[:,iSS] \
#      = Integrate( plotfileDirectoryGR, plotfileBaseNameGR, plotfileGR )
#
#    plotfileNR = plotfileDirectoryNR + plotfileArrayNR[iSS]
#    t, NR[:,iSS] \
#      = Integrate( plotfileDirectoryNR, plotfileBaseNameNR, plotfileNR )
#
#for i in range( nT ):
#    np.savetxt( 'GR_{:}_{:}.dat'.format( ID, i ), np.vstack( ( time, GR[i] ) ) )
#    np.savetxt( 'NR_{:}_{:}.dat'.format( ID, i ), np.vstack( ( time, NR[i] ) ) )

### Plotting

fig, ax  = plt.subplots( 1, 1 )

for i in range( nT ):

    time, GR = np.loadtxt( 'GR_{:}_{:}.dat'.format( ID, i ) )
    time, NR = np.loadtxt( 'NR_{:}_{:}.dat'.format( ID, i ) )
    ax.plot( time, NR - GR, \
             label \
               = r'$\theta/\pi={:}$' \
                 .format( np.round( X2[0,ind[i],0] / np.pi, 2 ) ) )

ax.grid()
ax.legend()

if zScale == 'log': ax.set_yscale( 'symlog', linthresh = 1.0e40 )

#ax.set_ylim( 1.0e26, 1.0e45 )
#ax.set_xlim( -1.0, 55.0 )
ax.set_xlabel( r'$t\ \left[\mathrm{ms}\right]$' )
ax.set_ylabel( r'$\frac{1}{\sin\theta}\int_{R_{\mathrm{PNS}}}^{1.5\,R_{\mathrm{S}}}\left(\tau^{\theta}_{\mathrm{NR}}-\tau^{\theta}_{\mathrm{GR}}\right)\sqrt{\gamma}\,dr$' )
ax.text( 40, 1.0e30, \
         r'$\tau^{\theta}:=\frac{S^{2}S_{2}}{2\,D}$', fontsize = 15 )

#plt.show()

plt.savefig( saveFigAs, dpi = 300 )
print( '\n  Saved {:}'.format( saveFigAs ) )

plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
