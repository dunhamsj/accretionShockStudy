#!/usr/bin/env python3

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
plt.style.use( 'publication.sty' )

from computeTimeScales import ComputeTimeScales
from globalVariables import *

with open( dataDirectory + 'fft.dat', 'w' ) as f:
    f.write( '# Generated from fft.py\n' )
    f.write( '# Model T/ms fwhm/ms\n' )

IDs = [ 'NR2D_M1.4_Rpns040_Rs1.20e2' ]

for i in range( len( IDs ) ):

    fig, ax = plt.subplots( 1, 1, figsize = (2,2) )

    ID = IDs[i]

    time, data \
      = np.loadtxt( dataDirectory + 'LatFlux_{:}.dat'.format( ID ) )

    f = open( dataDirectory + 'LegendrePowerSpectrum_{:}.dat'.format( ID ) )
    s = f.readline()
    s = f.readline(); ind = s.find( '#' )+2
    sarr = s[ind:-2].split( ' ' )
    tMin = np.float64( sarr[0] )
    f.close()

    RsFileName \
      = dataDirectory + 'ShockRadiusVsTime_{:}.dat'.format( ID )
    Time, RsAve, RsMin, RsMax = np.loadtxt( RsFileName )

    print( time );exit()

    ind = np.where( RsMax > 1.1 * RsAve[0] )[0][0]

    time = np.copy( time[:-1] )
    data = np.copy( data[:-1] )

    time = np.copy( time[0:ind] )
    data = np.copy( data[0:ind] )

    indt = np.where( time > tMin )[0]
    time = np.copy( time[indt] )
    data = np.copy( data[indt] )

    dataFileName = 'FFT_{:}.dat'.format( ID )

    # Compute and plot FFT

    N = time.shape[0]
    T = ( time[-1] - time[0] )/ np.float64( N ) # milliseconds

    from scipy.signal.windows import blackman
    w = blackman( N )

    if( N % 2 == 0 ):
        y   = np.abs( sp.fft.fft    ( data )    [1:N//2] )**2
        ywf = np.abs( sp.fft.fft    ( data * w )[1:N//2] )**2
        x   =         sp.fft.fftfreq( N, T )    [1:N//2]
    else:
        y   = np.abs( sp.fft.fft    ( data     )[1:(N-1)//2] )**2
        ywf = np.abs( sp.fft.fft    ( data * w )[1:(N-1)//2] )**2
        x   =         sp.fft.fftfreq( N, T     )[1:(N-1)//2]

    x = 1.0 / x

    x   = x  [::-1]
    y   = y  [::-1]
    ywf = ywf[::-1]

    rel   = ID[0:2]
    M_s   = ID[6:9]
    M     = np.float64( M_s )
    rsh_s = ID[20:26]
    rsh   = np.float64( rsh_s )
    rpns  = np.int64  ( ID[14:17] )

    rInner = rpns
    rOuter = rsh

    IDD = ID[5:].replace( 'Rs', 'Rsh' )
    ax.set_title( r'$\texttt{{{:}}}$'.format( IDD ), fontsize = 9 )

    yy   = np.abs( y   / y  .max() )
    yywf = np.abs( ywf / ywf.max() )

    ax.plot( x, yy, '-', label = rel )
    #yy = yywf
    #ax.plot( x, yywf, '-', label = rel )

    yInterp = sp.interpolate.interp1d( x, yy )
    xInterp = np.linspace( x.min(), x.max(), 1000 )
    ind = np.where( yInterp(xInterp) >= 0.5 )[0]
    dt = xInterp[ind[-1]] - xInterp[ind[0]]
    fwhm = dt
    T    = xInterp[ np.argmax( yInterp(xInterp) ) ]
    #ax.plot( [xInterp[ind[0]],xInterp[ind[-1]]], [0.5,0.5])

    if M_s == '1.4':
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

    if M_s == '1.4' and rsh_s == '1.20e2':
        ax.legend( loc = 1 )

    ax.set_ylabel( r'$\widetilde{F}^{r}_{\theta}/\max\limits_{\widetilde{T}}\left(\widetilde{F}^{1}_{2}\right)$', fontsize = 10 )
    ax.set_xlabel \
      ( r'$\widetilde{T}\ \left[\mathrm{ms}\right]$', fontsize = 14 )

    plt.show()
#    IDD = ID.replace( 'Rs', 'Rsh' )
#    plt.savefig( '/home/kkadoogan/Work/accretionShockPaper/Figures/' \
#                   + 'fig.FFT_{:}.pdf'.format( IDD[3:] ), dpi = 300 )
    plt.close()
#    with open( dataDirectory + 'fft.dat', 'a' ) as f:
#        f.write( '{:} {:.16e} {:.16e}\n' \
#                 .format( ID, T, fwhm ) )
