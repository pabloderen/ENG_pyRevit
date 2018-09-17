"""Show one side grid bubbles in the active view."""

from pyrevit import revit, DB


__min_revit_ver__ = 2016


grids = DB.FilteredElementCollector(revit.doc)\
          .OfCategory(DB.BuiltInCategory.OST_Grids)\
          .WhereElementIsNotElementType().ToElements()

with revit.Transaction('Show one side Grid Bubbles'):
      
    for grid in grids:
        try:  
            grid.HideBubbleInView(DB.DatumEnds.End0, revit.activeview)
            grid.ShowBubbleInView(DB.DatumEnds.End1, revit.activeview)
            
        except Exception:
            pass

revit.uidoc.RefreshActiveView()
