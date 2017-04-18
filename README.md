## Spatial interpolation methods are included here.

### Using IDW

```python
from math import sqrt
import sys
sys.path.append('/Users/xiao/programs/lib/gisalgs')

from geom.point import *
from interpolation.idw import *
from interpolation.prepare_interpolation_data import *

fname = '/Users/xiao/lib/gisalgs/data/necoldem.dat'

f = open(fname, 'r')
Z = f.readlines()
Z = [x.strip().split() for x in Z]
Z = [ [ float(x[0]),float(x[1]),float(x[2])] for x in Z]

x = Point(337000, 4440911)
N = 10

Z1 = prepare_interpolation_data(x, Z, N)[0]

print 'power=0.0:', IDW(Z1, 0)
print 'power=0.5:', IDW(Z1, 0.5)
print 'power=1.0:', IDW(Z1, 1.0)
print 'power=1.5:', IDW(Z1, 1.5)
print 'power=2.0:', IDW(Z1, 2.0)
```

Cross validation on different power values:

```python
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
    rmse = sqrt(sum([r[i]**2 for r in test_results])/len(test_results))
    print rmse, '[', powers[i], ']'
```

### Kriging

```python
import sys
sys.path.append('/Users/xiao/lib/gisalgs')

from math import sqrt
import numpy as np

from geom.point import *
from indexing.kdtree1 import *
from indexing.kdtree3 import *

from interpolation.fitsemivariance import *
from interpolation.semivariance import *
from interpolation.covariance import *
from interpolation.read_data import *
from interpolation.prepare_interpolation_data import *
from interpolation.okriging import *
from interpolation.skriging import *

fname = '/Users/Xiao/lib/gisalgs/data/necoldem.dat'

Z = read_data(fname)

hh = 50
lags = range(0, 3000, hh)
gamma = semivar(Z, lags, hh)
covariance = covar(Z, lags, hh)

Z1 = np.array(Z)
semivariogram = fitsemivariogram(Z1, gamma, spherical)

x = Point(337000, 4440911)
P1 = prepare_interpolation_data(x, Z1)[0]
print okriging(np.array(P1), semivariogram)[0:2]

x = Point(Z1[0,0], Z1[0,1])
P1 = prepare_interpolation_data(x, Z1)[0]
print okriging(np.array(P1), semivariogram)[0:2]
```

Features in the kriging functions are adopted from the [geostatsmodels](https://github.com/cjohnson318/geostatsmodels) by cjohnson318.
