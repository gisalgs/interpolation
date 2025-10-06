import numpy as np
from .semivariance import distance

def covar(z, lags, hh):
    """
    Calculates empirical covariance from data
    Input:
      z    - a list where each element is a list [x, y, data]
      lags - distance bins in 1-D array
      hh   - half of the bin size in distance
    Output:
      A 2-D array of [ [h, C(h)], ...]
    """
    covariance = []
    N = len(z)
    D = [ [distance(z[i][0:2],z[j][0:2])
           for i in range(N)] for j in range(N)]
    for h in lags:
        C = []
        mu = 0
        for i in range(N):
            for j in range(N):
                if D[i][j] >= h-hh and D[i][j]<=h+hh:
                    C.append(z[i][2]*z[j][2])
                    mu += z[i][2] + z[j][ 2]
        if len(C)==0:
            Ch = 0
        else:
            mu = mu/(2*len(C))
            Ch = np.sum(C) / len(C) - mu*mu
        covariance.append(Ch)
    covariance = [ [lags[i], covariance[i]]
                     for i in range(len(lags))]
    return np.array(covariance).T
