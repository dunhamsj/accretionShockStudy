#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from UtilitiesModule import GetFileArray, GetData, GetNorm

Rs0 = '1.20e2'
#rootDirectory = '/home/kkadoogan/'
ID = 'GR2D_M1.4_Rpns040_Rs{:}'.format( Rs0 )

rootDirectory \
  = '/lump/data/accretionShockStudy/newData/2D/'

plotfileBaseName = ID + '.plt'

plotfileDirectory = rootDirectory + ID + '/'

plotfileArray = GetFileArray( plotfileDirectory, plotfileBaseName )

plotfileArray = np.copy( plotfileArray[:-1] )

nSS = plotfileArray.shape[0]

plotfile = ( plotfileDirectory + plotfileArray[0] )[-8:]
dum, dum2, X1, X2, X3, dX1, dX2, dX3, xL, xH, nX \
  = GetData( plotfileDirectory, plotfileBaseName, 'DF_TCI', \
             'spherical', True, argv = [ 'a', plotfile ], \
             ReturnTime = False, ReturnMesh = True, Verbose = False )

#t  = np.empty( nSS, np.float64 )
#y0 = np.empty( (nSS,nX[0]), np.float64 )
#Rs = np.empty( nSS, np.float64 )
#
#for iSS in range( nSS ):
#
#    plotfile = ( plotfileDirectory + plotfileArray[iSS] )[-8:]
#
#    print( '  {:}/{:}'.format( iSS, nSS ) )
#    data, dataUnits, \
#    X1, X2, X3, dX1, dX2, dX3, xL, xH, nX, Time \
#      = GetData( plotfileDirectory, plotfileBaseName, 'DF_TCI', \
#                 'spherical', True, argv = [ 'a', plotfile ], \
#                 ReturnTime = True, ReturnMesh = True, Verbose = False )
#    data = np.copy( data[:,:,0] )
#
#    t [iSS] = Time
#    y0[iSS] = np.max( data, axis = 1 )
#
#    entropy, dataUnits, \
#    X1, X2, X3, dX1, dX2, dX3, xL, xH, nX, Time \
#      = GetData( plotfileDirectory, plotfileBaseName, 'PolytropicConstant', \
#                 'spherical', True, argv = [ 'a', plotfile ], \
#                 ReturnTime = True, ReturnMesh = True, Verbose = False )
#    entropy = np.copy( entropy[:,:,0] )
#
#    Rs[iSS] = -np.inf
#    for iX2 in range( nX[1] ):
#        ind = np.where( entropy[:,iX2] > 4.0e14 )[0][-1]
#        Rs[iSS] = max( Rs[iSS], X1[ind,0,0] )
#
#np.savetxt( 'TCI_{:}_t.dat' .format( ID ), t  )
#np.savetxt( 'TCI_{:}_y0.dat'.format( ID ), y0 )
#np.savetxt( 'TCI_{:}_Rs.dat'.format( ID ), Rs )

t  = np.loadtxt( 'TCI_{:}_t.dat' .format( ID ) )
y0 = np.loadtxt( 'TCI_{:}_y0.dat'.format( ID ) )
Rs = np.loadtxt( 'TCI_{:}_Rs.dat'.format( ID ) )

xmin = 4.0e1
xmax = 1.4e2
indT = np.where( ( t < 2.2e2 ) & ( t > 1.0e2 ) )[0]
indX = np.where( X1[:,0,0] < xmax )[0]
t  = np.copy( t [indT[0]:indT[-1]+1] )
y0 = np.copy( y0[indT[0]:indT[-1]+1,indX[0]:indX[-1]+1] )
Rs = np.copy( Rs[indT[0]:indT[-1]+1] )

Rs0 = np.float64( Rs0 )
plt.title( r'$\texttt{{{:}}}$'.format( ID ) )
plt.imshow( np.log10( np.abs( y0 ) ), \
            extent = [ xmin / Rs0, xmax / Rs0, t.min(), t.max() ], \
            aspect = 'auto', \
            origin = 'lower' )
plt.xlim( xmin / Rs0, xmax / Rs0 )
plt.plot( Rs / Rs0, t, color = 'r' )
plt.xlabel( r'$r/R_{\mathrm{S}}$', fontsize = 15 )
plt.ylabel( r'$t\ \left[\mathrm{ms}\right]$', fontsize = 15 )
plt.colorbar( label = r'$\log_{10}\ C_{\mathrm{TCI}}$' )
#plt.show()
plt.savefig( '/home/kkadoogan/fig.TCI_{:}.png'.format( ID ), dpi = 300 )
plt.close()
