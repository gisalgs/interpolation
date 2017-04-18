from osgeo import gdal                 # import GDAL
from random import sample

drv = gdal.GetDriverByName('USGSDEM')  # driver for USGS DEM
drv.Register()                         # must register the driver
fname = "../data/my425de0017.dem"
raster = gdal.Open(fname,
                   gdal.GA_ReadOnly)
raster is not None                     # check if the file is loaded
ncols = raster.RasterXSize             # get raster size in x
nrows = raster.RasterYSize             # get raster size in y
raster.RasterCount                     # get number of bands
geotrans = raster.GetGeoTransform()    # get spatial reference info
ul_x  = geotrans[0]                    # upper left x: -2493045.0
x_res = geotrans[1]                    # west-east pixel resolution
x_rot = geotrans[2]                    # rotation on X, 0 = north up
ul_y  = geotrans[3]                    # upper left y: 4359175.61243151
y_rot = geotrans[4]                    # rotation on Y
y_res = geotrans[5]                    # north-south pixel resolution
band  = raster.GetRasterBand(1)        # this is 1-based

data=band.ReadAsArray(0,0,ncols,nrows) # all into an numpy array (time!)

row0 = 50
row1 = 150
col0 = 250
col1 = 350
sub = []
for r in range(row0, row1):
    r = row1 - r - 1 + row0
    for c in range(col0, col1):
        sub.append([ul_y+y_res*r, ul_x+x_res*c, data[r, c]])
        #print data[r, c],
    # print

#import sys
#sys.exit()

x0 = ul_x+x_res*col0
y0 = ul_y+y_res*row0

samplesize = 250
sampidx = sample(range(len(sub)), samplesize)
samp = [sub[i] for i in sampidx]
for s in samp:
    print s[1], s[0], s[2]


band=None                              # release memory that is not needed
data=None

"""
my425de0017.dem is for Northeast Columbus
I will use a subset 100x100 pixels of the DEM in the middle
and sample them into a point data set. The coordinate of each pixel 
will be used.

rows: 50 - 149
cols: 250 - 349

The data is generated as follows:

$ python gdal_ohio_dem.py > necoldem.dat
$ mv necoldem.dat ../data/

The coordiantes at the top-left corner of the sample area are:
>>> x0
336765.0
>>> y0
4441875.0

This is done in a spreadsheet using formulas:

=(A1-336765)/30+1
=100-(4441875-B1)/30+1

We will use these to get the row/col of each cell in the sampled data.

The three columns in each line of the data are: X, Y, and Elevation.
All in meters.

"""
