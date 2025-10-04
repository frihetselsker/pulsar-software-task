from PIL import Image
import numpy
import argparse
import math
import heapq

class Cell:
    def __init__(self):
        # To backtrack the path from the source node to the destination node
        self.parent_x = 0
        self.parent_y = 0
        # g + h
        self.f = float('inf')
        # The distance start_node -> current_node
        self.g = float('inf')
        # The Euclidean distance from the node to the destination node
        # i.e. heuristic cost
        self.h = 0

def main(path):
    grid = resize_image(path).
    height_map = prepare_weights(grid)
    print(f"Size: {len(grid)}x{len(grid[0])}")
    print(height_map)

def is_valid(row, col):
    limit_row = 100
    limit_col = 100    
    return (row >= 0) and (row < limit_row) and (col >= 0) and (col < limit_col)

def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

def can_be_climbed(grid, row_start, col_start, row_end, col_end):
    leg_vertical = abs(grid[row_start][col_start] - grid[row_end][col_end])
    if row_start == row_end or col_start == col_end:
        leg_horizontal = 0.1 * (2 ** 0.5)
    else: 
        leg_horizontal = 0.1
    angle = math.degrees(math.atan2(log_vertical, log_horizontal))
    return angle <= 30

def calculate_h(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5
    

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
