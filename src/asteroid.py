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
    self.spin_angle = random.uniform(0, 360)
    self.spin_speed = random.uniform(-3, 3)
    self.radius = {"large": 60, "medium": 40, "small": 20}[self.size]
    self.marked_for_removal = False
    self.image_original = pygame.image.load(f'assets/images/asteroid/asteroid.png').convert_alpha()
    self.image_original = pygame.transform.scale(self.image_original, (self.radius*2, self.radius*2))
    self.image = self.image_original
    self.rect = self.image.get_rect(center=(self.x, self.y))

  def update(self):
    self.x += math.cos(self.angle) * self.speed
    self.y += math.sin(self.angle) * self.speed

    self.spin_angle = (self.spin_angle + self.spin_speed) % 360
    self.image = pygame.transform.rotate(self.image_original, -self.spin_angle)
    self.rect = self.image.get_rect(center=(self.x, self.y))

    if (self.x < -100 or self.x > self.screen.get_width() + 100 or
        self.y < -100 or self.y > self.screen.get_height() + 100):
      self.marked_for_removal = True

  def draw(self):
    self.screen.blit(self.image, self.rect.topleft)
  