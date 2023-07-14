#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( './publication.sty' )
from os.path import isfile

Rpns = [ '040', '020' ]
M    = [ '1.4', '2.8' ]
Rs   = [ [ '1.20e2', '1.50e2', '1.75e2' ], \
         [ '6.00e1', '7.00e1' ] ]

col = [ '#377eb8', '#ff7f00' ]
mkr = [ ','      , ','       ]
cs = 5.0

NX = 5.0
NY = NX * 3/4
fig, ax = plt.subplots( 1, 1, figsize = (NX,NY) )

i = -1
for m in range( len( M ) ):
    rpns = m
    for rs in range( len( Rs[m] ) ):

        dataFileName_NR \
        = '../plottingData/NR2D_M{:}_Rpns{:}_Rs{:}_LegendrePowerSpectrum.dat' \
            .format( M[m], Rpns[rpns], Rs[rpns][rs] )

        dataFileName_GR \
        = '../plottingData/GR2D_M{:}_Rpns{:}_Rs{:}_LegendrePowerSpectrum.dat' \
            .format( M[m], Rpns[rpns], Rs[rpns][rs] )

        if not isfile( dataFileName_NR ):
            print( 'File {:} not found. Skipping'.format( dataFileName_NR ) )
            continue

        i += 1

        # NR

        f = open( dataFileName_NR )
        dum = f.readline()
        s = f.readline(); ind = s.find( '#' )+1
        tmp \
          = np.array( list( map( np.float64, s[ind:].split() ) ), \
                      np.float64 )
        G_NR = tmp[3]
        dum = f.readline()
        s = f.readline(); ind = s.find( '#' )+1
        tmp \
          = np.array( list( map( np.float64, s[ind:].split() ) ), \
                      np.float64 )
        dG_NR = tmp[1]
        f.close()

        # GR

        f = open( dataFileName_GR )
        dum = f.readline()
        s = f.readline(); ind = s.find( '#' )+1
        tmp \
          = np.array( list( map( np.float64, s[ind:].split() ) ), \
                      np.float64 )
        G_GR = tmp[3]
        dum = f.readline()
        s = f.readline(); ind = s.find( '#' )+1
        tmp \
          = np.array( list( map( np.float64, s[ind:].split() ) ), \
                      np.float64 )
        dG_GR = tmp[1]
        f.close()

        if rs == 0 and m == 0:

            ax.errorbar( np.float64( Rs[m][rs] ), G_NR , ls = 'none', \
                         yerr = dG_NR, capsize = cs, \
                         c = col[0], marker = mkr[0], mfc = 'none' , \
                         label = r'\texttt{{NR}}' )
            ax.errorbar( np.float64( Rs[m][rs] ), G_GR , ls = 'none', \
                         yerr = dG_GR, capsize = cs, \
                         c = col[1], marker = mkr[1], mfc = 'none', \
                         label = r'\texttt{{GR}}' )

        else:

            ax.errorbar( np.float64( Rs[m][rs] ), G_NR , ls = 'none', \
                         yerr = dG_NR, capsize = cs, \
                         c = col[0], marker = mkr[0], mfc = 'none' )
            ax.errorbar( np.float64( Rs[m][rs] ), G_GR , ls = 'none', \
                         yerr = dG_GR, capsize = cs, \
                         c = col[1], marker = mkr[1], mfc = 'none' )

handles, labels = ax.get_legend_handles_labels()
mapping = [ 0, 1 ]
h = []
l = []
for i in range( len( handles ) ):
    h.append( handles[mapping[i]] )
    l.append( labels [mapping[i]] )
ax.legend( h, l, prop = { 'size' : 10 }, loc = 1 )
ax.grid()

ax.text( 60 , 0.05, r'$\texttt{M2.8}$', fontsize = 15 )
ax.text( 140, 0.10, r'$\texttt{M1.4}$', fontsize = 15 )

ax.tick_params( which = 'both', top = True, right = True )
ax.set_xlabel( r'$R_{\textsc{s}}\ \left[\mathrm{km}\right]$' )
ax.set_ylabel( r'$\omega\ \left[\mathrm{ms}^{-1}\right]$' )
plt.show()
#plt.savefig( '../Figures/fig.GrowthRateComparison.pdf', dpi = 300 )
plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
