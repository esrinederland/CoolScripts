# Logging in Python

## Configuring:
The ```ConfigureLogging ``` function will set up  the logging:<br/>
The first parameter is the logfilepath, if you do not want a LogFile than set this to None<br/>
if you put ```[date]``` in the logfilepath it will be replaced with the current datetime so youcan create a new logfile for each run.<br/>
The second parameter is the loglevel, standard is DEBUG


Sample:
```python
ConfigureLogging(r'D:\temp\logging\mylog_[date].log')
```
## Using:
After setting up the logging you can just use the logging functions for each loglevel.
```python
LogInfo("My Info Message")
LogDebug("My Debug Message")
LogWarning("My Warning Message")
LogError("My Error Message")
```
will result in:
```
20210409-08:42:42 INFO My Info Message
20210409-08:42:42 DEBUG My Debug Message
20210409-08:42:42 WARNING My Warning Message
20210409-08:42:42 ERROR My Error Message
```

The LogException function will log a complete error and stacktrace and a message (if provided):
```
20210409-08:42:42 ERROR some error message
Traceback (most recent call last):
  File "D:\path\LoggingExample.py", line 24, in main
    result = 34 / num
ZeroDivisionError: division by zero
```