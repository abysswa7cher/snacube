import turtle
from src.classes.game_object import GameObject
from src.classes.ui import UI
from src.classes.input_handler import InputHandler

def main():
    game = GameObject()
    game.ui = UI(game, game.turtle).init()
    
    input_handler = InputHandler(game)
    game.input_handler = input_handler
    
    game.update_and_render()
    turtle.mainloop()
    

if __name__ == "__main__":
    main()  
