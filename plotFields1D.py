#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from UtilitiesModule import GetFileArray, GetData

#### ========== User Input ==========


ID = 'StandingAccretionShock_Relativistic'

rootDirectory \
  = '/home/kkadoogan/Work/Codes/thornado/SandBox/AMReX/Applications/\
{:}/'.format( ID )
#rootDirectory \
#  = '/lump/data/accretionShockStudy/newData/1D/'

field = 'PF_D'

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

GRID = ID
plotfileBaseName = GRID + '.plt'
plotfileDirectory = rootDirectory + GRID + '_new/'
dataGR, dataUnits, \
X1, X2, X3, dX1, dX2, dX3, xL, xH, nX \
  = GetData( plotfileDirectory, plotfileBaseName, field, \
             'spherical', True, argv = ['a'], \
             ReturnTime = False, ReturnMesh = True )
ax.plot( X1[:,0,0], dataGR[:,0,0], '.', label = 'new' )

GRID = ID
plotfileBaseName = GRID + '.plt'
plotfileDirectory = rootDirectory + GRID + '_old/'
dataGR, dataUnits, \
X1, X2, X3, dX1, dX2, dX3, xL, xH, nX \
  = GetData( plotfileDirectory, plotfileBaseName, field, \
             'spherical', True, argv = ['a'], \
             ReturnTime = False, ReturnMesh = True )
ax.plot( X1[:,0,0], dataGR[:,0,0], '.', label = 'old' )

ax.legend()
ax.grid()

ax.set_title( r'$\texttt{{{:}}}$'.format( ID ) )
if zScale == 'symlog':
    ax.set_yscale( zScale, linthresh = linthresh )
else:
    ax.set_yscale( zScale )

xRef = [ 1.55e2, 1.25e2, 5.0e1 ]
for xx in xRef:
    ax.axvline( xx, c = 'b' )

ax.set_xlabel( r'$r\ \left[\mathrm{km}\right]$' )
ax.set_ylabel( r'$p_{\mathrm{NR}}/p_{\mathrm{GR}}$' )

#plt.savefig( saveFigAs, dpi = 300 )
#print( '\n  Saved {:}'.format( saveFigAs ) )

plt.show()
plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
