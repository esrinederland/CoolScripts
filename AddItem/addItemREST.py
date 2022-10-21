import requests
import json
import os
import Security

username = ""
portalUrl = "https://www.arcgis.com"

# specify the file to be uploaded
fileFolder = r"D:\data"
fileName = "uploadFile.geojson"
fileType = "GeoJson"

def main():
    # generating a token (see other coolscripts voor that)
    token = Security.GenerateToken()

    # the url to the addItem endpoint in ArcGIS Online
    addItemUrl = f"{portalUrl}/sharing/rest/content/users/{username}/addItem"

    # open the file in a file stream
    filePath = os.path.join(fileFolder, fileName)
    file = {"file": open(filePath, 'rb')}
    title = os.path.splitext(fileName)[0]
    extension = title = os.path.splitext(fileName)[1]
    
    # specify the paramaters to be sent with the request
    data = {
        "f":"json",
        "token":token,
        "type":fileType,
        "extension":extension,
        "title":title,
        "description":"GeoJson with polygon data",
        "tags":"python, geojson, polygons",
        "filename":fileName
        }

    print(f"Start uploading '{fileName}' to Arcgis Online")
    response = requests.post(addItemUrl, data=data, files=file)
    itemPartJSON = json.loads(response.text)

    if "success" in itemPartJSON:
        itemID = itemPartJSON['id']
        print(f"Added File with itemID: {itemID}")
    else:
        print("\n.File not uploaded. Check the errors and try again.\n")
        print(response.text)


if __name__ == "__main__":
    main()