# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 10:26:48 2021

@author: 22007604
"""
import os
import glob

if __name__ == "__main__":

#%% Definition of parameters
    wd = r"E:\Kelp\Data"
    year_study = ["2018", "2021"]
    
#%%
    from tools import SAFE2band, raster2array
    os.chdir(wd)
    year_list = glob.glob() 
    
    for year in year_list:
        if year in year_study:
            print(year)
            year_fd = os.path.join(wd,year) #fd : folder
            os.chdir(year_fd)
            
            #open image Sentinel-2
            S2_list = glob.glob("*.SAFE")
            print("There are %s Sentinel-2 tiles in %s."%(len(S2_list),year))
            
            for S2_safe in S2_list:
                
                #define .SAFE path name
                SAFE_path = os.path.join(year_fd,S2_safe)
                
                #define band path name and open raster
                B4_20m_fn = SAFE2band(SAFE_path, "B04", "20m")
                B4_20m = raster2array(B4_20m_fn)
                
                B7_20m_fn = SAFE2band(SAFE_path, "B07", "20m")
                B7_20m = raster2array(B7_20m_fn)
                
                #apply mask
                
                #compute index
                ndvi = ndvi(B7_20m, B4_20m)
