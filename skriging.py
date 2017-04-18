import numpy as np
from semivariance import distance

def skriging(Z, mu, model):
    """
    Simple kriging
    Input
      Z: an array of [X, Y, Val, Distance to x0]
      mu: mean of the data
      model: the name of fitted semivariance model
    Output
      zhat: the estimated value at the target location
      sigma: standard error
      w: weights
    """
    N = len(Z)                          # number of points
    k = model(Z[:,3])                   # get [gamma(xi, x0)]
    k = np.matrix(k).T                  # 1xN matrix
    K = [ [distance(Z[i][0:2],Z[j][0:2])
           for i in range(N)] for j in range(N)]
    K = np.array(K)                     # list -> NumPy array
    K = model(K.ravel())                # [gamma(xi, xj)]
    K = np.matrix(K.reshape(N, N))      # array -> NxN matrix
    w = np.linalg.solve(K, k)           # solve K w = k
    R = Z[:,2] - mu                     # get residuals
    zhat = (np.matrix(R)*w)[0, 0]       # est residual
    zhat = zhat + mu                    # est value
    sigmasq = (w.T*k)[0, 0]             # est error variance
    if sigmasq<0:
        sigma = 0
    else:
        sigma = np.sqrt(sigmasq)        # error
    return zhat, sigma, w               # est, error, weights
