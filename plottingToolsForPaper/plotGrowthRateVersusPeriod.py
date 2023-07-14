#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )
from scipy.optimize import curve_fit

T_ES = np.array( [ [ 20.7488, 34.4430, 47.7477 ], \
                   [ 23.6262, 38.7335, 53.6116 ] ], np.float64 )
T_LS = np.array( [ [ 5.2217, 7.4151 ], \
                   [ 8.6407, 12.1527 ] ], np.float64 )
G_ES = np.array( [ [ 0.0733, 0.0409, 0.0300 ], \
                   [ 0.0578, 0.0360, 0.0265 ] ], np.float64 )
G_LS = np.array( [ [ 0.2910, 0.1897 ], \
                   [ 0.1365, 0.0954 ] ], np.float64 )

def f( x, m, b ):
    return m * x + b

T_ESS = T_ES.flatten()
G_ESS = G_ES.flatten()
T_LSS = T_LS.flatten()
G_LSS = G_LS.flatten()

T = np.hstack( (T_ESS,T_LSS) )
G = np.hstack( (G_ESS,G_LSS) )

ind = np.argsort( T )
T = np.copy( T[ind] )
G = np.copy( G[ind] )
[ m, b ], pcov = curve_fit( f, np.log10( T ), np.log10( G ) )


fig, ax = plt.subplots( 1, 1 )

log10G = m * np.log10( T ) + b

ax.plot( T, 10**( log10G ), 'k-', \
         label = r'$\log_{{10}}\omega={:.3f}\,\log_{{10}}T+{:.3f}$' \
                 .format( m, b ) )

ax.plot( T_LS[0], G_LS[0], 'b.', label = 'Late-stage (NR)' )
ax.plot( T_LS[1], G_LS[1], 'b^', label = 'Late-stage (GR)' )
ax.plot( T_ES[0], G_ES[0], 'r.', label = 'Early-stage (NR)' )
ax.plot( T_ES[1], G_ES[1], 'r^', label = 'Early-stage (GR)' )

ax.set_xlabel( r'$T\ \left[\mathrm{ms}\right]$' )
ax.set_ylabel( r'$\omega\ \left[\mathrm{ms}^{-1}\right]$' )

ax.set_xscale( 'log' )
ax.set_yscale( 'log' )

ax.legend()

#filename = '/Users/dunhamsj/fig.GrowthRateVersusPeriod.png'
#print( '\n  Saving {:}'.format( filename ) )
#plt.savefig( filename, dpi = 300 )

plt.show()
