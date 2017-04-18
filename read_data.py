def read_data(fname):
    """
    Reads in data from a file. Each line in the file must have
    three columns: X, Y, and Value.

    Input
      fname: name of and path to the file
    Output
      x3: list of lists with a dimension of 3 x n
          Each inner list has 3 elements: X, Y, and Value
    """
    f = open(fname, 'r')
    x1 = f.readlines()
    x2 = [x.strip().split() for x in x1]
    x3 = [[float(x[0]),float(x[1]),float(x[2])] for x in x2]
    return x3
