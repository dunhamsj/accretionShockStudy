#!/usr/bin/env python3

from os.path import isfile
import numpy as np

from globalVariables import *

IDs = [ 'M1.4_Rpns070_Rs1.50e2', \
        'M1.4_Rpns040_Rs1.20e2', \
        'M1.4_Rpns040_Rs1.50e2', \
        'M1.4_Rpns040_Rs1.75e2', \
        'M1.8_Rpns020_Rs7.00e1', \
        'M2.8_Rpns020_Rs6.00e1', \
        'M2.8_Rpns020_Rs7.00e1' ]

#R_ac_NR = [ [ 87.45, 122.25, 152.25 ], [ 43.95, 55.45 ] ]
#R_ac_GR = [ [ 93.55, 130.65, 162.55 ], [ 57.65, 69.95 ] ]

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

Models = {}
with open( dataDirectory + 'fft.dat' ) as f:
    i = -1
    for line in f:
       i += 1
       if i < 2: continue
       x = line.split()
       Models[x[0]] = [ np.float64( x[1] ), np.float64( x[2] ) ]

table = \
'\
\\begin{deluxetable}{cccccc}[ht]\n\
  \\tablecaption{Results}\n\
  \\tablehead %\n\
  { %\n\
  \\colhead{Model}                                          &\n\
  \\colhead{$T\\pm\\Delta T\\,\\left[\\ms\\right]$}               &\n\
  \\colhead{$\\omega\\pm\\Delta\\omega\\,\\left[\\ms^{-1}\\right]$} &\n\
  \\colhead{$\\omega\,T$}                                    &\n\
  \\colhead{$\\taa\\,\\left[\\ms\\right]$}                       &\n\
  \\colhead{$\\tac\\,\\left[\\ms\\right]$}                       %\n\
  }\n\
  \\startdata\n\
'

GrowthRateRatioGRoverNRxi04 = +np.inf
GrowthRateRatioGRoverNRxi07 = +np.inf
GrowthRateRatioGRoverNRxi18 = +np.inf
GrowthRateRatioGRoverNRxi28 = +np.inf
PeriodRatioGRoverNRxi04     = -np.inf
PeriodRatioGRoverNRxi07     = -np.inf
PeriodRatioGRoverNRxi18     = -np.inf
PeriodRatioGRoverNRxi28     = -np.inf
RelDiffAAxi04               = -np.inf
RelDiffAAxi07               = -np.inf
RelDiffAAxi18               = -np.inf
RelDiffAAxi28               = -np.inf
RelDiffACxi04               = -np.inf
RelDiffACxi07               = -np.inf
RelDiffACxi18               = -np.inf
RelDiffACxi28               = -np.inf

omegaT_xi04 = []
omegaT_xi07 = []
omegaT_xi18 = []
omegaT_xi28 = []

for i in range( len( IDs ) ):

        ID = IDs[i]

        dataFileName_NR \
          = dataDirectory + 'LegendrePowerSpectrum_NR2D_{:}.dat'.format( ID )

        dataFileName_GR \
          = dataDirectory + 'LegendrePowerSpectrum_GR2D_{:}.dat'.format( ID )

        if not isfile( dataFileName_NR ):
            print( 'File {:} not found. Skipping'.format( dataFileName_NR ) )
            continue

        if not isfile( dataFileName_GR ):
            print( 'File {:} not found. Skipping'.format( dataFileName_GR ) )
            continue

        # NR

        f = open( dataFileName_NR )
        dum = f.readline()
        s = f.readline(); ind = s.find( '#' )+1
        tmp \
          = np.array( list( map( np.float64, s[ind:].split() ) ), \
                      np.float64 )
        omegaR_NR = tmp[3]
        omegaI_NR = tmp[4]
        dum = f.readline()
        s = f.readline(); ind = s.find( '#' )+1
        tmp \
          = np.array( list( map( np.float64, s[ind:].split() ) ), \
                      np.float64 )
        dOmegaR_NR = tmp[1]
        dOmegaI_NR = tmp[2]
        f.close()

        TNR, dT_NR = Models['NR2D_'+ID]
        G_NR  = omegaR_NR
        dG_NR = dOmegaR_NR

        wT_NR = omegaR_NR * TNR

        T_aa_NR = T_aa['NR1D_'+ID]
        T_ac_NR = T_ac['NR1D_'+ID]

        # GR

        f = open( dataFileName_GR )
        dum = f.readline()
        s = f.readline(); ind = s.find( '#' )+1
        tmp \
          = np.array( list( map( np.float64, s[ind:].split() ) ), \
                      np.float64 )
        omegaR_GR = tmp[3]
        omegaI_GR = tmp[4]
        dum = f.readline()
        s = f.readline(); ind = s.find( '#' )+1
        tmp \
          = np.array( list( map( np.float64, s[ind:].split() ) ), \
                      np.float64 )
        dOmegaR_GR = tmp[1]
        dOmegaI_GR = tmp[2]
        f.close()

        TGR, dT_GR = Models['GR2D_'+ID]
        G_GR  = omegaR_GR
        dG_GR = dOmegaR_GR

        wT_GR = omegaR_GR * TGR

        T_aa_GR = T_aa['GR1D_'+ID]
        T_ac_GR = T_ac['GR1D_'+ID]

        M_s    = ID[1:4]
        M      = np.float64( M_s )
        rsh_s  = ID[15:21]
        rsh    = np.float64( rsh_s )
        rpns_s = ID[9:12]
        rpns   = np.int64  ( rpns_s )

        xi = '{:.1f}'.format( M / ( rpns / 20.0 ) )

        if xi == '0.4':

            GrowthRateRatioGRoverNRxi04 \
              = min( GrowthRateRatioGRoverNRxi04, G_GR / G_NR )

            PeriodRatioGRoverNRxi04 = max( PeriodRatioGRoverNRxi04, TGR / TNR )

            RelDiffAAxi04     \
              = max( RelDiffAAxi04, \
                     abs( TGR - T_aa_GR ) / ( 0.5 * ( TGR + T_aa_GR ) ) )

            RelDiffACxi04     \
              = max( RelDiffACxi04, \
                     abs( TGR - T_ac_GR ) / ( 0.5 * ( TGR + T_ac_GR ) ) )

            omegaT_xi04.append( wT_NR )
            omegaT_xi04.append( wT_GR )

        if xi == '0.7':

            GrowthRateRatioGRoverNRxi07 \
              = min( GrowthRateRatioGRoverNRxi07, G_GR / G_NR )

            PeriodRatioGRoverNRxi07 = max( PeriodRatioGRoverNRxi07, TGR / TNR )

            RelDiffAAxi07     \
              = max( RelDiffAAxi07, \
                     abs( TGR - T_aa_GR ) / ( 0.5 * ( TGR + T_aa_GR ) ) )

            RelDiffACxi07     \
              = max( RelDiffACxi07, \
                     abs( TGR - T_ac_GR ) / ( 0.5 * ( TGR + T_ac_GR ) ) )

            omegaT_xi07.append( wT_NR )
            omegaT_xi07.append( wT_GR )

        if xi == '1.8':

            GrowthRateRatioGRoverNRxi18 \
              = min( GrowthRateRatioGRoverNRxi18, G_GR / G_NR )

            PeriodRatioGRoverNRxi18 = max( PeriodRatioGRoverNRxi18, TGR / TNR )

            RelDiffAAxi18     \
              = max( RelDiffAAxi18, \
                     abs( TGR - T_aa_GR ) / ( 0.5 * ( TGR + T_aa_GR ) ) )

            RelDiffACxi18     \
              = max( RelDiffACxi18, \
                     abs( TGR - T_ac_GR ) / ( 0.5 * ( TGR + T_ac_GR ) ) )

            omegaT_xi18.append( wT_NR )
            omegaT_xi18.append( wT_GR )

        if xi == '2.8':

            GrowthRateRatioGRoverNRxi28 \
              = min( GrowthRateRatioGRoverNRxi28, G_GR / G_NR )

            PeriodRatioGRoverNRxi28 = max( PeriodRatioGRoverNRxi28, TGR / TNR )

            RelDiffAAxi28     \
              = max( RelDiffAAxi28, \
                     abs( TGR - T_aa_GR ) / ( 0.5 * ( TGR + T_aa_GR ) ) )

            RelDiffACxi28     \
              = max( RelDiffACxi28, \
                     abs( TGR - T_ac_GR ) / ( 0.5 * ( TGR + T_ac_GR ) ) )

            omegaT_xi28.append( wT_NR )
            omegaT_xi28.append( wT_GR )

        table += '  \\texttt{{NR\_{:}}}'.format( ID.replace( '_', '\\_' ) )

        table += ' & {:.4f} $\\pm$ {:.4f}'.format \
                   ( TNR, dT_NR )

        table += ' & {:.4f} $\\pm$ {:.4f}'.format \
                   ( G_NR, dG_NR )

        table += ' & {:.4f}'.format \
                   ( wT_NR )

        table += ' & {:.4f}'.format \
                   ( T_aa_NR )

        table += ' & {:.4f} \\\\\n'.format \
                   ( T_ac_NR )

        table += '  \\texttt{{GR\_{:}}}'.format( ID.replace( '_', '\\_' ) )

        table += ' & {:.4f} $\\pm$ {:.4f}'.format \
                   ( TGR, dT_GR )

        table += ' & {:.4f} $\\pm$ {:.4f}'.format \
                   ( G_GR, dG_GR )

        table += ' & {:.4f}'.format \
                   ( wT_GR )

        table += ' & {:.4f}'.format \
                   ( T_aa_GR )

        table += ' & {:.4f} \\\\\n'.format \
                   ( T_ac_GR )

table += '  \\enddata\n'
table += '  \\label{tab.results}\n'
table += '  \\tablecomments{\n'
table += \
'Oscillation periods, growth rates, and their uncertainties for all\n'
table += \
'fourteen models having the same accretion rate of $0.3\\,\\msun\\,\\s^{-1}$.\n'
table += \
'\\repl{The first six are the low-compactness models; the last four\n'
table += \
'are the high-compactness models.}{}\n'
table += \
'The uncertainties for the growth rates are defined as the square roots of the\n'
table += \
'diagonal entries of the covariance matrix corresponding to the growth rate.\n'
table += \
'The uncertainies for the oscillation period are defined as the full-width\n'
table += \
'half-maximum values of the Fourier amplitudes (see \\figref{fig.fft}).\n'
table += \
'The fourth column shows the product of the best-fit growth rate multiplied\n'
table += \
'by the best-fit oscillation period.\n'
table += \
'The fifth column shows the estimate for the period assuming an\n'
table += \
'advective-acoustic origin of the SASI (\\eqref{eq.MullerEst}),\n'
table += \
'and the sixth column shows the estimate for the period assuming\n'
table += \
'a purely acoustic origin of the SASI (\\eqref{eq.Tac}), where we use\n'
table += \
'$\\rac=0.85\\,\\rsh$, the midpoint\n'
table += \
'of the shell in which we compute the power (see \\secref{sec.results}).}\n'
table += '\\end{deluxetable}'

print( '\\newcommand{{\\PeriodRatioGRoverNRxiA}}{{{:.2f}}}' \
       .format( PeriodRatioGRoverNRxi04 ) )
print( '\\newcommand{{\\PeriodRatioGRoverNRxiB}}{{{:.2f}}}' \
       .format( PeriodRatioGRoverNRxi07 ) )
print( '\\newcommand{{\\PeriodRatioGRoverNRxiC}}{{{:.2f}}}' \
       .format( PeriodRatioGRoverNRxi18 ) )
print( '\\newcommand{{\\PeriodRatioGRoverNRxiD}}{{{:.2f}}}' \
       .format( PeriodRatioGRoverNRxi28 ) )
print( '\\newcommand{{\\GrowthRateRatioGRoverNRxiA}}{{{:.2f}}}' \
       .format( GrowthRateRatioGRoverNRxi04 ) )
print( '\\newcommand{{\\GrowthRateRatioGRoverNRxiB}}{{{:.2f}}}' \
       .format( GrowthRateRatioGRoverNRxi07 ) )
print( '\\newcommand{{\\GrowthRateRatioGRoverNRxiC}}{{{:.2f}}}' \
       .format( GrowthRateRatioGRoverNRxi18 ) )
print( '\\newcommand{{\\GrowthRateRatioGRoverNRxiD}}{{{:.2f}}}' \
       .format( GrowthRateRatioGRoverNRxi28 ) )
print( '\\newcommand{{\\RelDiffAAxiA}}{{{:.2f}}}' \
       .format( RelDiffAAxi04 ) )
print( '\\newcommand{{\\RelDiffAAxiB}}{{{:.2f}}}' \
       .format( RelDiffAAxi07 ) )
print( '\\newcommand{{\\RelDiffAAxiC}}{{{:.2f}}}' \
       .format( RelDiffAAxi18 ) )
print( '\\newcommand{{\\RelDiffAAxiD}}{{{:.2f}}}' \
       .format( RelDiffAAxi28 ) )
print( '\\newcommand{{\\RelDiffACxiA}}{{{:.2f}}}' \
       .format( RelDiffACxi04 ) )
print( '\\newcommand{{\\RelDiffACxiB}}{{{:.2f}}}' \
       .format( RelDiffACxi07 ) )
print( '\\newcommand{{\\RelDiffACxiC}}{{{:.2f}}}' \
       .format( RelDiffACxi18 ) )
print( '\\newcommand{{\\RelDiffACxiD}}{{{:.2f}}}' \
       .format( RelDiffACxi28 ) )

omegaT_xi04 = np.array( omegaT_xi04 )
omegaT_xi07 = np.array( omegaT_xi07 )
omegaT_xi18 = np.array( omegaT_xi18 )
omegaT_xi28 = np.array( omegaT_xi28 )

mu_xi04 = omegaT_xi04.mean()
mu_xi07 = omegaT_xi07.mean()
mu_xi18 = omegaT_xi18.mean()
mu_xi28 = omegaT_xi28.mean()

print( 'omega * T (xi = 0.4): {:.2f} +{:.2f} -{:.2f}' \
       .format( mu_xi04, omegaT_xi04.max() - mu_xi04, \
                mu_xi04 - omegaT_xi04.min() ) )
print( 'omega * T (xi = 0.7): {:.2f} +{:.2f} -{:.2f}' \
       .format( mu_xi07, omegaT_xi07.max() - mu_xi07, \
                mu_xi07 - omegaT_xi07.min() ) )
print( 'omega * T (xi = 1.8): {:.2f} +{:.2f} -{:.2f}' \
       .format( mu_xi18, omegaT_xi18.max() - mu_xi18, \
                mu_xi18 - omegaT_xi18.min() ) )
print( 'omega * T (xi = 2.8): {:.2f} +{:.2f} -{:.2f}' \
       .format( mu_xi28, omegaT_xi28.max() - mu_xi28, \
                mu_xi28 - omegaT_xi28.min() ) )

#print( table )
#with open( paperDirectory + 'resultsTable.tex', 'w' ) as tab:
#    tab.write( table )
