#-------------------------------------------------------------------------------
# Name:        Upsert
# Purpose:     CodeSnippet that shows how to use Append to upsert features on a 
#              hosted feature layer having a list of features as input
#
# Author:      EsriNL DevTeam (MJA)
#
# Created:     20211216
# Copyright:   (c) Esri Nederland 2021
# Licence:     MIT License
#-------------------------------------------------------------------------------

import arcgis
import json
	
# get the hosted feature layer item using the (ArcGIS Online) item id
_targetId = "HOSTED-FEATURE-LAYER-ITEM-ID"
# get the layer id
_targetLayerId = 0

# ArcGIS Online username
_portalUsername = "YOUR-PORTAL-USERNAME"

_portalUrl = "https://www.arcgis.com"

# the field that contains the unique identifier for the upsert
# has to have unique values in the hosted feature layer!
_upsertMatchingField = "driverID"

def main():
    try:
        print("Connecting to ArcGIS")
        gis = getGIS()

        # get the target service (item) from the gis object based on the item id
        targetService = gis.content.get(_targetId)
        if(targetService):
            # get the featurelayer object from the item
            featureLayerObject = targetService.layers[_targetLayerId]
        else:
            print(f"Error no target id present {_targetId}.")
            return

        # create the fields list for the layerDefinition
        fields = [
            {
                "name": "driverID",
                "type": "esriFieldTypeInteger",
                "alias": "driverID"
            },
            {
                "name": "driverName",
                "type": "esriFieldTypeString",
                "alias": "driverName"
            },
            {
                "name": "totalWorldChampionships",
                "type": "esriFieldTypeInteger",
                "alias": "totalWorldChampionships"
            },
            {
                "name": "isWorldChampion",
                "type": "esriFieldTypeInteger",
                "alias": "isWorldChampion"
            }
        ]

        # update Lewis Hamilton's world championship status and add a new record for Max Verstappen
        upsertFeatures = [
            {
                "attributes": {
                    "driverID": 44,
                    "driverName": "Lewis Hamilton",
                    "totalWorldChampionships": 7,
                    "isWorldChampion": False
                },
                "geometry": {
                    "x": -0.18870527571223092,
                    "y": 51.90555244589362
                }
            },
                {
                "attributes": {
                    "driverID": 1,
                    "driverName": "Max Verstappen",
                    "totalWorldChampionships": 3,
                    "isWorldChampion": True
                },
                "geometry": {
                    "x": 5.338622083009606,
                    "y": 50.92990138162017
                }
            }
        ]

        # create a feature collection using the field and features
        featureCollection = {
            "layers" : [
                {
                    "layerDefinition": {
                        "geometryType": featureLayerObject.properties.geometryType,
                        "fields": fields
                    },
                    "featureSet": {
                        "geometryType": featureLayerObject.properties.geometryType,
                        "spatialReference": {'wkid': featureLayerObject.properties.extent.spatialReference.wkid},
                        "features": upsertFeatures
                    }
                }
            ]
        }

        # create a json string from the feature collection to be used in the append/upsert operation  
        featureCollectionJson = json.dumps(featureCollection)

        # upsert the features to the feature layer
        # the Python API returns a boolean value whether the upsert operation has succeeded or not
        success =  featureLayerObject.append(
            edits=featureCollectionJson, 
            upsert=True, 
            use_globalids=False, # in this case the field "driverID" is used
            update_geometry=True, 
            skip_inserts=False, 
            skip_updates=False, 
            upsert_matching_field=_upsertMatchingField
            )

        if success:
            print("The Formula One driver data was successfully upserted to the feature layer.")
        else:
            print("Something went wrong while upserting the data.")


    except Exception as ex:
        print(f"Error in main: {ex}") 


    print("Script complete")



def getGIS():
    """Get a GIS object using the profile. If the user is not signed in, the password for the portal user can be entered."""
    profileName = f"arcgis_{_portalUsername}"

    # get the GIS object
    gis = arcgis.GIS(_portalUrl, profile=profileName)

    # if the users.me is None, the user couldn't sign in to the portal. In that case have the user enter the password and create the profile
    if gis.users.me is None:
        print("Please provide password:")
        import getpass
        pwd = getpass.getpass()
        gis = arcgis.GIS(_portalUrl, username=_portalUsername,password=pwd,profile=profileName)

    print(f"Successfully signed in to '{gis.properties.portalHostname}' using the '{gis.properties.user.username}' user") 

    return gis


if __name__ == "__main__":
    main()
