#-------------------------------------------------------------------------------
# Name:        myNotebookScript 
# Purpose:     Some random functions to be executed from a scheduled 
#              hosted notebook
# Author:      mjagt
#
# Created:     20211007
# Copyright:   (c) Esri Nederland 2021
# Licence:     MIT License
#-------------------------------------------------------------------------------

import requests
import sys
from datetime import datetime
import random

version = 20211007.01

def main():
    print (f"Number of arguments: {len(sys.argv)}")
    print (f"Argument List: {str(sys.argv)}")
    username = sys.argv[1]
    password = sys.argv[2]
    RunCompleteScript(username, password)

def RunCompleteScript(username, password):
    print("Execute RunCompleteScript()")
    GenerateToken(username, password)
    GenerateRandomGeometry()

def GenerateToken(username, password):
    print("Execute GenerateToken()")
    # Get token
    token_URL = 'https://www.arcgis.com/sharing/generateToken'
    token_params = {'username':username,'password':password,'referer': 'https://www.arcgis.com','f':'json','expiration':60}

    print(f"Generating token for username '{username}' and password '{password}', version: '{version}', datetime: '{datetime.now().strftime('%Y%m%d %H:%M:%S')}'")
    
    r = requests.post(token_URL,token_params)
    token_obj= r.json()
    
    token = token_obj['token']
    expires = token_obj['expires']

    tokenExpires = datetime.fromtimestamp(int(expires)/1000)

    print(f"new token: {token}")
    print(f"token for {username} expires: {tokenExpires}")

def GenerateRandomGeometry():
    print("Execute GenerateRandomGeometry()")
    x = random.randrange(0,300000)
    y = random.randrange(300000,650000)
    newGeom = {"x":x,"y":y,"spatialReference":{"wkid":28992}}
    print(newGeom)

if __name__ == "__main__":
    main()