from PIL import Image, ImageDraw, ImageFilter

def draw_path(paths):
    image = Image.open("map_smoothed.jpg")
    image = image.convert("RGB")
    image_draw = ImageDraw.Draw(image)
    pixel_path = [(col, row) for row, col in paths]
    image_draw.line(pixel_path, fill='red', width = 1)
    image.show()
    image.save("path.jpg")

def prepare_image(path, blur):
    image = Image.open(path)
    width, height = image.size
    image = image.crop((0, 0.15 * height, width, height))
    image = image.resize((100, 100))
    r,g,b = image.split()
    r.save("map.jpg")
    r_smoothed = r.filter(ImageFilter.GaussianBlur(radius = blur))
    r_smoothed.show()
    r_smoothed.save("map_smoothed.jpg")
    return r_smoothed
 
