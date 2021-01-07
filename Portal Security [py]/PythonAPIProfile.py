#-------------------------------------------------------------------------------
# Name:        PythonAPIProfile
# Purpose:     Demo to show the use of the profile from the Python API for storing a username 
#              and password in the credential store of the OS instead of the script 
#
# Author:      EsriNL DevTeam (PM/MVH)
#
# Created:     20210107
# Copyright:   (c) Esri Nederland 2020
# Licence:     MIT License
#-------------------------------------------------------------------------------
# package requirements
# pip install arcgis
#-------------------------------------------------------------------------------

import arcgis 

#ArcGIS Online username the script uses
_portalUsername = "<<username>>"

#Portal url
_portalUrl = "https://www.arcgis.com"

def main():    
    try:
        print ("ArcGIS Version: " + arcgis.__version__)
        #get an python api GIS object
        gis = GetGIS()

        #use the gis to search for items.
        items = gis.content.search('Zwolle', 'feature layer')
        for item in items:
            print(item)

    except:
        print("Error in main") 

    print("Demo gereed")


def GetGIS():
    """Get a GIS object using the profile, if the user not logged in then the password can be filled in"""
    profileName = "arcgis_{}".format(_portalUsername)
    print(profileName)
    
    #get GIS
    gis = arcgis.GIS(_portalUrl, profile=profileName)

    #if the users.me is None, logging in through the profilename did not succeed. Then get a password and create the profile
    if gis.users.me is None:
        import getpass
        pwd = getpass.getpass("Voer een wachtwoord in: ")
        gis = arcgis.GIS(_portalUrl, username=_portalUsername, password=pwd, profile=profileName)

    print("Successfully logged into '{}' via the '{}' user".format(gis.properties.portalHostname,gis.properties.user.username)) 

    return gis

if __name__ == "__main__":
    main()