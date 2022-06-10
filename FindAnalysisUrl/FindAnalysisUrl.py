import Security
import requests
import time
import json

#generating a token (see other coolscripts voor that)
token = Security.GenerateToken()

#getting the analysis URL for this portal
print("Get analysis URL")
defaultParams = {"f":"json","token":token}
portalSelfUrl = "https://www.arcgis.com/sharing/rest/portals/self"

portalInfo = requests.get(portalSelfUrl,params=defaultParams).json()
analysisUrl = portalInfo["helperServices"]["analysis"]["url"]
print(f"analysisUrl:{analysisUrl}")

#Setting up the tesselation parameters (in this case only city center of Zwolle)
print("setup Tesselation parameters parameters")
tesselationParams = defaultParams.copy()
tesselationParams["binType"] ="HEXAGON"
tesselationParams["binSize"] = 1000
tesselationParams["binSizeUnit"] = "Meters"
tesselationParams["extentLayer"] = json.dumps({"url": "https://services.arcgis.com/nSZVuSZjHpEZZbRo/arcgis/rest/services/CBS_Wijk_actueel/FeatureServer/0", "filter": "statcode='WK019310'"})
tesselationParams["intersectStudyArea"] = False
tesselationParams["outputName"] = json.dumps({"serviceProperties": {"name": "Export_Tesselation_2"}})

#submitting the jon
print("Executing Tesselation job")
tesselationUrl = analysisUrl + "/GenerateTessellations/submitJob"
print(f"tesselationUrl:{tesselationUrl}")
jobResponse = requests.post(tesselationUrl,tesselationParams).json()

#getting the job id and status
print("check for job completion")
jobid = jobResponse["jobId"]
status = jobResponse["jobStatus"]
counter = 1
jobstatusurl = f"{analysisUrl}/GenerateTessellations/jobs/{jobid}"

#checking for job completion (or more than 100 trips to avoid endless loop)
while((status == "esriJobSubmitted" or status=="esriJobWaiting" or status=="esriJobExecuting") and counter < 100):
    jobstatusresponse = requests.get(jobstatusurl,params=defaultParams).json()
    print(jobstatusresponse)
    status = jobstatusresponse["jobStatus"]
    print("Job status: {}".format(status))
    counter +=1
    time.sleep(2)

print("Script complete")