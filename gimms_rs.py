# -*- coding: utf-8 -*-

"""

Created on Sat Jan 31 21:52:23 2015

@author: Zhaofei Wen

Note: The output NDVI value have been multiplied by 1000

"""

# importing modules

from osgeo import gdal

import numpy as np

#projection information
def getPRJwkt(epsg):
    '''Grab an WKT version of an EPSG code
       usage getPRJwkt(4326)
       This makes use of links like
       http://spatialreference.org/ref/epsg/4326/prettywkt/
       need internet to work'''
    import urllib
    f = urllib.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg))
    return(f.read())

# setting pj parameters

transform = (-180.0000000, 0.083333, 0.0,90.00000, 0.0, -0.083333)

# proj = 'GEOGCS["WGS84",DATUM["WGS_1984",\
#
# SPHEROID["WGS84",6378137,298.257223563,\
#
# AUTHORITY["EPSG","7030"]],\
#
# AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],\
#
# UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]'

proj = getPRJwkt(4326)

# read ndvi3g data and reshape it to 2-D array

inds = np.fromfile('/media/munees/New Volume2/NDVI3g/1980/geo81aug15a.n07-VI3g',dtype='>i2') # ‘geo81sep15b’ is the filename of ndvi3g

inds = inds.reshape(4320, 2160)



#transpose (flip and rotate)

ndvi3g = np.transpose(inds)



# retrieve ndvi and flag data

ndvi = np.floor(ndvi3g/10)  # ndvi*1000

flag = ndvi3g-np.floor(ndvi3g/10)*10+1



#output data

fn_ndvi = '/media/munees/New Volume2/NDVI3g/output/ndvi.tif'

fn_flag = '/media/munees/New Volume2/NDVI3g/output/flag.tif'



driver = gdal.GetDriverByName('GTIFF')  # other formats can also be specified here

outndvi = driver.Create(fn_ndvi, 4320,2160, 1, gdal.GDT_Int16)

outflag = driver.Create(fn_flag, 4320,2160, 1, gdal.GDT_Byte)  # 1 <= flagvalue<= 7



bandndvi = outndvi.GetRasterBand(1)

bandndvi.WriteArray(ndvi, 0, 0)

bandndvi.FlushCache()

bandndvi.SetNoDataValue(-9999)

bandndvi.GetStatistics(0, 1)



bandflag = outflag.GetRasterBand(1)

bandflag.WriteArray(flag, 0, 0)

bandflag.FlushCache()

bandflag.SetNoDataValue(-9999)

bandflag.GetStatistics(0, 1)



# georeferencing the output images

outndvi.SetGeoTransform(transform)

outndvi.SetProjection(proj)



outflag.SetGeoTransform(transform)

outflag.SetProjection(proj)



# release memory

outndvi = None

outflag = None
