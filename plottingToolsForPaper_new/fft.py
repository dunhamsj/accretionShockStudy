#!/usr/bin/env python3

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
plt.style.use( 'publication.sty' )

from computeTimeScales import ComputeTimeScales
from globalVariables import *

writeData = True

if writeData:
    with open( dataDirectory + 'fft.dat', 'w' ) as f:
        f.write( '# Generated from fft.py\n' )
        f.write( '# Model T/ms fwhm/ms\n' )

IDs = [ '2D_M1.4_Rpns040_Rs1.20e2', \
        '2D_M1.4_Rpns040_Rs1.50e2', \
        '2D_M1.4_Rpns070_Rs1.50e2', \
        '2D_M1.4_Rpns040_Rs1.75e2', \
        '2D_M1.8_Rpns020_Rs7.00e1', \
        '2D_M2.8_Rpns020_Rs6.00e1', \
        '2D_M2.8_Rpns020_Rs7.00e1' ]

def getFFT( ID ):

    time, data \
      = np.loadtxt( dataDirectory + 'LatFlux_{:}.dat'.format( ID ) )

    # Remove unperturbed file
    time = np.copy( time[:-1] )
    data = np.copy( data[:-1] )

    f = open( dataDirectory + 'LegendrePowerSpectrum_{:}.dat'.format( ID ) )
    s = f.readline()
    s = f.readline(); ind = s.find( '#' )+2
    sarr = s[ind:-2].split( ' ' )
    tMin = np.float64( sarr[0] )
    f.close()

    RsFileName \
      = dataDirectory + 'ShockRadiusVsTime_{:}.dat'.format( ID )
    Time, RsAve, RsMin, RsMax = np.loadtxt( RsFileName )

    # Remove unperturbed file
    Time  = np.copy( Time [:-1] )
    RsAve = np.copy( RsAve[:-1] )
    RsMin = np.copy( RsMin[:-1] )
    RsMax = np.copy( RsMax[:-1] )

    ind = np.where( RsMax > 1.1 * RsAve[0] )[0]
    if ind.shape[0] == 0:
        ind = -1
    else:
        ind = ind[0]

    time = np.copy( time[0:ind] )
    data = np.copy( data[0:ind] )

    indt = np.where( time > tMin )[0]
    time = np.copy( time[indt] )
    data = np.copy( data[indt] )

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

    yy   = np.abs( y   / y  .max() )
    yywf = np.abs( ywf / ywf.max() )

    return x, yy

def getPeriodAndUncertainty( x, y ):

    yInterp = sp.interpolate.interp1d( x, y )
    xInterp = np.linspace( x.min(), x.max(), 1000 )
    ind = np.where( yInterp( xInterp ) >= 0.5 )[0]
    fwhm = xInterp[ind[-1]] - xInterp[ind[0]]
    T    = xInterp[ np.argmax( yInterp(xInterp) ) ]

    return T, fwhm, xInterp, ind

for i in range( len( IDs ) ):

    ID = IDs[i]

    xNR, yNR = getFFT( 'NR' + ID )
    xGR, yGR = getFFT( 'GR' + ID )
    TNR, fwhmNR, xNRI, indNR = getPeriodAndUncertainty( xNR, yNR )
    TGR, fwhmGR, xGRI, indGR = getPeriodAndUncertainty( xGR, yGR )

    M_s   = ID[4:7]
    M     = np.float64( M_s )
    rsh_s = ID[18:24]
    rsh   = np.float64( rsh_s )
    rpns  = np.int64  ( ID[12:15] )

    rInner = rpns
    rOuter = rsh

    fig, ax = plt.subplots( 1, 1, figsize = (2,2) )

    IDD = ID[3:].replace( 'Rs', 'Rsh' )
    ax.set_title( r'$\texttt{{{:}}}$'.format( IDD ), fontsize = 9 )

    ax.plot( xNR, yNR, '-', label = 'NR' )
    ax.plot( xGR, yGR, '-', label = 'GR' )

    #ax.plot( [xNRI[indNR[0]],xNRI[indNR[-1]]], [0.5,0.5] )
    #ax.plot( [xGRI[indGR[0]],xGRI[indGR[-1]]], [0.5,0.5] )

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

    ax.set_ylabel( r'$\widetilde{F}^{r}_{\theta}/$' \
                     + r'$\max\limits_{\widetilde{T}}$' \
                     + r'$\left(\widetilde{F}^{1}_{2}\right)$', \
                   fontsize = 10 )
    ax.set_xlabel \
      ( r'$\widetilde{T}\ \left[\mathrm{ms}\right]$', fontsize = 14 )

    plt.show()

    #figName = figuresDirectory + 'fig.FFT_{:}.pdf'.format( IDD )
    #plt.savefig( figName, dpi = 300 )
    #print( '\n  Saved {:}'.format( figName ) )

    plt.close()

    if writeData:
        with open( dataDirectory + 'fft.dat', 'a' ) as f:
            f.write( '{:} {:.16e} {:.16e}\n' \
                     .format( 'NR' + ID, TNR, fwhmNR ) )
            f.write( '{:} {:.16e} {:.16e}\n' \
                     .format( 'GR' + ID, TGR, fwhmGR ) )

import os
os.system( 'rm -rf __pycache__ ' )
