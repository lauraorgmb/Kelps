# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import glob
import os
from xml.dom import minidom
from osgeo import gdal, osr
import numpy.ma as ma

def SAFE2band(SAFE_path, band_nb, resolution):
    """
    Look for granule path name.

    Parameters
    ----------
    SAFE_path : str
        Path name to .SAFE folder.
    band_nb : str
        Number of band selected, such as "B02", "B8A", etc.
    resolution : TYPE
        Selected resolution (10 or 20).

    Returns
    -------
    granule_path : str
        Path to selected granule.

    """
    granule_path = os.path.join(SAFE_path, "GRANULE") #go to granule path
    os.chdir(granule_path) #work in granule path
    list_L2A = glob.glob("L2A*") #look for folders begining by "L2A"
    suffix = list_L2A[0] + r"\IMG_DATA\R" + resolution + "m"
    resolution_path = os.path.join(granule_path, suffix)
    os.chdir(resolution_path) #work in the granule path
    band_suffix = "*" + band_nb + "_" + resolution + "m.jp2"
    band_list = glob.glob(band_suffix)
    band_path = os.path.join(granule_path, band_list[0])
    return band_path 

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
    out_rasterSRS.ImportFromEPSG(32742)
    out_raster.SetProjection(out_rasterSRS.ExportToWkt())
    outband.FlushCache()
    
def get_origin(granule_path):

    list_L2A = glob.glob("L2A*") #look for folders begining by "L2A"
    suffix = os.path.join(list_L2A[0], "MTD_TL.xml")
    xml_path = os.path.join(granule_path, suffix)
    mtd_xml = minidom.parse(xml_path)
    return mtd_xml

