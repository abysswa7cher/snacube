from math import isclose
from src.classes.body_part import BodyPart
from src.classes.helpers.vectors import Vector3
from src.classes.asset_loader import AssetLoader

import src.globals as GLOBALS


class Snake:
    """
    Player class that holds the data and the behavior of the snake.
    """
    def __init__(self, turtle, position=None):
        self.turtle = turtle
        self.head = AssetLoader.HEAD_PART.copy()
        self.head.turtle = self.turtle

        if position is None:
            center = GLOBALS.GRID_DIMENSIONS // GLOBALS.GRID_SIZE
            self.head.world_position = Vector3(center, center, center)
        else:
            self.head.world_position = position

        self.head.direction = Vector3(0, 0, 1)
        self.head.update()

        self.body_parts = []
        self.trail_positions = [self.head.world_position.copy()]
        self.trail_directions = [self.head.direction.copy()]
        self.grow()

    def grow(self):
        new_part = AssetLoader.BODY_LAST_PART.copy()
        new_part.turtle = self.turtle

        if not self.body_parts:
            new_part.world_position = (
                self.head.world_position - self.head.direction.scale(GLOBALS.GRID_SIZE)
            )
        else:
            new_part.world_position = self.body_parts[
                len(self.body_parts) - 1
            ].world_position.copy()

        new_part.direction = (
            self.head.direction.copy() if not self.body_parts
            else self.body_parts[len(self.body_parts) - 1].direction.copy()
        )
        new_part.update()
        self.body_parts.append(new_part)
        self.update_body_parts()

    def update_body_parts(self):
        for i, body in enumerate(self.body_parts):
            if 0 <= i < len(self.body_parts) - 1:
                old = body.copy()
                new = AssetLoader.BODY_HOLLOW_PART.copy()
                new.direction = old.direction
                new.world_position = old.world_position
                new.world_rotation = old.world_rotation
                new.turtle = old.turtle
                self.body_parts[i] = new
    
    def move(self):
        self.trail_positions.insert(0, self.head.world_position.copy())
        self.trail_directions.insert(0, self.head.direction.copy())

        dxyz = self.head.direction.scale(GLOBALS.SNAKE_SPEED)
        new_pos = self.head.world_position + Vector3(
            round(dxyz.x, 1), round(dxyz.y, 1), round(dxyz.z, 1)
        )
        
        move_success = True

        if (
            isclose(new_pos.x, GLOBALS.GRID_DIMENSIONS, abs_tol=0.1)
            or isclose(
                new_pos.x, 0, abs_tol=0.1
            )
            or isclose(
                new_pos.y, GLOBALS.GRID_DIMENSIONS, abs_tol=0.1
            )
            or isclose(
                new_pos.y, 0, abs_tol=0.1
            )
            or isclose(
                new_pos.z, GLOBALS.GRID_DIMENSIONS, abs_tol=0.1
            )
            or isclose(
                new_pos.z, 0, abs_tol=0.1
            )
        ):
            move_success = False

        for body in self.body_parts:
            if body.world_position.isclose(new_pos):
                move_success = False
            
        self.head.world_position = new_pos
        
        for f, food in enumerate(GLOBALS.FOODS):
            if self.head.world_position.isclose(food.world_position):
                GLOBALS.FOODS.pop(f)
                GLOBALS.SCORE += 1000
                self.grow()

        self.head.update()

        while len(self.trail_positions) <= len(self.body_parts):
            last_pos = (
                self.trail_positions[-1].copy()
                if self.trail_positions
                else self.head.world_position.copy()
            )
            last_dir = (
                self.trail_directions[-1].copy()
                if self.trail_directions
                else self.head.direction.copy()
            )
            self.trail_positions.append(last_pos)
            self.trail_directions.append(last_dir)

        for i, part in enumerate(self.body_parts):
            part.world_position = self.trail_positions[i].copy()
            part.direction = self.trail_directions[i].copy()
            part.update()

        while len(self.trail_positions) > len(self.body_parts) + 1:
            self.trail_positions.pop()
            self.trail_directions.pop()
        return move_success

    def draw_snake(self, camera):
        self.head.draw(camera)
        for body_part in self.body_parts:
            body_part.draw(camera)