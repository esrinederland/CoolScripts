from arcgis import GIS

from arcgis.apps.storymap.story import StoryMap
from arcgis.apps.storymap.story_content import Image, Map, Gallery

## Connect to your GIS
gis = GIS("Home")

## Get the template StoryMap
templateStoryMap = StoryMap(item="9cc15ffdbedb4d9798a0b3598dfeccc1", gis=gis)
print(f"Template StoryMap: {templateStoryMap._item.title}")

## Duplicate the template StoryMap
newStoryMapItem = templateStoryMap.duplicate("Keko")
newStoryMap = StoryMap(item=newStoryMapItem, gis=gis)
print(f"New StoryMap: {newStoryMapItem.title}")

## Create an Image object for the Cover
print("Changing StoryMap Cover")
coverImage = Image(path="https://www.arcgis.com/sharing/rest/content/items/2b1610b08d2d460b95f978067e4076b3/data")

## Add a Cover
newStoryMap.cover(
    title = "Keko",
    summary = "I Love My Dog", 
    type = "sidebyside",
    by_line = "Me",
    image = coverImage
    )

## Change the StoryMap Theme
print("Changing StoryMap Theme")
newStoryMap.theme("faf8b808a7d04ff6b0050b50e056bc37")

## Update the Text nodes
print("Changing StoryMap Text")
for textNode in newStoryMap.get(type="text"):
    for nodeID in textNode:
        if "Noodle" in textNode[nodeID].text:
            textNode[nodeID].text = "'<em>My playgrounds - </em><strong>Keko</strong>'"
        elif "Pico" in textNode[nodeID].text:
            textNode[nodeID].text = "'<em>The way I am - </em><strong>Keko</strong>'"

## Add the current WebMap with a new WebMap
print("Replacing WebMap")
newMap = Map(item="e716361549ca48e799040c2a9177d1a0")
newMapID = newStoryMap.add(newMap, caption=None, display="full")
newStoryMap.move(newMapID, position=4, delete_current=True)

## Replace the current Gallery with a new Gallery
print("Replacing Gallery")
imageIDs = ["fbb26d3474734604aaed69107b487ed7", "88c5d02ff7db4ed98bb60770e08a87b8", "3844d8006f1641b2966bb7429d71472b", "b7bf6a526f5a4506b818642d53f0dee2", "e4d16ce7ce124e76a96536f6c3171861", "5eca2a8ea54542b4ba9a690bb1d2e86d"]
newImages = [Image(path=f"https://www.arcgis.com/sharing/rest/content/items/{imageID}/data") for imageID in imageIDs]
newGallery = Gallery()
newGalleryID = newStoryMap.add(newGallery, caption=None)
newGallery.add_images(newImages)
newStoryMap.move(newGalleryID, position=7, delete_current=True)

## Remove current credits
print("Updating Credits")
for nodeID in newStoryMap.get(type="credits")[0]:
    newStoryMap.properties["nodes"][nodeID]["children"] = []

## Add new Credits
newStoryMap.credits(
    content = "Special thanks to",
    attribution = "Keko"
    )

## Edit the StoryMap Item
print("Updating StoryMap Item properties")
newStoryMapItem.update(item_properties={"snippet": "I Love My Dog"}, thumbnail="https://www.arcgis.com/sharing/rest/content/items/b7bf6a526f5a4506b818642d53f0dee2/data")

## Save the StoryMap
print("Saving StoryMap")
newStoryMap.save()

## Print the StoryMap URL
print(f"Open the StoryMap here: https://storymaps.arcgis.com/stories/{newStoryMapItem.id}/edit")
