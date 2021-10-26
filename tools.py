# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from osgeo import gdal, osr
import numpy.ma as ma


def raster2array(rasterfn):
    """
    Convert raster to array object.

    Parameters
    ----------
    rasterfn : str
        Raster path.

    Returns
    -------
    array : array
        Selected raster converted to array.

    """
    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    array = band.ReadAsArray()
    array = ma.masked_where(array == 0, array)
    return array

def array2raster(out_fn, raster_origin, pixel_width, pixel_height, array):
    """
    Convert array to raster georeferenced.

    Parameters
    ----------
    out_fn : str
        Raster path.
    raster_origin : tuple
        Coordinates of left-upper pixel.
    pixel_width : INT
        Pixel width in m.
    pixel_height : INT
        Pixel Height in m.
    array : numpy array
        Array to convert in raster.

    Returns
    -------
    None.

    """
    #reverse array (Python does not take same origin pixel)
    reversed_arr = array[::-1]
    cols = reversed_arr.shape[1]
    rows = reversed_arr.shape[0]
    origin_x = raster_origin[0] #select raster origin
    origin_y = raster_origin[1]
    driver = gdal.GetDriverByName('GTiff') #raster format selected
    out_raster = driver.Create(out_fn, cols, rows, 1, gdal.GDT_Float32)
    out_raster.SetGeoTransform((origin_x, pixel_width, 0,
                                origin_y, 0, pixel_height))
    outband = out_raster.GetRasterBand(1)
    outband.WriteArray(reversed_arr)
    outband.SetNoDataValue(-9999)
    out_rasterSRS = osr.SpatialReference()
    out_rasterSRS.ImportFromEPSG(32629)
    out_raster.SetProjection(out_rasterSRS.ExportToWkt())
    outband.FlushCache()
