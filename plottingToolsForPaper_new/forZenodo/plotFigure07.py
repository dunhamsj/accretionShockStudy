#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( './publication.sty' )

from globalVariables import *

IDs = [ 'M1.4_Rpns070_Rs1.50e2', \
        'M1.4_Rpns040_Rs1.20e2', \
        'M1.4_Rpns040_Rs1.50e2', \
        'M1.4_Rpns040_Rs1.75e2', \
        'M1.8_Rpns020_Rs7.00e1', \
        'M2.8_Rpns020_Rs6.00e1', \
        'M2.8_Rpns020_Rs7.00e1' ]

col = { '0.4' : '#ff7f00', \
        '0.7' : '#377eb8', \
        '1.8' : '#4daf4a', \
        '2.8' : '#f781bf' }
mkr = 's'

ms = 6

fig, ax = plt.subplots( 1, 1 )

Models = {}
with open( dataDirectory + 'fft.dat' ) as f:
    i = -1
    for line in f:
       i += 1
       if i < 2: continue
       x = line.split()
       Models[x[0]] = [ np.float64( x[1] ), np.float64( x[2] ) ]

xi1 = '0.'
for i in range( len( IDs ) ):

    ID = IDs[i]

    T_NR, dT_NR = Models['NR2D_'+ID]
    T_GR, dT_GR = Models['GR2D_'+ID]

    Rsh = np.float64( ID[15:21] )
    M   = np.float64( ID[1:4] )
    R   = np.float64( ID[9:12] )

    xi = '{:.1f}'.format( M / ( R / 20.0 ) )

    if xi != xi1:

        ax.plot  ( Rsh, T_NR , ls = 'none', \
                       c = col[xi], marker = mkr, ms = ms, mfc = 'none', \
                       label = r'$\texttt{{NR}}, \xi={:}$'.format( xi ) )
        ax.plot  ( Rsh, T_GR , ls = 'none', \
                       c = col[xi], marker = mkr, ms = ms, \
                       label = r'$\texttt{{GR}}, \xi={:}$'.format( xi ) )

    else:

        ax.plot( Rsh, T_NR , ls = 'none', \
                     c = col[xi], marker = mkr, ms = ms, mfc = 'none' )
        ax.plot( Rsh, T_GR , ls = 'none', \
                     c = col[xi], marker = mkr, ms = ms )

    xi1 = xi

ax.legend( loc = 2 )
ax.grid( which = 'both' )

ax.tick_params( which = 'both', top = True, right = True )
ax.set_xlabel( r'$R_{\textrm{sh}}\ \left[\mathrm{km}\right]$' )
ax.set_ylabel( r'$T\ \left[\mathrm{ms}\right]$' )

ax.set_ylim( 3, 100 )

ax.set_yscale( 'log' )

#plt.show()

figName = figuresDirectory + 'fig.OscillationPeriodComparison.pdf'
plt.savefig( figName, dpi = 300, bbox_inches = 'tight' )
print( '\n  Saved {:}'.format( figName ) )

plt.close()

import os
os.system( 'rm -rf __pycache__ ' )