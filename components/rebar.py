"""
Reinforcement bar (rebar) geometry components for bridge model.
"""

import math
from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir, gp_Vec, gp_Trsf
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.TopoDS import TopoDS_Shape


def create_rebar_bar(diameter, length):
    """
    Create a single reinforcement bar as a cylinder.
    
    Parameters:
    -----------
    diameter : float
        Diameter of the rebar in mm
    length : float
        Length of the rebar in mm
    
    Returns:
    --------
    TopoDS_Shape
        Cylinder solid representing a single rebar
    """
    radius = diameter / 2.0
    
    # Create cylinder along X-axis at origin
    axis = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0))
    cylinder = BRepPrimAPI_MakeCylinder(axis, radius, length).Shape()
    
    return cylinder


def create_rebar_grid_in_deck(deck_width, span_length, cover, bar_diam, spacing):
    """
    Create a grid of reinforcement bars inside the deck slab.
    
    The grid consists of:
    - Longitudinal bars running along X-axis (span direction)
    - Transverse bars running along Y-axis (width direction)
    
    All bars are placed at z = cover from the bottom of the deck.
    
    Parameters:
    -----------
    deck_width : float
        Total width of deck along Y-axis in mm
    span_length : float
        Total span length along X-axis in mm
    cover : float
        Concrete cover (distance from deck bottom to rebar center) in mm
    bar_diam : float
        Diameter of rebar in mm
    spacing : float
        Spacing between parallel bars in mm
    
    Returns:
    --------
    list of TopoDS_Shape
        List of cylinder solids representing all rebar in the deck
    """
    rebar_list = []
    
    # Longitudinal bars (running along X-axis, span direction)
    # These bars are spaced along the Y-axis
    n_longitudinal = int(deck_width / spacing) + 1
    
    for i in range(n_longitudinal):
        y_pos = i * spacing
        
        # Create bar along X-axis
        bar = create_rebar_bar(bar_diam, span_length)
        
        # Position at (0, y_pos, cover)
        transform = gp_Trsf()
        transform.SetTranslation(gp_Vec(0, y_pos, cover))
        bar_positioned = BRepBuilderAPI_Transform(bar, transform, False).Shape()
        
        rebar_list.append(bar_positioned)
    
    # Transverse bars (running along Y-axis, width direction)
    # These bars are spaced along the X-axis
    n_transverse = int(span_length / spacing) + 1
    
    for i in range(n_transverse):
        x_pos = i * spacing
        
        # Create bar along Y-axis (rotate from X-axis)
        bar_x = create_rebar_bar(bar_diam, deck_width)
        
        # Rotate 90 degrees around Z-axis to align with Y-axis
        transform_rot = gp_Trsf()
        transform_rot.SetRotation(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)).Axis(), math.pi / 2)
        bar_y = BRepBuilderAPI_Transform(bar_x, transform_rot, False).Shape()
        
        # Position at (x_pos, 0, cover + bar_diam)
        # Offset slightly in Z to avoid overlap with longitudinal bars
        transform_trans = gp_Trsf()
        transform_trans.SetTranslation(gp_Vec(x_pos, 0, cover + bar_diam))
        bar_positioned = BRepBuilderAPI_Transform(bar_y, transform_trans, False).Shape()
        
        rebar_list.append(bar_positioned)
    
    return rebar_list


def create_rebar_cage_in_pier(pier_diameter, pier_height, main_diam, n_main_bars, 
                               tie_diam, tie_spacing, cover):
    """
    Create a reinforcement cage inside a circular pier.
    
    The cage consists of:
    - Longitudinal bars arranged in a circle (main reinforcement)
    - Circular tie bars (stirrups) at regular spacing along height
    
    Parameters:
    -----------
    pier_diameter : float
        Diameter of the pier in mm
    pier_height : float
        Height of the pier in mm
    main_diam : float
        Diameter of longitudinal bars in mm
    n_main_bars : int
        Number of longitudinal bars arranged in a circle
    tie_diam : float
        Diameter of tie bars (stirrups) in mm
    tie_spacing : float
        Vertical spacing between tie bars in mm
    cover : float
        Concrete cover (distance from pier surface to rebar center) in mm
    
    Returns:
    --------
    list of TopoDS_Shape
        List of cylinder solids representing all rebar in the pier
    """
    rebar_list = []
    
    # Radius of the circle on which longitudinal bars are placed
    rebar_circle_radius = (pier_diameter / 2.0) - cover - (main_diam / 2.0)
    
    # Longitudinal bars (vertical bars along pier height)
    for i in range(n_main_bars):
        angle = (2 * math.pi * i) / n_main_bars
        x_pos = rebar_circle_radius * math.cos(angle)
        y_pos = rebar_circle_radius * math.sin(angle)
        
        # Create vertical bar along Z-axis
        bar_z = create_rebar_bar(main_diam, pier_height)
        
        # Rotate to align with Z-axis (from X-axis)
        transform_rot = gp_Trsf()
        transform_rot.SetRotation(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0)).Axis(), math.pi / 2)
        bar_vertical = BRepBuilderAPI_Transform(bar_z, transform_rot, False).Shape()
        
        # Position at (x_pos, y_pos, 0)
        transform_trans = gp_Trsf()
        transform_trans.SetTranslation(gp_Vec(x_pos, y_pos, 0))
        bar_positioned = BRepBuilderAPI_Transform(bar_vertical, transform_trans, False).Shape()
        
        rebar_list.append(bar_positioned)
    
    # Circular tie bars (horizontal rings at regular spacing)
    tie_circle_radius = rebar_circle_radius
    n_ties = int(pier_height / tie_spacing) + 1
    
    # Approximate circular ties with octagonal rings (8 segments)
    n_segments = 8
    segment_length = 2 * tie_circle_radius * math.sin(math.pi / n_segments)
    
    for tie_level in range(n_ties):
        z_pos = tie_level * tie_spacing
        
        # Create octagonal ring approximation
        for seg in range(n_segments):
            angle_start = (2 * math.pi * seg) / n_segments
            angle_end = (2 * math.pi * (seg + 1)) / n_segments
            
            x_start = tie_circle_radius * math.cos(angle_start)
            y_start = tie_circle_radius * math.sin(angle_start)
            x_end = tie_circle_radius * math.cos(angle_end)
            y_end = tie_circle_radius * math.sin(angle_end)
            
            # Calculate segment length and angle
            dx = x_end - x_start
            dy = y_end - y_start
            seg_length = math.sqrt(dx**2 + dy**2)
            seg_angle = math.atan2(dy, dx)
            
            # Create horizontal bar segment
            bar_seg = create_rebar_bar(tie_diam, seg_length)
            
            # Rotate to align with segment direction
            transform_rot = gp_Trsf()
            transform_rot.SetRotation(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)).Axis(), seg_angle)
            bar_rotated = BRepBuilderAPI_Transform(bar_seg, transform_rot, False).Shape()
            
            # Rotate to horizontal plane (around Y-axis)
            transform_rot2 = gp_Trsf()
            transform_rot2.SetRotation(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0)).Axis(), math.pi / 2)
            bar_horizontal = BRepBuilderAPI_Transform(bar_rotated, transform_rot2, False).Shape()
            
            # Position at segment start point
            transform_trans = gp_Trsf()
            transform_trans.SetTranslation(gp_Vec(x_start, y_start, z_pos))
            bar_positioned = BRepBuilderAPI_Transform(bar_horizontal, transform_trans, False).Shape()
            
            rebar_list.append(bar_positioned)
    
    return rebar_list
