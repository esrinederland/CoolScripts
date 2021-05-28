import json
import copy
import requests
import datetime

from logUtils import *

# Log file location
_logFilePath = r"D:/Temp/Logging/createViews_[date].log"

# ArcGIS Online
_sourceFLUrl = "[YOUR-FEATURE-LAYER-URL]"
_uniqueValueField = "PROVINCIE"
_username = "[YOUR-USERNAME]"
_password = "[YOUR-PASSWORD]"

# Sript parameters
_viewServiceProperties = ["serviceDescription", "hasStaticData","maxRecordCount", "supportedQueryFormats", "capabilities",	"description", 
                        "copyrightText", "spatialReference", "initialExtent", "allowGeometryUpdates", "units", "xssPreventionInfo"]
_viewLayerProperties = ["currentVersion", "id", "name",	"type", "displayField", "extent"]

# Global parameters
_token = None
_tokenExpires = None
_sourceService = None
_sourceServiceData = None
_sourceLayer = None
_sourceItem = None

def main():

    # Start logging
    ConfigureLogging(_logFilePath, level="INFO")
    LogInfo("Script started")   

    # Read source service information
    readSourceData()

    # Get unique values
    uniqueValues = getUniqueValues()

    # Loop through all unique values and create a view for it
    for uniqueValue in uniqueValues:
        createViewForUniqueValue(uniqueValue)
    
    LogInfo("Script completed")

def getUniqueValues():
    """Get the unique values from the Feature Service"""

    queryUrl = f"{_sourceFLUrl}/query"
    queryParams = {}
    queryParams["where"] = "1 = 1"
    queryParams["outFields"] = _uniqueValueField
    queryParams["returnDistinctValues"] = True
    queryParams["returnGeometry"] = False
    queryResponse = sendRequest(queryUrl, queryParams)

    uniqueValues = [feature["attributes"][_uniqueValueField] for feature in queryResponse["features"]]

    return uniqueValues

def createViewForUniqueValue(uniqueValue):
    """Create a new View from the source layer"""

    # Create json with view information using source service
    viewJson = {}
    # Generate a unique name for the view (fs name + unique value)
    viewJson["name"] = f"{_sourceFLUrl.split('/')[-3]} {uniqueValue}"
    for serviceProperty in _viewServiceProperties:
        viewJson[serviceProperty] = _sourceService[serviceProperty]

    # CreateService
    LogInfo(f"Creating Service for {uniqueValue}")
    createServiceUrl = f"https://www.arcgis.com/sharing/rest/content/users/{_username}/createService"
    createServiceParams = {}
    createServiceParams["isView"] = True
    createServiceParams["outputType"] = "featureService"
    createServiceParams["createParameters"] = json.dumps(viewJson)

    createServiceResponse = sendRequest(createServiceUrl, createServiceParams)

    # If service is created successfull
    if createServiceResponse["success"] == True:
        viewItemID = createServiceResponse["itemId"]
        viewItemUrl = f"https://www.arcgis.com/sharing/rest/content/users/{_username}/items/{viewItemID}"
        viewServiceUrl = createServiceResponse["serviceurl"]

        # Add layer to View definition
        LogInfo("AddToDefinition View")
        adminServiceUrl = viewServiceUrl.replace("rest/services", "rest/admin/services")
        addToDefinitionUrl = f"{adminServiceUrl}/addToDefinition"

        sourceLayerJson = {}
        for layerProperty in _viewLayerProperties:
            sourceLayerJson[layerProperty] = json.dumps(_sourceLayer[layerProperty])
        sourceLayerJson["url"] = _sourceFLUrl
        sourceLayerJson["adminLayerInfo"] = {
            "viewLayerDefinition": {
                "sourceServiceName": sourceLayerJson["url"].split("/")[-3],
                "sourceLayerId": 0,
                "sourceLayerFields": "*"
            }
        }
        addToDefinitionParams = {}
        addToDefinitionParams["addToDefinition"] = json.dumps({
            "layers": [sourceLayerJson]
            })

        addToDefinitionResponse = sendRequest(addToDefinitionUrl, addToDefinitionParams)
        if addToDefinitionResponse["success"] == False:
            LogException(f"Unable to add layer to view for {uniqueValue}: {addToDefinitionResponse['error']['message']}")

        # Update _sourceServiceData for current unique value
        uniqueValueData = editViewData(uniqueValue)

        # Update View
        LogInfo("Update View")
        updateViewUrl = f"{viewItemUrl}/update"
        updateViewParams = {}
        updateViewParams["title"] = viewJson["name"]
        updateViewParams["id"] = viewItemID
        updateViewParams["text"] = json.dumps(uniqueValueData)

        updateViewResponse = sendRequest(updateViewUrl, updateViewParams)
        if updateViewResponse["success"] == False:
            LogException(f"Unable to update view for {uniqueValue}: {updateViewResponse['error']['message']}")

        # Share View
        LogInfo("Share View")
        shareViewUrl = f"{viewItemUrl}/share"
        shareViewParams = {}
        shareViewParams["everyone"] = True

        shareViewResponse = sendRequest(shareViewUrl, shareViewParams)
        if len(shareViewResponse["notSharedWith"]) > 0:
            LogException(f"Unable to share view for {uniqueValue}")
    else:
        LogException(f"Could not create view for {uniqueValue}: {createServiceResponse['error']['message']}")

    return viewItemID, viewServiceUrl

def editViewData(uniqueValue):
    """Edit the source service data for the current unique value"""

    # Create a copy from the source service data
    uniqueValueData = copy.deepcopy(_sourceServiceData)

    # Change service data to use current unique value information (assumes a string value )
    uniqueValueData["layers"][0]["layerDefinition"]["definitionExpression"] = f"{_uniqueValueField} = '{uniqueValue}'"

    return uniqueValueData

def readSourceData():
    """Read information from the source Feature Service"""
    global _sourceService
    global _sourceServiceData
    global _sourceLayer
    global _sourceItem

    LogInfo("Loading source data and information into memory")

    # Feature Service Definition
    _sourceService = sendRequest(_sourceFLUrl[:-2])

    # Feature Layer (0) Definition
    sourceLayerUrl = _sourceFLUrl
    _sourceLayer = sendRequest(sourceLayerUrl)

    # Item Description
    sourceItemUrl = f"https://www.arcgis.com/sharing/rest/content/items/{_sourceService['serviceItemId']}"
    _sourceItem = sendRequest(sourceItemUrl)

    # Item Data
    sourceDataUrl = f"{sourceItemUrl}/data"
    _sourceServiceData  = sendRequest(sourceDataUrl)

def checkToken():
    """Check if ArcGIS token is still valid, if not, retrieve new one"""

    global _token
    global _tokenExpires

    # If token is expired, or not yet created, generate a new token
    if not _tokenExpires or _tokenExpires < (datetime.datetime.now().timestamp() * 1000) + 3600:
        portalUrl = "https://www.arcgis.com"
        
        tokenURL = "{}/sharing/generateToken".format(portalUrl)
        tokenParams = {'username':_username,'password': _password,'referer': portalUrl,'f':'json','expiration':60}

        r = requests.post(tokenURL, tokenParams)
        
        tokenObject = r.json()
            
        _token = tokenObject['token']
        _tokenExpires = tokenObject["expires"]

def sendRequest(requestUrl, params={}):
    """Send a request to the given url to retrieve data"""

    # Check if the token is still valid
    checkToken()

    # Set token and output type
    params["token"] = _token
    params["f"] = "json"

    # Send the request
    r = requests.post(requestUrl, params)

    results = r.json()

    return results

if __name__ == "__main__":
    main()
