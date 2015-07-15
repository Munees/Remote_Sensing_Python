__author__ = 'munees'
from osgeo import  gdal
import numpy as np
import os
import fnmatch
import ogr
import subprocess

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

def gimms_to_tiff(input_folder,output_folder,dest_proj=4326):
    '''
    converts gimms vi3g to tiff
    :param input_folder:
    :param output_folder:
    :param dest_proj:
    :return:
    '''
    transform = (-180.0000000, 0.083333, 0.0,90.00000, 0.0, -0.083333)
    proj = getPRJwkt(dest_proj)
    files_list = os.listdir(input_folder)
    for item in files_list:
        print 'processing %s' % item
        inds = np.fromfile(input_folder+item,dtype='>i2')
        inds = inds.reshape(4320, 2160)
        ndvi3g = np.transpose(inds)
        ndvi = np.floor(ndvi3g/10)  # ndvi*1000
        flag = ndvi3g-np.floor(ndvi3g/10)*10+1
        fn_ndvi = output_folder + item + '.tif'
        fn_flag = output_folder + 'flag_' + item + '.tif'
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



def clip_raster_by_vector(input_folder, in_shape, output_folder, file_extension='*.tif', t_srs='EPSG:4326' ):
    files_list = os.listdir(input_folder)
    ds = ogr.Open(in_shape)
    lyr = ds.GetLayer(0)
    lyr.ResetReading()
    ft = lyr.GetNextFeature()
    for item in files_list:
        if fnmatch.fnmatch(item, file_extension):
            print "processing %s" %item
            in_raster = input_folder + '/' + item
            out_raster = output_folder + '/' +'tg_' + item
            subprocess.call(['gdalwarp', in_raster, out_raster, '-cutline', in_shape, '-t_srs', t_srs, '-crop_to_cutline'])





# gimms_to_tiff(input_folder='/media/munees/New Volume2/NDVI3g/1990/',output_folder='/media/munees/New Volume2/NDVI3g/output/1990/', dest_proj=4326)
# print "1990 done"
# gimms_to_tiff(input_folder='/media/munees/New Volume2/NDVI3g/2000/',output_folder='/media/munees/New Volume2/NDVI3g/output/2000/', dest_proj=4326)
# print "2000 done"
# gimms_to_tiff(input_folder='/media/munees/New Volume2/NDVI3g/2010/',output_folder='/media/munees/New Volume2/NDVI3g/output/2010/', dest_proj=4326)
# print "2010 done"

clip_raster_by_vector(input_folder="/media/munees/New Volume2/NDVI3g/output/1980",in_shape="/media/munees/New Volume/Service/Jhagdish/Bhavani/AI_annual/AI_annual/india_semiarid.shp",output_folder="/media/munees/New Volume2/NDVI3g/output/clipped")