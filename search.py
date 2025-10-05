import heapq
import math
import numpy

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

def is_valid(row, col):
    limit_row = 100
    limit_col = 100    
    return (row >= 0) and (row < limit_row) and (col >= 0) and (col < limit_col)

def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

def can_be_climbed(grid, row_start, col_start, row_end, col_end):
    leg_vertical = abs(grid[row_start][col_start] - grid[row_end][col_end])
    if row_start == row_end or col_start == col_end:
        leg_horizontal = 0.1
    else: 
        leg_horizontal = 0.1 * (2 ** 0.5)    
    angle = math.degrees(math.atan2(leg_vertical, leg_horizontal))
    # print(f"Angle: {angle}")
    return angle <= 30

def calculate_h(row, col, dest):
    dx = abs(row - dest[0]) * 0.1 
    dy = abs(col - dest[1]) * 0.1
    return (2 ** 0.5 - 1) * min(dx, dy) + max(dx, dy)
    # return (dx ** 2 + dy ** 2) ** 0.5
    

# def trace_path(cells, src, dest):
#     path = []
#     row = dest[0]
#     col = dest[1]

#     while not(src[0] == row and src[1] == col):
#         # Add the current node
#         path.append((row, col))
#         # print(f"Path now: {path}")
#         # Update the data, go to the previous node
#         row = cells[row][col].parent_x
#         col = cells[row][col].parent_y

#     path.append((row, col))
#     path.reverse()
#     return path

def trace_path(cells, src, dest):
    path = []
    row, col = dest
    visited = set()

    while (row, col) not in visited:
        visited.add((row, col))
        path.append((row, col))

        if (row, col) == src:   # stop when we reach the source
            break

        row, col = cells[row][col].parent_x, cells[row][col].parent_y

    path.reverse()
    return path

# A* algorithm
# Dijkstra is not as effective as it can be in these settings.
def a_star(grid, src, dest):
    print("Start search")   
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
    open_set = set()
    heapq.heappush(open_list, (0.0, i, j))
    open_set.add((i, j))
    found_dest = False

    directions = [(0, 1),(1, 0),(-1, 0),(0, -1),(1, 1),(-1, -1),(1, -1),(-1, 1)]

    while len(open_list) > 0:
        p = heapq.heappop(open_list)

        i = p[1]
        j = p[2]
        if closed_list[i][j]:
            continue
        closed_list[i][j] = True

        # print(f"Considered node: {p}")

        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]
      
            if not is_valid(new_i, new_j):
                continue

            if closed_list[new_i][new_j]:
                continue
            
            if not can_be_climbed(grid, i, j, new_i, new_j):
                continue
            
            # print(f"New node: ({new_i}, {new_j})")
            if is_destination(new_i, new_j, dest):
                cells[new_i][new_j].parent_x = i
                cells[new_i][new_j].parent_y = j
                print("The destination was found")
                found_dest = True
                return trace_path(cells, src, dest)
                
            g_new = cells[i][j].g + 1.0 * (2 ** 0.5 if abs(dir[0]) == abs(dir[1]) else 1)
            h_new = calculate_h(new_i, new_j, dest)
            f_new = g_new + h_new

            if cells[new_i][new_j].f > f_new:
                cells[new_i][new_j].f = f_new
                cells[new_i][new_j].g = g_new
                cells[new_i][new_j].h = h_new
                cells[new_i][new_j].parent_x = i
                cells[new_i][new_j].parent_y = j

                if (new_i, new_j) not in open_set:
                    heapq.heappush(open_list, (f_new, new_i, new_j))
                    open_set.add((new_i, new_j))
                    

    if not found_dest:
        print("Failed to find the path to the destination")

def prepare_weights(red_channel):
    grid = numpy.array(red_channel)
    normalized = grid / 255.0
    height_map = normalized * 3.0
    return height_map
 
