import pytest
from PIL import Image

from png2svg.core import Hexagon, Triangle, average_color, make_grid, palette_to_svg, png_to_svg

RED, GREEN = (255, 0, 0), (0, 255, 0)


def test_avg_color_of_image():
    image = Image.new("RGB", (20, 20), RED)
    assert average_color(image, 10, 10, 5) == RED


def test_hexagon_has_6_corners():
    assert len(Hexagon(10, 10, 5).corners()) == 6


def test_triangle_has_3_corners():
    assert len(Triangle(10, 10, 5, up=True).corners()) == 3


def test_png_to_svg():
    svg = png_to_svg(Image.new("RGB", (30, 30), GREEN), 5)
    assert svg.startswith("<svg")
    assert 'fill="rgb(0,255,0)"' in svg


def test_png_to_svg_with_triangles():
    svg = png_to_svg(Image.new("RGB", (30, 30), GREEN), 5, "triangle")
    assert 'fill="rgb(0,255,0)"' in svg


def test_unknown_shape_raises():
    with pytest.raises(ValueError):
        make_grid(10, 10, 5, "circle")


def test_palette_to_svg_uses_only_palette_colors():
    svg = palette_to_svg(100, 100, [RED, GREEN], 10)
    assert "rgb(255,0,0)" in svg or "rgb(0,255,0)" in svg
    assert "rgb(0,0,255)" not in svg


def test_palette_gradient_goes_left_to_right():
    svg = palette_to_svg(100, 100, [RED, GREEN], 10, distribution="gradient")
    lines = svg.splitlines()
    assert "rgb(255,0,0)" in lines[1]  # first shape is on the left
