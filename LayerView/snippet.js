var url = "https://services.arcgis.com/[ORGID]/arcgis/rest/services/[LAYERNAME]/FeatureServer/0";
loaderStatus(true, "getting featurecount");

serviceFl = new FeatureLayer(url);

getAllDataFromFeatureLayer(serviceFl, view.spatialReference.wkid).then((result) => {

    loaderStatus(true, "Received features: creating layer");

    fLayer = new FeatureLayer({

    // create an instance of esri/layers/support/Field for each field object
    fields: serviceFl.fields,
    objectIdField: serviceFl.objectIdField, // inferred from fields array if not specified
    geometryType: serviceFl.geometryType, // geometryType and spatialReference are inferred from the first feature
    //   in the source array if they are not specified.
    spatialReference: view.spatialReference,
    source: [result[0]],  //  an array of graphics with geometry and attributes
    // popupTemplate and symbol are not required in each feature
    // since those are handled with the popupTemplate and
    // renderer properties of the layer
    popupTemplate: serviceFl.popupTemplate,
    // a default simple renderer will be applied if not set.
    renderer: serviceFl.renderer  // UniqueValueRenderer based on `type` attribute
    });
    map.add(fLayer);

    view.whenLayerView(fLayer).then(function (layerView) {
        flView = layerView;
    });

    loaderStatus(true, "Adding features to layer");
    fLayer.applyEdits({ addFeatures: result }).then(() => {
        loaderStatus(false, "")
    });

});

function loaderStatus(status, msg) {
    var loader = document.getElementById("loader");
    document.getElementById("loaderText").innerHTML = msg;
    if (status) {
      loader.classList.add("is-active");
    }
    else {
      loader.classList.remove("is-active");
    }

  }

  function getAllDataFromFeatureLayer(fLayer, outSrWkid) {
    return new Promise(resolve => {
      // First, get the count of all features...
      fLayer.queryFeatureCount().then((resultCount) => {
        features = []
        loaderStatus(true, `featurecount ${resultCount}`);
        nrOfRequests = Math.ceil(resultCount / 1000)
        for (i = 0; i < nrOfRequests; i++) {
          j = 0

          var query = { num: 1000, start: i * 1000, returnGeometry: true, outSpatialReference: { wkid: outSrWkid }, outFields: "*" }
          fLayer.queryFeatures(query).then((resultFeatures) => {

            features = features.concat(resultFeatures.features)
            loaderStatus(true, `got features ${features.length} from ${resultCount}`)
            j = j + 1
            if (j === nrOfRequests) {
              var newgraphics = features.map(f => new Graphic({ attributes: f.attributes, geometry: f.geometry }));
              resolve(newgraphics);
            }
          });
        }
      })

    })
  };