#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from globalVariables import *

IDs = [ '1D_M1.4_Rpns070_Rs1.50e2', \
        '1D_M1.4_Rpns040_Rs1.20e2', \
        '1D_M1.4_Rpns040_Rs1.50e2', \
        '1D_M1.4_Rpns040_Rs1.75e2', \
        '1D_M1.8_Rpns020_Rs7.00e1', \
        '1D_M2.8_Rpns020_Rs6.00e1', \
        '1D_M2.8_Rpns020_Rs7.00e1' ]

# Ratio of signal-speeds

fig, axs = plt.subplots( 2, 1, figsize = (8,4) )

handles = []
labelLC = []
labelHC = []

for i in range( len( IDs ) ):

    ID = IDs[i]

    fileName = dataDirectory + 'signalSpeeds_{:}.dat'.format( ID )

    X1, lambda0_NR, lambda0_GR, lambda1_NR, lambda1_GR, \
    lambda2_NR, lambda2_GR \
      = np.loadtxt( fileName )

    rsh  = np.float64( ID[-6:] )
    rpns = np.int64  ( ID[12:15] )

    eta = ( X1 - rpns ) / ( rsh - rpns )

    if( rpns == 20 ):
        m = 1
    else:
        m = 0

    if i < 4:
        j = i
    else:
        j = i - 4

    l1, \
      = axs[m].plot( eta, lambda1_GR / lambda1_NR, \
                     c = color[j], ls = '-'  )
    l2, \
      = axs[m].plot( eta, lambda2_GR / lambda2_NR, \
                     c = color[j], ls = '--' )
    l3, \
      = axs[m].plot( eta, lambda0_GR / lambda0_NR, \
                     c = color[j], ls = ':'  )

    handles.append( [ l1, l2, l3 ] )

    lab = ID.replace( 'Rs', 'Rsh' )
    if m == 0:
        labelLC.append( r'$\texttt{{{:}}}$'.format( lab ) )
    else:
        labelHC.append( r'$\texttt{{{:}}}$'.format( lab ) )

axs[0].grid()
axs[1].grid()
axs[0].set_xlim( -0.05, 1.05 )
axs[1].set_xlim( -0.05, 1.05 )

handles = np.array( handles )

label1p \
  = r'$\lambda^{r,\mathrm{GR}}_{+}/\lambda^{r,\mathrm{NR}}_{+}$'
label2p \
  = r'$\lambda^{\theta,\mathrm{GR}}_{+}/\lambda^{\theta,\mathrm{NR}}_{+}$'
label0 \
  = r'$\lambda^{r,\mathrm{GR}}_{0}/\lambda^{r,\mathrm{NR}}_{0}$'

label1 = [ label1p, label2p, label0 ]

legend1 = axs[0].legend( handles[0]    , label1 , loc = (0.40,0.02) )
legend2 = axs[0].legend( handles[0:4,0], labelLC, loc = (0.62,0.02) )
legend3 = axs[1].legend( handles[4:,0] , labelHC, loc = (0.62,0.02))

axs[-1].set_xlabel( r'$\eta$', fontsize = 15 )
axs[0].add_artist( legend1 )
axs[0].add_artist( legend2 )
axs[1].add_artist( legend3 )

plt.subplots_adjust( hspace = 0.0 )

axs[0].tick_params \
      ( which = 'both', \
        top = True, left = True, bottom = True, right = True, \
        labeltop    = False, \
        labelleft   = True, \
        labelright  = False, \
        labelbottom = False )
axs[0].set_ylim( 0.8, 1.0 )
axs[1].tick_params \
      ( which = 'both', \
        top = True, left = True, bottom = True, right = True, \
        labeltop    = False, \
        labelleft   = True, \
        labelright  = False, \
        labelbottom = True )
axs[1].set_ylim( 0.45, 1.0 )
yticks = [ 0.5, 0.6, 0.7, 0.8, 0.9 ]
axs[1].set_yticks( yticks )

#plt.show()

figName = figuresDirectory + 'fig.SignalSpeedRatios.pdf'
plt.savefig( figName, dpi = 300, bbox_inches = 'tight' )
print( '\n  Saved {:}'.format( figName ) )

import os
os.system( 'rm -rf __pycache__ ' )
