# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 10:26:48 2021

@author: 22007604
"""
import os
import glob

if __name__ == "__main__":
    
    wd = r"E:\Kelp"
    os.chdir(wd)
    
#%%
    from tools import SAFE2band, raster2array, array2raster
    from index import ndvi, kelpDiff, floatAlgae
    
#%%
    
    data_wd = os.path.join(wd, "Data")
    year_study = ["2018", "2021"]
    
    os.chdir(data_wd)
    year_list = glob.glob("*") 
    
    for year in year_list:
        if year in year_study:
            year_fd = os.path.join(data_wd,year) #fd : folder
            os.chdir(year_fd)
            
            #open image Sentinel-2
            S2_list = glob.glob("*.SAFE")
            print("There are %s Sentinel-2 tiles in %s."%(len(S2_list),year))
            
            for S2_safe in S2_list:
                #define .SAFE path name
                SAFE_path = os.path.join(year_fd,S2_safe)
                granule_path = os.path.join(SAFE_path, "GRANULE")
                
                #define band path name and open raster
                B4_20m_fn = SAFE2band(SAFE_path, "B04", "20")
                B4_20m = raster2array(B4_20m_fn)
                
                B6_20m_fn = SAFE2band(SAFE_path, "B06", "20")
                B6_20m = raster2array(B6_20m_fn)
                
                B7_20m_fn = SAFE2band(SAFE_path, "B07", "20")
                B7_20m = raster2array(B7_20m_fn)
                
                B8A_20m_fn = SAFE2band(SAFE_path, "B8A", "20")
                B8A_20m = raster2array(B8A_20m_fn)
                
                B11_20m_fn = SAFE2band(SAFE_path, "B11", "20")
                B11_20m = raster2array(B11_20m_fn)
                
                #apply mask
                
                #compute index
                ndvi_20m = ndvi(B4_20m, B7_20m)
                kd_20m = kelpDiff(B4_20m, B6_20m)
                FAI_20m = floatAlgae(B4_20m, B8A_20m, B11_20m)

                #create a folder containing results
                result_path = os.path.join(year_fd, "Results")
                if not os.path.exists(result_path):
                    os.mkdir(result_path)
                date_path = os.path.join(result_path, S2_safe[15:17] + 
                                         "-" + S2_safe[17:19])
                if not os.path.exists(date_path):
                    os.mkdir(date_path)
                
                #save index products as rasters
                out_fn = os.path.join(date_path, 'S2_ndvi_20m.tif')
                array2raster(out_fn, 20, ndvi_20m, granule_path)
                
                out_fn = os.path.join(date_path, 'S2_kd_20m.tif')
                array2raster(out_fn, 20, kd_20m, granule_path)
                
                out_fn = os.path.join(date_path, 'S2_FAI_20m.tif')
                array2raster(out_fn, 20, FAI_20m, granule_path)
                
