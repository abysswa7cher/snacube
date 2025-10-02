import turtle
from turtle import Turtle
from src.globals import SCREEN_WIDTH, SCREEN_HEIGHT, TRACER_COLOR


class RenderTurtle(Turtle):
    """
    Helper class for initialization of the Turtle drawing.
    """
    def __init__(self):
        super().__init__()

        turtle.Screen().setup(SCREEN_WIDTH, SCREEN_HEIGHT)
        turtle.Screen().screensize(SCREEN_WIDTH, SCREEN_HEIGHT, "#000")
        turtle.tracer(0)
        turtle.hideturtle()
        turtle.colormode(255)

        self.speed(0)
        self.color(TRACER_COLOR)
