from PIL import Image
import math
def hexagon_points(cx:float, cy:float, size:float) -> str:
    points = []
    for i in range(6):
        angle = math.radians(60*i-30)
        x = cx+ size*math.cos(angle)
        y = cy+ size*math.sin(angle)
        points.append(f"{x:.1f},{y:.1f}")
    return " ".join(points)

def average_color(img:Image.Image,cx:float,cy:float,size:float) -> tuple[int,int,int]:
    w,h = img.size
    red = green = blue = count = 0
    for x in range(int(cx-size/2), int(cx+size/2)+1):
        for y in range(int(cy-size/2), int(cy+size/2)+1):
            x = min(max(x,0),w-1) #stay inside the image
            y = min(max(y,0),h-1)
            pixel = img.getpixel((x,y))
            red+= pixel[0]
            green+= pixel[1]
            blue+= pixel[2]
            count+=1
    return red // count, green//count, blue//count

def png_to_svg(image: Image.Image, size: float = 10) -> str:
    if size <= 0:
        raise ValueError("Hexagon size must be positive.")
    image = image.convert("RGB")
    w, h = image.size
    #pointy top
    step_x = math.sqrt(3) * size 
    step_y = 1.5 * size
    hexagons = []
    for row in range(int(h/step_y)+2):
        for col in range(int(w/step_x)+2):
            cx = col*step_x
            if row %2 ==1:
                cx+=step_x/2
            cy = row*step_y
            r,g,b = average_color(image,cx,cy,size)
            points = hexagon_points(cx,cy,size)
            hexagons.append(f'<polygon points="{points}" fill="rgb({r},{g},{b})" />')
    svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">\n'
    svg_content += "\n".join(hexagons)
    svg_content += "\n</svg>\n"
    return svg_content

def convert(input_filename: str, output_filename: str, size: float = 10) -> None:
    image = Image.open(input_filename)
    svg_content = png_to_svg(image, size)
    with open(output_filename, "w") as f:
        f.write(svg_content)