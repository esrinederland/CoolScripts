import arcgis
import datetime

#create gis
gis = arcgis.gis.GIS("HOME")
print("Successfully logged into '{}' via the '{}' user".format(gis.properties.portalHostname,gis.users.me)) 

#loop through all users
source_users = gis.users.search()
tasklist = []
for user in source_users:
    print(user.username + "\t:\t" + str(user.role))
    #get tasks
    for task in user.tasks.all:
        tasklist.append(task)

print('username, scheduletype, itemtitle (id), state, lastrundate')
for task in tasklist:
    #put properties in a variable for easy string formatting
    tp = task.properties
    #create a date from the arcgis timestamp
    lastrundate = datetime.datetime.fromtimestamp(tp.lastStart/1000)
    print(f'{tp.userId}, {tp.type}, {tp.title} ({tp.itemId}), {tp.taskState}, {lastrundate}')

print('script complete')