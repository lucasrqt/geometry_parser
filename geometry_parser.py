from typing import Dict, List
from utils.shapes import Square, Cubes, Point
from utils.error_geometry import ErrorGeometry
import numpy as np
 

def get_squares(grouped_by_x: Dict[int, List[int]]) -> List[Square]:
    """
    Get the squares from the grouped by x
    """
    squares = []
    xs = list(grouped_by_x.keys())
    for i in range(len(xs) - 1):
        for j in range(len(xs[i+1:])):
            x1, x2 = xs[i], xs[j+i+1]
            if x1 == x2:
                continue
            y1 = set(grouped_by_x[x1])
            y2 = set(grouped_by_x[x2])
            intersection = y1.intersection(y2)
            if len(intersection) >= 2:
                unique_pairs = set()
                for y1_val in intersection:
                    for y2_val in intersection:
                        if y1_val != y2_val:
                            pair = tuple(sorted([y1_val, y2_val]))
                            if pair not in unique_pairs:
                                unique_pairs.add(pair)
                                squares.append(Square([
                                    Point(-1, x1, y1_val),
                                    Point(-1, x1, y2_val),
                                    Point(-1, x2, y1_val),
                                    Point(-1, x2, y2_val)
                                ]))
    return squares



def get_cuboids(corrupted_positions) -> List[Cubes]:
    """Get all the cuboids from the corrupted coordinates and return the count of the cuboids

    Input:
    corrupted_positions: np.ndarray - corrupted positions in the tensor
    """
    cuboids = []
    
    values_d, counts_d = np.unique(corrupted_positions[:, 0], return_counts=True)
    values_x, counts_x  = np.unique(corrupted_positions[:, 1], return_counts=True)
    values_y, counts_y = np.unique(corrupted_positions[:, 2], return_counts=True)

    grouped_by_depth = {
        x: [] for x in values_d
    }

    squares_by_depth = {
        x: [] for x in values_d
    }

    for i in range(len(corrupted_positions)):
        d, x, y = corrupted_positions[i]
        grouped_by_depth[d].append((x, y))

    for depth, coordinates in grouped_by_depth.items():
        grouped_by_x = group_by_axis([x for x, _ in coordinates], [y for _, y in coordinates])
        squares_by_depth[depth] = get_squares(grouped_by_x)

    for i in range(len(values_d) - 1):
        for j in range(len(values_d[i+1:])):
            d1, d2 = values_d[i], values_d[j+i+1]
            if d1 == d2:
                continue
            squares1 = squares_by_depth[d1]
            squares2 = squares_by_depth[d2]
            for s1 in squares1:
                for s2 in squares2:
                    if s1 == s2:
                        cuboids.append(Cubes([
                            Point(d1, s1.coordinates[0].row, s1.coordinates[0].col),
                            Point(d1, s1.coordinates[1].row, s1.coordinates[1].col),
                            Point(d1, s1.coordinates[2].row, s1.coordinates[2].col),
                            Point(d1, s1.coordinates[3].row, s1.coordinates[3].col),
                            Point(d2, s2.coordinates[0].row, s2.coordinates[0].col),
                            Point(d2, s2.coordinates[1].row, s2.coordinates[1].col),
                            Point(d2, s2.coordinates[2].row, s2.coordinates[2].col),
                            Point(d2, s2.coordinates[3].row, s2.coordinates[3].col),
                        ]))
        

    return cuboids
    
    

def group_by_axis(a1, a2) -> Dict[int, List[int]]:
    """Group the values by axis, this is useful to get the squares (with intersections)
        -- if the intersection is greater than 2, then it is a square

    Input:
    a1: List[int] - values for the first axis
    a2: List[int] - values for the second axis
    
    Example:
    a1 = [1, 1, 1, 2, 2, 2]
    a2 = [1, 4, 3, 10, 28, 93]
    grouped = {
        1: [1, 4, 3],
        2: [10, 28, 93]
    }
    """
    grouped = {
        x: [] for x in a1
    }
    
    for i, x in enumerate(a1):
        grouped[x].append(a2[i])

    return grouped

def check_1D(values: np.ndarray) -> ErrorGeometry:
    """
    Check error shape in 1D tensor
    """
    if len(values) > 1:
        return ErrorGeometry.LINE
    elif len(values) == 1:
        return ErrorGeometry.SINGLE
    else:
        return ErrorGeometry.MASKED
    
def check_2D(corrupted_positions) -> ErrorGeometry:
    """
    Check if the error is in a 2D tensor
    """
    rows, cols = corrupted_positions[:, 0], corrupted_positions[:, 1]
    values_x, counts_x  = np.unique(x_axis, return_counts=True)
    values_y, counts_y = np.unique(y_axis, return_counts=True)
    x_axis = [int(x) for x in x_axis]
    y_axis = [int(x) for x in y_axis]
    values_x = [int(x) for x in values_x]

    grouped_by_x = group_by_axis(x_axis, y_axis)

    squares = get_squares(grouped_by_x)

    if len(squares) > 0:
        return ErrorGeometry.SQUARE_2D
    elif len(counts_x) == 1 or len(counts_y) == 1:
        return ErrorGeometry.LINE
    elif len(counts_x) > 1 and len(counts_y) > 1:
        return ErrorGeometry.RANDOM
    elif len(counts_x) == 1 and len(counts_y) == 1:
        return ErrorGeometry.SINGLE

    return ErrorGeometry.MASKED
    
def check_3D(corrupted_positions) -> ErrorGeometry:
    """
    Check if the error is in a 3D tensor
    """
    error = ErrorGeometry.MASKED
    
    depths, rows, cols = corrupted_positions[:, 0], corrupted_positions[:, 1], corrupted_positions[:, 2]

    values_z, counts_z = np.unique(depths, return_counts=True)
    values_x, counts_x  = np.unique(rows, return_counts=True)
    values_y, counts_y = np.unique(cols, return_counts=True)

    # check for lines, if no lines, return, else check for squares
    if counts_x.max() == 1 and counts_y.max() == 1 and counts_z.max() == 1:
        return ErrorGeometry.RANDOM    
        
    error = ErrorGeometry.LINE

    rows = [int(x) for x in rows]
    cols = [int(x) for x in cols]
    depths = [int(x) for x in depths]

    values_x = [int(x) for x in values_x]
    values_y = [int(x) for x in values_y]
    values_z = [int(x) for x in values_z]

    grouped_by_x = group_by_axis(rows, cols)
    grouped_by_y = group_by_axis(cols, depths)
    grouped_by_z = group_by_axis(depths, rows)

    squares_xy = get_squares(grouped_by_x)
    squares_yz = get_squares(grouped_by_y)
    squares_xz = get_squares(grouped_by_z)

    if not squares_xy and not squares_yz and not squares_xz: # if no squares, return line
        return error

    error = ErrorGeometry.SQUARE_3D 

    cubes = get_cuboids(corrupted_positions)
    
    if not cubes:
        return error

    error = ErrorGeometry.CUBIC
    return error

def geometry_comparison(diff: np.ndarray) -> ErrorGeometry:
    """
    This should receive as input a diff matrix np array with the same size of the tensors
    """
    count_non_zero_diff = np.count_nonzero(diff)

    if count_non_zero_diff == 1:
        return ErrorGeometry.SINGLE
    elif count_non_zero_diff > 1:
        dim = diff.ndim
        if dim > 3 or dim < 1:
            raise ValueError("Diff dimensions should be between 1-3")

        # Use label function to labeling the matrix
        corrupted_positions = np.argwhere(diff != 0)
        # print(corrupted_positions[:, 0])

        if dim == 1:
            return check_1D(corrupted_positions)
        elif dim == 2:
            return check_2D(corrupted_positions)
        elif dim == 3:
            return check_3D(corrupted_positions)

    return ErrorGeometry.MASKED