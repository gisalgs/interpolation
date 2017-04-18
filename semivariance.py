import numpy as np
from math import sqrt

def distance(a, b):
    """
    Computes distance between points a and b
    Input
      a: a list of [X, Y]
      b: a list of [X, Y]
    Output
      Distance between a and b
    """
    d = (a[0]-b[0])**2 + (a[1]-b[1])**2
    return sqrt(d)

def semivar(z, lags, hh):
    """
    Calculates empirical semivariance from data
    Input:
      z    - a list or 2-D NumPy array,
             where each element has X, Y, Value
      lags - distance bins in 1-D array
      hh   - half of the bin size in distance
    Output:
      A 2-D array of [ [h, gamma(h)], ...]
    """
    semivariance = []
    N = len(z)
    D = [[distance(z[i][0:2], z[j][0:2])
          for i in range(N)] for j in range(N)]
    for h in lags:
        gammas = []
        for i in range(N):
            for j in range(N):
                if D[i][j] >= h-hh and D[i][j]<=h+hh:
                    gammas.append((z[i][2]-z[j][2])**2)
        if len(gammas)==0:
            gamma = 0
        else:
            gamma = np.sum(gammas) / (len(gammas)*2.0)
        semivariance.append(gamma)
    semivariance = [ [lags[i], semivariance[i]]
                     for i in range(len(lags))
                     if semivariance[i]>0]
    return np.array(semivariance).T
