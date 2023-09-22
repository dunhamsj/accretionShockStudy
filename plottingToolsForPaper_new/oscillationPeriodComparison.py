#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( './publication.sty' )

from globalVariables import *

IDs = [ 'M1.4_Rpns040_Rs1.20e2', \
        'M1.4_Rpns040_Rs1.50e2', \
        'M1.4_Rpns040_Rs1.75e2', \
        'M1.4_Rpns070_Rs1.50e2', \
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

col = [ '#ff7f00', '#377eb8', 'red', 'blue' ]
mkr = [ 'x'      , ','      , ','      , '.', 's' ]
cs = 5.0
ms = 10
ms1= 4
fs = 'full'
lw = 0.1

NX = 5.0
NY = NX * 3/4
#fig, ax = plt.subplots( 1, 1, figsize = (NX,NY) )
fig, ax = plt.subplots( 1, 1, figsize = (8,6) )

Models = {}
with open( dataDirectory + 'fft.dat' ) as f:
    i = -1
    for line in f:
       i += 1
       if i < 2: continue
       x = line.split()
       Models[x[0]] = [ np.float64( x[1] ), np.float64( x[2] ) ]

for i in range( len( IDs ) ):

    ID = IDs[i]

    T_NR, dT_NR = Models['NR2D_'+ID]
    T_GR, dT_GR = Models['GR2D_'+ID]

    T_aa_NR = T_aa['NR1D_'+ID]
    T_ac_NR = T_ac['NR1D_'+ID]

    T_aa_GR = T_aa['GR1D_'+ID]
    T_ac_GR = T_ac['GR1D_'+ID]

    Rpns =             ID[9:12]
    Rsh  = np.float64( ID[15:21] )

    if Rpns == '070':

        ax.errorbar( Rsh, T_NR , ls = 'none', \
                     yerr = dT_NR, capsize = cs, lw = lw, \
                     c = col[3], marker = mkr[1], ms = ms1, mfc = 'none' , \
                     label = r'\texttt{{NR}}' )
        ax.errorbar( Rsh, T_GR , ls = 'none', \
                     yerr = dT_GR, capsize = cs, lw = lw, \
                     c = col[2], marker = mkr[2], ms = ms1, mfc = 'none', \
                     label = r'\texttt{{GR}}' )
        ax.plot    ( Rsh, T_aa_NR, ls = 'none', \
                     c = col[3], marker = mkr[0], \
                     ms = ms, \
                     label = r'$T^{\mathrm{NR}}_{\mathrm{aa}}$' )
        ax.plot    ( Rsh, T_aa_GR, ls = 'none', \
                     c = col[2], marker = mkr[0], \
                     ms = ms, \
                     label = r'$T^{\mathrm{GR}}_{\mathrm{aa}}$' )
        ax.plot    ( Rsh, T_ac_NR, ls = 'none', \
                     c = col[3], marker = mkr[3], lw = lw, \
                     ms = ms, fillstyle = fs, \
                     label = r'$T^{\mathrm{NR}}_{\mathrm{ac}}$' )
        ax.plot    ( Rsh, T_ac_GR, ls = 'none', \
                     c = col[2], marker = mkr[3], lw = lw, \
                     ms = ms, fillstyle = fs, \
                     label = r'$T^{\mathrm{GR}}_{\mathrm{ac}}$' )


    elif i == 0:

        ax.errorbar( Rsh, T_NR , ls = 'none', \
                     yerr = dT_NR, capsize = cs, lw = lw, \
                     c = col[1], marker = mkr[1], ms = ms1, mfc = 'none' , \
                     label = r'\texttt{{NR}}' )
        ax.errorbar( Rsh, T_GR , ls = 'none', \
                     yerr = dT_GR, capsize = cs, lw = lw, \
                     c = col[0], marker = mkr[2], ms = ms1, mfc = 'none', \
                     label = r'\texttt{{GR}}' )
        ax.plot    ( Rsh, T_aa_NR, ls = 'none', \
                     c = col[1], marker = mkr[0], \
                     ms = ms, \
                     label = r'$T^{\mathrm{NR}}_{\mathrm{aa}}$' )
        ax.plot    ( Rsh, T_aa_GR, ls = 'none', \
                     c = col[0], marker = mkr[0], \
                     ms = ms, \
                     label = r'$T^{\mathrm{GR}}_{\mathrm{aa}}$' )
        ax.plot    ( Rsh, T_ac_NR, ls = 'none', \
                     c = col[1], marker = mkr[3], lw = lw, \
                     ms = ms, fillstyle = fs, \
                     label = r'$T^{\mathrm{NR}}_{\mathrm{ac}}$' )
        ax.plot    ( Rsh, T_ac_GR, ls = 'none', \
                     c = col[0], marker = mkr[3], lw = lw, \
                     ms = ms, fillstyle = fs, \
                     label = r'$T^{\mathrm{GR}}_{\mathrm{ac}}$' )

    else:

        ax.errorbar( Rsh, T_NR , ls = 'none', \
                     yerr = dT_NR, capsize = cs, lw = lw, \
                     c = col[1], marker = mkr[1], ms = ms1, mfc = 'none' )
        ax.errorbar( Rsh, T_GR , ls = 'none', \
                     yerr = dT_GR, capsize = cs, lw = lw, \
                     c = col[0], marker = mkr[2], ms = ms1, mfc = 'none' )
        ax.plot    ( Rsh, T_aa_NR, ls = 'none', \
                     c = col[1], marker = mkr[0], \
                     ms = ms )
        ax.plot    ( Rsh, T_aa_GR, ls = 'none', \
                     c = col[0], marker = mkr[0], \
                     ms = ms )
        ax.plot    ( Rsh, T_ac_NR, ls = 'none', \
                     c = col[1], marker = mkr[3], lw = lw, \
                     ms = ms, fillstyle = fs )
        ax.plot    ( Rsh, T_ac_GR, ls = 'none', \
                     c = col[0], marker = mkr[3], lw = lw, \
                     ms = ms, fillstyle = fs )

handles, labels = ax.get_legend_handles_labels()
mapping = [ 8, 9, 10, 11, 0, 1, 4, 5, 2, 3, 6, 7 ]
#mapping = [ 4, 5, 0, 1, 2, 3 ]
h = []
l = []
for i in range( len( handles ) ):
    h.append( handles[mapping[i]] )
    l.append( labels [mapping[i]] )
ax.legend( h, l, prop = { 'size' : 10 }, loc = 2 )
ax.grid()

ax.text( 60 , 20, r'$\texttt{M2.8}$', fontsize = 15 )
ax.text( 140, 5 , r'$\texttt{M1.4}$', fontsize = 15 )

ax.tick_params( which = 'both', top = True, right = True )
ax.set_xlabel( r'$R_{\textrm{sh}}\ \left[\mathrm{km}\right]$' )
ax.set_ylabel( r'$T\ \left[\mathrm{ms}\right]$' )

yticks = np.linspace( 0, 80, 9 )
ax.set_yticks( yticks )

plt.show()

#figName = figuresDirectory + 'fig.OscillationPeriodComparison.pdf'
#figName = 'fig.png'
#plt.savefig( figName, dpi = 300 )
#print( '\n  Saved {:}'.format( figName ) )

plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
