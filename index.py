# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 10:02:29 2021

@author: 22007604
"""

def ndvi(RED, NIR):
    import numpy.ma as ma
    import matplotlib.pyplot as plt
    
    ndvi = (NIR - RED) / (RED + NIR)
    ndvi = ma.masked_greater(ndvi, 1)
    plt.imshow(ndvi)
    plt.colorbar()
    plt.show()

    return ndvi

def kelpDiff(RED, RED_EDGE2):
    import numpy.ma as ma
    import matplotlib.pyplot as plt
    
    kd = RED_EDGE2 - RED
    kd = ma.masked_greater(kd, 1)
    plt.imshow(kd)
    plt.colorbar()
    plt.show()
    
    return kd

def floatAlgae(REDrc, NIRrc, SWIRrc):
    """
    

    Parameters
    ----------
    REDrc : NUMPY ARRAY
        Rayleigh TOA reflectance in red band.
    NIRrc : NUMPY ARRAY
        Rayleigh TOA reflectance in nir band.
    SWIRrc : NUMPY ARRAY
        Rayleigh TOA reflectance in swir band.

    Returns
    -------
    FAI : NUMPY ARRAY
        Floating Algae Index array.

    """
    
    rrcNIR = (REDrc * (865 - 1650) + SWIRrc * (665 - 865))/(665-1650)
    FAI = NIRrc - rrcNIR
    
    return FAI
