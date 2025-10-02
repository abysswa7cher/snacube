import turtle, math
import src.globals as GLOBALS
from src.classes.helpers.vectors import Vector3


class InputHandler:
    def __init__(self, game):
        self.game = game
        self.snake = game.snake
        self.camera = game.camera
        self.ui = game.ui
        
        self.ui_button_count = len(self.ui.start_screen_buttons) - 1
        turtle.onkey(self.on_escape, "Escape")
        
        turtle.onkey(self.on_w, "w")
        turtle.onkey(self.on_s, "s")
        turtle.onkey(self.on_a, "a")
        turtle.onkey(self.on_d, "d")
        turtle.onkey(self.on_space, "space")
        turtle.onkey(self.on_up, "Up")
        turtle.onkey(self.on_down, "Down")
        turtle.onkey(self.on_right, "Right")
        turtle.onkey(self.on_left, "Left")
        turtle.onkey(self.on_plus, "+")
        turtle.onkey(self.on_minus, "-")
        turtle.onkey(self.on_q, "q")
        turtle.onkey(self.on_e, "e")
        turtle.listen()
    
    def on_escape(self):
        if self.game.game_running:
            self.game.game_over()
    
    def on_space(self):
        if not self.game.game_running and not self.game.dead:
            self.ui.start_screen_buttons[self.game.selected_button].callback()
        if self.game.dead:
            self.game.restart()
    
    def change_direction(self, new_dir):
        if new_dir != self.snake.head.direction.negate():
            self.snake.head.direction = new_dir
            self.snake.head.update()
    
    def on_up(self):
        if self.game.game_running:
            self.camera.move_y(1)
        else:
            self.game.selected_button = max(0, self.game.selected_button - 1)
    def on_down(self):
        if self.game.game_running:
            self.camera.move_y(-1)
        else:
            self.game.selected_button = min(self.ui_button_count, self.game.selected_button + 1)
    def on_right(self):
        if self.game.game_running:
            self.camera.move_x(1)
    def on_left(self):
        if self.game.game_running:
            self.camera.move_x(-1)
    def on_plus(self):
        if self.game.game_running:
            self.camera.adjust_zoom(0.1)
    def on_minus(self):
        if self.game.game_running:
            self.camera.adjust_zoom(-0.1)
    def on_q(self):
        if self.game.game_running:
            self.camera.orbit_horizontal(math.pi / 12)
    def on_e(self):
        if self.game.game_running:
            self.camera.orbit_horizontal(-math.pi / 12)
        
    def on_w(self):
        if self.game.game_running:
            if not GLOBALS.MOVE_QUEUED:
                current = self.snake.head.direction
                if current.y == 0:
                    self.change_direction(Vector3(0, 1, 0))
                elif current.y > 0:
                    self.change_direction(Vector3(-1, 0, 0))
                elif current.y < 0:
                    self.change_direction(Vector3(1, 0, 0))
                GLOBALS.MOVE_QUEUED = True

    def on_s(self):
        if self.game.game_running:
            if not GLOBALS.MOVE_QUEUED:
                current = self.snake.head.direction
                if current.y == 0:
                    self.change_direction(Vector3(0, -1, 0))
                elif current.y > 0:
                    self.change_direction(Vector3(1, 0, 0))
                elif current.y < 0:
                    self.change_direction(Vector3(-1, 0, 0))
                GLOBALS.MOVE_QUEUED = True

    def on_a(self):
        if self.game.game_running:
            if not GLOBALS.MOVE_QUEUED:
                current = self.snake.head.direction

                if current.y == 0:
                    if current == Vector3(1, 0, 0):
                        self.change_direction(Vector3(0, 0, -1))
                    elif current == Vector3(0, 0, -1):
                        self.change_direction(Vector3(-1, 0, 0))
                    elif current == Vector3(-1, 0, 0):
                        self.change_direction(Vector3(0, 0, 1))
                    elif current == Vector3(0, 0, 1):
                        self.change_direction(Vector3(1, 0, 0))
                elif current.y > 0:
                    self.change_direction(Vector3(0, 0, 1))
                elif current.y < 0:
                    self.change_direction(Vector3(0, 0, -1))

                GLOBALS.MOVE_QUEUED = True

    def on_d(self):
        if self.game.game_running:
            if not GLOBALS.MOVE_QUEUED:
                current = self.snake.head.direction

                if current.y == 0:
                    if current == Vector3(1, 0, 0):
                        self.change_direction(Vector3(0, 0, 1))
                    elif current == Vector3(0, 0, 1):
                        self.change_direction(Vector3(-1, 0, 0))
                    elif current == Vector3(-1, 0, 0):
                        self.change_direction(Vector3(0, 0, -1))
                    elif current == Vector3(0, 0, -1):
                        self.change_direction(Vector3(1, 0, 0))
                elif current.y > 0:
                    self.change_direction(Vector3(0, 0, -1))
                elif current.y < 0:
                    self.change_direction(Vector3(0, 0, 1))
                GLOBALS.MOVE_QUEUED = True