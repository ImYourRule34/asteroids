import pygame
import player
import utils
import settings
from asteroid import Asteroid
import random
import math
from aux_ui import show_start_screen, show_game_over_screen
from score_manager import read_scores, write_scores
import aux_ui

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, 
                                               settings.SCREEN_HEIGHT))
        self.state = 'START'
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = player.Player(400, 300, self.screen)
        self.asteroids = []
        self.bullets = []
        self.current_wave = 1
        self.asteroids_in_wave = 3
        self.time_between_waves = 5000
        self.last_wave_time = pygame.time.get_ticks()
        self.score = 0
        self.lives = 3
        self.background = pygame.image.load('assets/images/background/space_background.png').convert()
        self.bg_x = 0
        self.bg_y = 0
        self.bg_move_speed = .05
        self.bg_max_move = 20
        self.bg_width = self.background.get_width()
        self.bg_height = self.background.get_height()


    def spawn_asteroids(self):
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            x = random.uniform(0, settings.SCREEN_WIDTH)
            y = -50
            angle = random.uniform(-math.pi / 2, math.pi / 2)
        elif edge == 'bottom':
            x = random.uniform(0, settings.SCREEN_WIDTH)
            y = settings.SCREEN_HEIGHT + 50
            angle = random.uniform(math.pi / 2, 3 * math.pi / 2)
        elif edge == 'left':
            x = -50
            y = random.uniform(0, settings.SCREEN_HEIGHT)
            angle = random.uniform(0, math.pi)
        elif edge == 'right':
            x = settings.SCREEN_WIDTH + 50
            y = random.uniform(0, settings.SCREEN_HEIGHT)
            angle = random.uniform(-math.pi, 0)

        size = random.choice(['large', 'medium', 'small'])
        speed = random.uniform(1, 3)

        new_asteroid = Asteroid(x, y, size, self.screen, angle, speed)
        self.asteroids.append(new_asteroid)

    def spawn_wave(self):
        for _ in range(self.asteroids_in_wave):
            self.spawn_asteroids()
        self.current_wave += 1
        self.asteroids_in_wave = min(5 + self.current_wave, 15)
        self.time_between_waves = max(5000, self.time_between_waves - 100)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot(self.bullets)
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), 
                                                       pygame.RESIZABLE)
                settings.SCREEN_WIDTH = event.w
                settings.SCREEN_HEIGHT = event.h
                    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.rotate_left()
        if keys[pygame.K_RIGHT]:
            self.player.rotate_right()
        if keys[pygame.K_UP]:
            self.player.accelerate()

    def run(self):
        while self.running:
            if self.state == 'START':
                top_scores = read_scores()
                show_start_screen(self.screen, top_scores)
                self.wait_for_input_start_screen()
                self.state = 'RUNNING'
            elif self.state == 'RUNNING':
                self.handle_events()
                self.update()
                self.draw()
                pygame.display.flip()
                self.clock.tick(120)
            elif self.state == 'FINISH':
                player_name = self.prompt_for_name()
                
                if player_name:
                    self.check_and_update_high_scores(self.score, player_name)
                show_game_over_screen(self.screen, self.score)
                self.wait_for_input_after_game_over()
                self.state = 'START'

    def prompt_for_name(self):
        self.screen.fill(settings.BLACK)
        aux_ui.draw_text(self.screen, "Game Over! Enter Your Name:", 
                         (settings.SCREEN_WIDTH // 2, 
                          settings.SCREEN_HEIGHT // 4), 32, 
                          pygame.Color('white'))

        input_box = pygame.Rect(settings.SCREEN_WIDTH // 4, 
                                settings.SCREEN_HEIGHT // 2, 
                                settings.SCREEN_WIDTH // 2, 50)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        font = pygame.font.Font(None, 32)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "" 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            return text 
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode 

            self.screen.fill(settings.BLACK) 
            aux_ui.draw_text(self.screen, "Game Over! Enter Your Name:", 
                             (settings.SCREEN_WIDTH // 2, 
                              settings.SCREEN_HEIGHT // 4), 32, 
                              pygame.Color('white'))

            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(self.screen, color, input_box, 2)

            pygame.display.flip()
            self.clock.tick(30)

    def wait_for_input_after_game_over(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.state = 'START'
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        waiting = False

    def check_and_update_high_scores(self, new_score, player_name):
        current_scores = read_scores() 
        current_scores = [(name, int(score)) for name, score in current_scores]
        
        if len(current_scores) < 5 or new_score > current_scores[-1][1]:
            current_scores.append((player_name, new_score))
            new_scores = sorted(current_scores, 
                                key=lambda x: x[1], reverse=True)[:5]
            write_scores(new_scores)


    def wait_for_input_start_screen(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    waiting = False

    def reset_game(self):
        self.asteroids.clear()
        self.bullets.clear()
        self.play = player.Player(400, 300, self.screen)
        self.score = 0
        self.current_wave = 1
        self.asteroids_in_wave = 3
        self.lives = 3
        self.last_wave_time = pygame.time.get_ticks()
        self.angle = 0
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_wave_time > self.time_between_waves:
            self.spawn_wave()
            self.last_wave_time = current_time

        if self.current_wave >= 35:
            self.asteroids_in_wave += 1
        elif self.current_wave > 30:
            self.asteroids_in_wave = 20
        elif self.current_wave > 23:
            self.asteroids_in_wave = 13
        elif self.current_wave > 15:
            self.asteroids_in_wave = 12
        elif self.current_wave > 12:
            self.asteroids_in_wave = 9
        elif self.current_wave > 9:
            self.asteroids_in_wave = 7
        elif self.asteroids_in_wave > 7:
            self.asteroids_in_wave = 6
        elif self.asteroids_in_wave > 5:
            self.asteroids_in_wave = 5

        self.player.update()
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_alive():
                self.bullets.remove(bullet)
            else:
                for asteroid in self.asteroids[:]:  
                    if utils.check_collision(bullet, asteroid):
                        self.handle_asteroid_destruction(asteroid)
                        bullet.alive = False
                        break
        
        for asteroid in self.asteroids[:]:
            asteroid.update()
            if utils.check_collision(self.player, asteroid):
                self.lives -= 1
                self.asteroids.remove(asteroid)
                if self.lives <= 0:
                    self.state = 'FINISH'
                    break

        self.asteroids = [a for a in self.asteroids if 
                          not getattr(a, 'marked_for_removal', False)]
    


    def handle_asteroid_destruction(self, asteroid):
        if asteroid.size == 'large':
            new_sizes = ['medium', 'medium']
        elif asteroid.size == 'medium':
            new_sizes = ['small', 'small', 'small']
        else:
            new_sizes = []
        
        angle_spread = math.pi / 3

        asteroid_points = {
            'large': 10,
            'medium': 15,
            'small': 20
        }
        self.score += asteroid_points.get(asteroid.size, 0)

        for size in new_sizes:
            new_angle_variation = random.uniform(-angle_spread, angle_spread)
            new_angle = asteroid.angle + new_angle_variation

            new_speed = asteroid.speed + random.uniform(0.5, 1.5)

            new_asteroid = Asteroid(asteroid.x, asteroid.y, size, self.screen, 
                                    new_angle, new_speed)
            self.asteroids.append(new_asteroid)

        self.asteroids.remove(asteroid)

    def update_background_position(self):
        target_x, target_y = 0, 0
        if self.player.accelerating:
            angle_rad = math.radians(self.player.angle)
            target_x = math.cos(angle_rad) * self.bg_max_move * -1  # Invert direction for opposite shift
            target_y = math.sin(angle_rad) * self.bg_max_move * -1

        self.bg_x += (target_x - self.bg_x) * self.bg_move_speed
        self.bg_y += (target_y - self.bg_y) * self.bg_move_speed

        self.bg_x = max(min(self.bg_x, self.bg_max_move), -self.bg_max_move)
        self.bg_y = max(min(self.bg_y, self.bg_max_move), -self.bg_max_move)

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.update_background_position()
        bg_pos = (self.bg_x - self.bg_max_move, self.bg_y - self.bg_max_move)
        self.screen.blit(self.background, bg_pos)

        self.player.draw()
        for bullet in self.bullets:
            bullet.draw()
        for asteroid in self.asteroids:
            asteroid.draw()
        self.draw_ui()
        
        pygame.display.flip()


    def draw_ui(self):
        ammo_count = 5 - len([b for b in self.bullets if b.is_alive()])
        dot_radius = 5
        dot_spacing = 15
        start_x = 10
        start_y = self.screen.get_height() - 40
        box_padding = 5
        
        box_width = ammo_count * dot_spacing + box_padding * 2
        box_height = dot_radius * 2 + box_padding * 2
        box_x = 12 + start_x - box_padding
        box_y = start_y - dot_radius - box_padding

        font = pygame.font.SysFont(None, 24)
        score_text = f"Score: {self.score}"
        lives_text = f"Lives: {self.lives}"
        score_surf = font.render(score_text, True, settings.WHITE)
        lives_surf = font.render(lives_text, True, settings.WHITE)
        self.screen.blit(score_surf, (10, 10))
        self.screen.blit(lives_surf, (10, 35))

        pygame.draw.rect(self.screen, settings.OFF_WHITE, 
                         pygame.Rect(box_x, box_y, box_width, box_height))
        for i in range(ammo_count):
            dot_x = 20 + start_x + i * dot_spacing
            pygame.draw.circle(self.screen, settings.RED, 
            (dot_x, start_y), dot_radius)