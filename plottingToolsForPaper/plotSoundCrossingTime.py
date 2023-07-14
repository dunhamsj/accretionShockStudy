#!/usr/bin/env python3

from sys import argv
import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from UtilitiesModule import GetFileArray, GetData

#### ========== User Input ==========

Rpns = '003'
M    = '2.8'
Rsh  = '7.00e1'

verbose = False

#### ====== End of User Input =======

ID   = '1D_M{:}_Rpns{:}_Rs{:}'.format( M, Rpns, Rsh )
GRID = 'GR' + ID
NRID = 'NR' + ID

saveFigAs = '../Figures/fig.SoundCrossingTime_{:}.pdf'.format( ID )

plotfileDirectory = '../plottingData/'

plotfileBaseName_GR = GRID + '.plt'
plotfileBaseName_NR = NRID + '.plt'

plotfile_GR = plotfileDirectory + plotfileBaseName_GR + '00000000/'
plotfile_NR = plotfileDirectory + plotfileBaseName_NR + '00000000/'

time, V    , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
  = GetData( plotfile_GR, 'PF_V1'   , verbose = verbose )
time, Cs   , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
  = GetData( plotfile_GR, 'AF_Cs'   , verbose = verbose )
time, alpha, dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
  = GetData( plotfile_GR, 'GF_Alpha', verbose = verbose )
time, Gm11 , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
  = GetData( plotfile_GR, 'GF_Gm_11', verbose = verbose )

c = 2.99792458e5
VSq = Gm11 * V**2
lambdaP_GR = alpha / ( 1.0 - VSq * Cs**2 / c**4 ) \
            * ( V * ( 1.0 - Cs**2 / c**2 ) \
            + Cs * np.sqrt( ( 1.0 - VSq / c**2 ) \
            * ( 1.0 / Gm11 * ( 1.0 - VSq * Cs**2 / c**4 ) \
            - V / c * V / c * ( 1.0 - Cs**2 / c**2 ) ) ) )
lambdaP_GR = np.copy( lambdaP_GR[:,0,0] )

time, V   , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
  = GetData( plotfile_NR, 'PF_V1'   , verbose = verbose )
time, Cs  , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
  = GetData( plotfile_NR, 'AF_Cs'   , verbose = verbose )
time, Gm11, dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
  = GetData( plotfile_NR, 'GF_Gm_11', verbose = verbose )

lambdaP_NR = V + Cs * np.sqrt( 1.0 / Gm11 )
lambdaP_NR = np.copy( lambdaP_NR[:,0,0] )

ind = np.where( X1 < np.float64( Rsh ) )[0]

X1         = np.copy( X1[ind] )
lambdaP_GR = np.copy( lambdaP_GR[ind] )
lambdaP_NR = np.copy( lambdaP_NR[ind] )

### Plotting

fig, ax = plt.subplots( 1, 1 )

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = ['#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00']

T_GR = 2.0 * np.pi * X1 / lambdaP_GR * 1.0e3
T_NR = 2.0 * np.pi * X1 / lambdaP_NR * 1.0e3

print( T_GR[-1] - T_NR[-1] )

ax.plot( X1, T_GR, label = 'GR' )
ax.plot( X1, T_NR, label = 'NR' )

ax.set_xlabel( r'$r\ \left[\mathrm{km}\right]$', fontsize = 15 )
ax.set_ylabel( r'$2\pi\,r/\lambda_{+}\ \left[\mathrm{ms}\right]$', \
               fontsize = 15 )
ax.set_title( r'$\texttt{{{:}}}$'.format( ID ), fontsize = 15 )
ax.grid()
ax.legend()

#figName = 'fig.SoundCrossingTime_{:}.png'.format( ID )
#plt.savefig( figName, dpi = 300 )
#print( '\n  Saved {:}'.format( figName ) )

plt.show()

import os
os.system( 'rm -rf __pycache__ ' )
