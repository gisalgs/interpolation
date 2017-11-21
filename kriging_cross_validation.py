from __future__ import print_function
import numpy as np
import sys
sys.path.append('../geom')
from point import *
from fitsemivariance import *
from semivariance import *
from covariance import *
from read_data import *
from prepare_interpolation_data import *
from okriging import *

Z = read_data('../data/necoldem250.dat')

hh = 50
lags = np.arange(0, 3000, hh)
test_results = []
N = len(Z)
mask = [True for i in range(N)]
numNeighbors = 10

for i in range(N):
    mask[i] = False
    x = Point(Z[i][0], Z[i][1])
    P = [ Z[j] for j in range(N) if mask[j] == True]
    P1 = prepare_interpolation_data(x, P, numNeighbors)[0]
    P1 = np.array(P1)
    gamma = semivar(P1, lags, hh)    #*@\label{krig:cross:semivar}
    if len(gamma) == 0:
        continue
    semivariogram = fitsemivariogram(P1, gamma, spherical)
    kresult = okriging(P1, semivariogram)
    test_results.append(kresult[0]-Z[i][2])
    mask[i] = True

print(np.sqrt(sum([r**2 for r in test_results])/len(test_results)))
