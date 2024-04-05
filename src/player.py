import pygame
import math

class Player: 
  def __init__(self, x, y, screen):
    self.x = x
    self.y = y
    self.screen = screen
    self.angle = 0
    self.speed = 0
    self.rotation_speed = 5
    self.color = (255, 255, 255)
    self.size = 20

  def update(self):
    self.x += math.cos(math.radians(self.angle)) * self.speed
    self.y += math.sin(math.radians(self.angle)) * self.speed

    self.x %= self.screen.get_width()
    self.y %= self.screen.get_height()

  def draw(self):
    front = (self.x + math.cos(math.radians(self.angle)) * self.size,
             self.y + math.sin(math.radians(self.angle)) * self.size)
    back_left = (self.x + math.cos(math.radians(self.angle + 120)) * self.size, 
                 self.y + math.sin(math.radians(self.angle + 120)) * self.size)
    back_right = (self.x + math.cos(math.radians(self.angle - 120)) * self.size, 
                  self.y + math.sin(math.radians(self.angle - 120)) * self.size)
    pygame.draw.polygon(self.screen, self.color, [front, back_left, back_right])

  def rotate_left(self):
    self.angle -= self.rotation_speed
    if self.angle < 0:
      self.angle += 360

  def rotate_right(self):
    self.angle += self.rotation_speed
    if self.angle >= 360:
      self.angle -= 360

  def accelerate(self):
    self.speed += .1