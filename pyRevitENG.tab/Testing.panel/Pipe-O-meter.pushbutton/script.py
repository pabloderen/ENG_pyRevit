"""
Pipe-O-meter
Version: 1.0
Date : 06/10/18
Autor: Pablo Derendinger 
pyrevit: 4.5
"""

__title__ = 'Pipe-O-meter'


from pyrevit import script
from pyrevit.extensions import extensionmgr
from os import path

logger = script.get_logger()
logger.set_quiet_mode()

# import clr
# clr.AddReference('RevitAPI') 
# clr.AddReference('RevitAPIUI') 
# from Autodesk.Revit.DB import * 
# from Autodesk.Revit.UI import * 
# app = __revit__.Application
# uidoc = __revit__.ActiveUIDocument

filepath = path.expanduser('~\Output.txt')

with open(filepath, "r") as text_file:
    text = text_file.readlines()
    for l in text:
        print(l)

logger.reset_level()
