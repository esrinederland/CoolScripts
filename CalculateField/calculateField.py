import requests
import json

featureLayerUrl = "[FEATURELAYER URL]"
params = {}
params["f"] = "json"
# multiply the field that contains the value by 5
params["calcExpression"] = json.dumps([{"field" : "[DESTINATION FIELD NAME]", "sqlExpression" : "[VALUE FIELD NAME] * 5"}])
params["sqlFormat"] = "standard"
params["token"] = "[TOKEN]"

response = requests.post(f"{featureLayerUrl}/calculate", params)
print(response.json())