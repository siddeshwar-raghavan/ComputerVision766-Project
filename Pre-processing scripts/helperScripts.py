# **Siddeshwar Raghavan**
# Helper functions
#Visualize SAR layers
import os
import rasterio as rio
import earthpy as et
import rasterio.features
import rasterio.warp
from matplotlib import pyplot
def visualizer(filePath):
	dataset = rasterio.open(filePath)
	for i in range (0, dataset.count):
    	pyplot.imshow(dataset.read(i+1), cmap='copper')
    	pyplot.show()

#Create own test and train sets
# mainDir = '/Volumes/SIDD/CV Project/train/AOI_11_Rotterdam/geojson_buildings/'
# compareToDir = '/Volumes/SIDD/CV Project/train/AOI_11_Rotterdam/ValidateSAR/'
# destDir = '/Volumes/SIDD/CV Project/train/AOI_11_Rotterdam/final_geojson_buildings/'
# fileName = '/Volumes/SIDD/CV Project/train/AOI_11_Rotterdam/geojson_buildings/SN6_Train_AOI_11_Rotterdam_Buildings_'
def fileSplitAndMove(mainDir, compareToDir, destDir, fileName):
	l=[]

	for item in os.listdir(mainDir):
	    if not item.startswith('.') and os.path.isfile(os.path.join(mainDir, item)):
	        l.append(item)
	print(len(l))
	m = os.listdir(compareToDir)
	li=[x.split('.')[0] for x in l]
	mi=[x.split('.')[0] for x in m]
	filesToCopyGeo = []
	filesToCopySAR = []
	s='_'


	for i in range(0, len(li)):
	    fileCore = li[i].split('_')
	    joinStr = [fileCore[6],fileCore[7],fileCore[8],fileCore[9]]
	    filesToCopyGeo.append(s.join(joinStr))
	    
	for j in range(0, len(mi)):
	    fileCore = mi[j].split('_')
	    joinStr = [fileCore[6],fileCore[7],fileCore[8],fileCore[9]]
	    filesToCopySAR.append(s.join(joinStr))


	result = list((Counter(filesToCopyGeo) - Counter(filesToCopySAR)).elements())
	print(len(result))
	for i in result:
	    strJoin = fileName+i+'.geojson'
	    shutil.copy(strJoin, destDir)

#Create validation (test) sets for SAR and optical images
#create directory for validation set SAR and EO
import os
import glob
import errno
import shutil
def createValidationSets():
	sarDir = 'validateSAR'
	eoDir = 'validateEO'

	parentDir = '/Volumes/SIDD/CV Project/train/AOI_11_Rotterdam/'

	currDirectorySAR = '/Volumes/SIDD/CV Project/train/AOI_11_Rotterdam/SAR-Intensity/*'
	currDirectoryEO = '/Volumes/SIDD/CV Project/train/AOI_11_Rotterdam/PS-RGB/*'
	joinSAR = '/Volumes/SIDD/CV Project/train/AOI_11_Rotterdam/SAR-Intensity/SN6_Train_AOI_11_Rotterdam_SAR-Intensity_'
	joinEO = '/Volumes/SIDD/CV Project/train/AOI_11_Rotterdam/PS-RGB/SN6_Train_AOI_11_Rotterdam_PS-RGB_'
	destDirectorySAR = '/Volumes/SIDD/CV Project/train/AOI_11_Rotterdam/validateSAR/'
	destDirectoryEO = '/Volumes/SIDD/CV Project/train/AOI_11_Rotterdam/validateEO/'
	filesToCopy = []
	s = '_'

	pathSAR = os.path.join(parentDir, sarDir)
	pathEO = os.path.join(parentDir, eoDir)
	try:
	    os.mkdir(pathSAR) 
	    os.mkdir(pathEO) 
	except OSError as e:
	    if e.errno != errno.EEXIST:
	        print ('error')

	filenameSAR = []
	filenameEO = []
	for name in glob.glob(currDirectorySAR):
	    filenameSAR.append(os.path.basename(name))
	for name in glob.glob(currDirectoryEO):
	    filenameEO.append(os.path.basename(name))

	for i in range(0,299):
	    fileCore = filenameSAR[i].split('_')
	    joinStr = [fileCore[6],fileCore[7],fileCore[8],fileCore[9]]
	    filesToCopy.append(s.join(joinStr))
	    
	for i in range(0,299):
	    s1 = joinSAR+filesToCopy[i]
	    s2 = joinEO+filesToCopy[i]
	    newPath1 = shutil.copy(s1,destDirectorySAR)
	    newPath2 = shutil.copy(s2,destDirectoryEO) 

