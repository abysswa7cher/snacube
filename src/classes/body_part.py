from copy import copy
from random import choice
import src.globals as GLOBALS
from src.classes.generic_model import Model
from src.classes.helpers.vectors import Vector3

# Static values for body parts rotations

POS_Z_ROT = Vector3(0, 1.53, 0)
NEG_Z_ROT = Vector3(0, -1.58, 0)
POS_Y_ROT = Vector3(0, 0, -1.64)
NEG_Y_ROT = Vector3(0, 0, -4.75)
POS_X_ROT = Vector3(0, 3.08, 0)
NEG_X_ROT = Vector3(0, 0, 0)


class BodyPart(Model):
    """Class representing a body part of the snake.

    Args:
        Model (Model): type of model to use (e.g. head, middle section, tail).
    """
    def __init__(self, turtle, color=None, path=None):
        """Default constructor.

        Args:
            turtle (turtle): The Turle object to draw the body part with.
            color (Color, optional): Optional color argument to override the default one. Defaults to None.
            path (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(turtle, path)
        self.direction = Vector3(0, 0, 1)
        if color is None:
            for mesh in self.meshes:
                mesh.color = choice(GLOBALS.COLORS)
        else:
            for mesh in self.meshes:
                mesh.color = color
        self.next = None

    def update(self):
        if self.direction == Vector3(1, 0, 0):
            self.world_rotation = POS_X_ROT
        elif self.direction == Vector3(-1, 0, 0):
            self.world_rotation = NEG_X_ROT
        elif self.direction == Vector3(0, 1, 0):
            self.world_rotation = POS_Y_ROT
        elif self.direction == Vector3(0, -1, 0):
            self.world_rotation = NEG_Y_ROT
        elif self.direction == Vector3(0, 0, 1):
            self.world_rotation = POS_Z_ROT
        elif self.direction == Vector3(0, 0, -1):
            self.world_rotation = NEG_Z_ROT

    def displace(self, direction):
        return Vector3(
            self.world_position.x - direction.x,
            self.world_position.y - direction.y,
            self.world_position.z - direction.z,
        )

    def get_last(self) -> "BodyPart":
        last = self
        while last.next is not None:
            last = last.next

        return last

    def __repr__(self):
        return f"BodyPart(pos: {self.world_position}, dir: {self.direction}, rot: {self.world_rotation})"

    def copy(self):
        return copy(self)