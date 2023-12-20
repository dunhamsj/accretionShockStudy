#!/usr/bin/env python3

import numpy as np

home = '/home/kkadoogan/'

dataDirectory    = './plottingData/'
figuresDirectory = home + 'Work/accretionShockPaper/Figures/'

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = ['#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00']

def getRsInd( ID ):

    RsFileName \
      = dataDirectory + 'ShockRadiusVsTime_{:}.dat'.format( ID )
    Time, RsAve, RsMin, RsMax = np.loadtxt( RsFileName )

    # Remove unperturbed file
    RsAve = np.copy( RsAve[:-1] )
    RsMax = np.copy( RsMax[:-1] )

    ind = np.where( RsMax > 1.1 * RsAve[0] )[0]
    if ind.shape[0] == 0:
        ind = -1
    else:
        ind = ind[0]

    return ind
