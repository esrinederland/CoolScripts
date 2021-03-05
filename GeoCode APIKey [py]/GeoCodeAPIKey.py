import requests

#setting up variables
API_KEY = "<<YOUR API KEY>>"
address="Koggelaan 33, Zwolle"
geocode_url = "https://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates"

#setting up parameters
params = {}
params["f"] = "json"
params["address"] = address
params["token"] = API_KEY

#sending request
r = requests.post(geocode_url,params)

#getting response as python dictionairy from json response
response = r.json()

#getting x and y from response
candidate = response["candidates"][0]
x = candidate["location"]["x"]
y = candidate["location"]["y"]

#doing something with the response
print(f"{address} is on x:{x}, y:{y}")
