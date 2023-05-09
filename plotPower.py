#!/usr/bin/env python3

import numpy as np
from os.path import isfile, isdir
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from FitPowerToModel import FittingFunction
from computeTimeScales import ComputeTimeScales

stage   = 'late'
vsTau   = False
saveFig = False

arrShape = (2,3)

indd = np.empty( arrShape, np.int64 )

if stage == 'early':

    R    = np.array( [ 'NR', 'GR' ], str )
    M    = np.array( [ '1.4' ], str )
    Rs   = np.array( [ '1.20e2', '1.50e2', '1.75e2' ], str )
    Rpns = np.array( [ '040' ], str )
    # RsMax < 1.45 * Rs(t=0)
    indd[0,0] = 847
    indd[0,1] = 1473
    indd[0,2] = 2033
    indd[1,0] = 1071
    indd[1,1] = -1
    indd[1,2] = 2294
    Rs   = np.array( [ '1.80e2', '1.80e2' ], str )
    indd[:,:] = -1
    suffix = ''

elif stage == 'late':

    R    = np.array( [ 'NR', 'GR' ], str )
    M    = np.array( [ '2.8' ], str )
    Rs   = np.array( [ '9.00e1', '9.00e1' ], str )
    Rpns = np.array( [ '020' ], str )
    # RsMax < 1.45 * Rs(t=0)
    indd[:,:] = -1
    suffix = ''

else:

    exit('Ya done fucked up')

ID = np.empty( arrShape, object )

t  = np.empty( arrShape, object )
P0 = np.empty( arrShape, object )
P1 = np.empty( arrShape, object )
P2 = np.empty( arrShape, object )
P3 = np.empty( arrShape, object )
P4 = np.empty( arrShape, object )

t0         = np.empty( arrShape, object )
t1         = np.empty( arrShape, object )
LogF       = np.empty( arrShape, object )
omegaR     = np.empty( arrShape, object )
omegaI     = np.empty( arrShape, object )
delta      = np.empty( arrShape, object )
omegaR_err = np.empty( arrShape, object )
omegaI_err = np.empty( arrShape, object )

T_SASI     = np.empty( arrShape, object )

for r in range( R.shape[0] ):
    for rs in range( Rs.shape[0] ):

        ID[r,rs] \
          = '{:}2D_M{:}_Rpns{:}_Rs{:}{:}'.format \
             ( R[r], M[0], Rpns[0], Rs[rs], suffix )

        plotFileDirectory \
          = '/lump/data/accretionShockStudy/newData/2D/{:}/'.format \
            ( ID[r,rs] )

        if not isdir( plotFileDirectory ):
            print( '{:} does not exist. Skipping.' \
                   .format( plotFileDirectory ) )
            continue

        plotFileBaseName = '{:}.plt'.format( ID[r,rs] )
        rInner = np.float64( Rpns[0] )
        rOuter = np.float64( Rs[rs] )
        tAd = 0
        tAc = 0
        tAd, tAc \
          = ComputeTimeScales \
              ( plotFileDirectory+plotFileBaseName+'00000000', \
                rInner, rOuter, R[r] )

        T_SASI[r,rs] = tAd + tAc

        dataFileName \
          = '.{:}_LegendrePowerSpectrum.dat'.format( ID[r,rs] )

        if not isfile( dataFileName ):
            print( '{:} does not exist. Skipping.' \
                   .format( dataFileName ) )
            continue

        t [r,rs], \
        P0[r,rs], \
        P1[r,rs], \
        P2[r,rs], \
        P3[r,rs], \
        P4[r,rs] \
          = np.loadtxt( dataFileName )

        # Read in fit data

        f = open( dataFileName )

        dum = f.readline()

        s = f.readline(); ind = s.find( '#' )+1
        tmp \
          = np.array( list( map( np.float64, s[ind:].split() ) ), \
                      np.float64 )
        t0    [r,rs] = tmp[0]
        t1    [r,rs] = tmp[1]
        LogF  [r,rs] = tmp[2]
        omegaR[r,rs] = tmp[3]
        omegaI[r,rs] = tmp[4]
        delta [r,rs] = tmp[5]

        dum = f.readline()

        s = f.readline(); ind = s.find( '#' )+1
        tmp \
          = np.array( list( map( np.float64, s[ind:].split() ) ), \
                      np.float64 )
        omegaR_err[r,rs] = tmp[1]
        omegaI_err[r,rs] = tmp[2]

        f.close()

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = ['#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00']

fig, axs = plt.subplots( R.shape[0], 1)#, figsize = (16,9) )

m = 0
for r in range( R.shape[0] ):
    for rs in range( Rs.shape[0] ):

        dataFileName \
          = '.{:}_LegendrePowerSpectrum.dat'.format( ID[r,rs] )

        if not isfile( dataFileName ):
            print( '{:} does not exist. Skipping.' \
                   .format( dataFileName ) )
            continue

        tt  = t [r,rs]
        P1t = P1[r,rs]
        t0t = t0[r,rs]
        t1t = t1[r,rs]

        tt  = np.copy( tt [0:indd[r,rs]] )
        P1t = np.copy( P1t[0:indd[r,rs]] )

        indF = np.where( ( tt >= t0t ) & ( tt <= t1t ) )[0]

        tF = tt[indF]

        logFt   = LogF  [r,rs]
        omegaRt = omegaR[r,rs]
        omegaIt = omegaI[r,rs]
        deltat  = delta [r,rs]

        F = np.exp( FittingFunction \
                      ( tF - tF[0], logFt, \
                        omegaRt, omegaIt, deltat ) )

        tau = T_SASI[r,rs]

        ind = np.where( tt/tau <= 10.0 )[0]

        if not vsTau: tau = 1.0

        if R.shape[0] == 1:
            axs   .plot( tt[ind]/tau, P1t[ind], '-', color = color[rs], \
                         label = r'$\texttt{{{:}}}$'.format( ID[r,rs] ) )
        else:
            axs[r].plot( tt[ind]/tau, P1t[ind], '-', color = color[rs], \
                         label = r'$\texttt{{{:}}}$'.format( ID[r,rs] ) )
#            axs[r].plot( tF / tau, F, color = 'r' )

        # END for rs in range( Rs.shape[0] )

    if R.shape[0] == 1:

        axs.grid()
        axs.legend()
        axs.set_yscale( 'log' )
#        axs.set_ylim( 1.0e11, 5.0e26 )

        if vsTau:
            axs.set_xlim( -0.5, 10.5 )
        else:
            if stage == 'early':
                axs.set_xlim( -10.0, 600.0 )
            elif stage == 'late':
                axs.set_xlim( -1.0, 140.0 )
    else:

        axs[r].grid()
        axs[r].legend()
        axs[r].set_yscale( 'log' )
        axs[r].set_ylim( 1.0e11, 5.0e26 )

        if vsTau:
            axs[r].set_xlim( -0.5, 10.5 )
        else:
            if stage == 'early':
                axs[r].set_xlim( -10.0, 600.0 )
            elif stage == 'late':
                axs[r].set_xlim( -1.0, 140.0 )
        if r == 0: axs[r].xaxis.set_ticklabels( '' )

    # END for r in range( R.shape[0] )

#if R.shape[0] == 1:
#    axs.xaxis.set_ticklabels( '' )
#else:
#    axs[0].xaxis.set_ticklabels( '' )

if vsTau:
    fig.supxlabel \
      ( r'$t/T_{\mathrm{SASI}}$', y = +0.025, fontsize = 15 )
else:
    fig.supxlabel \
      ( 'Time [ms]'             , y = +0.025, fontsize = 15 )

if stage == 'early':
    fig.suptitle( 'Early-Stage Models', y = 0.95 )
elif stage == 'late':
    fig.suptitle( 'Late-Stage Models' , y = 0.95 )

fig.supylabel( r'$H_{1}$ [cgs]', x = +0.025, fontsize = 15 )

plt.subplots_adjust( hspace = 0.0 )

if saveFig:

    if stage == 'early':
        if vsTau:
            fileName \
              = '/home/kkadoogan/fig.PowerInLegendreMode_earlyStage_tau.png'
        else:
            fileName \
              = '/home/kkadoogan/fig.PowerInLegendreMode_earlyStage_t.png'
    elif stage == 'late':
        if vsTau:
            fileName \
              = '/home/kkadoogan/fig.PowerInLegendreMode_lateStage_tau.png'
        else:
            fileName \
              = '/home/kkadoogan/fig.PowerInLegendreMode_lateStage_t.png'

    print( '\n  Saving figure: {:}'.format( fileName ) )

    plt.savefig( fileName, dpi = 300 )

else:

    plt.show()

import os
os.system( 'rm -rf __pycache__ ' )
