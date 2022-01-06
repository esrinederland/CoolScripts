#-------------------------------------------------------------------------------
# Name:        QueryInterval
# Purpose:     CodeSnippet that shows how query a feature layer for data 
#              within an interval
#
# Author:      EsriNL DevTeam
#
# Created:     20220106
# Copyright:   (c) Esri Nederland 2022
# Licence:     MIT License
#-------------------------------------------------------------------------------

# Create a feature layer based on a url and a previously created arcgis.GIS object
logInfo("Creating FeatureLayer")
featureLayerObject = arcgis.features.FeatureLayer(featureLayerUrl,gis)

# Get a feature count of all features that were edited within the last 12 hours
features = featureLayerObject.query(where="EditDate > CURRENT_TIMESTAMP - INTERVAL '12' HOUR")
logInfo(f"These features were edited within the last 12 hours: {features}")

# These are a few of the options you can use when working with the INTERVAL syntax in your queries

# <DateField> >= CURRENT_TIMESTAMP -+ INTERVAL 'DD' DAY

# <DateField> >= CURRENT_TIMESTAMP -+ INTERVAL 'HH' HOUR

# <DateField> >= CURRENT_TIMESTAMP -+ INTERVAL 'MI' MINUTE

# <DateField> >= CURRENT_TIMESTAMP -+ INTERVAL 'SS(.FFF)' SECOND

# <DateField> >= CURRENT_TIMESTAMP -+ INTERVAL 'DD HH' DAY TO HOUR

# <DateField> >= CURRENT_TIMESTAMP -+ INTERVAL 'DD HH:MI' DTY TO MINUTE

# <DateField> >= CURRENT_TIMESTAMP -+ INTERVAL 'DD HH:MI:SS(.FFF)' DAY TO SECOND

# <DateField> >= CURRENT_TIMESTAMP -+ INTERVAL 'HH:MI' HOUR TO MINUTE

# <DateField> >= CURRENT_TIMESTAMP -+ INTERVAL 'HH:SS(.FFF)' HOUR TO SECOND

# <DateField> >= CURRENT_TIMESTAMP -+ INTERVAL 'MI:SS(.FFF)' MINUTE TO SECOND