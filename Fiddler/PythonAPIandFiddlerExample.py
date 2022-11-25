proxies = {'http': 'http://127.0.0.1:8888', 'https': 'https://127.0.0.1:8888', 'ftp': 'http://127.0.0.1:8888'}

print("importing ArcGIS")
import arcgis 
print("ArcGIS Version: " + arcgis.__version__)

print("logging into ArcGIS")
gis = arcgis.gis.GIS(profile="arcgis_mvanhulzen_esrinl",proxies=proxies, trust_env=False, verify_cert = False)
print("Successfully logged into '{}' via the '{}' user".format(gis.properties.portalHostname,gis.properties.user.username)) 
gis._con._session.proxies = proxies

print("getting Creating Featurelayer")
featureLayerUrl = "https://services2.arcgis.com/YDRnp3rdop6mVcUC/ArcGIS/rest/services/4004_TestFeatures/FeatureServer/0"
fl = arcgis.features.FeatureLayer(featureLayerUrl,gis)

print("getting featurelayer")
count = fl.query(return_count_only=True)
print(f"Count: {count}")

print("Script complete")