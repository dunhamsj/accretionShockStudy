#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from globalVariables import *

def addPlot( ID, Rsh, Rpns, text, xlim, ylim, ax ):

    dataFileName \
      = dataDirectory + 'Relaxation_PF_D_{:}.dat'.format( ID )

    Time, Data = np.loadtxt( dataFileName )
    tauAd = Time[-1] / 1.0e2

    ind = np.where( Time[:-1] / tauAd < 100 )[0]
    ax.plot( Time[ind] / tauAd, np.abs( Data[ind] ), 'k.', \
             markersize = 2.0, markevery = 1 )

    ax.text( 0.3, 0.87, text, \
             transform = ax.transAxes, fontsize = 15 )

    ax.set_xlim( xlim )
    ax.set_ylim( ylim )

    ax.set_yscale( 'log' )

    ax.grid( axis = 'x' )

    return

fig, axs = plt.subplots( 2, 1 )

xlim = [ -5.0, +105 ]

# Low xi

ID   = 'GR1D_M1.4_Rpns040_Rs1.20e2_nX0280'
Rsh  = 1.20e2
Rpns = 4.00e1
text = r'$\texttt{GR1D\_M1.4\_Rpns040\_Rsh1.20e2}$'
ylim = 1.0e-6

dataFileName      = dataDirectory + 'Relaxation_PF_D_{:}.dat'.format( ID )
Time, Data        = np.loadtxt( dataFileName )

addPlot( ID, Rsh, Rpns, text, xlim, ylim, axs[0] )

axs[0].tick_params \
  ( which = 'both', \
    top = True, left = True, bottom = True, right = True, \
    labeltop    = False, \
    labelleft   = True, \
    labelright  = False, \
    labelbottom = False )

# High xi

ID   = 'GR1D_M2.8_Rpns020_Rs6.00e1_nX0280'
Rsh  = 6.00e1
Rpns = 2.00e1
text = r'$\texttt{GR1D\_M2.8\_Rpns020\_Rsh6.00e1}$'
ylim = 1.0e-13

dataFileName = dataDirectory + 'Relaxation_PF_D_{:}.dat'.format( ID )
Time, Data   = np.loadtxt( dataFileName )

addPlot( ID, Rsh, Rpns, text, xlim, ylim, axs[1] )

axs[1].tick_params \
  ( which = 'both', \
    top = True, left = True, bottom = True, right = True, \
    labeltop    = False, \
    labelleft   = True, \
    labelright  = False, \
    labelbottom = True )

axs[1].set_xlabel( r'$t/\tau_{\mathrm{ad}}$', fontsize = 15 )

ylabel \
= r'$\max\limits_{r\in\left[R_{\mathrm{PNS}},1.5\,R_{\mathrm{sh}}\right]}$' \
    + r'$\left|\dot{\rho}\left(t\right)/\rho\left(t\right)\right|$' \
           + r'$\ \left[\mathrm{ms}^{-1}\right]$'

fig.supylabel( ylabel, x = -0.01, fontsize = 15 )

plt.subplots_adjust( hspace = 0 )

#plt.show()

figName = figuresDirectory + 'fig.Relaxation.pdf'
plt.savefig( figName, dpi = 300, bbox_inches = 'tight' )
print( '\n  Saved {:}'.format( figName ) )

plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
