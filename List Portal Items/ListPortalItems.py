from arcgis.gis import GIS
from getpass import getpass
from datetime import datetime

portalUrl = "https://mjagtportal.maps.arcgis.com"
portalUser = "mjagtPortal"
# Item types
# If you want to list all item types: "*"
# Oherwise list one or more of the following item types foud here: https://developers.arcgis.com/rest/users-groups-and-items/items-and-item-types.htm
# Some examples of Item Types: "Web Map", "API Key", "Web Mapping Application", "Code Attachment", "Feature Service", "Application", "Service Definition", "CSV Collection", "File Geodatabase", "Dashboard", "WFS", "Vector Tile Service", "Image Collection", "CSV", "KML", "Microsoft Excel", "Feature Collection"
listItemTypes = ["*"]

print(f"Starting 'list portal items' script for portal: {portalUrl}")
print("\n---------------------------------------------------------------------------------------------------\n")
password = getpass("Enter password for the portal: ")
portal = GIS(portalUrl, portalUser, password)


# Get the list of users in the portal. Ignore system accounts
print("\nUsers in portal:")
users = portal.users.search('!esri_ & !admin')
for user in users:
    print(user.username + "\t:\t" + str(user.role))

# Filter out system created groups
groups = portal.groups.search("!owner:esri_* & !Basemaps")
print("\nGroups in portal: ")
for group in groups:
    print(group.title)

# List the number of folders and items per users in the portal
print("\nNumber of items per user in portal:")
items_by_id = {}
for user in users:
    num_items = 0
    num_folders = 0
    user_content = user.items()
    
    # Get item ids from root folder first
    for item in user_content:
        num_items += 1
        items_by_id[item.itemid] = item 
    
    # Get item ids from each of the folders
    folders = user.folders
    for folder in folders:
        num_folders += 1
        folder_items = user.items(folder=folder['title'])
        for item in folder_items:
            num_items += 1
            items_by_id[item.itemid] = item
    
    print(f"{user['username']} has {num_folders} folders and {num_items} items")

# Prepare sharing information for each item
for group in groups:
    # Iterate through each item shared to the portal group
    for group_item in group.content():
        try:
            # Get the item
            item = items_by_id[group_item.itemid]
            if item is not None:
                if not 'groups'in item:
                    item['groups'] = []
                
                # Assign the portal's corresponding group name
                item['groups'].append(group['title'])
        except:
            print(f"\nItem '{group_item.itemid}' shared with group '{group['title']}' no longer exists")

print("\nItems in portal:")
print(f"\n{'Title':60s}| {'Type':30s}| {'ItemID':40s}| {'Owner':30s}| {'Created':30s}| {'Modified':30s}| {'Access':15s}| Shared with group(s)")

for key in items_by_id.keys():
    item = items_by_id[key]
    # if item.type in listItemTypes or len(listItemTypes) == 0:
    if item.type in listItemTypes or listItemTypes[0] == "*":
        print(f"\n{item.title:60s}| {item.type:30s}| {item.itemid:40s}| {item.owner:30s}| {datetime.utcfromtimestamp(item.created/1000).strftime('%Y-%m-%d %H:%M:%S'):30s}| {datetime.utcfromtimestamp(item.modified/1000).strftime('%Y-%m-%d %H:%M:%S'):30s}| {item.access:15s}", end = "| ")
        if 'groups' in item:
            print(f"{item.groups}", end = "")

print("\n\nScript complete")