#!/usr/bin/env python3

import yt
import numpy as np
import matplotlib.pyplot as plt
import os
plt.style.use( 'publication.sty' )
from multiprocessing import Process, cpu_count, Manager

from UtilitiesModule import Overwrite, GetData, GetFileArray

yt.funcs.mylog.setLevel(40) # Suppress initial yt output to screen

def MakeLineOutPlot( plotfileDirectory, plotfileBaseName, entropyThreshold ):

    plotfileArray = GetFileArray( plotfileDirectory, plotfileBaseName )

    plotfile = plotfileDirectory + plotfileArray[-2]

    time, data, dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
      = GetData( plotfile, 'PolytropicConstant', verbose = True )

    fig2, ax2 = plt.subplots()
    ax2.semilogy( X1, data[:,0,0], 'k-' )
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
    plotfileArray = np.copy( plotfileArray[:-1] ) # ignore 99999999 file

    plotfileArray = plotfileArray[0::markEvery]
    plotfile      = plotfileDirectory + plotfileArray[0]

    nSS = plotfileArray.shape[0]

    RsAve  = np.empty( nSS, np.float64 )
    RsMin  = np.empty( nSS, np.float64 )
    RsMax  = np.empty( nSS, np.float64 )
    Time   = np.empty( nSS, np.float64 )

    def loop( iLo, iHi, iProc, \
              RsAve       , RsMin       , RsMax       , Time, \
              return_RsAve, return_RsMin, return_RsMax, return_Time ):

        for i in range( iLo, iHi ):

            N = iHi - iLo
            j = i - iLo

            if j % 1 == 0:
                print( '    File {:d}/{:d}'.format( j+1, N ) )

            plotfile = plotfileDirectory + plotfileArray[i]

            Time[j], Data, dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
              = GetData( plotfile, 'PolytropicConstant', verbose = False )

            ind = np.where( Data < entropyThreshold )[0]
            RsMin[j] = X1[ind.min()]

            ind = np.where( Data > entropyThreshold )[0]
            RsMax[j] = X1[ind.max()]

            Volume = 0.0
            for iX1 in range( nX[0] ):
                for iX2 in range( nX[1] ):
                    for iX3 in range( nX[2] ):

                        if( Data[iX1,iX2,iX3] > entropyThreshold ):

                            Volume \
                              += 4.0 * np.pi \
                                   * 1.0 / 3.0 * ( ( X1[iX1] + dX1[iX1] )**3 \
                                                       - X1[iX1]**3 )

            # 4/3 * pi * Rs^3 = Volume
            # ==> Rs = ( Volume / ( 4/3 * pi ) )^( 1 / 3 )
            Rs = ( Volume / ( 4.0 / 3.0 * np.pi ) )**( 1.0 / 3.0 )

            RsAve[j] = Rs
            if RsMin[j] >= Rs: RsMin[j] = Rs
            if RsMax[j] <= Rs: RsMax[j] = Rs

        return_RsAve[iProc] = RsAve
        return_RsMin[iProc] = RsMin
        return_RsMax[iProc] = RsMax
        return_Time [iProc] = Time

    # Adapted from:
    # https://www.benmather.info/post/
    # 2018-11-24-multiprocessing-in-python/

    nProcs = max( 10, cpu_count() // 2 )

    manager      = Manager()
    return_RsAve = manager.dict()
    return_RsMin = manager.dict()
    return_RsMax = manager.dict()
    return_Time  = manager.dict()

    if nProcs > 1:

        processes = []

        for iProc in range( nProcs ):

            iLo \
              = np.int64( np.float64( iProc     ) \
                  / np.float64( nProcs ) * nSS )
            iHi \
              = np.int64( np.float64( iProc + 1 ) \
                  / np.float64( nProcs ) * nSS )

            rsAve = np.empty( (iHi-iLo), np.float64 )
            rsMin = np.empty( (iHi-iLo), np.float64 )
            rsMax = np.empty( (iHi-iLo), np.float64 )
            time  = np.empty( (iHi-iLo), np.float64 )

            p = Process \
                  ( target = loop, \
                    args = ( iLo, iHi, iProc, \
                             rsAve, rsMin, rsMax, time, \
                             return_RsAve, return_RsMin, \
                             return_RsMax, return_Time ) )
            p.start()
            processes.append( p )

        # MPI BARRIER
        [ p.join() for p in processes ]

        for iProc in range( nProcs ):

            iLo \
              = np.int64( np.float64( iProc     ) \
                  / np.float64( nProcs ) * nSS )
            iHi \
              = np.int64( np.float64( iProc + 1 ) \
                  / np.float64( nProcs ) * nSS )

            RsAve[iLo:iHi] = return_RsAve[iProc]
            RsMin[iLo:iHi] = return_RsMin[iProc]
            RsMax[iLo:iHi] = return_RsMax[iProc]
            Time [iLo:iHi] = return_Time [iProc]

    else:

        loop( 0, nSS-1, 0, \
              RsAve       , RsMin       , RsMax       , Time, \
              return_RsAve, return_RsMin, return_RsMax, return_Time )

    header = 'Generated from shockRadius_1D.py'
    np.savetxt( dataFileName, \
                np.vstack( ( Time, RsAve, RsMin, RsMax ) ), header = header )

    return


if __name__ == "__main__":

    rootDirectory_LC \
      = '/lump/data/accretionShockStudy/newData/resolutionStudy_lowCompactness/'

    rootDirectory_HC \
      = '/lump/data/accretionShockStudy/newData/resolutionStudy_highCompactness/'

    IDs_LC = [ 'GR1D_M1.4_Rpns040_Rs1.20e2_nX0140', \
               'GR1D_M1.4_Rpns040_Rs1.20e2_nX0280', \
               'GR1D_M1.4_Rpns040_Rs1.20e2_nX0560', \
               'GR1D_M1.4_Rpns040_Rs1.20e2_nX1120' ]

    IDs_HC = [ 'GR1D_M2.8_Rpns020_Rs6.00e1_nX0140', \
               'GR1D_M2.8_Rpns020_Rs6.00e1_nX0280', \
               'GR1D_M2.8_Rpns020_Rs6.00e1_nX0560', \
               'GR1D_M2.8_Rpns020_Rs6.00e1_nX1120' ]

    fc = True
    OW = False

    dataDirectory = '../plottingData_new/'

    fig, axs = plt.subplots( 2, 1 )

    for i in range( len( IDs_LC ) ):

        ID = IDs_LC[i]

        plotfileDirectory = rootDirectory_LC + ID + '/'
        plotfileBaseName = ID + '.plt'
        entropyThreshold = 1.0e15

        if not os.path.isdir( plotfileDirectory ): continue

        #MakeLineOutPlot \
        #  ( plotfileDirectory, plotfileBaseName, entropyThreshold )

        dataFileName = dataDirectory + '{:}_ShockRadiusVsTime.dat'.format( ID )
        MakeDataFile \
          ( plotfileDirectory, plotfileBaseName, dataFileName, \
            entropyThreshold, markEvery = 1, \
            forceChoice = fc, \
            OW = OW )

        Time, RsAve, RsMin, RsMax = np.loadtxt( dataFileName )

        axs[0].plot( Time, ( RsAve - RsAve[0] ) / RsAve[0] )

    for i in range( len( IDs_HC ) ):

        ID = IDs_HC[i]

        plotfileDirectory = rootDirectory_HC + ID + '/'
        plotfileBaseName = ID + '.plt'
        entropyThreshold = 1.0e15

        if not os.path.isdir( plotfileDirectory ): continue

        #MakeLineOutPlot \
        #  ( plotfileDirectory, plotfileBaseName, entropyThreshold )

        dataFileName = dataDirectory + '{:}_ShockRadiusVsTime.dat'.format( ID )
        MakeDataFile \
          ( plotfileDirectory, plotfileBaseName, dataFileName, \
            entropyThreshold, markEvery = 1, \
            forceChoice = fc, \
            OW = OW )

        Time, RsAve, RsMin, RsMax = np.loadtxt( dataFileName )

        axs[1].plot( Time, ( RsAve - RsAve[0] ) / RsAve[0] )

    plt.show()

    import os
    os.system( 'rm -rf __pycache__ ' )
