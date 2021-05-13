import requests
import datetime
import json

import security

_flUrl = "<yourFeatureLayerURL>"
_stravaActivitiesUrl = "https://www.strava.com/api/v3/athlete/activities?after={}"
_stravaOauthUrl = "https://www.strava.com/api/v3/oauth/token?client_id={}&client_secret={}&refresh_token={}&grant_type=refresh_token"
_athletes = {
    "<AthleteName>": {
        "clientID": 00000, #<yourClientID>
        "clientSecret": "<yourClientSecret>",
        "tokenFile": r"yourToken.txt"
    }
}

_token = None
_tokenExpires = None

def checkStravaToken(athlete):
    """Check if Strava token is still valid, if not, retrieve new one"""

    # Get token information from token file
    with open(_athletes[athlete]["tokenFile"]) as tokenFile:
        tokenJson = json.load(tokenFile)

    # If token is not expired, use token from file
    if tokenJson["expires_at"] > (datetime.datetime.now().timestamp() + 1000):
        token = tokenJson["access_token"]

    # If token is (almost) expired, generate new token and store information in token file
    else:
        oauthUrl = _stravaOauthUrl.format(_athletes[athlete]["clientID"], _athletes[athlete]["clientSecret"], tokenJson["refresh_token"])
        response = requests.post(oauthUrl).json()

        if "access_token" in response:
            with open(_athletes[athlete]["tokenFile"], "w") as tokenWriteFile:
                json.dump(response, tokenWriteFile)

            token = response["access_token"]

    return token

def getStravaActivities(token):
    """Get the activities from the last hour for the current athlete"""

    # Get all activities from the last hour
    lastHours = datetime.datetime.now().timestamp() - 3600
    dateUrl = _stravaActivitiesUrl.format(lastHours)

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(dateUrl, headers=headers)

    return response.json()

def decode(pointString):
    """Decode the route string from Strava to a list of coordinates"""
            
    # Coordinate offset is represented by 4 to 5 binary chunks
    coordChunks = [[]]
    for character in pointString:
        
        # Convert each character to decimal from ascii
        value = ord(character) - 63
        
        # Values that have a chunk following have an extra 1 on the left
        splitAfter = not (value & 0x20)         
        value &= 0x1F
        
        coordChunks[-1].append(value)
        
        if splitAfter:
            coordChunks.append([])
        
    del coordChunks[-1]
    
    coordinates = []
    
    for coordChunk in coordChunks:
        coordinate = 0
        
        for i, chunk in enumerate(coordChunk):                    
            coordinate |= chunk << (i * 5) 
        
        # There is a 1 on the right if the coord is negative
        if coordinate & 0x1:
            coordinate = ~coordinate #invert
        coordinate >>= 1
        coordinate /= 100000.0
                    
        coordinates.append(coordinate)
    
    # Convert the 1 dimensional list to a 2 dimensional list and offsets to 
    # actual values
    points = []
    previousX = 0
    previousY = 0
    for i in range(0, len(coordinates) - 1, 2):
        if coordinates[i] == 0 and coordinates[i + 1] == 0:
            continue
        
        previousX += coordinates[i + 1]
        previousY += coordinates[i]
        # Round to 6 digits ensures that the floats are the same as when 
        # they were encoded
        points.append([round(previousX, 6), round(previousY, 6)])

    return points    

def checkToken():
    """Check if ArcGIS token is still valid, if not, retrieve new one"""
    global _token
    global _tokenExpires

    # If token is expired, or not yet created, generate a new token
    if not _tokenExpires or _tokenExpires < (datetime.datetime.now().timestamp() * 1000) + 3600:
        portalUrl = "https://www.arcgis.com"
        
        tokenURL = "{}/sharing/generateToken".format(portalUrl)
        tokenParams = {'username':security.username(),'password': security.password(),'referer': portalUrl,'f':'json','expiration':60}

        r = requests.post(tokenURL, tokenParams)
        
        tokenObject = r.json()
            
        _token = tokenObject['token']
        _tokenExpires = tokenObject["expires"]

def activityPresent(activity):
    """Check if the activity is already in the Feature Layer"""

    # Get the number of records with the given activity id
    activityID = activity["id"]
    queryUrl = f"{_flUrl}/query"
    
    params = {}
    params["f"] = "json"
    params["where"] = f"activity_id = '{activityID}'"
    params["returnCountOnly"] = True
    params["token"] = _token

    checkToken()
    queryFeaturesResult = requests.post(queryUrl, params).json()

    # If there are already records with the given activity_id return True
    if queryFeaturesResult["count"] > 0:
        return True
    else:
        return False

def addFeature(activity, coordinates, athlete):
    """Add a new feature to the Feature Layer representing the activity"""

    feature = {}
    feature["geometry"] = {
        "paths": [coordinates],
        "spatialReference" : {"wkid" : 4326}
    }

    activityTime = activity["start_date_local"][:-1]

    # Check if heartrate information is present in the current activity
    averageHeartrate = None
    maxHearthrate = None
    if activity["has_heartrate"]:
        averageHeartrate = activity["average_heartrate"]
        maxHearthrate = activity["max_heartrate"]

    feature["attributes"] = {
        # Convert datetime to timestamp
        "start_date": datetime.datetime.fromisoformat(activityTime).timestamp() * 1000,

        # Convert distance from m to km
        "distance": activity["distance"] / 1000,
        "moving_time": activity["moving_time"],

        # Convert speeds from m/s to km/h
        "average_speed": activity["average_speed"] * 3.6,
        "max_speed": activity["max_speed"] * 3.6,
        "average_heartrate": averageHeartrate,
        "max_heartrate": maxHearthrate,
        "athlete": athlete,
        "activity_id": activity["id"]
    }

    addFeaturesUrl = f"{_flUrl}/addFeatures"

    params = {}
    params["f"] = "json"
    params["features"] = json.dumps([feature])
    params["token"] = _token

    checkToken()
    addFeaturesResult = requests.post(addFeaturesUrl, params).json()
    print(addFeaturesResult)

if __name__ == "__main__":

    # Loop through dict of athletes and get athletes activities
    for athlete in _athletes:
        token = checkStravaToken(athlete)
        activities = getStravaActivities(token)

        for activity in activities:
            # Only get running activities with stored routes
            if activity["type"] == "Run" and activity["map"]["summary_polyline"]:

                # Check if the activity is already in the Feature Layer, if not, add it as a new feature
                if not activityPresent(activity):
                    polylineString = activity["map"]["summary_polyline"]
                    polyline = decode(polylineString)

                    addFeature(activity, polyline, athlete)