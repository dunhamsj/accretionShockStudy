#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )
import os

from UtilitiesModule import Overwrite, GetData, GetFileArray
from computeTimeScales import ComputeTimeScales

def getRelaxationData( plotfileDirectory, ID, field, nX, forceChoice, ow ):

    dataFileName = '../plottingData/{:}_Relaxation_{:}.dat' \
                   .format( ID, field )

    ow = Overwrite( dataFileName, ForceChoice = forceChoice, OW = ow )

    if ow:

        plotfileBaseName = ID + '.plt'

        plotfileArray = GetFileArray( plotfileDirectory, plotfileBaseName )

        nSS = plotfileArray.shape[0]

        ind = np.linspace( 0, nSS-1, nSS, dtype = np.int64 )

        def loop( iLo, iHi, nodalData, Time, iProc, \
                  return_data, return_time ):

            for i in range( iLo, iHi ):

                N = iHi - iLo
                j = i - iLo

                if j % 10 == 0:
                    print( 'File {:d}/{:d}'.format( j, N ) )

                plotfile = plotfileDirectory + plotfileArray[i]

                Time[j], data, dataUnits, r, theta, phi, \
                dr, dtheta, dphi, nX \
                  = GetData( plotfile, field )

                nodalData[j] = np.copy( data[:,0,0] )

            return

        nodalData = np.zeros( (nSS,nX), np.float64 )
        DiffData  = np.zeros( (nSS-1) , np.float64 )
        Time      = np.zeros( (nSS)   , np.float64 )

        loop( 0, nSS-1, nodalData, Time, 0, 0, 0 )
        Den = np.empty( (nX), np.float64 )

        for i in range( DiffData.shape[0] ):

            Num = np.abs( nodalData[i+1] - nodalData[i] ) \
                    / ( Time[i+1] - Time[i] )

            for j in range( Num.shape[0] ):

                Den[j] \
                  = max( 1.0e-17, \
                         0.5 * np.abs( nodalData[i+1,j] + nodalData[i,j] ) )

            DiffData[i] = ( Num / Den ).max()

        np.savetxt( dataFileName, np.vstack( (Time[:-1],DiffData) ) )

        del plotfileBaseName, plotfileArray, \
            nodalData, DiffData, Time, Den

    Time, Data = np.loadtxt( dataFileName )

    return Time, Data


def getShockRadiusData \
      ( plotfileDirectory, plotfileBaseName, dataFileName, \
        entropyThreshold, markEvery = 1, forceChoice = False, ow = True ):

    ow = Overwrite( dataFileName, ForceChoice = forceChoice, OW = ow )

    if not ow: return

    print( '\n  Creating {:}'.format( dataFileName ) )
    print(   '  --------' )

    plotfileArray = GetFileArray( plotfileDirectory, plotfileBaseName )

    plotfileArray = plotfileArray[0::markEvery]

    # Just to get number of elements
    plotfile = plotfileDirectory + plotfileArray[0]
    dmy0, dmy1, dmy2, dmy3, dmy4, dmy5, dmy6, dmy7, dmy8, nX \
      = GetData( plotfile, 'PolytropicConstant' )

    nSS = plotfileArray.shape[0]

    Data = np.empty( (nSS,nX[0],nX[1],nX[2]), np.float64 )

    Time = np.empty( nSS, np.float64 )

    Volume = np.zeros( nSS, np.float64 )
    RsMin  = np.empty( nSS, np.float64 )
    RsMax  = np.empty( nSS, np.float64 )

    for i in range( nSS ):

        print( '    {:}/{:}'.format( i,nSS) )

        plotfile = plotfileDirectory + plotfileArray[i]

        Time[i], Data[i], dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
          = GetData( plotfile, 'PolytropicConstant' )

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

    np.savetxt( dataFileName, \
                np.vstack( ( Time, RsAve, RsMin, RsMax ) ) )

    return


if __name__ == "__main__":

    fig, axs = plt.subplots( 2, 1 )

    stage = 'earlyStage'
#    stage = 'lateStage'

    if stage == 'earlyStage':

        rootDirectory = '/lump/data/accretionShockStudy/newData/resolutionStudy_earlyStage/'

        IDD  = 'GR1D_M1.4_Rpns040_Rs1.20e2'
        nX   = [ '0140', '0280', '0560', '1120' ]
        nXX  = 280
        Rs   = 1.20e2
        Rpns = 4.00e1
        text = r'$\texttt{GR1D\_M1.4\_Rpns040\_Rs1.20e2}$'
        ylim = 1.0e-6

    elif stage == 'lateStage':

        rootDirectory = '/lump/data/accretionShockStudy/newData/resolutionStudy_lateStage/'

        IDD  = 'GR1D_M2.8_Rpns020_Rs6.00e1'
        nX   = [ '0140', '0280', '0560', '1120' ]
        nXX  = 280
        Rs   = 6.00e1
        Rpns = 2.00e1
        text = r'$\texttt{GR1D\_M2.8\_Rpns020\_Rs6.00e1}$'
        ylim = 1.0e-13

    ID = IDD + '_nX{:}'.format( nX[1] )
    plotfileDirectory = rootDirectory + ID + '/'
    plotfileBaseName = ID + '.plt'
    tauAd, tauAc \
      = ComputeTimeScales \
          ( plotfileDirectory + plotfileBaseName + '00000000/', \
            Rpns, Rs, 'GR' )

    for i in range( len( nX ) ):

        ID = IDD + '_nX{:}'.format( nX[i] )
        plotfileDirectory = rootDirectory + ID + '/'
        plotfileBaseName = ID + '.plt'
        entropyThreshold = 1.0e15

        dataFileName = '../plottingData/{:}_ShockRadiusVsTime.dat'.format( ID )
        forceChoice = True
        ow = False
        getShockRadiusData \
          ( plotfileDirectory, plotfileBaseName, dataFileName, \
            entropyThreshold, markEvery = 1, \
            forceChoice = forceChoice, ow = ow )

        Time, RsAve, RsMin, RsMax = np.loadtxt( dataFileName )

        dr = ( 1.5 * Rs - Rpns ) / np.float64( nX[i] )

        lab = r'$dr={:.2f}\ \mathrm{{km}}$'.format( dr )
        ind = np.where( Time[:-1] / tauAd < 100 )[0]
        axs[0].plot( Time[ind] / tauAd, ( RsAve[ind] - RsAve[0] ) / RsAve[0], \
                     label = lab )

    # Relaxation

    ID = IDD + '_nX{:}'.format( str( nXX ).zfill( 4 ) )
    plotFileDirectory = rootDirectory + ID + '/'

    Time, Data \
      = getRelaxationData( plotFileDirectory, ID, 'PF_D', nXX, True, False )

    ind = np.where( Time[:-1] / tauAd < 100 )[0]
    axs[1].plot( Time[ind] / tauAd, np.abs( Data[ind] ), 'k.', \
                 markersize = 2.0, markevery = 1 )

    # Labels

    axs[0].text( 0.3, 0.87, text, \
                 transform = axs[0].transAxes, fontsize = 15 )

    axs[1].set_ylim( ylim )
    axs[1].set_yscale( 'log' )

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

    xlim = axs[0].get_xlim()
    axs[1].set_xlim( xlim )

    axs[1].set_xlabel( r'$t/\tau_{\mathrm{ad}}$' )

    ylabel = r'$\left(R_{s}\left(t\right)-R_{s}\left(0\right)\right)$' \
               + r'$/R_{s}\left(0\right)$'
    axs[0].set_ylabel( ylabel, labelpad = +3.0 )

    if stage == 'earlyStage':

        ylabel \
        = r'$\max\limits_{r/\mathrm{km}\in\left[40,180\right]}\left(\dot{\rho}\left(t\right)/\rho\left(t\right)\right)$' \
                   + r'$\ \left[\mathrm{ms}^{-1}\right]$'
    elif stage == 'lateStage':

        ylabel \
        = r'$\max\limits_{r/\mathrm{km}\in\left[20,60\right]}\left(\dot{\rho}\left(t\right)/\rho\left(t\right)\right)$' \
                   + r'$\ \left[\mathrm{ms}^{-1}\right]$'
    axs[1].set_ylabel( ylabel, fontsize = 10 )

    axs[0].grid(axis = 'x')
    axs[1].grid(axis = 'x')

    axs[0].legend( loc = (0.6,0.4) )

    plt.subplots_adjust( hspace = 0 )

    #plt.show()
    plt.savefig( '../Figures/fig.RadialResolution_Relaxation_{:}.pdf' \
                 .format( IDD ), dpi = 300 )

    plt.close()

    import os
    os.system( 'rm -rf __pycache__ ' )
