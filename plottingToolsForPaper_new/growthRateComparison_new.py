#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( './publication.sty' )
from os.path import isfile

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
cs  = 7.0

NX = 5.0
NY = NX * 3/4
fig, ax = plt.subplots( 1, 1, figsize = (NX,NY) )

xi1 = '0.'
for i in range( len( IDs ) ):

    ID = IDs[i]

    dataFileName_NR \
    = dataDirectory + 'LegendrePowerSpectrum_NR2D_{:}.dat'.format( ID )

    dataFileName_GR \
    = dataDirectory + 'LegendrePowerSpectrum_GR2D_{:}.dat'.format( ID )

    Rsh  = np.float64( ID[15:21] )

    M = np.float64( ID[1:4] )
    R = np.float64( ID[9:12] )
    xi = '{:.1f}'.format( M / ( R / 20.0 ) )

    # NR

    f = open( dataFileName_NR )
    dum = f.readline()
    s = f.readline(); ind = s.find( '#' )+1
    tmp \
      = np.array( list( map( np.float64, s[ind:].split() ) ), \
                  np.float64 )
    G_NR = tmp[3]
    dum = f.readline()
    s = f.readline(); ind = s.find( '#' )+1
    tmp \
      = np.array( list( map( np.float64, s[ind:].split() ) ), \
                  np.float64 )
    dG_NR = tmp[1]
    f.close()

    # GR

    f = open( dataFileName_GR )
    dum = f.readline()
    s = f.readline(); ind = s.find( '#' )+1
    tmp \
      = np.array( list( map( np.float64, s[ind:].split() ) ), \
                  np.float64 )
    G_GR = tmp[3]
    dum = f.readline()
    s = f.readline(); ind = s.find( '#' )+1
    tmp \
      = np.array( list( map( np.float64, s[ind:].split() ) ), \
                  np.float64 )
    dG_GR = tmp[1]
    f.close()

    if xi != xi1:

        ax.plot( Rsh, G_NR , ls = 'none', \
                 c = col[xi], marker = mkr, mfc = 'none' , \
                 label = r'$\texttt{{NR}}, \xi={:}$'.format( xi ) )
        ax.plot( Rsh, G_GR , ls = 'none', \
                 c = col[xi], marker = mkr, \
                 label = r'$\texttt{{GR}}, \xi={:}$'.format( xi ) )

    else:

        ax.plot( Rsh, G_NR , ls = 'none', \
                 c = col[xi], marker = mkr, mfc = 'none' )
        ax.plot( Rsh, G_GR , ls = 'none', \
                 c = col[xi], marker = mkr )

    xi1 = xi

ax.legend( loc = 1 )
ax.grid( which = 'both' )

ax.tick_params( which = 'both', top = True, right = True )
ax.set_xlabel( r'$R_{\textrm{sh}}\ \left[\mathrm{km}\right]$' )
ax.set_ylabel( r'$\omega\ \left[\mathrm{ms}^{-1}\right]$' )

#plt.show()

figName = figuresDirectory + 'fig.GrowthRateComparison.pdf'
plt.savefig( figName, dpi = 300 )
print( '\n  Saved {:}'.format( figName ) )

plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
