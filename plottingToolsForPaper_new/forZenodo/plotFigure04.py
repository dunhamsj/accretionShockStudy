#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from globalVariables import *

IDs = [ 'GR1D_M1.4_Rpns040_Rs1.20e2_nX0140', \
        'GR1D_M1.4_Rpns040_Rs1.20e2_nX0280', \
        'GR1D_M1.4_Rpns040_Rs1.20e2_nX0560', \
        'GR1D_M1.4_Rpns040_Rs1.20e2_nX1120', \
        'GR1D_M2.8_Rpns020_Rs6.00e1_nX0140', \
        'GR1D_M2.8_Rpns020_Rs6.00e1_nX0280', \
        'GR1D_M2.8_Rpns020_Rs6.00e1_nX0560', \
        'GR1D_M2.8_Rpns020_Rs6.00e1_nX1120' ]

fig, axs = plt.subplots( 2, 1 )

for i in range( len( IDs ) ):

    ID = IDs[i]

    rpns = np.int64  ( ID[14:17] )
    rsh  = np.float64( ID[20:26] )
    nX = np.int64( ID[-4:] )

    dataFileName = dataDirectory \
                     + 'ShockRadiusVsTime_{:}.dat'.format( ID )

    t, RsAve, RsMin, RsMax = np.loadtxt( dataFileName )
    tauAd = t[-1] / 1.0e2

    dr = ( 1.5 * rsh - rpns ) / np.float64( nX )

    lab = r'$dr={:.2f}\ \mathrm{{km}}$'.format( dr )
    if i < 4:
        m = 0
    else:
        m = 1

    axs[m].plot( t[:-1] / tauAd, ( RsAve[:-1] - RsAve[0] ) / RsAve[0], \
                 label = lab, markevery = 10 )

text = r'$\texttt{GR1D\_M1.4\_Rpns040\_Rsh1.20e2}$'
axs[0].text( 0.06, 0.87, text, \
             transform = axs[0].transAxes, fontsize = 13 )

text = r'$\texttt{GR1D\_M2.8\_Rpns020\_Rsh6.00e1}$'
axs[1].text( 0.06, 0.87, text, \
             transform = axs[1].transAxes, fontsize = 13 )

axs[0].tick_params \
  ( which = 'both', \
    top = True, left = True, bottom = True, right = True, \
    labeltop    = False, \
    labelleft   = True, \
    labelright  = False, \
    labelbottom = False )

axs[1].tick_params \
  ( which = 'both', \
    top = True, left = True, bottom = True, right = True, \
    labeltop    = False, \
    labelleft   = True, \
    labelright  = False, \
    labelbottom = True )

xlim = [ -5, 105 ]
axs[0].set_xlim( xlim )
axs[1].set_xlim( xlim )

axs[1].set_xlabel( r'$t/\tau_{\mathrm{ad}}$' )

axs[0].grid( axis = 'x' )
axs[1].grid( axis = 'x' )

axs[0].legend( loc = (0.6,0.49) )
axs[1].legend( loc = (0.6,0.53) )

ylabel \
  = r'$\left(R_{\mathrm{sh}}\left(t\right)-R_{\mathrm{sh}}\left(0\right)\right)$' \
      + r'$/R_{\mathrm{sh}}\left(0\right)$'
fig.supylabel( ylabel )

plt.subplots_adjust( hspace = 0 )

#plt.show()

figName = figuresDirectory + 'fig.RadialResolution.pdf'
plt.savefig( figName, dpi = 300, bbox_inches = 'tight' )
print( '\n  Saved {:}'.format( figName ) )

import os
os.system( 'rm -rf __pycache__ ' )
