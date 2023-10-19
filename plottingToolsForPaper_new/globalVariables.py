#!/usr/bin/env python3

import numpy as np

home = '/home/kkadoogan/'
#home = '/Users/dunhamsj/'

dataDirectory         = '../plottingData_new/'
plotfileRootDirectory = '/lump/data/accretionShockStudy/newData/'
#plotfileRootDirectory = home + 'Desktop/SASI_Data/'
paperDirectory        = home + 'Work/accretionShockPaper/'
figuresDirectory      = paperDirectory + 'Figures/'

def getRsInd( ID ):

    RsFileName \
      = dataDirectory + 'ShockRadiusVsTime_{:}.dat'.format( ID )
    Time, RsAve, RsMin, RsMax = np.loadtxt( RsFileName )

    # Remove unperturbed file
    Time  = np.copy( Time [:-1] )
    RsAve = np.copy( RsAve[:-1] )
    RsMin = np.copy( RsMin[:-1] )
    RsMax = np.copy( RsMax[:-1] )

    ind = np.where( RsMax > 1.1 * RsAve[0] )[0]
    if ind.shape[0] == 0:
        ind = -1
    else:
        ind = ind[0]

    return ind
