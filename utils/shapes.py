from typing import List

# Geometry utils
class Point():
    d = 0
    row = 0
    col = 0

    def __init__(self, d: int, row: int, col: int):
        self.d = d
        self.row = row
        self.col = col
    
    def __str__(self):
        return f"Point({self.d}, {self.row}, {self.col})"
    
    def __repr__(self):
        return f"Point({self.d}, {self.row}, {self.col})"
    
    def __eq__(self, other) -> bool:
        return self.d == other.d and self.row == other.row and self.col == other.col


class Square():
    coordinates = []

    def __init__(self, coordinates: List[Point]):
        if len(coordinates) != 4:
            raise ValueError("Square should have 4 coordinates")
        self.coordinates = coordinates

    def __str__(self):
        return f"Square({self.coordinates})"
    
    def __repr__(self):
        return f"Square({self.coordinates})"
    
    def __eq__(self, other) -> bool:
        return all([p in other.coordinates for p in self.coordinates])


class Cubes():
    coordinates = []

    def __init__(self, coordinates: List[Point]):
        if len(coordinates) != 8:
            raise ValueError("Cubes should have 8 coordinates")
        self.coordinates = coordinates

    def __str__(self):
        return f"Cubes({self.coordinates})"
    
    def __repr__(self):
        return f"Cubes({self.coordinates})"