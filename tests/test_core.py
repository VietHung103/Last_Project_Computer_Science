from PIL import Image

from png2svg.core import average_color, hexagon_points, png_to_svg


def test_avg_color_of_image():
    image = Image.new("RGB", (20, 20), (255, 0, 0))
    assert average_color(image, 10, 10, 5) == (255, 0, 0)


def test_hexagon_point():
    assert len(hexagon_points(10, 10, 5).split()) == 6


def test_png_to_svg():
    img = Image.new("RGB", (30, 30), (0, 255, 0))
    svg = png_to_svg(img, 5)
    assert svg.startswith("<svg")
