import pygame
import sys


class Game:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, 
                                               self.screen_height))
        pygame.display.set_caption('Asteroids')
        self.bg_color = (0,0,0)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
              if event.type == pygame.QUIT:
                running = False
            self.screen.fill(self.bg_color)
            pygame.display.flip()
        pygame.quit()
        sys.exit()