import turtle, sys
import src.globals as GLOBALS
from random import choice
from src.classes.asset_loader import AssetLoader
from src.classes.camera_persp import Camera
from src.classes.render_turtle import RenderTurtle
from src.classes.snake import Snake
from src.classes.helpers.obj import OBJ
from src.classes.wcv import world_coordinate_vectors

from src.classes.helpers.vectors import Vector3


class GameObject:
    """
    Main game object container.
    """
    def __init__(self):
        self.asset_loader = AssetLoader()
        self.turtle = RenderTurtle()
        self.ui = None
        self.selected_button = 0

        self.logo_static = self.asset_loader.LOGO_STATIC
        self.logo_static.turtle = self.turtle
        self.logo_static.world_position = Vector3(0,4,0)
        
        self.logo_dynamic = self.asset_loader.LOGO_DYNAMIC
        self.logo_dynamic.turtle = self.turtle
        self.logo_dynamic.world_position = Vector3(0,4,0)
        
        self.game_running = False
        self.dead = False

        center = GLOBALS.GRID_DIMENSIONS // GLOBALS.GRID_SIZE
        self.center = Vector3(center, center, center)
        
        self.camera = Camera(position=Vector3(69, 69, 69))
        self.setup_camera_start()

        self.snake = Snake(self.turtle, self.center)
        
        self.world = OBJ()
        

    def init(self):
        self.setup_camera_game()
        self.game_running = True
        self.move_snake()
        self.spawn_food()
        
    def restart(self):
        GLOBALS.SCORE = 0
        GLOBALS.MOVE_QUEUED = False
        
        self.dead = False
        self.snake = Snake(self.turtle, self.center)
        self.input_handler.snake = self.snake
        self.init()
        
    
    def spawn_food(self):
        if len(GLOBALS.FOODS) < 3:
            food = AssetLoader.FOOD.copy()
            food.turtle = self.turtle
            food.world_position = Vector3(
                choice(list(range(2, GLOBALS.GRID_DIMENSIONS - 2, 2))),
                choice(list(range(2, GLOBALS.GRID_DIMENSIONS - 2, 2))),
                choice(list(range(2, GLOBALS.GRID_DIMENSIONS - 2, 2))),
            )
            GLOBALS.FOODS.append(food)
        turtle.ontimer(self.spawn_food, 3000)

    def update_food(self):
        if GLOBALS.FOODS:
            for food in GLOBALS.FOODS:
                food.rotate(GLOBALS.FOOD_ROTATION)
    
    def draw_foods(self):
        for food in GLOBALS.FOODS:
            food.draw(self.camera)

    def draw_world(self):
        self.turtle.pencolor(GLOBALS.TRACER_COLOR)
        for edge in world_coordinate_vectors:
            v1 = Vector3(edge[0][0], edge[0][1], edge[0][2])
            v2 = Vector3(edge[1][0], edge[1][1], edge[1][2])

            v1_trans = self.world.get_transformed_vertex(v1)
            v2_trans = self.world.get_transformed_vertex(v2)

            v1_proj = self.camera.project_point(v1_trans)
            v2_proj = self.camera.project_point(v2_trans)

            self.turtle.teleport(
                -GLOBALS.SCREEN_WIDTH // 2 + v1_proj.x,
                -GLOBALS.SCREEN_HEIGHT // 2 + v1_proj.y,
            )
            self.turtle.goto(
                -GLOBALS.SCREEN_WIDTH // 2 + v2_proj.x,
                -GLOBALS.SCREEN_HEIGHT // 2 + v2_proj.y,
            )

    def draw_nav_grid(self):
        nav_grid = [
            [
                [0, self.snake.head.world_position.y, 0],
                [0, self.snake.head.world_position.y, GLOBALS.GRID_DIMENSIONS],
            ],
            [
                [0, self.snake.head.world_position.y, 0],
                [GLOBALS.GRID_DIMENSIONS, self.snake.head.world_position.y, 0],
            ],
            [
                [0, self.snake.head.world_position.y, GLOBALS.GRID_DIMENSIONS],
                [
                    GLOBALS.GRID_DIMENSIONS,
                    self.snake.head.world_position.y,
                    GLOBALS.GRID_DIMENSIONS,
                ],
            ],
            [
                [GLOBALS.GRID_DIMENSIONS, self.snake.head.world_position.y, 0],
                [
                    GLOBALS.GRID_DIMENSIONS,
                    self.snake.head.world_position.y,
                    GLOBALS.GRID_DIMENSIONS,
                ],
            ],
        ]

        self.turtle.pencolor(GLOBALS.GRID_COLOR)
        
        for edge in nav_grid:
            v1 = Vector3(edge[0][0], edge[0][1], edge[0][2])
            v2 = Vector3(edge[1][0], edge[1][1], edge[1][2])

            v1_trans = self.world.get_transformed_vertex(v1)
            v2_trans = self.world.get_transformed_vertex(v2)

            v1_proj = self.camera.project_point(v1_trans)
            v2_proj = self.camera.project_point(v2_trans)

            self.turtle.teleport(
                -GLOBALS.SCREEN_WIDTH // 2 + v1_proj.x, -GLOBALS.SCREEN_HEIGHT // 2 + v1_proj.y
            )
            self.turtle.goto(
                -GLOBALS.SCREEN_WIDTH // 2 + v2_proj.x, -GLOBALS.SCREEN_HEIGHT // 2 + v2_proj.y
            )

        pole_v1 = self.snake.head.world_position
        pole_v2 = Vector3(pole_v1.x, GLOBALS.GRID_DIMENSIONS // 2, pole_v1.z)

        v1_trans = self.world.get_transformed_vertex(pole_v1)
        v2_trans = self.world.get_transformed_vertex(pole_v2)

        v1_proj = self.camera.project_point(v1_trans)
        v2_proj = self.camera.project_point(v2_trans)

        self.turtle.teleport(
            -GLOBALS.SCREEN_WIDTH // 2 + v1_proj.x,
            -GLOBALS.SCREEN_HEIGHT // 2 + v1_proj.y,
        )
        self.turtle.goto(
            -GLOBALS.SCREEN_WIDTH // 2 + v2_proj.x,
            -GLOBALS.SCREEN_HEIGHT // 2 + v2_proj.y,
        )

        for food in GLOBALS.FOODS:
            pole_v1 = food.world_position
            pole_v2 = Vector3(pole_v1.x, self.snake.head.world_position.y, pole_v1.z)

            v1_trans = self.world.get_transformed_vertex(pole_v1)
            v2_trans = self.world.get_transformed_vertex(pole_v2)

            v1_proj = self.camera.project_point(v1_trans)
            v2_proj = self.camera.project_point(v2_trans)

            self.turtle.teleport(
                -GLOBALS.SCREEN_WIDTH // 2 + v1_proj.x,
                -GLOBALS.SCREEN_HEIGHT // 2 + v1_proj.y,
            )
            self.turtle.goto(
                -GLOBALS.SCREEN_WIDTH // 2 + v2_proj.x,
                -GLOBALS.SCREEN_HEIGHT // 2 + v2_proj.y,
            )

    def update_and_render(self):
        self.turtle.clear()
        if not self.dead and not self.game_running:
            self.update_logo()
            self.draw_start_screen()
        elif not self.dead and self.game_running:
            self.update_food()
            self.draw_everything()
        elif self.dead:
            self.draw_game_over()
            
        turtle.ontimer(self.update_and_render, 16)
    
    def draw_everything(self):
        self.draw_world()
        self.draw_nav_grid()
        self.snake.draw_snake(self.camera)
        self.draw_foods()
        self.draw_score()

    def move_snake(self):
        if not self.snake.move():
            self.draw_everything()
            self.game_over()
            return
        GLOBALS.MOVE_QUEUED = False
        if not self.dead:
            turtle.ontimer(self.move_snake, 1000)

    def draw_start_screen(self):
        self.draw_logo()
        self.draw_ui()
        self.turtle.teleport(0, GLOBALS.SCREEN_HEIGHT // 2 - 100)
        self.turtle.write("SNAKE^3", align="center", font=("Arial", 40, "bold"))
        self.turtle.teleport(0, -200)
        self.turtle.write(
            "Snake Controls: WASD\nCamera Move: Arrow Buttons\nCamera Zoom: Num+/Num-\nCamera Rotation: Q/E", 
            align="center", 
            font=("Arial", 20, "normal")
        )
        
    def game_over(self):
        self.dead = True
        self.game_running = False
        
    def draw_game_over(self):
        self.turtle.teleport(0, 0)
        self.turtle.write("GAME OVER", align="center", font=("Arial", 40, "bold"))
        self.turtle.teleport(0, -50)
        self.turtle.write(f"SCORE: {GLOBALS.SCORE}", align="center", font=("Arial", 34, "bold"))
        self.turtle.teleport(0, -100)
        self.turtle.write("PRESS SPACE TO RESTART", align="center", font=("Arial", 20, "normal"))

    def draw_score(self):
        self.turtle.teleport(-GLOBALS.SCREEN_WIDTH // 2 + 100, GLOBALS.SCREEN_WIDTH // 2 - 100)
        self.turtle.write(f"SCORE: {GLOBALS.SCORE}", align="left", font=("Arial", 20, "bold"))

    def draw_logo(self):
        self.turtle.pencolor(GLOBALS.TRACER_COLOR)
        self.logo_dynamic.draw(self.camera)
        self.logo_static.draw(self.camera)

    def update_logo(self):
        self.logo_dynamic.rotate(Vector3(0, -1, 0))

    def setup_camera_start(self):
        self.camera.look_at(Vector3(0,0,0))
        # self.camera.move_y(10)
        self.camera.set_zoom(3)

    def setup_camera_game(self):
        # self.camera.position=Vector3(69, 69, 69)
        self.camera.look_at(self.center)
        self.camera.set_zoom(1.8)
        # self.camera.move_y(5)
        
    def draw_ui(self):
        self.ui.draw(self.selected_button)
        
    def exit_game(self):
        turtle.bye()
        sys.exit()