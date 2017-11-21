from __future__ import print_function
import sys
sys.path.append('../geom')
from point import *
from idw import *
from read_data import *
from math import sqrt
from prepare_interpolation_data import *

Z = read_data('../data/necoldem.dat')
N = len(Z)
numNeighbors = 10
mask = [True for i in range(N)]
powers = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
test_results = []
for i in range(N):
    mask[i] = False
    x = Point(Z[i][0], Z[i][1])
    P = [ Z[j] for j in range(N) if mask[j] == True]
    P1 = prepare_interpolation_data(x, P, numNeighbors)[0]
    diff = []
    for n in powers:
        zz = IDW(P1, n)
        diff.append(zz-Z[i][2])
    test_results.append(diff)
    mask[i] = True

for i in range(len(powers)):
    rmse = sqrt(sum([r[i]**2 for r in test_results])/
                len(test_results))
    print(rmse, '[', powers[i], ']')
