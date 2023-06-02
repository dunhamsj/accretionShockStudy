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
#zScale = None
zScale = 'log'

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

dummy, dataUnits, \
X1, X2, X3, dX1, dX2, dX3, xL, xH, nX \
  = GetData( plotfileDirectoryGR, plotfileBaseNameGR, 'GF_SqrtGm', \
             'spherical', True, \
             ReturnTime = False, ReturnMesh = True )
nX2 = nX[1]
nT = 5
ind = np.empty( nT, dtype = np.int64 )
ind[0] = 0
ind[1] = nX2 // 4
ind[2] = nX2 // 2
ind[3] = 3 * nX2 // 4
ind[4] = -1

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
    for i in range( nT ):
        for iX1 in range( nX[0] ):
            integral[i] += data[iX1,ind[i],0] * sqrtGm[iX1,ind[i],0] \
                             * dX1[iX1,ind[i],0] / np.sin( X2[iX1,ind[i],0] )

    return Time, integral

#nSS = plotfileArrayNR.shape[0]
#time = np.empty( nSS, np.float64 )
#GR   = np.empty( (nT,nSS), np.float64 )
#NR   = np.empty( (nT,nSS), np.float64 )
#for iSS in range( nSS ):
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
#    np.savetxt( 'GR_{:}.dat'.format( i ), np.vstack( ( time, GR[i] ) ) )
#    np.savetxt( 'NR_{:}.dat'.format( i ), np.vstack( ( time, NR[i] ) ) )

### Plotting

fig, ax  = plt.subplots( 1, 1 )

for i in range( nT ):

    time, GR = np.loadtxt( 'GR_{:}.dat'.format( i ) )
    time, NR = np.loadtxt( 'NR_{:}.dat'.format( i ) )
    ax.plot( time, NR - GR, \
             label \
               = r'$\theta/\pi={:}$' \
                 .format( np.round( X2[0,ind[i],0] / np.pi, 2 ) ) )

ax.grid()
ax.legend()

if zScale == 'log': ax.set_yscale( 'log' )

ax.set_xlim( -1.0, 55.0 )
ax.set_xlabel( r'$t\ \left[\mathrm{ms}\right]$' )
ax.set_ylabel( r'$\frac{1}{\sin\theta}\int_{R_{\mathrm{PNS}}}^{1.5\,R_{\mathrm{S}}}\left(\tau^{\theta}_{\mathrm{NR}}-\tau^{\theta}_{\mathrm{GR}}\right)\sqrt{\gamma}\,dr$' )
ax.text( 40, 1.0e30, \
         r'$\tau^{\theta}:=\frac{S^{2}S_{2}}{2\,D}$', fontsize = 15 )

plt.show()

#plt.savefig( saveFigAs, dpi = 300 )
#print( '\n  Saved {:}'.format( saveFigAs ) )

plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
