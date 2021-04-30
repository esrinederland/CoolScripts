import arcgis

#Creating an GIS object using the login from ArcGIS Pro (or use one of the many other way's to create a GIS Object
print("Creating GIS")
gis = arcgis.GIS("PRO")

print("Creating FeatureLayer")
flayer = arcgis.features.FeatureLayer("https://services.arcgis.com/emS4w7iyWEQiulAb/arcgis/rest/services/DummyLayers/FeatureServer/0",gis)

print("Creating Feature")
newfeature = arcgis.features.Feature({"x":6.1,"y":52.5,"spatialReference":{"wkid":4326}},{"NAME":"Point42"})

#Create Feature
print("Adding new Feature")
results = flayer.edit_features(adds = [newfeature])
print(results)

#Select Feature
print("Selecting Features")
fset = flayer.query(where="NAME='Point42'")
existingfeature = fset.features[0]
print(existingfeature)

#Update Feature
print("changing feature")
existingfeature.attributes["NAME"] = "Point43"
print("updating feature")
results = flayer.edit_features(updates = [existingfeature])
print(results)

#Delete Feature
#the delete function expects a comma seprated string of OID's (or a where clause)
oidstring = f'{existingfeature.attributes["OBJECTID"]}'
print("Deleting feature")
results = flayer.delete_features(deletes=oidstring)
print(results)

print("Script complete")