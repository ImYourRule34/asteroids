import pygame
from game import Game

def main():
    pygame.init()
    pygame.mixer.init()
    game = Game()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()