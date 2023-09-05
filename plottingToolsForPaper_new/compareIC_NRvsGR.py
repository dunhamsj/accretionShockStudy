#!/usr/bin/env python3

from sys import argv
import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from UtilitiesModule import GetFileArray, GetData

M = argv[1]

if( M == '1.4' ):
    IDs = [ '1D_M1.4_Rpns003_Rs1.20e2', \
            '1D_M1.4_Rpns003_Rs1.50e2', \
            '1D_M1.4_Rpns003_Rs1.75e2' ]
else:
    IDs = [ '1D_M2.8_Rpns003_Rs6.00e1', \
            '1D_M2.8_Rpns003_Rs7.00e1' ]

nRuns = len( IDs )

plotfileDirectory = '../plottingData_new/'

nRows = 2
nCols = 2

ax00ylabel = r'$\rho/\rho_{1}$'
ax01ylabel = r'$v/v_{1}$'
ax10ylabel = r'$p/\left(\rho_{1}\,v_{1}^{2}\right)$'
ax11ylabel = r'$\alpha/\alpha_{1}$'

verbose = False

### Plotting

fig, axs = plt.subplots( nRows, nCols )

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = ['#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00']

def plot( plotfile, Rsh, Rpns, rel, verbose ):

    time, rho, dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
      = GetData( plotfile, 'PF_D'    , verbose = verbose )
    time, p  , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
      = GetData( plotfile, 'AF_P'    , verbose = verbose )
    time, v  , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
      = GetData( plotfile, 'PF_V1'   , verbose = verbose )
    time, alpha , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
      = GetData( plotfile, 'GF_Alpha', verbose = verbose )

    eta = np.copy( X1 )

    ind   = np.where( eta < 0.99 * Rsh )[0]
    ind_1 = np.where( eta > 1.00 * Rsh )[0][0]

    if( rel == 'NR' ):
        print( 'Rsh: {:}, Omega: {:}' \
               .format( Rsh, 1.0e-3 \
                               * np.abs( v[ind[-1],0,0] ) / ( Rsh - Rpns ) ) )

    p = np.copy( p[ind,0,0] \
                   / ( rho[ind_1,0,0] * ( v[ind_1,0,0] * 1.0e5 )**2 ) )

    rho = np.copy( rho[ind,0,0] / rho[ind_1,0,0] )

    v = np.copy( v[ind,0,0] / v[ind_1,0,0] )

    if( rel == 'NR' ):
        time, Phi  , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
          = GetData( plotfile, 'GF_Phi_N', verbose = verbose )
        alpha = 1.0 + Phi

    alpha = np.copy( alpha[ind,0,0] / alpha[ind_1,0,0] )

    eta = np.copy( eta[ind] )

    return eta, rho, v, p, alpha

for i in range( nRuns ):

    Mpns_s = IDs[i][4 :7 ]
    Rpns_s = IDs[i][12:15]
    Rsh_s  = IDs[i][18:  ]

    Mpns = np.float64( Mpns_s )
    Rpns = np.int64  ( Rpns_s )
    Rsh  = np.float64( Rsh_s  )

    rel = 'GR'
    plotfile = plotfileDirectory + rel + IDs[i] + '.plt00000000'
    eta, rho, v, p, alpha = plot( plotfile, Rsh, Rpns, rel, verbose )
    lab = r'$\texttt{{{:}_Rsh{:}}}$'.format( rel, Rsh_s )
    axs[0,0].plot( eta, rho  , color = color[i], ls = '-' )
    axs[0,1].plot( eta, v    , color = color[i], ls = '-' )
    axs[1,0].plot( eta, p    , color = color[i], ls = '-' )
    axs[1,1].plot( eta, alpha, color = color[i], ls = '-', label = lab )

    rel = 'NR'
    plotfile = plotfileDirectory + rel + IDs[i] + '.plt00000000'
    eta, rho, v, p, alpha = plot( plotfile, Rsh, Rpns, rel, verbose )
    lab = r'$\texttt{{{:}_Rsh{:}}}$'.format( rel, Rsh_s )
    axs[0,0].plot( eta, rho  , color = color[i], ls = '--' )
    axs[0,1].plot( eta, v    , color = color[i], ls = '--' )
    axs[1,0].plot( eta, p    , color = color[i], ls = '--' )
    axs[1,1].plot( eta, alpha, color = color[i], ls = '--', label = lab )

xlabel = r'$r \left[\mathrm{km}\right]$'

for i in range( nRows ):
    for j in range( nCols ):
        axs[i,j].set_xscale( 'log' )
        if j == nCols-1:
            axs[i,j].yaxis.set_label_position( 'right' )

top   , ltop    = True , False
left  , lleft   = True , True
bottom, lbottom = True , False
right , lright  = False, False
axs[0,0].tick_params \
  ( which = 'both', \
    top = top, left = left, bottom = bottom, right = right, \
    labeltop    = ltop, \
    labelleft   = lleft, \
    labelright  = lright, \
    labelbottom = lbottom )

top   , ltop    = True , False
left  , lleft   = False, False
bottom, lbottom = True , False
right , lright  = True , True
axs[0,1].tick_params \
  ( which = 'both', \
    top = top, left = left, bottom = bottom, right = right, \
    labeltop    = ltop, \
    labelleft   = lleft, \
    labelright  = lright, \
    labelbottom = lbottom )

top   , ltop    = True , False
left  , lleft   = True , True
bottom, lbottom = True , True
right , lright  = False, False
axs[1,0].tick_params \
  ( which = 'both', \
    top = top, left = left, bottom = bottom, right = right, \
    labeltop    = ltop, \
    labelleft   = lleft, \
    labelright  = lright, \
    labelbottom = lbottom )

top   , ltop    = True , False
left  , lleft   = False, False
bottom, lbottom = True , True
right , lright  = True , True
axs[1,1].tick_params \
  ( which = 'both', \
    top = top, left = left, bottom = bottom, right = right, \
    labeltop    = ltop, \
    labelleft   = lleft, \
    labelright  = lright, \
    labelbottom = lbottom )

for i in range( nRows ):
    for j in range( nCols ):
        axs[i,j].grid( which = 'both', axis = 'x' )
axs[0,0].set_ylabel( ax00ylabel, fontsize = 15 )
axs[0,1].set_ylabel( ax01ylabel, fontsize = 15 )
axs[1,0].set_ylabel( ax10ylabel, fontsize = 15 )
axs[1,1].set_ylabel( ax11ylabel, fontsize = 15 )
fig.supxlabel( xlabel, y = 0.02, fontsize = 15 )
axs[0,0].set_yscale( 'log' )
axs[1,0].set_yscale( 'log' )

axs[1,1].text( 0.625, 0.775, r'$\texttt{{M{:}}}$'.format( M ), \
               transform = axs[1,1].transAxes, fontsize = 14 )

axs[1,1].legend( loc = (0.43,0.10), prop = { 'size' : 10 } )

y11ticks = np.array( [ 0.90, 0.95, 1.00 ], np.float64 )

plt.subplots_adjust( wspace = 0.0, hspace = 0.0 )

#plt.savefig( saveFigAs, dpi = 300 )
#print( '\n  Saved {:}'.format( saveFigAs ) )

plt.show()

plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
