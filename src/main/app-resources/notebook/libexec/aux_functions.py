#!/opt/anaconda/bin/python

import sys
import os
import string
import numpy as np
from osgeo import gdal, ogr, osr

def matrix_sum(mat1, mat2, no_data_value=None):
    if no_data_value is not None:
        if not isinstance(mat1, int):
            mat1[(mat1 == no_data_value)] = 0
        if not isinstance(mat2, int):
            mat2[(mat2 == no_data_value)] = 0
    return mat1 + mat2

def write_output_image(filepath, output_matrix, image_format, data_format, output_projection=None, output_geotransform=None, mask=None, no_data_value=None):
    
    driver = gdal.GetDriverByName(image_format)
    out_rows = np.size(output_matrix, 0)
    out_columns = np.size(output_matrix, 1)
    if mask is not None:
        output = driver.Create(filepath, out_columns, out_rows, 2, data_format)
        mask_band = output.GetRasterBand(2)
        mask_band.WriteArray(mask)
    else:
        output = driver.Create(filepath, out_columns, out_rows, 1, data_format)
        
    if output_projection is not None:
        output.SetProjection(output_projection)
    if output_geotransform is not None:
        output.SetGeoTransform(output_geotransform)
    
    raster_band = output.GetRasterBand(1)
    if no_data_value is not None:
        raster_band.SetNoDataValue(no_data_value)
    raster_band.WriteArray(output_matrix)
    gdal.Warp(filepath, output, format="GTiff", outputBoundsSRS='EPSG:4326', xRes=output_geotransform[1], yRes=-output_geotransform[5], targetAlignedPixels=True)
    
    output.FlushCache()
    
def calc_average(matrix_list, n_years):
    if not isinstance(matrix_list, list):
        return 0
    result = matrix_list[0]
    for i in range(1, n_years):
        result = matrix_sum(result, matrix_list[i])
    
    return np.divide(result, (n_years*1.00))

def get_matrix_list(image_list):
    mat_list = []
    for img in image_list:
        dataset = gdal.Open(img)
        product_array = dataset.GetRasterBand(1).ReadAsArray()
        mat_list.append(product_array)
        dataset = None
    return mat_list