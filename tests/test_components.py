"""
Unit tests for bridge component factory functions.

Run with: python tests/test_components.py
"""

import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from components.pier import create_circular_pier, create_trapezoidal_pier_cap
from components.pile import create_pile, create_pile_cap
from components.rebar import (
    create_rebar_bar,
    create_rebar_grid_in_deck,
    create_rebar_cage_in_pier
)
from draw_i_section import create_i_section
from draw_rectangular_prism import create_rectangular_prism

from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_VolumeProperties


def test_circular_pier():
    """Test circular pier creation."""
    print("Testing create_circular_pier...")
    
    diameter = 800
    height = 3000
    
    pier = create_circular_pier(diameter, height)
    
    assert pier is not None, "Pier should not be None"
    assert isinstance(pier, TopoDS_Shape), "Pier should be a TopoDS_Shape"
    
    # Check volume (approximate)
    props = GProp_GProps()
    brepgprop_VolumeProperties(pier, props)
    volume = props.Mass()
    
    # Expected volume = π * r^2 * h
    import math
    expected_volume = math.pi * (diameter / 2) ** 2 * height
    
    assert abs(volume - expected_volume) / expected_volume < 0.01, \
        f"Volume mismatch: {volume} vs {expected_volume}"
    
    print("✓ create_circular_pier passed")


def test_trapezoidal_pier_cap():
    """Test trapezoidal pier cap creation."""
    print("Testing create_trapezoidal_pier_cap...")
    
    length = 7000
    top_width = 3000
    bottom_width = 1200
    depth = 600
    
    pier_cap = create_trapezoidal_pier_cap(length, top_width, bottom_width, depth)
    
    assert pier_cap is not None, "Pier cap should not be None"
    assert isinstance(pier_cap, TopoDS_Shape), "Pier cap should be a TopoDS_Shape"
    
    # Check that shape has volume
    props = GProp_GProps()
    brepgprop_VolumeProperties(pier_cap, props)
    volume = props.Mass()
    
    assert volume > 0, "Pier cap should have positive volume"
    
    print("✓ create_trapezoidal_pier_cap passed")


def test_pile():
    """Test pile creation."""
    print("Testing create_pile...")
    
    diameter = 400
    length = 5000
    
    pile = create_pile(diameter, length)
    
    assert pile is not None, "Pile should not be None"
    assert isinstance(pile, TopoDS_Shape), "Pile should be a TopoDS_Shape"
    
    # Check volume
    props = GProp_GProps()
    brepgprop_VolumeProperties(pile, props)
    volume = props.Mass()
    
    import math
    expected_volume = math.pi * (diameter / 2) ** 2 * length
    
    assert abs(volume - expected_volume) / expected_volume < 0.01, \
        f"Volume mismatch: {volume} vs {expected_volume}"
    
    print("✓ create_pile passed")


def test_pile_cap():
    """Test pile cap creation."""
    print("Testing create_pile_cap...")
    
    length = 2200
    width = 1200
    depth = 600
    
    pile_cap = create_pile_cap(length, width, depth)
    
    assert pile_cap is not None, "Pile cap should not be None"
    assert isinstance(pile_cap, TopoDS_Shape), "Pile cap should be a TopoDS_Shape"
    
    # Check volume
    props = GProp_GProps()
    brepgprop_VolumeProperties(pile_cap, props)
    volume = props.Mass()
    
    expected_volume = length * width * depth
    
    assert abs(volume - expected_volume) / expected_volume < 0.01, \
        f"Volume mismatch: {volume} vs {expected_volume}"
    
    print("✓ create_pile_cap passed")


def test_rebar_bar():
    """Test single rebar bar creation."""
    print("Testing create_rebar_bar...")
    
    diameter = 16
    length = 1000
    
    rebar = create_rebar_bar(diameter, length)
    
    assert rebar is not None, "Rebar should not be None"
    assert isinstance(rebar, TopoDS_Shape), "Rebar should be a TopoDS_Shape"
    
    # Check volume
    props = GProp_GProps()
    brepgprop_VolumeProperties(rebar, props)
    volume = props.Mass()
    
    import math
    expected_volume = math.pi * (diameter / 2) ** 2 * length
    
    assert abs(volume - expected_volume) / expected_volume < 0.01, \
        f"Volume mismatch: {volume} vs {expected_volume}"
    
    print("✓ create_rebar_bar passed")


def test_rebar_grid_in_deck():
    """Test deck rebar grid creation."""
    print("Testing create_rebar_grid_in_deck...")
    
    deck_width = 7000
    span_length = 12000
    cover = 40
    bar_diam = 16
    spacing = 150
    
    rebar_list = create_rebar_grid_in_deck(
        deck_width, span_length, cover, bar_diam, spacing
    )
    
    assert rebar_list is not None, "Rebar list should not be None"
    assert isinstance(rebar_list, list), "Should return a list"
    assert len(rebar_list) > 0, "Should create at least one rebar"
    
    # Check that all items are shapes
    for rebar in rebar_list:
        assert isinstance(rebar, TopoDS_Shape), "Each rebar should be a TopoDS_Shape"
    
    print(f"✓ create_rebar_grid_in_deck passed (created {len(rebar_list)} bars)")


def test_rebar_cage_in_pier():
    """Test pier rebar cage creation."""
    print("Testing create_rebar_cage_in_pier...")
    
    pier_diameter = 800
    pier_height = 3000
    main_diam = 16
    n_main_bars = 8
    tie_diam = 8
    tie_spacing = 200
    cover = 40
    
    rebar_list = create_rebar_cage_in_pier(
        pier_diameter, pier_height, main_diam, n_main_bars,
        tie_diam, tie_spacing, cover
    )
    
    assert rebar_list is not None, "Rebar list should not be None"
    assert isinstance(rebar_list, list), "Should return a list"
    assert len(rebar_list) > 0, "Should create at least one rebar"
    
    # Check that all items are shapes
    for rebar in rebar_list:
        assert isinstance(rebar, TopoDS_Shape), "Each rebar should be a TopoDS_Shape"
    
    print(f"✓ create_rebar_cage_in_pier passed (created {len(rebar_list)} bars)")


def test_i_section():
    """Test I-section girder creation (from provided module)."""
    print("Testing create_i_section...")
    
    d = 900
    bf = 300
    tf = 16
    tw = 10
    length = 12000
    
    girder = create_i_section(d, bf, tf, tw, length)
    
    assert girder is not None, "Girder should not be None"
    assert isinstance(girder, TopoDS_Shape), "Girder should be a TopoDS_Shape"
    
    # Check that shape has volume
    props = GProp_GProps()
    brepgprop_VolumeProperties(girder, props)
    volume = props.Mass()
    
    assert volume > 0, "Girder should have positive volume"
    
    print("✓ create_i_section passed")


def test_rectangular_prism():
    """Test rectangular prism creation (from provided module)."""
    print("Testing create_rectangular_prism...")
    
    width = 7000
    height = 200
    length = 12000
    
    prism = create_rectangular_prism(width, height, length)
    
    assert prism is not None, "Prism should not be None"
    assert isinstance(prism, TopoDS_Shape), "Prism should be a TopoDS_Shape"
    
    # Check volume
    props = GProp_GProps()
    brepgprop_VolumeProperties(prism, props)
    volume = props.Mass()
    
    expected_volume = width * height * length
    
    assert abs(volume - expected_volume) / expected_volume < 0.01, \
        f"Volume mismatch: {volume} vs {expected_volume}"
    
    print("✓ create_rectangular_prism passed")


def run_all_tests():
    """Run all component tests."""
    print("=" * 60)
    print("Running Bridge Component Tests")
    print("=" * 60)
    
    tests = [
        test_circular_pier,
        test_trapezoidal_pier_cap,
        test_pile,
        test_pile_cap,
        test_rebar_bar,
        test_rebar_grid_in_deck,
        test_rebar_cage_in_pier,
        test_i_section,
        test_rectangular_prism
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
