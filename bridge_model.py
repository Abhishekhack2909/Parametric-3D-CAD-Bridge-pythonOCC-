"""
3D Bridge Model using pythonocc-core 7.9.3
A parametric short-span steel girder bridge with concrete deck, pier, piles, and rebar.
"""

import sys
import math
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax2, gp_Dir, gp_Trsf
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeBox
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Core.BRep import BRep_Builder
from OCC.Display.SimpleGui import init_display
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB

# Import provided functions
from draw_i_section import create_i_section
from draw_rectangular_prism import create_rectangular_prism

# Import component factory functions
from components.pier import create_circular_pier, create_trapezoidal_pier_cap
from components.pile import create_pile, create_pile_cap
from components.rebar import (
    create_rebar_bar,
    create_rebar_grid_in_deck,
    create_rebar_cage_in_pier
)

# ================================================================
# ALL PARAMETERS (in millimetres)
# ================================================================

# ---- UNITS ----
# All values are in millimetres (mm)

# ---- SPAN & LAYOUT ----
span_length_L = 12000           # total bridge span length
n_girders = 3                   # number of I-section girders
girder_centroid_spacing = 3000  # center-to-center spacing between girders
deck_overhang = 500             # deck extends this much beyond outer girders

# ---- GIRDER (I-SECTION) ----
girder_section_d = 900          # depth of I-section
girder_section_bf = 300         # flange width
girder_section_tf = 16          # flange thickness
girder_section_tw = 10          # web thickness
girder_length = 12000           # same as span_length_L

# ---- DECK SLAB ----
deck_width = 7000               # total width of deck
deck_thickness = 200            # thickness of deck slab
deck_cover = 40                 # concrete cover for rebar

# ---- PIER ----
pier_diameter = 800             # diameter of circular pier
pier_height = 3000              # height of pier column

# ---- PIER CAP ----
pier_cap_length = 7000          # full length of pier cap
pier_cap_top_width = 3000       # width at top (hammerhead shape)
pier_cap_bottom_width = 1200    # width at bottom
pier_cap_depth = 600            # height/depth of pier cap

# ---- PILE CAP ----
pile_cap_length = 2200          # length of pile cap
pile_cap_width = 1200           # width of pile cap
pile_cap_depth = 600            # depth/thickness of pile cap

# ---- PILES ----
n_piles_per_cap = 4             # number of piles (arranged in 2x2 grid)
pile_diameter = 400             # diameter of each pile
pile_length = 5000              # length of each pile going down
pile_spacing = 600              # spacing between pile centres

# ---- REINFORCEMENT BARS (REBAR) ----
rebar_main_diameter = 16        # diameter of longitudinal bars
rebar_transverse_diameter = 8   # diameter of stirrups/ties
rebar_spacing_longitudinal = 150  # spacing of longitudinal bars
rebar_spacing_transverse = 200    # spacing of stirrups
rebar_cover = 40                  # concrete cover
rebar_visible = True              # show or hide rebar

# ---- VISUALIZATION ----
concrete_opacity = 0.35         # concrete is semi-transparent
steel_opacity = 1.0             # steel is fully opaque
rebar_opacity = 1.0             # rebar is fully opaque
show_axes = True
background_color = "white"

# ---- EXPORT ----
save_step = False
step_filename = "bridge_model.step"


# ================================================================
# ASSEMBLY FUNCTIONS
# ================================================================

def build_girders():
    """
    Create all I-section girders spaced along Y-axis.
    Returns list of TopoDS_Shape objects.
    """
    girders = []
    
    for i in range(n_girders):
        # Create I-section using provided function
        girder = create_i_section(
            girder_section_d,
            girder_section_bf,
            girder_section_tf,
            girder_section_tw,
            girder_length
        )
        
        # Position girder along Y-axis
        y_position = i * girder_centroid_spacing
        
        # Transform to position
        transform = gp_Trsf()
        transform.SetTranslation(gp_Vec(0, y_position, 0))
        girder_positioned = BRepBuilderAPI_Transform(girder, transform, False).Shape()
        
        girders.append(girder_positioned)
    
    return girders


def build_deck():
    """
    Create concrete deck slab on top of girders.
    Returns TopoDS_Shape.
    """
    # Create deck using provided function
    # Width along Y, thickness along Z, length along X
    deck = create_rectangular_prism(deck_width, deck_thickness, span_length_L)
    
    # Position on top of girders
    # Girders are at z=0, deck sits on top at z=girder_section_d
    transform = gp_Trsf()
    transform.SetTranslation(gp_Vec(0, 0, girder_section_d))
    deck_positioned = BRepBuilderAPI_Transform(deck, transform, False).Shape()
    
    return deck_positioned


def build_pier():
    """
    Create circular pier column below deck at mid-span.
    Returns TopoDS_Shape.
    """
    pier = create_circular_pier(pier_diameter, pier_height)
    
    # Position at center of span, center of deck width
    # Pier top connects to pier cap, which is below deck
    x_position = span_length_L / 2
    y_position = deck_width / 2
    z_position = -(pier_cap_depth + pier_height)  # Below pier cap
    
    transform = gp_Trsf()
    transform.SetTranslation(gp_Vec(x_position, y_position, z_position))
    pier_positioned = BRepBuilderAPI_Transform(pier, transform, False).Shape()
    
    return pier_positioned


def build_pier_cap():
    """
    Create trapezoidal pier cap on top of pier, below deck.
    Returns TopoDS_Shape.
    """
    pier_cap = create_trapezoidal_pier_cap(
        pier_cap_length,
        pier_cap_top_width,
        pier_cap_bottom_width,
        pier_cap_depth
    )
    
    # Position at center of span, below deck
    x_position = span_length_L / 2
    y_position = deck_width / 2
    z_position = -pier_cap_depth  # Just below deck level (z=0 is deck bottom)
    
    transform = gp_Trsf()
    transform.SetTranslation(gp_Vec(x_position, y_position, z_position))
    pier_cap_positioned = BRepBuilderAPI_Transform(pier_cap, transform, False).Shape()
    
    return pier_cap_positioned


def build_pile_cap():
    """
    Create rectangular pile cap below pier.
    Returns TopoDS_Shape.
    """
    pile_cap = create_pile_cap(pile_cap_length, pile_cap_width, pile_cap_depth)
    
    # Position below pier
    x_position = span_length_L / 2
    y_position = deck_width / 2
    z_position = -(pier_cap_depth + pier_height + pile_cap_depth)
    
    transform = gp_Trsf()
    transform.SetTranslation(gp_Vec(x_position, y_position, z_position))
    pile_cap_positioned = BRepBuilderAPI_Transform(pile_cap, transform, False).Shape()
    
    return pile_cap_positioned


def build_piles():
    """
    Create piles in 2x2 grid below pile cap.
    Returns list of TopoDS_Shape objects.
    """
    piles = []
    
    # 2x2 grid arrangement
    grid_positions = [
        (-pile_spacing / 2, -pile_spacing / 2),
        (pile_spacing / 2, -pile_spacing / 2),
        (-pile_spacing / 2, pile_spacing / 2),
        (pile_spacing / 2, pile_spacing / 2)
    ]
    
    for dx, dy in grid_positions:
        pile = create_pile(pile_diameter, pile_length)
        
        # Position below pile cap
        x_position = span_length_L / 2 + dx
        y_position = deck_width / 2 + dy
        z_position = -(pier_cap_depth + pier_height + pile_cap_depth + pile_length)
        
        transform = gp_Trsf()
        transform.SetTranslation(gp_Vec(x_position, y_position, z_position))
        pile_positioned = BRepBuilderAPI_Transform(pile, transform, False).Shape()
        
        piles.append(pile_positioned)
    
    return piles


def build_rebar():
    """
    Create reinforcement bars in deck and pier if rebar_visible is True.
    Returns list of TopoDS_Shape objects.
    """
    if not rebar_visible:
        return []
    
    rebar_shapes = []
    
    # Deck rebar grid
    deck_rebar = create_rebar_grid_in_deck(
        deck_width,
        span_length_L,
        rebar_cover,
        rebar_main_diameter,
        rebar_spacing_longitudinal
    )
    
    # Position deck rebar at deck level
    for rebar in deck_rebar:
        transform = gp_Trsf()
        transform.SetTranslation(gp_Vec(0, 0, girder_section_d))
        rebar_positioned = BRepBuilderAPI_Transform(rebar, transform, False).Shape()
        rebar_shapes.append(rebar_positioned)
    
    # Pier rebar cage
    n_main_bars = 8  # Number of longitudinal bars in circular arrangement
    pier_rebar = create_rebar_cage_in_pier(
        pier_diameter,
        pier_height,
        rebar_main_diameter,
        n_main_bars,
        rebar_transverse_diameter,
        rebar_spacing_transverse,
        rebar_cover
    )
    
    # Position pier rebar
    for rebar in pier_rebar:
        transform = gp_Trsf()
        x_position = span_length_L / 2
        y_position = deck_width / 2
        z_position = -(pier_cap_depth + pier_height)
        transform.SetTranslation(gp_Vec(x_position, y_position, z_position))
        rebar_positioned = BRepBuilderAPI_Transform(rebar, transform, False).Shape()
        rebar_shapes.append(rebar_positioned)
    
    return rebar_shapes


def assemble_bridge():
    """
    Assemble all bridge components with colors and transparency.
    Returns list of (shape, color, transparency) tuples.
    """
    components = []
    
    # Steel girders - steel grey, opaque
    print("Building girders...")
    girders = build_girders()
    steel_color = Quantity_Color(0.5, 0.5, 0.6, Quantity_TOC_RGB)
    steel_transparency = 1.0 - steel_opacity
    for girder in girders:
        components.append((girder, steel_color, steel_transparency))
    
    # Deck - concrete grey, semi-transparent
    print("Building deck...")
    deck = build_deck()
    deck_color = Quantity_Color(0.8, 0.8, 0.75, Quantity_TOC_RGB)
    concrete_transparency = 1.0 - concrete_opacity
    components.append((deck, deck_color, concrete_transparency))
    
    # Pier cap
    print("Building pier cap...")
    pier_cap = build_pier_cap()
    pier_cap_color = Quantity_Color(0.7, 0.7, 0.65, Quantity_TOC_RGB)
    components.append((pier_cap, pier_cap_color, concrete_transparency))
    
    # Pier - light blue, semi-transparent
    print("Building pier...")
    pier = build_pier()
    pier_color = Quantity_Color(0.6, 0.75, 0.9, Quantity_TOC_RGB)
    components.append((pier, pier_color, concrete_transparency))
    
    # Pile cap
    print("Building piles and pile cap...")
    pile_cap = build_pile_cap()
    pile_cap_color = Quantity_Color(0.7, 0.7, 0.65, Quantity_TOC_RGB)
    components.append((pile_cap, pile_cap_color, concrete_transparency))
    
    # Piles
    piles = build_piles()
    pile_color = Quantity_Color(0.7, 0.7, 0.65, Quantity_TOC_RGB)
    for pile in piles:
        components.append((pile, pile_color, concrete_transparency))
    
    # Rebar - red-brown, opaque
    print("Building rebar...")
    rebar_shapes = build_rebar()
    rebar_color = Quantity_Color(0.8, 0.2, 0.1, Quantity_TOC_RGB)
    rebar_transparency = 1.0 - rebar_opacity
    for rebar in rebar_shapes:
        components.append((rebar, rebar_color, rebar_transparency))
    
    return components


def export_to_step(components):
    """
    Export all components to STEP file if save_step is True.
    """
    if not save_step:
        return
    
    try:
        from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
        from OCC.Core.IFSelect import IFSelect_RetDone
        
        # Create compound
        builder = BRep_Builder()
        compound = TopoDS_Compound()
        builder.MakeCompound(compound)
        
        for shape, _, _ in components:
            builder.Add(compound, shape)
        
        # Write to STEP
        writer = STEPControl_Writer()
        writer.Transfer(compound, STEPControl_AsIs)
        status = writer.Write(step_filename)
        
        if status == IFSelect_RetDone:
            print(f"Successfully exported to {step_filename}")
        else:
            print(f"Failed to export to {step_filename}")
    except Exception as e:
        print(f"Error exporting to STEP: {e}")


def main():
    """
    Main function to assemble and display the bridge model.
    """
    print("=" * 60)
    print("3D Bridge Model - pythonocc-core 7.9.3")
    print("=" * 60)
    
    # Assemble bridge
    print("Assembling bridge...")
    components = assemble_bridge()
    
    # Export if requested
    if save_step:
        print("Exporting to STEP...")
        export_to_step(components)
    
    # Display
    print("Launching 3D viewer...")
    try:
        display, start_display, add_menu, add_function_to_menu = init_display()
        
        # Display all components
        for shape, color, transparency in components:
            display.DisplayShape(shape, color=color, transparency=transparency, update=False)
        
        # Fit view and set isometric view
        display.FitAll()
        display.View_Iso()
        
        print("=" * 60)
        print("3D viewer launched successfully!")
        print("Use mouse to rotate, zoom, and pan the model.")
        print("=" * 60)
        
        start_display()
    except Exception as e:
        print(f"Error launching display: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
