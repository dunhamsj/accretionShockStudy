#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
plt.style.use( 'publication.sty' )

from UtilitiesModule import GetNorm, MapCenterToCorners
from MakeDataFile import MakeDataFile, ReadHeader

"""

Creates a directory with structure as laid out
in MakeDataFile.py and makes a movie from it

Usage:
  $ python3 makeMovie2D.py

"""

#### ========== User Input ==========

# ID to be used for naming purposes
ID = 'GR2D_M2.8_Rpns020_Rs6.00e1'

# Directory containing AMReX plotfiles
plotfileDirectory \
  = '/lump/data/accretionShockStudy/newData/2D/{:}/'.format( ID )
#plotfileDirectory \
#  = '/home/kkadoogan/{:}/'.format( ID )

# plotfile base name (e.g., Advection2D.plt######## -> Advection2D.plt )
plotfileBaseName = ID + '.plt'

# Field to plot
field = 'PolytropicConstant'

# Scale of colorbar
zScale = 'None'
#zScale = 'log'
#zScale = 'symlog'
linthresh = 1.0e-4#1.0e27

# Coordinate system (currently supports 'cartesian' and 'spherical' )
CoordinateSystem = 'spherical'

# Only use every <plotEvery> plotfile
plotEvery   = 1
maxPlotfile = -1

# Colormap
cmap = 'viridis'

# First and last snapshots and number of snapshots to include in movie
SSi = -1 # -1 -> SSi = 0
SSf = -1 # -1 -> plotfileArray.shape[0] - 1
nSS = -1 # -1 -> plotfileArray.shape[0]

UseCustomLimits = True
vmin = 1.5e16
vmax = 1.9e16

MovieRunTime = 5.0 # seconds

Verbose = True

#### ====== End of User Input =======

if CoordinateSystem == 'spherical':
    polar = True
else:
    polar = False

DataDirectory = '.{:s}'.format( ID )
MovieName     = 'mov.{:s}_{:s}.mp4'.format( ID, field )

# Append "/" if not present
if not plotfileDirectory[-1] == '/': plotfileDirectory += '/'
if not DataDirectory    [-1] == '/': DataDirectory     += '/'

plotfileArray \
  = MakeDataFile( field, plotfileDirectory, DataDirectory, \
                  plotfileBaseName, CoordinateSystem, \
                  SSi = SSi, SSf = SSf, nSS = nSS, \
                  UsePhysicalUnits = True, \
                  MaxLevel = -1, Verbose = Verbose )
plotfileArray = np.copy( plotfileArray[::plotEvery] )
plotfileArray = np.copy( plotfileArray[0:maxPlotfile] )

def f(t):

    FileDirectory = DataDirectory + plotfileArray[t] + '/'

    TimeFile = FileDirectory + '{:}.dat'.format( 'Time' )
    X1File   = FileDirectory + '{:}.dat'.format( 'X1' )
    X2File   = FileDirectory + '{:}.dat'.format( 'X2' )
    dX1File  = FileDirectory + '{:}.dat'.format( 'dX1' )
    dX2File  = FileDirectory + '{:}.dat'.format( 'dX2' )
    DataFile = FileDirectory + '{:}.dat'.format( field )

    DataShape, DataUnits, MinVal, MaxVal = ReadHeader( DataFile )

    Time = np.loadtxt( TimeFile )
    X1_C = np.loadtxt( X1File   ).reshape( np.int64( DataShape ) )
    X2_C = np.loadtxt( X2File   ).reshape( np.int64( DataShape ) )
    dX1  = np.loadtxt( dX1File  ).reshape( np.int64( DataShape ) )
    dX2  = np.loadtxt( dX2File  ).reshape( np.int64( DataShape ) )
    Data = np.loadtxt( DataFile )

    shape = ( X2_C.shape[0], 2*X2_C.shape[1] )

    X22_C = np.empty( shape, np.float64 )
    dX22  = np.empty( shape, np.float64 )
    X11_C = np.empty( shape, np.float64 )
    dX11  = np.empty( shape, np.float64 )
    Dataa = np.empty( shape, np.float64 )

    for iX1 in range( shape[0] ):

        X22_C[iX1,0 :64] = np.copy( X2_C[iX1]       )
        X22_C[iX1,64:  ] = np.copy( X2_C[iX1] + np.pi )
        dX22 [iX1,0 :64] = np.copy( dX2 [iX1]       )
        dX22 [iX1,64:  ] = np.copy( dX2 [iX1][::-1] )

        X11_C[iX1,0 :64] = np.copy( X1_C[iX1] )
        X11_C[iX1,64:  ] = np.copy( X1_C[iX1] )
        dX11 [iX1,0 :64] = np.copy( dX1 [iX1] )
        dX11 [iX1,64:  ] = np.copy( dX1 [iX1] )

        Dataa[iX1,0 :64] = np.copy( Data[iX1]       )
        Dataa[iX1,64:  ] = np.copy( Data[iX1][::-1] )

    X2_C = np.copy( X22_C )
    dX2  = np.copy( dX22 )

    X1_C = np.copy( X11_C )
    dX1  = np.copy( dX11 )

    Data = np.copy( Dataa )

    return Data, DataUnits, X1_C, X2_C, dX1, dX2, Time

Data0, DataUnits, X1_C, X2_C, dX1, dX2, Time = f(0)

if nSS < 0: nSS = plotfileArray.shape[0]

if not UseCustomLimits:
    vmin = +np.inf
    vmax = -np.inf
    for j in range( nSS ):
        DataFile \
          = DataDirectory + plotfileArray[j] + '/{:}.dat'.format( field )
        DataShape, DataUnits, MinVal, MaxVal = ReadHeader( DataFile )
        vmin = min( vmin, MinVal )
        vmax = max( vmax, MaxVal )

nX = np.shape(X1_C)

x1L = X1_C[0 ,0 ] - 0.5 * dX1[0 ,0 ]
x1H = X1_C[-1,-1] + 0.5 * dX1[-1,-1]
x2L = X2_C[0 ,0 ] - 0.5 * dX2[0 ,0 ]
x2H = X2_C[-1,-1] + 0.5 * dX2[-1,-1]

fig = plt.figure()
ax  = fig.add_subplot( 111, polar = polar )
ax.set_title( r'$\texttt{{{:}}}$'.format( ID ) )

X1c, X2c = MapCenterToCorners( X1_C, X2_C, dX1, dX2 )

if CoordinateSystem == 'spherical':

    X1c = np.copy( X1c[:,0] )
    X2c = np.copy( X2c[0,:] )

    X1c, X2c = np.meshgrid( X2c, X1c )

    ax.grid( False )

elif CoordinateSystem == 'cartesian':

    ax.set_xlabel \
      ( r'$x^{{1}}\ \left[\mathrm{km}\right]$', \
        fontsize = 15 )
    ax.set_ylabel \
      ( r'$x^{{2}}\ \left[\mathrm{rad}\right]$', \
        fontsize = 15 )

#vmn = vmin
#vmx = vmax
#
#vmin = min( vmn, -vmx )
#vmax = max( vmx, -vmn )

Norm \
  = GetNorm( zScale, Data0, vmin = vmin, vmax = vmax, \
             linthresh = linthresh )

im = ax.pcolormesh( X1c, X2c, Data0, \
                    cmap = cmap, \
                    norm = Norm, \
                    shading = 'flat' )

time_text = ax.text( 0.3, 0.9, '', c = 'w', transform = ax.transAxes )

cbar = fig.colorbar( im )
#cbar.set_label( field + ' ' + r'$\mathrm{{{:}}}$'.format( DataUnits[1:-1] ) )
#cbar.set_label( r'$v^{\theta}\,\left[\mathrm{s}^{-1}\right]$' )
cbar.set_label( r'$K\,\left[\mathrm{cgs}\right]$' )

def InitializeFrame():

    Data, DataUnits, X1_C, X2_C, dX1, dX2, Time = f(0)
    im.set_array( Data.flatten() )
    time_text.set_text('')
    ret = ( im, time_text )
    return ret

def UpdateFrame(t):

    print( '    {:}/{:}'.format( t, nSS ) )
    Data, DataUnits, X1_C, X2_C, dX1, dX2, Time = f(t)

    im.set_array( Data.flatten() )
    time_text.set_text( r'$t={:.3e}\ \mathrm{{ms}}$' \
                        .format( Time ) )

    ret = ( im, time_text )

    return ret

# Call the animator
anim \
  = animation.FuncAnimation \
      ( fig, UpdateFrame, init_func = InitializeFrame, \
        frames = nSS, blit = True)

fps = max( 1, nSS // MovieRunTime )

print( '\n  Making Movie' )
print( '  ------------' )

if CoordinateSystem == 'spherical':

    ax.set_thetamin( 0.0 )
    ax.set_thetamax( 360.0 )
    ax.set_rmin( 0.0 )
    ax.set_rmax( 90.0 )

    ax.set_theta_zero_location( 'N' ) # z-axis vertical
    ax.set_theta_direction( -1 )
else:
    ax.grid()

anim.save( MovieName, fps = fps, dpi = 300 )
print( '\n  Saved movie: {:}'.format( MovieName ) )

import os
os.system( 'rm -rf __pycache__ ' )
