"""
Changes Select FabParts with half radius
Version: 1.0
Date : 06/15/18
Autor: Pablo Derendinger 
pyrevit: 4.5
"""

__title__ = 'Select FabParts with half radius'

import clr
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI') 
from Autodesk.Revit.DB import * 
from math import pi, degrees
from System.Collections.Generic import List
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument

logger = script.get_logger()
logger.set_quiet_mode()

def selectLinkedElement():
    """Selects FabParts Fittings that have a radius different than the diameter"""

    collector = FilteredElementCollector(doc).OfClass(FabricationPart).ToElementIds()
    wrongAngle = []
    for id in collector:
        element= doc.GetElement(id)
        chord = element.CenterlineLength
        angle = element.get_Parameter(BuiltInParameter.FABRICATION_PART_ANGLE).AsDouble()
        angle = degrees(angle)
        diameter = element.get_Parameter(BuiltInParameter.FABRICATION_PART_DIAMETER_IN).AsDouble()
        radius = ((360/angle)*chord )/(pi*2)
        print(diameter, radius, angle)
        if round(radius,4) == round(diameter,4):
            wrongAngle.append(id)

    wrongAngle = List[ElementId](wrongAngle)
    uidoc.Selection.SetElementIds(wrongAngle)

    
id = selectLinkedElement()


logger.reset_level()

