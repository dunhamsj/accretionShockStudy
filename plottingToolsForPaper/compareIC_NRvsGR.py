#!/usr/bin/env python3

from sys import argv
import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from UtilitiesModule import GetFileArray, GetData

#### ========== User Input ==========

rootDirectory_NR = '../plottingData/'
rootDirectory_GR = '../plottingData/'

Mpns_s = argv[1]
Mpns = np.float64( Mpns_s )

if  ( Mpns == 1.4 ):
    Rsh = np.array( [   '1.20e2',   '1.50e2',   '1.75e2' ], str )
    lab = np.array( [ 'Rs1.20e2', 'Rs1.50e2', 'Rs1.75e2' ], str )
elif( Mpns == 2.8 ):
    Rsh = np.array( [   '6.00e1',   '7.00e1' ], str )
    lab = np.array( [ 'Rs6.00e1', 'Rs7.00e1' ], str )

IDs = [ '1D_M{:.1f}_Rpns003_Rs{:}'.format( Mpns, r ) for r in Rsh ]

IDs = np.array( IDs, dtype = str )
Rsh = np.array( np.float64( Rsh ), dtype = np.int64 )

nRows = 2
nCols = 2

ax00ylabel = r'$\rho/\rho_{1}$'
ax01ylabel = r'$v/v_{1}$'
ax10ylabel = r'$p/\left(\rho_{1}\,v_{1}^{2}\right)$'
ax11ylabel = r'$\alpha/\alpha_{1}$'

saveFigAs = '../Figures/fig.CompareNRvsGR_SS_M{:.1f}.pdf'.format( Mpns )

verbose = False

#### ====== End of User Input =======

G_MKS = 6.673e-11
c_m   = 2.99792458e8
c_cm  = 2.99792458e10

### Plotting

fig, axs = plt.subplots( nRows, nCols )

plotFileDirectory_GR = rootDirectory_GR
plotFileDirectory_NR = rootDirectory_NR

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = ['#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00']

i = -1
for r in range( Rsh.shape[0] ):

    plotFileBaseName_GR = 'GR' + IDs[r] + '.plt'
    plotFileBaseName_NR = 'NR' + IDs[r] + '.plt'

    plotFileArray_GR \
      = GetFileArray( plotFileDirectory_GR, plotFileBaseName_GR )
    plotFileArray_NR \
      = GetFileArray( plotFileDirectory_NR, plotFileBaseName_NR )

    plotFile_GR = plotFileDirectory_GR + plotFileArray_GR[-1]
    plotFile_NR = plotFileDirectory_NR + plotFileArray_NR[-1]

    time, rho_GR, dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
      = GetData( plotFile_GR, 'PF_D' , verbose = verbose )
    time, rho_NR, dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
      = GetData( plotFile_NR, 'PF_D' , verbose = verbose )
    time, p_GR  , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
      = GetData( plotFile_GR, 'AF_P' , verbose = verbose )
    time, p_NR  , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
      = GetData( plotFile_NR, 'AF_P' , verbose = verbose )
    time, v_GR  , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
      = GetData( plotFile_GR, 'PF_V1', verbose = verbose )
    time, v_NR  , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
      = GetData( plotFile_NR, 'PF_V1', verbose = verbose )
    time, alpha , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
      = GetData( plotFile_GR, 'GF_Alpha', verbose = verbose )
    time, Phi   , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
      = GetData( plotFile_NR, 'GF_Phi_N', verbose = verbose )

    etaGR = np.copy( X1 )
    etaNR = np.copy( X1 )

    indGR   = np.where( etaGR < 0.99 * Rsh[r] )[0]
    indGR_1 = np.where( etaGR > 1.00 * Rsh[r] )[0][0]

    indNR   = np.where( etaNR < 0.99 * Rsh[r] )[0]
    indNR_1 = np.where( etaNR > 1.00 * Rsh[r] )[0][0]

    v = np.copy( v_GR[indGR,0,0] )
    if   Mpns_s == '1.4':
        Rpns = 4.0e1
    elif Mpns_s == '2.8':
        Rpns = 2.0e1
    print( 'Rs: {:}, Omega: {:}'.format( Rsh[r], 1.0e-3 * np.abs( v[-1] ) / ( Rsh[r] - Rpns ) ) )

    p_GR \
      = np.copy \
          ( p_GR[indGR  ,0,0] \
              / ( rho_GR[indGR_1,0,0] * ( v_GR[indGR_1,0,0] * 1.0e5 )**2 ) )

    p_NR \
      = np.copy \
          ( p_NR[indNR  ,0,0] \
              / ( rho_NR[indNR_1,0,0] * ( v_NR[indNR_1,0,0] * 1.0e5 )**2 ) )

    rho_GR = np.copy( rho_GR[indGR,0,0] / rho_GR[indGR_1,0,0] )
    rho_NR = np.copy( rho_NR[indNR,0,0] / rho_NR[indNR_1,0,0] )

    v_GR = np.copy( v_GR[indGR,0,0] / v_GR[indGR_1,0,0] )
    v_NR = np.copy( v_NR[indNR,0,0] / v_NR[indNR_1,0,0] )

    alpha_N = 1.0 + Phi
    alpha_GR = np.copy( alpha  [indGR,0,0] / alpha  [indGR_1,0,0] )
    alpha_NR = np.copy( alpha_N[indNR,0,0] / alpha_N[indNR_1,0,0] )

    etaGR = np.copy( etaGR[indGR] )
    etaNR = np.copy( etaNR[indNR] )

    i += 1

    axs[0,0].plot( etaGR, rho_GR, color = color[i], ls = '-' )
    axs[0,0].plot( etaNR, rho_NR, color = color[i], ls = '--' )

    axs[0,1].plot( etaGR, v_GR, color = color[i], ls = '-' )
    axs[0,1].plot( etaNR, v_NR, color = color[i], ls = '--' )

    axs[1,0].plot( etaGR, p_GR  , color = color[i], ls = '-' )
    axs[1,0].plot( etaNR, p_NR  , color = color[i], ls = '--' )

    axs[1,1].plot( etaGR, alpha_GR, color = color[i], ls = '-', \
             label = r'$\texttt{{GR_{:}}}$'.format( lab[r] ) )
    axs[1,1].plot( etaNR, alpha_NR, color = color[i], ls = '--', \
             label = r'$\texttt{{NR_{:}}}$'.format( lab[r] ) )

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

#import matplotlib.lines as mlines
#NR = mlines.Line2D( [], [], color = 'black', ls = '--', label = 'NR' )
#GR = mlines.Line2D( [], [], color = 'black', ls = '-' , label = 'GR' )
#axs[0,0].legend( handles = [ NR, GR ] )

axs[1,1].text( 0.625, 0.775, r'$\texttt{{M{:.1f}}}$'.format( Mpns ), \
               transform = axs[1,1].transAxes, fontsize = 14 )

axs[1,1].legend( loc = (0.45,0.10), prop = { 'size' : 10 } )

y11ticks = np.array( [ 0.90, 0.95, 1.00 ], np.float64 )

plt.subplots_adjust( wspace = 0.0, hspace = 0.0 )

plt.savefig( saveFigAs, dpi = 300 )
#plt.show()

plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
