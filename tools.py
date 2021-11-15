# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


def SAFE2band(SAFE_path, band_nb, resolution):
    """
    Look for granule path name.

    Parameters
    ----------
    SAFE_path : STR
        Path name to .SAFE folder.
    band_nb : STR
        Number of band selected, such as "B02", "B8A", etc.
    resolution : INT
        Selected resolution (10 or 20).

    Returns
    -------
    rasterfn : str
        Path to selected band.

    """
    import os 
    import glob

    granule_path = os.path.join(SAFE_path, "GRANULE") #go to granule path
    os.chdir(granule_path) #work in granule path
    list_L2A = glob.glob("L2A*") #look for folders begining by "L2A"
    suffix = list_L2A[0] + r"\IMG_DATA\R" + resolution + "m"
    resolution_path = os.path.join(granule_path, suffix)
    os.chdir(resolution_path) #work in the granule path
    band_list = glob.glob("*{0}_{1}m.jp2".format(band_nb, resolution))
    rasterfn = os.path.join(resolution_path, band_list[0])
    return rasterfn 

def raster2array(rasterfn):
    """
    Convert raster to array object.

    Parameters
    ----------
    rasterfn : STR
        Raster path.

    Returns
    -------
    array : NUMPY ARRAY
        Selected raster converted to array.

    """
    from osgeo import gdal
    import numpy.ma as ma
    
    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    array = band.ReadAsArray()/10000
    array = ma.masked_where(array == 0, array) #0 is reserved for NO_DATA
    return array

def array2raster(out_fn, resolution, array, granule_path):
    """
    Convert array to raster georeferenced.

    Parameters
    ----------
    out_fn : STR
        Path name of the final raster.
    resolution : INT
        Pixel width or height in m.
    array : NUMPY ARRAY
        Array to convert as raster.
    granule_path: STR
        Path name of the input granule.
    

    Returns
    -------
    None.

    """
    import os
    import glob
    import xml.etree.ElementTree as ET
    from osgeo import gdal, osr

    #reverse array (Numpy does not take same origin pixel)
    reversed_arr = array[::-1]
    cols = reversed_arr.shape[1]
    rows = reversed_arr.shape[0]
    
    #define raster origins from xml file
    os.chdir(granule_path)
    list_L2A = glob.glob("L2A*") #fetch folders begining by "L2A"
    suffix = os.path.join(list_L2A[0], "MTD_TL.xml")
    xml_path = os.path.join(granule_path, suffix)
    tree = ET.parse(xml_path)
    root = tree.getroot() #return the root element of the file
    ULX = int(root.findall(".//ULX")[0].text) #return X origin of image
    ULY = int(root.findall(".//ULY")[0].text) #return Y origin of image

    #create raster and set its spatial references
    driver = gdal.GetDriverByName('GTiff') #raster format selected
    out_raster = driver.Create(out_fn, cols, rows, 1, gdal.GDT_Float32)
    out_raster.SetGeoTransform((ULX, resolution, 0, ULY, 0, resolution))
    outband = out_raster.GetRasterBand(1)
    outband.WriteArray(reversed_arr)
    outband.SetNoDataValue(-9999)
    out_rasterSRS = osr.SpatialReference()
    out_rasterSRS.ImportFromEPSG(32742)
    out_raster.SetProjection(out_rasterSRS.ExportToWkt())
    outband.FlushCache()
    

