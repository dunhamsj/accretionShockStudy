#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( './publication.sty' )

from globalVariables import *

IDs = [ 'M1.4_Rpns070_Rs1.50e2', \
        'M1.4_Rpns040_Rs1.20e2', \
        'M1.4_Rpns040_Rs1.50e2', \
        'M1.4_Rpns040_Rs1.75e2', \
        'M1.8_Rpns020_Rs7.00e1', \
        'M2.8_Rpns020_Rs6.00e1', \
        'M2.8_Rpns020_Rs7.00e1' ]

T_aa = {}
T_ac = {}
with open( dataDirectory + 'T_SASI.dat' ) as f:
    i = -1
    for line in f:
       i += 1
       if i < 3: continue
       x = line.split()
       T_aa[x[0]] = np.float64( x[1] )
       T_ac[x[0]] = np.float64( x[2] )

col = { '0.4' : '#ff7f00', \
        '0.7' : '#377eb8', \
        '1.8' : '#4daf4a', \
        '2.8' : '#f781bf' }
mkr = [ 's', 'o', 'p' ]

ms = 5

NX = 5.0
NY = NX * 3/4
fig, ax = plt.subplots( 1, 1, figsize = (7,5) )
axaa = ax.twinx()
axac = ax.twinx()
axaa.yaxis.set_visible( False )
axac.yaxis.set_visible( False )

Models = {}
with open( dataDirectory + 'fft.dat' ) as f:
    i = -1
    for line in f:
       i += 1
       if i < 2: continue
       x = line.split()
       Models[x[0]] = [ np.float64( x[1] ), np.float64( x[2] ) ]

xi1 = '0.'
for i in range( len( IDs ) ):

    ID = IDs[i]

    T_NR, dT_NR = Models['NR2D_'+ID]
    T_GR, dT_GR = Models['GR2D_'+ID]

    T_aa_NR = T_aa['NR1D_'+ID]
    T_ac_NR = T_ac['NR1D_'+ID]

    T_aa_GR = T_aa['GR1D_'+ID]
    T_ac_GR = T_ac['GR1D_'+ID]

    Rsh  = np.float64( ID[15:21] )

    M = np.float64( ID[1:4] )
    R = np.float64( ID[9:12] )
    xi = '{:.1f}'.format( M / ( R / 20.0 ) )

    if xi != xi1:

        ax.plot  ( Rsh, T_NR , ls = 'none', \
                       c = col[xi], marker = mkr[0], ms = ms, mfc = 'none', \
                       label = r'$\texttt{{NR}}, \xi={:}$'.format( xi ) )
        ax.plot  ( Rsh, T_GR , ls = 'none', \
                       c = col[xi], marker = mkr[0], ms = ms, \
                       label = r'$\texttt{{GR}}, \xi={:}$'.format( xi ) )
        axaa.plot( Rsh, T_aa_NR, ls = 'none', \
                   c = col[xi], marker = mkr[1], ms = ms, mfc = 'none', \
                   label = r'$T^{\mathrm{NR}}_{\mathrm{aa}}$' )
        axaa.plot( Rsh, T_aa_GR, ls = 'none', \
                   c = col[xi], marker = mkr[1], ms = ms, \
                   label = r'$T^{\mathrm{GR}}_{\mathrm{aa}}$' )
        axac.plot( Rsh, T_ac_NR, ls = 'none', \
                   c = col[xi], marker = mkr[2], ms = ms, mfc = 'none', \
                   label = r'$T^{\mathrm{NR}}_{\mathrm{ac}}$' )
        axac.plot( Rsh, T_ac_GR, ls = 'none', \
                   c = col[xi], marker = mkr[2], ms = ms, \
                   label = r'$T^{\mathrm{GR}}_{\mathrm{ac}}$' )

    else:

        ax.plot( Rsh, T_NR , ls = 'none', \
                     c = col[xi], marker = mkr[0], ms = ms, mfc = 'none' )
        ax.plot( Rsh, T_GR , ls = 'none', \
                     c = col[xi], marker = mkr[0], ms = ms )
        axaa.plot( Rsh, T_aa_NR, ls = 'none', \
                 c = col[xi], marker = mkr[1], ms = ms, mfc = 'none' )
        axaa.plot( Rsh, T_aa_GR, ls = 'none', \
                 c = col[xi], marker = mkr[1], ms = ms )
        axac.plot( Rsh, T_ac_NR, ls = 'none', \
                   c = col[xi], marker = mkr[2], ms = ms, mfc = 'none' )
        axac.plot( Rsh, T_ac_GR, ls = 'none', \
                   c = col[xi], marker = mkr[2], ms = ms )

    xi1 = xi

ax  .legend( loc = (0.45,0.01) )
axaa.legend( loc = (0.67,0.01) )
axac.legend( loc = (0.825,0.01) )
ax.grid( which = 'both' )

ax.tick_params( which = 'both', top = True, right = True )
ax.set_xlabel( r'$R_{\textrm{sh}}\ \left[\mathrm{km}\right]$' )
ax.set_ylabel( r'$T\ \left[\mathrm{ms}\right]$' )

#yticks = np.linspace( 0, 80, 9 )
#ax.set_yticks( yticks )

ax  .set_ylim( 3, 90 )
axaa.set_ylim( 3, 90 )
axac.set_ylim( 3, 90 )

ax  .set_yscale( 'log' )
axaa.set_yscale( 'log' )
axac.set_yscale( 'log' )


#plt.show()

figName = figuresDirectory + 'fig.OscillationPeriodComparison.pdf'
figName = home + 'fig.png'
plt.savefig( figName, dpi = 300 )
print( '\n  Saved {:}'.format( figName ) )

plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
