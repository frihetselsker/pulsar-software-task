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
    grid = resize_image(path)
    height_map = prepare_weights(grid)
    print(f"Size: {len(grid)}x{len(grid[0])}")
    print(height_map)
    src = (1, 1)
    dest = (1, 10)
    paths = search(height_map, src, dest)
    print(paths)

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
    angle = math.degrees(math.atan2(leg_vertical, leg_horizontal))
    return angle <= 30

def calculate_h(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5
    

def trace_path(cells, dest):
    path = []
    row = dest[0]
    col = dest[1]

    while not(cells[row][col].parent_x == row and cells[row][col].parent_y == col):
        # Add the current node
        path.append((row, col))
        # Update the data, go to the previous node
        row = cells[row][col].parent_x
        col = cells[row][col].parent_y

    path.append((row, col))
    path.reverse()
    return path

# A* algorithm
# Dijkstra is not as effective as it can be in these settings.
def search(grid, src, dest):
    if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
        print("The coordinates are not correct")
        return
    if is_destination(src[0], src[1], dest):
        print("The search is unnecessary since it is already a destination")
        return

    closed_list = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    cells = [[Cell() for _ in range(len(grid[0]))] for _ in range(len(grid))]

    i = src[0]
    j = src[1]
    cells[i][j].f = 0
    cells[i][j].g = 0
    cells[i][j].h = 0
    # This is how we are gonna be able to find the root node.
    cells[i][j].parent_x = i
    cells[i][j].parent_y = j

    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    found_dest = False

    directions = [(0, 1),(1, 0),(-1, 0),(0, -1),(1, 1),(-1, -1),(1, -1),(-1, 1)]

    while len(open_list) > 0:
        p = heapq.heappop(open_list)

        i = p[1]
        j = p[2]
        closed_list[i][j] = True

        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            if abs(dir[0]) == abs(dir[1]):
                g_multiply = 2 ** 0.5
            else: 
                g_multiply = 1
            
            if is_valid(new_i, new_j) and can_be_climbed(grid, i, j, new_i, new_j) and not closed_list[new_i][new_j]:
                if is_destination(new_i, new_j, dest):
                    cells[new_i][new_j].parent_x = i
                    cells[new_i][new_j].parent_y = j
                    print("The destination was found")
                    return trace_path(cells, dest)
                else:
                    g_new = cells[i][j].g + 1.0 * g_multiply
                    h_new = calculate_h(new_i, new_j, dest)
                    f_new = g_new + h_new

                    if cells[new_i][new_j].f == float('inf') or cells[new_i][new_j].f > f_new:
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        cells[new_i][new_j].f = f_new
                        cells[new_i][new_j].g = g_new
                        cells[new_i][new_j].h = h_new
                        cells[new_i][new_j].parent_x = i
                        cells[new_i][new_j].parent_y = j

    if not found_dest:
        print("Failed to find the path to the destination")


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
