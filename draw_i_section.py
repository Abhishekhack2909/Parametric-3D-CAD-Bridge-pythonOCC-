"""
I-section beam factory function (placeholder for Osdag module).
Creates a steel I-beam with specified dimensions.
"""

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax2, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Trsf


def create_i_section(d, bf, tf, tw, length):
    """
    Create an I-section beam.
    
    Parameters:
    -----------
    d : float
        Total depth of I-section (mm)
    bf : float
        Flange width (mm)
    tf : float
        Flange thickness (mm)
    tw : float
        Web thickness (mm)
    length : float
        Extrusion length along X-axis (mm)
    
    Returns:
    --------
    TopoDS_Shape
        I-beam solid extruded along X-axis
    """
    # Create top flange
    top_flange = BRepPrimAPI_MakeBox(
        gp_Pnt(0, -bf/2, d - tf),
        length, bf, tf
    ).Shape()
    
    # Create web
    web = BRepPrimAPI_MakeBox(
        gp_Pnt(0, -tw/2, 0),
        length, tw, d
    ).Shape()
    
    # Create bottom flange
    bottom_flange = BRepPrimAPI_MakeBox(
        gp_Pnt(0, -bf/2, 0),
        length, bf, tf
    ).Shape()
    
    # Fuse all parts together
    i_section = BRepAlgoAPI_Fuse(top_flange, web).Shape()
    i_section = BRepAlgoAPI_Fuse(i_section, bottom_flange).Shape()
    
    return i_section
