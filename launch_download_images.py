###################################################################################################
# Download Raw Imagery
# Benjamin P. Stewart, May 2018
# Purpose: Use the AWS CLI for downloading S3 results 
#   - see the curFolder, imageFolder, and resultsFolder for specific folders to be downloaded
###################################################################################################

import sys, os, inspect
import geojson

import geopandas as gpd

from gbdxtools import Interface
from shapely.geometry import shape

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

sys.path.insert(0, r"C:\Users\WB411133\OneDrive - WBG\AAA_BPS\Code\Code\Github\GOST_GBDx")
from GOST_GBDx_Tools import gbdxTasks
from GOST_GBDx_Tools import gbdxURL_misc
from gbdxtools import CatalogImage
           
#In order for the interface to be properly authenticated, follow instructions here:
#   http://gbdxtools.readthedocs.io/en/latest/user_guide.html
#   For Ben, the .gbdx-config file belongs in C:\Users\WB411133 (CAUSE no one else qill f%*$&ing tell you that)
gbdx = Interface()
curTasks = gbdxTasks.GOSTTasks(gbdx)
gbdxUrl = gbdxURL_misc.gbdxURL(gbdx)

#There are two basic options for downloading Imagery - tasks and CatalogImage
#   Tasks: Run AOP strip processing and Clip raster to mount new imagery to S3
#   CatalogImage: Creates reference to image on IDAHO that can then be written locally
#
#   Use tasks for larger imagery and CatalogImage for smaller samples
initials = "bps" #This is used to create the output S3 folder 
location = "HCMC_PAN" #This is used to create the output S3 folder 
inputShapes = r"Q:\WORKINGPROJECTS\ImageryDownload\Bogota_ForSarah\bogota_AOI.shp"
inD = gpd.read_file(inputShapes)
curWKT = inD.geometry[0]

inImages = ['10400100387BFA00','1040010037B76500','10300100651A0500']
for x in inImages:
    outFile = r"Q:\WORKINGPROJECTS\ImageryDownload\Bogota_ForSarah\%s.tif" % x
    curTasks.downloadImage(x, outFile, curWKT=curWKT)


    
        
'''
###Download imagery using tasks
inShp = gpd.read_file(r"Q:\WORKINGPROJECTS\ImageryDownload\HCMC Admin Unit UTM WGS84\HCMC_province.shp")
if not inShp.crs == {'init': u'epsg:4326'}:
    inShp = inShp.to_crs({'init': 'epsg:4326'})
curWKT = str(inShp.geometry[0])
allTasks = []
for cat_id in inputImages:
    data = gbdx.catalog.get_data_location(cat_id)    
    x = curTasks.downloadAOP(cat_id, "%s/%s/%s" % (initials, location, cat_id), curWKT, band_type="PAN")
    allTasks.append(x)    
for x in allTasks:
    x.execute()
xx = gbdxUrl.monitorWorkflows(sleepTime=120)   


#Download imagery the new, hip way using Catalog Image
outputFolder = r"Q:\AFRICA\LBR\IMAGERY"
inputShapefile = r"Q:\AFRICA\LBR\ADMIN\Greater Monrovia admin boundary\Greater_Monrovia_admin_boundary.shp"
inShp = gpd.read_file(inputShapefile)    
cbbox = [inShp.bounds.minx[0], inShp.bounds.maxy[0], inShp.bounds.maxx[0], inShp.bounds.miny[0]]
for tID in ['1030010051A7CD00', '105041001207E600']:
    curTasks.downloadImage(tID, os.path.join(outputFolder, "%s.tif" % tID), boundingBox=cbbox, panSharpen=False)

#Download Imagery the old fashioned way
allTasks = []
cbbox = "%s,%s,%s,%s" % (inShp.bounds.minx[0], inShp.bounds.maxy[0], inShp.bounds.maxx[0], inShp.bounds.miny[0])
print cbbox

for tID in [['1030010051A7CD00','WORLDVIEW3_VNIR'],['105041001207E600','WORLDVIEW3_VNIR']]: 
    x = curTasks.createWorkflow(tID[0], cbbox, str(inShp.geometry[0]), tID[1], "bps/Monrovia/%s" % tID[0],
                    runCarFinder = 0, runSpfeas = 0, downloadImages = 1,
                    aopPan=True, aopDra=True, aopAcomp=True, aopBands='MS',
                    spfeasParams={"triggers":'dmp fourier gabor grad hog lac mean ndvi pantex saliency sfs', 
                                  "scales":'8 16 32 64', "block":'4'})
    allTasks.append(x)    

print allTasks

#for t in allTasks:
#    t.execute()
xy = allTasks[0].execute()
print xy

xx = gbdxUrl.monitorWorkflows(sleepTime=300)    
for x in xx['FAILED']:
    print x
'''
'''TESTING
gbdx = Interface()
##input shapes 
aligatorPond = [[[-77.607000,17.882000],[-77.528000,17.882000],[-77.531000,17.847000],[-77.605000,17.857000],[-77.607000,17.882000]]]
aligatorImages = ["105001000EA7BD00","105001000CD38A00","104001002238C400","10400100140AA900","10300100335D4500","1050410001F6FE00","101001000368CA00"]

portlandCottage = [[-77.269000,17.758000],[-77.189000,17.686000],[-77.090000,17.736000],[-77.152000,17.797000],[-77.269000,17.758000]]
portlandCottageImages = ["104001003BB30B00","1040010036299300","103001005290E700","1040010010219200","103001002E9EDF00","103001000877A600","1010010004C0E600"]

manchioneal = [[-76.280000,18.036000],[-76.271000,18.035000],[-76.272000,18.052000],[-76.283000,18.052000],[-76.280000,18.036000]]
manchionelImages = ["1030010063104000","1040010024C59400","1050410012158000","103001002FBFDC00","103001000783D500","10100100040ACF00"]

annottoBay = [[-76.796000,18.304876],[-76.798000,18.272000],[-76.755000,18.262000],[-76.748000,18.280000],[-76.796000,18.304876]]
anottoBayImages = ["105001000C399C00","1040010028A82700","10400100191B5000","10400100138E9100","103001002C227300","1030010006A89B00"]

cShape=aligatorPond
images=aligatorImages

inPoly = geojson.Polygon(cShape)
curWKT = shape(inPoly)
for x in images:
    try:
        cImg = CatalogImage(x, pansharpen=False, band_type="MS", acomp=True)
        outImg = cImg.aoi(wkt=str(curWKT))
'''