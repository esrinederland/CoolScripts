# the INTERVAL syntax
This samples shows how use the INTERVAL syntax with feature layer queries. At 10.6.1 and later, the INTERVAL syntax can be used in place of the date-time queries and will be standardized across all map and feature services. This means that you don't have to calculate intervals yourself in Python because you can use the build-in functionality in your queries. 

``` Python
# Create a feature layer based on a url and a previously created arcgis.GIS object
logInfo("Creating FeatureLayer")
featureLayerObject = arcgis.features.FeatureLayer(featureLayerUrl,gis)

# Get a feature count of all features that were edited within the last 12 hours
features = featureLayerObject.query(where="EditDate > CURRENT_TIMESTAMP - INTERVAL '12' HOUR")
logInfo(f"These features were edited within the last 12 hours: {features}")
```