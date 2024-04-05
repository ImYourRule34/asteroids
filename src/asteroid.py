import pygame
import random
import math

class Asteroid:
  def __init__(self, x, y, size, screen):
    self.x = x
    self.y = y
    self.size = size
    self.screen = screen
    self.angle = random.uniform(0, 2 * math.pi)
    self.speed = random.uniform(1, 3)
    self.color = (100, 100, 100)
    self.radius = self.size * 20

  def update(self):
    self.x += math.cos(self.angle) * self.speed
    self.y += math.sin(self.angle) * self.speed
    self.x %= self.screen.get_width()
    self.y %= self.screen.get_height()

  def draw(self):
    pygame.draw.circle(self.screen, self.color, 
                       (int(self.x), int(self.y)), self.radius)
  