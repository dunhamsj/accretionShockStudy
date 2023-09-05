#!/usr/bin/env python3

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

M    = [ '2.8' ]
Rs   = [ '6.00e1', '6.10e1' ]
Rpns = [ '020'   , '021' ]

fig, ax = plt.subplots( 1, 1 )

indd = 217

for rpns in range( len( Rpns ) ):

    m = 0
    rs = rpns

    ID_NR = 'NR2D_M{:}_Rpns{:}_Rs{:}'.format( M[m], Rpns[rpns], Rs[rs] )

    timeNR, dataNR \
      = np.loadtxt( '../plottingData/LatFlux_{:}.dat'.format( ID_NR ) )

    f = open( '../plottingData/{:}_LegendrePowerSpectrum.dat' \
              .format( ID_NR ) )
    s = f.readline()
    s = f.readline(); ind = s.find( '#' )+2
    sarr = s[ind:-2].split( ' ' )
    tMinNR = np.float64( sarr[0] )
    f.close()

    RsFileNameNR \
      = '../plottingData/{:}_ShockRadiusVsTime.dat'.format( ID_NR )
    TimeNR, RsAveNR, RsMinNR, RsMaxNR = np.loadtxt( RsFileNameNR )

    timeNR = np.copy( timeNR[:-1] )
    dataNR = np.copy( dataNR[:-1] )

    timeNR = np.copy( timeNR[0:indd] )
    dataNR = np.copy( dataNR[0:indd] )

    indNRt = np.where( timeNR > tMinNR )[0]
    timeNR = np.copy( timeNR[indNRt] )
    dataNR = np.copy( dataNR[indNRt] )

    dataFileNameNR = '{:}_FFT.dat'.format( ID_NR )

    # Compute and plot FFT

    NNR = timeNR.shape[0]
    TNR = ( timeNR[-1] - timeNR[0] )/ np.float64( NNR ) # milliseconds

    from scipy.signal.windows import blackman
    wNR = blackman( NNR )

    if( NNR % 2 == 0 ):
        yNR   = np.abs( sp.fft.fft    ( dataNR )      [1:NNR//2] )**2
        ywfNR = np.abs( sp.fft.fft    ( dataNR * wNR )[1:NNR//2] )**2
        xNR   =         sp.fft.fftfreq( NNR, TNR )    [1:NNR//2]
    else:
        yNR   = np.abs( sp.fft.fft    ( dataNR       )[1:(NNR-1)//2] )**2
        ywfNR = np.abs( sp.fft.fft    ( dataNR * wNR )[1:(NNR-1)//2] )**2
        xNR   =         sp.fft.fftfreq( NNR, TNR     )[1:(NNR-1)//2]

    xNR = 1.0 / xNR

    xNR   = xNR  [::-1]
    yNR   = yNR  [::-1]
    ywfNR = ywfNR[::-1]

    rInner = np.float64( Rpns[rpns] )
    rOuter = np.float64( Rs[rs] )

#    ax.set_title \
#      ( r'$\texttt{{M{:}_Rpns{:}_Rsh{:}}}$' \
#        .format( M[m], Rpns[rpns], Rs[rs] ), fontsize = 9 )

    yyNR   = np.abs( yNR   / yNR  .max() )
    yywfNR = np.abs( ywfNR / ywfNR.max() )

    ax.plot( xNR, yyNR, '-', label = ID_NR )

    yInterpNR = sp.interpolate.interp1d( xNR, yyNR )
    xInterpNR = np.linspace( xNR.min(), xNR.max(), 1000 )
    indNR = np.where( yInterpNR(xInterpNR) >= 0.5 )[0]
    dt_NR = xInterpNR[indNR[-1]] - xInterpNR[indNR[0]]
    fwhm_NR = dt_NR
    T_NR    = xInterpNR[ np.argmax( yInterpNR(xInterpNR) ) ]

ax.set_xlim( 0.0, 2.0e1 )
xticks = np.linspace( 0, 20, 21, dtype = np.int64 )

ax.xaxis.set_ticks_position( 'both' )
ax.tick_params \
  ( top = True, left = True, right = True, bottom = True )

ax.grid()

ax.legend( loc = 1 )

ax.set_ylabel \
( r'$\widetilde{F}^{r}_{\theta}/\max\limits_{\widetilde{T}}\left(\widetilde{F}^{1}_{2}\right)$', fontsize = 10 )
ax.set_xlabel \
          ( r'$\widetilde{T}\ \left[\mathrm{ms}\right]$', fontsize = 14 )

plt.savefig( '/home/kkadoogan/fig.FFT.png', dpi = 300 )

#plt.show()
