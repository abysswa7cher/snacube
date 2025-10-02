import turtle
import src.globals as GLOBALS
from PIL import ImageFont
from src.classes.helpers.vectors import Vector2
from typing import Tuple

class Button:
    def __init__(self, turtle: turtle.Turtle, text: str, size: Vector2, position: Vector2, font:Tuple[str, int, str], button_color: str = None, text_color: str = None, callback: callable=None):
        """UI Button class.

        Args:
            turtle (turtle.Turtle): turtle instance for drawing.
            text (str): Button text.
            size (Vector2): Size (width, height).
            position (Vector2): Position (top-left corner).
            font (Tuple[str, int, str]): Font settings.
            button_color (str, optional): Button color.. Defaults to None.
            text_color (str, optional): Text color.. Defaults to None.
            callback (callable, optional): Button callback function. Defaults to None.
        """
        
        self.turtle = turtle
        self.text = text
        self.font = font
        self.size = size
        self.position = position
        self.button_color = button_color if button_color else GLOBALS.TRACER_COLOR
        self.text_color = text_color if text_color else GLOBALS.TRACER_COLOR
        self.inverted_color = self.invert_color(self.button_color)
        self.callback = callback

        font = ImageFont.truetype(self.font[0].lower()+".ttf", self.font[1])
        font_box = font.getbbox(self.text)
        self.text_width = font_box[2] - font_box[0]
        self.text_height = font_box[3] - font_box[1]
    
    def draw(self, selected: bool=False) -> None:        
        left = -self.size.x // 2
        top = self.position.y
        right = -left
        bottom = top - self.size.y
        
        # draw the box
        if selected:
            self.turtle.fillcolor(self.inverted_color)
            self.turtle.begin_fill()
        else:
            self.turtle.pensize(3)
            
        self.turtle.teleport(left, top)
        self.turtle.goto(right, top)
        self.turtle.goto(right, bottom)
        self.turtle.goto(left, bottom)
        self.turtle.goto(left, top)
        
        if selected:
            self.turtle.end_fill()
        else:
            self.turtle.pensize(1)

        # calculate text position in screen space
        button_center = Vector2(right - self.size.x // 2, top - self.size.y // 2)
        
        if selected:
            self.turtle.pencolor(self.text_color)
        
        self.turtle.teleport(button_center.x, button_center.y - self.text_height)
        self.turtle.write(self.text, align="center", font=self.font)
    
    def invert_color(self, color: str) -> str:
        color = int(color[1:], 16)
        return "#"+hex((color & 0xff000000) | (~color & 0x00ffffff))[2:]