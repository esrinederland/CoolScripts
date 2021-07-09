# Server Admin in  Python

## Server admin token :
This sample shows how to get a server admin token based on your (admin) portal username and password.

This can be used to preform several admin tasks through scripting.

The following steps are followed:

1. Get a 'normal' token for the user with the referer on the server admin url
2. Exchange the portal token for a server admin token using the ServerUrl parameter
3. Use the admin token on the server endpoint


For more information about the ArcGIS REST API: https://developers.arcgis.com/rest/