# -*- coding: utf-8 -*-

import arcpy
from sqlalchemy import true


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Select nearest city"
        self.description = "Select nearest city"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="Point on map",
            name="selection_point",
            datatype="GPFeatureRecordSetLayer",
            parameterType="Required",
            direction="Input")

        param1 = arcpy.Parameter(
            displayName="City layer",
            name="city_layer",
            datatype="GPFeatureRecordSetLayer",
            parameterType="Required",
            direction="Input")

        param2 = arcpy.Parameter(
            displayName="City name",
            name="out_features",
            datatype="GPString",
            parameterType="Derived",
            direction="Output")

        params = [param0, param1, param2]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        arcpy.env.overwriteOutput = True

        selectie_layer = parameters[0].value
        city_layer = parameters[1].value
        
        arcpy.AddMessage(selectie_layer)
        arcpy.AddMessage(city_layer)

        if not selectie_layer:
            arcpy.AddError("No selection layer available")
            arcpy.SetParameter(2, "No results")
            return

        if not city_layer:
            arcpy.AddError("No city layer available")
            arcpy.SetParameter(2, "No results")
            return

        count = arcpy.GetCount_management(selectie_layer)
        if not count:
            arcpy.SetParameter(2, "No results")
            return

        int_count = int(count[0])
        if int_count == 0:
            arcpy.SetParameter(2, "No results")
            return

        mem_city_selection_layer = "tempcityselection"  

        arcpy.analysis.SpatialJoin(selectie_layer, city_layer, mem_city_selection_layer, match_option="CLOSEST")
        city_names = []

        with arcpy.da.SearchCursor(mem_city_selection_layer, ["CITY_NAME"]) as city_selection_cursor:
            for row in city_selection_cursor:
                city_names.append(row[0])

        arcpy.SetParameter(2, ",".join(city_names))

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
