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

nT = 5

Rs = '6.00e1'
# ID to be used for naming purposes
GRID = 'GR2D_M2.8_Rpns020_Rs{:}'.format( Rs )
NRID = 'NR2D_M2.8_Rpns020_Rs{:}'.format( Rs )

# Directory containing AMReX plotfiles
GRplotfileDirectory \
  = '/lump/data/accretionShockStudy/newData/2D/{:}'.format( GRID )
NRplotfileDirectory \
  = '/lump/data/accretionShockStudy/newData/2D/{:}'.format( NRID )

# plotfile base name (e.g., Advection1D.plt######## -> Advection1D.plt )
GRplotfileBaseName = GRID + '.plt'
NRplotfileBaseName = NRID + '.plt'

# Field to plot
Field = 'AngularKineticEnergy'

# Plot data in log10-scale?
UseLogScale_Y = True

# Only use every <plotEvery> plotfile
plotEvery = 1

# First and last snapshots and number of snapshots to include in movie
SSi = 0 # -1 -> SSi = 0
SSf = 220 # -1 -> plotfileArray.shape[0] - 1
nSS = -1 # -1 -> plotfileArray.shape[0]

Verbose = True

UseCustomLimits = False
vmin = -1.0e32
vmax = +1.0e40

MovieRunTime = 10.0 # seconds

#### ====== End of User Input =======

GRdataDirectory = '.{:}'.format( GRID )
NRdataDirectory = '.{:}'.format( NRID )
MovieName     = 'mov.{:}_EnergyBudget.mp4'.format( GRID[2:] )

# Append "/" if not present
if not GRplotfileDirectory[-1] == '/': GRplotfileDirectory += '/'
if not GRdataDirectory    [-1] == '/': GRdataDirectory     += '/'
if not NRplotfileDirectory[-1] == '/': NRplotfileDirectory += '/'
if not NRdataDirectory    [-1] == '/': NRdataDirectory     += '/'

TimeUnits = 'ms'
X1Units   = 'km'

fcD = False
owD = False
fcF = False
owF = False

GRplotfileArray \
  = MakeDataFile( Field, GRplotfileDirectory, GRdataDirectory, \
                  GRplotfileBaseName, 'spherical', \
                  SSi = SSi, SSf = SSf, nSS = nSS, \
                  UsePhysicalUnits = True, \
                  forceChoiceD = fcD, owD = owD, \
                  forceChoiceF = fcF, owF = owF, \
                  MaxLevel = -1, Verbose = Verbose )
GRplotfileArray = np.copy( GRplotfileArray[:-1] ) # ignore 99999999 file
#GRplotfileArray = np.copy( GRplotfileArray[::plotEvery] )
GRplotfileArray = np.copy( GRplotfileArray[SSi:SSf+1:plotEvery] )

NRplotfileArray \
  = MakeDataFile( Field, NRplotfileDirectory, NRdataDirectory, \
                  NRplotfileBaseName, 'spherical', \
                  SSi = SSi, SSf = SSf, nSS = nSS, \
                  UsePhysicalUnits = True, \
                  forceChoiceD = fcD, owD = owD, \
                  forceChoiceF = fcF, owF = owF, \
                  MaxLevel = -1, Verbose = Verbose )
NRplotfileArray = np.copy( NRplotfileArray[:-1] ) # ignore 99999999 file
#NRplotfileArray = np.copy( NRplotfileArray[::plotEvery] )
NRplotfileArray = np.copy( NRplotfileArray[SSi:SSf+1:plotEvery] )

# Get theta-mesh
FileDirectory = GRdataDirectory + GRplotfileArray[0] + '/'
X2File        = FileDirectory + '{:}.dat'.format( 'X2' )
DataFile      = FileDirectory + '{:}.dat'.format( Field )
DataShape, DataUnits, MinVal, MaxVal = ReadHeader( DataFile )
theta = np.loadtxt( X2File ).reshape( DataShape )[0]
N     = theta.shape[0]

def f(t):

    FileDirectory = GRdataDirectory + GRplotfileArray[t] + '/'
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
    GRy0 = Data[:,0   ]
    GRy1 = Data[:,N//4]
    GRy2 = Data[:,N//2]
    GRy3 = Data[:,3*N//4]
    GRy4 = Data[:,-1  ]

    FileDirectory = NRdataDirectory + NRplotfileArray[t] + '/'
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
    NRy0 = Data[:,0   ]
    NRy1 = Data[:,N//4]
    NRy2 = Data[:,N//2]
    NRy3 = Data[:,3*N//4]
    NRy4 = Data[:,-1  ]

    GRd = np.vstack( ( GRy0, GRy1, GRy2, GRy3, GRy4 ) )
    NRd = np.vstack( ( NRy0, NRy1, NRy2, NRy3, NRy4 ) )

    dd = ( NRd - GRd )# / ( 0.5 * ( NRd + GRd ) )
    return dd, DataUnits, X1_C[:,0], dX1[:,0], Time

Data0, DataUnits, X1_C0, dX10, Time = f(0)

if nSS < 0: nSS = NRplotfileArray.shape[0]

if not UseCustomLimits:
    vmin = +np.inf
    vmax = -np.inf
    for j in range( nSS ):
        GRDataFile \
          = GRdataDirectory + GRplotfileArray[j] + '/{:}.dat'.format( Field )
        NRDataFile \
          = NRdataDirectory + NRplotfileArray[j] + '/{:}.dat'.format( Field )
        DataShape, DataUnits, GRMinVal, GRMaxVal = ReadHeader( GRDataFile )
        DataShape, DataUnits, NRMinVal, NRMaxVal = ReadHeader( NRDataFile )
        vmin = min( vmin, GRMinVal, NRMinVal )
        vmax = max( vmax, GRMaxVal, NRMaxVal )

nX = np.shape( X1_C0 )

xL = X1_C0[0 ] - 0.5 * dX10[0 ]
xH = X1_C0[-1] + 0.5 * dX10[-1]

fig = plt.figure()
ax  = fig.add_subplot( 111 )
ax.set_title( r'$\texttt{{{:}}}$'.format( GRID[2:] ), fontsize = 15 )

Rs = np.float64( Rs )

time_text = ax.text( 0.65, 0.9, '', transform = ax.transAxes, fontsize = 13 )

ax.set_xlabel \
  ( r'$r\ \left[\mathrm{{{:}}}\right]$'.format( X1Units ), fontsize = 15 )
ax.set_ylabel( r'$\tau^{\theta}_{\mathrm{NR}}-\tau^{\theta}_{\mathrm{GR}}$' )

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = ['#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00']
ind = np.empty( nT, np.int64 )
ind[0] = 0
ind[1] = N//4
ind[2] = N//2
ind[3] = 3*N//4
ind[4] = -1
line = np.empty( (nT), object )
for i in range( nT ):
    line[i], \
      = ax.plot( [], [], '-', color = color[i], \
                 label = r'$\theta={:}$' \
                         .format \
                         ( np.round( theta[ind[i]] * 1.80e2 / np.pi, 2 ) ) )

def InitializeFrame():

    ret = []
    for i in range( nT ):
        line[i].set_data( [], [] )
        ret.append( line[i] )

    time_text.set_text( '' )
    ret.append( time_text )

    ret = ( ret )

    return ret

def UpdateFrame( t ):

    print('    {:}/{:}'.format( t, nSS ) )
    Data, DataUnits, X1_C, dX1, Time = f(t)

    ret = []
    for i in range( nT ):
        line[i].set_data( X1_C ,Data[i].flatten() )
        ret.append( line[i] )

    time_text.set_text( r'$t={:.3e}\ \left[\mathrm{{{:}}}\right]$' \
                        .format( Time, TimeUnits ) )
    ret.append( time_text )

    ret = ( ret )

    return ret

anim = animation.FuncAnimation( fig, UpdateFrame, \
                                init_func = InitializeFrame, \
                                frames = nSS, \
                                blit = True )

ax.text( 50, -1.0e30, r'$\tau^{\theta}:=\frac{S^{2}S_{2}}{2\,D}$', fontsize = 15 )
ax.set_xlim( xL-5.0, 1.01 * Rs )
ax.set_ylim( vmin, vmax )
if UseLogScale_Y: ax.set_yscale( 'symlog', linthresh = 1.0e30 )
ax.legend( loc = 3 )

fps = max( 1, nSS / MovieRunTime )

print( '\n  Making movie' )
print( '  ------------' )
anim.save( MovieName, fps = fps, dpi = 300 )

import os
os.system( 'rm -rf __pycache__ ' )
