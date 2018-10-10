#!/usr/bin/env python

# Illustrating the difference between Euler and Runge-Kutta propagation
# schemes, using an idealised (analytical) eddy current field.

from datetime import datetime, timedelta
import matplotlib.pyplot as plt

from opendrift.readers import reader_double_gyre
from opendrift.models.oceandrift import OceanDrift

o = OceanDrift(loglevel=20)  # Set loglevel to 0 for debug information

o.fallback_values['land_binary_mask'] = 0
# Note that Runge-Kutta here makes a difference to Euler scheme
o.set_config('drift:scheme', 'runge-kutta')

double_gyre = reader_double_gyre.Reader(epsilon=.1, omega=0.628, A=0.25)
print double_gyre

o.add_reader(double_gyre)

lcs = o.calculate_ftle(time=double_gyre.initial_time,
                       time_step=timedelta(seconds=.1),
                       duration=timedelta(seconds=5),
                       delta=.01)

# These plots should reproduce Mov 12 on this page (but they dont):
# http://shaddenlab.berkeley.edu/uploads/LCS-tutorial/examples.html
plt.subplot(2,1,1)
plt.imshow(lcs['RLCS'][0,:], interpolation='nearest', cmap='jet')
plt.colorbar()
plt.title('Repelling LCS (forwards)')
plt.subplot(2,1,2)
plt.imshow(lcs['ALCS'][0,:], interpolation='nearest', cmap='jet')
plt.colorbar()
plt.title('Attracting LCS (backwards)')
plt.show()