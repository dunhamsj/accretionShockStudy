#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from globalVariables import *

IDs = [ '2D_M1.4_Rpns070_Rs1.50e2', \
        '2D_M1.4_Rpns040_Rs1.50e2', \
        '2D_M1.8_Rpns020_Rs7.00e1', \
        '2D_M2.8_Rpns020_Rs6.00e1', \
        '2D_M2.8_Rpns020_Rs7.00e1' ]
xlim = [ [ -1.0e1, 2.5e2 ], \
         [ -2.0e1, 3.5e2 ], \
         [ -1.0e1, 1.5e2 ], \
         [ -5.0e0, 6.0e1 ], \
         [ -5.0e0, 8.5e1 ] ]
xticks = [ [ 0.0, 1.0e2, 2.0e2 ], \
           [ 0.0, 1.0e2, 2.0e2, 3.0e2 ], \
           [ 0.0, 5.0e1, 1.0e2, 1.50e2 ], \
           [ 0.0, 1.0e1, 2.0e1, 3.0e1, 4.0e1, 5.0e1 ], \
           [ 0.0, 1.0e1, 2.0e1, 3.0e1, 4.0e1, \
             5.0e1, 6.0e1, 7.0e1, 8.0e1 ] ]
yticks = [ 1.0e11, 1.0e16, 1.0e21, 1.0e26 ]
ylim  = [ 5.0e10, 5.0e26 ]

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = ['#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00']

def getRsInd( ID ):

    RsFileName \
      = dataDirectory + 'ShockRadiusVsTime_{:}.dat'.format( ID )
    Time, RsAve, RsMin, RsMax = np.loadtxt( RsFileName )

    # Remove unperturbed file
    Time  = np.copy( Time [:-1] )
    RsAve = np.copy( RsAve[:-1] )
    RsMin = np.copy( RsMin[:-1] )
    RsMax = np.copy( RsMax[:-1] )

    ind = np.where( RsMax > 1.1 * RsAve[0] )[0]
    if ind.shape[0] == 0:
        ind = -1
    else:
        ind = ind[0]

    return ind

for i in range( len( IDs ) ):

    fig, ax = plt.subplots( 1, 1, figsize = (2,2) )

    ID = IDs[i]

    dataNR = np.loadtxt( dataDirectory + 'LegendrePowerSpectrum_{:}.dat' \
                                         .format( 'NR' + ID ) )
    dataGR = np.loadtxt( dataDirectory + 'LegendrePowerSpectrum_{:}.dat' \
                                         .format( 'GR' + ID ) )

    indNR = getRsInd( 'NR' + ID )
    indGR = getRsInd( 'GR' + ID )

    IDD = ID[3:].replace( 'Rs', 'Rsh' )
    ax.set_title( r'$\texttt{{{:}}}$'.format( IDD ), fontsize = 9 )

    M_s    = ID[4:7]
    M      = np.float64( M_s )
    rpns_s = ID[12:15]
    rpns   = np.int64  ( rpns_s )

    xi = '{:.1f}'.format( M / ( rpns / 20.0 ) )
    ax.text( 0.5 * sum( xlim[i] ), 1.0e12, r'$\xi={:}$'.format( xi ) )

    ax.plot( dataNR[0][0:indNR], dataNR[2][0:indNR], \
             ls = '-', c = color[0], lw = 2, label = 'NR' )
    ax.plot( dataGR[0][0:indGR], dataGR[2][0:indGR], \
             ls = '-', c = color[1], lw = 2, label = 'GR' )

    ax.set_xlabel( r'$t$ [ms]'                          , fontsize = 14 )
    ax.set_ylabel( r'$H_{1}\,\left[\mathrm{cgs}\right]$', fontsize = 14 )
    ax.grid()

    if i == 0: ax.legend()

    ax.set_yscale( 'log' )

    ax.set_xticks( xticks[i] )
    ax.set_xlim( xlim[i] )

    ax.set_yticks( yticks )
    ax.set_ylim( ylim )

    #plt.show()

    figName \
      = figuresDirectory \
          + 'fig.LegendrePowerSpectrum_vst_{:}.pdf' \
             .format( ID.replace( '2D_', '' ).replace( 'Rs', 'Rsh' ) )
    plt.savefig( figName, dpi = 300 )
    print( '\n  Saved {:}'.format( figName ) )

    plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
