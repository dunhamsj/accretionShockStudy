#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( './publication.sty' )
from os.path import isfile

Rpns = [ '040', '020' ]
M    = [ '1.4', '2.8' ]
Rs   = [ [ '1.20e2', '1.50e2', '1.75e2' ], \
         [ '6.00e1', '7.00e1' ] ]

T_aa = {}
T_ac = {}
with open( '../plottingData/T_SASI.dat' ) as f:
    i = -1
    for line in f:
       i += 1
       if i < 3: continue
       x = line.split()
       T_aa[x[0]] = np.float64( x[1] )
       T_ac[x[0]] = np.float64( x[2] )

col = [ '#ff7f00', '#377eb8', '#ff7f00' ]
mkr = [ 'x'      , ','      , ','      , '.', 's' ]
cs = 5.0
ms = 2
fs = 'full'
lw = 0.1

NX = 5.0
NY = NX * 3/4
fig, ax = plt.subplots( 1, 1, figsize = (NX,NY) )

Models = {}
with open( '../plottingData/fft.dat' ) as f:
    i = -1
    for line in f:
       i += 1
       if i < 2: continue
       x = line.split()
       Models[x[0]] = [ np.float64( x[1] ), np.float64( x[2] ) ]

T = {}
with open( '../plottingData/Teye.dat' ) as f:
    i = -1
    for line in f:
       i += 1
       if i < 1: continue
       x = line.split()
       T[x[0]] = [ np.float64( x[1] ), np.float64( x[2] ) ]

i = -1
for m in range( len( M ) ):
    rpns = m
    for rs in range( len( Rs[m] ) ):

        ID = 'M{:}_Rpns{:}_Rs{:}'.format( M[m], Rpns[rpns], Rs[rpns][rs] )

        dataFileName_NR \
        = '../plottingData/NR2D_{:}_LegendrePowerSpectrum.dat'.format( ID )

        dataFileName_GR \
        = '../plottingData/GR2D_{:}_LegendrePowerSpectrum.dat'.format( ID )

        if not isfile( dataFileName_NR ):
            print( 'File {:} not found. Skipping'.format( dataFileName_NR ) )
            continue

        i += 1

        T_NR, dT_NR = Models['NR2D_'+ID]
        T_GR, dT_GR = Models['GR2D_'+ID]

        T_aa_NR = T_aa['NR1D_'+ID]
        T_ac_NR = T_ac['NR1D_'+ID]

        T_aa_GR = T_aa['GR1D_'+ID]
        T_ac_GR = T_ac['GR1D_'+ID]

        Teye_NR = T['NR2D_'+ID][1] / T['NR2D_'+ID][0]
        Teye_GR = T['GR2D_'+ID][1] / T['GR2D_'+ID][0]

        Rsh = np.float64( Rs[m][rs] )

        if rs == 0 and m == 0:

            ax.errorbar( Rsh, T_NR , ls = 'none', \
                         yerr = dT_NR, capsize = cs, lw = lw, \
                         c = col[1], marker = mkr[1], mfc = 'none' , \
                         label = r'\texttt{{NR}}' )
            ax.errorbar( Rsh, T_GR , ls = 'none', \
                         yerr = dT_GR, capsize = cs, lw = lw, \
                         c = col[2], marker = mkr[2], mfc = 'none', \
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
#            ax.plot    ( Rsh, Teye_NR, ls = 'none', \
#                         c = col[1], marker = mkr[4], lw = lw, \
#                         ms = ms, fillstyle = fs, \
#                         label = r'$T^{\mathrm{NR}}_{\mathrm{eye}}$' )
#            ax.plot    ( Rsh, Teye_GR, ls = 'none', \
#                         c = col[0], marker = mkr[4], lw = lw, \
#                         ms = ms, fillstyle = fs, \
#                         label = r'$T^{\mathrm{GR}}_{\mathrm{eye}}$' )

        else:

            ax.errorbar( Rsh, T_NR , ls = 'none', \
                         yerr = dT_NR, capsize = cs, lw = lw, \
                         c = col[1], marker = mkr[1], mfc = 'none' )
            ax.errorbar( Rsh, T_GR , ls = 'none', \
                         yerr = dT_GR, capsize = cs, lw = lw, \
                         c = col[2], marker = mkr[2], mfc = 'none' )
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
#            ax.plot    ( Rsh, Teye_NR, ls = 'none', \
#                         c = col[1], marker = mkr[4], lw = lw, \
#                         ms = ms, fillstyle = fs )
#            ax.plot    ( Rsh, Teye_GR, ls = 'none', \
#                         c = col[0], marker = mkr[4], lw = lw, \
#                         ms = ms, fillstyle = fs )

handles, labels = ax.get_legend_handles_labels()
#mapping = [ 6, 7, 4, 5, 0, 1, 2, 3 ]
mapping = [ 4, 5, 0, 1, 2, 3 ]
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
ax.set_xlabel( r'$R_{\textsc{s}}\ \left[\mathrm{km}\right]$' )
ax.set_ylabel( r'$T\ \left[\mathrm{ms}\right]$' )
#plt.show()
plt.savefig( '../Figures/fig.OscillationPeriodComparison.pdf', dpi = 300 )
#plt.savefig( 'fig.OscillationPeriodComparison.png', dpi = 300 )
plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
