# 3D Bridge Model - pythonocc-core 7.9.3

A complete parametric 3D model of a short-span steel girder bridge with concrete deck, pier, piles, and reinforcement bars.

## Features

- Steel I-section girders (3 or more, running along the span)
- Concrete deck slab with embedded reinforcement
- Circular concrete pier with rebar cage
- Trapezoidal pier cap (hammerhead shape)
- Rectangular pile cap with circular piles
- Visible steel reinforcement bars through semi-transparent concrete
- Fully parametric design - adjust all dimensions from parameters
- Interactive 3D visualization
- Optional STEP file export

## Installation

### Prerequisites

You need conda (Anaconda or Miniconda) installed on your system.

### Setup Environment

```bash
# Create a new conda environment with Python 3.12
conda create --name=pyoccenv python=3.12

# Activate the environment
conda activate pyoccenv

# Install pythonocc-core version 7.9.3
conda install -c conda-forge pythonocc-core=7.9.3
```

## Project Structure

```
.
├── bridge_model.py              # Main script - run this
├── components/
│   ├── __init__.py              # Package initializer
│   ├── pier.py                  # Pier and pier cap geometry
│   ├── pile.py                  # Pile and pile cap geometry
│   └── rebar.py                 # Reinforcement bar geometry
├── tests/
│   ├── __init__.py              # Package initializer
│   └── test_components.py       # Unit tests for components
├── draw_i_section.py            # Provided by Osdag (I-beam factory)
├── draw_rectangular_prism.py    # Provided by Osdag (box factory)
└── README.md                    # This file
```

## Run

Make sure you're in the project directory and the conda environment is activated:

```bash
conda activate pyoccenv
python bridge_model.py
```

The script will:
1. Build all bridge components (girders, deck, pier, piles, rebar)
2. Assemble them with appropriate colors and transparency
3. Launch an interactive 3D viewer window

### 3D Viewer Controls

- **Rotate**: Left mouse button + drag
- **Pan**: Middle mouse button + drag (or Shift + left mouse button)
- **Zoom**: Mouse wheel (or right mouse button + drag)
- **Fit view**: Press 'F' key
- **Close**: Close the window or press 'Q'

## Files

### Main Script
- `bridge_model.py`: Main assembly script with all parameters and visualization

### Component Modules
- `components/pier.py`: Functions to create circular pier and trapezoidal pier cap
- `components/pile.py`: Functions to create piles and pile cap
- `components/rebar.py`: Functions to create reinforcement bar grids and cages

### Provided Modules (DO NOT MODIFY)
- `draw_i_section.py`: Creates steel I-section beams (provided by Osdag)
- `draw_rectangular_prism.py`: Creates rectangular box solids (provided by Osdag)

### Tests
- `tests/test_components.py`: Unit tests for all component factory functions

## Parameters

All parameters are defined at the top of `bridge_model.py`. You can modify them to adjust the bridge dimensions.

### Key Parameters (all in millimetres)

#### Span & Layout
- `span_length_L = 12000` - Total bridge span length
- `n_girders = 3` - Number of I-section girders
- `girder_centroid_spacing = 3000` - Spacing between girders
- `deck_overhang = 500` - Deck overhang beyond outer girders

#### Girder (I-Section)
- `girder_section_d = 900` - Depth of I-section
- `girder_section_bf = 300` - Flange width
- `girder_section_tf = 16` - Flange thickness
- `girder_section_tw = 10` - Web thickness

#### Deck Slab
- `deck_width = 7000` - Total width of deck
- `deck_thickness = 200` - Thickness of deck slab
- `deck_cover = 40` - Concrete cover for rebar

#### Pier
- `pier_diameter = 800` - Diameter of circular pier
- `pier_height = 3000` - Height of pier column

#### Pier Cap
- `pier_cap_length = 7000` - Length of pier cap
- `pier_cap_top_width = 3000` - Width at top (hammerhead)
- `pier_cap_bottom_width = 1200` - Width at bottom
- `pier_cap_depth = 600` - Height of pier cap

#### Pile Cap
- `pile_cap_length = 2200` - Length of pile cap
- `pile_cap_width = 1200` - Width of pile cap
- `pile_cap_depth = 600` - Depth of pile cap

#### Piles
- `n_piles_per_cap = 4` - Number of piles (2x2 grid)
- `pile_diameter = 400` - Diameter of each pile
- `pile_length = 5000` - Length of pile going down
- `pile_spacing = 600` - Spacing between pile centers

#### Reinforcement Bars
- `rebar_main_diameter = 16` - Diameter of longitudinal bars
- `rebar_transverse_diameter = 8` - Diameter of stirrups/ties
- `rebar_spacing_longitudinal = 150` - Spacing of longitudinal bars
- `rebar_spacing_transverse = 200` - Spacing of stirrups
- `rebar_cover = 40` - Concrete cover
- `rebar_visible = True` - Show or hide rebar

#### Visualization
- `concrete_opacity = 0.35` - Concrete transparency (0.35 = 35% opaque)
- `steel_opacity = 1.0` - Steel opacity (fully opaque)
- `rebar_opacity = 1.0` - Rebar opacity (fully opaque)

#### Export
- `save_step = False` - Set to True to export STEP file
- `step_filename = "bridge_model.step"` - Output filename

## Coordinate System

- **X-axis**: Along the span (longitudinal, bridge length direction)
- **Y-axis**: Across the deck (transverse, bridge width direction)
- **Z-axis**: Vertical (up/down)
- **Origin**: Center of span at deck bottom level

## Colors

- **Steel girders**: Grey (RGB: 0.5, 0.5, 0.6)
- **Deck concrete**: Light grey (RGB: 0.8, 0.8, 0.75)
- **Pier concrete**: Light blue (RGB: 0.6, 0.75, 0.9)
- **Pile cap**: Grey (RGB: 0.7, 0.7, 0.65)
- **Piles**: Grey (RGB: 0.7, 0.7, 0.65)
- **Rebar**: Red-brown (RGB: 0.8, 0.2, 0.1)

All concrete parts are semi-transparent (65% transparent) to show internal reinforcement.

## Running Tests

To verify that all component factory functions work correctly:

```bash
python tests/test_components.py
```

This will run unit tests for all geometry creation functions and report results.

## Exporting to STEP Format

To export the bridge model to a STEP file:

1. Open `bridge_model.py`
2. Set `save_step = True` near the top of the file
3. Optionally change `step_filename` to your desired output name
4. Run the script: `python bridge_model.py`

The STEP file will be saved in the current directory and can be imported into CAD software like FreeCAD, SolidWorks, or Rhino.

## Troubleshooting

### Import Errors

If you get import errors like `ModuleNotFoundError: No module named 'OCC'`:
- Make sure you activated the conda environment: `conda activate pyoccenv`
- Verify pythonocc-core is installed: `conda list pythonocc-core`

### Display Window Not Opening

If the 3D viewer window doesn't open:
- Check that you're not running in a headless environment (no display)
- On Linux, ensure X11 is properly configured
- On Windows, ensure graphics drivers are up to date

### Performance Issues

If the model is slow to render:
- Reduce the number of rebar by increasing `rebar_spacing_longitudinal` and `rebar_spacing_transverse`
- Set `rebar_visible = False` to hide all reinforcement
- Reduce the number of girders with `n_girders`

## Customization

To create your own bridge design:

1. Modify parameters at the top of `bridge_model.py`
2. Run the script to see the updated model
3. Iterate until you achieve the desired design

All dimensions are in millimetres for precision in structural engineering applications.

## Library Information

- **Library**: pythonocc-core
- **Version**: 7.9.3
- **GitHub**: https://github.com/tpaviot/pythonocc-core
- **Documentation**: http://www.pythonocc.org/

## License

This project uses pythonocc-core which is licensed under LGPL 3.0.

## Author

Created as a parametric bridge modeling example using pythonocc-core 7.9.3.
