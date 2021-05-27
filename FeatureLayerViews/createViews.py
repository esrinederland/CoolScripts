import json
import copy
import requests

from logUtils import *

# Log file location
_logFilePath = r"D:/Temp/Logging/createViews_[date].log"

# ArcGIS Online
_sourceFSUrl = "https://services6.arcgis.com/PJ2O5BaHcA2bnIXr/ArcGIS/rest/services/Onderwijslocaties/FeatureServer"
_provinceFLUrl = "https://services.arcgis.com/nSZVuSZjHpEZZbRo/ArcGIS/rest/services/Provincie_veiligheidsregio_GGD_regio/FeatureServer/0"
_username = ""
_password = ""

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
    ConfigureLogging(_logFilePath)
    LogInfo("Script started")   

    # Read source service information
    readSourceData()

    # Get provinces
    provinces = getProvinces()

    for province in provinces:
        createViewForProvince(province)
    
    LogInfo("Script completed")

def getProvinces():
    """Get the provinces from the province Feature Service"""

    queryUrl = f"{_provinceFLUrl}/query"
    queryParams = {}
    queryParams["where"] = "SoortGebied = 'Provincie'"
    queryParams["outFields"] = "*"

    queryResponse = sendRequest(queryUrl, queryParams)

    provinces = [province["attributes"]["NaamGebied"] for province in queryResponse["features"]]

    return provinces

def createViewForProvince(province):
    """Create a new View from the source layer"""

    # Create json with view information using source service
    viewJson = {}
    viewJson["name"] = f"Onderwijslocaties {province}"
    for serviceProperty in _viewServiceProperties:
        viewJson[serviceProperty] = _sourceService[serviceProperty]

    # CreateService
    LogInfo(f"Creating Service for {province}")
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
        sourceLayerJson["url"] = f"{_sourceFSUrl}/0"
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
            LogException(f"Unable to add layer to view for {province}: {addToDefinitionResponse['error']['message']}")

        # Update _sourceServiceData for current province
        provinceData = editViewData(province)

        # Update View
        LogInfo("Update View")
        updateViewUrl = f"{viewItemUrl}/update"
        updateViewParams = {}
        updateViewParams["title"] = viewJson["name"]
        updateViewParams["id"] = viewItemID
        updateViewParams["text"] = json.dumps(provinceData)

        updateViewResponse = sendRequest(updateViewUrl, updateViewParams)
        if updateViewResponse["success"] == False:
            LogException(f"Unable to update view for {province}: {updateViewResponse['error']['message']}")

        # Share View
        LogInfo("Share View")
        shareViewUrl = f"{viewItemUrl}/share"
        shareViewParams = {}
        shareViewParams["everyone"] = True

        shareViewResponse = sendRequest(shareViewUrl, shareViewParams)
        if len(shareViewResponse["notSharedWith"]) > 0:
            LogException(f"Unable to share view for {province}")
    else:
        LogException(f"Could not create view for {province}: {createServiceResponse['error']['message']}")

    return viewItemID, viewServiceUrl

def editViewData(province):
    """Edit the source service data for the current province"""

    # Create a copy from the source service data
    provinceData = copy.deepcopy(_sourceServiceData)

    # Change service data to use current province information
    provinceData["layers"][0]["layerDefinition"]["definitionExpression"] = f"PROVINCIE = '{province}'"

    return provinceData

def readSourceData():
    """Read information from the source Feature Service"""
    global _sourceService
    global _sourceServiceData
    global _sourceLayer
    global _sourceItem

    LogInfo("Loading source data and information into memory")

    # Feature Service Definition
    _sourceService = sendRequest(_sourceFSUrl)

    # Feature Layer (0) Definition
    sourceLayerUrl = f"{_sourceFSUrl}/0"
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