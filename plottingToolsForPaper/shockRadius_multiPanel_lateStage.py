#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = ['#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00']

rel    = [ 'NR', 'GR' ]
M      = [ '2.8' ]
Mdot   = [ '0.3' ]
Rs     = [ '6.00e1', '7.50e1', '9.00e1' ]
suffix = '_RPNS2.00e1'

fig, axs = plt.subplots( 1, 3, figsize = (8,2) )

for m in range( len( M ) ):
    for mdot in range( len( Mdot ) ):
        for rs in range( len( Rs ) ):

            ID_NR = '{:}2D_M{:}_Mdot{:}_Rs{:}{:}' \
                    .format( rel[0], M[m], Mdot[mdot], Rs[rs], suffix )
            ID_GR = '{:}2D_M{:}_Mdot{:}_Rs{:}{:}' \
                    .format( rel[1], M[m], Mdot[mdot], Rs[rs], suffix )

            dataFileName_NR \
              = '../plottingData/{:}_ShockRadiusVsTime.dat'.format( ID_NR )
            dataFileName_GR \
              = '../plottingData/{:}_ShockRadiusVsTime.dat'.format( ID_GR )

            Time_NR, RsAve_NR, RsMin_NR, RsMax_NR \
              = np.loadtxt( dataFileName_NR )
            Time_GR, RsAve_GR, RsMin_GR, RsMax_GR \
              = np.loadtxt( dataFileName_GR )

            dr_NR = ( RsAve_NR - RsAve_NR[0] ) / RsAve_NR[0]
            dr_GR = ( RsAve_GR - RsAve_GR[0] ) / RsAve_GR[0]

            ind_NR = np.where( dr_NR > 0.1 )[0]
            if( np.size( ind_NR ) == 0 ):
                ind_NR = np.argmax( Time_NR )
                ind_NR = np.linspace( 0, ind_NR, ind_NR+1, dtype = np.int64 )
            else:
                ind_NR = np.linspace( 0, ind_NR[0]-1, ind_NR[0], \
                                      dtype = np.int64 )

            ind_GR = np.where( dr_GR > 0.1 )[0]
            if( np.size( ind_GR ) == 0 ):
                ind_GR = np.argmax( Time_GR )
                ind_GR = np.linspace( 0, ind_GR, ind_GR+1, dtype = np.int64 )
            else:
                ind_GR = np.linspace( 0, ind_GR[0]-1, ind_GR[0], \
                                      dtype = np.int64 )

            print( Time_NR[ind_NR][-1] )
            print( Time_GR[ind_GR][-1] )

            axs[rs].plot( Time_NR[ind_NR], dr_NR[ind_NR], \
                          color = color[0], label = 'NR' )
            axs[rs].plot( Time_GR[ind_GR], dr_GR[ind_GR], \
                          color = color[1], label = 'GR' )

            label = r'$\texttt{{M{:}_Rs{:}}}$'.format( M[m], Rs[rs] )
            axs[rs].set_title( label, fontsize = 12 )

            axs[rs].grid()
            axs[rs].set_xlim( 0.0, 100.0 )

            axs[rs].tick_params \
              ( top = True, left = True, right = True, bottom = True )

fig.supxlabel( r'$t\ \left[\mathrm{ms}\right]$', y = -0.1, fontsize = 15 )
fig.supylabel \
( r'$\left(\left<R_{s}\right>\left(t\right)-R_{s}\left(0\right)\right)$' \
    + r'$/R_{s}\left(0\right)$', x = 0.05, fontsize = 11 )

axs[0].legend( loc = 2 )
plt.subplots_adjust( wspace = 0.3, hspace = 0.0 )
plt.show()
#plt.savefig( '../Figures/fig.ShockRadiusVsTime_LateStage.pdf', dpi = 300 )
plt.close()
