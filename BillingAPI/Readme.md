# Get API key usage statistics
This samples shows how use the Billing API to get usage statistics for each API key in your ArcGIS Platform account.

``` Python
apiKeyInfos = getApiKeyInfos()
for apiKeyInfo in apiKeyInfos["results"]:
    apiKeyItemId = apiKeyInfo["id"]
    
    registeredAppInfo = getRegisteredAppInfo(apiKeyItemId)
    apiKeyClientId = registeredAppInfo["client_id"]
    
    usage = getUsage(apiKeyClientId)
```
