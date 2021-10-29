# List in Chunks
This samples shows how to split a large list into smaller lists of a maximum size.

``` Python
chunkSize = 250
chunks = [largeList[x:x+chunkSize] for x in range(0, len(largeList), chunkSize)]

for chunk in chunks:
    #do something with chunk
```
