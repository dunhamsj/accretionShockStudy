#!/usr/bin/env python3

import yt
import numpy as np
import matplotlib.pyplot as plt
import os
plt.style.use( 'publication.sty' )

from UtilitiesModule import Overwrite, GetData, GetFileArray
from globalVariables import *

yt.funcs.mylog.setLevel(40) # Suppress initial yt output to screen

def MakeLineOutPlot( plotfileDirectory, plotfileBaseName, entropyThreshold ):

    plotfileArray = GetFileArray( plotfileDirectory, plotfileBaseName )

    data, DataUnit, r, X2_C, X3_C, dX1, dX2, dX3, xL, xH, nX, time \
      = GetData( plotfileDirectory, plotfileBaseName, 'PolytropicConstant', \
                 'spherical', True, argv = ['a','0'], \
                 ReturnTime = True, ReturnMesh = True, Verbose = True )

    fig2, ax2 = plt.subplots()
    ax2.semilogy( r[:,0,0], data[:,0,0], 'k-' )
    ax2.text( 0.5, 0.7, 'Time = {:.3e}'.format( time ), \
              transform = ax2.transAxes )
    ax2.axhline( entropyThreshold, label = 'Shock radius cut-off' )

    plt.legend()
#    plt.savefig( 'entropyThresholdCheck.png', dpi = 300 )
    plt.show()
    plt.close()

    return


def MakeDataFile \
      ( plotfileDirectory, plotfileBaseName, dataFileName, \
        entropyThreshold, markEvery = 1, forceChoice = False, OW = True ):

    OW = Overwrite( dataFileName, ForceChoice = forceChoice, OW = OW )

    if not OW: return

    print( '\n plotfileDirectory: ', plotfileDirectory )
    print( '\n  Creating {:}'.format( dataFileName ) )
    print(   '  --------' )

    plotfileArray = GetFileArray( plotfileDirectory, plotfileBaseName )

    plotfileArray = plotfileArray[0::markEvery]

    data, DataUnit, r, X2_C, X3_C, dX1, dX2, dX3, xL, xH, nX, time \
      = GetData( plotfileDirectory, plotfileBaseName, 'PolytropicConstant', \
                 'spherical', True, \
                 ReturnTime = True, ReturnMesh = True, Verbose = False )

    nSS = plotfileArray.shape[0]

    Data = np.empty( (nSS,nX[0],nX[1],nX[2]), np.float64 )

    Time = np.empty( nSS, np.float64 )

    Volume = np.zeros( nSS, np.float64 )
    RsMin  = np.empty( nSS, np.float64 )
    RsMax  = np.empty( nSS, np.float64 )

    for i in range( nSS ):

        print( '    {:}/{:}'.format( i,nSS) )

        plotfile = plotfileDirectory + plotfileArray[i]

        Data[i], dataUnits, X1, X2, X3, dX1, dX2, dX3, xL, xH, nX, Time[i] \
          = GetData( plotfileDirectory, plotfileBaseName, \
                     'PolytropicConstant', \
                     'spherical', True, argv = ['a',plotfile[-8:]], \
                     ReturnTime = True, ReturnMesh = True, Verbose = False )

        X1 = np.copy( X1[:,0,0] )
        X2 = np.copy( X2[0,:,0] )
        dX1 = np.copy( dX1[:,0,0] )
        dX2 = np.copy( dX2[0,:,0] )

        ind = np.where( Data[i] < entropyThreshold )[0]
        RsMin[i] = X1[ind.min()]

        ind = np.where( Data[i] > entropyThreshold )[0]
        RsMax[i] = X1[ind.max()]

        for iX1 in range( nX[0] ):
            for iX2 in range( nX[1] ):
                for iX3 in range( nX[2] ):

                    if( Data[i,iX1,iX2,iX3] > entropyThreshold ):

                        if( nX[1] > 1 ):

                            Volume[i] \
                              += 2.0 * np.pi \
                                   * 1.0 / 3.0 * ( ( X1[iX1] + dX1[iX1] )**3 \
                                                       - X1[iX1]**3 ) \
                                   * ( np.cos( X2[iX2] ) \
                                         - np.cos( X2[iX2] + dX2[iX2] ) )

                        else:

                            Volume[i] \
                              += 4.0 * np.pi \
                                   * 1.0 / 3.0 * ( ( X1[iX1] + dX1[iX1] )**3 \
                                                       - X1[iX1]**3 )

        Rs = ( Volume[i] / ( 4.0 / 3.0 * np.pi ) )**( 1.0 / 3.0 )
        if RsMin[i] >= Rs: RsMin[i] = Rs
        if RsMax[i] <= Rs: RsMax[i] = Rs

    # 4/3 * pi * Rs^3 = Volume
    # ==> Rs = ( Volume / ( 4/3 * pi ) )^( 1 / 3 )
    RsAve = ( Volume / ( 4.0 / 3.0 * np.pi ) )**( 1.0 / 3.0 )

    header = 'Generated from shockRadius.py\n' \
               + 'Time [ms], RsAve [km], RsMin [km], RsMax [km]'
    np.savetxt( dataFileName, \
                np.vstack( ( Time, RsAve, RsMin, RsMax ) ), \
                header = header )

    return


if __name__ == "__main__":

    do1D         = False
    generateData = True
    plotData     = True

    if do1D:

        IDs = [ 'GR1D_M1.4_Rpns040_Rs1.20e2_nX0140', \
                'GR1D_M1.4_Rpns040_Rs1.20e2_nX0280', \
                'GR1D_M1.4_Rpns040_Rs1.20e2_nX0560', \
                'GR1D_M1.4_Rpns040_Rs1.20e2_nX1120', \
                'GR1D_M2.8_Rpns020_Rs6.00e1_nX0140', \
                'GR1D_M2.8_Rpns020_Rs6.00e1_nX0280', \
                'GR1D_M2.8_Rpns020_Rs6.00e1_nX0560', \
                'GR1D_M2.8_Rpns020_Rs6.00e1_nX1120' ]

    else:

        IDs = [ 'NR2D_M1.4_Rpns040_Rs1.20e2', \
                'NR2D_M1.4_Rpns040_Rs1.50e2', \
                'NR2D_M1.4_Rpns040_Rs1.75e2', \
                'GR2D_M1.4_Rpns040_Rs1.20e2', \
                'GR2D_M1.4_Rpns040_Rs1.50e2', \
                'GR2D_M1.4_Rpns040_Rs1.75e2', \
                'NR2D_M2.8_Rpns020_Rs6.00e1', \
                'NR2D_M2.8_Rpns020_Rs7.00e1', \
                'GR2D_M2.8_Rpns020_Rs6.00e1', \
                'GR2D_M2.8_Rpns020_Rs7.00e1' ]
        IDs = [ 'GR2D_M1.8_Rpns020_Rs7.00e1' ]

    if( generateData ):

        forceChoice = True
        OW          = True

        for i in range( len( IDs ) ):

            ID = IDs[i]

            if do1D:

                if i < 4:
                    plotfileDirectory \
                      = plotfileRootDirectory \
                          + 'resolutionStudy_lowCompactness/' + ID + '/'
                else:
                    plotfileDirectory \
                      = plotfileRootDirectory \
                          + 'resolutionStudy_highCompactness/' + ID + '/'

            else:

                plotfileDirectory \
                  = plotfileRootDirectory + '2D/{:}/'.format( ID )

            plotfileBaseName = ID + '.plt'
            entropyThreshold = 1.0e15

            if not os.path.isdir( plotfileDirectory ): continue

            #MakeLineOutPlot \
            #  ( plotfileDirectory, plotfileBaseName, entropyThreshold )

            dataFileName = dataDirectory \
                             + 'ShockRadiusVsTime_{:}.dat'.format( ID )
            MakeDataFile \
              ( plotfileDirectory, plotfileBaseName, dataFileName, \
                entropyThreshold, markEvery = 1, \
                forceChoice = forceChoice, \
                OW = OW )

    if( plotData ):

        fig, axs = plt.subplots( 2, 1 )

        for i in range( len( IDs ) ):

            ID = IDs[i]

            rpns = np.int64  ( ID[14:17] )
            rsh  = np.float64( ID[20:26] )
            if do1D:
                nX = np.int64( ID[-4:] )
            else:
                nX = -1

            dataFileName = dataDirectory \
                             + 'ShockRadiusVsTime_{:}.dat'.format( ID )

            t, RsAve, RsMin, RsMax = np.loadtxt( dataFileName )
            if do1D:
                tauAd = t[-1] / 1.0e2
            else:
                tauAd = 1.0

            dr = ( 1.5 * rsh - rpns ) / np.float64( nX )

            if do1D:
                lab = r'$dr={:.2f}\ \mathrm{{km}}$'.format( dr )
                if i < 4:
                    m = 0
                else:
                    m = 1
            else:
                lab = ID
                if i < 6:
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

        if do1D:
            lb = False
        else:
            lb = True

        axs[0].tick_params \
          ( which = 'both', \
            top = True, left = True, bottom = True, right = True, \
            labeltop    = False, \
            labelleft   = True, \
            labelright  = False, \
            labelbottom = lb )

        axs[1].tick_params \
          ( which = 'both', \
            top = True, left = True, bottom = True, right = True, \
            labeltop    = False, \
            labelleft   = True, \
            labelright  = False, \
            labelbottom = True )

        if do1D:
            xlim = [ -5, 105 ]
            axs[0].set_xlim( xlim )
            axs[1].set_xlim( xlim )

        if do1D:
            axs[1].set_xlabel( r'$t/\tau_{\mathrm{ad}}$' )
        else:
            axs[1].set_xlabel( r'$t/\mathrm{ms}$' )

        axs[0].grid( axis = 'x' )
        axs[1].grid( axis = 'x' )

        axs[0].legend( loc = (0.6,0.49) )
        axs[1].legend( loc = (0.6,0.53) )

        ylabel \
          = r'$\left(R_{\mathrm{sh}}\left(t\right)-R_{\mathrm{sh}}\left(0\right)\right)$' \
              + r'$/R_{\mathrm{sh}}\left(0\right)$'
        fig.supylabel( ylabel )

        if do1D: plt.subplots_adjust( hspace = 0 )

        plt.show()

        #figName = figuresDirectory + 'fig.RadialResolution.pdf'
        #plt.savefig( figName, dpi = 300 )
        #print( '\n  Saved {:}'.format( figName ) )

    import os
    os.system( 'rm -rf __pycache__ ' )
