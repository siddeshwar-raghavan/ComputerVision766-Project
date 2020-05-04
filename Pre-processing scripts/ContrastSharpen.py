# **Siddeshwar Raghavan**
# A script to change contrast and sharpen images with BM3D filtering

import cv2
import os
import shutil
import numpy as np
import gdal
import copy
import tqdm
import bm3d
from tqdm import tnrange
from scipy import ndimage

def filterContrast(sLayers):
    optimg=copy.copy(sLayers[:]) 
    for i in range(len(sLayers)):
        copySAR = copy.copy(sLayers[:][i])
        sarArrayI = np.array(copySAR)
#         optimg[i] = cv2.equalizeHist(sarArrayI.astype(np.uint8))
        clahe = cv2.createCLAHE(clipLimit=300.0, tileGridSize=(8,8))
        cl1 = clahe.apply(sarArrayI.astype(np.uint8))
        optimg[i] = cl1
    return(optimg)

def filterSharpen(sLayers):
    ker = np.array([[0, -1, 0], 
                   [-1, 5,-1], 
                   [0, -1, 0]])
    optimg=copy.copy(sLayers[:]) 
    for i in range(len(sLayers)):
        copySAR = copy.copy(sLayers[:][i])
        sarArrayI = np.array(copySAR)
        denoised_image = bm3d.bm3d(sLayers[i], sigma_psd=4, stage_arg=bm3d.BM3DStages.HARD_THRESHOLDING)
        x = ndimage.convolve(denoised_image, ker)
        optimg[i] = x
    return(optimg)
    

def openSAR(sLayers):
    return(sLayers)

#Code to copy in folders
#change these 3 folders for it to run
dirSAR = '/Users/siddeshwarraghavan/Desktop/CV project files/data/SAR-Intensity/x4/'
joinSAR = '/Users/siddeshwarraghavan/Desktop/CV project files/data/SAR-Intensity/x4/SN6_Train_AOI_11_Rotterdam_SAR-Intensity_'
outputPath = '/Users/siddeshwarraghavan/Desktop/CV project files/data/sharpenbm3d/xf4/'
for data_file in tqdm.tqdm(os.listdir(dirSAR)):
    if not data_file.startswith('.'):
        data = data_file.split('_')
        #print(data_file)
        joinStr = [data[6],data[7],data[8],data[9]]
        joinedName = '_'.join(joinStr)
        imgSAR = joinSAR+joinedName
        SARt = gdal.Open(imgSAR)
        SAR = SARt.ReadAsArray()
        ds = SARt #original SAR image with 4 bands, using for Geo information
        output = filterSharpen(SAR) #processing the SAR images
        os.chdir(outputPath) 
        filename = 'sharp_bm3d_'+joinedName
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