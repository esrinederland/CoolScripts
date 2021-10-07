# Schedule a python script using an ArcGIS Online Hosted Notebook
You can schedule your own Python scripts using ArcGIS Online Hosted Notebooks. This eliminates the need of having your own server to schedule scripts. If you want to use ArcPy functionality you will need to create an "Advanced" Notebook, otherwise a "Standard" Notebook is sufficient. And of course you can't use local data sources when using ArcGIS Online Hosted Notebooks.
<br>
These are the steps to schedule a script called "myNotebookScript.py":
<br>
1. Create a new Notebook (in this case we choose "Standard")
![Step 1](../images/ScheduledNotebook/step1.png)<br/>
![Step 2](../images/ScheduledNotebook/step2.png)<br/>
2. Save the Notebook to enable the "Tasks"
![Step 3](../images/ScheduledNotebook/step3.png)<br/>
![Step 4](../images/ScheduledNotebook/step4.png)<br/>
![Step 5](../images/ScheduledNotebook/step5.png)<br/>
3. Delete all existing cells, except the title
![Step 6](../images/ScheduledNotebook/step6.png)<br/>
4. Navigate to Files > home and add (upload) myNotebookScript.py
![Step 7](../images/ScheduledNotebook/step7.png)<br/>
5. Add a new cell and add "import sys" and  the path to home folder
6. Add another cell and add "import myNotebookScript"
![Step 8](../images/ScheduledNotebook/step8.png)<br/>
7. Add another cell and add a line of code to execute one function in the Python script
8. Add another cell and add a line of code to execute the complete Python script (by calling the function "RunCompleteScript")
![Step 9](../images/ScheduledNotebook/step9.png)<br/>
9. Create a task and call it "Execute Script"
![Step 10](../images/ScheduledNotebook/step10.png)<br/>
10. Add the parameters "username" and "password" to the task. This allows you to pass variables into the script, so you don't have to store a username and password in the script itself
![Step 11](../images/ScheduledNotebook/step11.png)<br/>
11. Set a schedule for the task
![Step 12](../images/ScheduledNotebook/step12.png)<br/>
12. Save the task
![Step 13](../images/ScheduledNotebook/step13.png)<br/>
<br>
The task will now run at whatever schedule you have chosen. The minimum interval is 15 minutes, so you can't run the script more often than that.
<br>
<br>
By clicking on the task you reveal all runs.
![Step 14](../images/ScheduledNotebook/step14.png)<br/>
<br>
By clicking on the results of a run you reveal the executed Notebook, which itself has executed your Python script.
![Step 15](../images/ScheduledNotebook/step15.png)<br/>