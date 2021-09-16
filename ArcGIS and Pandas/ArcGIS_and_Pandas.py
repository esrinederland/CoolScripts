import arcgis

# Create an ArcGIS Feature
newFeature = arcgis.features.Feature({
    "x":202857, "y":501912,"spatialReference":{"wkid":28992}
   }
  ,{"NAME":"Point42"})

# Create an list of the features (in this case only one)
features = [newFeature]

# Create a FeatureSet of the list of features
fs = arcgis.features.FeatureSet(features)

# Get the FeatureSet as Spatially Enabled Pandas dataframe
df = fs.sdf

# Insert Pandas Magic Here

# Convert the dataframe back to a FeatureSet
fsAfterPandas = arcgis.features.FeatureSet.from_dataframe(df)

# Write the FeatureSet to the FeatureService
myFeatureLayer.edit_features(adds=fsAfterPandas)

print("Script complete")