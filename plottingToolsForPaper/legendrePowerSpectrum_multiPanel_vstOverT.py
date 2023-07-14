#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )
from os.path import isfile

from FitPowerToModel import FittingFunction
from UtilitiesModule import GetFileArray, GetData

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color =[ '#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00' ]

indices = {}
with open( '../plottingData/indices_RshCutOff1.10.dat' ) as f:
    i = -1
    for line in f:
        i += 1
        if i < 2: continue
        x = line.split()
        indices[x[0]] = [ np.int64( x[1] ), np.float64( x[2] ) ]

T_aa = {}
T_ac = {}
with open( '../plottingData/T_SASI.dat' ) as f:
    i = -1
    for line in f:
       i += 1
       if i < 3: continue
       x = line.split()
       T_aa[x[0]] = np.float64( x[1] )
       T_ac[x[0]] = np.float64( x[2] )

Rpns = [ '040', '020' ]
M    = [ '1.4', '2.8' ]
Rs   = [ [ '1.20e2', '1.50e2', '1.75e2' ], \
         [ '6.00e1', '7.00e1' ] ]
R    = [ 'NR', 'GR' ]

fig, axs = plt.subplots( len( Rpns ), len( R ) )

lw = 1
ms = 1

for rpns in range( len( Rpns ) ):

    s = rpns
    m = rpns

    for r in range( len( R ) ):

        for rs in range( len( Rs[s] ) ):

            ID \
              = '{:}2D_M{:}_Rpns{:}_Rs{:}' \
                .format( R[r], M[m], Rpns[rpns], Rs[s][rs] )

            dataFileName \
              = '../plottingData/{:}_LegendrePowerSpectrum.dat'.format( ID )

            if not isfile( dataFileName ):
                print( '{:} does not exist. Skipping.' \
                       .format( dataFileName ) )
                continue

            t, P0, P1, P2, P3, P4 \
              = np.loadtxt( dataFileName )

            t  = np.copy( t [0:indices[ID][0]] )
            P1 = np.copy( P1[0:indices[ID][0]] )

            TSASI = T_aa[ID.replace('2D','1D')]

            ind = np.where( t / TSASI <= 10.0 )[0]

            axs[s,r].plot( t[ind] / TSASI, P1[ind], '-', \
                           color = color[rs], \
                           label = r'$\texttt{{{:}}}$' \
                                   .format( ID.replace('2D','') ) )

        axs[s,r].set_yscale( 'log' )

        axs[s,r].tick_params \
          ( top = True, left = True, right = True, bottom = True )
        axs[s,r].grid()
        axs[s,r].set_xlim( -0.5, 10.5 )
        yticks = [ 1.0e11, 1.0e16, 1.0e21, 1.0e26 ]
        axs[s,r].set_ylim( 5.0e10, 5.0e26 )
        axs[s,r].set_yticks( yticks )
        axs[s,r].legend( loc = 4, prop = { 'size' : 8 } )

axs[0,0].set_xticklabels( '' )
axs[0,1].set_xticklabels( '' )
axs[0,1].set_yticklabels( '' )
axs[1,1].set_yticklabels( '' )
fig.supxlabel( r'$t/T$'        , fontsize = 14, y = 0.01 )
fig.supylabel( r'$H_{1}$ [cgs]', fontsize = 14, x = 0.02 )

plt.subplots_adjust( hspace = 0.0, wspace = 0.0 )

#plt.show()
plt.savefig \
  ( '../Figures/fig.LegendrePowerSpectrum_MultiPanel_vstOverT.pdf', \
    dpi = 300 )

import os
os.system( 'rm -rf __pycache__ ' )
