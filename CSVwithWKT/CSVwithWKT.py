import arcpy
import csv

_inputCSV = r"Sample table.csv"
_outputFCL = r"MyGeoDatabase.gdb\MyPolygons"

def main():
    #read csv
    print("Reading csv")
    csvRows = []
    #opening csv file
    with open(_inputCSV,'r') as f:
        #read all rows into a list of dicts
        csvRows = [{k: v for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]

    print(f"CSV parsed, nrof lines: {len(csvRows)}")
   
    #create insertcursor
    print("Creating insertcursor")
    with arcpy.da.InsertCursor(_outputFCL,["name","SHAPE@WKT"]) as icur:
        
        #insert all 'features'
        print("Start inserting")
        for csvRow in csvRows:
            newRow = (csvRow['name'],csvRow['geometry'])
            icur.insertRow(newRow)
    
    #party!!
    print("Script complete")

if __name__=="__main__":
    main()