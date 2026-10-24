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

    Pick a picture, then choose the shape (hexagon or triangle) and its size. The picture
    is rebuilt in SVG format: each shape is the average color of the pixels under it. This
    notebook uses the published "png2svg-viethung103" package.
    """)
    return


@app.cell
def _():
    upload = mo.ui.file(filetypes=[".png", ".jpg", ".jpeg"], kind="area", label="Pick a picture")
    shape = mo.ui.dropdown(["hexagon", "triangle"], value="hexagon", label="Shape")
    size = mo.ui.slider(4, 40, value=12, step=1, label="Shape size", show_value=True)
    mo.vstack([upload, shape, size])
    return shape, size, upload


@app.cell
def _(shape, size, upload):
    mo.stop(not upload.value, mo.md("Pick a picture above to start."))

    image = Image.open(io.BytesIO(upload.contents()))
    svg = png_to_svg(image, size.value, shape.value)
    return image, svg


@app.cell
def _(image, svg):
    mo.md(f"""
    **Picture size:** {image.width} × {image.height} px
    **Number of shapes:** {svg.count("<polygon")}
    """)
    return


@app.cell
def _(svg, upload):
    mo.vstack(
        [
            mo.md("### Original"),
            mo.image(upload.contents()),
            mo.md("### Mosaic (SVG)"),
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


if __name__ == "__main__":
    app.run()
