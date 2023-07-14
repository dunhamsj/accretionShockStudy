#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )
from os.path import isfile

from FitPowerToModel import FittingFunction
from UtilitiesModule import GetFileArray, GetData

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = ['#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00']

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

lw = 1
ms = 1

for rpns in range( len( Rpns ) ):

    s = rpns
    m = rpns

    for rs in range( len( Rs[s] ) ):

        fig, ax = plt.subplots( 1, 1, figsize = (2,2) )

        for r in range( len( R ) ):

            ID \
              = '{:}2D_M{:}_Rpns{:}_Rs{:}' \
                .format( R[r], M[m], Rpns[rpns], Rs[s][rs] )

            dataFileName \
              = '../plottingData/{:}_LegendrePowerSpectrum.dat'.format( ID )

            if not isfile( dataFileName ):
                print( '{:} does not exist. Skipping.' \
                       .format( dataFileName ) )
                plt.close()
                continue

            t, P0, P1, P2, P3, P4 \
              = np.loadtxt( dataFileName )

            t  = np.copy( t [0:indices[ID][0]] )
            P1 = np.copy( P1[0:indices[ID][0]] )

            TSASI = T_aa[ID.replace('2D','1D')]

            ind = np.where( t / TSASI <= 10.0 )[0]

            if s == 0 and rs == 0:

                ax.plot( t[ind], P1[ind], '-', \
                         color = color[r], \
                         label = R[r] )

            else:

                ax.plot( t[ind], P1[ind], '-', \
                         color = color[r] )

        ax.set_title( r'$\texttt{{{:}}}$'.format( ID[5:] ), \
                      fontsize = 9 )

        ax.set_yscale( 'log' )

        ax.tick_params \
          ( top = True, left = True, right = True, bottom = True )
        ax.grid()

        if s == 0:
            if   rs == 0:
                xticks = [ 0.0, 1.0e2, 2.0e2 ]
                ax.set_xticks( xticks )
                ax.set_xlim( -1.0e1, 2.2e2 )
            elif rs == 1:
                xticks = [ 0.0, 1.0e2, 2.0e2, 3.0e2 ]
                ax.set_xticks( xticks )
                ax.set_xlim( -2.0e1, 3.75e2 )
            elif rs == 2:
                xticks = [ 0.0, 1.0e2, 2.0e2, 3.0e2, 4.0e2, 5.0e2 ]
                ax.set_xticks( xticks )
                ax.set_xlim( -2.5e1, 5.25e2 )
        elif s == 1:
            if   rs == 0:
                xticks = [ 0.0, 1.0e1, 2.0e1, 3.0e1, 4.0e1, 5.0e1 ]
                ax.set_xticks( xticks )
                ax.set_xlim( -5.0e0, 5.5e1 )
            elif rs == 1:
                xticks = [ 0.0, 1.0e1, 2.0e1, 3.0e1, 4.0e1, \
                           5.0e1, 6.0e1, 7.0e1, 8.0e1 ]
                ax.set_xticks( xticks )
                ax.set_xlim( -5.0e0, 8.5e1 )
        yticks = [ 1.0e11, 1.0e16, 1.0e21, 1.0e26 ]
        ax.set_yticks( yticks )
        ax.set_ylim( 5.0e10, 5.0e26 )

        if s == 0 and rs == 0:
            ax.legend( loc = 4, prop = { 'size' : 8 } )

        ax.set_xlabel( r'$t$ [ms]'     , fontsize = 14 )
        ax.set_ylabel( r'$H_{1}$ [cgs]', fontsize = 14 )

        #plt.show()
        plt.savefig \
        ( '../Figures/fig.LegendrePowerSpectrum_vst_{:}.pdf' \
          .format( ID[5:] ), dpi = 300 )
        plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
