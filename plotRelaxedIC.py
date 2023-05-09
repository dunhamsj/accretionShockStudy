#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

root = '/lump/data/accretionShockStudy/newData/1D/'
ID   = 'NR1D_M1.4_Rpns040_Rs1.80e2'
data = np.loadtxt( '{:}{:}/{:}.IC'.format( root, ID, ID ), skiprows = 3 )

D = data[0::3].flatten()
V = data[1::3].flatten()
P = data[2::3].flatten()

plt.plot( V )
plt.show()
