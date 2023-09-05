#!/usr/bin/env python3

import numpy as np
from sys import argv
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )
from multiprocessing import Process, cpu_count, Manager

from UtilitiesModule import Overwrite, GetFileArray, GetData

def getData( plotfileDirectory, ID, field, nX, forceChoice, OW ):

    dataFileName = '../plottingData_new/{:}_Relaxation_{:}.dat'.format( ID, field )

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

                plotfile = plotfileDirectory + plotfileArray[i]
                time[j], data, dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
                  = GetData( plotfile, field, verbose = False )

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

        header = 'Generated from relaxation.py\n'
        header += 'Time [ms], |drho|/rho'
        np.savetxt( dataFileName, np.vstack( (Time[:-1],Gradient) ), \
                    header = header )

        del plotfileBaseName, plotfileArray, Data, Gradient, Time

    # END if OW

    Time, Data = np.loadtxt( dataFileName )

    return Time, Data

def plot( ID_LC, ID_HC, Time_LC, Time_HC, Data_LC, Data_HC ):

    # Early-stage

    tauAd = Time_LC[-1] / 1.0e2

    ind = np.where( Time_LC[:-1] / tauAd < 100 )[0]
    axs[0].plot( Time_LC[ind] / tauAd, np.abs( Data_LC[ind] ), 'k.', \
                 markersize = 2.0, markevery = 1 )

    # Early-stage

    tauAd = Time_HC[-1] / 1.0e2

    ind = np.where( Time_HC[:-1] / tauAd < 100 )[0]
    axs[1].plot( Time_HC[ind] / tauAd, np.abs( Data_HC[ind] ), 'k.', \
                 markersize = 2.0, markevery = 1 )

if __name__ == '__main__':

    UseLogScale = True

    nX = [ '0280' ]

    rootID_LC = 'GR1D_M1.4_Rpns040_Rs1.20e2'
    rootID_HC = 'GR1D_M2.8_Rpns020_Rs6.00e1'

    rootDirectory_LC \
      = '/lump/data/accretionShockStudy/newData/resolutionStudy_lowCompactness/'
    rootDirectory_HC \
      = '/lump/data/accretionShockStudy/newData/resolutionStudy_highCompactness/'

    fc = True
    OW = False
    for i in range( len( nX ) ):

        ID_LC = rootID_LC + '_nX{:}'.format( nX[i] )
        ID_HC = rootID_HC + '_nX{:}'.format( nX[i] )

        plotfileDirectory_LC = '{:}{:}/'.format( rootDirectory_LC, ID_LC )
        plotfileDirectory_HC = '{:}{:}/'.format( rootDirectory_HC, ID_HC )

        D = 'PF_D'

        Time_LC, Data_LC \
          = getData( plotfileDirectory_LC, ID_LC, D, np.int64( nX[i] ), \
                     forceChoice = fc, OW = OW )
        Time_HC, Data_HC \
          = getData( plotfileDirectory_HC, ID_HC, D, np.int64( nX[i] ), \
                     forceChoice = fc, OW = OW )

    fig, axs = plt.subplots( 2, 1 )

    xlim = [ -5.0, +105 ]

    textLC = r'$\texttt{GR1D\_M1.4\_Rpns040\_Rsh1.20e2}$'
    textHC = r'$\texttt{GR1D\_M2.8\_Rpns020\_Rsh6.00e1}$'

    dataDirectory = '../plottingData_new/'

    for i in range( len( nX ) ):

        ID_LC = rootID_LC + '_nX{:}'.format( nX[i] )
        ID_HC = rootID_HC + '_nX{:}'.format( nX[i] )

        Time_LC, Data_LC \
          = np.loadtxt( dataDirectory + ID_LC + '_Relaxation_PF_D.dat' )
        Time_HC, Data_HC \
          = np.loadtxt( dataDirectory + ID_HC + '_Relaxation_PF_D.dat' )

        plot( ID_LC, ID_HC, Time_LC, Time_HC, Data_LC, Data_HC )

    axs[0].set_xlim( xlim )
    axs[0].set_yscale( 'log' )
    axs[1].set_xlim( xlim )
    axs[1].set_yscale( 'log' )

    text = r'$\texttt{GR1D\_M1.4\_Rpns040\_Rsh1.20e2}$'
    axs[0].text( 0.3, 0.87, text, \
                 transform = axs[0].transAxes, fontsize = 15 )

    text = r'$\texttt{GR1D\_M2.8\_Rpns020\_Rsh6.00e1}$'
    axs[1].text( 0.3, 0.87, text, \
                 transform = axs[1].transAxes, fontsize = 15 )

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

    axs[0].grid( axis = 'x' )
    axs[1].grid( axis = 'x' )
    axs[0].set_ylim( 1.0e-6 , 6.0e-1 )
    axs[1].set_ylim( 1.0e-13, 6.0e-1 )

    axs[1].set_xlabel( r'$t/\tau_{\mathrm{ad}}$', fontsize = 15 )

    ylabel \
    = r'$\max\limits_{r\in\left[R_{\mathrm{PNS}},1.5\,R_{\mathrm{sh}}\right]}\left|\dot{\rho}\left(t\right)/\rho\left(t\right)\right|$' \
               + r'$\ \left[\mathrm{ms}^{-1}\right]$'
    fig.supylabel( ylabel, x = -0.01, fontsize = 15 )

    plt.subplots_adjust( hspace = 0 )

    plt.show()

#    figName = '/home/kkadoogan/Work/accretionShockPaper/Figures/fig.Relaxation.pdf'
#    plt.savefig( figName, dpi = 300 )
#    print( '\n  Saved {:}'.format( figName ) )

    import os
    os.system( 'rm -rf __pycache__ ' )
