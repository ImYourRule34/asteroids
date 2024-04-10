import pygame
import math
import settings

class Player: 
  def __init__(self, x, y, screen):
    self.x = x
    self.y = y
    self.screen = screen
    self.angle = 0
    self.speed_x = 0
    self.speed_y = 0
    self.rotation_speed = 3
    self.color = settings.WHITE
    self.size = 20
    self.max_speed = 3
    self.decel = .99
    self.radius = 15
    self.acceleration_timer = 0
    self.accelerating = False
    self.current_thrust = 0
    self.images = [
            pygame.transform.rotozoom(
                pygame.image.load(f'assets/images/ship/ship_thrust_{i}.png').convert_alpha(), -90, 0.5
            ) for i in range(4)
        ]
    self.image = self.images[self.current_thrust]
    self.rect = self.image.get_rect(center=(x, y + 20))

  def update(self):
    self.speed_x *= self.decel
    self.speed_y *= self.decel

    self.x += self.speed_x
    self.y += self.speed_y


    wrap_margin = 50

    screen_width = self.screen.get_width()
    screen_height = self.screen.get_height()

    if self.x < -wrap_margin:
        self.x = screen_width + wrap_margin
    elif self.x > screen_width + wrap_margin:
        self.x = -wrap_margin

    if self.y < -wrap_margin:
        self.y = screen_height + wrap_margin
    elif self.y > screen_height + wrap_margin:
        self.y = -wrap_margin

    if self.accelerating:
        speed_ratio = math.sqrt(self.speed_x**2 + self.speed_y**2) / self.max_speed
        self.current_thrust = min(int(speed_ratio * 3), 3)
    else:
        self.current_thrust = 0

    self.rotate()
    self.rect.center = (self.x, self.y)

  def rotate(self):
     self.image = pygame.transform.rotate(self.images[self.current_thrust],
                                           -self.angle)
     self.rect = self.image.get_rect(center=self.rect.center)

  def draw(self):
    self.screen.blit(self.image, self.rect.topleft)

  def rotate_left(self):
    self.angle -= self.rotation_speed
    self.angle %= 360

  def rotate_right(self):
    self.angle += self.rotation_speed
    self.angle %= 360

  def accelerate(self):
      self.accelerating = True
      thrust_x = math.cos(math.radians(self.angle)) * 0.1
      thrust_y = math.sin(math.radians(self.angle)) * 0.1

      self.speed_x += thrust_x
      self.speed_y += thrust_y

      self.speed = math.sqrt(self.speed_x ** 2 + self.speed_y ** 2)

      if self.speed > self.max_speed:
          normalized_speed_x = self.speed_x / self.speed
          normalized_speed_y = self.speed_y / self.speed
          self.speed_x = normalized_speed_x * self.max_speed
          self.speed_y = normalized_speed_y * self.max_speed
          self.speed = self.max_speed

  def shoot(self, bullets_list):
    if len(bullets_list) < 5:
        reusable_bullet = next((b for b in bullets_list if not 
                                b.is_alive()), None)
        if reusable_bullet:
            reusable_bullet.reset(self.x, self.y, math.radians(self.angle))
        else:
            bullet_x = self.x + math.cos(math.radians(self.angle)) * self.size
            bullet_y = self.y + math.sin(math.radians(self.angle)) * self.size
            bullet_angle = math.radians(self.angle)
            bullet_speed = 4
            bullet_color = settings.RED

            from bullet import Bullet
            bullets_list.append(Bullet(bullet_x, bullet_y, bullet_angle,
                                       bullet_color, bullet_speed, self.screen))
