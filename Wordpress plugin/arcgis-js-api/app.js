// get the complete source for the script (url + params)
var scriptSrc = document.currentScript.src;
// create a new url so we can read the params
var url = new URL(scriptSrc);
var webmapId  = url.searchParams.get("webmapId");
var apiKey  = url.searchParams.get("apiKey");
jQuery(window).load(function () {  
    require(["esri/config", "esri/views/MapView", "esri/WebMap"], function (
        esriConfig,
        MapView,
        WebMap
    ) {
        console.log("webmapId: ", webmapId);
        console.log("apiKey: ", apiKey);

        esriConfig.apiKey = apiKey;
        /************************************************************
         * Creates a new WebMap instance. A WebMap must reference
         * a PortalItem ID that represents a WebMap saved to
         * arcgis.com or an on-premise portal.
         *
         * To load a WebMap from an on-premise portal, set the portal
         * url with esriConfig.portalUrl.
         ************************************************************/
        var webmap = new WebMap({
            portalItem: {
                // autocasts as new PortalItem()
                id: webmapId
            }
        });

        /************************************************************
         * Set the WebMap instance to the map property in a MapView.
         ************************************************************/
        var view = new MapView({
            map: webmap,
            popup: {
            dockEnabled: true,
            dockOptions: {
                // Disables the dock button from the popup
                buttonEnabled: false,
                // Ignore the default sizes that trigger responsive docking
                breakpoint: false
            }
            },
            // IMPORTANT! don't change the container name or make sure it corresponds with the id of the div returned in the file arcgis-js-api.php at line 60
            container: "viewDiv"
        });
    });
});