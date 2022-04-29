#-------------------------------------------------------------------------------
# Name:        ReturnUpdates
# Purpose:     Update the time extent of the Feature Service
#
# Author:      EsriNL DevTeam
#
# Created:     20220429
# Copyright:   (c) Esri Nederland 2022
# Licence:     MIT License
#-------------------------------------------------------------------------------

import requests
import datetime

## URL to the Feature Layer with updated data
feature_layer_url = "https://services.arcgis.com/emS4w7iyWEQiulAb/arcgis/rest/services/Meetwaarden_Update/FeatureServer/0"

## Update parameters
update_params = {}
update_params["returnUpdates"] = True
update_params["f"] = "json"
update_params["token"] = generate_token()

## Call the Feature Layer URL with the 'returnUpdates' parameter
update_response = requests.get(feature_layer_url, params=update_params).json()

## Print the new time extent
updated_start_time = datetime.datetime.fromtimestamp(update_response["timeExtent"][0]/1000)
updated_end_time = datetime.datetime.fromtimestamp(update_response["timeExtent"][1]/1000)
print(f"Updated the time extent to: {updated_start_time} --- {updated_end_time}")
