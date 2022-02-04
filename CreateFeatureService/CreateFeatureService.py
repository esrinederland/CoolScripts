import requests
import json
import datetime

username = ""
password = ""
portalUrl = "https://www.arcgis.com"

def main():
    #getting a token with the username and password
    token = GenerateToken()

    #deteremine a service name
    serviceName = "generatedService_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    #create a service
    createParams = {
        "name": serviceName
    }

    #determine the create Service URL
    createServiceUrl = f"{portalUrl}/sharing/rest/content/users/{username}/createService"

    createServiceParams = {
        "token": token,
        "f": "json",
        "targetType": "featureService",
        "createParameters": json.dumps(createParams),
    }

    print("Creating service")
    r = requests.post(createServiceUrl, createServiceParams)
    serviceInfo = r.json()
    print("Service created: serviceInfo: {}".format(serviceInfo))

    #get the serivce url that just got created
    serviceURL = serviceInfo["serviceurl"]

    #determine the layer parameters, a RD Point with two fields
    addParams = {
        "layers": [
            {
                "id": 0,
                "name": "MyPointLayer",
                "geometryType": "esriGeometryPoint",
                "type": "Feature Layer",
                "minScale": 0,
                "maxScale": 0,
                "extent": {
                    "xmin": 0,
                    "ymin": 300000,
                    "xmax": 300000,
                    "ymax": 700000,
                    "spatialReference": {"wkid": 28992},
                },
                "drawingInfo": {
                    "renderer": {
                        "type": "simple",
                        "symbol": {
                            "type": "esriSMS",
                            "style": "esiSMSCircle",
                            "size": 15,
                            "color": [255, 0, 0, 125],
                            "outline": {"color": [255, 255, 255, 255], "width": 1},
                        },
                    }
                },
                "hasAttachments": False,
                "hasMetadata": True,
                "hasM": False,
                "hasZ": False,
                "objectIdField": "OBJECTID",
                "uniqueIdField": {"name": "OBJECTID", "isSystemMaintained": True},
                "fields": [
                    {
                        "name": "OBJECTID",
                        "type": "esriFieldTypeOID",
                        "alias": "OBJECTID",
                        "sqlType": "sqlTypeOther",
                        "nullable": False,
                        "editable": False,
                        "domain": None,
                        "defaultValue": None,
                    },
                    {
                        "name": "MyName",
                        "type": "esriFieldTypeString",
                        "alias": "MyNameAlias",
                        "sqlType": "sqlTypeOther",
                        "length": 42,
                        "nullable": False,
                        "editable": False,
                        "domain": None,
                        "defaultValue": None,
                    },
                ],
                "capabilities": "Query,Editing,Create,Update,Delete,Sync",
            }
        ]
    }
    
    #determine the add layer URL (note the adding of the 'admin' between the 'rest' and 'services')
    addToDefinitionUrl = f"{serviceURL.replace('/rest/services/','/rest/admin/services/')}/addToDefinition"
    addToDefinitionParams = {
        "token": token,
        "f": "json",
        "addToDefinition": json.dumps(addParams),
    }

    print(f"adding to definition on url: {addToDefinitionUrl}")
    r = requests.post(addToDefinitionUrl, addToDefinitionParams)

    print("added to definition")
    print(r.json())

    print("Script complete")

def GenerateToken():
    print("GenerateToken::Start")

    # Get token
    token_URL = f"{portalUrl}/sharing/generateToken"
    token_params = {
        "username": username,
        "password": password.password,
        "referer": {portalUrl},
        "f": "json",
        "expiration": 60,
    }

    r = requests.post(token_URL, token_params)
    token_obj = r.json()

    token = token_obj["token"]
    expires = token_obj["expires"]

    tokenExpires = datetime.datetime.fromtimestamp(int(expires) / 1000)

    print("new token: {}".format(token))
    print("token for {} expires: {}".format(username, tokenExpires))
    return token


if __name__ == "__main__":
    main()
