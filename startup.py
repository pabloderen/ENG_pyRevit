"""Example of IronPython script to be executed by pyRevit on extension load

The script filename must end in startup.py

To Test:
- rename file to startup.py
- reload pyRevit: pyRevit will run this script after successfully
  created the DLL for the extension.

pyRevit runs the startup script in a dedicated IronPython engine and output
window. Thus the startup script is isolated and can not hurt the load process.
All errors will be printed to the dedicated output window similar to the way
errors are printed from pyRevit commands.
"""

# with open(r'C:\Temp\test.txt', 'w') as f:
#     f.write('test')

from pyrevit.framework import clr


clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference('AdWindows')
clr.AddReference('UIFramework')
clr.AddReference('UIFrameworkServices')
clr.AddReference('Newtonsoft.Json')

import Autodesk.Revit.DB.Events as Event

import Autodesk.Revit.DB as DB
import Autodesk.Revit.UI as UI
import time
from os import path

app = __revit__.Application

def SaveChangeJournal(sender, event):
    '''Save journal of elements changed during document edition'''
    
    outputString= []
    docName = ""
    userName = ""
    date = int(time.time())
    doc = __revit__.ActiveUIDocument.Document
    comment = ""
    try:
        docName = doc.Title
        userName = app.Username
    
    except:
        pass
    #Look for elements created in last event
    AddedElementsIds  = event.GetAddedElementIds()
    for i in AddedElementsIds:
        element= doc.GetElement(i)
        categoryName = element.Category.Name
        if "Pipes" in categoryName:
            comment = element.LookupParameter('Length').AsDouble()
            s = "%s,%s, %s, %s, %s, %s, %s" % (date, userName, docName,"Added",str(i),categoryName ,comment)
            outputString.append(s)
        elif "Pipe Fitting" in categoryName:
            comment = element.LookupParameter('Size').AsString()
            s = "%s,%s, %s, %s, %s, %s, %s" % (date, userName, docName,"Added",str(i),categoryName ,comment)
            outputString.append(s)

    
    # #Look for elements modified in last event
    # ModifiedElementsIds  = event.GetModifiedElementIds()
    # for i in ModifiedElementsIds:
    #     element= doc.GetElement(i)
    #     categoryName = element.Category.Name
    #     if  categoryName is "Pipes" or categoryName is "Duct":
    #         comment = element.LookupParameter('Length').AsDouble()
    #     s = "%s,%s, %s, %s, %s, %s, %s" % (date, userName, docName,"Added",str(i),categoryName ,comment)
    #     outputString.append(s)

    ##TODO: find a way to retrieve delete element information
    # DeletedElementsIds  = event.GetDeletedElementIds()
    # for i in DeletedElementsIds:
    #     s = "%s,%s, %s, %s, %s" % (date, userName, docName,"Deleted",str(i))
    #     outputString.append(s)
    
    filepath = path.expanduser('~\Output.txt')
    
    with open(filepath, "a") as text_file:
        for l in outputString:
            print(l)
            text_file.write(l + "\n")
        text_file.close()

app.DocumentChanged += SaveChangeJournal


#print('Startup script execution test.')
