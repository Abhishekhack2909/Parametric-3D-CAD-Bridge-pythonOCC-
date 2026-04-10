"""
Rectangular prism factory function (placeholder for Osdag module).
Creates a rectangular box solid.
"""

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox


def create_rectangular_prism(width, height, length):
    """
    Create a rectangular prism (box).
    
    Parameters:
    -----------
    width : float
        Dimension along Y-axis (mm)
    height : float
        Dimension along Z-axis (mm)
    length : float
        Dimension along X-axis (mm)
    
    Returns:
    --------
    TopoDS_Shape
        Rectangular box solid
    """
    # Create box at origin
    # Box extends from (0, 0, 0) to (length, width, height)
    box = BRepPrimAPI_MakeBox(
        gp_Pnt(0, 0, 0),
        length, width, height
    ).Shape()
    
    return box
