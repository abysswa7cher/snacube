from random import randint
from src.classes.generic_model import Model
from src.classes.helpers.vectors import Vector3
from src.globals import CWD, GRID_DIMENSIONS, GRID_SIZE, FOOD_MODEL


class Food(Model):
    """
    Food class for player to eat.
    """
    def __init__(self, turtle):
        """Default constructor.

        Args:
            turtle (turtle.Turtle): Turtle instance reference for drawing.
        """
        path = f"{CWD}\\assets\\{FOOD_MODEL}"
        super().__init__(turtle, path)
        self.world_position = Vector3(
            randint(-GRID_DIMENSIONS, GRID_DIMENSIONS) // GRID_SIZE,
            randint(-GRID_DIMENSIONS, GRID_DIMENSIONS) // GRID_SIZE,
            randint(-GRID_DIMENSIONS, GRID_DIMENSIONS) // GRID_SIZE,
        )

    def update(self):
        self.rotate(Vector3(0, 2, 0))
