# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 15:11:05 2021

@author: 22007604
"""
#%% CREATE NEW ENVIRONMENT
import os

os.system("conda create -n kelp")
print("""Be careful! The script is now stopped. You have to open Anaconda 
      interface, activate via the interface Kelp environment and 
      INSTALL SPYDER! Otherwise, Gdal will not be functional.
      """)


#%% INSTALL LIBRARIES IN THE NEW ENVIRONMENT 

os.system("conda activate kelp")   

os.system("conda install -c conda-forge gdal")

os.system("conda install -c conda-forge matplotlib")

os.system("conda install -c anaconda pandas")

os.system("conda install -c anaconda scikit-learn")

os.system("conda install -c anaconda lxml")
