import pygame
import math

class Bullet:
  def __init__(self, x, y, angle, color, speed, screen):
    self.x = x
    self.y = y
    self.angle = angle
    self.color = color
    self.speed = speed
    self.screen = screen
    self.radius = 2
    self.alive = True
  
  def update(self):
    self.x += self.speed * math.cos(self.angle)
    self.y += self.speed * math.sin(self.angle)
    if (self.x <0 or self.x > self.screen.get_width() or 
        self.y < 0 or self.y > self.screen.get_height()):
      self.alive = False
    
  def draw(self):
    pygame.draw.circle(self.screen, self.color, 
                       (int(self.x), int(self.y)), 
                       self.radius)
    
  def reset(self, x, y, angle):
    self.x = x
    self.y = y
    self.angle = angle
    self.alive = True

  def is_alive(self):
    return self.alive