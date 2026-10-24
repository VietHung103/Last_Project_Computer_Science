import math
import random

from PIL import Image

Color = tuple[int, int, int]


# OOP
class Shape:
    def __init__(self, cx: float, cy: float, size: float) -> None:
        self.cx = cx
        self.cy = cy
        self.size = size

    def corners(self) -> list[tuple[float, float]]:
        raise NotImplementedError  # not implement because each shape give its own corners

    def to_svg(self, color: Color) -> str:
        points = " ".join(f"{x:.1f},{y:.1f}" for x, y in self.corners())
        r, g, b = color
        return f'<polygon points="{points}" fill="rgb({r},{g},{b})" />'


class Hexagon(Shape):
    def corners(self) -> list[tuple[float, float]]:
        points = []
        for i in range(6):
            angle = math.radians(60 * i - 30)
            points.append(
                (self.cx + self.size * math.cos(angle), self.cy + self.size * math.sin(angle))
            )
        return points


class Triangle(Shape):
    def __init__(self, cx: float, cy: float, size: float, up: bool) -> None:
        super().__init__(cx, cy, size)
        self.up = up

    def corners(self) -> list[tuple[float, float]]:
        half = self.size / 2
        h = self.size * math.sqrt(3) / 2 / 2  # half of the triangle height
        if self.up:  # up = true mean /\
            return [
                (self.cx, self.cy - h),
                (self.cx + half, self.cy + h),
                (self.cx - half, self.cy + h),
            ]
        return [  # up = false mean \/
            (self.cx - half, self.cy - h),
            (self.cx + half, self.cy - h),
            (self.cx, self.cy + h),
        ]


def make_grid(width: int, height: int, size: float, shape: str = "hexagon") -> list[Shape]:
    if size <= 0:
        raise ValueError("Size must be positive.")
    shapes: list[Shape] = []
    if shape == "hexagon":
        step_x = math.sqrt(3) * size
        step_y = 1.5 * size
        for row in range(int(height / step_y) + 2):
            for col in range(int(width / step_x) + 2):
                cx = col * step_x
                if row % 2 == 1:
                    cx += step_x / 2
                shapes.append(Hexagon(cx, row * step_y, size))
    elif shape == "triangle":
        step_x = size / 2
        step_y = size * math.sqrt(3) / 2
        for row in range(int(height / step_y) + 1):
            for col in range(int(width / step_x) + 2):
                up = (row + col) % 2 == 0
                shapes.append(Triangle(col * step_x, row * step_y + step_y / 2, size, up))
    else:
        raise ValueError(f"Unknown shape: {shape}")
    return shapes


def average_color(img: Image.Image, cx: float, cy: float, size: float) -> Color:
    w, h = img.size
    red = green = blue = count = 0
    for x in range(int(cx - size / 2), int(cx + size / 2) + 1):
        for y in range(int(cy - size / 2), int(cy + size / 2) + 1):
            x_in = min(max(x, 0), w - 1)  # stay inside the image
            y_in = min(max(y, 0), h - 1)
            pixel = img.getpixel((x_in, y_in))
            assert isinstance(pixel, tuple)
            red += pixel[0]
            green += pixel[1]
            blue += pixel[2]
            count += 1
    return red // count, green // count, blue // count


def pallette_color(palette: list[Color], x: float, width: int, distribution: str) -> Color:
    if distribution == "random":
        return random.choice(palette)
    index = int(x / width * len(palette))
    return palette[min(max(index, 0), len(palette) - 1)]


def build_svg(width: int, height: int, polygons: list[str]) -> str:
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
    svg += f'viewBox="0 0 {width} {height}">\n'
    svg += "\n".join(polygons)
    svg += "\n</svg>\n"
    return svg


def png_to_svg(image: Image.Image, size: float = 10, shape: str = "hexagon") -> str:
    image = image.convert("RGB")
    w, h = image.size
    polygons = []
    for s in make_grid(w, h, size, shape):
        polygons.append(s.to_svg(average_color(image, s.cx, s.cy, s.size)))
    return build_svg(w, h, polygons)


def palette_to_svg(
    width: int,
    height: int,
    palette: list[Color],
    size: float = 10,
    shape: str = "hexagon",
    distribution: str = "random",
) -> str:
    polygons = []
    for s in make_grid(width, height, size, shape):
        polygons.append(s.to_svg(pallette_color(palette, s.cx, width, distribution)))
    return build_svg(width, height, polygons)


def convert(
    input_filename: str, output_filename: str, size: float = 10, shape: str = "hexagon"
) -> None:
    image = Image.open(input_filename)
    svg_content = png_to_svg(image, size, shape)
    with open(output_filename, "w") as f:
        f.write(svg_content)
