from PIL import Image
import numpy
import argparse

def main(path):
    grid = resize_image(path)
    height_map = prepare_weights(grid)
    print(height_map)

def resize_image(path):
    image = Image.open(path)
    width, height = image.size
    image = image.crop((0.15 * width, 0.15 * height, 0.85 * width, 0.815 * height))
    image = image.resize((100, 100))
    r,g,b = image.split()
    grid = numpy.array(r)
    r.show()
    r.save("map.jpg")
    return grid

def prepare_weights(grid):
    normalized = grid / 255.0
    height_map = normalized * 3.0
    return height_map
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate the shortest path to an object for a rover")
    parser.add_argument("--path", type=str, required=True, help="Path to the map")

    args = parser.parse_args()
        
    main(args.path)
