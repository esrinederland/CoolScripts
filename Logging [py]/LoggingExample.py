#-------------------------------------------------------------------------------
# Name:        LoggingExample.py
# Purpose:     Simple Logging 
#
# Author:      EsriNL DevTeam (MVH)
#
# Created:     20210409
# Copyright:   (c) Esri Nederland 2021
# Licence:     MIT License
#-------------------------------------------------------------------------------
import LogUtils as log

#defin the logpath: [date] will be replaced with current datetime
_logFilePath = r"D:\temp\logging\LoggingExample_[date].log"
def main():
    #setup logging
    log.ConfigureLogging(_logFilePath)
    log.LogInfo("Start LoggingExample")

    #create a random list of nombers
    fibolist = [1,2,3,5,0,8,13,21]

    log.LogDebug(f"Start parsing {len(fibolist)} numbers")
    for num in fibolist:
        try:
            log.LogDebug(f"Start parsing {num}")
            
            result = 34 / num
            
        except:
            #LogException logs the error and stacktrace
            log.LogException(f"error parsing {num}")

    #script complete: party \o/
    log.LogInfo("Script complete")

if __name__== "__main__":
    main()