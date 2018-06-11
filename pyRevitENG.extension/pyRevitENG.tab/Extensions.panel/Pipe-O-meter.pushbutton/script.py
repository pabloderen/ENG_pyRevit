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


logger = script.get_logger()
logger.set_quiet_mode()

import clr
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI') 
from Autodesk.Revit.DB import * 
from Autodesk.Revit.UI import * 
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument

logger.reset_level()
