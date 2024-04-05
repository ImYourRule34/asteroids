import pygame
import math
import settings

class Player: 
  def __init__(self, x, y, screen):
    self.x = x
    self.y = y
    self.screen = screen
    self.angle = 0
    self.speed = 0
    self.rotation_speed = 5
    self.color = settings.WHITE
    self.size = 20
    self.max_speed = 5
    self.decel = .99

  def update(self):
    self.speed *= self.decel

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
    self.angle %= 360
    print(f"Rotating left: {self.angle}")

  def rotate_right(self):
    self.angle += self.rotation_speed
    self.angle %= 360
    print(f"Rotating right: {self.angle}")

  def accelerate(self):
    self.speed += 0.1
    self.speed = min(self.speed, self.max_speed)
    print(f"Accelerating: {self.speed}")

  def shoot(self, bullets_list):
    if len(bullets_list) < 20:
        reusable_bullet = next((b for b in bullets_list if not b.is_alive()), None)
        if reusable_bullet:
            reusable_bullet.reset(self.x, self.y, math.radians(self.angle))
        else:
            bullet_x = self.x + math.cos(math.radians(self.angle)) * self.size
            bullet_y = self.y + math.sin(math.radians(self.angle)) * self.size
            bullet_angle = math.radians(self.angle)
            bullet_speed = 10
            bullet_color = settings.RED

            from bullet import Bullet
            bullets_list.append(Bullet(bullet_x, bullet_y, bullet_angle,
                                       bullet_color, bullet_speed, self.screen))
