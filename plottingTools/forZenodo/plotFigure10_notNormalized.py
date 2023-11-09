#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from globalVariables import *

Models = {}
with open( dataDirectory + 'fft.dat' ) as f:
    i = -1
    for line in f:
       i += 1
       if i < 2: continue
       x = line.split()
       Models[x[0]] = [ np.float64( x[1] ), np.float64( x[2] ) ]

IDs = [ 'NR2D_M1.4_Rpns070_Rs1.50e2', \
        'NR2D_M1.4_Rpns040_Rs1.20e2', \
        'NR2D_M1.4_Rpns040_Rs1.50e2', \
        'NR2D_M1.4_Rpns040_Rs1.75e2', \
        'NR2D_M1.8_Rpns020_Rs7.00e1', \
        'NR2D_M2.8_Rpns020_Rs6.00e1', \
        'NR2D_M2.8_Rpns020_Rs7.00e1', \
        'GR2D_M1.4_Rpns070_Rs1.50e2', \
        'GR2D_M1.4_Rpns040_Rs1.20e2', \
        'GR2D_M1.4_Rpns040_Rs1.50e2', \
        'GR2D_M1.4_Rpns040_Rs1.75e2', \
        'GR2D_M1.8_Rpns020_Rs7.00e1', \
        'GR2D_M2.8_Rpns020_Rs6.00e1', \
        'GR2D_M2.8_Rpns020_Rs7.00e1' ]

xlim   = [ [ [ -1.00e1, 5.10e2 ], [ -1.0e1, 5.50e2 ] ], \
           [ [ -1.00e0, 9.00e1 ], [ -1.0e1, 1.30e2 ] ] ]
xticks = [ [ [ 0.0, 1.0e2, 2.0e2, 3.0e2, 4.0e2, 5.0e2 ], \
             [ 0.0, 1.0e2, 2.0e2, 3.0e2, 4.0e2, 5.0e2 ] ], \
           [ [ 0.0, 2.5e1, 5.0e1, 7.5e1 ], \
             [ 0.0, 2.5e1, 5.0e1, 7.5e1, 1.0e2, 1.25e2 ] ] ]

ylim   = [ 5.0e10, 5.0e26 ]
yticks = [ 1.0e11, 1.0e16, 1.0e21, 1.0e26 ]

fig, axs = plt.subplots( 2, 2 )

c = [ [ -1, -1 ], [ -1, -1 ] ]
for i in range( len( IDs ) ):

    ID = IDs[i]

    T, dT = Models[ID]

    data = np.loadtxt( dataDirectory + 'LegendrePowerSpectrum_{:}.dat' \
                                       .format( ID ) )

    ind = getRsInd( ID )

    time = data[0][0:ind]
    H1   = data[2][0:ind]

    ind = np.where( time / T < 10.0 )[0]

    T = 1.0
    time = data[0][ind] / T
    H1   = data[2][ind]

    lab = r'$\texttt{{{:}}}$' \
          .format( ID.replace( 'Rs', 'Rsh' ).replace( '2D', '' ) )

    rel = ID[0:1]

    M      = np.float64( ID[6 :9 ] )
    rpns   = np.float64( ID[14:17] )

    xi = M / ( rpns / 20.0 )

    if xi < 1.7:
        j = 0
    else:
        j = 1

    if rel == 'N':
        k = 0
    else:
        k = 1

    c[j][k] = c[j][k] + 1

    axs[j,k].plot( time, H1, \
                   ls = '-', c = color[c[j][k]], lw = 2, label = lab )

for j in range( 2 ):
    for k in range( 2 ):

        axs[j,k].grid()

        axs[j,k].legend( prop = { 'size' : 6.5 } )

        axs[j,k].set_yscale( 'log' )

        axs[j,k].set_xticks( xticks[j][k] )
        axs[j,k].set_xlim( xlim[j][k] )

        axs[j,k].set_yticks( yticks )
        axs[j,k].set_ylim( ylim )

fig.supxlabel( r'$t/\mathrm{ms}$', fontsize = 14, y = 0.01 )
fig.supylabel( r'$H_{1}$ [cgs]'  , fontsize = 14, x = 0.02 )

#plt.show()

figName \
  = figuresDirectory \
      + 'fig.LegendrePowerSpectrum_MultiPanel_vstOverms.pdf'
plt.savefig( figName, dpi = 300 )
print( '\n  Saved {:}'.format( figName ) )

plt.close()

import os
os.system( 'rm -rf __pycache__ ' )