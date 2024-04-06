import pygame
import random
import math

class Asteroid:
  def __init__(self, x, y, size, screen, angle=None, speed=None):
    self.x = x
    self.y = y
    self.size = size
    self.screen = screen
    self.angle = angle if angle is not None else random.uniform(0, 2 * math.pi)
    self.speed = speed if speed is not None else random.uniform(1, 3)
    self.color = (100, 100, 100)
    self.radius = {"large": 60, "medium": 40, "small": 20}[self.size]
    self.marked_for_removal = False

  def update(self):
    self.x += math.cos(self.angle) * self.speed
    self.y += math.sin(self.angle) * self.speed
    if (self.x < -100 or self.x > self.screen.get_width() + 100 or
        self.y < -100 or self.y > self.screen.get_height() + 100):
      self.marked_for_removal = True

  def draw(self):
    pygame.draw.circle(self.screen, self.color, 
                       (int(self.x), int(self.y)), self.radius)
  