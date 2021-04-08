#-------------------------------------------------------------------------------
# Name:        LogUtils
# Purpose:     Simple Logging implementation
#
# Author:      EsriNL DevTeam (MVH)
#
# Created:     20210409
# Copyright:   (c) Esri Nederland 2021
# Licence:     MIT License
#-------------------------------------------------------------------------------
import logging
import datetime
_logger = None


def ConfigureLogging(logFilePath,level = logging.DEBUG):
    global _logger
    #get the root logger
    _logger = logging.getLogger()
    
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%Y%m%d-%H:%M:%S') #%(threadName)s %(processName)s
    if logFilePath != None:
        #if there is a logfilepath than set the file handler
        #replace the [date] with the current datetime in format yyyymmdd_HHMMSS
        logFilePath = logFilePath.replace("[date]",datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
        fh = logging.FileHandler(logFilePath)
        fh.setFormatter(fmt)
        fh.setLevel(level)
        _logger.addHandler(fh)

    #add the streamhandler (writes to console)
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    ch.setLevel(level)
    _logger.addHandler(ch)
    _logger.setLevel(level)

    return _logger
    
def GetLogger():
    if _logger == None:
        ConfigureLogging(None)
    return _logger

def LogException(msg = ""):
    GetLogger().exception(msg)

def LogError(msg):
    GetLogger().error(msg)

def LogWarning(msg):
    GetLogger().warning(msg)

def LogInfo(msg):
    GetLogger().info(msg)

def LogDebug(msg):
    GetLogger().debug(msg)

