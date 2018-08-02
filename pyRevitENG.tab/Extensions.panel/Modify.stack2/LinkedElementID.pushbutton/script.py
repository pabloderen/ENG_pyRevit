"""
Gets the id number of a linked element
Version: 1.0
Date : 06/06/18
Autor: Pablo Derendinger 
pyrevit: 4.5
"""

__title__ = 'Get Linked element id'


from pyrevit import script
from pyrevit.extensions import extensionmgr


logger = script.get_logger()
logger.set_quiet_mode()

import clr
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI') 
from Autodesk.Revit.DB import * 
from Autodesk.Revit.UI import * 
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument


def selectLinkedElement():
    """Returns the id as an INT of an element selected from a Linked File
    
    Return: Element Id as int
    """
    #Import ObjectType
    from Autodesk.Revit.UI.Selection import ObjectType
    #Invoke selection method
    choices = uidoc.Selection
    #Execute method
    hasPickOne = choices.PickObject(ObjectType.LinkedElement)
    if hasPickOne is not None:
        return hasPickOne.LinkedElementId.IntegerValue

id = selectLinkedElement()
#Copy id to clipboard
script.clipboard_copy(str(id))
TaskDialog.Show("Id",str(id))

logger.reset_level()
