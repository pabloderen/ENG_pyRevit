"""
Changes Select FabParts with half radius
Version: 1.0
Date : 06/15/18
Autor: Pablo Derendinger 
pyrevit: 4.5
"""

__title__ = 'Select FabParts with half radius'
from pyrevit import script
#Import pyRevit form library
import clr
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI') 
from Autodesk.Revit.DB import * 
from math import pi, degrees
from System.Collections.Generic import List

app = __revit__.Application
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

logger = script.get_logger()
logger.set_quiet_mode()

def selectLinkedElement():
    """Selects FabParts Fittings that have a radius different than the diameter"""

    collector = FilteredElementCollector(doc).ToElementIds()
    wrongAngle = []
    for id in collector:
        
        element= doc.GetElement(id)

        if element.get_Parameter(BuiltInParameter.FABRICATION_PART_ANGLE) is not None:
            try:
                chord = element.CenterlineLength
                angle = element.get_Parameter(BuiltInParameter.FABRICATION_PART_ANGLE).AsDouble()
                angle = degrees(angle)
                diameter = element.get_Parameter(BuiltInParameter.FABRICATION_PART_DIAMETER_IN).AsDouble()
                radius = ((360/angle)*chord )/(pi*2)
                        
                if round(radius,4) == round(diameter,4):
                    wrongAngle.append(id)

            except Exception as ex:
                print(ex, str(id))
                pass

    wrongAngle = List[ElementId](wrongAngle)
    uidoc.Selection.SetElementIds(wrongAngle)

    
id = selectLinkedElement()


logger.reset_level()

