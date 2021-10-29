#-------------------------------------------------------------------------------
# Name:        ListInChunks
# Purpose:     CodeSnippet that shows how to split a large list of Features into 
#              a list of smaller lists with the same features
#
# Author:      EsriNL DevTeam (MVH)
#
# Created:     20211022
# Copyright:   (c) Esri Nederland 2021
# Licence:     MIT License
#-------------------------------------------------------------------------------
...

#creating a feature layer based on a url and a previously created arcgis.GIS object
LogInfo("Getting FeatureLayer")
someFeatureLayer = arcgis.features.FeatureLayer(flTargetUrl,gis)

#chopping op a large list of features into a list of lists with a smaller size (chunks)
LogInfo("Creating chunks")
chunkSize = 250

chunks = [features[x:x+chunkSize] for x in range(0, len(features), chunkSize)]

#loop through all the chunks and add the features to the featurelayer
counter = 0
for chunk in chunks:
    counter +=1
    LogInfo(f"Adding chunk {counter} / {len(chunks)}, featureCount: {len(chunk)}")
    try:
        someFeatureLayer.edit_features(adds = chunk)
    except:
        LogException(f"Error adding {chunk}")

LogInfo(f"Insert complete: nrof features created {len(features)}")

...