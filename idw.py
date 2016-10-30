def IDW(Z, b):
    """
    Inverse distance weighted interpolation.
    Input
      Z: a list of lists where each element list contains 
         four values: X, Y, Value, and Distance to target
          point. Z can also be a NumPy 2-D array.
      b: power of distance
    Output
      Estimated value at the target location.
    """
    zw = 0.0                # sum of weighted z
    sw = 0.0                # sum of weights
    N = len(Z)              # number of points in the data
    for i in range(N):
        d = Z[i][3]
        if d == 0:
            return Z[i][2]
        w = 1.0/d**b
        sw += w
        zw += w*Z[i][2]
    return zw/sw
