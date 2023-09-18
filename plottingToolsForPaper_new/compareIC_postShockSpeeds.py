#!/usr/bin/env python3

from sys import argv
import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from UtilitiesModule import GetFileArray, GetData
from globalVariables import *

IDs = [ '1D_M1.4_Rpns040_Rs1.20e2', \
        '1D_M1.4_Rpns040_Rs1.50e2', \
        '1D_M1.4_Rpns040_Rs1.75e2', \
        '1D_M2.8_Rpns020_Rs6.00e1', \
        '1D_M2.8_Rpns020_Rs7.00e1' ]

verbose = False

c = 2.99792458e5

#### ====== End of User Input =======

# Generate data files

plotfileDirectory = plotfileRootDirectory + '1D/'

generateData = False
plotData     = True

if generateData:

    for i in range( len( IDs ) ):

        ID = IDs[i]

        # GR

        GRID = 'GR' + ID

        plotfileDirectory_GR = plotfileDirectory + GRID + '/'

        plotfileBaseName_GR = GRID + '.plt'

        plotfile_GR = plotfileDirectory_GR + plotfileBaseName_GR + '00000000/'

        V, dataUnits, X1, X2, X3, dX1, dX2, dX3, xL, xH, nX, time \
          = GetData( plotfileDirectory_GR, plotfileBaseName_GR, 'PF_V1', \
                    'spherical', True, \
                    ReturnTime = True, ReturnMesh = True, Verbose = False )
        V  = np.copy( V [:,0,0] )
        X1 = np.copy( X1[:,0,0] )

        Cs, dataUnits \
          = GetData( plotfileDirectory_GR, plotfileBaseName_GR, 'AF_Cs', \
                    'spherical', True )
        Cs = np.copy( Cs[:,0,0] )

        alpha, dataUnits \
          = GetData( plotfileDirectory_GR, plotfileBaseName_GR, 'GF_Alpha', \
                    'spherical', True )
        alpha = np.copy( alpha[:,0,0] )

        Gm11, dataUnits \
          = GetData( plotfileDirectory_GR, plotfileBaseName_GR, 'GF_Gm_11', \
                    'spherical', True )
        Gm11 = np.copy( Gm11[:,0,0] )

        Gm22, dataUnits \
          = GetData( plotfileDirectory_GR, plotfileBaseName_GR, 'GF_Gm_22', \
                    'spherical', True )
        Gm22 = np.copy( Gm22[:,0,0] )

        VSq = Gm11 * V**2
        lambda0_GR = alpha * V
        lambda1_GR = alpha / ( 1.0 - VSq * Cs**2 / c**4 ) \
                       * ( V * ( 1.0 - Cs**2 / c**2 ) \
                       + Cs * np.sqrt( ( 1.0 - VSq / c**2 ) \
                       * ( 1.0 / Gm11 * ( 1.0 - VSq * Cs**2 / c**4 ) \
                       - V / c * V / c * ( 1.0 - Cs**2 / c**2 ) ) ) )
        # Assume V2 = 0
        lambda2_GR = alpha / ( 1.0 - VSq * Cs**2 / c**4 ) \
                       * Cs * np.sqrt( ( 1.0 - VSq / c**2 ) \
                       * 1.0 / Gm22 * ( 1.0 - VSq * Cs**2 / c**4 ) )
        lambda0_GR = np.copy( ( lambda0_GR * np.sqrt( Gm11 ) ) )
        lambda1_GR = np.copy( ( lambda1_GR * np.sqrt( Gm11 ) ) )
        lambda2_GR = np.copy( ( lambda2_GR * np.sqrt( Gm22 ) ) )

        # NR

        NRID = 'NR' + ID

        plotfileDirectory_NR = plotfileDirectory + NRID + '/'

        plotfileBaseName_NR = NRID + '.plt'

        plotfile_NR = plotfileDirectory_NR + plotfileBaseName_NR + '00000000/'

        V, dataUnits \
          = GetData( plotfileDirectory_NR, plotfileBaseName_NR, 'PF_V1', \
                    'spherical', True )
        V  = np.copy( V [:,0,0] )

        Cs, dataUnits \
          = GetData( plotfileDirectory_NR, plotfileBaseName_NR, 'AF_Cs', \
                    'spherical', True )
        Cs = np.copy( Cs[:,0,0] )

        Gm11, dataUnits \
          = GetData( plotfileDirectory_GR, plotfileBaseName_GR, 'GF_Gm_11', \
                    'spherical', True )
        Gm11 = np.copy( Gm11[:,0,0] )

        Gm22, dataUnits \
          = GetData( plotfileDirectory_GR, plotfileBaseName_GR, 'GF_Gm_22', \
                    'spherical', True )
        Gm22 = np.copy( Gm22[:,0,0] )

        lambda0_NR = V
        lambda1_NR = V + Cs * np.sqrt( 1.0 / Gm11 )
        # Assume V2 = 0
        lambda2_NR = Cs * np.sqrt( 1.0 / Gm22 )
        lambda0_NR = np.copy( ( lambda0_NR * np.sqrt( Gm11 ) ) )
        lambda1_NR = np.copy( ( lambda1_NR * np.sqrt( Gm11 ) ) )
        lambda2_NR = np.copy( ( lambda2_NR * np.sqrt( Gm22 ) ) )

        rsh  = np.float64( ID[-6:] )
        rpns = np.int64  ( ID[12:15] )
        ind = np.where( ( X1 < rsh ) & ( X1 > rpns ) )[0][:-1]

        X1         = np.copy( X1        [ind] )
        lambda0_GR = np.copy( lambda0_GR[ind] )
        lambda1_GR = np.copy( lambda1_GR[ind] )
        lambda2_GR = np.copy( lambda2_GR[ind] )
        lambda0_NR = np.copy( lambda0_NR[ind] )
        lambda1_NR = np.copy( lambda1_NR[ind] )
        lambda2_NR = np.copy( lambda2_NR[ind] )

        signalSpeeds = np.vstack( ( X1, lambda0_NR, lambda0_GR, \
                                        lambda1_NR, lambda1_GR, \
                                        lambda2_NR, lambda2_GR ) )

        header = '{:} X1_C, lambda0_NR, lambda0_GR, lambda1_NR, lambda1_GR, ' \
                 .format( ID ) + 'lambda2_NR, lambda2_GR'

        fileName = dataDirectory + '{:}_signalSpeeds.dat'.format( ID )

        np.savetxt( fileName, signalSpeeds, header = header )

if plotData:

    ### Plotting

    # colorblind-friendly palette: https://gist.github.com/thriveth/8560036
    color = ['#377eb8', '#ff7f00', '#4daf4a', \
             '#f781bf', '#a65628', '#984ea3', \
             '#999999', '#e41a1c', '#dede00']

    # Ratio of signal-speeds

    fig, axs = plt.subplots( 2, 1, figsize = (8,4) )

    handles = []
    labelLC = []
    labelHC = []

    for i in range( len( IDs ) ):

        ID = IDs[i]

        fileName = dataDirectory + '{:}_signalSpeeds.dat'.format( ID )

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

        if i < 3:
            j = i
        else:
            j = i - 3

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
    axs[0].set_xlim( -0.1, 1.1 )
    axs[1].set_xlim( -0.1, 1.1 )

    handles = np.array( handles )

    label1p = r'$\lambda^{r,\mathrm{GR}}_{+}/\lambda^{r,\mathrm{NR}}_{+}$'
    label2p = r'$\lambda^{\theta,\mathrm{GR}}_{+}/\lambda^{\theta,\mathrm{NR}}_{+}$'
    label0  = r'$\lambda^{r,\mathrm{GR}}_{0}/\lambda^{r,\mathrm{NR}}_{0}$'

    label1 = [ label1p, label2p, label0 ]

    legend1 = axs[0].legend( handles[0]    , label1 , loc = 8 )
    legend2 = axs[0].legend( handles[0:3,0], labelLC, loc = 4 )
    legend3 = axs[1].legend( handles[3:,0] , labelHC, loc = 4 )

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

    plt.show()

    #figName = figuresDirectory + 'fig.SignalSpeedRatios.pdf'
    #plt.savefig( figName, dpi = 300 )
    #print( '\n  Saved {:}'.format( figName ) )

import os
os.system( 'rm -rf __pycache__ ' )
