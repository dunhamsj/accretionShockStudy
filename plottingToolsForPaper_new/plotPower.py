#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from globalVariables import *

fig, ax = plt.subplots( 1, 1 )

IDs = [ '2D_M1.8_Rpns020_Rs7.00e1' ]

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = ['#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00']

for i in range( len( IDs ) ):

    dataNR = np.loadtxt( dataDirectory + 'LegendrePowerSpectrum_NR{:}.dat'.format( IDs[i] ) )
    dataGR = np.loadtxt( dataDirectory + 'LegendrePowerSpectrum_GR{:}.dat'.format( IDs[i] ) )

    ax.plot( dataNR[0], dataNR[2], ls = '-' , c = color[i], lw = 2, label = 'NR'+IDs[i] )
#    ax.plot( dataGR[0], dataGR[2], ls = '--', c = color[i], lw = 2, label = 'GR'+IDs[i] )

ax.set_xlabel( r'$t/\mathrm{ms}$' )
ax.set_ylabel( r'$H_{1}\,\left[\mathrm{cgs}\right]$' )
ax.grid()

ax.legend()
ax.set_yscale( 'log' )
plt.show()

#figName = 'fig.Rpns070_Rpns040.png'
#plt.savefig( figName, dpi = 300 )
#print( '\n  Saved {:}'.format( figName ) )
