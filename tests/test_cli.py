import pytest
from PIL import Image

from png2svg.cli import build_parser, main


def test_parser_default_values():
    args = build_parser().parse_args(["in.png"])
    assert args.input == "in.png"
    assert args.output == "output.svg"
    assert args.size == 10.0


def test_parser_custom_values():
    args = build_parser().parse_args(["in.png", "-o", "out.svg", "-s", "15"])
    assert args.output == "out.svg"
    assert args.size == 15.0


def test_main_writes_svg_file(monkeypatch, tmp_path, capsys):
    input_file = tmp_path / "in.png"
    output_file = tmp_path / "out.svg"
    Image.new("RGB", (30, 30), (255, 0, 0)).save(input_file)
    monkeypatch.setattr("sys.argv", ["png2svg", str(input_file), "-o", str(output_file)])

    main()

    assert 'fill="rgb(255,0,0)"' in output_file.read_text()
    assert capsys.readouterr().out.strip() == f"Wrote {output_file}"


def test_main_requires_an_input(monkeypatch):
    monkeypatch.setattr("sys.argv", ["png2svg"])
    with pytest.raises(SystemExit):
        main()


def test_main_rejects_missing_file(monkeypatch, tmp_path):
    monkeypatch.setattr("sys.argv", ["png2svg", str(tmp_path / "missing.png")])
    with pytest.raises(SystemExit):
        main()


def test_main_rejects_bad_size(monkeypatch, tmp_path):
    input_file = tmp_path / "in.png"
    Image.new("RGB", (10, 10)).save(input_file)
    monkeypatch.setattr("sys.argv", ["png2svg", str(input_file), "-s", "0"])
    with pytest.raises(SystemExit):
        main()


def test_main_with_triangles(monkeypatch, tmp_path):
    input_file = tmp_path / "in.png"
    output_file = tmp_path / "out.svg"
    Image.new("RGB", (30, 30), (255, 0, 0)).save(input_file)
    monkeypatch.setattr(
        "sys.argv", ["png2svg", str(input_file), "-o", str(output_file), "--shape", "triangle"]
    )
    main()
    assert output_file.exists()


def test_main_with_palette(monkeypatch, tmp_path):
    output_file = tmp_path / "out.svg"
    monkeypatch.setattr(
        "sys.argv", ["png2svg", "--palette", "#ff0000,#00ff00", "-o", str(output_file)]
    )
    main()
    assert 'width="800"' in output_file.read_text()
