#!/usr/bin/env python3

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
plt.style.use( 'publication.sty' )

from computeTimeScales import ComputeTimeScales

# Early-Stage
# RsMax < 1.45 * Rs(t=0)
ind_ES = np.empty( (2,3), np.int64 )
ind_ES[0,0] = 847
ind_ES[0,1] = 1473
ind_ES[0,2] = 2033
ind_ES[1,0] = 1071
ind_ES[1,1] = -1
ind_ES[1,2] = 2294

# Late-Stage
# RsMax < 1.45 * Rs(t=0)
ind_LS = np.empty( (2,3), np.int64 )
ind_LS[0,0] = 217
ind_LS[0,1] = 317
ind_LS[0,2] = 510
ind_LS[1,0] = -1
ind_LS[1,1] = -1
ind_LS[1,2] = -1

S    = [ 'early', 'late' ]
M    = [ '1.4', '2.8' ]
Rs   = [ [ '1.20e2', '1.50e2', '1.75e2' ], \
         [ '6.00e1', '7.00e1', '8.75e1' ] ]
Rpns = [ '040', '020' ]

cutoff = 0.03

with open( '../plottingData/fft.dat', 'w' ) as f:
    f.write( '# Generated from fft.py\n' )
    f.write( '# Model T/ms fwhm/ms\n' )

for m in range( len( M ) ):

    if   m == 0:
        indd = np.copy( ind_ES )
    elif m == 1:
        indd = np.copy( ind_LS )

    for rs in range( len( Rs[0] ) ):

        if m == 1 and rs == 2:
            continue

        if ( ( m == 1 ) & ( rs == 2 ) ): continue

        fig, ax = plt.subplots( 1, 1, figsize = (2,2) )

        ID = '2D_M{:}_Rpns{:}_Rs{:}'.format( M[m], Rpns[m], Rs[m][rs] )

        ID_GR = 'GR' + ID
        ID_NR = 'NR' + ID
        timeGR, dataGR \
          = np.loadtxt( '../plottingData/LatFlux_{:}.dat'.format( ID_GR ) )
        timeNR, dataNR \
          = np.loadtxt( '../plottingData/LatFlux_{:}.dat'.format( ID_NR ) )

        f = open( '../plottingData/{:}_LegendrePowerSpectrum.dat' \
                  .format( ID_NR ) )
        s = f.readline()
        s = f.readline(); ind = s.find( '#' )+2
        sarr = s[ind:-2].split( ' ' )
        tMinNR = np.float64( sarr[0] )
        f.close()

        f = open( '../plottingData/{:}_LegendrePowerSpectrum.dat' \
                  .format( ID_GR ) )
        s = f.readline()
        s = f.readline(); ind = s.find( '#' )+2
        sarr = s[ind:-2].split( ' ' )
        tMinGR = np.float64( sarr[0] )
        f.close()

        RsFileNameGR \
          = '../plottingData/{:}_ShockRadiusVsTime.dat'.format( ID_GR )
        TimeGR, RsAveGR, RsMinGR, RsMaxGR = np.loadtxt( RsFileNameGR )
        RsFileNameNR \
          = '../plottingData/{:}_ShockRadiusVsTime.dat'.format( ID_NR )
        TimeNR, RsAveNR, RsMinNR, RsMaxNR = np.loadtxt( RsFileNameNR )

        timeNR = np.copy( timeNR[:-1] )
        timeGR = np.copy( timeGR[:-1] )
        dataNR = np.copy( dataNR[:-1] )
        dataGR = np.copy( dataGR[:-1] )

        timeNR = np.copy( timeNR[0:indd[0,rs]] )
        timeGR = np.copy( timeGR[0:indd[1,rs]] )
        dataNR = np.copy( dataNR[0:indd[0,rs]] )
        dataGR = np.copy( dataGR[0:indd[1,rs]] )

        indNRt = np.where( timeNR > tMinNR )[0]
        timeNR = np.copy( timeNR[indNRt] )
        dataNR = np.copy( dataNR[indNRt] )

        indGRt = np.where( timeGR > tMinGR )[0]
        timeGR = np.copy( timeGR[indGRt] )
        dataGR = np.copy( dataGR[indGRt] )

        dataFileNameGR = '{:}_FFT.dat'.format( ID_GR )
        dataFileNameNR = '{:}_FFT.dat'.format( ID_NR )

        # Compute and plot FFT

        NGR = timeGR.shape[0]
        NNR = timeNR.shape[0]
        TGR = ( timeGR[-1] - timeGR[0] )/ np.float64( NGR ) # milliseconds
        TNR = ( timeNR[-1] - timeNR[0] )/ np.float64( NNR ) # milliseconds

        from scipy.signal.windows import blackman
        wGR = blackman( NGR )
        wNR = blackman( NNR )

        if( NGR % 2 == 0 ):
            yGR   = np.abs( sp.fft.fft    ( dataGR       )[1:NGR//2] )**2
            ywfGR = np.abs( sp.fft.fft    ( dataGR * wGR )[1:NGR//2] )**2
            xGR =           sp.fft.fftfreq( NGR, TGR     )[1:NGR//2]
        else:
            yGR   = np.abs( sp.fft.fft    ( dataGR       )[1:(NGR-1)//2] )**2
            ywfGR = np.abs( sp.fft.fft    ( dataGR * wGR )[1:(NGR-1)//2] )**2
            xGR   =         sp.fft.fftfreq( NGR, TGR     )[1:(NGR-1)//2]

        if( NNR % 2 == 0 ):
            yNR   = np.abs( sp.fft.fft    ( dataNR )      [1:NNR//2] )**2
            ywfNR = np.abs( sp.fft.fft    ( dataNR * wNR )[1:NNR//2] )**2
            xNR   =         sp.fft.fftfreq( NNR, TNR )    [1:NNR//2]
        else:
            yNR   = np.abs( sp.fft.fft    ( dataNR       )[1:(NNR-1)//2] )**2
            ywfNR = np.abs( sp.fft.fft    ( dataNR * wNR )[1:(NNR-1)//2] )**2
            xNR   =         sp.fft.fftfreq( NNR, TNR     )[1:(NNR-1)//2]

        xGR = 1.0 / xGR
        xNR = 1.0 / xNR

        xGR   = xGR  [::-1]
        yGR   = yGR  [::-1]
        ywfGR = ywfGR[::-1]
        xNR   = xNR  [::-1]
        yNR   = yNR  [::-1]
        ywfNR = ywfNR[::-1]

        rInner = np.float64( Rpns[m] )
        rOuter = np.float64( Rs[m][rs] )

        ax.set_title \
          ( r'$\texttt{{M{:}_Rpns{:}_Rs{:}}}$' \
            .format( M[m], Rpns[m], Rs[m][rs] ), fontsize = 9 )

        yyNR   = np.abs( yNR   / yNR  .max() )
        yywfNR = np.abs( ywfNR / ywfNR.max() )
        yyGR   = np.abs( yGR   / yGR  .max() )
        yywfGR = np.abs( ywfGR / ywfGR.max() )

        ax.plot( xNR, yyNR, '-', label = 'NR' )
        ax.plot( xGR, yyGR, '-', label = 'GR' )
#        yyNR = yywfNR
#        yyGR = yywfGR
#        ax.plot( xNR, yywfNR, '-', label = 'NR' )
#        ax.plot( xGR, yywfGR, '-', label = 'GR' )

        yInterpNR = sp.interpolate.interp1d( xNR, yyNR )
        xInterpNR = np.linspace( xNR.min(), xNR.max(), 1000 )
        indNR = np.where( yInterpNR(xInterpNR) >= 0.5 )[0]
        dt_NR = xInterpNR[indNR[-1]] - xInterpNR[indNR[0]]
        fwhm_NR = dt_NR
        T_NR    = xInterpNR[ np.argmax( yInterpNR(xInterpNR) ) ]
        #ax.plot( [xInterpNR[indNR[0]],xInterpNR[indNR[-1]]], [0.5,0.5])

        yInterpGR = sp.interpolate.interp1d( xGR, yyGR )
        xInterpGR = np.linspace( xGR.min(), xGR.max(), 1000 )
        indGR = np.where( yInterpGR(xInterpGR) >= 0.5 )[0]
        dt_GR = xInterpGR[indGR[-1]] - xInterpGR[indGR[0]]
        fwhm_GR = dt_GR
        T_GR    = xInterpGR[ np.argmax( yInterpGR(xInterpGR) ) ]
        #ax.plot( [xInterpGR[indGR[0]],xInterpGR[indGR[-1]]], [0.5,0.5])

        if m == 0:
            ax.set_xlim( 0.0, 1.0e2 )
            ax.xaxis.set_major_locator( MultipleLocator( 25 ) )
            ax.xaxis.set_minor_locator( MultipleLocator( 10 ) )
        else:
            ax.set_xlim( 0.0, 2.0e1 )
            xticks = np.linspace( 0, 20, 21, dtype = np.int64 )
            ax.xaxis.set_major_locator( MultipleLocator( 5 ) )
            ax.xaxis.set_minor_locator( MultipleLocator( 1 ) )

        ax.xaxis.set_ticks_position( 'both' )
        ax.tick_params \
          ( top = True, left = True, right = True, bottom = True )

        ax.grid()

        if m == 0 and rs == 0:
            ax.legend( loc = 1 )

        ax.set_ylabel \
( r'$\widetilde{F}^{r}_{\theta}/\max\limits_{\widetilde{T}}\left(\widetilde{F}^{1}_{2}\right)$', fontsize = 10 )
        ax.set_xlabel \
          ( r'$\widetilde{T}\ \left[\mathrm{ms}\right]$', fontsize = 14 )

#        plt.show()
        plt.savefig( '../Figures/fig.FFT_{:}.pdf'.format( ID[3:] ), dpi = 300 )
        plt.close()
        with open( '../plottingData/fft.dat', 'a' ) as f:
            f.write( '{:} {:.16e} {:.16e}\n' \
                     .format( ID_NR, T_NR, fwhm_NR ) )
            f.write( '{:} {:.16e} {:.16e}\n' \
                     .format( ID_GR, T_GR, fwhm_GR ) )
