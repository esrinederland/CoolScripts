import requests

def main():
    serviceurl = "https://services2.arcgis.com/YDRnp3rdop6mVcUC/ArcGIS/rest/services/4004_TestFeatures/FeatureServer"
    layerid = 0
    whereClause = "1=1"
    print("Start getting all features")
    allFeatures = GetFeaturesByWhereClause(serviceurl,layerid,whereClause)
    print(f"We got {len(allFeatures)} features from the service")

    print("Script complete")


def GetFeaturesByWhereClause(featureServiceUrl, layerId, whereClause, start=0):
    print("GetFeaturesByWhereClause::start::id={}, where={}, start={}".format(layerId,whereClause,start))
    #create the query url
    queryUrl = f"{featureServiceUrl}/{layerId}/query"
    
    #set all the parameters, all fields, change outSR if needed
    params = {}
    params["where"] = whereClause
    params["outFields"] = "*"
    params["resultOffset"]=start
    params["outSR"] = 4326
    params["f"] = "json"

    #get the data
    r = requests.post(queryUrl,params)
    results = r.json()
    features = results["features"]

    #if there are more features to get the exeededTransferLimit parameter is present and has value True
    if "exceededTransferLimit" in results and results["exceededTransferLimit"]==True:
        
        #determine new offset
        newStart = start+len(results["features"])
        
        #get a new set of features (yes, with recursion)
        extraResults = GetFeaturesByWhereClause(featureServiceUrl,layerId,whereClause,newStart)
        features = features + extraResults

    print("Returning {} features".format(len(features)))        
    return features


if __name__ == "__main__":
    main()