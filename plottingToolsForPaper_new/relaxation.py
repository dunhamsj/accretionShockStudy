#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )
import os
from multiprocessing import Process, cpu_count, Manager

from UtilitiesModule import Overwrite, GetFileArray, GetData
from globalVariables import *

def generateData( plotfileDirectory, ID, forceChoice, OW ):

    dataFileName = dataDirectory + 'Relaxation_PF_D_{:}.dat'.format( ID )

    OW = Overwrite( dataFileName, ForceChoice = forceChoice, OW = OW )

    if OW:

        plotfileBaseName = ID + '.plt'

        plotfileArray = GetFileArray( plotfileDirectory, plotfileBaseName )
        plotfileArray = np.copy( plotfileArray[:-1] )

        nSS = plotfileArray.shape[0]

        ind = np.linspace( 0, nSS-1, nSS, dtype = np.int64 )

        print()
        print( '  Generating derivative data' )
        print( '  --------------------------' )

        nX = np.int64( ID[-4:] )

        Data     = np.zeros( (nSS,nX), np.float64 )
        Gradient = np.zeros( (nSS-1) , np.float64 )
        Time     = np.zeros( (nSS)   , np.float64 )

        def loop( iLo, iHi, nodalData, time, iProc, \
                  return_data, return_time ):

            for i in range( iLo, iHi ):

                N = iHi - iLo
                j = i - iLo

                if j % 10 == 0:
                    print( '    File {:d}/{:d}'.format( j+1, N ) )

                data, dataUnits, time[j] \
                  = GetData( plotfileDirectory, plotfileBaseName, 'PF_D', \
                             'spherical', True, argv = ['a',plotfileArray[i]], \
                             ReturnTime = True, ReturnMesh = False, \
                             Verbose = False )

                nodalData[j] = np.copy( data[:,0,0] )

            return_data[iProc] = nodalData
            return_time[iProc] = time

        # Adapted from:
        # https://www.benmather.info/post/
        # 2018-11-24-multiprocessing-in-python/

        nProcs = max( 10, cpu_count() // 2 )

        manager     = Manager()
        return_data = manager.dict()
        return_time = manager.dict()

        if nProcs > 1:

            processes = []

            for iProc in range( nProcs ):

                iLo \
                  = np.int64( np.float64( iProc     ) \
                      / np.float64( nProcs ) * nSS )
                iHi \
                  = np.int64( np.float64( iProc + 1 ) \
                      / np.float64( nProcs ) * nSS )

                d = np.empty( (iHi-iLo,nX), np.float64 )
                t = np.empty( (iHi-iLo)   , np.float64 )

                p = Process \
                      ( target = loop, \
                        args = (iLo,iHi,d,t,iProc,return_data,return_time) )
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

                Data[iLo:iHi] = return_data[iProc]
                Time[iLo:iHi] = return_time[iProc]

        else:

            loop( 0, nSS-1, Data, Time, 0, return_data, return_time )

        for i in range( Gradient.shape[0] ):

            Num = ( Data[i] - Data[i-1] ) / ( 0.5 * ( Data[i] + Data[i-1] ) )
            Den = Time[i+1] - Time[i-1]

            Gradient[i-1] = ( Num / Den ).max()

        header \
          = 'Generated from relaxation.py\nTime [ms]\n1/rho x drho/dt [1/ms]'

        np.savetxt( dataFileName, np.vstack( (Time[:-1],Gradient) ), \
                    header = header )

        del plotfileBaseName, plotfileArray, \
            Data, Gradient, Time

    # END if OW

    Time, Data = np.loadtxt( dataFileName )

    return Time, Data

def addPlot( rootDirectory, ID, Rsh, Rpns, text, xlim, ylim, ax ):

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

if __name__ == "__main__":

    fig, axs = plt.subplots( 2, 1 )

    xlim = [ -5.0, +105 ]

    fc = True
    ow = False

    # Early-stage

    rootDirectory_lowXi \
      = plotfileRootDirectory + 'resolutionStudy_lowCompactness/'
    ID   = 'GR1D_M1.4_Rpns040_Rs1.20e2_nX0280'
    Rsh  = 1.20e2
    Rpns = 4.00e1
    text = r'$\texttt{GR1D\_M1.4\_Rpns040\_Rsh1.20e2}$'
    ylim = 1.0e-6

    plotfileDirectory = rootDirectory_lowXi + '{:}/'.format( ID )

    Time, Data \
      = generateData( plotfileDirectory, ID, \
                      forceChoice = fc, OW = ow )

    addPlot( rootDirectory_lowXi, ID, Rsh, Rpns, text, xlim, ylim, axs[0] )

    axs[0].tick_params \
      ( which = 'both', \
        top = True, left = True, bottom = True, right = True, \
        labeltop    = False, \
        labelleft   = True, \
        labelright  = False, \
        labelbottom = False )

    # High-compactness

    rootDirectory_highXi \
      = plotfileRootDirectory + 'resolutionStudy_highCompactness/'
    ID   = 'GR1D_M2.8_Rpns020_Rs6.00e1_nX0280'
    Rsh  = 6.00e1
    Rpns = 2.00e1
    text = r'$\texttt{GR1D\_M2.8\_Rpns020\_Rsh6.00e1}$'
    ylim = 1.0e-13

    plotfileDirectory = rootDirectory_highXi + '{:}/'.format( ID )

    Time, Data \
      = generateData( plotfileDirectory, ID, \
                      forceChoice = fc, OW = ow )

    addPlot( rootDirectory_highXi, ID, Rsh, Rpns, text, xlim, ylim, axs[1] )

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

    plt.show()

    #figName = figuresDirectory + 'fig.Relaxation.pdf'
    #plt.savefig( figName, dpi = 300 )
    #print( '\n  Saved {:}'.format( figName ) )

    plt.close()

    import os
    os.system( 'rm -rf __pycache__ ' )
