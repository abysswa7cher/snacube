import os
from src.classes.helpers.vectors import Vector3

# helper file for global constants

CWD = os.getcwd()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 2
GRID_DIMENSIONS = 20
SNAKE_SPEED = 2
BACKGROUND_COLOR = "#000"
TRACER_COLOR = "#189900"
GRID_COLOR = "#189900"
SNAKE_HEAD_COLOR = "#1ABC9C"
SNAKE_BODY_COLOR = "#16A085"
FOOD_COLOR = "#E74C3C"

HEAD_MODEL = "head.obj"
BODY_MODEL = "body.obj"
BODY_HOLLOW = "body_hollow.obj"
BODY_LAST = "body_last.obj"
FOOD_MODEL = "food.obj"

SCORE = 0
FOODS = []

MOVE_QUEUED = False

FOOD_ROTATION = Vector3(0, 4, 0)

COLORS = []