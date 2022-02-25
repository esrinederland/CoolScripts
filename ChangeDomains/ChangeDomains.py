#-------------------------------------------------------------------------------
# Name:        ChangeDomains.py
# Purpose:     Demo to show how to update a coded domain with new values through the REST API
#
# Author:      EsriNL DevTeam (MVH)
#
# Created:     20220224
# Copyright:   (c) Esri Nederland 2022
# Licence:     MIT License
#-------------------------------------------------------------------------------

import requests
import json

_featureLayerUrl = "<<YourFeatureLayerUrl>>"
_fieldName = "<<YourFieldName>>"
_csvFile = "newvaluesList.csv"

def main():
    #get a token to access the REST API (this is not in this script)
    token = GetToken()

    #to get the current coded domain first get the infor from the service
    print("Getting service info")    
    layerInfoUrl = "{}?f=json&token={}".format(_featureLayerUrl,token)
    layerInfo = requests.get(layerInfoUrl).json()

    #get the current field definition from the service
    currentField = [field for field in layerInfo["fields"] if field["name"]==_fieldName][0]
    print("Currently field {} has {} domain values".format(_fieldName,len(currentField["domain"]["codedValues"])))
    
    #open the CSV file and read all the values
    f = open(_csvFile,"r")
    lines = f.readlines()
    #define the new coded values list
    newCodedValues = []
    for line in lines:
        #for everyline in the CSV file file create a new dictionary with a code (the actual value in the DB) and a name (the value to show in the UI)
        parts = line.split(",")
        newCodedValues.append({"code":parts[0],"name":parts[1].strip()})

    #update the coded values in the field definition
    currentField["domain"]["codedValues"] = newCodedValues
    
    #update the field definition through the admin part of t FeatureService, to get to the admin part, replace the /rest/services/ with /rest/admin/services/
    layerUpdateUrl = f'{_featureLayerUrl.replace("/rest/services/"," /rest/admin/services/")}/updateDefinition'

    print(f"Updating field {_fieldName} to have  {len(newCodedValues)} domain values")
    params = {"f":"json","token":token}
    #the update defintion is a json string with the field definition
    params["updateDefinition"] = json.dumps({"fields":[currentField]})
    
    layerResult = requests.post(layerUpdateUrl,params).json()
    print(layerResult)

    print("script complete")



if __name__=="__main__":
    main()
