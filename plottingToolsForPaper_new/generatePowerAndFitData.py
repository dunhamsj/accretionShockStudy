#!/usr/bin/env python3

import numpy as np
from os.path import isdir

from ComputePowerInLegendreModes import ComputePowerInLegendreModes
from FitPowerToModel import FitPowerToModel
from computeTimeScales import ComputeTimeScales
from globalVariables import *

IDs = [ 'NR2D_M1.4_Rpns040_Rs1.20e2', \
        'GR2D_M1.4_Rpns040_Rs1.20e2', \
        'NR2D_M1.4_Rpns040_Rs1.50e2', \
        'GR2D_M1.4_Rpns040_Rs1.50e2', \
        'NR2D_M1.4_Rpns040_Rs1.75e2', \
        'GR2D_M1.4_Rpns040_Rs1.75e2', \
        'NR2D_M2.8_Rpns020_Rs6.00e1', \
        'GR2D_M2.8_Rpns020_Rs6.00e1', \
        'NR2D_M2.8_Rpns020_Rs7.00e1', \
        'GR2D_M2.8_Rpns020_Rs7.00e1' ]

IDs = [ 'NR2D_M2.8_Rpns024_Rs6.40e1' ]

#IDs = [ 'GR2D_M2.0_Mdot0.1_Rs150', \
#        'GR2D_M2.0_Mdot0.3_Rs150', \
#        'GR2D_M2.0_Mdot0.5_Rs150' ]

for i in range( len( IDs ) ):

    ID = IDs[i]

    rel  = ID[0:2]
    rsh  = np.float64( ID[20:26] )
    rpns = np.int64  ( ID[14:17] )

    #rel  = ID[0:2]
    #rsh  = np.float64( ID[-3:] )
    #rpns = 40
    #mdot = np.float64( ID[14:17] )

    plotfileDirectory \
      = plotfileRootDirectory + '2D/{:}/'.format( ID )

    #plotfileDirectory \
    #  = plotfileRootDirectory + '../oldData/{:}/'.format( ID )

    if not isdir( plotfileDirectory ):
        print( '\n{:} does not exist. Skipping.\n' \
               .format( plotfileDirectory ) )
        continue

    plotfileBaseName = '{:}.plt'.format( ID )
    #plotfileBaseName = '{:}.plt_'.format( ID )

    dataFileName = dataDirectory \
                     + 'LegendrePowerSpectrum_{:}.dat'.format( ID )

    ComputePowerInLegendreModes \
      ( plotfileDirectory, plotfileBaseName, dataFileName, \
        'DivV2', 0.8, 0.9, rsh, \
        fc = False, ow = False, verbose = True )

    t, P0, P1, P2, P3, P4 = np.loadtxt( dataFileName )

    LogF  = 31.0
    tauR  = 20.0
    delta = np.pi/4.0

    rInner = rpns
    rOuter = rsh
    tAd, tAc, T_aa, T_ac \
      = ComputeTimeScales \
          ( plotfileDirectory+plotfileBaseName+'00000000', \
            rInner, rOuter, rel )

    T_SASI = tAd + tAc
    tF0 = 1.0 * T_SASI
    tF1 = 8.0 * T_SASI

    omegaR = 1.0 / tauR
    omegaI = 2.0 * np.pi / T_SASI

    InitialGuess \
      = np.array( [ LogF, omegaR, omegaI, delta ], np.float64 )

    beta, perr \
      = FitPowerToModel \
          ( tF0, tF1, t, P1, InitialGuess )

    b = ''
    e = ''
    for i in range( len( beta ) ):
        b += str( beta[i] ) + ' '
    for i in range( len( perr ) ):
        e += str( perr[i] ) + ' '
    header = 'tF0, tF1, LogF1, omegaR, omegaI, delta\n' \
             + str( tF0 ) + ' ' + str( tF1 ) + ' ' + b \
             + '\ndLogF1, domegaR, domegaI, ddelta\n' + e \
             + '\nTime [ms], P0 [cgs], P1 [cgs], ' \
             + 'P2 [cgs], P3 [cgs], P4 [cgs]'

    t, P0, P1, P2, P3, P4 = np.loadtxt( dataFileName )

    Data = np.vstack( (t,P0,P1,P2,P3,P4) )
    np.savetxt( dataFileName, Data, header = header )

import os
os.system( 'rm -rf __pycache__ ' )
