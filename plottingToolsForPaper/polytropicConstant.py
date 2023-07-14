#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
plt.style.use( 'publication.sty' )

Gamma = 4.0 / 3.0
G     = 6.67e-8
Msun  = 2.0e33
Mdot  = 0.3 * Msun
K1 = 2.0e14

def y( M, Mdot, Rs ):
    V1   = -np.sqrt( 2.0 * G * M / Rs )
    rho1 = -Mdot / ( 4.0 * np.pi * Rs**2 * V1 )
    return V1**2 / ( Gamma * rho1**( Gamma - 1.0 ) )

M  = np.linspace( 1.4 , 2.8  , 1000 ) * Msun
Rs = np.linspace( 60.0, 180.0, 1000 ) * 1.0e3

Mv, Rsv = np.meshgrid( M, Rs )

extent = [ M.min()/Msun, M.max()/Msun, Rs.min()/1.0e3, Rs.max()/1.0e3 ]

yv = np.sqrt( y( Mv, Mdot, Rsv ) / K1 )

plt.title( r'$K_{1}=2\times10^{14}\,\left[\mathrm{cgs}\right]$' )
im = plt.imshow( yv, \
                 origin = 'lower', \
                 aspect = 'auto', \
#                 norm = LogNorm( vmin = yv.min(), vmax = yv.max() ), \
                 extent = extent )
cbar = plt.colorbar( im )
cbar.set_label( r'$\mathrm{Ma}_{1}$' )
#cbar.set_label( r'$K_{1}\,\mathrm{Ma}^{2}$' )
plt.xlabel( r'$M_{\textsc{pns}}/\mathrm{M}_{\odot}$' )
plt.ylabel( r'$R_{\textsc{S}}/\mathrm{km}$' )
#plt.show()
plt.savefig( '../../../fig.MachNumber.png', dpi = 300 )
