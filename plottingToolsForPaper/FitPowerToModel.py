#!/usr/bin/env python3

import numpy as np

def FittingFunction( t, logF1, omega_r, omega_i, delta ):

  # Modified fitting function
  # (log of Eq. (9) in Blondin & Mezzacappa, (2006))

  return logF1 + 2.0 * omega_r * t \
           + np.log( np.sin( omega_i * t + delta )**2 )

def Jacobian( t, logF1, omega_r, omega_i, delta ):

  # Jacobian of modified fitting function

  J = np.empty( (t.shape[0],4), np.float64 )

  ImPhase = omega_i * t + delta

  J[:,0] = 1.0

  J[:,1] = 2.0 * t

  J[:,2] = 2.0 * np.cos( ImPhase ) / np.sin( ImPhase ) * t

  J[:,3] = 2.0 * np.cos( ImPhase ) / np.sin( ImPhase )

  return J

