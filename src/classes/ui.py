import turtle, sys
from src.classes.button import Button
from src.classes.helpers.vectors import Vector2

class UI:
    FONT_SETTINGS = ("Arial", 16, "bold");
    
    def __init__(self, game, turtle: turtle.Turtle):
        self.turtle = turtle
        self.game = game
        self.button_size = Vector2(200, 40)
        self.start_screen_buttons = []
        self.pause_menu_buttons = []
        
    def init_start_screen(self):
        start = Button(self.turtle,
                    "START",
                    self.button_size,
                    Vector2(0, 60),
                    UI.FONT_SETTINGS,
                    callback=self.game.init
                )
        exit = Button(self.turtle,
                    "EXIT",
                    self.button_size,
                    Vector2(0, 15),
                    UI.FONT_SETTINGS,
                    callback=self.game.exit_game
                )
        self.start_screen_buttons.append(start)
        self.start_screen_buttons.append(exit)
        
    def init_pause_screen(self):
        yes = Button(self.turtle,
                    "YES",
                    self.button_size,
                    Vector2(0, 60),
                    UI.FONT_SETTINGS
                )
        no = Button(self.turtle,
                    "NO",
                    self.button_size,
                    Vector2(0, 60),
                    UI.FONT_SETTINGS
                )
    
    def init(self):
        self.init_start_screen()
        return self
    
    def draw(self, selection: int = 0):
        for i, button in enumerate(self.start_screen_buttons):
            if i == selection:
                button.draw(selected=True)
            else:
                button.draw()
