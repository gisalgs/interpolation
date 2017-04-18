import numpy as np

@np.vectorize
def spherical(h, c0, c, a):
    """
    Input
      h: distance
      c0: sill
      c: nugget
      a: range
    Output
      Theoretical semivariogram at distance h
    """
    if h<=a:
        return c0 + c*(3.0*h/(2.0*a) - ((h/a)**3.0)/2.0)
    else:
        return c0 + c

@np.vectorize
def gaussian(h, c0, c, a):
    """
    Same as spherical
    """
    return c0 + c*(1-np.exp(-h*h/((a)**2)))

@np.vectorize
def exponential(h, c0, c, a):
    """
    Same as spherical
    """
    return c0 + c*(1-np.exp(-h/a))

@np.vectorize
def linear(h, c0, c, a):
    """
    Same as spherical
    """
    if h<=a:
        return c0 + c*(h/a)
    else:
        return c0 + c

def fitsemivariogram(z, s, model, numranges=200):
    """
    Fits a theoretical semivariance model.
    Input
      z:     data, NumPy 2D array, each row has (X, Y, Value)
      s:     empirical semivariances
      model: one of the semivariance models: spherical,
             Gaussian, exponential, and linear
    Output
      A lambda function that serves as a fitted model of
      semivariogram. This function will require one parameter
      (distance).
    """
    c = np.var(z[:,2])          # c, sill
    if s[0][0] is not 0.0:      # c0, nugget
        c0 = 0.0
    else:
        c0 = s[0][1]
    minrange, maxrange = s[0][1], s[0][-1]
    ranges = np.linspace(minrange, maxrange, numranges)
    errs = [np.mean((s[1] - model(s[0], c0, c, r))**2)
            for r in ranges]
    a = ranges[errs.index(min(errs))]  # optimal range
    return lambda h: model(h, c0, c, a)
