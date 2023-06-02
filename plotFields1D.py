#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from UtilitiesModule import GetFileArray, GetData

#### ========== User Input ==========

#rootDirectory \
#  = '/home/kkadoogan/Work/Codes/thornado/SandBox/AMReX/Applications/\
#StandingAccretionShock_Relativistic/'
rootDirectory \
  = '/lump/data/accretionShockStudy/newData/1D/'

ID = '1D_M1.4_Rpns040_Rs1.20e2'
#ID = '1D_M2.8_Rpns020_Rs6.00e1'

field = 'AF_P'

# Scale of colorbar
#zScale = 'None'
zScale = 'log'
#zScale = 'symlog'
linthresh = 1.0e-2

saveFigAs = '/home/kkadoogan/fig.{:}.png'.format( ID )

verbose = True

#### ====== End of User Input =======

### Plotting

fig, ax  = plt.subplots( 1, 1 )

GRID = 'GR' + ID
plotfileBaseName = GRID + '.plt'
plotfileDirectory = rootDirectory + GRID + '/'
plotfileArray = GetFileArray( plotfileDirectory, plotfileBaseName )
plotfile      = plotfileDirectory + plotfileArray[0]
dataGR, dataUnits, \
X1, X2, X3, dX1, dX2, dX3, xL, xH, nX \
  = GetData( plotfileDirectory, plotfileBaseName, field, \
             'spherical', True, \
             ReturnTime = False, ReturnMesh = True )
NRID = 'NR' + ID
plotfileBaseName = NRID + '.plt'
plotfileDirectory = rootDirectory + NRID + '/'
plotfileArray = GetFileArray( plotfileDirectory, plotfileBaseName )
plotfile      = plotfileDirectory + plotfileArray[0]
dataNR, dataUnits, \
X1, X2, X3, dX1, dX2, dX3, xL, xH, nX \
  = GetData( plotfileDirectory, plotfileBaseName, field, \
             'spherical', True, \
             ReturnTime = False, ReturnMesh = True )
ax.plot( X1[:,0,0], dataNR[:,0,0]/dataGR[:,0,0] )

ax.grid()

ax.set_title( r'$\texttt{{{:}}}$'.format( ID ) )
if zScale == 'symlog':
    ax.set_yscale( zScale, linthresh = linthresh )
else:
    ax.set_yscale( zScale )

ax.set_xlabel( r'$r\ \left[\mathrm{km}\right]$' )
ax.set_ylabel( r'$p_{\mathrm{NR}}/p_{\mathrm{GR}}$' )

plt.savefig( saveFigAs, dpi = 300 )
print( '\n  Saved {:}'.format( saveFigAs ) )

#plt.show()
plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
