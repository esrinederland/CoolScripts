# Wordpress plugin

## Shortcode
Wordpress allows you to use a shortcode to add functionality. With the shortcode you basically define a set of properties that are used by the plugin.

## Using the plugin 
Copy and paste the complete "arcgis-js-api" folder into the "plugins" directory of your Wordpress installation. Alternatively you can navigate to the "plugins" section in your Wordpress admin section and choose "Upload Plugin" to upload the folder as a zip file.

Once the plugin is installed, navigate to the "Installed Plugins" and make sure to activate the plugin.

On the page where you want to add your map, add a new block called "shortcode". You could even use a regular Paragraph block if you want. In this block, add the following (width and height can be changed of course):

[arcgis-js-app webmapid="YOUR-WEBMAP-ID" apikey="YOUR-API-KEY" width="90%" height="500px"]

Click the "Update" button, navigate to the live page and refresh it to see your map on the page!


![Add shortcode](../images/wp_plugin_admin.png)<br/>

![Map in page](../images/wp_plugin.png)<br/>


## app.js
The app.js file in this sample is very basic and only adds a webmap. But you can of course take it as a boilerplate sample to create a complete ArcGIS JavaScript API application that can be used within any Wordpress site.