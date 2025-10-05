from PIL import Image, ImageDraw, ImageFilter

def draw_path(paths):
    image = Image.open("map.jpg")
    image = image.convert("RGB")
    new_image = ImageDraw.Draw(image)
    pixel_path = [(int(col), int(row)) for row, col in paths]
    new_image.line(pixel_path, fill='red', width = 1)
    image.show()

def prepare_image(path):
    image = Image.open(path)
    width, height = image.size
    image = image.crop((0.15 * width, 0.15 * height, 0.85 * width, 0.815 * height))
    image = image.resize((100, 100))
    r,g,b = image.split()
    r_smoothed = r.filter(ImageFilter.GaussianBlur(radius = 2))
    r_smoothed.show()
    r_smoothed.save("map.jpg")
    return r_smoothed
 
