#-------------------------------------------------------------------------------
# Name:        SinglePostAddWithAttachments
# Purpose:     Example that shows how to add featurse with attachments to a 
#              FeatureService with one call to the edit_features() method.
#
# Author:      EsriNL DevTeam (MVH)
#
# Created:     20211104
# Copyright:   (c) Esri Nederland 2021
# Licence:     MIT License
#-------------------------------------------------------------------------------
import arcgis
import base64
import uuid
from LogUtils import *

_logFilePath = ""
_gisProfileName = ""
_featureServiceUrl = ""


def main():
    ConfigureLogging(_logFilePath)
    # Create ArcGIS features
    LogInfo("Creating features")
    # Creating global id to use in the feature as well as by the attachments
    globalid1 = str(uuid.uuid4())
    globalid2 = str(uuid.uuid4())

    # Creating the features using the global id
    features = [
        {
            "geometry": {"x": 6.1, "y": 52.5, "spatialReference": {"wkid": 4326}},
            "attributes": {
                "TYPE": "CharlesPoint",
                "NAME": "This is a random point1",
                "GlobalID": globalid1,
            },
        },
        {
            "geometry": {"x": 5.94, "y": 52.95, "spatialReference": {"wkid": 4326}},
            "attributes": {
                "TYPE": "CharlesPoint",
                "NAME": "This is a random point2",
                "GlobalID": globalid2,
            },
        },
    ]

    # create the info for the attachments using the global id from the features as parentGlobalID
    attachmentInfo = {
        "adds": [
            {
                "contentType": "image/jpg",
                "name": "1.jpg",
                "data": getBase64FromFile(r"D:\temp\1.jpg"),
                "globalId": str(uuid.uuid4()),
                "parentGlobalId": globalid1,
            },
            {
                "contentType": "image/jpg",
                "name": "2.jpg",
                "data": getBase64FromFile(r"D:\temp\2.jpg"),
                "globalId": str(uuid.uuid4()),
                "parentGlobalId": globalid1,
            },
            {
                "contentType": "image/jpg",
                "name": "3.jpg",
                "data": getBase64FromFile(r"D:\temp\3.jpg"),
                "globalId": str(uuid.uuid4()),
                "parentGlobalId": globalid2,
            }
        ]
    }

    # create GIS
    LogInfo("Creating GIS")
    gis = arcgis.GIS("https://www.arcgis.com", profile=_gisProfileName)

    # create FeatureLayer
    LogInfo("Creating FeatureLayer")
    fl = arcgis.features.FeatureLayer(url=_featureServiceUrl)

    # Add features and attachments in one call, with the use_global_ids parameter set to True
    LogInfo("Adding features")
    result = fl.edit_features(
        adds=features, attachments=attachmentInfo, use_global_ids=True
    )
    LogDebug(f"result:{result}")
    LogInfo("Script complete")


def getBase64FromFile(filepath):
    """
    Reads a file and returns the base64 encoded string
    """
    LogDebug(f"getBase64FromFile::filepath:{filepath}")
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

if __name__ == "__main__":
    main()