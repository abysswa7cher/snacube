import src.globals as GLOBALS
from src.classes.body_part import BodyPart
from src.globals import HEAD_MODEL, BODY_MODEL, FOOD_MODEL, BODY_HOLLOW, BODY_LAST, CWD, SNAKE_HEAD_COLOR, SNAKE_BODY_COLOR, FOOD_COLOR, COLORS

class AssetLoader:
    """
    Helper class to load and hold the required assets on startup.
    """
    
    with open(f"{CWD}\\assets\\colors.txt") as f:
        GLOBALS.COLORS = [line.strip() for line in f.readlines()]
    
    LOGO_STATIC = BodyPart(turtle=None, path=f"{CWD}\\assets\\logo_static.obj")
    LOGO_DYNAMIC = BodyPart(turtle=None, path=f"{CWD}\\assets\\logo_dynamic.obj")
    
    HEAD_PART = BodyPart(turtle=None, color=SNAKE_HEAD_COLOR, path=f"{CWD}\\assets\\{HEAD_MODEL}")
    BODY_PART = BodyPart(turtle=None, color=SNAKE_BODY_COLOR, path=f"{CWD}\\assets\\{BODY_MODEL}")
    FOOD = BodyPart(turtle=None, color=FOOD_COLOR, path=f"{CWD}\\assets\\{FOOD_MODEL}")
    BODY_HOLLOW_PART = BodyPart(turtle=None, color=SNAKE_BODY_COLOR, path=f"{CWD}\\assets\\{BODY_HOLLOW}")
    BODY_LAST_PART = BodyPart(turtle=None, color=SNAKE_BODY_COLOR, path=f"{CWD}\\assets\\{BODY_LAST}")