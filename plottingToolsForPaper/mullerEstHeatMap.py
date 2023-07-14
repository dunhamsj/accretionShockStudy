#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )
from matplotlib.colors import LogNorm
from scipy.interpolate import interp1d
from sys import argv

M = argv[1]

tauAd_GR = np.loadtxt( '../plottingData/tauAd_GR_M{:}.dat'.format( M ) )
tauAc_GR = np.loadtxt( '../plottingData/tauAc_GR_M{:}.dat'.format( M ) )
tauAd_NR = np.loadtxt( '../plottingData/tauAd_NR_M{:}.dat'.format( M ) )
tauAc_NR = np.loadtxt( '../plottingData/tauAc_NR_M{:}.dat'.format( M ) )

with open( '../plottingData/tauAd_GR_M{:}.dat'.format( M ), 'r' ) as f:
    Rs   = f.readline()[3:-2]
    RPNS = f.readline()[3:-2]
Rs   = np.array( Rs  .split( ',' ), np.float64 )
RPNS = np.array( RPNS.split( ',' ), np.float64 )

Rs   = np.array( [ np.float64( rs   ) for rs   in Rs   ], np.float64 )
RPNS = np.array( [ np.float64( rpns ) for rpns in RPNS ], np.float64 )

T_SASI_GR = tauAd_GR + tauAc_GR
T_SASI_NR = tauAd_NR + tauAc_NR

fig, ax = plt.subplots()

dRs   = np.diff( Rs   )[0]
dRPNS = np.diff( RPNS )[0]
extent = [ RPNS.min()-0.5*dRPNS, RPNS.max()+0.5*dRPNS, \
           Rs  .min()-0.5*dRs  , Rs  .max()+0.5*dRs ]

dT = T_SASI_GR / T_SASI_NR

cmap = 'terrain'

if M == '1.4':
    vmin = 1.0
    vmax = 3.0

    # Heat-map colorbar
    ticks = np.linspace( vmin, vmax, 6 )
    ticklabels = [ '{:.1f}'.format( tick ) for tick in ticks ]

    # Contour plot
    #levels = list( np.arange( 1.125, 1.250, 0.02 ) )
    #for lev in [ 1.3, 1.4, 1.5, 1.75, 2.0 ]:
    #    levels.append( lev )
    levels = [ 1.125   , 1.135   , 1.150   , 1.175   , 1.200     , 1.250     , 1.325   , 1.50     , 2.000   ]
    manual = [ [40,165], [37,150], [35,150], [30,150], [23.5,148], [18.5,159], [15,130], [9.5,108], [6,90]  ]

elif M == '2.8':
    vmin =1.0
    vmax = 10.0

    # Heat-map colorbar
    ticks = [ 1.0, 5.0, 10.0 ]
    ticklabels = [ str( int( tick ) ) for tick in ticks ]

    # Contour plot
    #levels = list( np.arange( 1.25, 1.5, 0.04 ) )
    #for lev in [ 1.55, 1.6, 1.7, 1.8, 1.9, 2.0, 2.25, 2.5, \
    #             3.0, 4.0, 5.0 ]:
    #    levels.append( lev )
    levels = [ 1.27    , 1.30      , 1.40    , 1.50    , 1.60    , 1.70       , 2.0    , 2.5       , 5.0    ]
    manual = [ [39,160], [37.5,127], [26,160], [22,132], [20,120], [15.65,120], [13,94], [9.55,110], [6,90] ]

im = ax.imshow( dT, \
                extent = extent, \
                aspect = 'auto', \
                origin = 'lower', \
                cmap = cmap, \
                interpolation = None, \
                norm = LogNorm( vmin = vmin , vmax = vmax ) )

xv, yv = np.meshgrid( RPNS, Rs )
contour = ax.contour( xv, yv, dT, \
                      levels = levels, \
                      norm = LogNorm(), \
                      colors = 'white', \
                      linestyles = ':', \
                      origin = 'lower', \
                      extent = extent )
clabels = ax.clabel( contour, levels, manual = manual )

if   M == '1.4':
    x0 = np.array( [ 40 , 40 , 40  ], np.float64 )
    y0 = np.array( [ 120, 150, 175 ], np.float64 )
    ax.plot( x0, y0, 'wo' )

elif M == '2.8':
    x0 = np.array( [ 20, 20 ], np.float64 )
    y0 = np.array( [ 60, 70 ], np.float64 )
    ax.plot( x0, y0, 'wo' )

ax.tick_params( which = 'both', top = True, right = True )

x = np.linspace( RPNS.min()-1.5, RPNS.max()+1.5, 100 )
Rso = y0 / x0

ax.set_xlim( extent[0], extent[1] )
ax.set_ylim( extent[2], extent[3] )

# align Rso label with corresponding line
xt = ax.get_xticks()
yt = ax.get_yticks()
sc = np.mean( np.diff( xt ) / np.diff( yt ) )

fl = 29.75
os = 1.05
# 3.00
y = Rso[0] * x
f = interp1d( x, y )
m = sc*( y[-1] - y[-2] ) / ( x[-1] - x[-2] )
theta = np.arctan( m ) * 180.0 / np.pi
#ax.plot( x, y, 'w-' )
#ax.text( fl, f(fl)*os, r'$\bf{{R_{{\textsc{{so}}}}={:.2f}}}$' \
#         .format( Rso[0] ), \
#         rotation = theta, color = 'w' )

# 3.75
y = Rso[1] * x
f = interp1d( x, y )
m = sc*( y[-1] - y[-2] ) / ( x[-1] - x[-2] )
theta = np.arctan( m ) * 180.0 / np.pi
#ax.plot( x, y, 'w-' )
#ax.text( fl, f(fl)*os, r'$\bf{{R_{{\textsc{{so}}}}={:.2f}}}$' \
#         .format( Rso[1] ), \
#         rotation = theta, color = 'w' )

# 4.375
if Rso.shape[0] > 2:
    y = Rso[2] * x
    f = interp1d( x, y )
    m = sc*( y[-1] - y[-2] ) / ( x[-1] - x[-2] )
    theta = np.arctan( m ) * 180.0 / np.pi
    #ax.plot( x, y, 'w-' )
    #ax.text( fl, f(fl)*os, r'$\bf{{R_{{\textsc{{so}}}}={:.2f}}}$' \
    #         .format( Rso[2] ), \
    #         rotation = theta, color = 'w' )

ax.set_xlabel( r'$R_{\textsc{pns}}\,\left[\mathrm{km}\right]$' )
ax.set_ylabel( r'$R_{\textsc{s}}\,\left[\mathrm{km}\right]$' )

ax.text( 35.0, 40.0, r'$\texttt{{M{:}}}$'.format( M ), fontsize = 15 )

#if  ( M == '1.4' ): ax.axvline( 40.0, color = 'r' )
#elif( M == '2.8' ): ax.axvline( 20.0, color = 'r' )
cbar = plt.colorbar( im, ticks = ticks )
cbar.set_ticklabels( ticklabels )
cbar.set_ticklabels( [], minor = True )
if M == '1.4': cbar.set_ticks( [], minor = True )
#cbar.set_label( r'$\frac{T_{\textsc{gr}}-T_{\textsc{nr}}}{T_{\textsc{nr}}}$' )
#cbar.set_label( r'$T_{\textsc{gr}}-T_{\textsc{nr}}\,\left[\mathrm{ms}\right]$' )
cbar.set_label( r'$T_{\textsc{gr}}/T_{\textsc{nr}}$' )

#plt.show()
plt.savefig( '../Figures/fig.MullerEstimate_M{:}.pdf'.format( M ), dpi = 300 )
