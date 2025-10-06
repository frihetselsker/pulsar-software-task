from PIL import Image, ImageDraw, ImageFilter, ImageFile

def draw_path(paths: [(int, int)]) -> None:
    """
    Draw the path over the processed image.

    Args:
        paths ( [(int, int)] ): A list of the coordinates found. 

    Returns:
        None
    """    
    image = Image.open("map_smoothed.jpg")
    image = image.convert("RGB")
    image_draw = ImageDraw.Draw(image)
    pixel_path = [(col, row) for row, col in paths]
    image_draw.line(pixel_path, fill='red', width = 1)
    image.show()
    image.save("path.jpg")

def prepare_image(path: str, blur: int) -> ImageFile.ImageFile:
    """
    Process the image for the further search of the path.
    Crop, resize, and blur if necessary.
    The processed file is saved under the name 'map_smoothed.jpg'

    Args:
        path (str): Path to the image that will be processed.
        blur (int): The radius of Gaussian blur. If no effect is wanted, then blur is 0.

    Returns:
       ImageFile.ImageFile: cropped PIL image object with red channel extracted and smoothed.
    """    
    image = Image.open(path)
    width, height = image.size
    image = image.crop((0, 0.15 * height, width, height))
    image = image.resize((100, 100))
    r,g,b = image.split()
    r.save("map.jpg")
    r_smoothed = r.filter(ImageFilter.GaussianBlur(radius = blur))
    r_smoothed.save("map_smoothed.jpg")
    return r_smoothed
 
