#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )
import os

def getRelaxationData( dataFileName ):

    Time, Data = np.loadtxt( dataFileName )

    return Time, Data


if __name__ == "__main__":

    fig, axs = plt.subplots( 2, 1 )

    xlim = [ -5.0, +105 ]

    # Early-stage

    rootDirectory = '/lump/data/accretionShockStudy/newData/resolutionStudy_earlyStage/'

    IDD  = 'GR1D_M1.4_Rpns040_Rs1.20e2'
    nXX  = 280
    Rs   = 1.20e2
    Rpns = 4.00e1
    text = r'$\texttt{GR1D\_M1.4\_Rpns040\_Rsh1.20e2}$'
    ylim = 1.0e-6

    ID = IDD + '_nX{:}'.format( str( nXX ).zfill( 4 ) )

    dataFileName = '../plottingData/{:}_Relaxation_{:}.dat' \
                   .format( ID, 'PF_D' )

    Time, Data = getRelaxationData( dataFileName )
    tauAd = Time[-1] / 1.0e2

    ind = np.where( Time[:-1] / tauAd < 100 )[0]
    axs[0].plot( Time[ind] / tauAd, np.abs( Data[ind] ), 'k.', \
                 markersize = 2.0, markevery = 1 )

    axs[0].text( 0.3, 0.87, text, \
                 transform = axs[0].transAxes, fontsize = 15 )
    axs[0].set_ylim( ylim )
    axs[0].set_xlim( xlim )
    axs[0].set_yscale( 'log' )

    axs[0].tick_params \
      ( which = 'both', \
        top = True, left = True, bottom = True, right = True, \
        labeltop    = False, \
        labelleft   = True, \
        labelright  = False, \
        labelbottom = False )

    axs[0].grid(axis = 'x')

    # Late-stage

    rootDirectory = '/lump/data/accretionShockStudy/newData/resolutionStudy_lateStage/'

    IDD  = 'GR1D_M2.8_Rpns020_Rs6.00e1'
    nXX  = 280
    Rs   = 6.00e1
    Rpns = 2.00e1
    text = r'$\texttt{GR1D\_M2.8\_Rpns020\_Rsh6.00e1}$'
    ylim = 1.0e-13

    ID = IDD + '_nX{:}'.format( str( nXX ).zfill( 4 ) )

    dataFileName = '../plottingData/{:}_Relaxation_{:}.dat' \
                   .format( ID, 'PF_D' )

    Time, Data = getRelaxationData( dataFileName )
    tauAd = Time[-1] / 1.0e2

    ind = np.where( Time[:-1] / tauAd < 100 )[0]
    axs[1].plot( Time[ind] / tauAd, np.abs( Data[ind] ), 'k.', \
                 markersize = 2.0, markevery = 1 )

    axs[1].text( 0.3, 0.87, text, \
                 transform = axs[1].transAxes, fontsize = 15 )

    axs[1].set_ylim( ylim )
    axs[1].set_xlim( xlim )
    axs[1].set_yscale( 'log' )

    axs[1].tick_params \
      ( which = 'both', \
        top = True, left = True, bottom = True, right = True, \
        labeltop    = False, \
        labelleft   = True, \
        labelright  = False, \
        labelbottom = True )

    xlim = axs[0].get_xlim()
    axs[1].set_xlim( xlim )

    axs[1].set_xlabel( r'$t/\tau_{\mathrm{ad}}$', fontsize = 15 )

    ylabel \
    = r'$\max\limits_{r\in\left[R_{\mathrm{PNS}},1.5\,R_{\mathrm{sh}}\right]}\left|\dot{\rho}\left(t\right)/\rho\left(t\right)\right|$' \
               + r'$\ \left[\mathrm{ms}^{-1}\right]$'
    fig.supylabel( ylabel, x = -0.01, fontsize = 15 )

    axs[1].grid(axis = 'x')

    plt.subplots_adjust( hspace = 0 )

    #plt.show()
    plt.savefig( '/home/kkadoogan/Work/accretionShockPaper/Figures/fig.Relaxation.pdf', dpi = 300 )

    plt.close()

    import os
    os.system( 'rm -rf __pycache__ ' )
