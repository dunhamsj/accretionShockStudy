#!/usr/bin/env python3

from sys import argv
import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from UtilitiesModule import GetFileArray, GetData

#### ========== User Input ==========

dataDirectory = '../plottingData_new/'

IDs = [ [ '1D_M1.4_Rpns040_Rs1.20e2', \
          '1D_M1.4_Rpns040_Rs1.50e2', \
          '1D_M1.4_Rpns040_Rs1.75e2' ], \
        [ '1D_M2.8_Rpns020_Rs6.00e1', \
          '1D_M2.8_Rpns020_Rs7.00e1' ] ]

verbose = False

plotfileDirectory = '../plottingData_new/'

c = 2.99792458e5

#### ====== End of User Input =======

# Generate data files

for i in range( len( IDs[1] ) ):
    for j in range( len( IDs[i] ) ):

        ID = IDs[i][j]

        Mpns_s = ID[4 :7 ]
        Rpns_s = ID[12:15]
        Rsh_s  = ID[18:  ]

        Mpns = np.float64( Mpns_s )
        Rpns = np.int64  ( Rpns_s )
        Rsh  = np.float64( Rsh_s  )

        # GR

        GRID = 'GR' + ID

        plotfileBaseName_GR = GRID + '.plt'

        plotfile_GR = plotfileDirectory + plotfileBaseName_GR + '00000000/'

        time, V    , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
          = GetData( plotfile_GR, 'PF_V1'   , verbose = verbose )
        time, Cs   , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
          = GetData( plotfile_GR, 'AF_Cs'   , verbose = verbose )
        time, alpha, dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
          = GetData( plotfile_GR, 'GF_Alpha', verbose = verbose )
        time, Gm11 , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
          = GetData( plotfile_GR, 'GF_Gm_11', verbose = verbose )
        time, Gm22 , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
          = GetData( plotfile_GR, 'GF_Gm_22', verbose = verbose )

        VSq = Gm11 * V**2
        lambda0_GR = alpha * V
        lambda1_GR = alpha / ( 1.0 - VSq * Cs**2 / c**4 ) \
                       * ( V * ( 1.0 - Cs**2 / c**2 ) \
                       + Cs * np.sqrt( ( 1.0 - VSq / c**2 ) \
                       * ( 1.0 / Gm11 * ( 1.0 - VSq * Cs**2 / c**4 ) \
                       - V / c * V / c * ( 1.0 - Cs**2 / c**2 ) ) ) )
        # Assume V2 = 0
        lambda2_GR = alpha / ( 1.0 - VSq * Cs**2 / c**4 ) \
                       * Cs * np.sqrt( ( 1.0 - VSq / c**2 ) \
                       * 1.0 / Gm22 * ( 1.0 - VSq * Cs**2 / c**4 ) )
        lambda0_GR = np.copy( ( lambda0_GR * np.sqrt( Gm11 ) )[:,0,0] )
        lambda1_GR = np.copy( ( lambda1_GR * np.sqrt( Gm11 ) )[:,0,0] )
        lambda2_GR = np.copy( ( lambda2_GR * np.sqrt( Gm22 ) )[:,0,0] )

        # NR

        NRID = 'NR' + ID

        plotfileBaseName_NR = NRID + '.plt'

        plotfile_NR = plotfileDirectory + plotfileBaseName_NR + '00000000/'

        time, V   , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
          = GetData( plotfile_NR, 'PF_V1'   , verbose = verbose )
        time, Cs  , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
          = GetData( plotfile_NR, 'AF_Cs'   , verbose = verbose )
        time, Gm11, dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
          = GetData( plotfile_NR, 'GF_Gm_11', verbose = verbose )
        time, Gm22, dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
          = GetData( plotfile_NR, 'GF_Gm_22', verbose = verbose )

        lambda0_NR = V
        lambda1_NR = V + Cs * np.sqrt( 1.0 / Gm11 )
        # Assume V2 = 0
        lambda2_NR = Cs * np.sqrt( 1.0 / Gm22 )
        lambda0_NR = np.copy( ( lambda0_NR * np.sqrt( Gm11 ) )[:,0,0] )
        lambda1_NR = np.copy( ( lambda1_NR * np.sqrt( Gm11 ) )[:,0,0] )
        lambda2_NR = np.copy( ( lambda2_NR * np.sqrt( Gm22 ) )[:,0,0] )

        ind = np.where( ( X1 < Rsh ) & ( X1 > Rpns ) )[0]

        X1         = np.copy( X1        [ind] )
        lambda0_GR = np.copy( lambda0_GR[ind] )
        lambda1_GR = np.copy( lambda1_GR[ind] )
        lambda2_GR = np.copy( lambda2_GR[ind] )
        lambda0_NR = np.copy( lambda0_NR[ind] )
        lambda1_NR = np.copy( lambda1_NR[ind] )
        lambda2_NR = np.copy( lambda2_NR[ind] )

        signalSpeeds = np.vstack( ( X1, lambda0_NR, lambda0_GR, \
                                        lambda1_NR, lambda1_GR, \
                                        lambda2_NR, lambda2_GR ) )

        header = 'Generated from compareIC_postShockSpeeds.py\n'
        header += '{:} X1_C, lambda0_NR, lambda0_GR, lambda1_NR, lambda1_GR, ' \
                  .format( ID ) + 'lambda2_NR, lambda2_GR'

        fileName = dataDirectory + '{:}_signalSpeeds.dat'.format( ID )

        np.savetxt( fileName, signalSpeeds, header = header )

### Plotting

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = [ '#377eb8', '#ff7f00', '#4daf4a', \
          '#f781bf', '#a65628', '#984ea3', \
          '#999999', '#e41a1c', '#dede00' ]

# Ratio of signal-speeds

fig, axs = plt.subplots( 2, 1, figsize = (8,4) )

handles = []
labelLC = []
labelHC = []

for i in range( len( IDs[1] ) ):
    for j in range( len( IDs[i] ) ):

        ID = IDs[i][j]

        Mpns_s = ID[4 :7 ]
        Rpns_s = ID[12:15]
        Rsh_s  = ID[18:  ]

        Mpns = np.float64( Mpns_s )
        Rpns = np.int64  ( Rpns_s )
        Rsh  = np.float64( Rsh_s  )

        fileName = dataDirectory + '{:}_signalSpeeds.dat'.format( ID )

        X1, lambda0_NR, lambda0_GR, lambda1_NR, lambda1_GR, \
        lambda2_NR, lambda2_GR \
          = np.loadtxt( fileName )

        eta = ( X1 - Rpns ) / ( Rsh - Rpns )

        ind = np.where( ( eta > 0.0 ) & ( eta < 1.0 ) )[0]

        eta        = eta       [ind]
        lambda0_GR = lambda0_GR[ind]
        lambda0_NR = lambda0_NR[ind]
        lambda1_GR = lambda1_GR[ind]
        lambda1_NR = lambda1_NR[ind]
        lambda2_GR = lambda2_GR[ind]
        lambda2_NR = lambda2_NR[ind]

        l1, \
          = axs[i].plot( eta, lambda1_GR / lambda1_NR, \
                         c = color[j], ls = '-'  )
        l2, \
          = axs[i].plot( eta, lambda2_GR / lambda2_NR, \
                         c = color[j], ls = '--' )
        l3, \
          = axs[i].plot( eta, lambda0_GR / lambda0_NR, \
                         c = color[j], ls = ':'  )

        handles.append( [ l1, l2, l3 ] )

        lab = ID.replace( 'Rs', 'Rsh' )
        if i == 0:
            labelLC.append( r'$\texttt{{{:}}}$'.format( lab ) )
        else:
            labelHC.append( r'$\texttt{{{:}}}$'.format( lab ) )

    axs[i].grid()
    axs[i].set_xlim( -0.1, 1.1 )

handles = np.array( handles )

label1p = r'$\lambda^{r,\mathrm{GR}}_{+}/\lambda^{r,\mathrm{NR}}_{+}$'
label2p = r'$\lambda^{\theta,\mathrm{GR}}_{+}/\lambda^{\theta,\mathrm{NR}}_{+}$'
label0  = r'$\lambda^{r,\mathrm{GR}}_{0}/\lambda^{r,\mathrm{NR}}_{0}$'

label1 = [ label1p, label2p, label0 ]

legend1 = axs[0].legend( handles[0]    , label1 , loc = 8 )
legend2 = axs[0].legend( handles[0:3,0], labelLC, loc = 4 )
legend3 = axs[1].legend( handles[3:,0] , labelHC, loc = 4 )

axs[-1].set_xlabel( r'$\eta$', fontsize = 15 )
axs[0].add_artist( legend1 )
axs[0].add_artist( legend2 )
axs[1].add_artist( legend3 )

plt.subplots_adjust( hspace = 0.0 )

axs[0].tick_params \
      ( which = 'both', \
        top = True, left = True, bottom = True, right = True, \
        labeltop    = False, \
        labelleft   = True, \
        labelright  = False, \
        labelbottom = False )
axs[1].tick_params \
      ( which = 'both', \
        top = True, left = True, bottom = True, right = True, \
        labeltop    = False, \
        labelleft   = True, \
        labelright  = False, \
        labelbottom = True )

plt.show()

#figName = '/home/kkadoogan/Work/accretionShockPaper/Figures/fig.SignalSpeedRatios.pdf'
#plt.savefig( figName, dpi = 300 )
#print( '\n  Saved {:}'.format( figName ) )

import os
os.system( 'rm -rf __pycache__ ' )
