"""
Pier and pier cap geometry components for bridge model.
"""

from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir, gp_Vec
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeBox
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_ThruSections
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Trsf
from OCC.Core.TopoDS import TopoDS_Shape
import math


def create_circular_pier(diameter, height):
    """
    Create a circular pier (column) using a cylinder.
    
    Parameters:
    -----------
    diameter : float
        Diameter of the circular pier in mm
    height : float
        Height of the pier column in mm
    
    Returns:
    --------
    TopoDS_Shape
        Cylinder solid representing the pier
    """
    radius = diameter / 2.0
    
    # Create cylinder along Z-axis at origin
    axis = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
    cylinder = BRepPrimAPI_MakeCylinder(axis, radius, height).Shape()
    
    return cylinder


def create_trapezoidal_pier_cap(length, top_width, bottom_width, depth):
    """
    Create a trapezoidal/hammerhead pier cap.
    
    This creates a pier cap that is wider at the top than at the bottom,
    resembling a hammerhead shape when viewed from the side.
    
    Parameters:
    -----------
    length : float
        Length of pier cap along X-axis in mm
    top_width : float
        Width at top (along Y-axis) in mm
    bottom_width : float
        Width at bottom (along Y-axis) in mm
    depth : float
        Height/depth of pier cap (along Z-axis) in mm
    
    Returns:
    --------
    TopoDS_Shape
        Trapezoidal solid representing the pier cap
    
    Note:
    -----
    This implementation uses a simplified box approximation.
    For a true trapezoidal shape, a loft between two rectangular profiles
    could be implemented using BRepOffsetAPI_ThruSections.
    """
    # Simplified implementation using a box with average width
    # This can be improved later with proper lofting for trapezoidal shape
    
    # Use average width for simplified box representation
    avg_width = (top_width + bottom_width) / 2.0
    
    # Create box centered at origin
    # Length along X, width along Y, depth along Z
    box = BRepPrimAPI_MakeBox(
        gp_Pnt(-length / 2, -avg_width / 2, 0),
        length,
        avg_width,
        depth
    ).Shape()
    
    # Note: For a more accurate trapezoidal shape, implement lofting:
    # 1. Create bottom rectangle wire at z=0 with bottom_width
    # 2. Create top rectangle wire at z=depth with top_width
    # 3. Use BRepOffsetAPI_ThruSections to loft between them
    
    return box


def create_trapezoidal_pier_cap_lofted(length, top_width, bottom_width, depth):
    """
    Create a true trapezoidal pier cap using lofting (advanced implementation).
    
    This creates a proper trapezoidal shape by lofting between two rectangular profiles.
    
    Parameters:
    -----------
    length : float
        Length of pier cap along X-axis in mm
    top_width : float
        Width at top (along Y-axis) in mm
    bottom_width : float
        Width at bottom (along Y-axis) in mm
    depth : float
        Height/depth of pier cap (along Z-axis) in mm
    
    Returns:
    --------
    TopoDS_Shape
        Trapezoidal solid representing the pier cap
    """
    try:
        # Create bottom rectangle (wider)
        bottom_pts = [
            gp_Pnt(-length / 2, -top_width / 2, depth),
            gp_Pnt(length / 2, -top_width / 2, depth),
            gp_Pnt(length / 2, top_width / 2, depth),
            gp_Pnt(-length / 2, top_width / 2, depth),
            gp_Pnt(-length / 2, -top_width / 2, depth)  # Close the wire
        ]
        
        bottom_edges = []
        for i in range(len(bottom_pts) - 1):
            edge = BRepBuilderAPI_MakeEdge(bottom_pts[i], bottom_pts[i + 1]).Edge()
            bottom_edges.append(edge)
        
        bottom_wire_builder = BRepBuilderAPI_MakeWire()
        for edge in bottom_edges:
            bottom_wire_builder.Add(edge)
        bottom_wire = bottom_wire_builder.Wire()
        
        # Create top rectangle (narrower)
        top_pts = [
            gp_Pnt(-length / 2, -bottom_width / 2, 0),
            gp_Pnt(length / 2, -bottom_width / 2, 0),
            gp_Pnt(length / 2, bottom_width / 2, 0),
            gp_Pnt(-length / 2, bottom_width / 2, 0),
            gp_Pnt(-length / 2, -bottom_width / 2, 0)  # Close the wire
        ]
        
        top_edges = []
        for i in range(len(top_pts) - 1):
            edge = BRepBuilderAPI_MakeEdge(top_pts[i], top_pts[i + 1]).Edge()
            top_edges.append(edge)
        
        top_wire_builder = BRepBuilderAPI_MakeWire()
        for edge in top_edges:
            top_wire_builder.Add(edge)
        top_wire = top_wire_builder.Wire()
        
        # Loft between the two wires
        loft = BRepOffsetAPI_ThruSections(True)  # True = create solid
        loft.AddWire(top_wire)
        loft.AddWire(bottom_wire)
        loft.Build()
        
        if loft.IsDone():
            return loft.Shape()
        else:
            # Fallback to simple box if lofting fails
            return create_trapezoidal_pier_cap(length, top_width, bottom_width, depth)
    
    except Exception as e:
        print(f"Warning: Lofting failed ({e}), using simplified box approximation")
        return create_trapezoidal_pier_cap(length, top_width, bottom_width, depth)
