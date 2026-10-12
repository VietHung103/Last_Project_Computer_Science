import argparse
from pathlib import Path

from png2svg.core import convert


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="png2svg",
        description="Convert the PNG Image to SVG Format.",
    )
    parser.add_argument("input", help="Add the path of the image.")
    parser.add_argument(
        "-o",
        "--output",
        default="output.svg",
        help="Path of the output is output.svg(default path)",
    )
    parser.add_argument(
        "-s", "--size", type=float, default=10.0, help="Size of hexagon in pixels (default: 10)."
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if not Path(args.input).is_file():
        parser.error(f"Input file not found: {args.input}")
    if args.size <= 0:
        parser.error("Size must be positive number.")
    convert(args.input, args.output, args.size)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
