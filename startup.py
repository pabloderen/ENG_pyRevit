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

import time
import sqlite3
import os
from os import path

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference('AdWindows')
clr.AddReference('UIFramework')
clr.AddReference('UIFrameworkServices')
clr.AddReference('Newtonsoft.Json')

import Autodesk.Revit.DB.Events as Event

import Autodesk.Revit.DB as DB
import Autodesk.Revit.UI as UI

app = __revit__.Application

#Try to create the db if does not exists


def SaveChangeJournal(sender, event):
    '''Save journal of elements changed during document edition'''
    DBpath = os.path.expanduser(r'~\log.sqlite')
    conn = sqlite3.connect(DBpath)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS elements
                (date text, username text, document text, action text, id INTEGER, category text, length real, comment text )''')
    try:
        outputString= []
        docName, categoryName , userName ,comment= "","","",""
        
        date = int(time.time())
        doc = __revit__.ActiveUIDocument.Document
        
        
        try:
            docName = doc.Title
            userName = app.Username
        
        except:
            pass
        #Look for elements created in last event
        AddedElementsIds  = event.GetAddedElementIds()
        for i in AddedElementsIds:
            action = "Added"
            element= doc.GetElement(i)
            try:
                categoryName = element.Category.Name
            except:
                pass
            try:
                if "Pipes" in categoryName:
                    length = element.LookupParameter('Length').AsDouble()
                    comment  = ""
                    c.execute("INSERT INTO elements VALUES ('%s','%s','%s','%s',%s,'%s',%s,'%s')"
                    % (date, userName, docName, action, i, categoryName, length, comment))
                    conn.commit()
                elif "Pipe Fitting" in categoryName:
                    length =0
                    comment = element.LookupParameter('Size').AsString()
                    c.execute("INSERT INTO elements VALUES ('%s','%s','%s','%s',%s,'%s',%s,'%s')"
                    % (date, userName, docName, action, i, categoryName, length, comment))
                    conn.commit()
            except:
                pass
        

    except Exception as ex:
        erroLog = os.path.expanduser(r'~\error.log')
        with open(erroLog, 'a') as file:
            file.write(str(ex))
            #Closing the connections in case something fails
    conn.close()       
        
app.DocumentChanged += SaveChangeJournal
