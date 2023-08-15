#!/usr/bin/env python3

from sys import argv
import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from UtilitiesModule import GetFileArray, GetData

#### ========== User Input ==========

Rpns = [ '040', '020' ]
M    = [ '1.4', '2.8' ]
Rs   = [ [ '1.20e2', '1.50e2', '1.75e2' ], \
         [ '6.00e1', '7.00e1' ] ]

verbose = False

plotfileDirectory = '../plottingData/'

c = 2.99792458e5

#### ====== End of User Input =======

# Generate data files

#for m in range( len( M ) ):
#    if m == 0: rpns = 0
#    if m == 1: rpns = 1
#    for rs in range( len( Rs[m] ) ):
#
#        ID = '1D_M{:}_Rpns{:}_Rs{:}'.format( M[m], Rpns[rpns], Rs[m][rs] )
#
#        # GR
#
#        GRID = 'GR' + ID
#
#        plotfileBaseName_GR = GRID + '.plt'
#
#        plotfile_GR = plotfileDirectory + plotfileBaseName_GR + '00000000/'
#
#        time, V    , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
#          = GetData( plotfile_GR, 'PF_V1'   , verbose = verbose )
#        time, Cs   , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
#          = GetData( plotfile_GR, 'AF_Cs'   , verbose = verbose )
#        time, alpha, dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
#          = GetData( plotfile_GR, 'GF_Alpha', verbose = verbose )
#        time, Gm11 , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
#          = GetData( plotfile_GR, 'GF_Gm_11', verbose = verbose )
#        time, Gm22 , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
#          = GetData( plotfile_GR, 'GF_Gm_22', verbose = verbose )
#
#        VSq = Gm11 * V**2
#        lambda0_GR = alpha * V
#        lambda1_GR = alpha / ( 1.0 - VSq * Cs**2 / c**4 ) \
#                       * ( V * ( 1.0 - Cs**2 / c**2 ) \
#                       + Cs * np.sqrt( ( 1.0 - VSq / c**2 ) \
#                       * ( 1.0 / Gm11 * ( 1.0 - VSq * Cs**2 / c**4 ) \
#                       - V / c * V / c * ( 1.0 - Cs**2 / c**2 ) ) ) )
#        # Assume V2 = 0
#        lambda2_GR = alpha / ( 1.0 - VSq * Cs**2 / c**4 ) \
#                       * Cs * np.sqrt( ( 1.0 - VSq / c**2 ) \
#                       * 1.0 / Gm22 * ( 1.0 - VSq * Cs**2 / c**4 ) )
#        lambda0_GR = np.copy( ( lambda0_GR * np.sqrt( Gm11 ) )[:,0,0] )
#        lambda1_GR = np.copy( ( lambda1_GR * np.sqrt( Gm11 ) )[:,0,0] )
#        lambda2_GR = np.copy( ( lambda2_GR * np.sqrt( Gm22 ) )[:,0,0] )
#
#        # NR
#
#        NRID = 'NR' + ID
#
#        plotfileBaseName_NR = NRID + '.plt'
#
#        plotfile_NR = plotfileDirectory + plotfileBaseName_NR + '00000000/'
#
#        time, V   , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
#          = GetData( plotfile_NR, 'PF_V1'   , verbose = verbose )
#        time, Cs  , dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
#          = GetData( plotfile_NR, 'AF_Cs'   , verbose = verbose )
#        time, Gm11, dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
#          = GetData( plotfile_NR, 'GF_Gm_11', verbose = verbose )
#        time, Gm22, dataUnits, X1, X2, X3, dX1, dX2, dX3, nX \
#          = GetData( plotfile_NR, 'GF_Gm_22', verbose = verbose )
#
#        lambda0_NR = V
#        lambda1_NR = V + Cs * np.sqrt( 1.0 / Gm11 )
#        # Assume V2 = 0
#        lambda2_NR = Cs * np.sqrt( 1.0 / Gm22 )
#        lambda0_NR = np.copy( ( lambda0_NR * np.sqrt( Gm11 ) )[:,0,0] )
#        lambda1_NR = np.copy( ( lambda1_NR * np.sqrt( Gm11 ) )[:,0,0] )
#        lambda2_NR = np.copy( ( lambda2_NR * np.sqrt( Gm22 ) )[:,0,0] )
#
#        rsh = np.float64( Rs[m][rs] )
#        rsh = np.float64( Rs[m][rs] )
#        rpnss = np.float64( Rpns[rpns] )
#        ind = np.where( ( X1 < rsh ) & ( X1 > rpnss ) )[0]
#
#        X1         = np.copy( X1        [ind] )
#        lambda0_GR = np.copy( lambda0_GR[ind] )
#        lambda1_GR = np.copy( lambda1_GR[ind] )
#        lambda2_GR = np.copy( lambda2_GR[ind] )
#        lambda0_NR = np.copy( lambda0_NR[ind] )
#        lambda1_NR = np.copy( lambda1_NR[ind] )
#        lambda2_NR = np.copy( lambda2_NR[ind] )
#
#        signalSpeeds = np.vstack( ( X1, lambda0_NR, lambda0_GR, \
#                                        lambda1_NR, lambda1_GR, \
#                                        lambda2_NR, lambda2_GR ) )
#
#        header = '{:} X1_C, lambda0_NR, lambda0_GR, lambda1_NR, lambda1_GR, ' \
#                 .format( ID ) + 'lambda2_NR, lambda2_GR'
#
#        fileName = '../plottingData/{:}_signalSpeeds.dat'.format( ID )
#
#        np.savetxt( fileName, signalSpeeds, header = header )

### Plotting

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = ['#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00']

# Ratio of signal-speeds

#color = [ 'k' for i in range( len( color ) ) ]
fig, axs = plt.subplots( 2, 1, figsize = (8,4) )

handles = []
labelLC = []
labelHC = []
for m in range( len( M ) ):
    if m == 0: rpns = 0
    if m == 1: rpns = 1
    i = -1
    for rs in range( len( Rs[m] ) ):

        i += 1
        ID = '1D_M{:}_Rpns{:}_Rs{:}'.format( M[m], Rpns[rpns], Rs[m][rs] )

        fileName = '../plottingData/{:}_signalSpeeds.dat'.format( ID )

        X1, lambda0_NR, lambda0_GR, lambda1_NR, lambda1_GR, \
        lambda2_NR, lambda2_GR \
          = np.loadtxt( fileName )

        rsh   = np.float64( Rs[m][rs] )
        rpnss = np.float64( Rpns[rpns] )

        eta = ( X1 - rpnss ) / ( rsh - rpnss )

        ind = np.where( ( eta > 0.0 ) & ( eta < 1.0 ) )[0]

        eta        = eta       [ind]
        lambda0_GR = lambda0_GR[ind]
        lambda0_NR = lambda0_NR[ind]
        lambda1_GR = lambda1_GR[ind]
        lambda1_NR = lambda1_NR[ind]
        lambda2_GR = lambda2_GR[ind]
        lambda2_NR = lambda2_NR[ind]

        l1, \
          = axs[m].plot( eta, lambda1_GR / lambda1_NR, \
                         c = color[i], ls = '-'  )
        l2, \
          = axs[m].plot( eta, lambda2_GR / lambda2_NR, \
                         c = color[i], ls = '--' )
        l3, \
          = axs[m].plot( eta, lambda0_GR / lambda0_NR, \
                         c = color[i], ls = ':'  )

        handles.append( [ l1, l2, l3 ] )

        lab = ID.replace( 'Rs', 'Rsh' )
        if m == 0:
            labelLC.append( r'$\texttt{{{:}}}$'.format( lab ) )
        else:
            labelHC.append( r'$\texttt{{{:}}}$'.format( lab ) )

    axs[m].grid()
    axs[m].set_xlim( -0.1, 1.1 )

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

#plt.show()

#figName = 'fig.SignalSpeedRatios.png'
figName = '/home/kkadoogan/Work/accretionShockPaper/Figures/fig.SignalSpeedRatios.pdf'

plt.savefig( figName, dpi = 300 )
print( '\n  Saved {:}'.format( figName ) )

import os
os.system( 'rm -rf __pycache__ ' )
