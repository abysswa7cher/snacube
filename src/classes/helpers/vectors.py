import math


class Vector2:
    """
    Default constructor.
    
    Args:
        x (int | float): X coordinate.
        y (int | float): Y coordinate.
        
    Returns:
        Vector2: object representing a vector with 2 coordinates and vector math helper functions.
    """
    def __init__(self, x: int | float = 0, y: int | float= 0):
        self.x = x
        self.y = y

    @classmethod
    def from_list(cls, vertices: list | tuple) -> "Vector2":
        """
        Creates a Vector2 object from a list-like object with coordinates.
        """
        if len(vertices) == 2:
            x = vertices[0]
            y = vertices[1]
            return cls(x, y)
        else:
            raise ValueError(
                f"a list has to contain exactly 2 values to construct Vector2 ({len(vertices)} was given)"
            )

    def length(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)
    
    def __mul__(self, other: "Vector2") -> int | float:
        return self.x * other.x + self.y * other.y

    def __sub__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x - other.x, self.y - other.y)

    def __add__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x + other.x, self.y + other.y)

    def __repr__(self) -> str:
        return f"Vector2({self.x}, {self.y})"


class Vector3:
    """
    Default constructor.
    
    Args:
        x (int | float): X coordinate.
        y (int | float): Y coordinate.
        z (int | float): Z coordinate.
        
    Returns:
        Vector3: object representing a vector with 3 coordinates  and vector math helper functions.
    """
    def __init__(self, x: int | float = 0, y: int | float = 0, z: int | float = 0):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_list(cls, vertices: list | tuple) -> "Vector3":
        """
        Creates a Vector3 object from a list-like object with coordinates.
        """
        if len(vertices) == 3:
            x = vertices[0]
            y = vertices[1]
            z = vertices[2]
            return cls(x, y, z)
        else:
            raise ValueError(
                f"a list has to contain exactly 3 values to construct Vector3 ({len(vertices)} was given)"
            )

    def length(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __sub__(self, other: "Vector3") -> "Vector3":
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other: "Vector3") -> "Vector3":
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other: "Vector3") -> "Vector3":
        return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __eq__(self, other):
        if isinstance(other, Vector3):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False

    def __repr__(self) -> str:
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def copy(self) -> "Vector3":
        return Vector3(self.x, self.y, self.z)

    def isclose(self, other: "Vector3") -> bool:
        return (
            math.isclose(self.x, other.x, abs_tol=0.1)
            and math.isclose(self.y, other.y, abs_tol=0.1)
            and math.isclose(self.z, other.z, abs_tol=0.1)
        )

    def normalize(self) -> "Vector3":
        length = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        return Vector3(
            self.x / length,
            self.y / length,
            self.z / length
        )

    def scale(self, n) -> "Vector3":
        return Vector3(
            self.x * n, self.y * n, self.z * n
        )
    
    def negate(self) -> "Vector3":
        return Vector3(
            -self.x, -self.y, -self.z
        )