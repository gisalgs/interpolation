from pylab import *
import numpy as np
import sys
sys.path.append('../geom')
from point import *
from semivariance import *
from covariance import *
from read_data import *
from fitsemivariance import *

Z = read_data('../data/necoldem.dat')

hh = 50
lags = range(0, 3000, hh)
gamma = semivar(Z, lags, hh)
covariance = covar(Z, lags, hh)
Z1 = np.array(Z)
svs = fitsemivariogram(Z1, gamma, spherical)
svl = fitsemivariogram(Z1, gamma, linear)
svg = fitsemivariogram(Z1, gamma, gaussian)
sve = fitsemivariogram(Z1, gamma, exponential)

p1, = plot(gamma[0], gamma[1], 'o')
p2, = plot(gamma[0], svs(gamma[0]), color='grey', lw=2)
p3, = plot(gamma[0], svl(gamma[0]), color='grey', lw=2,
           linestyle="--")
p4, = plot(gamma[0], svg(gamma[0]), color='grey', lw=2,
           linestyle="-.")
p5, = plot(gamma[0], sve(gamma[0]), color='grey', lw=2,
           linestyle=":")
models = ["Empirical", "Spherical", "Linear",
          "Gaussian", "exponential"]
l1 = legend([p1,p2,p3,p4, p5], models, loc='lower right')
ylabel('Semivariance')
xlabel('Lag (m)')
savefig('semivariogram_data_model.eps',fmt='eps')
show()
