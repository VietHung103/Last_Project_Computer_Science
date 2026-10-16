# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "png2svg-viethung103",
#     "marimo>=0.10",
#     "pillow",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")

with app.setup:
    import io
    
    import marimo as mo
    from PIL import Image

    from png2svg import png_to_svg


@app.cell
def _():
    mo.md(r"""
    # PNG to SVG Format

    Pick the PNG image and chose the hexagon size. The picture is rebuilt in to
    SVG format: each hexagon is the average of pixels under it. This nootbook uses
    the published "png2svg-viethung103" package - it dose not reimplement the conversion.
    """)
    return


@app.cell
def _():
    upload = mo.ui.file(filetypes=[".png"], kind="area", label="Pick a SVG Picture")
    size = mo.ui.slider(4,40, value=12, step=1, label="Choose the hexagon size", show_value=True)
    mo.vstack([upload,size])
    return size, upload


@app.cell
def _(size, upload):
    mo.stop(not upload.value, mo.md("_Pick a PNG file above to start._"))

    image = Image.open(io.BytesIO(upload.contents()))
    svg = png_to_svg(image, size.value)
    return image, svg


@app.cell
def _(image, svg):
    mo.md(f"""
    **Picture size:** {image.width} × {image.height} px
    **Number of hexagons:** {svg.count("<polygon")}
    """)
    return


@app.cell
def _(svg, upload):
    mo.vstack(
        [
            mo.md("### Original"),
            mo.image(upload.contents()),
            mo.md("### Hexagon mosaic (SVG)"),
            mo.Html(f'<div style="overflow:auto">{svg}</div>'),
        ]
    )
    return


@app.cell
def _(svg, upload):
    mo.download(
        data=svg.encode(),
        filename=upload.name().rsplit(".", 1)[0] + ".svg",
        mimetype="image/svg+xml",
        label="Download the SVG",
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
