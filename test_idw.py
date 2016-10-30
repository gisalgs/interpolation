import sys
sys.path.append('../geom')
from point import *
from idw import *
from read_data import *
from math import sqrt
from prepare_interpolation_data import *

Z = read_data('../data/necoldem.dat')

x = Point(337000, 4440911)

N = 10

Z1 = prepare_interpolation_data(x, Z, N)[0]

print 'power=0.0:', IDW(Z1, 0)
print 'power=0.5:', IDW(Z1, 0.5)
print 'power=1.0:', IDW(Z1, 1.0)
print 'power=1.5:', IDW(Z1, 1.5)
print 'power=2.0:', IDW(Z1, 2.0)
