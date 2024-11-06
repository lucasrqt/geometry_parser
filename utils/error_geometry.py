import enum

class ErrorGeometry(enum.Enum):
    MASKED = -1
    SINGLE = 0
    RANDOM = 1
    LINE = 2
    SQUARE_2D = 3
    SQUARE_3D = 4
    CUBIC = 5

    def __gt__(self, other): return self.value > other.value

    def __lt__(self, other): return self.value < other.value

    def __str__(self): return self.name

    def __repr__(self): return self.name