#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
plt.style.use( 'publication.sty' )

from MakeDataFile import MakeDataFile, ReadHeader
from UtilitiesModule import ProjectOntoP1

"""

Creates a directory with structure as laid out
in MakeDataFile.py and makes a movie from it

Usage:
  $ python3 makeMovie1D.py

"""

#### ========== User Input ==========

Rs = '6.00e1'
# ID to be used for naming purposes
ID = 'GR2D_M2.8_Rpns020_Rs{:}'.format( Rs )

# Directory containing AMReX plotfiles
plotfileDirectory \
  = '/lump/data/accretionShockStudy/newData/2D/{:}'.format( ID )

# plotfile base name (e.g., Advection1D.plt######## -> Advection1D.plt )
plotfileBaseName = ID + '.plt'

# Field to plot
Field = 'DivV2'

# Plot data in log10-scale?
UseLogScale_Y = True

# Only use every <plotEvery> plotfile
plotEvery = 1

# First and last snapshots and number of snapshots to include in movie
SSi = -1 # -1 -> SSi = 0
SSf = -1 # -1 -> plotfileArray.shape[0] - 1
nSS = -1 # -1 -> plotfileArray.shape[0]

Verbose = True

UseCustomLimits = True
vmin = 0.0
vmax = 1.0e10

MovieRunTime = 10.0 # seconds

#### ====== End of User Input =======

dataDirectory = '.{:}'.format( ID )
MovieName     = 'mov.{:}_H1integrand.mp4'.format( ID )

# Append "/" if not present
if not plotfileDirectory[-1] == '/': plotfileDirectory += '/'
if not dataDirectory    [-1] == '/': dataDirectory     += '/'

TimeUnits = 'ms'
X1Units   = 'km'

dum \
  = MakeDataFile( 'GF_Psi', plotfileDirectory, dataDirectory, \
                  plotfileBaseName, 'spherical', \
                  SSi = SSi, SSf = SSf, nSS = nSS, \
                  UsePhysicalUnits = True, \
                  MaxLevel = -1, Verbose = Verbose )
plotfileArray \
  = MakeDataFile( Field, plotfileDirectory, dataDirectory, \
                  plotfileBaseName, 'spherical', \
                  SSi = SSi, SSf = SSf, nSS = nSS, \
                  UsePhysicalUnits = True, \
                  MaxLevel = -1, Verbose = Verbose )
plotfileArray = np.copy( plotfileArray[:-1] ) # ignore 99999999 file
plotfileArray = np.copy( plotfileArray[::plotEvery] )

def f(t):

    FileDirectory = dataDirectory + plotfileArray[t] + '/'

    TimeFile = FileDirectory + '{:}.dat'.format( 'Time' )
    X1File   = FileDirectory + '{:}.dat'.format( 'X1' )
    X2File   = FileDirectory + '{:}.dat'.format( 'X2' )
    dX1File  = FileDirectory + '{:}.dat'.format( 'dX1' )
    dX2File  = FileDirectory + '{:}.dat'.format( 'dX2' )
    DataFile = FileDirectory + '{:}.dat'.format( Field )

    DataShape, DataUnits, MinVal, MaxVal = ReadHeader( DataFile )

    Time = np.loadtxt( TimeFile )
    X1_C = np.loadtxt( X1File   ).reshape( DataShape )
    X2_C = np.loadtxt( X2File   ).reshape( DataShape )
    dX1  = np.loadtxt( dX1File  ).reshape( DataShape )
    dX2  = np.loadtxt( dX2File  ).reshape( DataShape )
    Data = np.loadtxt( DataFile )

    G1 = ProjectOntoP1( Data, X2_C[0,:], dX2[0,:] )

    PsiFile = FileDirectory + '{:}.dat'.format( 'GF_Psi' )
    Psi = np.loadtxt( PsiFile ).reshape( DataShape )

    H1integrand = 4.0 * np.pi * G1**2 * Psi[:,0]**6 * X1_C[:,0]**2

    return H1integrand, DataUnits, X1_C[:,0], dX1[:,0], Time

Data0, DataUnits, X1_C0, dX10, Time = f(0)

if nSS < 0: nSS = plotfileArray.shape[0]

if not UseCustomLimits:
    vmin = +np.inf
    vmax = -np.inf
    for j in range( nSS ):
        DataFile \
          = dataDirectory + plotfileArray[j] + '/{:}.dat'.format( Field )
        DataShape, DataUnits, MinVal, MaxVal = ReadHeader( DataFile )
        vmin = min( vmin, MinVal )
        vmax = max( vmax, MaxVal )

nX = np.shape( X1_C0 )

xL = X1_C0[0 ] - 0.5 * dX10[0 ]
xH = X1_C0[-1] + 0.5 * dX10[-1]

fig = plt.figure()
ax  = fig.add_subplot( 111 )
ax.set_title( r'$\texttt{{{:}}}$'.format( ID ), fontsize = 15 )

Rs = np.float64( Rs )
ax.axvline( 0.8 * Rs, color = 'k' )
ax.axvline( 0.9 * Rs, color = 'k' )

time_text = ax.text( 0.65, 0.9, '', transform = ax.transAxes, fontsize = 13 )

ax.set_xlabel \
  ( r'$r\ \left[\mathrm{{{:}}}\right]$'.format( X1Units ), fontsize = 15 )
ax.set_ylabel( \
  r'$4\pi\,\left[G_{1}\right]^{2}\,\psi^{6}\,r^{2}\,\left[\mathrm{km^{2}/s^{2}}\right]$' )

ax.set_xlim( xL-5.0, xH )
ax.set_ylim( vmin, vmax )

if UseLogScale_Y: ax.set_yscale( 'symlog', linthresh = 1.0e1 )

line, = ax.plot( [], [], 'b.' )

def InitializeFrame():

    line.set_data( [], [] )
    time_text.set_text( '' )

    ret = ( line, time_text )

    return ret

def UpdateFrame( t ):

    print('    {:}/{:}'.format( t, nSS ) )
    Data, DataUnits, X1_C, dX1, Time = f(t)

    time_text.set_text( r'$t={:.3e}\ \left[\mathrm{{{:}}}\right]$' \
                        .format( Time, TimeUnits ) )

    line.set_data( X1_C ,Data.flatten() )

    ret = ( line, time_text )

    return ret

anim = animation.FuncAnimation( fig, UpdateFrame, \
                                init_func = InitializeFrame, \
                                frames = nSS, \
                                blit = True )

fps = max( 1, nSS / MovieRunTime )

print( '\n  Making movie' )
print( '  ------------' )
anim.save( MovieName, fps = fps, dpi = 300 )

import os
os.system( 'rm -rf __pycache__ ' )
