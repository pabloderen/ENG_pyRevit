"""
Draw line from coordinates
Version: 1.0
Date : 06/25/18
Autor: Pablo Derendinger 
pyrevit: 4.5
"""

__title__ = 'Draw line from spots'


from pyrevit import script
#Import pyRevit form library

import clr
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI') 
from Autodesk.Revit.DB import * 
from Autodesk.Revit.DB import Category
from Autodesk.Revit.UI import * 
import sys
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
from Autodesk.Revit.UI.Selection import ObjectType
import math



def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin.X,origin.Y
    px, py = point.X, point.Y

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return XYZ(qx, qy,0)

#Project locations
locations = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_ProjectBasePoint)

#Real world Coordinates
originPBP = XYZ(0,0,0)
RevitZeroRelativeToPBP=None
angle = 0
for locationPoint in locations:
    svLoc = locationPoint.Location
    projectSurvpntX = locationPoint.get_Parameter(BuiltInParameter.BASEPOINT_EASTWEST_PARAM).AsDouble()
    projectSurvpntY = locationPoint.get_Parameter(BuiltInParameter.BASEPOINT_NORTHSOUTH_PARAM).AsDouble()
    projectSurvpntZ = locationPoint.get_Parameter(BuiltInParameter.BASEPOINT_ELEVATION_PARAM).AsDouble()
    bbox = locationPoint.get_BoundingBox(doc.ActiveView)
    print( bbox.Max.X, bbox.Max.Y)
    print(projectSurvpntX,projectSurvpntY)
    angle = locationPoint.get_Parameter(BuiltInParameter.BASEPOINT_ANGLETON_PARAM).AsDouble()
    print(angle)
    RevitZeroRelativeToPBP  = XYZ(projectSurvpntX,projectSurvpntY,0)
    originPBP = XYZ(projectSurvpntX -bbox.Min.X ,projectSurvpntY-bbox.Min.Y,0) 


# define start and end for bound line
Xinput = raw_input("Enter X coordinates")
Yinput = raw_input("Enter Y coordinates")
startPoint =  XYZ( float(Xinput),float(Yinput), 0)


origin = XYZ.Zero
startPoint =   rotate(RevitZeroRelativeToPBP,startPoint,angle) - originPBP


reference = uidoc.Selection.PickObject(ObjectType.Element)

typeId = doc.GetElement(reference).GetTypeId()
ty =doc.GetElement(typeId)

t = Transaction(doc, "Draw line")
t.Start()
dt= doc.Create.PlaceGroup(startPoint, ty)
t.Commit()