#!/usr/bin/env python3

from os.path import isfile
import numpy as np

Rpns = [ '040', '020' ]
M    = [ '1.4', '2.8' ]
Rs   = [ [ '1.20e2', '1.50e2', '1.75e2' ], \
         [ '6.00e1', '7.00e1' ] ]

#R_ac_NR = [ [ 87.45, 122.25, 152.25 ], [ 43.95, 55.45 ] ]
#R_ac_GR = [ [ 93.55, 130.65, 162.55 ], [ 57.65, 69.95 ] ]

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

Models = {}
with open( '../plottingData/fft.dat' ) as f:
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
  \\colhead{Model}                                                  &\n\
  \\colhead{$T\\pm\\Delta T\\,\\left[\\ms\\right]$}                 &\n\
  \\colhead{$\\omega\\pm\\Delta\\omega\\,\\left[\\ms^{-1}\\right]$} &\n\
  \\colhead{$\\omega\,T$}                                           &\n\
  \\colhead{$T_{\\mathrm{aa}}\\,\\left[\\ms\\right]$}               &\n\
  \\colhead{$T_{\\mathrm{ac}}\\,\\left[\\ms\\right]$}               %\n\
  }\n\
  \\startdata\n\
'

ratio_nrgr_LC_w = +np.inf
ratio_nrgr_HC_w = +np.inf
ratio_nrgr_LC_T = -np.inf
ratio_nrgr_HC_T = -np.inf
reldiff_aa_LC   = -np.inf
reldiff_ac_LC   = -np.inf
reldiff_aa_HC   = -np.inf
reldiff_ac_HC   = -np.inf

wt_g1 = []
wt_g2 = []

i = -1
for m in range( len( M ) ):
    for rs in range( len( Rs[m] ) ):

        ID = 'M{:}_Rpns{:}_Rs{:}'.format( M[m], Rpns[m], Rs[m][rs] )

        dataFileName_NR \
          = '../plottingData/NR2D_{:}_LegendrePowerSpectrum.dat'.format( ID )

        dataFileName_GR \
          = '../plottingData/GR2D_{:}_LegendrePowerSpectrum.dat'.format( ID )

        if not isfile( dataFileName_NR ):
            print( 'File {:} not found. Skipping'.format( dataFileName_NR ) )
            continue

        if not isfile( dataFileName_GR ):
            print( 'File {:} not found. Skipping'.format( dataFileName_GR ) )
            continue

        if m == 1 and rs == 0: table += '\\hline\n'

        i += 1

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

        if m == 0:
            ratio_nrgr_LC_w = min( ratio_nrgr_LC_w, G_GR / G_NR )
            ratio_nrgr_LC_T = max( ratio_nrgr_LC_T, TGR / TNR )
            reldiff_aa_LC     \
              = max( reldiff_aa_LC, \
                     abs( TGR - T_aa_GR ) / ( 0.5 * ( TGR + T_aa_GR ) ) )
            reldiff_ac_LC     \
              = max( reldiff_ac_LC, \
                     abs( TGR - T_ac_GR ) / ( 0.5 * ( TGR + T_ac_GR ) ) )
        if m == 1:
            ratio_nrgr_HC_w = min( ratio_nrgr_HC_w, G_GR / G_NR )
            ratio_nrgr_HC_T = max( ratio_nrgr_HC_T, TGR / TNR )
            reldiff_aa_HC     \
              = max( reldiff_aa_HC, \
                     abs( TGR - T_aa_GR ) / ( 0.5 * ( TGR + T_aa_GR ) ) )
            reldiff_ac_HC     \
              = max( reldiff_ac_HC, \
                     abs( TGR - T_ac_GR ) / ( 0.5 * ( TGR + T_ac_GR ) ) )

        table += '  \\texttt{{NR\_M{:}\\_Rpns{:}\\_Rs{:}}}'.format \
                   ( M[m], Rpns[m], Rs[m][rs] )

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

        table += '  \\texttt{{GR\_M{:}\\_Rpns{:}\\_Rs{:}}}'.format \
                   ( M[m], Rpns[m], Rs[m][rs] )

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

        if m == 0:
            wt_g1.append( wT_NR )
            wt_g1.append( wT_GR )
        if m == 1:
            wt_g1.append( wT_NR )
            wt_g2.append( wT_GR )

table += '  \\enddata\n'
table += '  \\label{tab.results}\n'
table += '  \\tablecomments{\n'
table += \
'Oscillation periods, growth rates, and their uncertainties for all\n'
table += \
'ten models having the same accretion rate of $0.3\\,\\msun\\,\\s^{-1}$.\n'
table += \
'The first six are the low-compactness models; the last four\n'
table += \
'are the high-compactness models.\n'
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
'$R_{\\mathrm{ac}}=0.85\\,\\rs$, the midpoint\n'
table += \
'of the shell in which we compute the power (see \\secref{sec.results}).}\n'
table += '\\end{deluxetable}'

print( 'TGR/TNR (LC)       : {:.2f}'.format( ratio_nrgr_LC_T ) )
print( 'TGR/TNR (HC)       : {:.2f}'.format( ratio_nrgr_HC_T ) )
print( 'GGR/GNR (LC)       : {:.2f}'.format( ratio_nrgr_LC_w ) )
print( 'GGR/GNR (HC)       : {:.2f}'.format( ratio_nrgr_HC_w ) )
print( '|TGR-Taa|/avg. (LC): {:.2f}'.format( reldiff_aa_LC   ) )
print( '|TGR-Taa|/avg. (HC): {:.2f}'.format( reldiff_aa_HC   ) )
print( '|TGR-Tac|/avg. (LC): {:.2f}'.format( reldiff_ac_LC   ) )
print( '|TGR-Tac|/avg. (HC): {:.2f}'.format( reldiff_ac_HC   ) )

wt_g1 = np.array( wt_g1 )
wt_g2 = np.array( wt_g2 )

mu_g1 = wt_g1.mean()
mu_g2 = wt_g2.mean()

print( 'omega * T (Group 1): {:.2f} +{:.2f} -{:.2f}' \
       .format( mu_g1, wt_g1.max() - mu_g1, mu_g1 - wt_g1.min() ) )
print( 'omega * T (Group 2): {:.2f} +{:.2f} -{:.2f}' \
       .format( mu_g2, wt_g2.max() - mu_g2, mu_g2 - wt_g2.min() ) )

#print( table )
#with open( '../resultsTable.tex', 'w' ) as tab:
#    tab.write( table )
