#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from UtilitiesModule import GetFileArray, GetData

#### ========== User Input ==========


#ID = '1D_M2.8_Rpns020_Rs6.00e1'
ID = '1D_M1.4_Rpns040_Rs1.20e2'

rootDirectory \
  = '/lump/data/accretionShockStudy/newData/1D/'

saveFigAs = '/home/kkadoogan/fig.{:}_Eirik.png'.format( ID )

#### ====== End of User Input =======

### Plotting

fig, ax  = plt.subplots( 1, 1 )

cCGS = 2.99792458e10

GRID = 'GR' + ID
plotfileBaseName = GRID + '.plt'
plotfileDirectory = rootDirectory + GRID + '/'
alphaGR, dataUnits, \
X1, X2, X3, dX1, dX2, dX3, xL, xH, nX \
  = GetData( plotfileDirectory, plotfileBaseName, \
             'GF_Alpha', \
             'spherical', True, argv = ['a'], \
             ReturnTime = False, ReturnMesh = True )
hGR, dataUnits, \
X1, X2, X3, dX1, dX2, dX3, xL, xH, nX \
  = GetData( plotfileDirectory, plotfileBaseName, \
             'RelativisticSpecificEnthalpy', \
             'spherical', True, argv = ['a'], \
             ReturnTime = False, ReturnMesh = True )
hGR /= cCGS**2
psiGR, dataUnits, \
X1, X2, X3, dX1, dX2, dX3, xL, xH, nX \
  = GetData( plotfileDirectory, plotfileBaseName, \
             'GF_Psi', \
             'spherical', True, argv = ['a'], \
             ReturnTime = False, ReturnMesh = True )
WGR, dataUnits, \
X1, X2, X3, dX1, dX2, dX3, xL, xH, nX \
  = GetData( plotfileDirectory, plotfileBaseName, \
             'LorentzFactor', \
             'spherical', True, argv = ['a'], \
             ReturnTime = False, ReturnMesh = True )

NRID = 'NR' + ID
plotfileBaseName = NRID + '.plt'
plotfileDirectory = rootDirectory + NRID + '/'
phiNR, dataUnits, \
X1, X2, X3, dX1, dX2, dX3, xL, xH, nX \
  = GetData( plotfileDirectory, plotfileBaseName, \
             'GF_Phi_N', \
             'spherical', True, argv = ['a'], \
             ReturnTime = False, ReturnMesh = True )
alphaNR = 1.0 + phiNR / cCGS**2
psiNR   = 1.0 - phiNR / cCGS**2

ylim = [ 0.78, 1.25 ]

ax.set_ylim( ylim )

ax.plot( X1[:,0,0], alphaGR[:,0,0], 'k-' , label = r'$\alpha$' )
ax.plot( X1[:,0,0], alphaNR[:,0,0], 'r-' , label = r'$\alpha_{\mathrm{N}}$' )
ax.plot( X1[:,0,0], hGR    [:,0,0], 'k--', label = r'$h/c^{2}$' )
ax.plot( X1[:,0,0], psiGR  [:,0,0], 'k-.', label = r'$\psi$' )
ax.plot( X1[:,0,0], psiNR  [:,0,0], 'r-.', label = r'$\psi_{\mathrm{N}}$' )
ax.plot( X1[:,0,0], WGR    [:,0,0], 'k:' , label = r'$W$' )

ax.legend()
ax.grid()

ax.set_title( r'$\texttt{{{:}}}$'.format( ID ) )

ax.set_xlabel( r'$r\ \left[\mathrm{km}\right]$' )

plt.savefig( saveFigAs, dpi = 300 )
print( '\n  Saved {:}'.format( saveFigAs ) )

#plt.show()
#plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
