#!/usr/bin/env python3

import yt
import numpy as np
from gc import collect

from globalVariables import *

yt.funcs.mylog.setLevel(40) # Suppress initial yt output to screen

def ComputeTimeScales( plotFileDirectory, rInner, rOuter, rel ):

    # Read in data

    ds       = yt.load( '{:}'.format( plotFileDirectory ) )
    MaxLevel = ds.index.max_level
    nX       = ds.domain_dimensions
    xL       = ds.domain_left_edge
    xU       = ds.domain_right_edge

    CoveringGrid \
      = ds.covering_grid \
          ( level           = MaxLevel, \
            left_edge       = xL, \
            dims            = nX * 2**MaxLevel, \
            num_ghost_zones = nX[0] )

    ds.force_periodicity()

    xL = np.copy( xL.to_ndarray() )
    xU = np.copy( xU.to_ndarray() )

    # Get mesh and isolate elements below shock

    dr = ( xU[0] - xL[0] ) / np.float64( nX[0] )

    r = np.linspace( xL[0] + dr / 2.0, xU[0] - dr / 2.0, nX[0] )

    # Isolate shocked region

    ind = np.where( ( r > rInner ) & ( r < rOuter ) )[0]

    alpha = np.copy( CoveringGrid['GF_Alpha'].to_ndarray()[ind,0,0] )
    Gm11  = np.copy( CoveringGrid['GF_Gm_11'].to_ndarray()[ind,0,0] )
    Gm22  = np.copy( CoveringGrid['GF_Gm_22'].to_ndarray()[ind,0,0] )
    V     = np.copy( CoveringGrid['PF_V1'   ].to_ndarray()[ind,0,0] )
    Cs    = np.copy( CoveringGrid['AF_Cs'   ].to_ndarray()[ind,0,0] )

    del ds
    collect()

    # Integrate over shocked region to get advection/acoustic times

    tauAd = 0.0
    tauAc = 0.0

    nShocked = np.int64( ind.shape[0] )

    c = 2.99792458e5

    VSq = Gm11 * V  * V

    if  ( rel == 'NR' ):
        lambda0 = V
        lambdap = V + Cs * np.sqrt( 1.0 / Gm11 )
        lambda2 = Cs * np.sqrt( 1.0 / Gm22 ) # Assume V2 = 0
    elif( rel == 'GR' ):
        lambda0 = alpha * V
        lambdap = alpha / ( 1.0 - VSq * Cs**2 / c**4 ) \
                    * ( V * ( 1.0 - Cs**2 / c**2 ) \
                    + Cs * np.sqrt( ( 1.0 - VSq / c**2 ) \
                    * ( 1.0 / Gm11 * ( 1.0 - VSq * Cs**2 / c**4 ) \
                    - V / c * V / c * ( 1.0 - Cs**2 / c**2 ) ) ) )
        lambda2 = alpha / ( 1.0 - VSq * Cs**2 / c**4 ) \
                       * Cs * np.sqrt( ( 1.0 - VSq / c**2 ) \
                       * 1.0 / Gm22 * ( 1.0 - VSq * Cs**2 / c**4 ) ) # Assume V2 = 0

    lambda2 *= np.sqrt( Gm22 )

    for i in range( ind.shape[0] ):

        # Account for integrating inwards in advective timescale
        tauAd += -np.sqrt( Gm11[ind[i]] ) * dr / lambda0[ind[i]]
        tauAc += +np.sqrt( Gm11[ind[i]] ) * dr / lambdap[ind[i]]

    ind085Rs = np.where( r >= 0.85 * rOuter )[0][0]
    T_ac = 2.0 * np.pi * r[ind085Rs] / lambda2[ind085Rs]

    # Convert to ms

    tauAd *= 1.0e3
    tauAc *= 1.0e3
    T_aa = tauAd + tauAc

    T_ac *= 1.0e3

    return tauAd, tauAc, T_aa, T_ac

if __name__ == '__main__':

    IDs = [ 'NR1D_M1.4_Rpns040_Rs1.20e2', \
            'GR1D_M1.4_Rpns040_Rs1.20e2', \
            'NR1D_M1.4_Rpns040_Rs1.50e2', \
            'GR1D_M1.4_Rpns040_Rs1.50e2', \
            'NR1D_M1.4_Rpns070_Rs1.50e2', \
            'GR1D_M1.4_Rpns070_Rs1.50e2', \
            'NR1D_M1.4_Rpns040_Rs1.75e2', \
            'GR1D_M1.4_Rpns040_Rs1.75e2', \
            'NR1D_M1.8_Rpns020_Rs7.00e1', \
            'GR1D_M1.8_Rpns020_Rs7.00e1', \
            'NR1D_M2.8_Rpns020_Rs6.00e1', \
            'GR1D_M2.8_Rpns020_Rs6.00e1', \
            'NR1D_M2.8_Rpns020_Rs7.00e1', \
            'GR1D_M2.8_Rpns020_Rs7.00e1' ]

    with open( dataDirectory + 'T_SASI.dat', 'w' ) as f:

        f.write( '# Generated from computeTimeScales.py\n' )
        f.write( '# Model T_aa/ms T_ac/ms\n\n' )

        for i in range( len( IDs ) ):

            ID = IDs[i]

            rel  =             ID[0:2]
            Rpns = np.float64( ID[14:17] )
            Rsh  = np.float64( ID[20:26] )

            Root = plotfileRootDirectory + '1D/{:}/'.format( ID )

            pfd = Root + '{:}.plt00000000'.format( ID )

            tAd, tAc, T_aa, T_ac \
              = ComputeTimeScales( pfd, Rpns, Rsh, rel )

            f.write( ID + ' {:.16e} {:.16e}\n'.format( T_aa, T_ac ) )

    import os
    os.system( 'rm -rf __pycache__ ' )
