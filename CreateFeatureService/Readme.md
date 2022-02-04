# Creating a hosted Feature Service
This sample shows how to create a FeatureService using the ArcGIS REST API.

Creating a FeatureService is a two step process.
1. Creating an empty service (just a name is enough)
2. Adding a layer to that service defining the geometry type and fields for it.

``` Python
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
...
```
For more information about creating a service see the documentation page:

https://developers.arcgis.com/rest/users-groups-and-items/create-service.htm

For more information about the add to Definition call see:

https://developers.arcgis.com/rest/services-reference/enterprise/add-to-definition-feature-service-.htm
