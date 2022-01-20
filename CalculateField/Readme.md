# Calculate Field
This samples shows how use field calculation to add data to fields based on values in other fields.

``` Python
params = {}
params["f"] = "json"
# multiply the field that contains the value by 5
params["calcExpression"] = json.dumps([{"field" : "[DESTINATION FIELD NAME]", "sqlExpression" : "[VALUE FIELD NAME] * 5"}])
params["sqlFormat"] = "standard"
```

Documentation on field calculations can be found
[here](https://developers.arcgis.com/rest/services-reference/enterprise/calculate-feature-service-layer-.htm)