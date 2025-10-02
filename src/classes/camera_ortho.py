import math
from src.globals import SCREEN_WIDTH, SCREEN_HEIGHT
from src.classes.helpers.vectors import Vector3, Vector2


class Camera:
    """
    Orthographic camera.
    """
    def __init__(self, position: Vector3 = Vector3(), scale: float = 1.0):
        self.position = position
        self.scale = scale

        self.angle_x = math.radians(30)
        self.angle_y = math.radians(40)

        self.cos_x = math.cos(self.angle_x)
        self.sin_x = math.sin(self.angle_x)
        self.cos_y = math.cos(self.angle_y)
        self.sin_y = math.sin(-self.angle_y)

    def project_point(self, point: Vector3) -> Vector2:
        rel_x = point.x - self.position.x
        rel_y = point.y - self.position.y
        rel_z = point.z - self.position.z

        rot_x = rel_x * self.cos_y - rel_z * self.sin_y
        rot_z = rel_x * self.sin_y + rel_z * self.cos_y

        proj_x = rot_x
        proj_y = rel_y * self.cos_x + rot_z * self.sin_x

        screen_x = proj_x * self.scale + SCREEN_WIDTH / 2
        screen_y = proj_y * self.scale + SCREEN_HEIGHT / 2

        return Vector2(screen_x, screen_y)
