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
    return angle <= 30


def calculate_h(row, col, dest, is_diagonal_allowed):
    dx = abs(row - dest[0]) * 0.1 
    dy = abs(col - dest[1]) * 0.1
    if is_diagonal_allowed:
        return (2 ** 0.5 - 1) * min(dx, dy) + max(dx, dy)
    else:
        return dx + dy
    
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
    path_coords = [(col, row) for row, col in path]
    print(f"Path: {path_coords}")
    return path

# A* algorithm
# Dijkstra is not as effective as it can be in these settings.
def a_star(grid, src, dest, is_diagonal_allowed):
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
    counter = 0
    heapq.heappush(open_list, (0.0, counter, i, j))
    counter += 1
    if is_diagonal_allowed:
        directions = [(0, 1),(1, 0),(-1, 0),(0, -1),(1, 1),(-1, -1),(1, -1),(-1, 1)]
    else:
        directions = [(0, 1),(1, 0),(-1, 0),(0, -1)]
        
    while open_list:
        p = heapq.heappop(open_list)

        # f = p[0]
        i = p[2]
        j = p[3]
        if closed_list[i][j]:
            continue
        closed_list[i][j] = True

        if is_destination(i, j, dest):
            print("The destination was found")
            return trace_path(cells, src, dest)

        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            
            if not is_diagonal_allowed and abs(new_i - i) + abs(new_j - j) != 1:
                continue      
            if not is_valid(new_i, new_j):
                continue
            if closed_list[new_i][new_j]:
                continue
            if not can_be_climbed(grid, i, j, new_i, new_j):
                continue
            
             
            if is_diagonal_allowed and abs(dir[0]) == abs(dir[1]):
                g_step = (2 ** 0.5)
            else:
                g_step = 1.0
            g_new = cells[i][j].g + g_step * 0.1
            h_new = calculate_h(new_i, new_j, dest, is_diagonal_allowed)
            f_new = g_new + h_new

            if cells[new_i][new_j].f > f_new:
                cells[new_i][new_j].f = f_new
                cells[new_i][new_j].g = g_new
                cells[new_i][new_j].h = h_new
                cells[new_i][new_j].parent_x = i
                cells[new_i][new_j].parent_y = j

                heapq.heappush(open_list, (f_new, counter, new_i, new_j))
                counter += 1

                if is_destination(new_i, new_j, dest):
                    return trace_path(cells, src, dest)
                    
    print("Failed to find the path to the destination")
    return None

def prepare_weights(red_channel):
    grid = numpy.array(red_channel)
    normalized = grid / 255.0
    height_map = normalized * 3.0
    return height_map
 
