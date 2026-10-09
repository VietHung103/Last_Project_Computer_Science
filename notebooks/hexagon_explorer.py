import marimo

__generated_with = "0.25.1"
app = marimo.App()


@app.cell
def _():
    from PIL import Image

    image = Image.open("images/screenshot.png")
    image.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    """)
    return


if __name__ == "__main__":
    app.run()
