#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( './publication.sty' )
from os.path import isfile

from globalVariables import *

Models = {}
with open( dataDirectory + 'fft.dat' ) as f:
    i = -1
    for line in f:
       i += 1
       if i < 2: continue
       x = line.split()
       Models[x[0]] = [ np.float64( x[1] ), np.float64( x[2] ) ]

IDs = [ 'M1.4_Rpns040_Rs1.20e2', \
        'M1.4_Rpns040_Rs1.50e2', \
        'M1.4_Rpns040_Rs1.75e2', \
        'M1.4_Rpns070_Rs1.50e2', \
        'M1.8_Rpns020_Rs7.00e1', \
        'M2.8_Rpns020_Rs6.00e1', \
        'M2.8_Rpns020_Rs7.00e1' ]

col = [ '#377eb8', '#ff7f00' ]
mkr = [ ','      , ','       ]
cs  = 5.0

NX = 5.0
NY = NX * 3/4
fig, ax = plt.subplots( 1, 1, figsize = (NX,NY) )

for i in range( len( IDs ) ):

    ID = IDs[i]

    dataFileName_NR \
    = dataDirectory + 'LegendrePowerSpectrum_NR2D_{:}.dat'.format( ID )

    dataFileName_GR \
    = dataDirectory + 'LegendrePowerSpectrum_GR2D_{:}.dat'.format( ID )

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

    Rpns =             ID[9:12]
    Rsh  = np.float64( ID[15:21] )

    if i == 0:

        ax.errorbar( Rsh, G_NR , ls = 'none', \
                     yerr = dG_NR, capsize = cs, \
                     c = col[0], marker = mkr[0], mfc = 'none' , \
                     label = r'\texttt{{NR}}' )
        ax.errorbar( Rsh, G_GR , ls = 'none', \
                     yerr = dG_GR, capsize = cs, \
                     c = col[1], marker = mkr[1], mfc = 'none', \
                     label = r'\texttt{{GR}}' )

    else:

        ax.errorbar( Rsh, G_NR , ls = 'none', \
                     yerr = dG_NR, capsize = cs, \
                     c = col[0], marker = mkr[0], mfc = 'none' )
        ax.errorbar( Rsh, G_GR , ls = 'none', \
                     yerr = dG_GR, capsize = cs, \
                     c = col[1], marker = mkr[1], mfc = 'none' )

    if Rpns == '070':
        ax.text( 1.03 * Rsh, 0.9 * G_NR, \
                 r'$R_{\mathrm{PNS}}=70\,\mathrm{km}$' )

    T_NR, dT_NR = Models['NR2D_'+ID]
    T_GR, dT_GR = Models['GR2D_'+ID]

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
ax.set_xlabel( r'$R_{\textrm{sh}}\ \left[\mathrm{km}\right]$' )
ax.set_ylabel( r'$\omega\ \left[\mathrm{ms}^{-1}\right]$' )

plt.show()

#figName = figuresDirectory + 'fig.GrowthRateComparison.pdf'
#figName = 'fig.GrowthRateComparison.png'
#plt.savefig( figName, dpi = 300 )
#print( '\n  Saved {:}'.format( figName ) )

plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
