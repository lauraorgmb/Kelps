# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 10:02:29 2021

@author: 22007604
"""

import numpy as np

def ndvi(RED, NIR):
    ndvi = (NIR - RED) / (RED + NIR)
    return ndvi