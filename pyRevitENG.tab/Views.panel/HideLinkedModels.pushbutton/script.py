"""
Hide Linked Models
Version: 1.0
Date : 06/08/18
Autor: Pablo Derendinger 
pyrevit: 4.5
"""

__title__ = 'Hide Linked Models'


from pyrevit import script
#Import pyRevit form library

import clr
clr.AddReference('RevitAPI') 
from Autodesk.Revit.DB import * 
from Autodesk.Revit.DB import Category

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

logger = script.get_logger()
logger.set_quiet_mode()

collector = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_RvtLinks).ToElements()
cat = None
for i in collector:
    cat = i.Category
if cat is not None:
    t = Transaction(doc,'Hide Links')
    t.Start()
    doc.ActiveView.HideCategoryTemporary(cat.Id)
    t.Commit()

logger.reset_level()
