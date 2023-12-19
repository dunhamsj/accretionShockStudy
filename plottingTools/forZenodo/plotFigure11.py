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

xlim = [ 55, 185 ]

fig, axs = plt.subplots( 3, 1, figsize = (12,9) )

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

    dataFileName_NR \
    = dataDirectory + 'LegendrePowerSpectrum_NR2D_{:}.dat'.format( ID )
    f = open( dataFileName_NR )
    dum = f.readline()
    s = f.readline(); ind = s.find( '#' )+1
    tmp \
      = np.array( list( map( np.float64, s[ind:].split() ) ), \
                  np.float64 )
    omega_NR = tmp[3]

    dataFileName_GR \
    = dataDirectory + 'LegendrePowerSpectrum_GR2D_{:}.dat'.format( ID )
    f = open( dataFileName_GR )
    dum = f.readline()
    s = f.readline(); ind = s.find( '#' )+1
    tmp \
      = np.array( list( map( np.float64, s[ind:].split() ) ), \
                  np.float64 )
    omega_GR = tmp[3]

    Rsh = np.float64( ID[15:21] )
    M   = np.float64( ID[1:4] )
    R   = np.float64( ID[9:12] )

    xi = '{:.1f}'.format( M / ( R / 20.0 ) )

    if col[xi] == '#4daf4a':
        mew = 2
    else:
        mew = 1

    if xi != xi1:

        axs[0].plot  ( Rsh, T_NR , ls = 'none', mew = mew, \
                       c = col[xi], marker = mkr, ms = ms, mfc = 'none', \
                       label = r'$\texttt{{NR}}, \xi={:}$'.format( xi ) )
        axs[0].plot  ( Rsh, T_GR , ls = 'none', \
                       c = col[xi], marker = mkr, ms = ms, \
                       label = r'$\texttt{{GR}}, \xi={:}$'.format( xi ) )
        axs[1].plot( Rsh, omega_NR , ls = 'none', mew = mew, \
                     c = col[xi], marker = mkr, ms = ms, mfc = 'none' )
        axs[1].plot( Rsh, omega_GR, ls = 'none', \
                     c = col[xi], marker = mkr, ms = ms )
        axs[2].plot  ( Rsh, omega_NR * T_NR , ls = 'none', mew = mew, \
                       c = col[xi], marker = mkr, ms = ms, mfc = 'none' )
        axs[2].plot  ( Rsh, omega_GR * T_GR , ls = 'none', \
                       c = col[xi], marker = mkr, ms = ms )

    else:

        axs[0].plot( Rsh,  T_NR , ls = 'none', mew = mew, \
                     c = col[xi], marker = mkr, ms = ms, mfc = 'none' )
        axs[0].plot( Rsh, T_GR , ls = 'none', \
                     c = col[xi], marker = mkr, ms = ms )
        axs[1].plot( Rsh, omega_NR , ls = 'none', mew = mew, \
                     c = col[xi], marker = mkr, ms = ms, mfc = 'none' )
        axs[1].plot( Rsh, omega_GR, ls = 'none', \
                     c = col[xi], marker = mkr, ms = ms )
        axs[2].plot  ( Rsh, omega_NR * T_NR , ls = 'none', mew = mew, \
                       c = col[xi], marker = mkr, ms = ms, mfc = 'none' )
        axs[2].plot  ( Rsh, omega_GR * T_GR , ls = 'none', \
                       c = col[xi], marker = mkr, ms = ms )

    xi1 = xi

axs[0].legend( loc = 4 )

for i in range( 3 ):
    axs[i].set_xlim( xlim )
    axs[i].grid( which = 'both' )
    axs[i].tick_params( which = 'both', top = True, right = True )
    axs[i].set_xlabel( r'$R_{\textrm{sh}}\ \left[\mathrm{km}\right]$' )

axs[0].set_yscale( 'log' )
axs[0].set_ylabel( r'$T\ \left[\mathrm{ms}\right]$' )
axs[1].set_ylabel( r'$\omega\ \left[\mathrm{ms}^{-1}\right]$' )
axs[2].set_ylabel( r'$\omega\,T$' )

plt.show()

#figName = '/home/kkadoogan/fig.EfficiencyComparison.png'
#plt.savefig( figName, dpi = 300, bbox_inches = 'tight' )
#print( '\n  Saved {:}'.format( figName ) )

plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
