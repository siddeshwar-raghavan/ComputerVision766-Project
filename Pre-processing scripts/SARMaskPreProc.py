import cv2
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
import os
import rasterio
import glob
import errno
import shutil
import tqdm

  #Code to copy in folders
dirSAR = '/Volumes/SIDD/CV Project/train/AOI_11_Rotterdam/finalSAR/'
joinSAR = '/Volumes/SIDD/CV Project/train/AOI_11_Rotterdam/finalSAR/SN6_Train_AOI_11_Rotterdam_SAR-Intensity_'
joinEO = '/Volumes/SIDD/CV Project/train/AOI_11_Rotterdam/finalEO/SN6_Train_AOI_11_Rotterdam_PS-RGB_'
outputPath = '/Volumes/SIDD/CV Project/train/AOI_11_Rotterdam/post_process/'

def getSARmask(SARimg,OPimg):
  refmat=cv2.Canny(cv2.GaussianBlur(OPimg,(5,5),0),100,100) #Basic mask creation
  refmat2=cv2.dilate(refmat,np.ones([10,10]))                 #Dilated mask
  refmat3=((np.array(refmat2))/255)                         #Pushed mask down to 1/0 values
  refmatp=refmat3                                           #Created a positive negative mask pair
  refmatn=refmat3-1
  ker=np.ones([2,2])                                        #kernel
  optimg=SARimg                                             #output
  for i in range(4):
    csar=SARimg[i]
    minam=min(csar[csar>0])                                 #the threshold that we multiply by a ratio
    SAR1=np.array(csar)
    tempt=SAR1
    tempt[np.where(tempt<(1)*minam)]=0                      #all of this is to calculate the normalization value at basically no thresholding
    tempt=cv2.morphologyEx(tempt, cv2.MORPH_OPEN,ker )
    tempt=cv2.medianBlur(tempt,5)
    prodp=np.multiply(tempt,refmatp)
    prodn=np.multiply(tempt,refmatn)
    prodsp1=sum(sum(prodp))
    prodsn1=sum(sum(prodn))                                 #products of positive and negative masks with the temp image
    ratio=1
    negn=-prodsn1
    posn=prodsp1
    breakcount=0
    for k in range(1,30):
      SAR1=np.array(csar)
      tempt=SAR1
      tempt[np.where(tempt<(ratio)*minam)]=0                #recalculate with changing ratio
      tempt=cv2.morphologyEx(tempt, cv2.MORPH_OPEN,ker )
      tempt=cv2.medianBlur(tempt,5)
      prodp=np.multiply(tempt,refmatp)
      prodn=np.multiply(tempt,refmatn)
      prodsp=sum(sum(prodp))
      prodsn=sum(sum(prodn))
      if k==1:
        newp=prodsp/posn+prodsn/negn
        finrat=ratio
        fink=k                                              #initialization
      if newp<prodsp/posn+prodsn/negn:
        newp=prodsp/posn+prodsn/negn
        fink=k
        finrat=ratio                                        #updating ratio
      ratio=ratio+0.08                                      #can tweak this or increase iterations
    ratio=finrat
    SAR1=np.array(csar)
    tempt=SAR1
    tempt[np.where(tempt<(ratio)*minam)]=0
    tempt=cv2.morphologyEx(tempt, cv2.MORPH_OPEN,ker )      #these operations need more looking into for even better performance
    tempt=cv2.medianBlur(tempt,5)
    optimg[i]=tempt
  return(optimg)


for data_file in tqdm.tqdm(os.listdir(dirSAR)):
    data = data_file.split('_')
    joinStr = [data[6],data[7],data[8],data[9]]
    joinedName = '_'.join(joinStr)
    imgSAR = joinSAR+joinedName
    imgEO = joinEO+joinedName
    SARt = gdal.Open(imgSAR)
    SAR=SARt.ReadAsArray()
    opref = cv2.imread(imgEO)
    ds = SARt #original SAR image with 4 bands, using for Geo information
    output=getSARmask(SAR, opref) #processing the SAR images
    os.chdir(outputPath) 
    filename = 'post_process_'+joinedName
    r, c = output[1].shape
    driver = gdal.GetDriverByName("GTiff")
    outdata = driver.Create(filename, c, r, len(output), gdal.GDT_Float32)
    outdata.SetGeoTransform(ds.GetGeoTransform())##sets same geotransform as input 
    outdata.SetProjection(ds.GetProjection())##sets same projection as 

    for i in range(len(output)):

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