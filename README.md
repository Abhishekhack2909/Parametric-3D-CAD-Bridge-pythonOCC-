<div align="center">

# 🌉 Parametric 3D Bridge Model

### Built with pythonocc-core 7.9.3

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![pythonocc](https://img.shields.io/badge/pythonocc--core-7.9.3-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-LGPL%203.0-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-success?style=for-the-badge)

**A fully parametric 3D CAD model of a steel girder bridge with concrete deck, pier, piles, and reinforcement bars**

[🔗 View Repository](https://github.com/Abhishekbcs2009/Parametric-3D-CAD-Bridge-pythonOCC) • [📖 Documentation](#installation) • [🚀 Quick Start](#run)

</div>

---

## 📋 Submission Information

> **FOSSEE Osdag Summer Fellowship 2026**  
> Screening Task: Parametric 3D CAD Model of a Steel Girder Bridge

| Field | Details |
|-------|---------|
| **Submitted by** | Abhishek |
| **Date** | April 2026 |
| **Task** | Osdag Task 1 |
| **Repository** | [Parametric-3D-CAD-Bridge-pythonOCC](https://github.com/Abhishekbcs2009/Parametric-3D-CAD-Bridge-pythonOCC) |

> ℹ️ **Note:** `osdag-admin` has been added as a collaborator as required by submission guidelines.

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🏗️ Structural Components
- ✅ Steel I-section girders (3 or more)
- ✅ Concrete deck slab
- ✅ Circular concrete pier
- ✅ Trapezoidal pier cap (hammerhead)
- ✅ Rectangular pile cap
- ✅ Circular foundation piles

</td>
<td width="50%">

### 🔧 Technical Features
- ✅ Fully parametric design
- ✅ Visible steel reinforcement
- ✅ Semi-transparent concrete
- ✅ Interactive 3D visualization
- ✅ STEP file export
- ✅ Unit tested components

</td>
</tr>
</table>

## 📦 Installation

### Prerequisites

You need conda (Anaconda or Miniconda) installed on your system.

> 💡 **Don't have conda?** Download Miniconda: https://docs.conda.io/en/latest/miniconda.html

### Setup Environment

```bash
# Create a new conda environment with Python 3.12
conda create --name=pyoccenv python=3.12 -y

# Activate the environment
conda activate pyoccenv

# Install pythonocc-core version 7.9.3
conda install -c conda-forge pythonocc-core=7.9.3 -y
```

> ⚡ **Installation time:** ~5-10 minutes depending on your internet speed

---

## 📁 Project Structure

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

## 🚀 Run

Make sure you're in the project directory and the conda environment is activated:

```bash
# Activate environment
conda activate pyoccenv

# Run the bridge model
python bridge_model.py
```

The script will:
1. 🔨 Build all bridge components (girders, deck, pier, piles, rebar)
2. 🎨 Assemble them with appropriate colors and transparency
3. 🖥️ Launch an interactive 3D viewer window

### 🎮 3D Viewer Controls

| Action | Control |
|--------|---------|
| **Rotate** | Left mouse button + drag |
| **Pan** | Middle mouse button + drag (or Shift + left mouse button) |
| **Zoom** | Mouse wheel (or right mouse button + drag) |
| **Fit view** | Press `F` key |
| **Close** | Close the window or press `Q` |

---

## 📂 Files

### Main Script
- **`bridge_model.py`** - Main assembly script with all parameters and visualization

### Component Modules
- **`components/pier.py`** - Functions to create circular pier and trapezoidal pier cap
- **`components/pile.py`** - Functions to create piles and pile cap
- **`components/rebar.py`** - Functions to create reinforcement bar grids and cages

### Provided Modules (DO NOT MODIFY)
- **`draw_i_section.py`** - Creates steel I-section beams (provided by Osdag)
- **`draw_rectangular_prism.py`** - Creates rectangular box solids (provided by Osdag)

### Tests
- **`tests/test_components.py`** - Unit tests for all component factory functions

---

## ⚙️ Parameters

All parameters are defined at the top of `bridge_model.py`. You can modify them to adjust the bridge dimensions.

### 📏 Key Parameters (all in millimetres)

<details>
<summary><b>🏗️ Span & Layout</b></summary>

```python
span_length_L = 12000           # Total bridge span length
n_girders = 3                   # Number of I-section girders
girder_centroid_spacing = 3000  # Spacing between girders
deck_overhang = 500             # Deck overhang beyond outer girders
```
</details>

<details>
<summary><b>🔩 Girder (I-Section)</b></summary>

```python
girder_section_d = 900          # Depth of I-section
girder_section_bf = 300         # Flange width
girder_section_tf = 16          # Flange thickness
girder_section_tw = 10          # Web thickness
```
</details>

<details>
<summary><b>🏢 Deck Slab</b></summary>

```python
deck_width = 7000               # Total width of deck
deck_thickness = 200            # Thickness of deck slab
deck_cover = 40                 # Concrete cover for rebar
```
</details>

<details>
<summary><b>🏛️ Pier & Pier Cap</b></summary>

```python
pier_diameter = 800             # Diameter of circular pier
pier_height = 3000              # Height of pier column
pier_cap_length = 7000          # Length of pier cap
pier_cap_top_width = 3000       # Width at top (hammerhead)
pier_cap_bottom_width = 1200    # Width at bottom
pier_cap_depth = 600            # Height of pier cap
```
</details>

<details>
<summary><b>🔨 Piles & Pile Cap</b></summary>

```python
n_piles_per_cap = 4             # Number of piles (2x2 grid)
pile_diameter = 400             # Diameter of each pile
pile_length = 5000              # Length of pile going down
pile_spacing = 600              # Spacing between pile centers
pile_cap_length = 2200          # Length of pile cap
pile_cap_width = 1200           # Width of pile cap
pile_cap_depth = 600            # Depth of pile cap
```
</details>

<details>
<summary><b>🔴 Reinforcement Bars</b></summary>

```python
rebar_main_diameter = 16        # Diameter of longitudinal bars
rebar_transverse_diameter = 8   # Diameter of stirrups/ties
rebar_spacing_longitudinal = 150  # Spacing of longitudinal bars
rebar_spacing_transverse = 200    # Spacing of stirrups
rebar_cover = 40                  # Concrete cover
rebar_visible = True              # Show or hide rebar
```
</details>

<details>
<summary><b>🎨 Visualization</b></summary>

```python
concrete_opacity = 0.35         # Concrete transparency (0.35 = 35% opaque)
steel_opacity = 1.0             # Steel opacity (fully opaque)
rebar_opacity = 1.0             # Rebar opacity (fully opaque)
```
</details>

<details>
<summary><b>💾 Export</b></summary>

```python
save_step = False               # Set to True to export STEP file
step_filename = "bridge_model.step"  # Output filename
```
</details>

---

## 📐 Coordinate System

| Axis | Direction | Description |
|------|-----------|-------------|
| **X-axis** | → | Along the span (longitudinal, bridge length direction) |
| **Y-axis** | ↔ | Across the deck (transverse, bridge width direction) |
| **Z-axis** | ↑ | Vertical (up/down) |
| **Origin** | 📍 | Center of span at deck bottom level |

---

## 🎨 Colors

| Component | Color | RGB | Transparency |
|-----------|-------|-----|--------------|
| 🔩 **Steel girders** | Grey | `(0.5, 0.5, 0.6)` | Opaque |
| 🏢 **Deck concrete** | Light grey | `(0.8, 0.8, 0.75)` | 65% transparent |
| 🏛️ **Pier concrete** | Light blue | `(0.6, 0.75, 0.9)` | 65% transparent |
| 🔨 **Pile cap** | Grey | `(0.7, 0.7, 0.65)` | 65% transparent |
| 🔨 **Piles** | Grey | `(0.7, 0.7, 0.65)` | 65% transparent |
| 🔴 **Rebar** | Red-brown | `(0.8, 0.2, 0.1)` | Opaque |

> 💡 All concrete parts are semi-transparent (65% transparent) to show internal reinforcement.

---

## 🧪 Running Tests

To verify that all component factory functions work correctly:

```bash
python tests/test_components.py
```

**Expected output:**
```
============================================================
Running Bridge Component Tests
============================================================
Testing create_circular_pier...
✓ create_circular_pier passed
Testing create_trapezoidal_pier_cap...
✓ create_trapezoidal_pier_cap passed
...
============================================================
Test Results: 9 passed, 0 failed
============================================================
```

---

## 💾 Exporting to STEP Format

To export the bridge model to a STEP file:

1. Open `bridge_model.py`
2. Set `save_step = True` near the top of the file
3. Optionally change `step_filename` to your desired output name
4. Run the script: `python bridge_model.py`

The STEP file will be saved in the current directory and can be imported into CAD software like FreeCAD, SolidWorks, or Rhino.

---

## 🔧 Troubleshooting

### ❌ Import Errors

**Problem:** `ModuleNotFoundError: No module named 'OCC'`

**Solution:**
```bash
# Make sure environment is activated
conda activate pyoccenv

# Verify installation
conda list pythonocc-core

# If not installed, reinstall
conda install -c conda-forge pythonocc-core=7.9.3 -y
```

### ❌ Display Window Not Opening

**Problem:** The 3D viewer window doesn't open

**Solution:**
- Check that you're not running in a headless environment (no display)
- On Linux, ensure X11 is properly configured
- On Windows, ensure graphics drivers are up to date

### ⚠️ Performance Issues

**Problem:** The model is slow to render

**Solution:**
- Reduce the number of rebar by increasing `rebar_spacing_longitudinal` and `rebar_spacing_transverse`
- Set `rebar_visible = False` to hide all reinforcement
- Reduce the number of girders with `n_girders`

---

## 🎯 Customization

To create your own bridge design:

1. 📝 Modify parameters at the top of `bridge_model.py`
2. ▶️ Run the script to see the updated model
3. 🔄 Iterate until you achieve the desired design

> 📏 All dimensions are in millimetres for precision in structural engineering applications.

---

## 📚 Library Information

| Property | Value |
|----------|-------|
| **Library** | pythonocc-core |
| **Version** | 7.9.3 |
| **GitHub** | [tpaviot/pythonocc-core](https://github.com/tpaviot/pythonocc-core) |
| **Documentation** | [pythonocc.org](http://www.pythonocc.org/) |

---

## 📄 License

This project uses pythonocc-core which is licensed under LGPL 3.0.

---

<div align="center">

## 👨‍💻 Author

**Abhishek**  
2nd Year Student  
FOSSEE Summer Fellowship 2026 - Osdag Task 1  
Parametric 3D Bridge Modeling using pythonocc-core 7.9.3

---

Made with ❤️ for FOSSEE Osdag

[⬆ Back to Top](#-parametric-3d-bridge-model)

</div>
