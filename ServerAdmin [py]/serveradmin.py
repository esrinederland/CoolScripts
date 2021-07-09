#-------------------------------------------------------------------------------
# Name:        servertoken
# Purpose:     Demo to show how to get a services list from a federated server
#              using a portal username and password
#
# Author:      EsriNL DevTeam (MVH)
#
# Created:     20210709
# Copyright:   (c) Esri Nederland 2021
# Licence:     MIT License
#-------------------------------------------------------------------------------
import requests

from logUtils import *

# Log file location
_logFilePath = r"D:/Temp/Logging/servertoken_[date].log"

# ArcGIS Enterprise settings
_portalUrl = "[YOUR-PORTAL-URL]"
_serverUrl = "[YOUR-SERVER-ADMIN-URL]"
_username = "[YOUR-USERNAME]"
_password = "[YOUR-PASSWORD]"


#Generate token from Portal
generateTokenUrl = f"{_portalUrl}/sharing/rest/generateToken"
params = {}
params["username"] = _username
params["password"] = _password
params["client"] = "referer"
params["referer"] = _serverUrl
params["f"] = "json"
LogInfo(f"Generating token on {generateTokenUrl} for {_username}")
r = requests.post(generateTokenUrl,params)
portalTokenObj = r.json()

portalToken = portalTokenObj["token"]

#Exchange the portal token for server token
params = {}
params["token"] = portalToken
params["serverURL"] = _serverUrl
params["f"] = "json"

LogInfo(f"changing token on {_serverUrl}")
r = requests.post(generateTokenUrl,params)
serverTokenObj = r.json()
serverToken = serverTokenObj["token"]

#Get Server contents
servicesUrl = f"{_serverUrl}/services"
params = {}
params["token"] = serverToken
params["f"] = "json"

LogInfo(f"Getting root services list on  {servicesUrl}")
r = requests.get(servicesUrl,params)
servicesList = r.json()

#getting the services list
services = servicesList["services"]
LogInfo(f"Got {len(services)} root services and {len(servicesList['folders'])} folders")

#looping through all the folders to get all services
for folder in servicesList["folders"]:
    folderUrl = f"{servicesUrl}/{folder}"

    LogInfo(f"Getting services for folder: {folderUrl}")
    r = requests.post(folderUrl,params)
    folderServicesList = r.json()
    services += folderServicesList["services"]

    LogInfo(f"Got {len(folderServicesList['services'])} services in folder {folder}")

#print the summary
LogInfo("="*80)
for service in services:
    LogInfo(f"{service['folderName']:<10} | {service['type']:<15} | {service['serviceName']}")


LogInfo(f"Found {len(services)} services in {len(servicesList['folders'])} folders and root")





    
    




