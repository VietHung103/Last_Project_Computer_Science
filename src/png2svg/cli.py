import argparse
from pathlib import Path

from png2svg.core import convert, palette_to_svg


def hex_to_rgb(code: str) -> tuple[int, int, int]:
    code = code.strip().lstrip("#")
    return int(code[0:2], 16), int(code[2:4], 16), int(code[4:6], 16)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="png2svg",
        description="Convert the PNG Image to SVG Format.",
    )
    parser.add_argument("input", nargs="?", help="Add the path of the image.")
    parser.add_argument(
        "-o",
        "--output",
        default="output.svg",
        help="Path of the output is output.svg(default path)",
    )
    parser.add_argument(
        "-s", "--size", type=float, default=10.0, help="Size of the shape in pixels (default: 10)."
    )
    parser.add_argument("--shape", choices=["hexagon", "triangle"], default="hexagon")
    parser.add_argument("--palette", help="Colors instead of an image, e.g. '#ff0000,#00ff00'.")
    parser.add_argument("--distribution", choices=["random", "gradient"], default="random")
    parser.add_argument("--width", type=int, default=800, help="Width with --palette.")
    parser.add_argument("--height", type=int, default=600, help="Height with --palette.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.size <= 0:
        parser.error("Size must be positive number.")
    if args.palette:
        palette = [hex_to_rgb(code) for code in args.palette.split(",")]
        svg = palette_to_svg(
            args.width, args.height, palette, args.size, args.shape, args.distribution
        )
        with open(args.output, "w") as f:
            f.write(svg)
    elif args.input:
        if not Path(args.input).is_file():
            parser.error(f"Input file not found: {args.input}")
        convert(args.input, args.output, args.size, args.shape)
    else:
        parser.error("Give an input image or --palette.")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
