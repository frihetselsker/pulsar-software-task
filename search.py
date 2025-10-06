from PIL import ImageFile

import heapq
import math
import numpy

class Cell:
    """
    A class representing a graph node.

    Attributes:
        parent_i (int): The row of the previous node.
        parent_j (int): The column of the previous node.
        f (float): The estimate of the total cost from start node to destination node through the current node.
        g (float): The actual cost from start node to the current node.
        h (float): The heuristic cost from the current node to desctination node.
    """    
    def __init__(self):
        """
        Initialize a Cell object.
        """        
        # To backtrack the path from the source node to the destination node
        self.parent_i = 0
        self.parent_j = 0
        # f = g + h
        self.f = float('inf')
        # The actual cost: src_node -> current_node
        self.g = float('inf')
        # The heuristic cost: current_node -> dest_node
        # Without diagonals: Manhattan distance 
        # With diagonals: Chebyshev distance with weigheted diagnal move
        self.h = 0

def is_valid(row: int, col: int) -> bool:
    """
    Check if the provided coordinates are valid, i.e. reachable.
    It is used to avoid IndexError.

    Args:
        row (int): The row of considered node.
        col (int): The column of considered node.

    Returns:
        bool: The result of check.
    """
    # Since limits are specified by the task, they are set in the program.
    limit_row = 100
    limit_col = 100
    # No negative and out of range indices.     
    return (row >= 0) and (row < limit_row) and (col >= 0) and (col < limit_col)

def is_destination(row: int, col: int, dest: (int, int)) -> bool:
    """
    Check if the provided coordinates are of the destination node.

    Args:
        row (int): The row of considered node.
        col (int): The column of considered node.
        dest ( (int, int) ): The tuple of destination node coordinates.

    Returns:
        bool: The result of check.
    """    
    return row == dest[0] and col == dest[1]

def can_be_climbed(grid: list[list[int]], row_start: int, col_start: int, row_end: int, col_end: int) -> bool:
    """
    Check if the rover can climb on this node, i.e. angle is less or equal than 30 degrees.

    Args:
        grid ([int][int]): The 2D list that contains all the heights of terrain considered.
        row_start (int): The row of current node.
        col_start (int): The column of current node.
        row_end (int): The row of next node.
        col_end (int): The column of next node.    
    
    Returns:
        bool: The result of check.
    """    
    
    # Like in the right triangle.
    # For simplicity, we are looking for the arctangent.
    
    # Calculate height.
    leg_vertical = abs(grid[row_start][col_start] - grid[row_end][col_end])
    # If one of the coordinates matches, then it is a non-diagonal move.
    if row_start == row_end or col_start == col_end:
        # According to the task, it is 0.1 m.
        leg_horizontal = 0.1
    else: 
        # Diagonal of square is sqrt(2) * side.
        leg_horizontal = 0.1 * (2 ** 0.5)    
    angle = math.degrees(math.atan2(leg_vertical, leg_horizontal))
    return angle <= 30


def calculate_h(row: int, col: int, dest: (int, int), is_diagonal_allowed: bool):
    """
    Calculate the heuristic cost to destination node (h) for the current node. 

    Args:
        row_start (int): The row of current node.
        col_start (int): The column of current node.        
        dest ( (int, int) ): The tuple of destination node coordinates.
        is_diagonal_allowed (bool): Checks if the diagonal moves are allowed.
        
    Returns:
        float: The calculated h.
    """    
    # Accroding to the task, the unit distance is 0.1 m.
    dx = abs(row - dest[0]) * 0.1 
    dy = abs(col - dest[1]) * 0.1
    if is_diagonal_allowed:
        # Use Chebyshev distance with weighted diagonal moves
        # If it is a non_diagonal move, then some of differences is zero.
        # Therefore, the formula turns into (e.g. dx = 0): 
        
        # (2 ** 0.5 - 1) * min(0, dy) + max(0, dy) = 
        # (2 ** 0.5 - 1) * 0 + dy =
        # dy

        # If it is a diagonal move, then all the differences are not zero.
        # Therefore, the formula becomes (dx = dy):
        # (2 ** 0.5 - 1) * min(dx, dy) + max(dx, dy) =
        # 2 ** 0.5 * dx - dx + dx = 2 ** 0.5 * dx
        # Which is right and covers the second case.
        return (2 ** 0.5 - 1) * min(dx, dy) + max(dx, dy)
    else:
        # Use Manhattan distance for only-diagonal movement.
        # It is more accurate than Euclidean distance and shows the actual distance in terms of movements.
        return dx + dy
    
def trace_path(cells: list[list[Cell]], src: (int, int), dest: (int, int)) -> [(int, int)]:
    
    """
    Create the list of coordinates that represent the path from source node to destination node. 
    This list is used for path drawing.

    Args:
        cells ([Cell][Cell]): The 2D list containing all the information about each node
        source ( (int, int) ):  The tuple source node coordinates. 
        dest ( (int, int) ): The tuple of destination node coordinates.
        
    Returns:
        [(int)(int)]: The list of coordinates from source to destination.
    """    
    path = []
    row, col = dest
    # We can use set since all the nodes are unique.
    visited = set()

    # Stay in loop till it reaches the source node.
    while (row, col) not in visited:
        visited.add((row, col))
        path.append((row, col))

        # It is the second check.
        # Stop when we reach the source.        
        if (row, col) == src:   
            break

        # This is the reason of parent_i and parent_j existance.
        row, col = cells[row][col].parent_i, cells[row][col].parent_j

    # Reverse because now path goes from destination to source.
    path.reverse()
    # Real coordinates are x = col and y = row
    # We change the order back.
    path_coords = [(col, row) for row, col in path]
    print(f"Path: {path_coords}")
    return path

# A* algorithm
# Dijkstra is not as effective as it can be in these settings.
def a_star(grid: list[list[Cell]], src: (int, int), dest: (int, int), is_diagonal_allowed: bool) -> [(int, int)]:
    # Check if both source and destination nodes are valid.
    if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
        print("The coordinates are not correct")
        return
    # Early exit
    if is_destination(src[0], src[1], dest):
        print("The search is unnecessary since it is already a destination")
        return

    # Initialization part
    closed_list = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    cells = [[Cell() for _ in range(len(grid[0]))] for _ in range(len(grid))]

    # Starting coordinates
    i = src[0]
    j = src[1]
    # At start, all the costs are zero.
    cells[i][j].f = 0
    cells[i][j].g = 0
    cells[i][j].h = 0
    # This is how source node can be found.
    cells[i][j].parent_i = i
    cells[i][j].parent_j = j

    # Priority queue to track the node with the least cost
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))
    if is_diagonal_allowed:
        directions = [(0, 1),(1, 0),(-1, 0),(0, -1),(1, 1),(-1, -1),(1, -1),(-1, 1)]
    else:
        directions = [(0, 1),(1, 0),(-1, 0),(0, -1)]
    # The actual search
    while open_list:
        # Pop the node wit hthe lowest f-cost.
        p = heapq.heappop(open_list)

        i = p[1]
        j = p[2]
        # Check if it is already visited.
        if closed_list[i][j]:
            continue
        # If not visited, continue the algorithm.
        closed_list[i][j] = True

        if is_destination(i, j, dest):
            print("The destination was found")
            return trace_path(cells, src, dest)

        # Check all the directions.
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            # Check if new node is valid.      
            if not is_valid(new_i, new_j):
                continue
            # Check if new node is visited.
            if closed_list[new_i][new_j]:
                continue
            # Check if it can be climbed.
            if not can_be_climbed(grid, i, j, new_i, new_j):
                continue
            
            # If diagonal, then square root of 2.
            # Otherwise, leave as-is. 
            if is_diagonal_allowed and abs(dir[0]) == abs(dir[1]):
                g_step = (2 ** 0.5)
            else:
                g_step = 1.0
            # Calculate costs for a new node.    
            g_new = cells[i][j].g + g_step * 0.1
            h_new = calculate_h(new_i, new_j, dest, is_diagonal_allowed)
            f_new = g_new + h_new

            # If new costs are less, then update cells.
            if cells[new_i][new_j].f > f_new:
                cells[new_i][new_j].f = f_new
                cells[new_i][new_j].g = g_new
                cells[new_i][new_j].h = h_new
                cells[new_i][new_j].parent_i = i
                cells[new_i][new_j].parent_j = j

                # Put it to the open list so that it can be considered during the loop.
                heapq.heappush(open_list, (f_new, new_i, new_j))
                if is_destination(new_i, new_j, dest):
                    return trace_path(cells, src, dest)
                    
    print("Failed to find the path to the destination")
    return None

def prepare_weights(red_channel: ImageFile.ImageFile) -> list[list[int]]:
    """
    Convert the image to the array.
    Normalize, multiple with the height.

    Args:
        red_channel (ImageFile.ImageFile): PIL ImageFile object with only red_channel extracted.

    Returns:
       [int][int]: height map, i.e 2D array with all the heights.
    """    
    grid = numpy.array(red_channel)
    normalized = grid / 255.0
    # According to the task, 0 corresponds to 0 m and 1 corresponds to 3 m.
    height_map = normalized * 3.0
    return height_map
 
