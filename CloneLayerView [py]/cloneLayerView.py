#-------------------------------------------------------------------------------
# Name:        cloneLayerView
# Purpose:     Clone a Feature Layer View, creating a copy of the View and the 
#              Feature Service it references.
#
# Author:      EsriNL DevTeam
#
# Created:     20220701
# Copyright:   (c) Esri Nederland 2022
# Licence:     MIT License
#-------------------------------------------------------------------------------

import arcgis

gis = arcgis.GIS("Pro")

# Retrieve the View Item using the ItemID
viewItemID = "26cc3839a91843f5b35306447a00b960"
viewItem = gis.content.get(viewItemID)
print(f"Cloning Feature Layer View: {viewItem.title}")

# Apply the clone_items() function
newItems = gis.content.clone_items(
    [viewItem],
    copy_data=True,
    search_existing_items=False
)
for newItem in newItems:
    print(f"Created new item: {newItem.title}")
