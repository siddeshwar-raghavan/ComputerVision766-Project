# **Siddeshwar Raghavan**
#BM3D - process image with two values of standard deviation 0.4 and 4
#Median filter with fixed kernal of size 5
import cv2
import os
import shutil
import numpy as np
import gdal
import copy
import tqdm
import bm3d
from tqdm import tnrange

def filterSAR(sLayers):
    optimg=copy.copy(sLayers[:]) 
    for i in range(len(sLayers)):
        copySAR = copy.copy(sLayers[:][i])
        sarArrayI = np.array(copySAR)
        median = cv2.medianBlur(sarArrayI, 5)
        optimg[i] = median
    return(optimg)

def filterBM3D(sLayers):
    optimg=copy.copy(sLayers[:]) 
    for i in range(len(sLayers)):
        copySAR = copy.copy(sLayers[:][i])
        sarArrayI = np.array(copySAR)
        denoised_image = bm3d.bm3d(sLayers[i], sigma_psd=4, stage_arg=bm3d.BM3DStages.HARD_THRESHOLDING)
        optimg[i] = denoised_image
    return(optimg)
    

#Code to copy in folders
dirSAR = '/Volumes/SIDD/CV Project/train/AOI_11_Rotterdam/finalSAR/'
joinSAR = '/Volumes/SIDD/CV Project/train/AOI_11_Rotterdam/SAR-Intensity/SN6_Train_AOI_11_Rotterdam_SAR-Intensity_'
outputPath = '/Volumes/SIDD/CV Project/train/AOI_11_Rotterdam/filtered/'
for data_file in tqdm.tqdm(os.listdir(dirSAR)):
    if not data_file.startswith('.'):
        data = data_file.split('_')
        joinStr = [data[6],data[7],data[8],data[9]]
        joinedName = '_'.join(joinStr)
        imgSAR = joinSAR+joinedName
        SARt = gdal.Open(imgSAR)
        SAR = SARt.ReadAsArray()
        ds = SARt #original SAR image with 4 bands, using for Geo information
        output = filterBM3D(SAR) #processing the SAR images
        os.chdir(outputPath) 
        filename = 'bm3d_3.8_'+joinedName
        driver = gdal.GetDriverByName("GTiff")
        outdata = driver.Create(filename, 900, 900, 4, gdal.GDT_Float32)
        outdata.SetGeoTransform(ds.GetGeoTransform())##sets same geotransform as input 
        outdata.SetProjection(ds.GetProjection())##sets same projection as 

        for i in range(4):

            arr = output[i]
            rows, cols = arr.shape
            arr_min = arr.min()
            arr_max = arr.max()
            arr_mean = int(arr.mean())
            arr_out = np.where((arr < arr_mean), 10000, arr)

            band = outdata.GetRasterBand(i+1)
            band.WriteArray(arr_out)
            band.SetNoDataValue(10000)##if you want these values transparent

        # outdata.FlushCache()  # Not required!!!
        band = None
        outdata = None
        ds=None 