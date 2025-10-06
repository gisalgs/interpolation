import numpy as np
from .semivariance import distance

def okriging(Z, model):
    """
    Ordinary kriging.
    Input
      Z: an array of [X, Y, Val, Distance to x0]
      model: the name of fitted semivariance model
    Output
      zhat: estimated value at x0
      sigma: standard error
      mu: estimated mean
      w: weights
    """
    N = len(Z)                          # number of points
    k = model(Z[:,3])                   # get [gamma(xi, x0)]
    k = np.matrix(k).T                  # k is a 1xN matrix
    k1 = np.matrix(1)
    k = np.concatenate((k, k1), axis=0) # add a new row of 1s
    K = [ [distance(Z[i][0:2],Z[j][0:2])
           for i in range(N)] for j in range(N)]
    K = np.array(K)                     # list -> NumPy array
    K = model(K.ravel())                # [gamma(xi, xj)]
    K = np.matrix(K.reshape(N, N))      # array -> NxN matrix
    ones = np.matrix(np.ones(N))        # Nx1 matrix of 1s
    K = np.concatenate((K, ones.T), axis=1) # add a col of 1s
    ones = np.matrix(np.ones(N+1))          # (N+1)x1 of 1s
    ones[0, N] = 0.0                        # last one is 0
    K = np.concatenate((K, ones), axis=0)   # add a new row
    w = np.linalg.solve(K, k)               # solve: K w = k
    zhat = (np.matrix(Z[:,2])*w[:-1])[0, 0] # est vlaue
    sigmasq = (w.T * k)[0, 0]               # est error var
    if sigmasq < 0:
        sigma = 0
    else:
        sigma = np.sqrt(sigmasq)            # error
    return zhat, sigma, w[-1][0], w         # est, err, mu, w
