"""
Changes Family/Types names to uppercase
Version: 1.0
Date : 06/08/18
Autor: Pablo Derendinger 
pyrevit: 4.5
"""

__title__ = 'Changes Family Name'


from pyrevit import script
from pyrevit.extensions import extensionmgr
#Import pyRevit form library
from pyrevit.forms import *


logger = script.get_logger()
logger.set_quiet_mode()

import clr
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI') 
from Autodesk.Revit.DB import * 
from Autodesk.Revit.UI import * 
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

def changeFamilyNames():
    '''Changes Family names to uppercase'''
    t = Transaction(doc, 'Rename Families to uppercase')
    t.Start()
    collector = FilteredElementCollector(doc).OfClass(Family).ToElements()
    for i in collector:
        #rename family
        print(i.Name + "  Changet to ;:   " + i.Name.upper() +" " + str(i.Id))
        i.Name = i.Name.upper()
    t.Commit()

def changeTypeNames():
    '''Changes Types names to uppercase'''
    tr = Transaction(doc, 'Rename Types to uppercase')
    tr.Start()
    collector = FilteredElementCollector(doc).OfClass(ElementType).ToElements()
    for i in collector:
        #rename type
        try:
            name = i.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
            i.Name = name.upper()
            print(name + "  Changet to :   " + name.upper() +" " + str(i.Id))
        except Exception as ex:
           print(str(ex))

            
    tr.Commit()




#Call pyRevit command switch to show properties
ops = ['Change Families', 'Change Types', 'Change both', 'Cancel']

optSelected = CommandSwitchWindow.show(ops, message='Select Option')



if optSelected == "Cancel":
    logger.reset_level()
elif optSelected == 'Change Families':
    changeFamilyNames()
elif optSelected == 'Change Types':
    changeTypeNames()

logger.reset_level()
