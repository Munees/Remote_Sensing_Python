__author__ = 'munees'
from osgeo import  gdal
import numpy as np
import os
import fnmatch
import ogr
import subprocess
import gdal2xyz


def convert_raster_to_CSV(input_folder, output_folder,raster_extension='*.tif', band=1):
    files_list = os.listdir(input_folder)
    for item in files_list:
        if fnmatch.fnmatch(item, raster_extension):
            print "processing %s" %item
            in_raster = input_folder + '/' + item
            out_csv_file = output_folder + '/' + item + '.csv'
            gdal2xyz.gdal2xyz(srcfile=in_raster, dstfile=out_csv_file)

convert_raster_to_CSV(input_folder='/media/munees/New Volume2/NDVI3g/output/clipped', output_folder='/media/munees/New Volume2/NDVI3g/output/clipped/1980')