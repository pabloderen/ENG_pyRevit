"""
Hide Point Cloud
Version: 1.0
Date : 06/08/18
Autor: Pablo Derendinger 
pyrevit: 4.5
"""

__title__ = 'Hide Point Cloud'


from pyrevit import script
#Import pyRevit form library

import clr
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI') 
from Autodesk.Revit.DB import * 
from Autodesk.Revit.DB import Category
from Autodesk.Revit.UI import * 
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

logger = script.get_logger()
logger.set_quiet_mode()

collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_PointClouds).ToElements()
cat = None
for i in collector:
    cat = i.Category
if cat is not None:
    t = Transaction(doc,'hide cloud')
    t.Start()
    doc.ActiveView.HideCategoryTemporary(cat.Id)
    t.Commit()

logger.reset_level()
