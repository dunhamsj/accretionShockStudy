#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )
import os

if __name__ == "__main__":

    fig, axs = plt.subplots( 2, 1 )

    # Early-stage

    rootDirectory \
      = '/lump/data/accretionShockStudy/newData/resolutionStudy_earlyStage/'

    ID   = 'GR1D_M1.4_Rpns040_Rs1.20e2'
    nX   = [ '0140', '0280', '0560', '1120' ]
    Rpns = 4.00e1
    Rs   = 1.20e2
    text = r'$\texttt{GR1D\_M1.4\_Rpns040\_Rs1.20e2}$'

    for i in range( len( nX ) ):

        IDD = ID + '_nX{:}'.format( nX[i] )
        plotfileDirectory = rootDirectory + IDD + '/'
        plotfileBaseName = IDD + '.plt'
        entropyThreshold = 1.0e15

        dataFileName = '../plottingData/{:}_ShockRadiusVsTime.dat'.format( IDD )

        Time, RsAve, RsMin, RsMax = np.loadtxt( dataFileName )
        tauAd = Time[-1] / 1.0e2

        dr = ( 1.5 * Rs - Rpns ) / np.float64( nX[i] )

        lab = r'$dr={:.2f}\ \mathrm{{km}}$'.format( dr )
        axs[0].plot( Time / tauAd, ( RsAve - RsAve[0] ) / RsAve[0], \
                     label = lab )

    axs[0].text( 0.08, 0.87, text, \
                 transform = axs[0].transAxes, fontsize = 13 )

    axs[0].tick_params \
      ( which = 'both', \
        top = True, left = True, bottom = True, right = True, \
        labeltop    = False, \
        labelleft   = True, \
        labelright  = False, \
        labelbottom = False )

    axs[0].grid(axis = 'x')

    axs[0].legend( loc = (0.6,0.49) )

    # Late-stage

    rootDirectory \
      = '/lump/data/accretionShockStudy/newData/resolutionStudy_lateStage/'

    ID   = 'GR1D_M2.8_Rpns020_Rs6.00e1'
    nX   = [ '0140', '0280', '0560', '1120' ]
    Rpns = 2.00e1
    Rs   = 6.00e1
    text = r'$\texttt{GR1D\_M2.8\_Rpns020\_Rs6.00e1}$'

    for i in range( len( nX ) ):

        IDD = ID + '_nX{:}'.format( nX[i] )
        plotfileDirectory = rootDirectory + IDD + '/'
        plotfileBaseName = IDD + '.plt'
        entropyThreshold = 1.0e15

        dataFileName = '../plottingData/{:}_ShockRadiusVsTime.dat'.format( IDD )

        Time, RsAve, RsMin, RsMax = np.loadtxt( dataFileName )
        tauAd = Time[-1] / 1.0e2

        dr = ( 1.5 * Rs - Rpns ) / np.float64( nX[i] )

        lab = r'$dr={:.2f}\ \mathrm{{km}}$'.format( dr )
        axs[1].plot( Time / tauAd, ( RsAve - RsAve[0] ) / RsAve[0], \
                     label = lab )

    axs[1].text( 0.08, 0.87, text, \
                 transform = axs[1].transAxes, fontsize = 13 )

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

    axs[1].grid(axis = 'x')

    axs[1].legend( loc = (0.6,0.53) )

    ylabel = r'$\left(R_{s}\left(t\right)-R_{s}\left(0\right)\right)$' \
               + r'$/R_{s}\left(0\right)$'
    fig.supylabel( ylabel )

    plt.subplots_adjust( hspace = 0 )

    #plt.show()
    plt.savefig( '../Figures/fig.RadialResolution.pdf', dpi = 300 )

    plt.close()

    import os
    os.system( 'rm -rf __pycache__ ' )
