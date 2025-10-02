import math, turtle
import src.globals as GLOBALS
from src.classes.helpers.vectors import Vector2, Vector3

class Camera:
    """
    Perspective camera.
    """
    def __init__(self, position: Vector3 = None, target: Vector3 = None):
        self.position = position or Vector3(50.0, 35.0, 45.0)
        self.target = target or Vector3(20.0, 20.0, 20.0)
        self.up = Vector3(0.0, 1.0, 0.0)

        self.fov = math.radians(80)
        self.aspect = GLOBALS.SCREEN_WIDTH / GLOBALS.SCREEN_HEIGHT
        self.near = 1.0
        self.far = 1000.0
        
        self.zoom = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 3.0
        
        self.initial_distance = math.sqrt(
            (self.position.x - self.target.x) ** 2 +
            (self.position.y - self.target.y) ** 2 +
            (self.position.z - self.target.z) ** 2
        )

        self._calculate_view_matrix()
        self._calculate_projection_matrix()
        
        
        turtle.listen()

    def move_x(self, dist):
        self.position += Vector3(dist, 0, 0)
        
    def move_y(self, dist):
        self.position += Vector3(0, dist, 0)
        
    def _calculate_view_matrix(self):
        # calculate forward vector (from camera to target)
        self.forward = Vector3(
            self.target.x - self.position.x,
            self.target.y - self.position.y,
            self.target.z - self.position.z
        )
        self.forward = self.forward.normalize()
        
        # calculate right vector
        world_up = Vector3(0.0, 1.0, 0.0)
        self.right = Vector3(
            self.forward.z * world_up.y - self.forward.y * world_up.z,
            self.forward.x * world_up.z - self.forward.z * world_up.x,
            self.forward.y * world_up.x - self.forward.x * world_up.y
        )
        self.right = self.right.normalize()
        
        # recalculate camera up vector from right and forward
        self.up = Vector3(
            self.right.y * self.forward.z - self.right.z * self.forward.y,
            self.right.z * self.forward.x - self.right.x * self.forward.z,
            self.right.x * self.forward.y - self.right.y * self.forward.x
        )
        self.up = self.up.normalize()

    def _calculate_projection_matrix(self):
        self.f = 1.0 / math.tan(self.fov / 2.0)
        self.projection_scale = self.f

    def project_point(self, point: Vector3) -> Vector2:
        # transform point to camera space
        rel_x = point.x - self.position.x
        rel_y = point.y - self.position.y
        rel_z = point.z - self.position.z

        # calculate dot products for view space transformation
        view_x = rel_x * self.right.x + rel_y * self.right.y + rel_z * self.right.z
        view_y = rel_x * self.up.x + rel_y * self.up.y + rel_z * self.up.z
        view_z = rel_x * self.forward.x + rel_y * self.forward.y + rel_z * self.forward.z

        if view_z <= self.near:
            return Vector2(GLOBALS.SCREEN_WIDTH / 2, GLOBALS.SCREEN_HEIGHT / 2)

        # apply perspective projection with zoom
        perspective_factor = self.f / view_z * self.zoom
        
        # apply perspective projection
        screen_x = -view_x * perspective_factor
        screen_y = view_y * perspective_factor
        
        # adjust x for aspect ratio
        screen_x *= self.aspect

        # convert to screen coordinates
        screen_x = (screen_x + 1.0) * GLOBALS.SCREEN_WIDTH * 0.5
        screen_y = (1.0 - screen_y) * GLOBALS.SCREEN_HEIGHT * 0.5  # Flip Y for screen coordinates

        return Vector2(screen_x, screen_y)

    def set_zoom(self, zoom: float):
        self.zoom = max(self.min_zoom, min(self.max_zoom, zoom))
        self._update_position_for_zoom()

    def adjust_zoom(self, amount: float):
        self.set_zoom(self.zoom + amount)

    def _update_position_for_zoom(self):
        # calculate direction from target to camera
        direction = Vector3(
            self.position.x - self.target.x,
            self.position.y - self.target.y,
            self.position.z - self.target.z
        )
        
        # calculate the distance based on zoom
        desired_distance = self.initial_distance / self.zoom
        
        # normalize direction and scale to desired distance
        length = math.sqrt(direction.x**2 + direction.y**2 + direction.z**2)
        self.position = Vector3(
            self.target.x + (direction.x / length) * desired_distance,
            self.target.y + (direction.y / length) * desired_distance,
            self.target.z + (direction.z / length) * desired_distance
        )
        
        self._calculate_view_matrix()

    def move(self, delta: Vector3):
        self.position = Vector3(
            self.position.x + delta.x,
            self.position.y + delta.y,
            self.position.z + delta.z
        )
        self.target = Vector3(
            self.target.x + delta.x,
            self.target.y + delta.y,
            self.target.z + delta.z
        )
        self._calculate_view_matrix()

    def look_at(self, target: Vector3):
        self.target = target
        self._update_position_for_zoom()

    def get_camera_spherical_coords(self):
        """
        Calculate the current spherical coordinates of the camera relative to the target
        Returns: (radius, phi, theta) where:
            - radius: distance from target to camera
            - phi: horizontal angle in xz-plane (azimuth)
            - theta: vertical angle from y-axis (polar angle)
        """
        # vector from target to camera
        direction = Vector3(
            self.position.x - self.target.x,
            self.position.y - self.target.y, 
            self.position.z - self.target.z
        )
        
        # calculate spherical coordinates
        radius = math.sqrt(direction.x**2 + direction.y**2 + direction.z**2)
        phi = math.atan2(direction.z, direction.x)  # horizontal angle in xz-plane
        theta = math.acos(max(-1.0, min(1.0, direction.y / radius)))  # vertical angle from y-axis
        
        return radius, phi, theta
        
    def set_position_from_spherical(self, radius, phi, theta):
        """
        Set camera position using spherical coordinates relative to target
        """
        # convert spherical to Cartesian coordinates
        self.position = Vector3(
            self.target.x + radius * math.sin(theta) * math.cos(phi),
            self.target.y + radius * math.cos(theta),
            self.target.z + radius * math.sin(theta) * math.sin(phi)
        )
        
        # update camera matrices
        self._calculate_view_matrix()

    def rotate_around_target(self, horizontal_angle: float, vertical_angle: float):
        """
        Rotate camera around target point, maintaining distance
        horizontal_angle: change in azimuth angle (around y-axis)
        vertical_angle: change in polar angle (from y-axis)
        """
        # get current spherical coordinates
        radius, phi, theta = self.get_camera_spherical_coords()
        
        # apply rotation with smaller angle changes for more control
        horizontal_angle *= 0.2 
        vertical_angle *= 0.2
        
        # apply the scaled angles
        phi -= horizontal_angle
        theta += vertical_angle
        
        # clamp vertical angle to prevent camera flipping or gimbal lock
        theta = max(0.1, min(math.pi - 0.1, theta))
        
        self.set_position_from_spherical(radius, phi, theta)

    def orbit_horizontal(self, angle: float):
        """
        Orbits the camera horizontally around the target.
        Positive angle rotates camera clockwise around the target.
        """
        
        rel_pos = Vector3(
            self.position.x - self.target.x,
            self.position.y - self.target.y,
            self.position.z - self.target.z
        )
        
        # apply rotation matrix around Y axis
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        
        new_x = rel_pos.x * cos_angle + rel_pos.z * sin_angle
        new_z = -rel_pos.x * sin_angle + rel_pos.z * cos_angle
        
        # update position
        self.position = Vector3(
            self.target.x + new_x,
            self.position.y,
            self.target.z + new_z
        )
        
        # update view matrix
        self._calculate_view_matrix()

    def orbit_vertical(self, angle: float):
        """
        Orbits the camera vertically around the target.
        Positive angle rotates camera upward, negative downward.
        """
        
        angle *= 0.1
        
        # get current position in spherical coordinates
        rel_pos = Vector3(
            self.position.x - self.target.x,
            self.position.y - self.target.y,
            self.position.z - self.target.z
        )
        
        # current horizontal distance and height
        horizontal_dist = math.sqrt(rel_pos.x**2 + rel_pos.z**2)
        current_height = rel_pos.y
        
        # current vertical angle
        current_angle = math.atan2(current_height, horizontal_dist)
        
        # apply new angle with limits to prevent flipping
        new_angle = current_angle + angle
        new_angle = max(-math.pi/2 + 0.1, min(math.pi/2 - 0.1, new_angle))
        
        # current distance from target
        distance = math.sqrt(horizontal_dist**2 + current_height**2)
        
        # calculate new horizontal distance and height
        new_horizontal_dist = distance * math.cos(new_angle)
        new_height = distance * math.sin(new_angle)
        
        # calculate new position
        if horizontal_dist > 0.001:
            scale_factor = new_horizontal_dist / horizontal_dist
            new_x = self.target.x + rel_pos.x * scale_factor
            new_z = self.target.z + rel_pos.z * scale_factor
        else:
            new_x = self.target.x + new_horizontal_dist
            new_z = self.target.z
            
        new_y = self.target.y + new_height
        
        self.position = Vector3(new_x, new_y, new_z)
        self._calculate_view_matrix()