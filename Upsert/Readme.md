# Upsert on hosted Feature Layer
This samples shows how to use Append to upsert features on a hosted feature layer using a list of features as input.

Upserting features can be especially useful when updating data to ArcGIS Online from an API call. Many API's contain data (with coordinates) that can be transformed into a list of features. That way you can add that data to a hosted feature layer to be used in maps. But if the data in the API constantly changes, where records can be edited and added, it's a lot of work to keep track of the changes when you would use 'insert' and 'update' for this. By using 'upsert' you eliminate that problem, so you can keep the feature layer up to date continuously.

``` Python
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
            "totalWorldChampionships": 1,
            "isWorldChampion": True
        },
        "geometry": {
            "x": 5.338622083009606,
            "y": 50.92990138162017
        }
    }
]

...

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
```
