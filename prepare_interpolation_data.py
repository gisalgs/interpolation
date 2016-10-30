from math import sqrt
def prepare_interpolation_data(x, Z, N=10):
    vals = [z[2] for z in Z]
    mu = sum(vals)/len(vals)
    dist = [sqrt((z[0]-x.x)**2 + (z[1]-x.y)**2) for z in Z]
    Z1 = [(Z[i][0], Z[i][1], Z[i][2], dist[i])
          for i in range(len(dist))]
    Z1.sort(key=lambda Z1: Z1[3])
    Z1 = Z1[:N]
    return Z1, mu
