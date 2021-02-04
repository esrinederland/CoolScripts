#-------------------------------------------------------------------------------
# Name:        formatEpoch
# Purpose:     to demo the query of datetime from features in an arcgis online 
#              and forat the resulting epoch to a python datetime
#
# Author:      mvanhulzen & mjagt
#
# Created:     04-02-2021
# Copyright:   (c) esri nederland bv 2021
#-------------------------------------------------------------------------------
import requests
import json
import datetime

featureLayerUrl = "https://services9.arcgis.com/kfCU77AsgNn9o1Ff/ArcGIS/rest/services/Datetime_Layer/FeatureServer/0"

def main():
    print("Start datetime query")

    print("sending request")
    queryFeatureUrl = "{}/query".format(featureLayerUrl)
    params = {
        "where":"datum > DATE '2019-01-16' AND Datum < DATE '2019-01-21'",
        "outFields":"Datum",
        "returnGeometry":"false",
        "f":"json"
        }
        
    response = requests.post(queryFeatureUrl,params)

    features = response.json()["features"]

    for feature in features:
        print(PortalTimestampToDate(feature["attributes"]["Datum"]))

    print("script complete")
    
def PortalTimestampToDate(timestamp):
    """This function converts a timestamp from the ArcGIS Rest API to a python datetime"""
    # We get timestamp in milliseconds python expects seconds
    timeStampSeconds = int(timestamp)/1000
    #convert the timeStampSeconds to datetime
    dt = datetime.datetime.fromtimestamp(timeStampSeconds)
    return dt

def DateToPortalTimeStamp(date):
    """This function converts a python datetime to an timestamp from the ArcGIS Rest API"""
    #get the seconds from 19700101
    s = (date - datetime.datetime(1970,1,1)).total_seconds()
    #multiply with 1000 because ArcGIS excpects that
    return s*1000


if __name__ == '__main__':
    main()