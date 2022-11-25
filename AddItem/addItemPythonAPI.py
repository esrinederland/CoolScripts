# adding items to ArcGIS Online using the Python API
import arcgis
import os

fileFolder = r"D:\Data"
fileName = "uploadFile.geojson"
fileType = "GeoJson"

gis = arcgis.GIS("Home")
filePath = os.path.join(fileFolder, fileName)
title = os.path.splitext(fileName)[0]
itemProperties={'type':fileType,
                'title':title,
                'description':'GeoJson with polygon data',
                'tags':'python, geojson, polygons'}

addedItem = gis.content.add(item_properties=itemProperties, data=filePath)
print(addedItem)