"""
Pile and pile cap geometry components for bridge model.
"""

from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.TopoDS import TopoDS_Shape

# Import provided rectangular prism function
from draw_rectangular_prism import create_rectangular_prism


def create_pile(diameter, length):
    """
    Create a circular pile (column) using a cylinder.
    
    Piles are vertical cylindrical elements that extend downward from the pile cap
    to provide foundation support.
    
    Parameters:
    -----------
    diameter : float
        Diameter of the pile in mm
    length : float
        Length of the pile extending downward in mm
    
    Returns:
    --------
    TopoDS_Shape
        Cylinder solid representing the pile
    """
    radius = diameter / 2.0
    
    # Create cylinder along Z-axis (downward) at origin
    axis = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
    cylinder = BRepPrimAPI_MakeCylinder(axis, radius, length).Shape()
    
    return cylinder


def create_pile_cap(length, width, depth):
    """
    Create a rectangular pile cap.
    
    The pile cap is a thick concrete slab that distributes loads from the pier
    to multiple piles.
    
    Parameters:
    -----------
    length : float
        Length of pile cap along X-axis in mm
    width : float
        Width of pile cap along Y-axis in mm
    depth : float
        Depth/thickness of pile cap along Z-axis in mm
    
    Returns:
    --------
    TopoDS_Shape
        Rectangular box solid representing the pile cap
    """
    # Use the provided rectangular prism function
    # Width along Y, depth along Z, length along X
    pile_cap = create_rectangular_prism(width, depth, length)
    
    return pile_cap
