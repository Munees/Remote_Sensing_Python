__author__ = 'munees'
from osgeo import  gdal
import numpy as np
import os
import fnmatch
import ogr
import subprocess
import gdal2xyz
import itertools
import csv
import itertools as IT
import pandas as pd
# function to convert raster to csv

def convert_raster_to_CSV(input_folder, output_folder,raster_extension='*.tif', band=1):
    files_list = os.listdir(input_folder)
    for item in files_list:
        if fnmatch.fnmatch(item, raster_extension):
            print "processing %s" %item
            in_raster = input_folder + '/' + item
            out_csv_file = output_folder + '/' + item + '.csv'
            gdal2xyz.gdal2xyz(srcfile=in_raster, dstfile=out_csv_file)


def combine_multiple_csv(input_folder, dst_file,template_file, extension='*.csv'):
    files_list = os.listdir(input_folder)
    dfs = []
    lat_lon_df = pd.read_csv(template_file, header=None)
    lat_lon_df = lat_lon_df.ix[:, :1]
    for item in files_list:
        if fnmatch.fnmatch(item,extension):
            df = pd.read_csv(input_folder +'/'+ item, header=None)
            df = df.ix[:, 2:]
            df.columns = [item[6:14]]
            dfs.append(df)

    merged_df  = pd.concat(dfs, axis=1)
    out_df = pd.concat([lat_lon_df, merged_df], axis=1)
    out_df.to_csv(dst_file, index=None)




# convert_raster_to_CSV(input_folder='/home/kiruba/PycharmProjects/Remote_Sensing_Python/raster', output_folder='/home/kiruba/PycharmProjects/Remote_Sensing_Python/raster')
combine_multiple_csv(input_folder='/home/kiruba/PycharmProjects/Remote_Sensing_Python/raster', dst_file='/home/kiruba/PycharmProjects/Remote_Sensing_Python/combined.csv', template_file='/home/kiruba/PycharmProjects/Remote_Sensing_Python/raster/tg_geo83apr15a.n07-VI3g.tif.csv')