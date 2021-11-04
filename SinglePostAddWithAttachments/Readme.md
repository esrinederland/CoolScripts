# Adding Features And Attachments in one post request

## Creating Features:
Create Features with a global id instead of letting ArcGIS determine it

## Creating Attachments
Creating attachment info's with the global id of the feature as the parentGlobalId

## Add Features
Call the edit_features function with the use_global_ids parameter set to True, this will set the global id of the feature to the global id of the feature in the feature set.
