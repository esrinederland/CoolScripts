#-------------------------------------------------------------------------------
# Name:        GetUsage Module
# Purpose:     get ArcGIS Platform usage statistics per API key
# Author:      Esri Nederland: Mark Jagt
# Created:     20211224
# Status:      Production
# Copyright:   (c) Esri Nederland BV 2021
#-------------------------------------------------------------------------------

import arcgis 
import requests
import json
from datetime import datetime, timedelta

_gis = None
#Portal url ("https://www.arcgis.com")
_portalUrl = "https://www.arcgis.com"
_portalUsername = "mjagtDev"

_dateFrom = "2021/01/01"
_dateTo = "2021/12/31"
# _returnPeriod possible values '1d' (day) or '1m' (month)
_returnPeriod = "1m"
_maxNumberOfTries = 10

def main():
    print("Start GetUsage V20211230.01")
    
    try:
        print("Connecting to ArcGIS")
        getGIS(_portalUsername)

        if _gis:
            apiKeyInfos = getApiKeyInfos()
            for apiKeyInfo in apiKeyInfos["results"]:
                apiKeyItemId = apiKeyInfo["id"]
                apiKeyTitle = apiKeyInfo["title"]
                
                registeredAppInfo = getRegisteredAppInfo(apiKeyItemId)
                apiKey = registeredAppInfo["apiKey"]
                apiKeyClientId = registeredAppInfo["client_id"]
                print(f"{apiKeyTitle}:\n\t{apiKey}")
                
                usage = getUsage(apiKeyClientId)
                
                if "totals" in usage and len(usage["totals"]) > 0:
                    for countObject in usage["totals"]:
                        print(f"\t\t{countObject['unit']}\n\t\t\tcount: {countObject['count']}\t| cost($): {countObject['total']}")
                else:
                    print(f"No usage could be determined for API key '{apiKeyTitle}'")

    except Exception as ex:
        print(f"Something went wrong: {ex}")
    
    print("Script complete")

def getApiKeyInfos():
    url = "https://www.arcgis.com/sharing/rest/search"
    params = {}
    params["f"] = "json"
    params["q"] = f"owner:{_portalUsername} AND (type:'API Key') AND (typekeywords:'Registered App')"
    params["sortField"] = "created"
    params["sortOrder"] = "desc"
    apiKeyinfos = sendPythonApiRequest(url,"GET",params)
    return apiKeyinfos

def getRegisteredAppInfo(apiKeyItemId):
    url = f"https://www.arcgis.com/sharing/rest/content/users/{_portalUsername}/items/{apiKeyItemId}/registeredAppInfo"
    params = {}
    params["f"] = "json"
    registeredAppInfo = sendPythonApiRequest(url,"POST",params)
    return registeredAppInfo

def getUsage(apiKeyClientId):
    url = f"https://billingapi.arcgis.com/developersubscription/dashboard/graph"
    params = {}
    params["startDate"] = createTimestamp(_dateFrom)
    params["endDate"] = createTimestamp(_dateTo)
    params["units"] = "requests"
    params["appId"] = apiKeyClientId
    params["period"] = _returnPeriod
    headers = {}
    headers["Authorization"] = f"Bearer {_gis._con.token}"
    usage = {}

    attempt = 1
    while attempt < _maxNumberOfTries:
        try:
            if attempt > 1:
                print(f"Attempt nr {attempt} to get usage data...")
            attempt += 1
            usage = sendRequest(url,"GET",params,headers)
            return usage
        except Exception as ex:
            print(f"Something went wrong while getting usage: {ex}")
    

def createTimestamp(dateString):
    element = datetime.strptime(dateString,"%Y/%m/%d")
    timestamp = round(datetime.timestamp(element) * 1000)
    return timestamp

def sendRequest(url, type="POST", params=None, headers=None):
    if type == "GET":
        r = requests.get(url, params=params, headers=headers)
    else:
        r = requests.post(url, params=params, headers=headers)
    response = r.json()
    return response

def sendPythonApiRequest(url, type="POST", params=None, headers=None):
    if type == "GET":
        response = _gis._con.get(url, params=params, headers=headers)
    else:
        response = _gis._con.post(url, params=params, headers=headers)

    if "error" in response:
        print(f"Error in response: {response['error']}")

    return response

# def getGIS():
#     global _gis
#     #get gis
#     profileName = "arcgis_{}".format(_portalUsername)
#     # change password
#     _gis = arcgis.GIS(_portalUrl, profile=profileName)

#     #if the users.me is None, logging in through the profilename did not succeed. Then get a password and create the profile
#     if _gis.users.me is None:
#         print("Please provide a password")
#         import getpass
#         pwd = getpass.getpass()
#         _gis = arcgis.GIS(_portalUrl, username=_portalUsername,password=pwd,profile=profileName)

#     print("Successfully signed in to '{}' via the '{}' user".format(_gis.properties.portalHostname,_gis.properties.user.username))

def getGIS(portalUsername=None, portalUrl=None):
    global _gis
    try:
        if portalUsername:
            print("Signing in using profile")
            profileName = "arcgis_{}".format(portalUsername)

            profileManager = arcgis.gis._impl._profile.ProfileManager()

            if profileName not in profileManager.list():
                portalUrl = "https://www.arcgis.com" if portalUrl == None else portalUrl 

                import getpass
                portalPassword = getpass.getpass()

                profileManager.create(profileName, portalUrl, portalUsername, portalPassword)
                print(f"Created new profile for user: {portalUsername}")
            
            # get gis
            _gis = arcgis.GIS(portalUrl, profile=profileName)
        else:
            print("Signing in using ArcGIS Pro")
            _gis = arcgis.GIS("Pro")

        print("Successfully signed in to '{}' with the '{}' user".format(_gis.properties.portalHostname,_gis.properties.user.username))
    except Exception as ex:
        print(f"The GIS object could not be created. You either need to be signed in with ArcGIS Pro or provide a portal username: {ex}")
        _gis = None



if __name__ == "__main__":
    main()