import os
import time
from osgeo import ogr
from osgeo import osr
#import pandas as pd

def reprojectShp2Shp(inShapefile, outLayerPath
              , OutPutProjection=3035
              , LayerName="DummyLayerName"
              , ReturnProjectionTransform=False):
    
    
    # set geometry type before you run the program: wkbLineString, wkbPolygon, ...
    # print("GDAL")
    driver = ogr.GetDriverByName('ESRI Shapefile')

    # get the input layer
    inDataSet = driver.Open(inShapefile)
    inLayer = inDataSet.GetLayer()
    # input SpatialReference
    # REMOVE if Working inSpatialRef = osr.SpatialReference()
    # REMOVE if Working inSpatialRef.ImportFromEPSG(4258)
    inSpatialRef = inLayer.GetSpatialRef()
    

    # output SpatialReference
    outSpatialRef = osr.SpatialReference()
    outSpatialRef.ImportFromEPSG(OutPutProjection)

    # create the CoordinateTransformation
    flag = False
    if inSpatialRef != outSpatialRef:
        flag = True
        coordTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)
    
    if ReturnProjectionTransform == True:
        return coordTrans
    
    else:
        # create the output layer
        outputShapefile = outLayerPath
        if os.path.exists(outputShapefile):
            driver.DeleteDataSource(outputShapefile)
        outDataSet = driver.CreateDataSource(outputShapefile)
        outLayer = outDataSet.CreateLayer(LayerName, outSpatialRef, geom_type=ogr.wkbPolygon)
        
    
        # add fields
        inLayerDefn = inLayer.GetLayerDefn()
        for i in range(0, inLayerDefn.GetFieldCount()):
            fieldDefn = inLayerDefn.GetFieldDefn(i)
            outLayer.CreateField(fieldDefn)
        
        
        # get the output layer's feature definition
        outLayerDefn = outLayer.GetLayerDefn()
    
        # loop through the input features
        inFeature = inLayer.GetNextFeature()
        while inFeature:
            # get the input geometry
            geom = inFeature.GetGeometryRef()
            #x = geom.Centroid().GetX()
            #y = geom.Centroid().GetY()
            # reproject the geometry
            if flag:
                # change projection of the geometry
                geom.Transform(coordTrans)
            # create a new feature
            outFeature = ogr.Feature(outLayerDefn)
            # set the geometry and attribute
            outFeature.SetGeometry(geom)
            for i in range(0, outLayerDefn.GetFieldCount()):
                outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(), inFeature.GetField(i))
            # add the feature to the shapefile
            outLayer.CreateFeature(outFeature)
            # dereference the features and get the next input feature
            
    
            inFeature = inLayer.GetNextFeature()
        outFeature = None
    
        
        # Save and close the shapefiles
        inDataSet = None
        #If not set to None, dataset will not be saved (?)
        outDataSet = None

        return
    
if __name__ == "__main__":
    start = time.time()
    layers = ['NUTS_BN_01M_2013']
    inputFolder = "/home/simulant/ag_lukas/personen/Mostafa/Frankfurt Buildingblocks/"
    outputFolder = "/home/simulant/ag_lukas/personen/Mostafa/Frankfurt Buildingblocks/"
    for i in range(len(layers)):
        inShapefile = inputFolder + layers[i] + '.shp'
        outLayerPath = outputFolder + layers[i] + '_3035.shp'
        reprojectShp2Shp(inShapefile, outLayerPath)
    print(time.time() - start)