#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from globalVariables import *

IDs = [ '1D_M1.4_Rpns003_Rs1.20e2', \
        '1D_M1.4_Rpns003_Rs1.50e2', \
        '1D_M1.4_Rpns003_Rs1.75e2', \
        '1D_M1.8_Rpns003_Rs7.00e1', \
        '1D_M2.8_Rpns003_Rs6.00e1', \
        '1D_M2.8_Rpns003_Rs7.00e1' ]

nRows = 2
nCols = 2

ax00ylabel = r'$\rho/\rho_{1}$'
ax01ylabel = r'$v/v_{1}$'
ax10ylabel = r'$p/\left(\rho_{1}\,v_{1}^{2}\right)$'
ax11ylabel = r'$\alpha/\alpha_{1}$'

xlabel = r'$r \left[\mathrm{km}\right]$'

def plotData( fig, axs, IDs ):

    for i in range( len( IDs ) ):

        M   = IDs[i][4:7]
        Rsh = IDs[i][-6:]

        plotFileBaseName_GR = 'GR' + IDs[i] + '.plt'
        plotFileBaseName_NR = 'NR' + IDs[i] + '.plt'

        filename \
          = dataDirectory + '{:}_PF_D.dat'.format( plotFileBaseName_GR[:-4] )
        X1, rho_GR = np.loadtxt( filename )
        filename \
          = dataDirectory + '{:}_PF_D.dat'.format( plotFileBaseName_NR[:-4] )
        X1, rho_NR = np.loadtxt( filename )

        filename \
          = dataDirectory + '{:}_AF_P.dat'.format( plotFileBaseName_GR[:-4] )
        X1, p_GR = np.loadtxt( filename )
        filename \
          = dataDirectory + '{:}_AF_P.dat'.format( plotFileBaseName_NR[:-4] )
        X1, p_NR = np.loadtxt( filename )

        filename \
          = dataDirectory + '{:}_PF_V1.dat'.format( plotFileBaseName_GR[:-4] )
        X1, v_GR = np.loadtxt( filename )
        filename \
          = dataDirectory + '{:}_PF_V1.dat'.format( plotFileBaseName_NR[:-4] )
        X1, v_NR = np.loadtxt( filename )

        filename \
          = dataDirectory + '{:}_GF_Alpha.dat'.format( plotFileBaseName_GR[:-4] )
        X1, alpha = np.loadtxt( filename )
        filename \
          = dataDirectory + '{:}_GF_Phi_N.dat'.format( plotFileBaseName_NR[:-4] )
        X1, Phi = np.loadtxt( filename )

        etaGR = np.copy( X1 )
        etaNR = np.copy( X1 )

        indGR   = np.where( etaGR < 0.99 * np.float64( Rsh ) )[0]
        indGR_1 = np.where( etaGR > 1.00 * np.float64( Rsh ) )[0][0]

        indNR   = np.where( etaNR < 0.99 * np.float64( Rsh ) )[0]
        indNR_1 = np.where( etaNR > 1.00 * np.float64( Rsh ) )[0][0]

        p_GR \
          = np.copy \
              ( p_GR[indGR] \
                  / ( rho_GR[indGR_1] * ( v_GR[indGR_1] * 1.0e5 )**2 ) )

        p_NR \
          = np.copy \
              ( p_NR[indNR] \
                  / ( rho_NR[indNR_1] * ( v_NR[indNR_1] * 1.0e5 )**2 ) )

        rho_GR = np.copy( rho_GR[indGR] / rho_GR[indGR_1] )
        rho_NR = np.copy( rho_NR[indNR] / rho_NR[indNR_1] )

        v_GR = np.copy( v_GR[indGR] / v_GR[indGR_1] )
        v_NR = np.copy( v_NR[indNR] / v_NR[indNR_1] )

        alpha_N = 1.0 + Phi / ( 2.99792458e10 )**2
        alpha_GR = np.copy( alpha  [indGR] / alpha  [indGR_1] )
        alpha_NR = np.copy( alpha_N[indNR] / alpha_N[indNR_1] )

        etaGR = np.copy( etaGR[indGR] )
        etaNR = np.copy( etaNR[indNR] )

        axs[0,0].plot( etaGR, rho_GR, color = color[i], ls = '-' )
        axs[0,0].plot( etaNR, rho_NR, color = color[i], ls = '--' )

        axs[0,1].plot( etaGR, v_GR, color = color[i], ls = '-' )
        axs[0,1].plot( etaNR, v_NR, color = color[i], ls = '--' )

        axs[1,0].plot( etaGR, p_GR  , color = color[i], ls = '-' )
        axs[1,0].plot( etaNR, p_NR  , color = color[i], ls = '--' )

        lab = 'M{:}_Rsh{:}'.format( M, Rsh )

        axs[1,1].plot( etaGR, alpha_GR, color = color[i], ls = '-', \
                 label = r'$\texttt{{GR_{:}}}$'.format( lab ) )
        axs[1,1].plot( etaNR, alpha_NR, color = color[i], ls = '--', \
                 label = r'$\texttt{{NR_{:}}}$'.format( lab ) )

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

    axs[1,1].legend( loc = (0.35,0.05), prop = { 'size' : 9 } )

    y11ticks = np.array( [ 0.90, 0.95, 1.00 ], np.float64 )

    plt.subplots_adjust( wspace = 0.0, hspace = 0.0 )

    #plt.show()

    if M == '1.4':
        suffix = 'loXi'
    else:
        suffix = 'hiXi'
    figName = figuresDirectory + 'fig.CompareNRvsGR_SS_{:}.pdf'.format( suffix )
    plt.savefig( figName, dpi = 300, bbox_inches = 'tight' )
    print( '\n  Saved {:}'.format( figName ) )

    plt.close()

fig0, axs0 = plt.subplots( nRows, nCols )
plotData( fig0, axs0, IDs[0:3] )

fig1, axs1 = plt.subplots( nRows, nCols )
plotData( fig1, axs1, IDs[3:] )

import os
os.system( 'rm -rf __pycache__ ' )
